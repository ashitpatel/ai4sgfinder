# Changelog

Each release on GitHub attaches the ready-to-use files from `dist/` and, from 1.7.0, the replay kit's workbooks. The version lives in [`VERSION`](VERSION).

## Unreleased

- **Tools mode proposed** ([plan](docs/plans/tools-mode.md)): a local package and MCP server alongside today's chat setup, from the same reference files.
- **Case harness in the repo** ([tests/cases](tests/cases/README.md)): runs any or all of the 25 worked cases through Claude Code, logs tokens, cost and time per turn, and grades the class or verdict against `expected.json`.
- **Chat-mode baseline** ([baseline.md](tests/cases/baseline.md)): 24 of 25 cases reached their expected outcome (Case 15 put the patrol game before the risk model); each turn read about 68,000 tokens, 98% of them from the cache; about US$0.32 an interview case and US$0.11 a funder review at list prices.
- The README's size for the all-in-one file is corrected to about 170,000 characters.
- **Snares and patrols (Case 15):** when something hidden must be found and the people responsible adapt, the assistant now recommends Class 12 first with a Class 3 layer, unless each place's value is already known (then Class 3, as in Case 3). The rule is in the system prompt's Filter 3 mapping and space-and-risk narrowing, the kickoff and taxonomy Section 2, which also asks the narrowing question even when answers seem to cover it. Case 15 passed in 3 of 3 reruns, Case 3 in 2 of 2. To fit, the system prompt drops a redundant sentence and the kickoff drops "(verified)" from its evidence label.

## 1.11.0 — 2026-11-23

- **Others' setups** (playbook, Follow-up 4, under *What it takes*): what twenty published deployments across eleven classes report about who built them, how long it took, what it cost and what happened later, from ARMMAN's weekly call list and Boston's school buses to Denver's school choice, Aarau's participatory budget and Flint's lead pipes. Every figure was checked against its source; three that failed were dropped. No setup publishes what its model cost to build, and the handover is the least documented step. The [record of the pass](docs/plans/reference-setups.md) lists what isn't published for each class and leads for a later pass.
- **Blog:** Part 4 describes what published setups report, including Denver, Aarau and Flint; Parts 2 and 10 point to them.

## 1.10.0 — 2026-11-23

- **What it takes** (playbook, Follow-up 4, now *Build options: tools, partners, costs*): effort tiers by class, from a written rule to research code, with a rough shape of the work labelled as a guide, not a measurement; the cost lines to put a figure on (one-off, each round, each year, often missed); the roles a program must name, and which a volunteer can fill; the phases from the test on past records to running it; questions to ask a partner or vendor; and red flags. The assistant never states a cost, hours or a duration as fact, and points to people who ran similar programs instead. Runs of Cases 1 and 10 filled it from the cases' own answers.
- **Budget check in the funder review:** the memo names cost lines the budget leaves out, such as running costs after launch, staff time and a maintenance owner, and asks how it was estimated, without judging the figures. Case 17's memo did this.
- **Cost of ownership** ([tools/replay-kit](tools/replay-kit/README.md#before-deciding-the-cost-of-ownership)), a fifth workbook: money and staff hours for each cost line, for the simple rule and the model, totalled over several years with a contingency, and the cost of each extra person the model reaches; blank lines are counted as *not found out yet*. Checked in Excel against an independent recomputation. Releases attach it.
- The kit's guide, README, docs index and cases checklist cover the new guidance. Excel lock files are ignored by git.
- **Blog:** Part 2 describes *what it takes* in Follow-up 4, Part 4 the cost worksheet, Part 10 the memo's budget check, and Part 9's table and the About page are updated.

## 1.9.0 — 2026-11-22

- **What the assistant does with the replay kit.** The playbook gains *The replay kit*, a table of which workbook goes with which class and what each needs, and names the workbook where it tells users to test on past records: pilot design (*Replay first*, and a random share with the monthly health check after launch), the partner brief's *Simpler option to beat*, and the funder memo's first and scale stages. It never asks for records in the chat. Runs of Cases 1, 13 and 17 named the right workbook in the recommendation, the follow-ups and the funding stages; the cases checklist now checks this.
- **How to use the kit:** the kit guide adds the records each workbook needs, the steps, how to decide from the results and where to share them, and what AI4SG Finder does with the kit. The README and tutorials index link to it.
- **Blog:** Parts 2, 4 and 10 say the assistant names the workbook for the user's class, and Part 4 links the kit's how-to.

## 1.8.0 — 2026-11-22

- **Monthly health check** ([tools/replay-kit](tools/replay-kit/README.md#after-launch-the-monthly-health-check)), a fourth workbook for a tool already in use. From each month's records it reports, with a status for each: change in records, whether staff follow the list, overrides, the random share, outcomes recorded, the tool's hit rate against the random share and calibration (pooled over up to three months, left blank until there are enough outcomes), calibration and share served by group, and overlap with a simple rule. Thresholds are settings. The sample shows staff overriding a stale model toward a hazard it never saw. Checked in Excel against an independent recomputation, including the first month. The fairness audit's recheck step and the *Human override* readiness check point to it, and releases attach it.
- **Docs and blog:** Parts 2, 4 and 10 and the About page describe the health check; the kit guide, README and docs index list it.

## 1.7.0 — 2026-11-22

- **Replay kit** ([tools/replay-kit](tools/replay-kit/README.md)): three Excel workbooks that replay a program's past records under its current practice, a simple rule and a model's scores, on its own computer. *Pick N once* (Classes 2 and 12) checks each rule's choices against an outcome learned later; *Weekly visit list* (Class 1) builds the six-cell table from past weeks and compares the expected gain of each rule's visits; *Waitlist* (Class 10) replays arrivals week by week under two ordering rules. Each reports results by group, says what a replay can't show, and ships with made-up sample records. Generated by `scripts/build_replay_kit.py`; checked in Excel against an independent Python replay. The playbook's privacy rule and *Simpler option tested* check, and taxonomy Section 4, point to it.
- **Docs and blog:** Parts 2, 4 and 10 and the About page point to the replay kit; the README and docs index list it. Releases now attach the three workbooks.

## 1.6.0 — 2026-11-22

- **Support before and after a session.** The assistant replies in the user's language; it won't ask for or work on records about named people, and asks for counts and fields instead, since comparisons on past records belong on the program's own computer. When a user doesn't know an answer, it assumes, marks the assumption to check and goes on. The playbook adds *Questions to settle before you start*, a list to work through with colleagues, which the assistant offers when key facts are missing.
- **A session record** after the partner brief (Follow-up 6): the answers, recommendation, assumptions, open questions and next steps in about 200 words, to paste into a later conversation and pick up where it left off.
- **NGOs can run the funder review on their own proposal** before sending it; the memo lists the questions a funder is likely to ask and what would answer each.
- **Docs and blog** describe the new support: Part 2 gains *Before you start*, Part 10 says NGOs can review their own proposal, Part 6 notes that the assistant already replies in the user's language, and the README's summary covers the session record, self-review and privacy rule. The cases checklist adds three spot checks.
- To fit the 8,000-character limit, the recommendation's first and fifth headings are described more briefly in the system prompt, and the note on tutorial figures is dropped (tutorials aren't attached to the assistant).

## 1.5.0 — 2026-11-22

- **Shorter, plainer recommendations** ([UX review](docs/plans/ux-review.md)). Each recommendation opens with a three-line summary and the month's next steps, aims for about 1,200 words, and uses plain headings: *What kind of problem this is*, *What goes wrong without it*, *How it runs on the ground*, *Where it has been used*, *What worked and what was hard*, *The simpler option*. One question per turn, with no sub-questions; a later answer brings a restatement of only what changes. The build's heading check follows the new headings.
- **A short funder path in the kickoff,** so the one-click links can give a brief memo; the full review still needs the playbook. The kickoff's class list drops method jargon to make room.
- **The funder memo** is plain text with headings, not a code block, aiming at about 800 words in all.
- **Taxonomy Section 7, *Beyond the twelve classes*,** now holds the parts on beneficiary scores, AI as the intervention, model-measured outcomes and near-class decisions; Section 6 keeps the input layers. Both reference files open with a contents list for people reading them directly.
- **Blog Part 11,** [*What the first scan missed, and what it changed*](https://ashitpatel.github.io/ai4sgfinder/what-the-scan-missed/), on the wider scan and what it added; the other posts now count eleven parts and describe the new recommendation and memo format.
- **Docs and blog reviewed:** the README is reordered for readers first, with a table of ways to use it and a funder section; the cases index is regrouped; a docs index and the UX review are added; the skill description lists all twelve methods.
- **A third scan pass** reached funder grantee lists and venues the first two missed. The table of decisions near the twelve classes (now in Section 7) grows by eight rows: people already eligible under written rules (*no model needed*: a rules engine), surplus donations placed as they arrive, live dispatch of crisis responders, which polluters or contractors to inspect, a funder's own grant choices, audits of past human decisions, splitting a fixed national stock across facilities, and AI that drafts statements a divided group can endorse.
- **Limits of prediction** in Section 4: in the Fragile Families Challenge, the best of 160 teams' predictions were only slightly better than a four-variable regression (Salganik et al., 2020), and a 2026 follow-up found the same across hundreds of outcomes.
- Section 6 adds phone mobility data as a geospatial input in emergencies (Bengtsson et al., 2011; Ebengo et al., 2026), RAND's way of grading chatbot answers with experts' rubrics and checked automated graders (McBain et al., 2026), and cautions that effect estimates from non-randomized records depend on the estimator and that label sources can disagree. The readiness checks add *contract terms*.

## 1.4.0 — 2026-11-22

- **Funder review.** A funder can paste an NGO's proposal instead of answering the interview. The assistant writes a seven-part review memo: the decision, whether the method fits (fits, heavier than needed, mismatch, or no model needed), the simpler option to beat, questions for the NGO, risks to people, an evidence check and suggested funding stages. It reviews the method, never the organization, and doesn't say whether to fund. The playbook's new last section holds the rules, verdict guide and template; the system prompt gains one line routing funders to it. Three new worked cases (17–19) cover a mismatch, a fit and a no-model verdict.
- The partner brief (Follow-up 6) now covers the program itself, where it works, its timeline and resources, and splits where a partner can help into build and evaluation.
- Follow-up 4 lists CEGA, J-PAL and IPA as evaluation partners, with a three-part test for when to suggest them; the consent and privacy readiness check is more specific.
- **Input layers.** The taxonomy's new [Section 6](prompt/knowledge/taxonomy.md#6-input-layers) covers tools that allocate nothing themselves but feed a decision: speech recognition, document extraction and prediction models. The assistant classifies the decision the tool feeds, not the tool. Section 6 also says when to build, adapt or use a published model, and what to measure on the program's own data before relying on one. The system prompt names the section. The funder review gains a rule for proposals that are input layers, with three questions to ask in every such memo. Follow-up 2 gains an input-layer readiness check, and Follow-up 4 says where to compare such models without recommending any.
- **Fairness audit for a risk score.** Follow-up 2 ends with a six-step audit: what the label measures, calibration by group, with and without group variables, share of slots by group, a random share, and a yearly recheck. The "Bias in risk scores" check and the funder memo's "Risks to people" heading link to it, and Fairlearn joins the Class 12 tools.
- Four new worked cases (20–23) follow the problem pattern of real projects: Adalat AI's courtroom speech recognition, an ECG deep-learning model for sudden cardiac death, research on race in clinical risk scores, and the Local Law Observatory's database of local ordinances. The [coverage plan](docs/plans/input-layers-and-fairness-audit.md) records what each project uses and what ai4sgfinder covered before.
- New verified references: Obermeyer et al. (2026), Zink, Obermeyer & Pierson (2024), Shanmugam, Hou & Pierson (2021), Gera & Pierson (2024), Nethil et al. (2025) and Peskoff et al. (2026). New unverified claims: Adalat AI's productivity results and scale, a Science Advances version of Gera & Pierson, and LOCUS at NeurIPS 2026.
- **More input layers, from an expanded scan.** Section 6 adds screening classifiers (a cheap test that decides who is referred), forecasts and ready-made maps, each with what to check on the program's own data: sensitivity against the reference test and a threshold matched to capacity; forecast skill against a simple baseline at the lead time needed; the age and calibration of a map. The [expanded scan](docs/plans/expanded-scan.md) records why the earlier scans missed these and the seven sweeps that found them.
- **Scoring the people a program serves.** A new part of Section 6, a readiness check and a funder-review rule warn about risk scores aimed at beneficiaries (fraud, overpayment, eligibility), the most common government failure: a legal basis, human review of every flag, a way to appeal and a published fairness audit are required before any pilot. Class 12's "avoid when" points to it.
- **When the AI is the intervention.** For tutors, coaches and advisers, the assistant now reviews how the tool will be tested (an outcome, not usage, against a comparison) instead of saying the review doesn't apply. Pilot design gains checks for this and for outcomes measured by a model.
- Two new funder-review cases: a benefit-fraud score (24, mismatch) and an AI tutor (25, mismatch in the test plan).
- **When a model measures the outcome.** Section 6 covers proxies such as satellite images or phone records standing in for surveys, with a positive case (Kenya cash transfers) and a negative one (Haiti), and recommends keeping a direct measure on a random sample (prediction-powered inference).
- **Decisions near the twelve classes.** A table in Section 6 maps decisions the scan found to existing classes: health posts upgraded year by year, survey-team routes, contact timing, connected reserves, subsidies, which villages to enter next, outreach to current clients, zone boundaries and case backlogs. Choosing a rule by simulation (Nigeria's malaria plan, UNDP's Policy Priority Inference) is described as a modelling partnership, not a thirteenth class.
- **Governance in the readiness checks:** advisory or binding (people follow a biased AI's advice unless the bias is severe), a threshold matched to staff capacity, review before use (OCHA's peer-review framework, the UK DWP's published fairness assessment) and analysing sensitive records where they live (OpenSAFELY). Extraction checks now ask for sampling after launch, since accuracy on past data can collapse on a live stream.
- **A repeatable scan.** [docs/scanning.md](docs/scanning.md) is the recipe for a quarterly scan; a second round reached many sources the first missed.
- Eleven more verified references, among them Huang et al. (2021), Barriga-Cabanillas et al. (2025), prediction-powered inference (2023), Ozodiegwu et al. (2023), Guerrero & Castañeda (2020), Dasgupta et al. (2025), Choo et al. (2026), Wilson et al. (2025) and Williamson et al. (2020).
- Fifteen more verified references, among them the SyRI judgment, the Robodebt Royal Commission, Elzayn et al. (2025) on tax audits, Muralidharan et al. (2025) on biometric checks, the Edo State and Khanmigo tutoring trials, Tutor CoPilot, and the observational study and randomized trial of Penda Health's AI Consult.

## 1.3.0 — 2026-11-01

- **Simpler alternatives.** Every recommendation now has a sixth heading, *The simpler alternative*: the best paper, spreadsheet or calculator option for the class, in what ways it comes close (total outcome, fairness, worst case, evidence) and what it gives up, the assumptions to check before settling for it, and how to compare it with the model on past records. The taxonomy's new [Section 4](prompt/knowledge/taxonomy.md#4-simpler-alternatives-for-each-class) lists the option for each class with verified evidence where it exists; the playbook adds a readiness check, a pilot comparison against the simple option, and a "Simpler option to beat" line in the partner brief.
- **Tutorials measure the simple option.** Each tutorial for Cases 1–13 ends with a section comparing the best simple rule with the method on the same illustrative data. New rules in the programs: a six-cell one-step table (Case 1), greedy with a district floor (2), a weighted patrol lottery and a Goal Seek equilibrium (3), an equal split of stock (4), greedy within area envelopes (7), greedy placement with quarterly allotments (11), most-named residents spread across friend groups (12) and oldest-first with a random share (13). Earlier figures in the tutorials are unchanged.
- **Two classes together.** The interview ends with a question about a second decision in the same program (when to act, where to look first, how it reaches people, or which version works for whom); a yes adds a second class as a layer. The taxonomy's new [Section 5](prompt/knowledge/taxonomy.md#5-when-two-classes-combine) lists combinations seen in practice, with real examples.
- Three new worked cases that combine classes: cash released before a flood (Class 4 trigger with a Class 2 targeting layer), snare search with randomized patrols (Class 12 with a Class 3 layer) and job-search support that learns which option works for whom (Class 8 with a Class 7 layer). Cases 1–13 gain an answer to the second-decision question and a simpler-alternative section; Cases 4, 7, 9 and 13 show second decisions that are not a separate layer, or only a later one.
- New tutorial 14, for the cash-before-a-flood case: choosing a forecast trigger with the cost-loss rule, a calculator table of past seasons, and a threshold that holds up across every forecast model a thin record can't rule out, with the targeting list as a second layer. Its program tests the rules on simulated monsoons and stress scenarios; the calculator table chose the same threshold as both models.
- New verified references: Hanna & Olken (2018), Kim et al. (2015), Abdulkadiroğlu & Sönmez (2003), Clarke & Wright (1964), Hadad et al. (2021), Gholami et al. (2017), Pople et al. (2021), Bansak et al. (2018), plus comparisons with simple rules reported in Mate et al. (2022), Aiken et al. (2022) and Kempe et al. (2003).

## 1.2.0 — 2026-10-31

- Seven new allocation classes, found by reviewing the research of Lily Xu, Roshni Sahoo and Ashish Goel's group, then their wider networks of collaborators and the AI-for-social-good literature, against the original five:
  - **Class 6: Participatory Allocation** — a community votes on how a shared budget is split (participatory budgeting, knapsack voting, the method of equal shares).
  - **Class 7: Effect-Based Targeting** — give a program to the people it helps most, learned from pilot or trial data, rather than to the neediest by default (policy learning, causal forests).
  - **Class 8: Learn-While-Allocating** — learn which of several stable options works while still serving people (bandits, adaptive experiments).
  - **Class 9: Routing & Logistics** — move goods or people through depots and routes at least cost (vehicle routing, supply-chain network design).
  - **Class 10: Online Assignment & Waitlists** — place people or items that arrive one at a time (online allocation, dynamic rationing, lotteries).
  - **Class 11: Network Seeding** — choose the few people whose social ties spread information furthest (influence maximization).
  - **Class 12: Risk-Based Inspection** — decide where to inspect or test to find hidden hazards (predictive risk ranking, active search).
- The twelve classes are grouped into five families in the system prompt and kickoff, which now list one line per class to stay within the 8,000- and 4,000-character limits. Class numbers 1–5 are unchanged.
- The taxonomy, decision tree, system prompt, kickoff prompt, playbook, README and social preview image cover all twelve classes. The interview now runs in two stages: five filters, each one plain question per turn (with an optional follow-up), place the problem in a family; then one or two narrowing questions pick the class. Each family's narrowing questions are in the taxonomy's decision tree, along with a table of the data each class needs.
- Feeding America's "Choice System" moves from Class 5 to Class 10: it is an auction with credits for donations as they arrive, not a two-sided stable match.
- Class 4 now covers forecast-triggered anticipatory action; Class 2 notes predict-then-assign variants and eligibility rules that applicants can game.
- The unverified "Roshni Sahu" attribution is corrected to Roshni Sahoo, with her verified papers.
- Seven new worked cases (Cases 7–13), one for each of Classes 6–12, each with interview answers, what a good recommendation contains, and Follow-ups 1 and 6 in full. The six existing cases are updated for the two-stage interview and name their new neighboring classes. The case index is grouped by family.
- Seven new tutorials (7–13), one per new case, each with a runnable program that produces every number in the text. Tutorials 1–6 reviewed and updated to name their new neighboring classes and link the new tutorials.

## 1.1.2 — 2026-10-31

- New in-depth tutorials, one per worked case, explaining how each method works for readers with basic statistics and no optimization background. Each comes with a runnable Python program that produces every number in the text.
- New `CITATION.cff`, so the repository can be cited (GitHub's "Cite this repository" button). Releases are archived on Zenodo with a DOI.
- The README now opens with a short sample session.
- The files in `dist/` are unchanged apart from the version number in the Claude Code plugin manifest.

## 1.1.1 — 2026-10-30

- Each class now has a plain-language definition in the taxonomy: what it is, the question it answers, and when to use or avoid it.
- Class names in the worked cases, cases index, playbook and README link to these definitions.
- The playbook uses the full Class 3 name (Spatiotemporal Security & Adaptive Search) throughout.

## 1.1.0 — 2026-10-30

- New implementation playbook (`playbook.md`), shipped as a second knowledge file in every package, covering what to do after an approach is chosen.
- After its recommendation, the assistant now offers six follow-ups tailored to the user's answers: fit the model to your program, readiness checks, pilot design, build options (tools and partners), reading and people to contact, and a one-page brief for a technical partner.
- The kickoff prompt offers the same follow-ups.
- Worked case 1 now includes a filled-in partner brief.

## 1.0.0 — 2026-10-30

First release.

- System prompt that diagnoses an allocation problem through five filters and recommends one of five AI4SG approaches, or no model at all.
- Reference taxonomy with a decision tree and verified citations; unverified claims from the original draft are flagged.
- Ready-made files for Claude Projects, Custom GPTs, Gemini Gems, Google AI Studio, and browser assistants (including a paste-in kickoff prompt under 4,000 characters).
- Claude Skill and Claude Code plugin.
- API chat examples for Claude, OpenAI, and Gemini.
- Six worked cases, one per class plus a "no model" case.
