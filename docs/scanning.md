# Scanning for AI-for-good work the project doesn't cover

How to repeat the [expanded scan](plans/expanded-scan.md) of November 2026, so the taxonomy keeps up with what researchers, funders and operators actually build. Run it quarterly. A pass takes one working session.

## Why a recipe

The first scans missed whole kinds of work because they followed one research community, looked only for allocation methods, counted projects instead of asking what each one feeds, and used one kind of source ([why](plans/expanded-scan.md#1-why-the-earlier-scans-missed-four-sources)). A fixed recipe guards against each of those.

## The seven sweeps

Use the same brief for each sweep and change only the sources. The brief states what is already covered (the twelve classes, the input layers in [taxonomy Section 6](../prompt/knowledge/taxonomy.md#6-input-layers), the warnings, and any items added since the last pass), what to look for, and the table to return.

| Sweep | Sources | Notes |
|---|---|---|
| A. US universities beyond CS/OR | Schools of public health, law, public policy, economics, earth sciences; labs such as Stanford RegLab, Chicago Crime Lab, CEGA, Penn's Nudge Unit, MIT J-PAL | Start from the lab's project page, not the department |
| B. Universities and institutes elsewhere | UK and Europe, Canada, India, Africa, Latin America, East and Southeast Asia, Australia | Last pass didn't reach Japan, Korea, Israel, Australia, KNUST, AIMS, IIIT Hyderabad, IIT Bombay, Ashoka |
| C. Funders, mined for grantees' methods | Gates, Wellcome, Rockefeller, Schmidt Sciences, McGovern, Google.org, Microsoft, Amazon, OpenAI and Anthropic programmes, Skoll, Echoing Green, MIT Solve, IDRC, Lacuna Fund, Grand Challenges Canada, Global Innovation Fund, Fast Forward, Pragati | Ask what decision each grant feeds, not only what kind of AI it uses |
| D. Labs and companies | Google Research and DeepMind, Microsoft AI for Good Lab, Meta Data for Good, IBM, NVIDIA, Ai2; impact companies and nonprofits | Separate deployments with partners from model releases |
| E. Venues and catalogues | AAAI AI for Social Impact, IJCAI AI for Social Good, KDD Applied Data Science, NeurIPS Datasets & Benchmarks and workshops, ML4H, CHIL, COMPASS, EAAMO, FAccT, Interspeech/ACL; OECD.AI and OPSI, ITU AI for Good | Count by role, to see the mix |
| F. Operators and governments | UN agencies, Red Cross, large NGOs, evaluators (IDinsight, IPA), government systems, including failures and court cases | Failures teach the warnings |
| G. University news | 20–30 news sites, followed to the paper | Gave about 20 new items in 280 stories in the first pass |

## How to run it

- **Split the budget.** One turn allows about 200 web searches shared by every agent. Run two or three sweeps per turn, each capped at 40–50 searches, rather than all seven at once.
- **Fetch listing pages instead of searching.** News topic and month archives, accepted-paper lists and grantee pages gave about three times the yield per call of search. Good starting pages: MIT News topic pages, washington.edu/news by month, Berkeley CDSS news, cam.ac.uk/stories, actu.epfl.ch, allenai.org/blog, urban.org, J-PAL Project AI Evidence, Stanford RegLab and HAI. Where a site blocks automated fetches (Stanford Report, Michigan, Princeton, Columbia, Imperial and Oxford did), use EurekAlert releases, RSS, or the desktop app's built-in browser: Stanford Report loaded normally there, but its site search ignored queries in the address, so plan to browse topic listings by hand.
- **Classify every item by role:** (a) allocates or decides, (b) input layer, (c) the intervention itself, (d) measurement or evaluation, (e) science, (f) governance or audit. Keep the counts in the write-up so the next pass can see whether the mix shifts.
- **Keep only items with a named partner** for the findings; research without one goes in a separate list.
- **Look for failures on purpose:** court rulings, inquiries, suspended systems and null trial results.

## From findings to changes

1. **Group items into patterns.** Keep a pattern only if at least two sweeps raised it.
2. **Map each pattern against the taxonomy and playbook:** covered, partly covered, or missing.
3. **Verify every reference before it is cited.** Most sweep rows come from search summaries. Check title, authors, venue, year and the key figure against the primary source; correct or drop anything that doesn't match, and list doubtful claims under *Unverified claims* in the taxonomy. In the first pass, 6 of 15 references needed a correction.
4. **Change the prompt files,** then rebuild (`python3 scripts/build.py`). The system prompt and kickoff are at their character limits, so new guidance usually belongs in the taxonomy or playbook.
5. **Write a case for each new pattern** that changes what the assistant should say, and run it, plus Case 6 (the most sensitive to a change that makes the assistant keener on technology), against the rebuilt assistant.
6. **Record the pass** in `docs/plans/`: sources reached and not reached, counts by role, patterns, changes made, case results.

## Last pass

| Date | Write-up | Items | New patterns | Changes |
|---|---|---|---|---|
| 2026-11-22 | [expanded-scan.md](plans/expanded-scan.md) | About 170 in the first round; about 120 more in a second round on sources the first didn't reach | 10, plus near-class decisions (zones, backlogs, timing, where to expand) | Section 6: input layers, warnings, model-measured outcomes, near-class decisions; governance readiness checks; Cases 24–25 |
