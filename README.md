# AI4SG Finder

An AI assistant that helps NGOs and public agencies choose the right **AI-for-social-good (AI4SG) allocation method** for a field problem. It interviews you one question at a time, classifies your problem into one of five mathematical archetypes, and writes a recommendation covering why the method fits, what goes wrong without it, how to deploy it on paper or in Excel, and what the published evidence says.

It is a system prompt plus a reference file, packaged so it runs in **Claude, ChatGPT, Gemini, Google AI Studio, and other browser-based assistants**, or through the Claude, OpenAI, and Gemini APIs.

## Why the method matters

Social-sector budgets almost never cover the need. In 2025, humanitarian appeals met only 35% of their funding target, the biggest funding gap in appeal history ([ALNAP, 2026](https://alnap.org/help-library/resources/sohs-2026/chapter-1-prioritisation-under-pressure/1-1-the-reality-of-funding-gaps/)). Every program is deciding who gets the call, the well, the patrol or the place, and those decisions are usually made with a ranked spreadsheet or a risk score.

The right method can do far better with the same budget, but "use AI" is not one thing. A prediction model tells you who is at risk; it doesn't tell you whom your visit will actually *help*, where poachers will move once you show up, or how to plan for a flood that looks nothing like the last one. Each of those is a different mathematical problem with its own tool, and most of these tools have already been tested in the field:

**1. Restless bandits: spend scarce contact time where it changes behavior.** *Which beneficiaries get a reminder call this week?* In ARMMAN's maternal-health program in India, a restless-bandit policy choosing which of about 23,000 enrolled mothers received a live call led to 32% fewer drops in engagement than standard care ([Google Research](https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/)).

**2. Welfare optimization: allocate permanent resources fairly, and prove it.** *Which villages get the new wells?* Integer programs with explicit fairness rules make allocations auditable. Panelot, a selection algorithm from Carnegie Mellon and Harvard researchers that evens out each volunteer's chance of being chosen, had been used to select more than 40 citizens' assemblies by 2021 ([Hertz Foundation](https://www.hertzfoundation.org/news/a-better-citizens-assembly-bailey-flanigan/)). A related approach, targeting with machine learning on phone data, cut the number of eligible poor people left out of Togo's emergency cash transfers by 4–21% compared with geographic targeting ([Aiken et al., Nature 2022](https://poverty-action.org/publication/machine-learning-and-phone-data-can-improve-targeting-humanitarian-aid)).

**3. Security games: patrol against adversaries who adapt.** *Where should rangers patrol when poachers move?* Randomized, game-theoretic schedules stay effective because they cannot be learned and avoided. In Uganda's Queen Elizabeth National Park, rangers who patrolled two rarely visited areas that the PAWS model flagged as high-risk found numerous snares and other signs of poaching ([IEEE Spectrum](https://spectrum.ieee.org/this-ai-hunts-poachers)); the same family of models has scheduled US Coast Guard patrols in Boston since 2011 ([AI Magazine](https://ojs.aaai.org/index.php/aimagazine/article/view/2401)).

**4. Robust optimization: prepare for disasters you can't forecast.** *Where should supplies wait before an unpredictable flood?* When there are only a handful of past events and getting it wrong costs lives, robust models plan against the bad cases instead of the average one. This is the least field-proven class: the evidence is mostly in models, including studies of the WFP-managed UN Humanitarian Response Depot network ([Stienen et al., Omega 2021](https://pure.uva.nl/ws/files/67452240/1_s2.0_S0305048321001031_main.pdf)). The assistant says so plainly.

**5. Matching markets: respect choice on both sides.** *How should students be assigned to schools when families and schools both have preferences?* When New York City redesigned its high-school admissions around deferred acceptance, the number of students assigned to a school they had not chosen fell from about 30,000 to about 3,000 in the first year ([Abdulkadiroğlu, Pathak & Roth, AER 2005](https://stanford.edu/~alroth/papers/nycAEAPP.pdf)). The National Kidney Registry's paired-exchange matching had facilitated more than 4,600 living-donor kidney transplants by 2021 ([Osbun et al., Am J Transplant](https://pmc.ncbi.nlm.nih.gov/articles/PMC8720056)).

Choosing the wrong class wastes money and can do harm: visits pile up on people who would have done fine anyway, patrols become predictable, or a placement scheme drives away the people it was meant to serve. Sometimes the honest answer is that a simple rule is enough, and the assistant will say that too.

See the [**worked cases**](docs/cases/) for six examples across health, water, conservation, disaster preparedness, youth employment and food security, one per class plus a "no model" case.

## Quick start

Pick your platform. Every file you need is in [`dist/`](dist/), and each [release](https://github.com/ashitpatel/ai4sgfinder/releases/latest) attaches the same files as downloads, so you don't need to clone the repository.

### Claude

**Claude Project** (claude.ai, any plan with Projects)
1. Create a Project named *AI4SG Finder*.
2. Paste [`dist/instructions.md`](dist/instructions.md) into **Project instructions**.
3. Upload [`dist/taxonomy.md`](dist/taxonomy.md) to **Project knowledge**.
4. Start a chat in the Project and describe your problem.

**Claude Skill** (claude.ai or Claude Desktop)
- **Settings → Capabilities → Skills → Upload skill**, and choose `ai4sg-finder.zip` from the [latest release](https://github.com/ashitpatel/ai4sgfinder/releases/latest) (also at [`dist/ai4sg-finder.zip`](dist/ai4sg-finder.zip)).

**Claude Code plugin**

This repository is also a Claude Code plugin marketplace. In Claude Code, run:
```
/plugin install ai4sg-finder --marketplace ashitpatel/ai4sgfinder
```
On versions of Claude Code without the one-step form, add the marketplace first:
```
/plugin marketplace add ashitpatel/ai4sgfinder
/plugin install ai4sg-finder@ai4sgfinder
```
Then type `/ai4sg-finder:finder`, or just ask Claude for help choosing an allocation method. Updates arrive through `/plugin` when a new version is released.

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
  claude-plugin/          Claude Code plugin (skill runs as /ai4sg-finder:finder)
.claude-plugin/           generated marketplace file that makes this repo installable
examples/                 API chat scripts for Claude, OpenAI, Gemini
scripts/build.py          regenerates dist/ and .claude-plugin/ from prompt/ and VERSION
VERSION, CHANGELOG.md     release version and notes
docs/cases/               six worked cases, one per outcome; also a manual test set
docs/original-draft.md    the first draft, kept for provenance
```

## Editing the prompt

Edit only the files under `prompt/` (and `VERSION` when releasing), then regenerate:

```bash
python3 scripts/build.py
```

`kickoff.md` is condensed by hand, so when you change the full prompt, update it to match. The build fails if the kickoff is missing any filter or recommendation heading from `system-prompt.md`, if it exceeds 4,000 characters, or if the instructions exceed the 8,000-character Custom GPT limit. After a substantive prompt change, run the [worked cases](docs/cases/README.md#using-the-cases) and check the results. CI runs `python3 scripts/build.py --check` and fails when the generated files were not regenerated after an edit.

## Releasing

1. Update [`VERSION`](VERSION) and add a matching `## <version> — <date>` section to [`CHANGELOG.md`](CHANGELOG.md).
2. Run `python3 scripts/build.py`. This writes the new version into the plugin manifest, which is how Claude Code users get the update.
3. Optionally run `claude plugin validate --strict .` to check the plugin and marketplace.
4. Commit, then tag and push:
   ```bash
   git tag v$(cat VERSION) && git push origin main --tags
   ```

The [release workflow](.github/workflows/release.yml) checks that the tag matches `VERSION` and that the generated files are current, then publishes a GitHub release with the changelog section as its notes and the `dist/` files attached.

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
