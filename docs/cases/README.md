# Worked cases

Twenty-five illustrative cases. They are the project's examples and its test set.

- **Cases 1–16** are interviews that together exercise every outcome the assistant can reach: one per allocation class, one where the right answer is "no model," and three where a program needs two classes working together.
- **Cases 21 and 23** are interviews where a tool feeds the decision: a published prediction model, and laws extracted from scanned documents ([taxonomy, Section 6](../../prompt/knowledge/taxonomy.md#6-input-layers)).
- **Cases 17–20, 22, 24 and 25** show the [funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal), in which a funder pastes an NGO's proposal instead of answering the interview.

Most span a different impact domain and intervention type, and each names the simpler alternative to its method and when it is close enough.

All organizations and programs in these cases are fictional. The research they cite is real and is drawn from the verified references in [`taxonomy.md`](../../prompt/knowledge/taxonomy.md).

## Coverage

The cases are listed by family, the grouping the interview uses to narrow down the class.

| Case | Domain | Intervention type | Expected outcome | Deciding question |
|------|--------|-------------------|------------------|-------------------|
| **Who gets a limited resource** | | | | |
| [2. Borehole siting](02-borehole-siting.md) | Water and sanitation | Irreversible infrastructure | [**Class 2** Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) (welfare ILP) | **Filter 1** (handed over once) + narrowing: everyone known up front, no trial data |
| [8. Business grants](08-business-grants-effect-targeting.md) | Livelihoods | One-off grant and training | [**Class 7** Effect-Based Targeting](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) (policy learning) | Narrowing: a randomized pilot shows who benefits most |
| [11. Refugee placement](11-refugee-placement-online.md) | Resettlement | Placement as families arrive | [**Class 10** Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists) (online allocation) | Narrowing: families arrive one at a time |
| **Repeated decisions that learn** | | | | |
| [1. CHW hypertension visits](01-chw-hypertension-visits.md) | Primary health care | Recurring behavioral nudge | [**Class 1** Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) (restless bandits) | **Filter 1** (given repeatedly) + narrowing: each patient's state drifts + **Filter 5** (weekly data) |
| [9. SMS reminders](09-sms-reminders-adaptive-experiment.md) | Child immunization | Message wording | [**Class 8** Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) (adaptive experiment) | Narrowing: unknown which option works best |
| **Space, movement and risk** | | | | |
| [3. Marine patrols](03-marine-patrols.md) | Conservation | Mobile enforcement | [**Class 3** Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) (security games) | **Filter 3** (an adversary adapts) |
| [4. Cyclone pre-positioning](04-cyclone-prepositioning.md) | Disaster preparedness | Contingency stockpiling | [**Class 4** Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) (DRO over a location model) | **Filter 4** (catastrophic, little history) |
| [10. Food delivery routes](10-food-delivery-routing.md) | Food assistance | Weekly truck deliveries | [**Class 9** Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics) (vehicle routing) | **Filter 1** (moved by vehicle) + narrowing: moving goods to many places |
| [13. Lead-pipe search](13-lead-pipe-inspection.md) | Environmental health | Limited inspections | [**Class 12** Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection) (predictive inspection) | **Filter 1** (used to find something hidden) + narrowing: finding hidden problems |
| **People choose** | | | | |
| [5. Apprenticeship matching](05-apprenticeship-matching.md) | Youth employment | Two-sided placement | [**Class 5** Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) (stable matching) | **Filter 2** (both sides choose) |
| [7. Neighborhood budget](07-neighborhood-participatory-budget.md) | Civic participation | Shared budget for projects | [**Class 6** Participatory Allocation](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation) (participatory budgeting) | **Filter 2** (the community votes) |
| **Spread through people** | | | | |
| [12. Peer educators](12-peer-educators-network-seeding.md) | HIV prevention | Training a few messengers | [**Class 11** Network Seeding](../../prompt/knowledge/taxonomy.md#class-11-network-seeding) (influence maximization) | **Filter 1** (a message to pass on) + narrowing: friendships can be mapped |
| **No model** | | | | |
| [6. Food pantry](06-food-pantry-no-model.md) | Food security | Recurring in-kind distribution | **No model needed** | **Filter 4** (supply already meets demand) |
| **Two classes together** | | | | |
| [14. Cash before a flood](14-anticipatory-cash-floods.md) | Disaster risk | Cash released on a forecast | [**Class 4**](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) trigger + [**Class 2**](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) targeting layer | **Second decision** (when to pay) + **Filter 4** (late is harmful, little history) |
| [15. Snare search](15-snare-search-patrols.md) | Conservation | Ranger foot patrols | [**Class 12**](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection) risk map + [**Class 3**](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) randomization layer | **Narrowing** (finding hidden snares) + **Filter 3** (poachers adapt) |
| [16. Job-search support](16-job-support-adaptive-targeting.md) | Youth employment | One of three supports per person | [**Class 8**](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) experiment + [**Class 7**](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) targeting layer | **Second decision** (for whom) + **Filter 4** (no randomized data yet) |
| **A tool feeds the decision** | | | | |
| [21. ECG cardiac referral](21-ecg-screening-cardiac-referral.md) | Cardiovascular health | Limited cardiology workups | [**Class 12**](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), using a published deep-learning model | Narrowing: finding hidden risk; too few local events to train, so validate instead |
| [23. Local-law campaigns](23-local-ordinance-advocacy-targeting.md) | Housing and tenant rights | Yearly advocacy campaigns | [**Class 2**](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) fed by an OCR and language-model extraction layer | Second decision: the data must be extracted first, and its labels checked |
| **Funder review** | | | | |
| [17. Risk-score home visits](17-funder-review-risk-score-visits.md) | Primary health care | Proposal: weekly visits chosen by a lapse-risk model | **Mismatch**: the decision is [**Class 1**](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) | A risk score measures need, not the effect of a visit |
| [18. Delivery routing](18-funder-review-delivery-routing.md) | Food assistance | Proposal: vehicle routing for three trucks | **Fits**: [**Class 9**](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics) | The method and data match the decision |
| [19. Screening chatbot](19-funder-review-screening-chatbot.md) | Emergency assistance | Proposal: a chatbot that scores applications | **No model needed** | Supply nearly meets demand; the allocation is hidden inside a chatbot |
| [20. Court transcription](20-funder-review-court-transcription.md) | Access to justice | Proposal: speech recognition and order summaries in courtrooms | **Review doesn't apply**; the rollout order needs **no model** | The tool is perception, not allocation; everyone is served in the end |
| [22. Race-blind risk score](22-funder-review-race-blind-risk-score.md) | Cancer screening | Proposal: a risk score for colonoscopy outreach | **Fits**: [**Class 12**](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), with fairness conditions | Removing race doesn't make a score fair; check calibration by group and the label |
| [24. Benefit-fraud score](24-funder-review-benefit-fraud-score.md) | Social protection | Proposal: a model that flags recipients and pauses payments | Flags beneficiaries first; automatic pauses ruled out; referral step *Heavier than needed* or *Mismatch* | The score targets the program's own beneficiaries |
| [25. AI tutor](25-funder-review-ai-tutor.md) | Secondary education | Proposal: an AI tutor on WhatsApp | **Mismatch** in the test plan | The AI is the intervention; usage is not learning |

Across Cases 1–16, every filter, every narrowing question and the second-decision question is the deciding one at least once, and each case names the classes it is most likely to be confused with, so the cases also show what separates neighboring classes. Cases 4, 7, 9 and 13 show second decisions that are *not* a separate layer, or only a later one.

Cases 1–13 each have an [in-depth tutorial](../tutorials/) that explains the method step by step, assuming only basic statistics, and measures the simpler alternative against it on illustrative data. Case 14 has its own tutorial on choosing a forecast trigger; Cases 15 and 16 point to the two tutorials that teach their layers.

Cases 20–25 follow the problem pattern of published real-world work: [Adalat AI](https://adalat.ai)'s courtroom speech recognition (20), an ECG deep-learning model for sudden cardiac death (21), research on race in clinical risk scores (22), the Local Law Observatory's database of local ordinances (23), government fraud scoring of benefit recipients (24) and randomized trials of AI tutors (25). The organizations in them are still fictional. They test the edges of the taxonomy: a tool that allocates nothing, a prediction model the program uses rather than builds, a fairness audit, a score aimed at the program's own beneficiaries, and an AI that is itself the intervention. Taxonomy [Sections 6](../../prompt/knowledge/taxonomy.md#6-input-layers) and [7](../../prompt/knowledge/taxonomy.md#7-beyond-the-twelve-classes) hold the rules they test, and the [plans](../plans/) record how they were added. Case 21 reuses the Class 12 tutorial and Case 23 the Class 2 tutorial.

## Each interview case contains

- **Scenario**: the organization and its constraint, in a few sentences.
- **Interview answers**: a realistic answer to each of the five filters, the narrowing question for its family and the second-decision question, written in the user's voice.
- **Why Class N: Name**: the selected class by number and name, how the answers map through the [two-stage decision tree](../../prompt/knowledge/taxonomy.md#2-the-ngo-decision-tree), and which classes are ruled out and why, each named alongside its number.
- **What a good recommendation contains**: the key points under each of the six required headings, named in the cases by short labels (1. Class, 2. Counterfactual warning, 3. Field pathway, 4. Evidence, 5. Report card, 6. Simpler alternative) that map in order to the assistant's headings (*What kind of problem this is*, *What goes wrong without it*, *How it runs on the ground*, *Where it has been used*, *What worked and what was hard*, *The simpler option*), including **6. Simpler alternative**: the best paper or spreadsheet option, in what ways it comes close, and what to check before settling for it. Combined cases cover a simpler option for each layer.
- **What the assistant should not do**: the most likely wrong answers.
- **After the recommendation**: how the assistant's follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md) help the user narrow down tools and partners, adapt the approach to their program, check readiness and plan a pilot. Each case works through one or two follow-ups in full, built from its own interview answers, and summarizes the rest.

## Each funder-review case contains

A header table (domain, who is using the assistant, the expected verdict, the most likely confusion, the playbook section, and for Cases 20–25 the real-world pattern; Case 20 also lists an acceptable alternative reading), then: the scenario; **what the funder pastes**, the proposal summary and the funder's own context; **why the verdict follows**; **what a good memo contains** under each of its seven headings; and **what the assistant should not do**. Case 20 adds a section on the real-world pattern behind it.

## Follow-ups shown in full

Together, the cases show each of the six follow-ups worked through at least once.

| Follow-up | Shown in full in |
|---|---|
| 1. Fit the model to your program | [Case 1](01-chw-hypertension-visits.md#follow-up-1-fit-the-model-to-your-program) (restless bandits), [Case 5](05-apprenticeship-matching.md#follow-up-1-fit-the-model-to-your-program) (stable matching), and each of Cases 7–16 |
| 2. Readiness checks | [Case 3](03-marine-patrols.md#follow-up-2-readiness-checks): a status table with what to fix before the pilot; [Case 21](21-ecg-screening-cardiac-referral.md#follow-up-2-readiness-checks): validating a published model; [Case 23](23-local-ordinance-advocacy-targeting.md#follow-up-2-readiness-checks): checking an extraction layer |
| 3. Pilot design | [Case 4](04-cyclone-prepositioning.md#follow-up-3-pilot-design): testing a plan when a live trial is impossible; Cases [14](14-anticipatory-cash-floods.md#follow-up-3-pilot-design), [15](15-snare-search-patrols.md#follow-up-3-pilot-design) and [16](16-job-support-adaptive-targeting.md#follow-up-3-pilot-design): piloting two layers in order |
| 4. Build options: tools and partners | [Case 2](02-borehole-siting.md#follow-up-4-build-options--tools-and-partners): narrowing software and partners to one choice |
| 5. Reading and people to contact | [Case 5](05-apprenticeship-matching.md#follow-up-5-reading-and-people-to-contact) |
| 6. One-page brief for a technical partner | [Case 1](01-chw-hypertension-visits.md#follow-up-6-one-page-brief-for-a-technical-partner), and each of Cases 7–13 |
| Funder review memo | Cases [17](17-funder-review-risk-score-visits.md), [18](18-funder-review-delivery-routing.md), [19](19-funder-review-screening-chatbot.md), [20](20-funder-review-court-transcription.md), [22](22-funder-review-race-blind-risk-score.md) (with the fairness audit), [24](24-funder-review-benefit-fraud-score.md) and [25](25-funder-review-ai-tutor.md) |
| Follow-ups when no model is needed | [Case 6](06-food-pantry-no-model.md#after-the-recommendation): the written rule, when to revisit, and a note to the funder |

## Using the cases

**To learn the method.** Read the "Why Class N" sections side by side, family by family. The contrasts that matter most: cases 1 and 9 (each person's state drifts vs. which option works), cases 2, 8 and 11 (need vs. effect vs. arrivals over time), cases 5 and 7 (two-sided choice vs. a vote), cases 3 and 13 (an adversary vs. a hidden problem), and case 15 against cases 3 and 13 (both at once). Then read the sixth heading across Cases 1–16: how close the simple option comes varies from "identical" (case 5) to "the simplest rotation was not enough" (case 1).

**To demo the assistant.** Start a chat on any platform, then paste the case's interview answers one at a time as the assistant asks each question.

**To test a prompt change.** After editing anything under `prompt/`, rebuild, then run the cases the change could affect, and always Case 6. The interview cases (1–16, 21, 23) work with any setup; the funder-review cases and anything that relies on taxonomy [Sections 6](../../prompt/knowledge/taxonomy.md#6-input-layers) and [7](../../prompt/knowledge/taxonomy.md#7-beyond-the-twelve-classes) need the full assistant (`dist/all-in-one.md`, a Project, a Custom GPT or the skill), not the kickoff.

For an interview case, paste the scenario, then each interview answer as its own turn, then ask for the recommendation and the follow-up the case shows in full. Check:
1. Does it reach the expected outcome, including the layer for Cases 14–16, the input layer for 21 and 23, and no extra layer elsewhere?
2. Did it ask one question per turn, including the narrowing and second-decision questions?
3. Does it open with a short summary and next steps, stay near 1,200 words, and cover the points listed under each of the six headings? Does the simpler option say in what ways it is close and what to check?
4. If you add a fact after the recommendation, does it restate only what changes?
5. Does it avoid everything under "should not do"?
6. Is every citation either in the verified list or marked unverified?
7. Does it end by offering the six follow-ups? Is the follow-up built from the case's answers, using only tools and partners from the playbook?
8. For Classes 1, 2, 10 and 12, do the simpler option and the follow-ups (readiness, pilot design, brief) name the matching [replay kit](../../tools/replay-kit/README.md) workbook, and does pilot design mention the monthly health check? Does it never ask for the records in the chat?
9. In Follow-up 4, does *What it takes* give the tier, cost lines, roles, phases, questions and red flags for this program, point to the cost worksheet, and avoid stating any cost, hours or duration as a fact?
10. Three spot checks outside the cases: paste a few made-up client names and phone numbers (it should decline to use them and ask for counts), open in another language (it should reply in that language), and answer one question with "I don't know" (it should assume, mark it to check and go on).

For a funder-review case, paste "I'm a program officer reviewing an NGO's proposal" with what the funder pastes, in one message. Check:
1. Does it ask for any missing funder context before writing, and only then write the memo?
2. Does the memo have the seven headings, as plain text rather than a code block and around 800 words, a verdict from the four, and no advice on whether to fund?
3. For a tool that feeds a decision, does it ask the three input-layer questions without judging the model? For a score aimed at beneficiaries, does the first line say so? For an AI that is the intervention, does it review the test plan?
4. Is every figure the proposal cites marked verified, unverified or overstated?
5. Does the memo name the cost lines the budget leaves out (running costs, staff time, a maintenance owner) and ask how the budget was estimated, without judging the figures?
6. When the decision is in Class 1, 2, 10 or 12, does the first funding stage name the replay kit workbook the NGO can run itself, and does the scale stage ask for the health check's measures?

To run cases unattended, a script can send each turn to `claude -p` (or an API) with `dist/all-in-one.md` as the system prompt, resuming the same session; the [plans](../plans/) record runs made this way.

Case 6 is the most sensitive test: a prompt change that makes the assistant more eager to recommend technology will show up there first.
