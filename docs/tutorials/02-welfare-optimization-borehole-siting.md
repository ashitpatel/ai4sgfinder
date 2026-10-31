# Welfare Optimization Masterclass: Where to Drill 25 Boreholes, Fairly

*An in-depth walkthrough of covering models, integer linear programming and fairness rules, built on [Case 2: Siting boreholes fairly across districts](../cases/02-borehole-siting.md).*

**You need:** proportions, means, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting). **Code:** [`code/case2_welfare_ilp.py`](code/case2_welfare_ilp.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A rural water NGO has a donor grant for 25 boreholes in a drought-prone region of 300 villages across 4 districts. The aim is to get as many people as possible within a **30-minute walk** of safe water. The team has a 2023 household census (village populations and GPS points) and a hydrogeology survey showing which candidate sites can be drilled. A borehole stays where it is for 20 years. Last time, two district councils complained that a third district got most of the wells.

The usual answer is a spreadsheet: give each village a need score, sort, and drill next to the top 25. It fails in two ways. Neighboring villages near the top of the list each get a borehole even though one would serve both, so boreholes are wasted on people who were already covered. And the top of the list clusters wherever the biggest villages are, which is exactly what the councils complained about.

This tutorial builds the alternative step by step:

1. **Chapter 1** turns the question into a *covering model*: yes/no choices, a goal, and rules.
2. **Chapter 2** names what makes this hard: overlapping catchments, fairness between districts, and no second chances.
3. **Chapter 3** turns the census and GPS points into a table of who can reach which site, and checks how much the answer depends on the inputs.
4. **Chapter 4** solves a small example by hand, adds a fairness rule, and shows how a solver searches.
5. **Chapter 4.5** scales up to 300 villages, with backup sites for dry boreholes and fairness options for the councils.
6. **Chapter 5** runs it all in code and compares the plans.
7. **Chapter 6** summarizes every piece on one page.

The idea that ties it together: **a site's value depends on which other sites you pick, so choose the 25 together, not one at a time.**

---

## Chapter 1: The Covering Leap – From a Ranked List to a Covering Model

### Why a ranked list is the wrong shape

A ranking gives each village a score on its own and takes the top of the list. That works when each choice's value stands alone, like handing out 25 identical grants. A borehole is different. It serves every village within a 30-minute walk, so the second borehole in a cluster adds little if the first already reaches the same people. **The value of a site depends on which other sites are chosen.** A list can't express that; a model that looks at all 25 choices at once can.

### The three parts of an optimization model

An **optimization model** is a precise statement of a choice. It always has three parts:

1. **Decision variables:** the things you choose. Here there is one per candidate site: $x_j = 1$ means "drill at site $j$", $x_j = 0$ means "don't." A variable that can only be 0 or 1 is called **binary**. We also add one bookkeeping variable per village: $y_i = 1$ if village $i$ ends up within a 30-minute walk of a borehole, $0$ if not.
2. **Objective:** the single number you want as large (or as small) as possible. Here, the number of people covered: add up the populations $p_i$ of every covered village.
3. **Constraints:** the rules every acceptable plan must obey. Here: exactly 25 boreholes, drill only at drillable sites, and a village counts as covered only if at least one chosen site is within reach.

Written out, with $N_i$ standing for "the list of drillable sites within a 30-minute walk of village $i$":

$$
\begin{aligned}
\text{maximize} \quad & \sum_{i} p_i\, y_i && \text{(people covered)} \\
\text{subject to} \quad & \sum_{j} x_j = 25 && \text{(the budget)} \\
& y_i \le \sum_{j \in N_i} x_j \quad \text{for every village } i && \text{(covered only if a chosen site is in reach)} \\
& x_j,\ y_i \in \{0, 1\} && \text{(yes/no choices)}
\end{aligned}
$$

Read the middle rule slowly. The right-hand side counts how many chosen boreholes are within reach of village $i$. If that count is 0, then $y_i$ must be 0: the village can't be counted. If it is 1 or more, $y_i$ may be 1, and because we are maximizing people covered, it will be. A village with two boreholes in reach is still counted once. **That one line is what stops the double counting.**

This is the **maximal covering location problem** of Church and ReVelle (1974), the standard model for siting clinics, schools and water points. Because the objective and the rules are all sums of variables times fixed numbers, it is a **linear** program; because the variables must be whole numbers (0 or 1), it is an **integer linear program**, or **ILP**.

### Mapping it to the program

| Model term | In this program |
|---|---|
| Decision variable $x_j$ | Drill (1) or don't drill (0) at each drillable site from the hydrogeology survey |
| Coverage variable $y_i$ | Village $i$ is within a 30-minute walk of a chosen borehole (1) or not (0) |
| Data $p_i$ | Village population, from the 2023 census |
| Data $N_i$ | Which drillable sites are within a 30-minute walk of village $i$ (Chapter 3 builds this) |
| Objective | People within a 30-minute walk of a borehole |
| Budget constraint | Exactly 25 boreholes |
| Fairness constraint | Every district reaches some share of its people covered (Chapter 4 adds this) |

The model is **static**: it is solved once, not every week. Nothing in the region reacts to the plan, and population shifts over years, not weeks. That is what places it in Class 2 rather than the restless bandits of the [Case 1 tutorial](01-restless-bandits-chw-visits.md).

---

## Chapter 2: The Core Bottleneck – Overlap, Fairness and No Second Chances

### Overlapping catchments

A site's **catchment** is the set of villages it can reach. Catchments overlap: two sites 1 km apart reach mostly the same villages. A spreadsheet that adds up each chosen site's catchment counts the shared villages twice. In the full-size example of Chapter 5, the need-ranking plan's 25 catchments add up to 98,600 people, but only 90,013 different people are actually covered: **8,587 people counted twice.**

### Clustering

The biggest, neediest-looking villages tend to sit together, in the river valley or near market towns. A ranking sends the boreholes there. In Chapter 5's illustrative region, the need ranking puts 15 of 25 boreholes in District A and none in hilly District D. That is the complaint from last time, reproduced by the method.

### Fairness has to be written down

"Fair across districts" means nothing to a computer until it is a rule. Two common versions:

- **A floor:** every district must have at least, say, 20% of its people covered.
- **Maximin:** make the worst-off district as well off as possible. The name is short for *maximize the minimum*.

Both are constraints or objectives the model can obey exactly. The hard part is not the math; it is agreeing the rule with the district officers **before** anyone sees which villages win. Otherwise every rule gets judged by its winners.

### No second chances

A borehole stays put for 20 years. There is no pilot week, no learning from feedback, no correcting next month. That changes what "good" means: the plan must be checked against its inputs *before* drilling (Chapter 3), and it must come with backups for the sites that turn out dry (Chapter 4.5).

---

## Chapter 3: From Census and GPS to Estimates – The Coverage Table

The model needs one table: for every village and every drillable site, **can people walk there in 30 minutes?** Building it is a statistics exercise.

### Step 1: From GPS points to walking minutes

GPS gives the straight-line distance between a village and a site (QGIS's distance-matrix tool computes the whole table). People don't walk in straight lines. Paths go around fields, rivers and hills. A **detour factor** converts one to the other: the ratio of path length to straight-line distance.

$$
\text{walking minutes} = \frac{\text{straight-line km} \times \text{detour factor}}{\text{walking speed (km/h)}} \times 60
$$

With a detour factor of 1.3 and a walking speed of 4 km/h, a village 1.2 km from a site in a straight line is 1.56 km away on foot: **23.4 minutes**, inside the limit. In hilly District D, where the code uses a factor of 1.6, the same straight-line distance takes **28.8 minutes**, just inside. Turned around: 30 minutes reaches 1.54 km in a straight line on ordinary ground, but only 1.25 km in the hills.

Every village–site pair below the 30-minute line gets a "yes" in the coverage table. That table is the $N_i$ lists of Chapter 1.

### Step 2: Check the detour factor with a sample

The detour factor is an estimate, and it's the shakiest input. The case warns that straight-line distances can be badly wrong in hilly terrain. The fix is basic statistics: have local staff walk a random sample of village–site pairs and record the true path length.

Suppose staff walk 30 pairs in District D (simulated in the code). The ratios have:

| Sample size | Mean ratio | Standard deviation | 95% confidence interval |
|---|---|---|---|
| 30 | 1.58 | 0.21 | 1.50 to 1.65 |

The interval is the usual $\bar x \pm 1.96\, s / \sqrt{n}$: $1.58 \pm 1.96 \times 0.21 / \sqrt{30}$. So the planning value of 1.6 is consistent with the sample, and we know the plausible range: 1.50 to 1.65.

### Step 3: Population figures are estimates too

The 2023 census counts are a few years old and contain counting errors. Suppose each village's count has a **standard error** of 5%: roughly, the true figure is within ±10% of the count 95% of the time.

Does that make the "people covered" total shaky? Less than you'd think. If the errors in different villages are independent, they partly cancel when added up. The standard deviation of a sum of independent errors is the square root of the sum of their squares:

$$
\text{sd of total} = \sqrt{\sum_{\text{covered } i} (0.05\, p_i)^2}
$$

For the fair plan of Chapter 5, which covers 86,767 people, that gives a standard deviation of 513 and a 95% interval of **85,761 to 87,773**: about ±1.2%, much tighter than ±10% per village. One caution: this cancelling only happens if errors are independent. If the census undercounted a whole district, every village there is off in the same direction, and the error doesn't shrink.

### Step 4: Sensitivity analysis: does the plan change?

The real question isn't "how precise is the total?" but "**would we drill in different places** if the inputs were a bit different?" A **sensitivity analysis** answers it: change one input, solve the model again, and compare.

The code does this for the two main plans of Chapter 5 (pure coverage and maximin-fair). For each change, it reports how many of the original 25 sites the new best plan keeps, and how much worse the original plan is than re-planning:

| Change | Max-coverage plan: sites kept | People missed by not re-planning | Fair plan: sites kept |
|---|---|---|---|
| Populations each moved randomly by up to 10% (20 tries) | 24.2 of 25 on average (lowest 23) | 0.05% on average (worst 0.14%) | 24.8 of 25 (lowest 24) |
| District D detour factor 1.5 (low end of interval) | 25 of 25 | 0.0% | 25 of 25 |
| District D detour factor 1.65 (high end of interval) | 25 of 25 | 0.0% | 24 of 25 |
| Walking limit 25 minutes instead of 30 | 18 of 25 | 6.2% | 20 of 25 |
| Walking limit 35 minutes instead of 30 | 14 of 25 | 7.2% | 17 of 25 |

The lesson is about where to spend effort. **Population errors of this size barely move the plan.** The detour factor, within its measured range, barely moves it either. **The walking limit moves it a lot**: changing 30 minutes to 35 swaps 11 of the 25 sites. So the 30-minute threshold, and the walking times near it, deserve the most checking with local staff. The changes in this table are illustrative; the method (change an input, re-solve, compare) is what carries over.

---

## Chapter 4: The Decision Engine – Integer Programming with a Fairness Rule

### Step-by-step concrete example: 6 villages, 4 sites, 2 boreholes

Here is a region small enough to check by hand. Two districts, six villages, four drillable sites, and budget for **2** boreholes. To keep the arithmetic simple, the need score is just the village's population.

| Village | District | Population | Nearest site |
|---|---|---|---|
| A | North | 1,000 | S1 |
| B | North | 800 | S2 |
| C | North | 600 | S2 |
| D | North | 500 | S3 |
| E | South | 150 | S4 |
| F | South | 200 | S4 |

North has 2,900 people, South 350, total 3,250.

| Site | Villages within a 30-minute walk |
|---|---|
| S1 | A, B |
| S2 | A, B, C |
| S3 | D |
| S4 | E, F |

**Step A: The spreadsheet's answer.** Sort villages by need score: A (1,000) first, then B (800). Drill at A's nearest site, S1, then at B's nearest site, S2. Covered: A, B and C, **2,400 people**. But S2 alone already reaches A and B. **S1 adds nobody.** One borehole out of two is wasted.

**Step B: The covering model's answer.** With 4 sites and 2 boreholes there are only 6 possible pairs, so we can list them all:

| Pair | People covered | North covered | South covered | Worst district |
|---|---|---|---|---|
| S1 + S2 | 2,400 | 82.8% | 0.0% | 0.0% |
| S1 + S3 | 2,300 | 79.3% | 0.0% | 0.0% |
| S1 + S4 | 2,150 | 62.1% | 100.0% | 62.1% |
| **S2 + S3** | **2,900** | 100.0% | 0.0% | 0.0% |
| **S2 + S4** | 2,750 | 82.8% | 100.0% | **82.8%** |
| S3 + S4 | 850 | 17.2% | 100.0% | 17.2% |

Check one row by hand: S2 + S4 reaches A, B, C, E and F, so $1000 + 800 + 600 + 150 + 200 = 2{,}750$ people. North's share is $2400 / 2900 = 82.8\%$; South's is $350 / 350 = 100\%$.

The most people covered is **S2 + S3: 2,900**, 500 more than the spreadsheet with the same two boreholes. The solver in the code finds the same pair. But South gets **nothing**: the same clustering the councils complained about.

**Step C: Add the fairness rule.** Now ask for maximin: make the worst-off district's covered share as large as possible. In the model, add one new variable $t$ (the worst share) and, for each district $d$ with total population $P_d$, the rule

$$
\frac{\sum_{i \in d} p_i\, y_i}{P_d} \ \ge\ t \qquad \text{then maximize } t.
$$

Since $t$ must sit below every district's share, pushing $t$ up pushes up the lowest one. Look at the "Worst district" column: the best is **S2 + S4, at 82.8%**. Both districts get a borehole, and everybody in South is covered.

**The price of fairness** is what the rule costs in total coverage: $2{,}900 - 2{,}750 = 150$ people, or $150 / 2{,}900 = 5.2\%$. In exchange, the worst district goes from 0% to 82.8% covered. Naming this trade-off is the point: the councils are no longer arguing about villages, they are choosing a rule and can see exactly what it costs.

### Maximin and leximin, in words

**Maximin** looks only at the worst-off group. It can leave ties: two plans might give the worst district the same share, while one treats the second-worst district much better. **Leximin** breaks those ties in order: first make the worst-off group as well off as possible; then, without making it worse, do the same for the second-worst; then the third; and so on. Flanigan and colleagues (Nature, 2021) used leximin to choose citizens' assemblies fairly, and it has been adopted in practice by the Sortition Foundation; the parallel here is districts rather than demographic quotas. The code uses a simpler tie-breaker that the councils will also understand: **first** find the best possible worst-district share, **then**, among plans that achieve it, pick the one covering the most people.

### Why yes/no choices are harder than ordinary ones

With 6 pairs, listing every option is easy. The full problem has 115 drillable sites and 25 boreholes. The number of ways to choose 25 of 115 is about $1.27 \times 10^{25}$: more than any computer could list.

If the variables could take any value between 0 and 1, the problem would be much easier. Problems with smooth, continuous variables can be solved by starting anywhere and sliding steadily toward better answers, and a standard method (the *simplex method*) does this reliably even for very large problems. Yes/no choices break the slide: there is nothing between "drill" and "don't."

### How a solver searches: relaxation, then branch and bound

A solver uses the easy problem to steer the hard one. Here is the fair toy problem, worked the way a solver would.

**1. Relax.** Pretend boreholes can be fractional and solve that easier problem. This is the **LP relaxation** ("LP" for linear program). The code's answer:

| Site | S1 | S2 | S3 | S4 |
|---|---|---|---|---|
| Relaxed answer | 0 | 1 | 0.147 | 0.853 |

Worst district: **85.3%**. You can't drill 0.147 of a borehole, but this number is still useful: it's a **bound**. Allowing more options can only help, so no real plan can beat 85.3%. You can check it: with S2 drilled, North's share is $(2400 + 500a)/2900$ and South's is $1 - a$, where $a$ is the fraction at S3. They are equal when $a = 500/3400 = 0.147$, giving $85.3\%$.

**2. Branch.** S3 is fractional, so split the problem in two: one branch where S3 is forced to 0, one where it is forced to 1. Solve the relaxation in each.

| Branch | Relaxed answer | Worst-district bound |
|---|---|---|
| S3 = 0 | S2 = 1, S4 = 1 (whole numbers) | 82.8% |
| S3 = 1 | S2 = 0.453, S4 = 0.547 | 54.7% |

**3. Bound and prune.** The S3 = 0 branch came out in whole numbers: a real plan, S2 + S4, with 82.8%. The S3 = 1 branch can do no better than 54.7%, even with fractional boreholes, so there's no point searching inside it. It is **pruned**. Nothing left can beat 82.8%, so S2 + S4 is proven best.

That is **branch and bound**: relax, split on a fractional choice, and discard any branch whose bound can't beat the best real plan found so far. On real problems, most branches get pruned early, which is why a model with $10^{25}$ possible plans solves in a fraction of a second. Note also why you can't just round the relaxed answer: here rounding happens to work, but in general rounded values can break the budget or miss the best plan, and you'd have no proof either way.

---

## Chapter 4.5: Scaling Up – 300 Villages, 25 Boreholes, Four Councils

### The full-size problem

The code generates an illustrative region that matches the case: 300 villages, 4 districts, and 180 candidate points from a hydrogeology survey, of which 115 are drillable.

| District | Villages | People | Median village | Drillable sites |
|---|---|---|---|---|
| A (river valley) | 95 | 93,798 | 867 | 39 |
| B | 80 | 58,584 | 645 | 28 |
| C | 70 | 48,394 | 591 | 24 |
| D (hills) | 55 | 25,345 | 382 | 24 |
| **Total** | **300** | **226,121** | | **115** |

Only 211 villages (165,321 people, 73.1% of the region) have any drillable site within a 30-minute walk. No plan can cover the rest; that's worth telling the donor up front.

### When Excel's Solver stops being enough

The model needs one variable per drillable site and one per village: $115 + 300 = 415$. Excel's standard built-in Solver handles at most 200 decision variables. Dropping the 89 villages no site can reach still leaves 326. The toy example (10 variables) fits easily; the real one doesn't. This is why the case recommends PuLP, a free Python library for writing such models, with a free solver. The code uses CBC, which ships with PuLP; PuLP can also use HiGHS, the free solver the case names, by changing the solve line, if HiGHS is installed. A script like this can also write the chosen sites to a CSV that QGIS maps directly (the tutorial's code just prints them).

### Fairness options for the councils

The case's advice is to put two or three options in front of the councils and let them choose. The model makes this easy: change one number and re-solve. The code tries a **floor** (every district must reach at least this share) at several levels:

| Every district at least | People covered | Worst district | Boreholes in A, B, C, D |
|---|---|---|---|
| no rule (pure coverage) | 108,488 | 0.0% | 10, 9, 6, 0 |
| 10% | 107,281 | 12.5% | 9, 8, 6, 2 |
| 20% (middle ground) | 104,877 | 22.2% | 8, 7, 6, 4 |
| 30% | 99,358 | 30.4% | 8, 4, 6, 7 |
| 37.1% (maximin) | 86,767 | 37.1% | 6, 4, 4, 11 |

Three things stand out:

- **The first steps of fairness are cheap.** A 20% floor costs $108{,}488 - 104{,}877 = 3{,}611$ people, 3.3% of the maximum, and takes District D from no boreholes to four.
- **The last steps are expensive.** Going from 30% to the maximin 37.1% costs $99{,}358 - 86{,}767 = 12{,}591$ people. District D's villages are small and scattered, so it takes 11 boreholes to lift its share that far.
- **The choice is a value judgment, not a technical one.** The model's job is to make the trade-off visible and exact; the councils' job is to pick the row.

The first, middle and last rows are the three options the case suggests presenting: pure coverage, a middle ground, and maximin.

### Backup sites for dry boreholes

Some boreholes will come up dry. If each has, say, a 20% chance (an illustrative figure; use the hydrogeologist's), then the number of dry holes out of 25 follows a **binomial distribution**: expected value $25 \times 0.2 = 5$, standard deviation $\sqrt{25 \times 0.2 \times 0.8} = 2$, and a **10.9%** chance of 8 or more. Planning for none is not realistic.

So for each chosen site, the code finds the best **backup**: the unchosen drillable site in the *same district* that recovers the most people if the original is dry. Keeping it in the same district keeps the fairness promise. For the maximin-fair plan:

- a single dry site loses 3,447 people on average (8,274 at worst);
- its best backup recovers 2,647 on average, **77% of the loss**;
- after any single swap, the worst district's share stays at or above 32.4%.

Publish the backup list with the plan, so a dry hole means drilling the next site on an agreed list, not reopening the argument.

---

## Chapter 5: Code Implementation & Simulation

The full program is [`code/case2_welfare_ilp.py`](code/case2_welfare_ilp.py). It needs `numpy` and PuLP 3, which includes the free CBC solver:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case2_welfare_ilp.py
```

### The covering model in PuLP

```python
prob = pulp.LpProblem("boreholes", pulp.LpMaximize)
x = [pulp.LpVariable(f"drill_{j}", cat="Binary") for j in range(n_s)]    # one per site
y = [pulp.LpVariable(f"covered_{i}", cat="Binary") for i in range(n_v)]  # one per village
prob += pulp.lpSum(int(pop[i]) * y[i] for i in range(n_v))               # people covered
prob += pulp.lpSum(x) == BUDGET                                          # 25 boreholes
for i in range(n_v):                                                     # covered only if a
    prob += y[i] <= pulp.lpSum(x[j] for j in np.flatnonzero(reach[i]))   # chosen site is in reach
prob.solve(pulp.PULP_CBC_CMD(msg=False))
```

Each line matches a line of the formula in Chapter 1. `reach` is the coverage table from Chapter 3: `reach[i, j]` is `True` when site `j` is within a 30-minute walk of village `i`.

### The fairness rule

```python
t = pulp.LpVariable("worst_share", 0, 1)
for d in DISTRICTS:
    members = np.flatnonzero(region["district"] == d)
    d_pop = int(pop[members].sum())
    prob += pulp.lpSum(int(pop[i]) * y[i] for i in members) >= floor * d_pop   # a floor
    prob += pulp.lpSum(int(pop[i]) * y[i] for i in members) >= t * d_pop       # for maximin
```

For a floor, keep the "people covered" objective and set `floor`. For maximin, make `t` the objective; then solve again with the best `t` as a floor and "people covered" as the objective, to break ties in favor of more people.

### Simulation: five plans, 25 boreholes

The code compares five ways of choosing 25 sites in the illustrative region:

- **Need ranking:** sort villages by population and drill the nearest drillable site to each, until 25 are chosen (the spreadsheet method).
- **Greedy:** a smarter spreadsheet. Each round, add the site that covers the most people *not already covered*.
- **Max coverage:** the covering model, no fairness rule.
- **Maximin fair:** the covering model with maximin, ties broken by people covered.
- **Middle ground:** the covering model with a 20% floor for every district.

```
Chapter 5 - five plans for 25 boreholes
  need ranking                     covered= 90,013 (39.8%)  A=52%  B=48%  C=26%  D=0%  worst=0.0%  sites/district=[15, 7, 3, 0]
  greedy (most new people)         covered=108,488 (48.0%)  A=52%  B=60%  C=51%  D=0%  worst=0.0%  sites/district=[10, 9, 6, 0]
  max coverage (ILP)               covered=108,488 (48.0%)  A=52%  B=60%  C=51%  D=0%  worst=0.0%  sites/district=[10, 9, 6, 0]  0.03s
  maximin fair (ILP)               covered= 86,767 (38.4%)  A=38%  B=39%  C=39%  D=37%  worst=37.1%  sites/district=[6, 4, 4, 11]  0.11s
  middle ground (ILP, floor 20%)   covered=104,877 (46.4%)  A=47%  B=52%  C=51%  D=22%  worst=22.2%  sites/district=[8, 7, 6, 4]  0.05s
  need ranking: sum of each site's catchment=98,600 vs people actually covered=90,013 (double counted=8,587)
```

The times at the end of each line are seconds on one laptop; they will differ slightly on yours. The whole program, 86 solves in all (most of them for the sensitivity analysis), runs in a few seconds.

### What the results say

- **The covering model beats the spreadsheet by a wide margin.** With the same 25 boreholes, max coverage reaches $108{,}488 - 90{,}013 = 18{,}475$ more people than the need ranking, 20.5% more.
- **The middle ground beats the spreadsheet on both counts.** It covers $104{,}877 - 90{,}013 = 14{,}864$ more people *and* gives every district at least 22.2%, where the spreadsheet left District D with nothing.
- **Maximin is the most equal, at a real cost.** All four districts land between 37% and 39%, but it covers 21,721 fewer people than max coverage (20.0%) and even 3,246 fewer than the spreadsheet.
- **Greedy matched the optimum here.** That happens when catchments are fairly separate, as in this region. It isn't guaranteed: greedy can lock in an early choice it would later regret, and it has no way to tell you whether it found the best plan or to add a fairness rule. The covering model does both, in a fraction of a second.

Two cautions. The region, populations and sites are invented to teach the method; real gains depend on the real coverage table, especially the walking times near the 30-minute line (Chapter 3). And "covered" means *within a 30-minute walk as modeled*, not "uses the borehole": that is worth checking after drilling.

---

## Chapter 6: Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Decisions** | $x_j \in \{0, 1\}$ per drillable site; $y_i \in \{0, 1\}$ per village | One yes/no choice per site from the hydrogeology survey |
| **Coverage table** | minutes $= \dfrac{\text{km} \times \text{detour}}{\text{speed}} \times 60 \le 30$ | Turns census GPS points into who can reach which site; check the detour factor by walking a sample |
| **Objective** | maximize $\sum_i p_i\, y_i$ | Counts each covered person once, however many boreholes are in reach |
| **Budget** | $\sum_j x_j = 25$ | The grant |
| **Coverage rule** | $y_i \le \sum_{j \in N_i} x_j$ | A village counts only if a chosen site is within a 30-minute walk |
| **Fairness** | share$_d \ge$ floor, or maximize $t$ with share$_d \ge t$ | Writes the councils' agreed rule into the model; the price of fairness is visible |
| **Solver** | LP relaxation + branch and bound | Finds and proves the best plan among about $10^{25}$, in under a second |
| **Sensitivity** | change one input, re-solve, compare | Shows which inputs matter (here, the walking limit) before anything is drilled |
| **Backups** | best same-district replacement per site | Turns a dry hole into the next site on an agreed list |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/02-borehole-siting.md#after-the-recommendation): build the village × site walking-time table, agree the fairness rule with district officers before running the model, and produce the map and comparison table for the donor. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) sections of the playbook cover the Class 2 specifics.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section lists the tools and partners; INFORMS Pro Bono Analytics is the case's best fit, because facility siting is a textbook operations-research problem.
- **Read** the integer programming chapters of Bradley, Hax and Magnanti, *Applied Mathematical Programming*, free from MIT, then Church & ReVelle (1974) on covering location and Flanigan et al. (2021) on leximin fairness, all listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Other tutorials:** [restless bandits](01-restless-bandits-chw-visits.md) for decisions that repeat every week; [robust optimization](04-robust-optimization-cyclone-prepositioning.md) for when you must plan against shocks you can't forecast, the natural next step if dry-borehole risk were severe; and [deciding without a model](06-no-model-food-pantry.md) for when a written rule is enough.
