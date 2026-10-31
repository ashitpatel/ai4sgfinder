# Worked cases

Six illustrative cases that together exercise every outcome the assistant can reach: one per allocation class, plus one where the right answer is "no model." Each spans a different impact domain and intervention type.

All organizations and programs in these cases are fictional. The research they cite is real and is drawn from the verified references in [`taxonomy.md`](../../prompt/knowledge/taxonomy.md).

## Coverage

| Case | Domain | Intervention type | Expected outcome | Deciding filter |
|------|--------|-------------------|------------------|-----------------|
| [1. CHW hypertension visits](01-chw-hypertension-visits.md) | Primary health care | Recurring behavioral nudge | **Class 1** Dynamic State Evolution (restless bandits) | 1 (reclaimable, probabilistic) + 5 (weekly data) |
| [2. Borehole siting](02-borehole-siting.md) | Water and sanitation | Irreversible infrastructure | **Class 2** Static Demographic Targeting (welfare ILP) | 1 (irreversible capital) |
| [3. Marine patrols](03-marine-patrols.md) | Conservation | Mobile enforcement | **Class 3** Spatiotemporal Security & Adaptive Search (security games) | 3 (adaptive adversary) |
| [4. Cyclone pre-positioning](04-cyclone-prepositioning.md) | Disaster preparedness | Contingency stockpiling | **Class 4** Robust Contingency Planning (DRO over a location model) | 4 (catastrophic, little history) |
| [5. Apprenticeship matching](05-apprenticeship-matching.md) | Youth employment | Two-sided placement | **Class 5** Strategic Matching Markets (stable matching) | 2 (both sides choose) |
| [6. Food pantry](06-food-pantry-no-model.md) | Food security | Recurring in-kind distribution | **No model needed** | 4 (supply already meets demand) |

Across the six, every filter is the deciding one at least once, and each case names the method it is most likely to be confused with, so the cases also show what separates neighboring classes.

## Each case contains

- **Scenario**: the organization and its constraint, in a few sentences.
- **Interview answers**: a realistic answer to each of the five filters, written in the user's voice.
- **Why Class N: Name**: the selected class by number and name, how the answers map through the decision tree, and which classes are ruled out and why, each named alongside its number.
- **What a good recommendation contains**: the key points under each of the five required headings.
- **What the assistant should not do**: the most likely wrong answers.

## Using the cases

**To learn the method.** Read the "Why Class N" sections side by side; the contrast between cases 1 and 2 (nudge vs. capital) and between cases 2 and 5 (central assignment vs. two-sided choice) shows the decision tree at work.

**To demo the assistant.** Start a chat on any platform, then paste the case's interview answers one at a time as the assistant asks each filter.

**To test a prompt change.** After editing `prompt/system-prompt.md`, run all six cases and check each final recommendation against the case:
1. Does it reach the expected outcome?
2. Did it ask one filter per turn?
3. Does each of the five headings cover the points listed?
4. Does it avoid everything under "should not do"?
5. Is every citation either in the verified list or marked unverified?

Case 6 is the most sensitive test: a prompt change that makes the assistant more eager to recommend technology will show up there first.
