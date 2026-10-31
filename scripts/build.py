#!/usr/bin/env python3
"""Generate the per-platform files in dist/ and .claude-plugin/ from the sources in prompt/.

Edit only the files in prompt/ (system-prompt.md, knowledge/*.md, kickoff.md) and
VERSION, then run:

    python3 scripts/build.py          # regenerate dist/ and .claude-plugin/
    python3 scripts/build.py --check  # fail if any generated file is stale (used in CI)
"""

import argparse
import io
import json
import re
import sys
import urllib.parse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompt" / "system-prompt.md"
TAXONOMY = ROOT / "prompt" / "knowledge" / "taxonomy.md"
PLAYBOOK = ROOT / "prompt" / "knowledge" / "playbook.md"
KICKOFF = ROOT / "prompt" / "kickoff.md"
README = ROOT / "README.md"
VERSION = ROOT / "VERSION"

SKILL_NAME = "ai4sg-finder"
SKILL_DESCRIPTION = (
    "Diagnose an NGO or public-sector resource-allocation problem and recommend the "
    "appropriate AI-for-social-good approach (restless bandits, welfare ILP, security "
    "games, distributionally robust optimization, matching markets, participatory "
    "budgeting, effect-based targeting, or adaptive experiments). Use when someone "
    "wants help choosing an algorithm or ML method for allocating aid, staff time, "
    "patrols, supplies, seats, or a community budget."
)

# The Claude Code plugin names its skill "finder", so it runs as /ai4sg-finder:finder.
PLUGIN_SKILL_NAME = "finder"
MARKETPLACE_NAME = "ai4sgfinder"
AUTHOR = "Ashit Patel"
REPO_URL = "https://github.com/ashitpatel/ai4sgfinder"

# Custom GPT instructions are capped at 8,000 characters.
GPT_INSTRUCTIONS_LIMIT = 8000
# The kickoff is pasted as a chat message; stay under the tightest common input box.
KICKOFF_LIMIT = 4000

ATTACHED_REF = "The attached reference, **AI4SG Allocation Taxonomy**,"
SKILL_REF = "The reference file `references/taxonomy.md` (**AI4SG Allocation Taxonomy**)"
ATTACHED_PLAYBOOK = "The attached **AI4SG Implementation Playbook**"
SKILL_PLAYBOOK = "The reference file `references/playbook.md` (**AI4SG Implementation Playbook**)"


def strip_title(text: str) -> str:
    """Drop the leading H1, which is a file label rather than an instruction."""
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "".join(lines).lstrip("\n")


def check_kickoff(prompt: str, kickoff: str) -> None:
    """Fail if the kickoff is too long or has lost a filter or section of the full prompt."""
    if len(kickoff) > KICKOFF_LIMIT:
        sys.exit(f"error: kickoff is {len(kickoff)} characters; keep it under {KICKOFF_LIMIT}.")
    headings = re.findall(r"\*\*(FILTER \d — [^*]+?|THE [A-Z &]+[A-Z])\*\*", prompt)
    headings += re.findall(r"\*\*(OPERATIONAL REPORT CARD)\*\*", prompt)
    missing = [h for h in headings if f"**{h}**" not in kickoff]
    follow_ups = prompt.split("## After the recommendation", 1)[1].split("\n## ", 1)[0]
    missing += [f for f in re.findall(r"^\d\. (.+)$", follow_ups, re.M) if f not in kickoff]
    if missing:
        sys.exit(f"error: {KICKOFF.name} is out of sync with {PROMPT.name}; missing: "
                 + "; ".join(missing))


def skill_zip(files: dict[str, str]) -> bytes:
    """Zip the skill folder with fixed timestamps so the output is reproducible."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(files):
            info = zipfile.ZipInfo(f"{SKILL_NAME}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            zf.writestr(info, files[name])
    return buf.getvalue()


def render() -> dict[str, bytes]:
    prompt = strip_title(PROMPT.read_text())
    taxonomy = TAXONOMY.read_text()
    playbook = PLAYBOOK.read_text()

    if len(prompt) > GPT_INSTRUCTIONS_LIMIT:
        sys.exit(
            f"error: instructions are {len(prompt)} characters; "
            f"Custom GPTs accept at most {GPT_INSTRUCTIONS_LIMIT}."
        )
    for phrase in (ATTACHED_REF, ATTACHED_PLAYBOOK):
        if phrase not in prompt:
            sys.exit(f"error: expected the phrase {phrase!r} in {PROMPT.name}")

    kickoff = KICKOFF.read_text()
    check_kickoff(prompt, kickoff)

    all_in_one = f"{prompt.rstrip()}\n\n---\n\n{taxonomy.rstrip()}\n\n---\n\n{playbook}"

    version = VERSION.read_text().strip()
    skill_body = prompt.replace(ATTACHED_REF, SKILL_REF).replace(ATTACHED_PLAYBOOK, SKILL_PLAYBOOK)

    def skill_files(name: str) -> dict[str, str]:
        front = f"---\nname: {name}\ndescription: {SKILL_DESCRIPTION}\n---\n\n"
        return {
            "SKILL.md": front + skill_body,
            "references/taxonomy.md": taxonomy,
            "references/playbook.md": playbook,
        }

    plugin_manifest = {
        "name": SKILL_NAME,
        "version": version,
        "description": SKILL_DESCRIPTION,
        "author": {"name": AUTHOR},
        "homepage": REPO_URL,
        "repository": REPO_URL,
        "license": "Apache-2.0",
        "keywords": ["ai-for-social-good", "nonprofit", "optimization", "resource-allocation"],
    }
    marketplace = {
        "name": MARKETPLACE_NAME,
        "owner": {"name": AUTHOR},
        "description": "AI4SG Finder: choose the right AI-for-social-good allocation method.",
        "plugins": [{
            "name": SKILL_NAME,
            "source": "./dist/claude-plugin",
            "description": SKILL_DESCRIPTION,
        }],
    }

    readme = with_try_links(README.read_text(), kickoff)
    citation = CITATION_TEMPLATE.format(
        version=version, given=AUTHOR.split()[0], family=AUTHOR.split()[-1], repo=REPO_URL)

    out = {
        "CITATION.cff": citation,
        "README.md": readme,
        "dist/instructions.md": prompt,
        "dist/taxonomy.md": taxonomy,
        "dist/playbook.md": playbook,
        "dist/all-in-one.md": all_in_one,
        "dist/kickoff.md": kickoff,
        f"dist/{SKILL_NAME}.zip": skill_zip(skill_files(SKILL_NAME)),
        "dist/claude-plugin/.claude-plugin/plugin.json": as_json(plugin_manifest),
        ".claude-plugin/marketplace.json": as_json(marketplace),
    }
    for name, content in skill_files(SKILL_NAME).items():
        out[f"dist/claude-skill/{SKILL_NAME}/{name}"] = content
    for name, content in skill_files(PLUGIN_SKILL_NAME).items():
        out[f"dist/claude-plugin/skills/{PLUGIN_SKILL_NAME}/{name}"] = content
    return {k: v.encode() if isinstance(v, str) else v for k, v in out.items()}


CITATION_TEMPLATE = """\
# Generated by scripts/build.py from VERSION; edit the template there, not this file.
cff-version: 1.2.0
message: "If you use AI4SG Finder in your work, please cite it as below."
type: software
title: "AI4SG Finder"
abstract: >-
  An AI assistant that helps NGOs and public agencies choose the right
  AI-for-social-good allocation method (restless bandits, welfare
  optimization, security games, robust optimization, matching markets,
  participatory budgeting, effect-based targeting, or adaptive experiments)
  for a field problem, packaged for Claude, ChatGPT and Gemini.
authors:
  - family-names: "{family}"
    given-names: "{given}"
version: "{version}"
# Zenodo concept DOI: always resolves to the latest archived release.
doi: 10.5281/zenodo.23840133
license: Apache-2.0
repository-code: "{repo}"
url: "{repo}"
keywords:
  - ai-for-social-good
  - nonprofit
  - resource-allocation
  - operations-research
  - restless-bandits
  - security-games
  - robust-optimization
  - matching-markets
  - participatory-budgeting
  - policy-learning
"""


TRY_START = "<!-- try-links:start (generated by scripts/build.py from prompt/kickoff.md) -->"
TRY_END = "<!-- try-links:end -->"
# Each assistant opens a new chat with the kickoff prompt as the first message.
TRY_LINK_BASES = {
    "ChatGPT": "https://chatgpt.com/?q=",
    "Claude": "https://claude.ai/new?q=",
    "Google AI Mode": "https://www.google.com/search?udm=50&q=",
}


def with_try_links(readme: str, kickoff: str) -> str:
    """Replace the README's "Try it now" links with ones carrying the current kickoff prompt."""
    if TRY_START not in readme or TRY_END not in readme:
        sys.exit(f"error: README.md must contain the markers {TRY_START!r} and {TRY_END!r}")
    query = urllib.parse.quote(kickoff, safe="")
    links = " · ".join(f"**[Open in {name}]({base}{query})**" for name, base in TRY_LINK_BASES.items())
    before, rest = readme.split(TRY_START, 1)
    after = rest.split(TRY_END, 1)[1]
    return f"{before}{TRY_START}\n{links}\n{TRY_END}{after}"


def as_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify generated files are up to date")
    args = parser.parse_args()

    outputs = render()

    if args.check:
        stale = [p for p, data in outputs.items()
                 if not (ROOT / p).exists() or (ROOT / p).read_bytes() != data]
        if stale:
            print("Generated files are out of date; run python3 scripts/build.py. Stale files:")
            print("\n".join(f"  {p}" for p in stale))
            sys.exit(1)
        print("Generated files are up to date.")
        return

    for path, data in outputs.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"wrote {path}")
    print(f"instructions: {len(outputs['dist/instructions.md'].decode())} / "
          f"{GPT_INSTRUCTIONS_LIMIT} characters")
    print(f"kickoff: {len(outputs['dist/kickoff.md'].decode())} / {KICKOFF_LIMIT} characters")


if __name__ == "__main__":
    main()
