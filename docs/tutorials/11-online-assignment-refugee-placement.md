# Online Assignment Masterclass: Placing Refugee Families as They Arrive

*An in-depth walkthrough of employment prediction, assignment integer programs, and online assignment with forecasts and bid prices, built on [Case 11: Placing refugee families as they arrive](../cases/11-refugee-placement-online.md).*

**You need:** proportions, means, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists). **Code:** [`code/case11_online_assignment.py`](code/case11_online_assignment.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A national resettlement agency works with partner offices in **30 cities**. Each city agrees a **yearly quota** of refugee families. Families are referred a few at a time all year, and each needs a city **within about a week**. The goal is that an adult in each family has a **job within six months**. Each family is placed once and stays. The agency has **five years of records**: every family's city and whether they were employed at six months. Caseworkers make the final call; one analyst can run a model.

Today caseworkers choose by judgment and by whichever quota still has room. Two obvious upgrades both fall short. A **prediction model** alone says where a family might do well, but not how to share 30 quotas across a year of families nobody has met yet. Placing each family in its **single best-predicted city** as it arrives fills the strongest cities by spring, and families who arrive in the autumn get whatever is left.

This tutorial builds the alternative step by step:

1. **[The Online Leap](#the-online-leap--from-first-available-to-placing-with-the-future-in-mind)** separates the two jobs: predict, then assign with the future in mind.
2. **[The Core Bottleneck](#the-core-bottleneck--unknown-arrivals-noisy-predictions-no-moving-back)** names what makes this hard: unknown arrivals, noisy predictions, and no moving families afterwards.
3. **[From Five Years of Records to Estimates](#from-five-years-of-records-to-estimates--employment-chances-by-family-and-city)** turns the records into an employment chance for every family type in every city, with margins of error.
4. **[The Decision Engine](#the-decision-engine--hindsight-best-greedy-re-solving-and-bid-prices)** works a 6-family example by hand: the hindsight best, greedy, re-solving with a forecast, and bid prices.
5. **[Scaling Up](#scaling-up--30-cities-a-year-of-arrivals-caseworkers-in-the-loop)** handles 30 cities and a year of arrivals, with caseworker overrides and explanations.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all and compares four rules over simulated years.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **a place in a strong city is worth most to the family that gains most from it, and that family may not have arrived yet.**

---

## The Online Leap – From First Available to Placing with the Future in Mind

### Two jobs, not one

The agency's question, "which city for this family?", hides two different jobs:

1. **Prediction:** for this family, what is the chance someone is working at six months in each of the 30 cities? That is a statistics question, answered from the five years of records.
2. **Assignment:** given those chances, the quotas left, and the families likely to come later, which city should *this* family get? That is a decision question.

A good prediction model with a poor assignment rule still wastes places. The rest of this tutorial is mostly about the second job, because that is where the year-long quotas bite.

### What "online" means

A problem is **offline** when everyone is known before you decide: you can line up all the families and all the places and solve once. It is **online** when people arrive one at a time (or a few at a time) and each must be placed before you see who comes next. The agency's problem is online: the narrowing answer says families "arrive a few at a time all year" and "we don't know who will come next month."

Online problems are judged against an impossible standard: the **hindsight best**, the plan you would have made if you had known the whole year's families on 1 January. No online rule can beat it. The useful question is how close a rule gets.

### Mapping it to the program

| Model term | In this program |
|---|---|
| Arrival | A refugee family, referred a few at a time; each needs a city within about a week |
| Family type | A short description from the case file; in the code, trade (skilled trade, service work, no prior work) × some English or none × small or large family: 12 types |
| City capacity $Q_c$ | City $c$'s yearly quota of families |
| Value $\hat p_{kc}$ | Predicted chance that a type-$k$ family placed in city $c$ has someone working at six months, from five years of records |
| Forecast $F_k$ | Expected number of type-$k$ families still to arrive this year, from the same five years |
| Objective | Expected number of families with someone employed at six months: the sum of $\hat p$ over placements |
| Decision rule | Each week, a suggested city for each new family; the caseworker decides |

---

## The Core Bottleneck – Unknown Arrivals, Noisy Predictions, No Moving Back

### Places used now are gone later

Each city's quota is for the whole year. A place used in March cannot be given to a family in October. If the best cities fill early, later families are placed by what is left, not by fit. In the simulation of [Code Implementation & Simulation](#code-implementation--simulation), the "best city now" rule fills **13.0 of the 30 cities by the end of June**, and families arriving in the last quarter of the year have a **32.4%** average employment chance, against **57.8%** for those arriving in the first quarter.

### Who comes next is unknown, but not unpredictable

The agency doesn't know next month's families. It does know, from five years of records, roughly how many come and what kinds. In the illustrative data, families with no prior work make up **22%** of first-quarter arrivals but **46%** of last-quarter arrivals. A forecast that is right on average is enough to reserve places sensibly; it does not need to name individual families.

### The predictions are noisy

Five years sounds like plenty, but it is spread over 12 family types × 30 cities = **360 cells**. In the illustrative data the median cell holds only **13** families, and **25** cells hold fewer than 5. A rate from 6 families has a 95% confidence interval about 80 percentage points wide. Any assignment rule built on raw cell rates will chase noise.

### No moving back, and people in the loop

Each family is placed once. A poor placement hurts the family's chances of work; it isn't life-threatening, and a family can move later on its own (Filter 4), which is why this is Class 10 and not the robust planning of [Class 4](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning). But it does mean a suggestion must be explainable to a caseworker, who keeps the final decision, and to the family.

---

## From Five Years of Records to Estimates – Employment Chances by Family and City

### Step 1: The raw table

The code invents five years of records in which caseworkers placed families with the current practice. It holds **4,841** families, of whom **40.0%** were employed at six months. Counting families and successes in each type × city cell gives a raw rate per cell, with the usual 95% interval $\hat p \pm 1.96\sqrt{\hat p(1-\hat p)/n}$.

### Step 2: Shrink thin cells toward a simpler estimate

A cell with 6 families is too thin to trust on its own. **Shrinkage** blends it with a simpler estimate that uses much more data. Here the simpler estimate, the **prior**, is

$$
\text{prior}_{kc} = \text{city } c\text{'s overall rate} + \text{type } k\text{'s overall rate} - \text{the overall rate}
$$

which says "a type that does a bit better than average, in a city that does a bit better than average." The shrunk estimate acts as if we had added $k$ imaginary families who behave exactly like the prior:

$$
\hat p_{kc} = \frac{\text{successes}_{kc} + k \times \text{prior}_{kc}}{n_{kc} + k}
$$

A cell with many families barely moves; a cell with few is pulled most of the way to the prior. (The $k$ here is a strength, not a family type; it is the only number to choose.)

### Step 3: Choose the strength on a held-out year

To choose $k$ honestly, fit on years 1–4 and test on year 5. The test score is the **Brier score**: the average of (predicted chance − actual outcome)², where the outcome is 1 for employed and 0 for not. Lower is better. Because the data are synthetic, the code can also report the average error against the true chances, which you could never see in real life.

| Estimate | Held-out Brier score | Average error vs truth (synthetic only) |
|---|---|---|
| Raw cell rates | 0.2245 | 0.115 |
| Shrunk, $k = 5$ | 0.2117 | 0.082 |
| Shrunk, $k = 10$ | 0.2095 | 0.073 |
| **Shrunk, $k = 20$** | **0.2086** | **0.068** |
| Shrunk, $k = 40$ | 0.2088 | 0.069 |
| Prior only | 0.2108 | 0.082 |

Both columns pick the same answer: $k = 20$. Shrinkage cuts the average error from 11.5 to 6.8 percentage points. The held-out year found that without knowing the truth, which is what you would rely on in practice.

### Step 4: What it does to individual cells

Three skilled-trade cells, raw rate (95% interval) against shrunk estimate (rough 95% interval):

| Cell | Raw | Prior | Shrunk | Truth (synthetic) |
|---|---|---|---|---|
| City 12 | 3/6 = 50% (10% to 90%) | 57% | 56% (37% to 75%) | 43% |
| City 27 | 8/13 = 62% (35% to 88%) | 47% | 53% (36% to 70%) | 37% |
| City 14 | 15/26 = 58% (39% to 77%) | 68% | 62% (48% to 76%) | 53% |

The shrunk intervals are narrower but still wide, and shrinkage doesn't always help a single cell (City 12 moved away from the truth). It helps on average, which is what the assignment needs. The shrunk interval here, $\hat p \pm 1.96\sqrt{\hat p(1-\hat p)/(n+k)}$, is a rough guide, not an exact one.

A **logistic regression** (a model for yes/no outcomes using family and city characteristics) is the usual next step, and the case's build options suggest a standard library for it. Shrunk group rates are a transparent first version the analyst can explain to caseworkers. Two cautions carry over to any model. It can learn only about city × family combinations that past placements covered; if caseworkers never sent large families to some cities, the model knows nothing about them. And the case's unknowns stand: check whether accuracy is equal across nationalities and family types, and whether this year's families resemble the last five years'.

---

## The Decision Engine – Hindsight Best, Greedy, Re-solving and Bid Prices

### Step-by-step concrete example: 3 cities, 6 families

Three cities with yearly quotas **A = 2, B = 2, C = 3** (7 places). Six families arrive one after another. Their predicted employment chances:

| Family kind | City A | City B | City C |
|---|---|---|---|
| Service work | 0.50 | 0.30 | 0.45 |
| Skilled trade | 0.60 | 0.55 | 0.20 |
| No prior work | 0.55 | 0.25 | 0.15 |

City A is a strong labor market for everyone. City B suits tradespeople. City C works nearly as well as A for service workers and badly for the others. The arrival order is: service, service, trade, trade, no prior work, no prior work. Past seasons suggest about 2 of each kind.

**Rule 1: Greedy ("best city with space now").** Family 1 (service) takes A (0.50). Family 2 takes A (0.50), and A is full. Families 3–4 (trade) take B (0.55 each). Families 5–6 (no prior work) find only C left: 0.15 each.

$$0.50 + 0.50 + 0.55 + 0.55 + 0.15 + 0.15 = 2.40 \text{ expected employed families.}$$

**Rule 2: The hindsight best.** Knowing all six in advance, put the service families in C (they lose only 0.05 each), the trade families in B, and the no-prior-work families in A:

$$0.45 + 0.45 + 0.55 + 0.55 + 0.55 + 0.55 = 3.10.$$

That is 0.70 more employed families from the same places, a 29% gain. The solver in the code agrees. In general it is found with an **assignment integer program**: let $x_{kc}$ be the number of type-$k$ families sent to city $c$ (a whole number), $n_k$ the number of type-$k$ families, and

$$
\text{maximize } \sum_{k,c} \hat p_{kc}\, x_{kc} \quad \text{subject to} \quad \sum_c x_{kc} = n_k \ \text{(everyone placed)}, \quad \sum_k x_{kc} \le Q_c \ \text{(quotas)}.
$$

The hindsight best is a **benchmark**, not a rule you can run: on the day family 1 arrives, families 5 and 6 don't exist yet.

**Rule 3: Re-solve with a forecast.** When a family arrives, pretend the forecast families are real, solve the assignment program for *this family plus the forecast*, and keep only this family's city. When family 1 arrives, the forecast says 1 more service family, 2 trade and 2 no-prior-work are coming. The best plan for that imagined group puts the service family in C, so family 1 goes to C. Repeating this for each arrival gives C, C, B, B, A, A: **3.10**, the hindsight best, because the forecast was right.

**Rule 4: Bid prices.** Instead of solving for every family, solve once and attach a **price** to each city's places. Relax the program for the forecast families so fractions are allowed (a **linear program**, or LP). Every quota rule then gets a **shadow price**: how much the forecast total would change with one more or one fewer place in that city. The code's LP returns:

| City | A | B | C |
|---|---|---|---|
| Bid price | 0.40 | 0.20 | 0.00 |

C's price is zero because it has a spare place. A's price, 0.40, is what a no-prior-work family loses if pushed out of A into C ($0.55 - 0.15$). The rule for each arrival: **pick the city with room that has the highest chance minus price.**

| Family kind | A | B | C | Choice |
|---|---|---|---|---|
| Service work | 0.10 | 0.10 | **0.45** | C |
| Skilled trade | 0.20 | **0.35** | 0.20 | B |
| No prior work | **0.15** | 0.05 | **0.15** | tie; higher raw chance → A |

This also gives C, C, B, B, A, A and **3.10**. Prices are cheap to compute and easy to show a caseworker ("City A costs 0.40 because families who need it more are expected later"). They are also not unique: any B price from 0.10 to 0.35 gives the same plan here, and ties like the last row are common. That is one reason the code recomputes them every four weeks.

### When the forecast is wrong

Now suppose families 5 and 6 turn out to be service families, not the expected no-prior-work families. Greedy gets **3.00**, which happens to be the hindsight best. Re-solving with the (wrong) forecast kept A free for families who never came, and gets **2.95**; bid prices give the same **2.95**. Reserving capacity is a bet on the forecast. When the forecast is right on average it pays (2.40 → 3.10 above); when it is wrong it costs a little. The simulation in [Code Implementation & Simulation](#code-implementation--simulation) tests this at full scale.

### Why not just assign the whole year at once, or run a stable match?

These are the case's two "most likely confusions." Assigning the whole year at once is the hindsight best: it needs a list of families the agency never has (that is [Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)). A stable match needs both sides to rank each other; here nobody ranks anybody (that is [Class 5](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets)). The online rules above borrow the hindsight program, but apply it to *this week's families plus a forecast*, again and again.

---

## Scaling Up – 30 Cities, a Year of Arrivals, Caseworkers in the Loop

### The full-size problem

The code builds an illustrative world matching the case: **30 cities** with yearly quotas from **16 to 56** families (total **1,050**), and about **960** families referred a year (the case gives no totals; these are invented). Averaged over family types, the true employment chance is **58%** in the best city, **41%** in the median city and **22%** in the worst. Arrivals vary by season, and the share with no prior work rises through the year.

### Re-solving every week

Each week, the analyst's script solves one program: this week's families (each must go to exactly one city, a yes/no choice) plus the forecast families still to come this year (fractions allowed, since they are expected numbers). With $x_{ic}$ for real family $i$, $y_{kc}$ for forecast families of type $k$, $F_k$ the forecast and $R_c$ the room left in city $c$:

$$
\begin{aligned}
\text{maximize} \quad & \sum_{i,c} \hat p_{k(i)c}\, x_{ic} + \sum_{k,c} \hat p_{kc}\, y_{kc} \\
\text{subject to} \quad & \sum_c x_{ic} = 1 \ \text{for each family this week}, \qquad \sum_c y_{kc} = F_k \ \text{for each type} \\
& \sum_i x_{ic} + \sum_k y_{kc} \le R_c \ \text{for each city}
\end{aligned}
$$

Only the $x$ answers are used; the $y$ answers are thrown away and recomputed next week with fresh arrivals and room. The forecast is the average of past years' arrivals by week and type; the code scales it down if it would exceed the room left. With about 20 families and 30 cities a week, each solve takes a fraction of a second, well within the case's one-week deadline. One could also draw several possible futures from past years and average the plans; the code keeps the single average forecast for simplicity.

### Fairness over the year

The case asks two fairness questions: should late arrivals get placements as good, on average, as early ones, and should every city get a mix of families? The first is measured directly in the simulation by quarter of arrival. Greedy fails it badly (57.8% in the first quarter, 32.4% in the last). Re-solving passes it (46.6% → 48.6%) without being told to, because reserving places for later arrivals is exactly what it does. If the agency agrees a firmer rule, such as "no quarter below X%" or a floor for a group, it can be added as a constraint, as the fairness floors are in the [Case 2 tutorial](02-welfare-optimization-borehole-siting.md#fairness-options-for-the-councils). Manshadi, Niazadeh & Rodilitz (Management Science, 2023) study fair rationing of scarce supplies to requests that arrive over time; Arnosti & Shi (Management Science, 2020) study lotteries and waitlists for affordable housing. Both are parallels from other domains, not refugee deployments.

Families with no prior work have lower predicted chances everywhere, so maximizing the total does not close their gap with other families. That is a value choice the agency should make on purpose, not by default.

### Families who must go to a particular city

The case flags a gap: some families must go to a particular city (relatives there, medical needs). Fix those first, subtract them from the quotas, and run the model on the rest.

### Caseworker override and explanations

The database shows the top suggestions with a reason. The code simulates caseworkers setting aside **15%** of suggestions and choosing another of the three cities with the highest predicted chance instead. Here is one placement the code explains, a week-27 skilled-trade family with some English:

| | City | Predicted chance | Quota used | Bid price | Chance − price |
|---|---|---|---|---|---|
| **Suggested** | 25 | 68.4% | 43% | 0.05 | +0.63 |
| Greedy's pick | 3 | 82.5% | 45% | 0.29 | +0.54 |

The one-line reason a caseworker could pass on: *"City 3 would raise this family's chance by 14.2 points, but service-work families expected later this year gain 45.7 points there; City 25 is a good fit with plenty of room."* Prices make this kind of explanation possible. The monthly override review then asks whether overrides cluster on certain cities or family types, which may point to something the model is missing.

---

## Code Implementation & Simulation

The full program is [`code/case11_online_assignment.py`](code/case11_online_assignment.py). It needs `numpy` and PuLP 3, which includes the free CBC solver:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case11_online_assignment.py
```

It takes about 40 seconds, mostly for the weekly re-solves.

### The weekly re-solve in PuLP

```python
prob = pulp.LpProblem("week", pulp.LpMaximize)
x = [[pulp.LpVariable(f"x_{i}_{c}", 0, 1, cat="Binary") for c in range(N_CITIES)]
     for i in range(len(fams))]                                 # this week's families
y = [[pulp.LpVariable(f"y_{k}_{c}", 0) for c in range(N_CITIES)] for k in range(N_TYPES)]
prob += (pulp.lpSum(p[k, c] * x[i][c] for i, k in enumerate(fams) for c in range(N_CITIES))
         + pulp.lpSum(p[k, c] * y[k][c] for k in range(N_TYPES) for c in range(N_CITIES)))
for i in range(len(fams)):
    prob += pulp.lpSum(x[i]) == 1                               # each family placed once
for k in range(N_TYPES):
    prob += pulp.lpSum(y[k]) == float(future[k])                # forecast arrivals
for c in range(N_CITIES):
    prob += (pulp.lpSum(x[i][c] for i in range(len(fams)))
             + pulp.lpSum(y[k][c] for k in range(N_TYPES)) <= float(room[c]), f"q{c}")
prob.solve(pulp.PULP_CBC_CMD(msg=False))
```

Each line matches a line of the formula in [Scaling Up](#scaling-up--30-cities-a-year-of-arrivals-caseworkers-in-the-loop). The bid-price rule solves the same program with the forecast families only and reads each quota's shadow price with `prob.constraints[f"q{c}"].pi`.

### Simulation: four rules and two benchmarks

All rules use the shrunk estimates from [From Five Years of Records to Estimates](#from-five-years-of-records-to-estimates--employment-chances-by-family-and-city); results are scored with the true chances, so prediction error counts against them.

- **First-available:** a proxy for current practice. Pick a city with room, more likely the more room it has. Real caseworkers also use judgment, so this baseline is probably worse than the agency's practice.
- **Greedy:** the city with room and the highest predicted chance.
- **Bid price:** highest predicted chance minus city price, prices recomputed every four weeks.
- **Re-solve:** the weekly program above.
- **Re-solve + 15% overrides:** caseworkers set aside 15% of suggestions.
- **Hindsight best:** the assignment program with the whole year known, using the estimates; then with the true chances, which no real agency could have.

"Employed" is the expected number of families with someone employed at six months (the sum of true chances). "Q1"–"Q4" are average chances by quarter of arrival; "no-prior" and "others" by group; "full by June" is the number of cities whose quota was used up by the end of June. The interval is a 95% confidence interval for the year-by-year difference from first-available.

```
Simulation - typical years: 6 years, 962 families a year on average
  policy                     employed    vs current (95% CI) quota use    Q1    Q2    Q3    Q4 no-prior others full by June
  first-available               374.9      +0.0 ( +0.0 to  +0.0)     91.7% 40.8% 39.1% 38.4% 37.5%    27.7%  44.8%          0.0
  greedy                        437.6     +62.7 (+59.9 to +65.6)     91.7% 57.8% 47.8% 42.1% 32.4%    30.8%  53.2%         13.0
  bid price                     457.8     +82.9 (+79.0 to +86.7)     91.7% 48.6% 49.4% 47.0% 44.4%    32.7%  55.3%          4.8
  re-solve                      455.4     +80.5 (+77.6 to +83.3)     91.7% 46.6% 46.7% 47.9% 48.6%    32.5%  55.0%          4.3
  re-solve + 15% overrides      447.1     +72.2 (+68.4 to +76.1)     91.7% 47.6% 46.7% 47.0% 44.1%    32.2%  53.9%          4.2
  hindsight best                461.5     +86.6 (+82.6 to +90.7)     91.7%   -     -     -     -      32.5%  56.0%            -
  hindsight, true chances       485.8    +110.9 (+108.3 to +113.5)     91.7%   -     -     -     -      32.2%  60.0%            -
```

### What the results say

- **Any use of the predictions beats first-available,** and the forecast-based rules beat greedy. Re-solving adds 80.5 expected employed families a year over first-available, $80.5 / 374.9 = 21.5\%$ more; greedy adds 62.7 (16.7%).
- **The online rules get close to the hindsight best.** Re-solving reaches $455.4 / 461.5 = 98.7\%$ of it and bid prices 99.2%; greedy reaches 94.8%. Bid prices did slightly better than re-solving here; the difference is small and could go either way on other data.
- **Greedy is unfair over time; re-solving is not.** Greedy's first-quarter families average 57.8% and last-quarter families 32.4%, a gap of 25 points, and 13 cities are full by June. Re-solving keeps every quarter between 46.6% and 48.6%.
- **Quota use is the same for every rule (91.7%),** because every family is placed and total quotas exceed arrivals. The rules differ in *who* gets which place, not how many are used.
- **Overrides cost little.** Setting aside 15% of suggestions loses $455.4 - 447.1 = 8.3$ expected employed families a year, still far above first-available. Caseworker control is affordable.
- **Prediction error costs more than being online.** The gap between the hindsight best with estimates (461.5) and with true chances (485.8) is 24.3 families; the gap between re-solving and the hindsight best is 6.1. Better predictions are worth the analyst's time.

### Robustness: the forecast is wrong

The second run flips the year's mix so no-prior-work families arrive early, the opposite of the five-year pattern the forecast learned:

```
Simulation - forecast wrong (arrival mix reversed): 4 years, 916 families a year on average
  policy                     employed    vs current (95% CI) quota use    Q1    Q2    Q3    Q4 no-prior others full by June
  first-available               353.2      +0.0 ( +0.0 to  +0.0)     87.2% 36.4% 37.8% 39.7% 40.6%    28.0%  43.8%          0.0
  greedy                        419.1     +65.9 (+63.0 to +68.7)     87.2% 53.3% 47.9% 44.8% 36.5%    33.5%  51.8%         11.8
  bid price                     438.7     +85.5 (+82.3 to +88.7)     87.2% 46.1% 48.6% 47.8% 49.1%    32.8%  55.3%          4.8
  re-solve                      434.8     +81.6 (+75.6 to +87.5)     87.2% 44.4% 45.0% 49.5% 51.4%    32.0%  55.1%          4.2
  hindsight best                439.4     +86.2 (+81.9 to +90.5)     87.2%   -     -     -     -      33.2%  55.3%            -
  hindsight, true chances       467.9    +114.7 (+112.5 to +116.9)     87.2%   -     -     -     -      34.4%  59.3%            -
```

The forecast-based rules held up: re-solving still gains 81.6 and stays within 4.6 of the hindsight best. The forecast got the *total* mix right, just the timing wrong, and the weekly re-solve corrects as families arrive. A bigger surprise, such as more families than the quotas can take, was not tested and needs its own plan.

### How this compares with the research

Ahani et al. (Operations Research, 2021) predict each family's chance of employment in each location and assign with an integer program; this is the basis of Annie MOORE at the US resettlement agency HIAS. Their backtests on past HIAS data suggested a **22–38% gain** in short-run employment. That is a **backtest on past data, not a randomized trial**. Ahani et al. (Operations Research, 2024) extend this to families arriving through the year, evaluated on HIAS data and incorporated into Annie MOORE: the closest parallel to this agency. The methods in this tutorial are simplified teaching versions in the same spirit, not their algorithms.

Our 21.5% looks similar, but **don't compare them.** Our world, quotas and chances are invented; the baseline is a crude proxy for caseworkers; and the gain is scored with true chances the agency will never know. The agency's own number has to come from replaying its own last year, as the case recommends.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Prediction** | $\hat p_{kc} = \dfrac{\text{successes}_{kc} + k\,\text{prior}_{kc}}{n_{kc} + k}$, $k$ chosen on a held-out year | Employment chance for each family type in each of 30 cities, from five years of records, steadied in thin cells |
| **Checking predictions** | Brier score on a held-out year; accuracy by nationality and family type | Shows whether the model helps, and for whom it may not |
| **Hindsight best** | max $\sum \hat p_{kc} x_{kc}$, everyone placed, $\sum_k x_{kc} \le Q_c$ | The benchmark: what knowing the whole year would allow |
| **Forecast** | $F_k$ = average past arrivals of type $k$ in the rest of the year | Tells the model which families to save places for |
| **Weekly re-solve** | hindsight program on this week's families + forecast; keep this week's answers | One suggestion per family each week, reserving strong cities for families who need them most |
| **Bid prices** | city with room maximizing $\hat p_{kc} - \lambda_c$ | A cheap alternative to re-solving, and a reason a caseworker can read |
| **Fairness over time** | average chance by quarter; optional floors | Keeps late arrivals from getting only leftovers |
| **Override** | caseworker sets the suggestion aside, with a reason | Keeps the decision human; reviewed monthly |
| **Robustness** | replay with the wrong forecast; compare with hindsight | Shows what reserving costs when the future surprises you |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/11-refugee-placement-online.md#after-the-recommendation): pull the five years into one table, agree the fairness rules with the partner cities, and replay last year's arrivals through a simple version of the model next to what caseworkers actually did. The playbook's [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) cover the replay and a one-season shadow run.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section lists the tools (a prediction library plus PuLP or Google OR-Tools) and partners such as INFORMS Pro Bono Analytics.
- **Read** Ahani et al. (2021) on Annie MOORE, then Ahani et al. (2024) on dynamic placement and Manshadi, Niazadeh & Rodilitz (2023) on fair dynamic rationing, all listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact), which also names the researchers who work on this problem.
- **Other tutorials:** [welfare optimization for borehole siting](02-welfare-optimization-borehole-siting.md) for the offline version, when everyone is known up front; [stable matching for apprenticeships](05-stable-matching-apprenticeships.md) for when both sides rank each other; and [restless bandits for home visits](01-restless-bandits-chw-visits.md) for when the same people are revisited week after week.
