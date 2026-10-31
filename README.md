# AI4SG Finder

An AI assistant that helps NGOs and public agencies choose the right **AI-for-social-good (AI4SG) allocation method** for a field problem. It interviews you one question at a time, classifies your problem into one of five mathematical archetypes, and writes a recommendation covering why the method fits, what goes wrong without it, how to deploy it on paper or in Excel, and what the published evidence says.

It is a system prompt plus a reference file, packaged so it runs in **Claude, ChatGPT, Gemini, Google AI Studio, and other browser-based assistants**, or through the Claude, OpenAI, and Gemini APIs.

| # | Archetype | Typical problem |
|---|-----------|-----------------|
| 1 | Dynamic State Evolution (restless bandits) | Which beneficiaries get a reminder call this week? |
| 2 | Static Demographic Targeting (welfare ILP) | Which villages get the new wells, fairly and auditably? |
| 3 | Spatiotemporal Security (security games) | Where should rangers patrol when poachers adapt? |
| 4 | Robust Contingency Planning (DRO) | Where to pre-position supplies before an unpredictable flood? |
| 5 | Strategic Matching Markets (stable matching) | How to assign students to schools when both sides have preferences? |

The assistant may also conclude that you don't need an optimization model at all.

See [**worked cases**](docs/cases/) for six examples across health, water, conservation, disaster preparedness, youth employment and food security, one per class plus a "no model" case.

## Quick start

Pick your platform. Every file you need is in [`dist/`](dist/).

### Claude

**Claude Project** (claude.ai, any plan with Projects)
1. Create a Project named *AI4SG Finder*.
2. Paste [`dist/instructions.md`](dist/instructions.md) into **Project instructions**.
3. Upload [`dist/taxonomy.md`](dist/taxonomy.md) to **Project knowledge**.
4. Start a chat in the Project and describe your problem.

**Claude Skill** (claude.ai, Claude Desktop, or Claude Code)
- claude.ai / Desktop: **Settings → Capabilities → Skills → Upload skill**, and choose [`dist/ai4sg-finder.zip`](dist/ai4sg-finder.zip).
- Claude Code: copy the folder into your skills directory:
  ```bash
  cp -r dist/claude-skill/ai4sg-finder ~/.claude/skills/
  ```
  Then ask Claude for help choosing an allocation method, or type `/ai4sg-finder`.

### ChatGPT (Custom GPT)
1. In ChatGPT, open **Explore GPTs → Create → Configure**.
2. Paste [`dist/instructions.md`](dist/instructions.md) into **Instructions** (it is kept under the 8,000-character limit).
3. Under **Knowledge**, upload [`dist/taxonomy.md`](dist/taxonomy.md).
4. Suggested conversation starter: *"I run a program and need help deciding how to allocate a limited resource."*

### Gemini (Gem)
1. In Gemini, open **Gems → New Gem**.
2. Paste [`dist/instructions.md`](dist/instructions.md) into **Instructions**.
3. Under **Knowledge**, add [`dist/taxonomy.md`](dist/taxonomy.md).

### Google AI Studio
1. Open [aistudio.google.com](https://aistudio.google.com) and start a new chat prompt.
2. Paste [`dist/all-in-one.md`](dist/all-in-one.md) into **System instructions**. It contains the instructions and the reference together, so nothing needs uploading.
3. Pick a Gemini model, type a first message about your problem, and save the prompt so you can reopen or share it.

### Browser assistants with a custom-instructions field
Assistants such as Perplexity Spaces let you save instructions and attach files. Paste [`dist/instructions.md`](dist/instructions.md) as the instructions and upload [`dist/taxonomy.md`](dist/taxonomy.md) as a file. If there is no file upload, paste [`dist/all-in-one.md`](dist/all-in-one.md) as the instructions instead, provided the field accepts it (about 17,000 characters).

### Any browser assistant, no setup
For assistants with no place for custom instructions, such as Google AI Mode in Search, Gemini in Chrome, Microsoft Copilot, or a fresh chat in any app, paste [`dist/kickoff.md`](dist/kickoff.md) as your **first message**. It is a condensed version (under 4,000 characters, so it fits most chat boxes) that asks the assistant to take on the role and start the interview.

The kickoff is shorter than the full prompt and carries only the core verified references, so expect less detailed evidence sections. Assistants without saved instructions can also drift out of the role in a long chat; paste it again if that happens.

### APIs
Each script in [`examples/`](examples/) loads `dist/all-in-one.md` as the system prompt and runs a terminal chat.

```bash
pip install -r examples/requirements.txt
```

| Provider | Script | Key | Model override |
|----------|--------|-----|----------------|
| Anthropic | [`examples/claude_chat.py`](examples/claude_chat.py) | `ANTHROPIC_API_KEY` | `CLAUDE_MODEL` |
| OpenAI | [`examples/openai_chat.py`](examples/openai_chat.py) | `OPENAI_API_KEY` | `OPENAI_MODEL` |
| Google | [`examples/gemini_chat.py`](examples/gemini_chat.py) | `GEMINI_API_KEY` | `GEMINI_MODEL` |

```bash
python3 examples/claude_chat.py
```

## Repository layout

```
prompt/
  system-prompt.md        <- source of truth: the assistant's instructions
  knowledge/taxonomy.md   <- source of truth: archetypes, decision tree, citations
  kickoff.md              <- hand-condensed paste-in version of the prompt
dist/                     <- generated, ready to paste or upload (do not edit)
  instructions.md         system prompt for Projects, Custom GPTs, Gems
  taxonomy.md             knowledge file to upload alongside it
  all-in-one.md           both in one file, for APIs and Google AI Studio
  kickoff.md              first-message version for browser assistants
  claude-skill/           Claude Skill folder
  ai4sg-finder.zip        the same Skill, zipped for upload
examples/                 API chat scripts for Claude, OpenAI, Gemini
scripts/build.py          regenerates dist/ from prompt/
docs/cases/               six worked cases, one per outcome; also a manual test set
docs/original-draft.md    the first draft, kept for provenance
```

## Editing the prompt

Edit only the files under `prompt/`, then regenerate:

```bash
python3 scripts/build.py
```

`kickoff.md` is condensed by hand, so when you change the full prompt, update it to match. The build fails if the kickoff is missing any filter or recommendation heading from `system-prompt.md`, if it exceeds 4,000 characters, or if the instructions exceed the 8,000-character Custom GPT limit. After a substantive prompt change, run the [worked cases](docs/cases/README.md#using-the-cases) and check the results. CI runs `python3 scripts/build.py --check` and fails when `dist/` was not regenerated after an edit.

## How the assistant works

1. **Five diagnostic filters**, asked one per turn: the resource and its intent; who holds choice and preferences; whether the environment is passive or adversarial; tolerance for being wrong; and how often field staff can record data.
2. **A five-part recommendation**: the recommended class, a counterfactual warning (what fails with a naive ML model or spreadsheet), a field deployment pathway using paper grids or Excel, real deployment evidence, and a report card of successes, challenges, and unknowns, ending with next steps.
3. **Evidence integrity rules**: the assistant must not invent citations, must prefer the verified references in `taxonomy.md`, and must label anything uncertain as unverified.

## Changes from the original draft

The first draft ([`docs/original-draft.md`](docs/original-draft.md)) was restructured as follows.

- **Added a filter for choice and preferences.** None of the original four filters could identify Class 5 (matching markets), so the assistant could never reach it.
- **Resolved "exactly one question at a time."** Filter 1 asked three questions at once. Each filter is now one turn, with its numbered prompts treated as optional guidance.
- **Added a "no model needed" outcome**, in line with the goal of shielding NGOs from fragile tech stacks.
- **Tied data feasibility to the recommendation.** Restless bandits need repeated observations per person; if the field can't supply them, the assistant now says so.
- **Added evidence integrity rules.** The draft asked for "documented deployments" and "literature tracking data" without guarding against fabricated citations, which language models produce readily.
- **Corrected the deployment examples.** Several attributions in the original taxonomy could not be verified or were misattributed. They are listed under *Unverified claims* in [`taxonomy.md`](prompt/knowledge/taxonomy.md), and the assistant is told not to cite them as fact. Verified references were added for each class.
- **Renamed Class 4** from "Robust Contingency Matching" to "Robust Contingency Planning," since it is not a matching method.

## Limitations

- The assistant recommends an *approach*; it does not build the model. Implementation still needs an operations-research or ML practitioner.
- Language models can still state inaccurate facts despite the integrity rules. Check every citation against its primary source before using it in a proposal or publication.
- The verified reference list reflects published work as of 2026 and is not exhaustive. Contributions with full citations are welcome.

## License

[Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution.
