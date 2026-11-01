# Case 14: Cash before a river flood

| | |
|---|---|
| **Domain** | Disaster risk and social protection |
| **Intervention type** | One-off cash transfer released on a forecast |
| **Expected class** | [4 — Robust Contingency Planning (forecast trigger)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning), with a [Class 2 — Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) layer for who receives the cash |
| **Combination** | [4 + 2: when to act, then who gets it](../../prompt/knowledge/taxonomy.md#5-when-two-classes-combine) |
| **Most likely confusion** | Treating it as targeting alone (Class 2) and paying after the flood, or as routing (Class 9) when the money moves by mobile phone |
| **In-depth tutorial** | [Anticipatory action: when should the cash go out before a flood?](../tutorials/14-anticipatory-cash-flood-trigger.md) (the trigger, the cost-loss rule, a robust threshold and the list). Background: [robust pre-positioning](../tutorials/04-robust-optimization-cyclone-prepositioning.md) and [welfare optimization](../tutorials/02-welfare-optimization-borehole-siting.md) |

## Scenario

A humanitarian NGO works in a lower river district where the river floods most years and floods badly about one year in four. It has a contingency fund of $500,000 for the coming monsoon, enough for $50 to each of 10,000 households. Last year it paid after the water receded, three weeks after the peak, by which time families had skipped meals, sold livestock cheaply and borrowed at high interest. A donor will now let it pay **before** the peak if the trigger is agreed in advance. The national flood forecasting service publishes a daily bulletin with river-level forecasts up to 5 days ahead. The NGO's 2024 household survey covers 40,000 households in six flood-prone areas, 70% of them with a mobile-money account.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> $500,000 in cash, $50 per household, to help families eat and protect their animals and belongings when a big flood is coming, instead of after it.

*Next turn, which fits best:*
> (a), handed over once. Each household gets one transfer in a season.

**Filter 2 — Choice and preferences.**
> We decide, with the district disaster committee. Households don't choose anything; local committees check the list.

**Filter 3 — Environment dynamics.**
> Nobody is avoiding us. If people knew a list was being drawn up, some might claim to live closer to the river, so the list was made from last year's survey, before any of this was announced.

**Filter 4 — Tolerance for being wrong.**
> Paying too late harms lives: families go without food and sell what they need to recover. Paying for a flood that doesn't come wastes money the donor won't give twice.

*Next turn, what records:*
> Twelve years of river levels at the main gauge and the forecasts issued before each peak. Three of those years had severe floods. And the 2024 household survey.

**Filter 5 — Field data and workflow friction.**
> Field staff use a phone survey app and update the household list once a year. The forecast bulletin comes by email every morning. Payments go through a mobile-money provider, which needs the list two days ahead.

*Next turn, who would run it:*
> Our program officer, in Excel. The decision to release money would be the country director's.

**Narrowing 1 — "Do you know everyone who could receive it before you decide, or do people or items arrive one at a time and need a decision on the spot?"**
> We know them all: the 40,000 surveyed households. We'd choose the 10,000 before the season.

**Narrowing 2 — "Do you have pilot or trial results showing the program helps some kinds of people much more than others?"**
> No. We've never paid before a flood.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> Yes: when to pay. That's the hardest part. Too early and the flood may not come; too late and it's the same as last year.

## Why Class 4 with a Class 2 layer

The assistant should select **[Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning)** as the primary class, in its anticipatory-action form, with **[Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)** as the layer that decides who receives the cash.

- **One-off transfer, everyone known up front, no trial data** (Filter 1, narrowing 1 and 2). On its own this is Class 2: choose 10,000 of 40,000 households under a budget.
- **Catastrophic if late, wasteful if early, with only three severe floods on record** (Filter 4). That is the Class 4 signature: plan for bad cases when history is too thin to trust an average.
- **The second decision is when to act** (second-decision question), and the user calls it the hardest part. So the trigger is the primary decision and the targeting is the layer: the list is drawn up once before the season; the trigger is what the director must get right under pressure.
- **Not [Class 9 (Routing & Logistics)](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics).** The cash moves by mobile money; there are no trucks or routes to plan. For the 30% without accounts, a cash-point plan is an operations task, not a model.
- **Not [Class 7 (Effect-Based Targeting)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting).** There is no trial showing who gains most from early cash (narrowing 2). Target by exposure and need, and record outcomes so a later season can ask the effect question.
- **Gaming is contained** (Filter 3) because the list comes from a survey taken before the program was announced; keep it that way by not reopening registration during the season.

## What a good recommendation contains

**1. Class.** Anticipatory action, a form of Class 4: agree in advance a forecast threshold, the action it releases (a $50 transfer to a fixed list) and the money behind it. Choose the threshold, and how much of the fund to keep back for a missed flood, by checking each option against all twelve past seasons and against worse cases experts can describe (a forecast that arrives late; a flood the gauge under-predicts). Layer: choose the 10,000 households from the survey with a small integer program or a ranked list, maximizing expected flood exposure weighted by need, with a minimum share for each of the six areas.

**2. Counterfactual warning.** Last year's after-the-flood payment is the failure the program exists to fix. A "smart" alternative fails differently: a machine-learning flood model built from twelve seasons would be fitted to three severe floods and would look accurate on paper while missing the fourth. Waiting for certainty means paying after the peak again.

**3. Field pathway.** One laminated **trigger card** on the director's desk: "If the morning bulletin forecasts the main gauge above [threshold] within 5 days, release the transfer to List A today; if the forecast falls back, there is no second release this season." The program officer keeps List A (10,000 households) in Excel, sends it to the mobile-money provider at the start of the season, and keeps List B (the next 2,000) for areas a forecast singles out. Field staff phone a sample of recipients within a week.

**4. Evidence.** WFP sent anticipatory cash by mobile money to pre-registered households in Bangladesh about five days before the July 2020 flood peak; recipients were 36% less likely to go a day without eating during the flood (Pople, Hill, Dercon & Brunckhorst, CSAE working paper 2021; later published in the World Bank Economic Review). OCHA and the CERF activated an anticipatory-action pilot in Somalia in 2020 on a pre-agreed trigger, and GiveDirectly sent cash ahead of forecast floods in Kogi State, Nigeria, in 2024. For targeting, Aiken et al. (Nature, 2022) show how much a better targeting method gains over simple geographic targeting in another emergency transfer, and how much a full registry would have gained over both.

**5. Report card.**
- *Successes:* the Bangladesh study is a rare quasi-experimental estimate showing that timing matters for food security.
- *Challenges:* a threshold agreed in advance must actually be honored on the day; the 30% without mobile money are often the poorest; a forecast that triggers in only one or two areas needs a rule for which households are paid.
- *Unknowns:* how often the main gauge's 5-day forecast misses a severe flood (twelve seasons give only a rough answer); whether $50 is enough to change what families do; whether a false alarm costs the program the community's trust.

**6. Simpler alternative.** Each layer has one.
- *Trigger:* a calculator table. For each candidate threshold, count over the twelve seasons how often it would have fired before a severe flood (hits), fired with no severe flood (false alarms) and stayed silent before one (misses). Choose the threshold with the fewest misses the donor's false-alarm tolerance allows, and keep part of the fund for a missed flood. This is close to the full method when the forecast record covers the kinds of flood that matter; it gives up the expert scenarios beyond the record. Check: are any of the twelve seasons like the worst floods older staff remember? If not, add those scenarios before choosing.
- *Targeting:* every surveyed household in the lowest-lying villages, in order of a simple need score (children under 5, no regular income), until 10,000 are reached. This is close when exposure is mostly a matter of location. Check: do the six areas each get a fair share? If not, add a per-area floor, the greedy-with-a-floor rule from the [borehole tutorial](../tutorials/02-welfare-optimization-borehole-siting.md#the-simpler-alternative-greedy-with-a-floor-in-a-spreadsheet). Simple geographic rules are a serious benchmark for cash targeting (Hanna & Olken, 2018), though better data can reduce exclusion errors (Aiken et al., 2022).

Together, a calculator trigger and a geographic list is a sound first season. The model's value is mostly in the trigger, when experts can describe floods the record doesn't contain.

**Next steps.** Build the twelve-season table of forecasts against what happened; agree the threshold, the reserve and the trigger card with the donor and the district committee before the monsoon; check List A's coverage of households without mobile money and plan cash points for them.

## What the assistant should *not* do

- Recommend targeting alone ([Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)) with payment after the flood, which repeats last year.
- Build a flood-prediction model from twelve seasons, or promise this district Bangladesh's 36%.
- Leave the trigger to judgment on the day. The point of anticipatory action is that the decision is made, and funded, in advance.
- Treat mobile-money delivery as a routing problem ([Class 9](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics)).

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 3** in full, because in a combination the order of the pilots matters; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

| Element | For this program | From |
|---|---|---|
| Trigger variable | The main gauge's forecast level in the morning bulletin, at up to 5 days' lead | Filters 4 and 5 |
| Threshold | Chosen from the twelve-season table, then checked against expert scenarios of worse or faster floods | Filter 4 |
| Action | $50 by mobile money to each household on List A, once per season | Filter 1 |
| Reserve | The share of $500,000 kept for a flood the trigger misses, agreed with the donor | Filter 4 |
| Eligible households | The 40,000 in the 2024 survey; no new registration during the season | Filters 2 and 3 |
| Targeting rule (layer) | Expected flood exposure (village elevation, past flood depth) weighted by need, 10,000 households, a floor for each of the six areas | Narrowing 1; Filter 2 |
| Partial trigger | If only some areas are forecast to flood, pay List A households in those areas first, then List B there | Filter 4 |
| Decision owner | The country director, bound by the trigger card | Filter 5 |
| Delivery | Mobile-money list sent two days ahead; cash points for the 30% without accounts | Filter 5 |

It should also flag the gap that matters most: **twelve seasons with three severe floods cannot show how often the forecast misses.** Ask the forecasting service for its own verification statistics, and add expert scenarios for what the record lacks.

### Follow-up 3: Pilot design

A flood trigger can't be piloted by waiting for floods, so the pilot has two parts, one per layer, in order:

1. **Before the season: backtest the trigger.** Replay the twelve seasons under the calculator threshold and the robust choice, and score each on hits, misses, false alarms and days of lead before the peak. Then run a tabletop exercise: on a simulated morning bulletin, the director, the program officer and the mobile-money provider go through the trigger card and time each step. The trigger is tested first because the targeting list is useless if the money arrives late.
2. **During the season: check the list.** When the trigger fires (or, if it doesn't, during a smaller flood), phone a random sample of 300 List A households and 300 surveyed households not on the list in the same villages, within two weeks of the peak. Compare days without food, livestock sold and debt taken on. This is an observational comparison, not a trial; say so in reports.
3. **Harm measure:** households in flooded villages who were not on the list, and complaints to the district committee.

### The other follow-ups, in brief

- **2. Readiness checks:** the trigger, reserve and card signed by the donor before the monsoon; the mobile-money provider's two-day lead time confirmed; a plan for households without accounts; the list's age and need data checked for gaps in the poorest areas.
- **4. Build options:** Excel for the twelve-season table and the list; PuLP if the per-area floor needs an integer program; the Anticipation Hub's guidance on triggers. Partners with forecast expertise (the national service, a university hydrology group) matter more than software. Confirm each tool and partner is still active before relying on it.
- **5. Reading and contacts:** Pople et al. (2021) on the Bangladesh transfers; the OCHA lessons from the 2020 Somalia pilot; Aiken et al. (2022) and Hanna & Olken (2018) on targeting.
- **6. Brief:** fill the playbook template, with the trigger as the decision, targeting as the layer, and both simpler options under "Simpler option to beat".
