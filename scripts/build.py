#!/usr/bin/env python3
"""Generate the per-platform files in dist/ and .claude-plugin/ from the sources in prompt/.

Edit only the files in prompt/ (system-prompt.md, knowledge/taxonomy.md, kickoff.md) and
VERSION, then run:

    python3 scripts/build.py          # regenerate dist/ and .claude-plugin/
    python3 scripts/build.py --check  # fail if any generated file is stale (used in CI)
"""

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompt" / "system-prompt.md"
TAXONOMY = ROOT / "prompt" / "knowledge" / "taxonomy.md"
KICKOFF = ROOT / "prompt" / "kickoff.md"
VERSION = ROOT / "VERSION"

SKILL_NAME = "ai4sg-finder"
SKILL_DESCRIPTION = (
    "Diagnose an NGO or public-sector resource-allocation problem and recommend the "
    "appropriate AI-for-social-good approach (restless bandits, welfare ILP, security "
    "games, distributionally robust optimization, or matching markets). Use when someone "
    "wants help choosing an algorithm or ML method for allocating aid, staff time, "
    "patrols, supplies, or seats."
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

    if len(prompt) > GPT_INSTRUCTIONS_LIMIT:
        sys.exit(
            f"error: instructions are {len(prompt)} characters; "
            f"Custom GPTs accept at most {GPT_INSTRUCTIONS_LIMIT}."
        )
    if ATTACHED_REF not in prompt:
        sys.exit(f"error: expected the phrase {ATTACHED_REF!r} in {PROMPT.name}")

    kickoff = KICKOFF.read_text()
    check_kickoff(prompt, kickoff)

    all_in_one = f"{prompt.rstrip()}\n\n---\n\n{taxonomy}"

    version = VERSION.read_text().strip()
    skill_body = prompt.replace(ATTACHED_REF, SKILL_REF)

    def skill_files(name: str) -> dict[str, str]:
        front = f"---\nname: {name}\ndescription: {SKILL_DESCRIPTION}\n---\n\n"
        return {"SKILL.md": front + skill_body, "references/taxonomy.md": taxonomy}

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

    out = {
        "dist/instructions.md": prompt,
        "dist/taxonomy.md": taxonomy,
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
