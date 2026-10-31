#!/usr/bin/env python3
"""Generate the per-platform files in dist/ from the canonical sources in prompt/.

Edit only prompt/system-prompt.md and prompt/knowledge/taxonomy.md, then run:

    python3 scripts/build.py          # regenerate dist/
    python3 scripts/build.py --check  # fail if dist/ is stale (used in CI)
"""

import argparse
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "prompt" / "system-prompt.md"
TAXONOMY = ROOT / "prompt" / "knowledge" / "taxonomy.md"
DIST = ROOT / "dist"

SKILL_NAME = "ai4sg-finder"
SKILL_DESCRIPTION = (
    "Diagnose an NGO or public-sector resource-allocation problem and recommend the "
    "appropriate AI-for-social-good approach (restless bandits, welfare ILP, security "
    "games, distributionally robust optimization, or matching markets). Use when someone "
    "wants help choosing an algorithm or ML method for allocating aid, staff time, "
    "patrols, supplies, or seats."
)

# Custom GPT instructions are capped at 8,000 characters.
GPT_INSTRUCTIONS_LIMIT = 8000

ATTACHED_REF = "The attached reference, **AI4SG Allocation Taxonomy**,"
SKILL_REF = "The reference file `references/taxonomy.md` (**AI4SG Allocation Taxonomy**)"


def strip_title(text: str) -> str:
    """Drop the leading H1, which is a file label rather than an instruction."""
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "".join(lines).lstrip("\n")


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

    all_in_one = f"{prompt.rstrip()}\n\n---\n\n{taxonomy}"

    skill_md = (
        f"---\nname: {SKILL_NAME}\ndescription: {SKILL_DESCRIPTION}\n---\n\n"
        + prompt.replace(ATTACHED_REF, SKILL_REF)
    )
    skill_files = {"SKILL.md": skill_md, "references/taxonomy.md": taxonomy}

    out = {
        "instructions.md": prompt,
        "taxonomy.md": taxonomy,
        "all-in-one.md": all_in_one,
        f"{SKILL_NAME}.zip": skill_zip(skill_files),
    }
    for name, content in skill_files.items():
        out[f"claude-skill/{SKILL_NAME}/{name}"] = content
    return {k: v.encode() if isinstance(v, str) else v for k, v in out.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify dist/ is up to date")
    args = parser.parse_args()

    outputs = render()

    if args.check:
        stale = [p for p, data in outputs.items()
                 if not (DIST / p).exists() or (DIST / p).read_bytes() != data]
        if stale:
            print("dist/ is out of date; run python3 scripts/build.py. Stale files:")
            print("\n".join(f"  dist/{p}" for p in stale))
            sys.exit(1)
        print("dist/ is up to date.")
        return

    for path, data in outputs.items():
        target = DIST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"wrote dist/{path}")
    print(f"instructions: {len(outputs['instructions.md'].decode())} / "
          f"{GPT_INSTRUCTIONS_LIMIT} characters")


if __name__ == "__main__":
    main()
