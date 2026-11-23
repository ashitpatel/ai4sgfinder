# UX review

Status: 2026-11-22. Documentation fixes and the prompt changes in Section 3 done; results in Section 4.

A review of the experience for three kinds of user, from first contact to a useful result: NGO program staff, foundation program officers reviewing proposals, and technical partners and contributors. It drew on the README, the blog, the prompts and reference files, and 17 transcripts of the assistant from the test runs recorded in the other plans.

## 1. What works

- **It copes with answers out of order.** When a user skips ahead, it confirms its reading and moves on instead of repeating questions. When it has to assume an answer, it says so and asks the user to correct it.
- **Follow-ups are easy to reach.** Typing a number gets the follow-up, built from the user's own answers; the pantry case turns the brief into a note to the foundation.
- **It holds the line on "no model needed".** The food-pantry case reached it in every run.

## 2. Problems, by impact

| # | Problem | Who | Evidence | Fix | Done? |
|---|---|---|---|---|---|
| 1 | Funders who click the most visible links get the NGO interview, not a review | Funders | The one-click links carry only the kickoff, which has no funder flow; the warning sat at the end of a long paragraph | A "Which way to use it" table under the links, and a funder section in Quick start | Done: docs, and a kickoff line |
| 2 | The recommendation is long (about 7,000–11,500 characters) and the next steps come last | NGO staff | Next steps started after 7,000–10,500 characters in most final answers; only some runs opened with a summary | Open with a short summary and the month's next steps; cap the length | Done (Section 4) |
| 3 | The required headings are jargon ("counterfactual audit warning", "operational report card"), and the body follows ("integer program", "leximin", "Thompson sampling") | NGO staff | System prompt and kickoff headings; transcripts | Plain headings, which are also shorter | Done (Section 4) |
| 4 | Full recommendations are sometimes given twice: a later answer brings another full reply | NGO staff | Several runs; partly caused by the test script, which keeps answering after the recommendation | "If a later answer changes the recommendation, restate only what changes"; make the test script answer what was asked | Done (Section 4) |
| 5 | Six to ten turns before anything useful, and some turns ask two questions | NGO staff | Transcripts | Say in the README how long a session takes; tighten "one question per turn" | Done: docs and prompt wording |
| 6 | Eight setup routes and no single place that says what each one gives up | Everyone | README | The comparison table; the corrected size of the all-in-one file (about 147,000 characters, not 107,000) | **Done** |
| 7 | The funder memo comes out in a monospace code block and runs about three pages | Funders | The playbook's memo template is in a code fence; outputs copy it, with hard line breaks that paste badly into email | Rewrite the template as headings and short paragraphs, with a word limit; "short memo", not "one-page" | Done (Section 4) |
| 8 | Funders aren't told what to include, so the request for their context varies | Funders | Runs where the risk appetite was missing | A paste template in the README and a funder conversation starter for the Custom GPT | **Done** |
| 9 | Stale counts ("sixteen cases") and a mixed group of cases | Everyone | README, cases index | Corrected counts; cases regrouped into interviews, tools that feed a decision, and funder reviews | **Done** |
| 10 | The reference files are written for the model, but users are sent to read them | NGO staff, funders | Taxonomy and playbook openings; Section 6 has grown large | A short "reading this yourself?" contents list at the top of each; consider splitting Section 6 | Done (Section 4) |

## 3. Prompt changes

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

## 4. What was done, and how it tested

All of Section 3 was carried out on 2026-11-22: plain headings, a summary first, a length target, restating only what changes, no sub-questions, a short funder path in the kickoff (the kickoff's class list lost its method jargon to make room), a scope line naming Sections 6–7, the memo as plain text, and taxonomy Section 7 split from Section 6. The system prompt is at 7,998 of 8,000 characters and the kickoff at 3,992 of 4,000. The build's heading check now reads the recommendation headings from the system prompt.

The test script was changed too: it stops sending scripted answers once a recommendation arrives, so a run no longer forces repeat recommendations, and it can run a case through the one-click kickoff.

Thirteen cases were run against the rebuilt assistant (Claude Opus 5.5 via `claude -p`):

| Measure | Before | After |
|---|---|---|
| Recommendation length | about 7,000–11,500 characters (roughly 1,400–1,900 words), next steps last | 1,200–1,470 words, opening with *Class / Why / This month* |
| Headings | the old jargon, sometimes renamed by the model | the six plain headings in every run |
| A fact added after the recommendation | another full recommendation | a restatement of what changes, about 2,300–2,500 characters (Cases 2 and 9) |
| Funder memo length | about 6,800–9,300 characters (roughly 1,100–1,500 words), in a code block | about 870–1,020 words including the filter reading, as plain text; a tighter instruction didn't shorten it further, so the target is now about 800 words in all |

Outcomes: interview Cases 2, 6, 9, 21 and 23 reached their expected classes, Case 6 still "no model needed". Funder Cases 17 (*Mismatch*), 18 (*Fits*), 19 (*No model needed* for the scoring), 20 (*No model needed* for the rollout, with the summaries judged on outcomes), 22 (*Fits, on conditions*), 24 (beneficiaries flagged at the top, *Heavier than needed*) and 25 (*Mismatch* in the test plan) all matched their cases.

One shortfall: Case 19 run through the one-click kickoff gave *Heavier than needed* where the full assistant gives *No model needed*. The kickoff's short funder path has no room for the playbook's verdict guide, so the README and blog now say the links give only a short memo and recommend the full setup for funders.
