# Case 2: Siting boreholes fairly across districts

| | |
|---|---|
| **Domain** | Water, sanitation and hygiene (WASH) |
| **Intervention type** | Irreversible infrastructure investment |
| **Expected class** | 2 — Static Demographic Targeting (welfare ILP) |
| **Most likely confusion** | A need-score ranking in a spreadsheet |

## Scenario

A rural water NGO has a donor grant for 25 boreholes in a drought-prone region of 300 villages across 4 districts. District governments and the donor require that the selection be fair across districts and publicly defensible.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We're drilling 25 boreholes. The aim is to get as many people as possible within a 30-minute walk of safe water. Once a borehole is drilled it stays there for 20 years; it can't be moved. A working borehole meets the need directly: people walk to it and collect water.

**Filter 2 — Choice and preferences.**
> We choose the sites, in consultation with district water officers. Villages want boreholes but don't get to bid or rank; they can't turn one down in any meaningful sense.

**Filter 3 — Environment dynamics.**
> Passive. Nobody is avoiding us. Population shifts slowly, over years.

**Filter 4 — Tolerance for being wrong.**
> A bad site is a 20-year mistake and a political problem: last time, two districts complained that a third got most of the wells. Nobody dies directly from one wrong site, but we can't redo it. We have a 2023 household census with village populations and GPS points, and a hydrogeology survey showing which sites can be drilled.

**Filter 5 — Field data and workflow friction.**
> This is a one-off decision. Our program team uses Excel and QGIS. The district councils will want to see the reasoning.

## Why Class 2: Static Demographic Targeting

The assistant should select **Class 2 (Static Demographic Targeting)**, solved with a welfare integer linear program.

- **Irreversible capital** (Filter 1 — The resource and its intent) and **central assignment** (Filter 2 — Choice and preferences) point straight to Class 2 (Static Demographic Targeting).
- **Passive, slow-moving environment** (Filter 3 — Environment dynamics): no adversary, no drift to track, so Class 1 (Dynamic State Evolution) and Class 3 (Spatiotemporal Security & Adaptive Search) don't apply.
- **Costly but not catastrophic error, with good data** (Filter 4 — Tolerance for being wrong): one-time census data is enough, and there is no unknown shock to hedge against, so Class 4 (Robust Contingency Planning) isn't needed.
- **Fairness and auditability are explicit requirements**, which is exactly what an integer program with an equity constraint can state and prove.

## What a good recommendation contains

**1. Class.** An integer linear program: a *maximal covering location* model that chooses 25 drillable sites to maximize the population within walking distance, with a maximin (or leximin) fairness rule across the 4 districts, such as "every district reaches at least X% coverage, and the worst-off district is made as well off as possible."

**2. Counterfactual warning.** Ranking villages by a need score and drilling the top 25 double-counts: two neighboring top-ranked villages each get a borehole even though one would serve both, and coverage clusters in whichever district has the highest scores. That is precisely the complaint from last time. A machine-learning poverty model can improve the need score but cannot decide *placement*, because the value of a site depends on which other sites are chosen.

**3. Field pathway.** This is solved once, centrally, by an analyst using a free solver (for example PuLP with CBC, or QGIS plus a solver plugin). Field staff and councils never see equations; they get a map and a table listing each chosen site, the villages it covers, the population served, and each district's coverage figure. Publishing a short "why these sites" note, plus a comparison against the need-ranking approach, makes the decision auditable.

**4. Evidence.** The maximal covering location problem (Church & ReVelle, 1974) is the standard formulation for siting facilities to maximize coverage and is widely used for clinics, schools and water points. For the fairness layer, leximin selection has been used in practice to choose citizens' assemblies (Flanigan et al., Nature 2021); the parallel is a transparent rule that protects the worst-off group, here districts rather than demographic quotas.

**5. Report card.**
- *Successes:* by construction, an optimal covering solution serves at least as many people (as modeled) as any ranking-based choice of the same number of sites, and a written fairness rule turns a political argument into an agreed parameter.
- *Challenges:* walking-distance estimates from straight-line GPS distance can be badly wrong in hilly terrain; validate with local staff. Hydrogeology failure rates mean some chosen sites may come up dry, so keep ranked backup sites.
- *Unknowns:* how the councils will weigh total coverage against district equity. Present two or three options (pure coverage, maximin, a middle ground) and let them choose.

**Next steps.** Build the village × candidate-site walking-distance table; agree the fairness rule with district officers *before* running the model; produce the map and comparison table for the donor.

## What the assistant should *not* do

- Recommend a restless bandit or any adaptive method; there is no repeated decision.
- Treat a poverty-prediction model as the answer; at most it feeds the need weights.
