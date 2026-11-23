# Chat-mode baseline

Recorded 2026-11-23 with the [case harness](README.md): all 25 worked cases, the full assistant as the system prompt (`dist/all-in-one.md`, release 1.11.0), Claude Opus 5.5 through Claude Code 2.1.310 in headless mode, four cases at a time. This is what [tools mode](../../docs/plans/tools-mode.md) is measured against.

## Results

| Case | Kind | Result | Got | Turns | Input tokens | Output tokens | Words in answer | Cost (list, US$) |
|---|---|---|---|---|---|---|---|---|
| 01 | interview | pass | 1 | 8 | 547,253 | 7,090 | 1275 | 1.26 |
| 02 | interview | pass | 2 | 7 | 476,355 | 6,345 | 1260 | 0.87 |
| 03 | interview | pass | 3 | 7 | 477,315 | 8,283 | 1381 | 1.16 |
| 04 | interview | pass | 4 | 7 | 479,880 | 7,429 | 1260 | 1.04 |
| 05 | interview | pass | 5 | 8 | 543,491 | 6,085 | 1304 | 1.04 |
| 06 | interview | pass | none | 6 | 404,982 | 6,128 | 1377 | 0.76 |
| 07 | interview | pass | 6 | 9 | 611,979 | 7,228 | 1494 | 1.35 |
| 08 | interview | pass | 7 | 8 | 545,577 | 9,080 | 1417 | 1.37 |
| 09 | interview | pass | 8 | 10 | 693,822 | 8,932 | 1354 | 1.82 |
| 10 | interview | pass | 9 | 7 | 473,817 | 7,399 | 1378 | 1.02 |
| 11 | interview | pass | 10 | 6 | 399,814 | 5,605 | 1203 | 0.79 |
| 12 | interview | pass | 11 | 7 | 479,690 | 5,754 | 1261 | 0.97 |
| 13 | interview | pass | 12 | 10 | 689,323 | 8,145 | 1341 | 1.74 |
| 14 | interview | pass | 4 | 9 | 610,069 | 8,299 | 1414 | 1.59 |
| 15 | interview | fail | 3 | 3 | 202,802 | 6,185 | 1417 | 0.33 |
| 16 | interview | pass | 8 | 9 | 615,498 | 7,548 | 1302 | 1.31 |
| 17 | funder | pass | mismatch | 1 | 63,057 | 2,771 | 973 | 0.08 |
| 18 | funder | pass | fits | 1 | 66,712 | 3,653 | 1014 | 0.10 |
| 19 | funder | pass | no model needed | 1 | 66,675 | 3,739 | 955 | 0.10 |
| 20 | funder | pass | no model needed | 1 | 66,713 | 3,595 | 966 | 0.10 |
| 21 | interview | pass | 12 | 9 | 618,642 | 7,868 | 1411 | 1.48 |
| 22 | funder | pass | fits | 1 | 66,760 | 3,979 | 1026 | 0.11 |
| 23 | interview | pass | 2 | 8 | 544,812 | 7,409 | 1340 | 1.16 |
| 24 | funder | pass | heavier than needed | 2 | 136,887 | 4,287 | 1033 | 0.25 |
| 25 | funder | pass | mismatch | 1 | 66,655 | 3,226 | 1001 | 0.09 |

Cases: 25; pass: 24; others to read by hand: 1.
Input tokens: 9,948,580 in all, 397,943 a case on average. Output tokens: 156,062 in all, 6,242 a case. List-price cost reported: US$21.91 in all, US$0.88 a case.

"Input tokens" counts everything the model read on every turn: fresh input, cache writes and cache reads. Costs are the list prices `claude -p` reports, not what a plan or account was billed.

## Outcomes

24 of 25 cases reached their expected class or verdict.

- **Case 15 (snare patrols) missed.** It recommended Class 3 with a Class 12 layer; the case expects the reverse, because the hidden, badly recorded risk has to be estimated before patrols can be planned against it. This is the case's named "most likely confusion". The assistant took the scenario as answering most filters and recommended after three turns, without the narrowing question that separates the two.
- **Case 24 passed on reading.** The memo gave *Heavier than needed*, an accepted verdict, but titled the heading "Is the method a good fit?" rather than the playbook's "Method fit"; the first version of the grader missed it and was fixed. Because of the same miss, the harness sent the funder's context after the memo, and the assistant revised only the funding stages, as it should.
- **Case 6 still reached "no model needed."**
- Interview recommendations ran 1,200–1,500 words; funder memos 950–1,030 words, against the playbook's target of about 800.

## Tokens

- **Every turn reads the whole assistant.** Input per turn ran from 62,939 to 71,589 tokens (median 68,245): the all-in-one file plus the conversation so far. An interview case averaged about 520,000 input tokens over 3–10 turns; a funder review about 76,000 in one or two.
- **Almost all of it is cached.** Of 9.9 million input tokens, 98.3% were cache reads, 1.7% cache writes and well under 0.1% fresh. Output was 156,000 tokens in all.
- **What it cost:** US$21.91 at list prices for all 25 cases, US$0.88 a case: about US$1.17 for an interview and US$0.12 for a funder review.

## What this means for tools mode

Because caching already makes the repeated prompt cheap, tools mode will not save much money with Claude: fetching sections on demand changes the prompt from turn to turn, which caches less well. Its token gain is a smaller context (around 68,000 tokens a turn today), which matters on platforms and plans without caching and in long sessions. The case for tools mode rests mainly on what code can enforce: the checks, the interview steps that Case 15 skipped, and keeping records off the chat. The plan's success criteria are adjusted accordingly.
