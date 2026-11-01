# Case 11: Placing refugee families as they arrive

| | |
|---|---|
| **Domain** | Refugee resettlement and employment |
| **Intervention type** | One-time placement of arrivals under yearly quotas |
| **Expected class** | [10 — Online Assignment & Waitlists (online allocation)](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists) |
| **Most likely confusion** | Assigning the whole year's families at once with an integer program, or a stable match between families and cities |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/11-online-assignment-refugee-placement.md) |

## Scenario

A national resettlement agency works with local partner offices in 30 cities. Each city agrees a yearly quota of refugee families it can receive, and families are referred to the agency a few at a time throughout the year. Caseworkers currently pick a city for each family by judgment and by whichever quota still has room. The agency's goal is that an adult in each family has a job within six months of arrival.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> We're allocating places in our 30 partner cities. The goal is for each family to have someone working within six months. Each family is placed once and stays; we don't move them afterwards.

**Filter 2 — Choice and preferences.**
> We decide, within each city's yearly quota. Families don't rank cities, and cities accept the families we send as long as the quota has room.

**Filter 3 — Environment dynamics.**
> No one avoids us. Families have no reason to change their answers; the information comes from their case files.

**Filter 4 — Tolerance for being wrong.**
> A poor placement hurts a family's chances of finding work, and that matters a lot to them, but it isn't life-threatening, and a family can move later on its own. We have five years of records: every family's placement city and whether they were employed at six months.

**Filter 5 — Field data and workflow friction.**
> Caseworkers enter everything into a web database as each case comes in; it's always online at our head office. One analyst on our data team could run a model, but caseworkers make the final call.

**Narrowing — "Do you know everyone who could receive it before you decide, or do people or items arrive one at a time and need a decision on the spot?"**
> They arrive a few at a time all year. Each family needs a city within about a week of referral, and we don't know who will come next month.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> Only the employment predictions for each family in each city, which this already needs.

## Why Class 10: Online Assignment & Waitlists

The assistant should select **[Class 10 (Online Assignment & Waitlists)](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists)**: predict each family's chance of employment in each city, then assign each arrival under the quotas while holding back capacity for families still to come.

- **Placed once and kept** (Filter 1 — The resource and its intent) and **we decide centrally** (Filter 2 — Choice and preferences) put this in the *Who gets a limited resource* family.
- **Nobody avoids or games the agency** (Filter 3 — Environment dynamics), so [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) does not apply. **A costly but not catastrophic error, with five years of outcome records** (Filter 4 — Tolerance for being wrong), so [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) is not needed and there is enough history to predict employment.
- **The narrowing answer is decisive:** families arrive a few at a time and each needs a city within a week. That rules out [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting), which assigns everyone at once from a known list; this agency never has the whole year's families in front of it. The second narrowing question (trial results for Class 7) is not needed.
- **Families do not rank cities and cities do not rank families**, so [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) does not apply. Each family is placed once, not revisited each week, so [Class 1 (Dynamic State Evolution)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) does not either.

## What a good recommendation contains

**1. Class.** Online assignment in two parts. A *prediction model*, trained on the five years of records, estimates each family's chance of employment at six months in each of the 30 cities. An *assignment model* then places each new family in the city that does best for it **and** for the families still likely to arrive, given each city's remaining quota and a forecast of future arrivals from past years. Fairness rules hold across the whole year, not just for each decision. The research behind this comes from Alex Teytelboym (Oxford) and Andrew Trapp (WPI) and colleagues, who built Annie MOORE for HIAS.

**2. Counterfactual warning.** Placing each family in its single best-predicted city as it arrives uses up the strongest cities' quotas early in the year; families who arrive in the autumn get whatever is left, regardless of fit. Assigning by "which quota has room" ignores fit altogether. A prediction model on its own does neither job: it says where a family might do well, not how to share 30 quotas across a year of unknown arrivals.

**3. Field pathway.** The analyst refreshes the prediction model once a year and keeps the assignment script running against the web database. When a caseworker opens a new case, the database shows the top two or three suggested cities, each with its predicted employment chance and a one-line reason ("strong demand for the family's trade; quota 40% used"). The caseworker chooses; if they set the suggestion aside, they pick a reason from a short list, and the analyst reviews overrides monthly.

**4. Evidence.** Ahani et al. (Operations Research, 2021) predict each family's chance of employment in each location and assign with an integer program; this is the basis of Annie MOORE, used by the US resettlement agency HIAS. Their backtests on past HIAS data suggested a 22–38% gain in short-run employment. That is a backtest, not a randomized trial. Ahani et al. (Operations Research, 2024) extend this to families arriving through the year, evaluated on HIAS data and incorporated into Annie MOORE: the closest parallel to this agency. Manshadi, Niazadeh & Rodilitz (Management Science, 2023) on fair dynamic rationing and Arnosti & Shi (Management Science, 2020) on housing lotteries and waitlists are parallels from other domains, not refugee deployments; they show how to keep allocation over time fair.

**5. Report card.**
- *Successes:* a resettlement agency, HIAS, uses the approach in its placement work; backtests on its past data point to a meaningful gain in short-run employment.
- *Challenges:* caseworkers must trust suggestions they did not make, so each placement needs a plain explanation; the model can only learn from cities and kinds of families that past placements covered.
- *Unknowns:* no randomized evidence on the employment gain; whether the predictions are equally accurate for every nationality and family type; whether this year's arrivals resemble the last five years.

**6. Simpler alternative.** Greedy from a printed table with quarterly allotments: the caseworker looks up the family type's predicted chance in each city and picks the highest city with room, but no city may use more than a quarter of its quota per quarter (cumulative). In the [tutorial](../tutorials/11-online-assignment-refugee-placement.md#the-simpler-alternative-greedy-with-quarterly-allotments) it captured about 72% of weekly re-solving's gain over first-available, kept early and late arrivals within 3 points of each other, and held up when the arrival mix was the reverse of the forecast (illustrative data). It is close on fairness over time; it gives up the look-ahead that saves a city's places for the families who gain most there. Check before settling for it: arrivals are spread fairly evenly through the year (otherwise shape the allotments to the expected pattern), and the predicted chances are trustworthy, since both rules depend on them. Replaying last year under both rules shows the agency its own gap.

**Next steps.** Pull the five years of records into one table (family characteristics, city, employed at six months); agree the year's fairness rules with the partner cities; replay last year's arrivals through a simple version of the model and compare it with what caseworkers actually did.

## What the assistant should *not* do

- Recommend assigning all of the year's families at once (Class 2 (Static Demographic Targeting)); the agency never has the full list.
- Recommend a stable match (Class 5 (Strategic Matching Markets)); nobody ranks anybody.
- Present the 22–38% figure as a measured result of a trial, or promise this agency a similar gain.
- Let the model place families with no caseworker override and no explanation the family can be given.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

| Element | For this program | From |
|---|---|---|
| Arrivals | Refugee families, referred a few at a time all year; each needs a city within about a week | Filter 2; narrowing answer |
| Destinations | 30 partner cities, each with a yearly quota of families | Filters 1 and 2 |
| Value of a placement | Predicted chance that someone in the family is employed at six months in that city, learned from five years of records | Filters 1 and 4 |
| Forecast | Expected arrivals by month and family type for the rest of the year, from the same five years, so quotas in the strongest cities are not used up by spring | Filter 4 |
| Fairness over time | Ask: should families arriving late in the year get placements as good, on average, as early ones? Should every city receive a mix of families, not only those predicted to do best there? | Filter 2 and ethics |
| Decision speed | One suggestion per family within the week, shown in the web database; the analyst maintains the script | Filter 5 |
| Override | Caseworkers may set any suggestion aside; each override and its reason is recorded and reviewed monthly | Ethics |
| Explanation | Each suggestion carries a one-line reason a caseworker can pass on to the family | Ethics |

It should also flag a gap and an extension. **The gap:** ask whether some families must go to a particular city (relatives already there, medical needs only some cities can meet); those are fixed before the model runs and count against the quota. **The extension:** families do not rank cities today. If the agency later asks families for their preferences, those can be added as a secondary layer with Class 5 elements, but that changes the design and should be a separate decision.

### Follow-up 6: One-page brief for a technical partner

```
PROJECT BRIEF — National refugee resettlement agency (illustrative)

The decision we need help with
  Choose one of 30 partner cities for each refugee family as it is
  referred, a few families at a time all year, within each city's quota.

Why it matters
  The goal is a job within six months. Placements today are by caseworker
  judgment and whichever quota has room, so fit is uneven and late-year
  families get whatever is left.

Current approach
  Caseworkers pick a city within about a week of referral, using the web
  database to see remaining quotas. No prediction or forecast is used.

Recommended approach
  Class 10 (Online Assignment & Waitlists): predict employment for each
  family in each city, then assign each arrival under the quotas while
  reserving capacity for families likely to arrive later in the year.

Simpler option to beat
  Greedy placement from a printed table of predicted chances, with quarterly
  allotments per city. Close on fairness over time; misses look-ahead.

Data we have
  Five years of placements: family characteristics, city, and employment
  at six months, in our web database. Monthly arrival counts by year.

Constraints
  30 city quotas per year. Some families must go to a fixed city.
  Fairness across the year and across cities (rules to be agreed).
  Caseworkers keep the final decision; overrides are recorded.

What success looks like
  Higher employment at six months than current practice in a replay of
  last year. Harm measure: employment gap between early- and late-year
  arrivals, and prediction accuracy by nationality.

How results must reach staff
  Top 2-3 suggested cities with a one-line reason in the web database.
  Our analyst runs and maintains the model.

What we are asking for
  A replay of last year's arrivals, then a one-season shadow run in
  which caseworkers see suggestions before deciding.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** five years of arrival and outcome records exceed the one-year minimum; agree the season's fairness rules with the partner cities before the model runs; check prediction accuracy by nationality and family type; confirm families' consent covers using their data this way; write the override reasons list.
- **3. Pilot design:** replay last year's arrivals through the model and through actual caseworker choices, comparing predicted employment and the early/late gap; then run one season in shadow, with caseworkers seeing the suggestion before deciding.
- **4. Build options:** no dedicated package; a prediction model (for example scikit-learn) plus an assignment model in PuLP or Google OR-Tools, re-solved as each family arrives. INFORMS Pro Bono Analytics or a university operations-research department fits best. Confirm any tool or partner is still active before relying on it.
- **5. Reading and contacts:** start with Ahani et al. (2021) on Annie MOORE, then Ahani et al. (2024) on dynamic placement and Manshadi, Niazadeh & Rodilitz (2023) on fair dynamic rationing. Alex Teytelboym (Oxford) and Andrew Trapp (WPI) work on exactly this problem.
