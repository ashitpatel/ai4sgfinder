# Case 2: Siting boreholes fairly across districts

| | |
|---|---|
| **Domain** | Water, sanitation and hygiene (WASH) |
| **Intervention type** | Irreversible infrastructure investment |
| **Expected class** | [Class 2: Static Demographic Targeting (welfare ILP)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) |
| **Most likely confusion** | A need-score ranking in a spreadsheet |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/02-welfare-optimization-borehole-siting.md) |

## Scenario

A rural water NGO has a donor grant for 25 boreholes in a drought-prone region of 300 villages across 4 districts. District governments and the donor require that the selection be fair across districts and publicly defensible.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We're drilling 25 boreholes. The aim is to get as many people as possible within a 30-minute walk of safe water. Once a borehole is drilled it stays there for 20 years; it can't be moved. A working borehole meets the need directly: people walk to it and collect water. So it's (a): handed over once and kept.

**Filter 2 — Choice and preferences.**
> We choose the sites, in consultation with district water officers. Villages want boreholes but don't get to bid or rank; they can't turn one down in any meaningful sense.

**Filter 3 — Environment dynamics.**
> No. Nobody is avoiding us, and villages don't apply, so there are no answers to game; we work from the census. Population shifts slowly, over years.

**Filter 4 — Tolerance for being wrong.**
> A bad site is a 20-year mistake and a political problem: last time, two districts complained that a third got most of the wells. Nobody dies directly from one wrong site, but we can't redo it. We have a 2023 household census with village populations and GPS points, and a hydrogeology survey showing which sites can be drilled. No pilot or trial results.

**Filter 5 — Field data and workflow friction.**
> This is a one-off decision. Our program team uses Excel and QGIS; our GIS officer would run the tool, probably with outside help to set it up. The district councils will want to see the reasoning.

**Narrowing question 1 — Who gets a limited resource.** *"Do you know everyone who could receive it before you decide, or do people or items arrive one at a time and need a decision on the spot?"*
> We know them all up front: the 300 villages are in the census, and we pick all 25 sites in one go.

**Narrowing question 2 — Who gets a limited resource.** *"Do you have pilot or trial results showing the program helps some kinds of people much more than others?"*
> No. A borehole helps everyone within walking distance; what matters is how many people that is.

## Why Class 2: Static Demographic Targeting

The assistant should select **[Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)**, solved with a welfare integer linear program.

- **Handed over once and kept** (Filter 1 — The resource and its intent) and **central assignment** (Filter 2 — Choice and preferences) place the problem in the *Who gets a limited resource* family.
- **Everyone is known up front** (narrowing question 1), which rules out [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists); that class is for families or items arriving one at a time.
- **No trial results, and the benefit doesn't vary much by who receives it** (narrowing question 2; Filter 4), which rules out [Class 7: Effect-Based Targeting](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting). Together the two answers point to Class 2: Static Demographic Targeting.
- **Passive, slow-moving environment** (Filter 3 — Environment dynamics): no adversary, no one gaming a rule, no drift to track, so [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) and [Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) don't apply.
- **Costly but not catastrophic error, with good data** (Filter 4 — Tolerance for being wrong): one-time census data is enough, and there is no unknown shock to hedge against, so [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) isn't needed.
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

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 4** in full, because it shows how the assistant narrows a list of tools and partners down to one choice for this program.

### Follow-up 4: Build options — tools and partners

A good answer starts from what this program needs, then narrows down:

**What the build has to do** (from the interview): a one-off decision; about 300 villages and the drillable candidate sites; 25 picks; a fairness rule across 4 districts; results that district councils can audit; a team that uses Excel and QGIS (Filter 5 — Field data and workflow friction).

**Software, narrowed:**

| Option | Verdict for this program |
|---|---|
| [PuLP](https://coin-or.github.io/pulp/) with the free [HiGHS](https://highs.dev) solver | **Recommended.** A covering model of this size typically solves in seconds. The result is a short Python script an analyst can rerun when the fairness rule changes, and it can write a CSV that QGIS maps directly. |
| [Google OR-Tools](https://developers.google.com/optimization) | Equally capable. Choose it only if your technical partner already uses it. |
| [Pyomo](https://www.pyomo.org) | More than this problem needs; worth it only if the model later grows into a multi-year investment plan. |
| Excel's built-in Solver | **Not suitable.** The standard Solver handles at most 200 decision variables, and this model needs one per candidate site and one per village. |

**Partner, narrowed:**

- **[INFORMS Pro Bono Analytics](https://connect.informs.org/probonoanalytics/nonprofits)** is the best fit: its volunteers are operations-research specialists, and facility siting is a textbook operations-research problem. It is free; the NGO commits staff time.
- **A university operations-research or industrial-engineering department** is the alternative, as a student capstone with faculty supervision. Slower, but often free.
- **General data-science volunteers** (for example DataKind) are a weaker fit: the hard part here is the optimization model, not machine learning.

**What to hand over:** a village table (ID, population, GPS point, district), a candidate-site table (ID, GPS point, drillable yes/no from the hydrogeology survey), the 30-minute walking threshold, and the fairness options for the councils to choose from.

**What to ask for back:** the script, a map, a table of chosen sites with the villages and population each covers, each district's coverage, a comparison against the need-score ranking, and a few runs with different fairness rules.

### The other follow-ups, in brief

- **1. Fit the model:** decision = which 25 drillable sites; objective = population within a 30-minute walk; constraints = budget of 25, one borehole per site, a minimum coverage share per district (or maximize the worst-off district).
- **2. Readiness checks:** agree the fairness rule with district officers *before* seeing results; replace straight-line distances with walking times checked by local staff; keep ranked backup sites in case boreholes come up dry.
- **3. Pilot design:** this is a one-off decision, so compare plans rather than run a trial: the model's plan against the need-score ranking, on coverage and district equity, reviewed with the councils.
- **5. Reading and contacts:** the integer-programming chapters of *Applied Mathematical Programming* (free from MIT), then Church & ReVelle (1974) on covering location.
- **6. Brief for a technical partner:** the "what to hand over" list above, plus the councils' complaint from last time, makes most of the brief.
