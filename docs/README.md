# Docs

Everything here explains, tests or records the assistant. The assistant itself lives in [`prompt/`](../prompt/): the system prompt and its two reference files, the [taxonomy](../prompt/knowledge/taxonomy.md) and the [playbook](../prompt/knowledge/playbook.md).

## Guides

| Document | For | What it is |
|---|---|---|
| [Worked cases](cases/README.md) | Anyone learning the method; contributors testing a change | 25 cases: interviews, tools that feed a decision, and funder reviews, each with what a good answer contains. Also the test set |
| [Replay kit](../tools/replay-kit/README.md) | NGO staff with Excel; partners | Three workbooks that test a simple rule against current practice and a model on a program's own past records, a monthly health check for a tool in use, and a cost-of-ownership worksheet |
| [Tutorials](tutorials/README.md) | Readers with basic statistics | How each method works, step by step, with runnable code |
| [Where it fits](landscape.md) | Funders, partners | How the project compares with fourteen AI-for-good organizations |
| [Scanning the field](scanning.md) | Maintainers | The quarterly recipe for finding AI-for-good work the project doesn't cover |
| [Building from scratch](building-from-scratch.md) | Anyone building something similar | The prompts that recreate a project like this one |
| [Original draft](original-draft.md) | The curious | The first draft of the prompt, kept for provenance |

## Records

[`plans/`](plans/) holds dated records of larger changes: what was found, what changed and how it was tested. They are kept as written, except for their status lines.

| Record | Date | Status |
|---|---|---|
| [Input layers and a fairness audit](plans/input-layers-and-fairness-audit.md) | 2026-11-22 | Done; released in 1.4.0 |
| [Expanded scan](plans/expanded-scan.md) | 2026-11-22 | Done; most changes released in 1.4.0, the third pass in 1.5.0 |
| [UX review](plans/ux-review.md) | 2026-11-22 | Done; released in 1.5.0 |
| [Reference setups](plans/reference-setups.md) | 2026-11-23 | Done; in the next release |
