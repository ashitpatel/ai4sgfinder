# Worked cases

Thirteen illustrative cases that together exercise every outcome the assistant can reach: one per allocation class, plus one where the right answer is "no model." Each spans a different impact domain and intervention type.

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

Across the thirteen, every filter and every narrowing question is the deciding one at least once, and each case names the classes it is most likely to be confused with, so the cases also show what separates neighboring classes.

Each case also has an [in-depth tutorial](../tutorials/) that explains its method step by step, assuming only basic statistics.

## Each case contains

- **Scenario**: the organization and its constraint, in a few sentences.
- **Interview answers**: a realistic answer to each of the five filters and to the narrowing question for its family, written in the user's voice.
- **Why Class N: Name**: the selected class by number and name, how the answers map through the [two-stage decision tree](../../prompt/knowledge/taxonomy.md#2-the-ngo-decision-tree), and which classes are ruled out and why, each named alongside its number.
- **What a good recommendation contains**: the key points under each of the five required headings.
- **What the assistant should not do**: the most likely wrong answers.
- **After the recommendation**: how the assistant's follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md) help the user narrow down tools and partners, adapt the approach to their program, check readiness and plan a pilot. Each case works through one or two follow-ups in full, built from its own interview answers, and summarizes the rest.

## Follow-ups shown in full

Together, the cases show each of the six follow-ups worked through at least once.

| Follow-up | Shown in full in |
|---|---|
| 1. Fit the model to your program | [Case 1](01-chw-hypertension-visits.md#follow-up-1-fit-the-model-to-your-program) (restless bandits), [Case 5](05-apprenticeship-matching.md#follow-up-1-fit-the-model-to-your-program) (stable matching), and each of Cases 7–13 |
| 2. Readiness checks | [Case 3](03-marine-patrols.md#follow-up-2-readiness-checks): a status table with what to fix before the pilot |
| 3. Pilot design | [Case 4](04-cyclone-prepositioning.md#follow-up-3-pilot-design): testing a plan when a live trial is impossible |
| 4. Build options: tools and partners | [Case 2](02-borehole-siting.md#follow-up-4-build-options--tools-and-partners): narrowing software and partners to one choice |
| 5. Reading and people to contact | [Case 5](05-apprenticeship-matching.md#follow-up-5-reading-and-people-to-contact) |
| 6. One-page brief for a technical partner | [Case 1](01-chw-hypertension-visits.md#follow-up-6-one-page-brief-for-a-technical-partner), and each of Cases 7–13 |
| Follow-ups when no model is needed | [Case 6](06-food-pantry-no-model.md#after-the-recommendation): the written rule, when to revisit, and a note to the funder |

## Using the cases

**To learn the method.** Read the "Why Class N" sections side by side, family by family. The contrasts that matter most: cases 1 and 9 (each person's state drifts vs. which option works), cases 2, 8 and 11 (need vs. effect vs. arrivals over time), cases 5 and 7 (two-sided choice vs. a vote), and cases 3 and 13 (an adversary vs. a hidden problem).

**To demo the assistant.** Start a chat on any platform, then paste the case's interview answers one at a time as the assistant asks each question.

**To test a prompt change.** After editing `prompt/system-prompt.md` or `prompt/kickoff.md`, run all thirteen cases and check each final recommendation against the case:
1. Does it reach the expected outcome?
2. Did it ask one question per turn, including the narrowing question?
3. Does each of the five headings cover the points listed?
4. Does it avoid everything under "should not do"?
5. Is every citation either in the verified list or marked unverified?
6. Does it end by offering the six follow-ups? Ask for the follow-up the case shows in full and compare: is it built from the case's answers, and does it use only tools and partners from the playbook?

Case 6 is the most sensitive test: a prompt change that makes the assistant more eager to recommend technology will show up there first.
