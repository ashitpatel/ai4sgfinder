# UX review

Status: 2026-11-22. Documentation fixes done; prompt changes in Section 3 proposed, not started.

A review of the experience for three kinds of user, from first contact to a useful result: NGO program staff, foundation program officers reviewing proposals, and technical partners and contributors. It drew on the README, the blog, the prompts and reference files, and 17 transcripts of the assistant from the test runs recorded in the other plans.

## 1. What works

- **It copes with answers out of order.** When a user skips ahead, it confirms its reading and moves on instead of repeating questions. When it has to assume an answer, it says so and asks the user to correct it.
- **Follow-ups are easy to reach.** Typing a number gets the follow-up, built from the user's own answers; the pantry case turns the brief into a note to the foundation.
- **It holds the line on "no model needed".** The food-pantry case reached it in every run.

## 2. Problems, by impact

| # | Problem | Who | Evidence | Fix | Done? |
|---|---|---|---|---|---|
| 1 | Funders who click the most visible links get the NGO interview, not a review | Funders | The one-click links carry only the kickoff, which has no funder flow; the warning sat at the end of a long paragraph | A "Which way to use it" table under the links, and a funder section in Quick start | **Docs done**; a kickoff line is proposed below |
| 2 | The recommendation is long (about 7,000–11,500 characters) and the next steps come last | NGO staff | Next steps started after 7,000–10,500 characters in most final answers; only some runs opened with a summary | Open with a short summary and the month's next steps; cap the length | Proposed |
| 3 | The required headings are jargon ("counterfactual audit warning", "operational report card"), and the body follows ("integer program", "leximin", "Thompson sampling") | NGO staff | System prompt and kickoff headings; transcripts | Plain headings, which are also shorter | Proposed |
| 4 | Full recommendations are sometimes given twice: a later answer brings another full reply | NGO staff | Several runs; partly caused by the test script, which keeps answering after the recommendation | "If a later answer changes the recommendation, restate only what changes"; make the test script answer what was asked | Proposed |
| 5 | Six to ten turns before anything useful, and some turns ask two questions | NGO staff | Transcripts | Say in the README how long a session takes; tighten "one question per turn" | **Docs done**; prompt wording proposed |
| 6 | Eight setup routes and no single place that says what each one gives up | Everyone | README | The comparison table; the corrected size of the all-in-one file (about 147,000 characters, not 107,000) | **Done** |
| 7 | The funder memo comes out in a monospace code block and runs about three pages | Funders | The playbook's memo template is in a code fence; outputs copy it, with hard line breaks that paste badly into email | Rewrite the template as headings and short paragraphs, with a word limit; "short memo", not "one-page" | Proposed (playbook only) |
| 8 | Funders aren't told what to include, so the request for their context varies | Funders | Runs where the risk appetite was missing | A paste template in the README and a funder conversation starter for the Custom GPT | **Done** |
| 9 | Stale counts ("sixteen cases") and a mixed group of cases | Everyone | README, cases index | Corrected counts; cases regrouped into interviews, tools that feed a decision, and funder reviews | **Done** |
| 10 | The reference files are written for the model, but users are sent to read them | NGO staff, funders | Taxonomy and playbook openings; Section 6 has grown large | A short "reading this yourself?" contents list at the top of each; consider splitting Section 6 | Proposed |

## 3. Proposed prompt changes

The system prompt is at 7,997 of 8,000 characters (the Custom GPT limit) and the kickoff at 3,989 of 4,000, so each addition needs an equal cut. Measure with `scripts/build.py`.

| Change | Adds | Pay for it by cutting |
|---|---|---|
| Plain recommendation headings, e.g. *What kind of problem this is*, *What goes wrong without it*, *How it runs on the ground*, *Where it has been used*, *What worked and what was hard*, *The simpler option* | Saves about 40 characters in each file | The build's check on headings (`scripts/build.py`, `check_kickoff`) must change with them, and the cases' "six headings" checks |
| Open with a three-line summary and the month's next steps; keep the answer to about 1,200 words | About 120 | "Tell users to check tools and partners are still active" (the playbook says it); "Tutorial figures are illustrations, not evidence" (tutorials aren't attached) |
| Restate only what a later answer changes | About 80 | "avoiding over-engineered tech and grounding advice in verifiable literature" in the opening line, which the rules below already cover |
| One question per turn, no sub-questions | A word swap | — |
| Kickoff: a short funder path (list what the proposal says per filter, ask for missing context, then a brief memo; never say whether to fund) | About 220 | The method names in brackets in the kickoff's class list; the reminder to check tools and partners |
| Scope line covering tools that feed a decision and AI that is the intervention, which Section 6 handles but the "stay in scope" line doesn't name | About 60 | From the savings above |

Structural options for the reference files, which have no length limit but are read by the model:
- **Split taxonomy Section 6.** Keep the input-layer table and checks as Section 6; move the parts on beneficiary scores, AI as the intervention and model-measured outcomes into a Section 7, *Beyond allocation*; move *Decisions near the twelve classes* next to the decision tree, where the assistant looks when classifying. Anchors used across the docs and cases would need updating.
- **Memo template as headings**, not a code block, with "under 600 words".

Every change in this section needs a rerun of the affected worked cases: at least 2, 6, 9 and 17–25, with Case 6 as the most sensitive.
