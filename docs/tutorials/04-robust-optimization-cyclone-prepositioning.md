# Robust Optimization Masterclass: Where Should Relief Kits Wait Before a Cyclone We Can't Forecast?

*An in-depth walkthrough of two-stage stochastic programming, robust optimization and distributionally robust optimization, built on [Case 4: Pre-positioning relief supplies before cyclone season](../cases/04-cyclone-prepositioning.md).*

**You need:** proportions, averages, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning). **Code:** [`code/case4_robust_prepositioning.py`](code/case4_robust_prepositioning.py). Every number in this tutorial comes from running that file. The coast, the populations, the storms and the road rules in it are made up for teaching; all scenario numbers are illustrative.

---

## Executive Overview

A humanitarian NGO serves a low-lying coastal delta. Before each cyclone season it stores **30,000 family kits** (water purification tablets, tarpaulins, five days of dry food) in **6 warehouses**. When a cyclone makes landfall, roads flood, bridges go out, and some warehouses are cut off for days. Kits in the wrong warehouse might as well not exist. The NGO has detailed records of only **8 severe cyclones in 25 years**.

The usual answer is to plan for the average storm: look at where past storms hit, and stock each warehouse in proportion. It fails in an instructive way. The average storm never happens. Each real storm hits one part of the coast hard, and the first one to hit an end of the coast finds the nearest warehouse nearly empty and the bridges from the well-stocked center washed out.

This tutorial builds the alternative step by step:

1. **[The Two-Stage Leap](#the-two-stage-leap--from-the-average-storm-to-a-plan-that-adapts)** splits the decision in two: what to commit before the season (stock per warehouse) and what to decide after landfall (where to send the kits). This is a **two-stage** plan.
2. **[The Core Bottleneck](#the-core-bottleneck--eight-storms-and-a-catastrophic-downside)** names what we can't know: with 8 storms, the probabilities of where the next one lands are barely measured, and the cost of guessing wrong is counted in sick children.
3. **[From Eight Storms to Estimates](#from-eight-storms-to-estimates--wide-intervals-and-a-plausible-set)** turns the 8-storm record into estimates, shows how wide their margins of error really are, and builds a **plausible set** of probability patterns around them.
4. **[The Decision Engine](#the-decision-engine--four-ways-to-stock-three-warehouses)** compares four ways to stock three warehouses, by hand: plan for the average storm, plan for the average outcome, plan for the worst storm, and plan for the worst plausible pattern of storms.
5. **[Scaling Up](#scaling-up--six-warehouses-broken-roads-and-dispatch-cards)** scales up to 6 warehouses, 30,000 kits and broken roads, and turns the plan into **dispatch cards** that work with no connectivity.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all in code and tests every plan on storms it never saw.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **don't plan for the storm you expect; plan so that no plausible storm finds you badly short.**

A word of honesty before we start. Of the twelve approaches in this project, robust pre-positioning is one of the **least field-proven**. The evidence is mostly in modeling studies, such as Rawls & Turnquist (2010) on hurricane pre-positioning and a modeling study of the WFP-managed UN Humanitarian Response Depot network ([Stienen et al., Omega 2021](https://pure.uva.nl/ws/files/67452240/1_s2.0_S0305048321001031_main.pdf)). Operational use by NGOs is much less documented. (Forecast-triggered anticipatory action, a related design within the same class, does have documented field use; see [Why this method and not another](#why-this-method-and-not-another).)

---

## The Two-Stage Leap – From the Average Storm to a Plan That Adapts

### Two decisions, made at different times

Look at what the NGO actually decides, and when.

1. **Before the season**, with no idea where the next storm will land: how many kits go into each of the 6 warehouses. Once the season starts, this is fixed. Trucks can't restock a warehouse behind a flooded bridge.
2. **After landfall**, when the NGO can see where the storm hit and which roads still work: how many kits each warehouse sends to each shelter area.

Planners call this a **two-stage** decision. **Stage 1** is the commitment made under uncertainty. **Stage 2** is the response made after the uncertainty is revealed. The key insight is that a good stage-1 plan is one that leaves stage 2 with good options **whatever happens**.

### What "planning for the average" gets wrong

The average-storm planner averages the damage of the 8 recorded storms, zone by zone, and stocks each zone's warehouse in proportion. That plan answers the question "how many families need kits in an average year?" But nobody lives through an average year. A real storm puts thousands of families in need in one zone and almost none elsewhere, and it cuts the very roads that would let the other warehouses help.

The two-stage view asks a different question: **for each storm that could happen, after it happens, how many families can we reach in time with the stock we placed?** Then it chooses the stock that makes those answers good across the storms we consider possible.

### A scenario is one storm, fully described

To make "whatever happens" concrete, we describe the uncertainty with **scenarios**. A scenario is one complete storm: where it makes landfall, how severe it is, how many families in each area need a kit, and which bridges and roads fail. The 8 recorded storms are 8 scenarios. Later we will add storms the record doesn't contain.

### Mapping it to the program

| Two-stage term | In this program |
|---|---|
| Stage-1 decision | Kits stored in each of the 6 warehouses, 30,000 in total, fixed before the season |
| Scenario | One storm: landfall zone, severity, families needing kits per shelter area, failed bridges and roads |
| Stage-2 decision | How many kits each warehouse sends to each shelter area, over the roads that still work |
| Outcome per scenario | Share of affected families reached with a kit **within 2 days** |
| Scenario set for planning | The 8 recorded storms (plus, for the robust models, the same storms moved along the coast) |
| Stress set for testing | About 10 workshop scenarios, kept **out** of the model so the test is fair |
| Robustness level | How far from the record the plan protects; chosen with funders |
| Field output | A stock table per warehouse and a laminated dispatch card per warehouse manager |

The success measure, as in the [case's pilot design](../cases/04-cyclone-prepositioning.md#follow-up-3-pilot-design), is the share of affected families reached with a kit within 2 days, **in the worst scenario and on average**.

---

## The Core Bottleneck – Eight Storms and a Catastrophic Downside

### Problem 1: Eight storms can't tell you the odds

To plan for the average outcome, you need the probability of each kind of storm: landfall in each zone, at each severity, with each pattern of road damage. Eight storms can't supply that. With five coastal zones, three severities and several bridges that can fail, there are dozens of storm types and only 8 observations. Most types have never been seen. [From Eight Storms to Estimates](#from-eight-storms-to-estimates--wide-intervals-and-a-plausible-set) puts numbers on how little 8 storms tell us.

### Problem 2: The downside is catastrophic

In the [Case 1 tutorial](01-restless-bandits-chw-visits.md), a wrong choice meant one patient missed one visit for one week, and the program could learn from it and adjust. Here, a wrong choice means families without clean water for days, and the program gets one chance per season. You can't learn by trial and error when each trial is a disaster. The NGO's own words: *zero tolerance in practice.*

### Problem 3: The average storm never happens

Averages hide exactly what matters. If half the storms hit the center and the rest are split between the two sides, the "average" landfall is the center, and an average-based plan concentrates stock there. That plan looks fine on paper and fails the first time a storm hits one end of the coast, which the record shows will happen eventually.

### What the method must do

Put together, the method must:

1. **Use the record** where it's informative (most storms so far have hit the middle of the coast).
2. **Not trust the record's proportions** as if they were exact.
3. **Protect against storms the record doesn't contain**, such as landfall at an end of the coast or a storm stronger than any on file.
4. **Say what that protection costs**, so funders can choose how much of it to buy.

### Why this method and not another

Two neighboring approaches look similar and are worth ruling out explicitly.

- **[Class 9: Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics).** Kits do move by truck, and the NGO's answer to the finder's narrowing question puts the movement in its place: *"Trucking kits out is something we know how to do; the problem is that we don't know where the next one will hit or which roads will survive."* Routing models minimize the cost of moving goods over a known network. Here the network itself is uncertain, so the after-landfall dispatch becomes a small routing problem *inside* the robust plan (stage 2, below), not the main decision. If the NGO later ran regular deliveries to many sites, Class 9 would be the right tool for those (see the [vehicle routing tutorial](10-vehicle-routing-food-delivery.md)).
- **Forecast-triggered anticipatory action**, a related design within [Class 4](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning). Partners agree in advance on a forecast threshold, the action and its funding, so money or supplies are released automatically when a forecast crosses the threshold. OCHA and the Central Emergency Response Fund activated such a pilot in Somalia in 2020, triggered by projected food insecurity, and GiveDirectly sent cash to about 3,250 households in Kogi State, Nigeria, in 2024 ahead of forecast peak flooding. A trigger suits a fixed action with a few days' warning. It could sit alongside this plan, for example to move stock forward once a cyclone is forecast, but it doesn't decide how many kits to hold in each warehouse months before the season. That is the question this tutorial answers.

---

## From Eight Storms to Estimates – Wide Intervals and a Plausible Set

### Step 1: Count landfalls

The (illustrative) record of 8 severe storms, as (landfall zone, severity on a 1–3 scale), with zones numbered Z1 in the west to Z5 in the east:

(Z3, 2), (Z2, 3), (Z3, 1), (Z4, 2), (Z3, 3), (Z2, 2), (Z4, 1), (Z3, 2)

Tally the landfall zones. The natural estimate of each zone's probability is the proportion $k/n$ with $n = 8$:

| Zone | Storms $k$ | Proportion $k/8$ |
|---|---|---|
| Z1 (west end) | 0 | 0.000 |
| Z2 | 2 | 0.250 |
| Z3 (center) | 4 | 0.500 |
| Z4 | 2 | 0.250 |
| Z5 (east end) | 0 | 0.000 |

This is the **empirical distribution**: the probabilities you get by treating the record as the truth. It says a storm can never land at either end of the coast. Nobody believes that.

### Step 2: Put a margin of error on each proportion

From basic statistics, the usual 95% confidence interval for a proportion (the **Wald interval**) is

$$
\hat p \pm 1.96 \sqrt{\frac{\hat p (1-\hat p)}{n}}
$$

With $n = 8$ it gives nonsense at the edges. For a zone with no storms, $\hat p = 0$, so the interval is 0.000 to 0.000: perfect certainty from zero evidence. A better choice for small samples is the **Wilson interval**, which shifts the center slightly toward one half and never collapses to a single point:

$$
\frac{\hat p + \dfrac{z^2}{2n} \;\pm\; z\sqrt{\dfrac{\hat p(1-\hat p)}{n} + \dfrac{z^2}{4n^2}}}{1 + \dfrac{z^2}{n}}, \qquad z = 1.96
$$

| Zone | $k/8$ | Wald 95% interval | Wilson 95% interval |
|---|---|---|---|
| Z1 | 0.000 | 0.000 to 0.000 | 0.000 to 0.324 |
| Z2 | 0.250 | 0.000 to 0.550 | 0.071 to 0.591 |
| Z3 | 0.500 | 0.154 to 0.846 | 0.215 to 0.785 |
| Z4 | 0.250 | 0.000 to 0.550 | 0.071 to 0.591 |
| Z5 | 0.000 | 0.000 to 0.000 | 0.000 to 0.324 |

A simpler check gives the same message. The **rule of three** says that if an event happened 0 times in $n$ tries, a rough 95% upper bound on its probability is $3/n$. Here $3/8 = 0.375$. **A zone that has never been hit could still take more than a third of future storms**, as far as 8 storms can tell.

The center's share is somewhere between about 0.2 and 0.8. The record can't even tell us whether the center takes most storms or a minority of them. This is [The Core Bottleneck](#the-core-bottleneck--eight-storms-and-a-catastrophic-downside) in numbers.

### Step 3: Build a plausible set of probability patterns

If we can't pin the probabilities down, we can at least describe **which patterns are plausible**. Researchers call this set the **ambiguity set**: all the probability distributions that are close enough to the record that we can't rule them out.

How to measure "close enough"? This tutorial uses an idea that needs nothing beyond the record itself. Think of each recorded storm as a pile of probability of size $1/8$ sitting at its landfall zone. Ask: **what if some storms had landed a little further along the coast?** Moving one storm's pile by one zone costs $1/8 \times 1$; moving it by two zones costs $1/8 \times 2$. Give "nature" a moving budget $\varepsilon$ (the Greek letter epsilon):

- $\varepsilon = 0.25$: two of the eight storms moved one zone each (or one storm moved two zones).
- $\varepsilon = 0.5$: four storms moved one zone each, or two storms moved two zones.

Every probability pattern you can reach within the budget is in the plausible set. This "cost of moving piles" is called the **Wasserstein distance** (also known as the earth mover's distance), and the plausible set is a **Wasserstein ball** around the record. It is the construction of Mohajerin Esfahani & Kuhn (2018), simplified here to moving landfall only. With $\varepsilon = 0.5$, two storms moved from Z2 to Z1 would give the west end a probability of $2/8 = 0.25$, comfortably inside its Wilson interval.

Mohajerin Esfahani & Kuhn's construction isn't the only one. Delage & Ye (2010) build the plausible set from averages and spreads (moments) instead. The Wasserstein version suits this case because it speaks the language of the coast: "what if storms had landed nearby?"

### Step 4: Add what the record doesn't contain

Moving recorded storms along the coast can't produce a storm **stronger** than any on file, or a failure the record never showed, such as the inland road washing out. No reweighting of history creates those. They have to come from people who know the delta: the district disaster office and local engineers, in a workshop. The case keeps those workshop scenarios **out of the model** and uses them only to test it. [Code Implementation & Simulation](#code-implementation--simulation) does exactly that.

---

## The Decision Engine – Four Ways to Stock Three Warehouses

### The four decision rules

Write $x$ for the stock plan (kits per warehouse) and $U_k(x)$ for the **unmet need** in storm $k$: affected families who don't get a kit in time, given stock $x$ and the best possible dispatch after landfall. Each rule picks the $x$ that minimizes a different summary of the $U_k$:

| Plan | Chooses the stock that minimizes | In words |
|---|---|---|
| **A. Average storm** | (no optimization) stock in proportion to the average storm's damage | Plan for a storm that never happens |
| **B. Expected value** | $\sum_k p_k\, U_k(x)$ | Best on average, trusting the record's proportions $p_k$ |
| **C. Robust** | $\max_k U_k(x)$ | Best in the single worst storm considered possible |
| **D. Distributionally robust (DRO)** | $\max_{q \in \text{plausible set}} \sum_k q_k\, U_k(x)$ | Best on average under the least favorable plausible pattern of storms |

Plan B is called **two-stage stochastic programming**: Rawls & Turnquist (2010) used this form for hurricane pre-positioning. Plan C is **robust optimization**: it plays a game against nature, where you choose the stock first and nature then picks the storm that hurts you most. Choosing the plan whose worst case is least bad is called **minimax** (minimize the maximum). Plan D is **distributionally robust optimization**: nature picks not a single storm but the worst plausible *probability pattern* from [From Eight Storms to Estimates](#from-eight-storms-to-estimates--wide-intervals-and-a-plausible-set). It sits between B (nature has no freedom) and C (nature has total freedom).

### Step-by-step concrete example: three warehouses, 120 kits

A coast with three zones, North, Center and South, each with one warehouse. There are **120 kits**. Every storm leaves **80 families** needing a kit in the zone where it lands, and it floods the coastal road on both sides, so **only that zone's own warehouse can reach them within 2 days**. Of 8 recorded storms, **1 landed North, 5 Center, 2 South**, so the record's probabilities are $1/8, 5/8, 2/8$.

Because only the local warehouse helps, the unmet need for a storm in zone $z$ is simply

$$
U_z = \max(0,\ 80 - x_z)
$$

**Step A: Four stock plans, and the unmet need if the storm lands in each zone.**

- **A, average storm.** The average storm needs $80 \times 1/8 = 10$ kits North, $80 \times 5/8 = 50$ Center and $80 \times 2/8 = 20$ South. Scale up in proportion to use all 120 kits: 15, 75, 30.
- **B, expected value.** A kit in the Center warehouse is used in 5 storms out of 8, so fill the Center to 80 first; a kit in the South is used in 2 of 8, so the remaining 40 go South; North gets nothing.
- **C, robust.** Nature will pick the zone with the least stock, so make the three equal: 40 each.
- **D, distributionally robust.** Fill the Center to 80, then split the remaining 40 evenly between the two ends: 20 and 20. Step C shows why.

| Plan | Stock N / C / S | Unmet if North | Unmet if Center | Unmet if South |
|---|---|---|---|---|
| A. Average storm | 15 / 75 / 30 | 65 | 5 | 50 |
| B. Expected value | 0 / 80 / 40 | 80 | 0 | 40 |
| C. Robust | 40 / 40 / 40 | 40 | 40 | 40 |
| D. DRO | 20 / 80 / 20 | 60 | 0 | 60 |

**Step B: Expected and worst-case unmet need.** The expected value weights each column by the record: $\tfrac18 \times \text{North} + \tfrac58 \times \text{Center} + \tfrac28 \times \text{South}$. For plan A:

$$
\tfrac18(65) + \tfrac58(5) + \tfrac28(50) = \frac{65 + 25 + 100}{8} = 23.75
$$

For plan D: $(60 + 0 + 120)/8 = 22.5$. For B: $(80 + 0 + 80)/8 = 20$. For C: 40. The worst case is the largest number in each row.

| Plan | Expected unmet (record's odds) | Worst-case unmet |
|---|---|---|
| A. Average storm | 23.75 | 65 |
| B. Expected value | **20.00** | 80 |
| C. Robust | 40.00 | **40** |
| D. DRO | 22.50 | 60 |

Plan A loses to plan D on **both** measures. Planning for the average storm isn't a cautious compromise; it is simply worse.

**Step C: The worst plausible pattern.** Use the plausible set from [From Eight Storms to Estimates](#from-eight-storms-to-estimates--wide-intervals-and-a-plausible-set) with $\varepsilon = 0.25$: nature may move two of the eight storms one zone each. Center is next to both ends, so nature's best move is to take two Center storms and land them at whichever end the plan has left weakest. The odds become $3/8, 3/8, 2/8$ (or $1/8, 3/8, 4/8$ if South is weaker). For plan D:

$$
\tfrac38(60) + \tfrac38(0) + \tfrac28(60) = \frac{180 + 0 + 120}{8} = 37.5
$$

| Plan | Worst plausible pattern (out of 8) | Expected unmet under it |
|---|---|---|
| A. Average storm | 3 / 3 / 2 | 38.75 |
| B. Expected value | 3 / 3 / 2 | 40.00 |
| C. Robust | any (all zones equal) | 40.00 |
| D. DRO | 3 / 3 / 2 | **37.50** |

Plan D wins this contest because it gives nature nothing to exploit: both ends are equally stocked, so moving storms to either end costs the same, and the Center, still the most likely landfall, stays full. Try nudging it: with 10 / 80 / 30, nature moves two storms North and the figure rises to $(3 \times 70 + 2 \times 50)/8 = 38.75$.

### Writing the plans as linear programs

The code doesn't reason through cases like this; it hands each rule to a solver as a **linear program**: a list of unknowns (the stock in each warehouse), a goal to minimize that is a sum of unknowns times fixed numbers, and rules (constraints) of the same simple form. The [Case 2 tutorial](02-welfare-optimization-borehole-siting.md) introduces linear and integer programs in more detail. Plan C, for example, is:

$$
\begin{aligned}
\text{minimize } & t \\
\text{subject to } & t \ge U_z, \quad U_z \ge 80 - x_z, \quad U_z \ge 0 \quad \text{for each zone } z \\
& x_N + x_C + x_S = 120, \quad x \ge 0
\end{aligned}
$$

The trick for "minimize the maximum" is the extra unknown $t$, forced to be at least every zone's unmet need. Minimizing $t$ pushes the largest $U_z$ down. The solver returns 40 / 40 / 40.

Plan D looks harder, because it contains a "worst plausible pattern" inside it. A result from the theory of linear programs (called **duality**, used by Mohajerin Esfahani & Kuhn) rewrites it as an ordinary minimization:

$$
\min_{x,\ \lambda \ge 0}\ \ \lambda\,\varepsilon \;+\; \frac{1}{N}\sum_{i=1}^{N}\ \max_{z}\ \Big[\, U_z(x) - \lambda\, |z - z_i| \,\Big]
$$

Read $\lambda$ (lambda) as **the price nature pays to move one storm by one zone**. For each recorded storm $i$ that landed in zone $z_i$, nature looks for the zone $z$ where moving it does the most harm after paying the moving price. The first term charges the total moving budget $\varepsilon$ at that price. The solver picks the stock and the price together, and returns 20 / 80 / 20.

### The price of robustness

Compare the plans with plan B, the best on the record's own odds:

- **Plan C** cuts the worst case from 80 families to 40, but doubles expected unmet need, from 20 to 40. It treats a Center storm, the most common kind, as no more likely than a North storm.
- **Plan D** cuts the worst case from 80 to 60 and raises expected unmet need only from 20 to 22.5.

The extra unmet need on average (or, with a flexible budget, the extra stock) that a plan accepts in exchange for a better worst case is called the **price of robustness**. Every robust plan pays it. The question is never "robust or not?" but "how much protection, at what price?" The plausible-set size $\varepsilon$ is the dial: $\varepsilon = 0$ gives plan B, and in this toy a large enough $\varepsilon$ gives plan C.

---

## Scaling Up – Six Warehouses, Broken Roads and Dispatch Cards

The toy has one warehouse per zone and a single road rule. The full model in the code keeps the same logic with more realistic pieces.

**1. The coast and its people.** Five coastal zones, Z1 (west) to Z5 (east). Each zone has a coastal shelter area of 45,000 families and an inland one of 30,000. A storm of severity $s$ leaves $12\% \times s$ of coastal families in the landfall zone needing a kit, $4\% \times s$ in each neighboring zone, and half those shares inland. A recorded storm landing in Z2–Z4 leaves 12,000, 24,000 or 36,000 families needing kits at severity 1, 2 or 3.

**2. Warehouses and roads.** W1–W5 sit one per zone on the coast; W6 is an inland hub behind Z3. Within 2 days, a coastal warehouse can reach its own zone and the neighboring zones, crossing a bridge; W6 reaches Z2–Z4 by an inland road. A storm of severity 2 or more cuts the bridges on both sides of landfall; a severity-4 storm also cuts the next ones out.

**3. Stage 2 as a small linear program.** For each storm, the dispatch decides $f_{wa}$, the kits warehouse $w$ sends to area $a$:

$$
\begin{aligned}
\text{maximize } & \textstyle\sum_{w,a} f_{wa} \\
\text{subject to } & \textstyle\sum_a f_{wa} \le x_w \ \text{(no more than the stock)}, \quad \sum_w f_{wa} \le d_a \ \text{(no more than the need)}, \\
& f_{wa} = 0 \text{ if the road from } w \text{ to } a \text{ is cut}, \quad f \ge 0
\end{aligned}
$$

The share reached is $\sum f_{wa} / \sum_a d_a$, and $U_k(x)$ is one minus that. The planning models put all the storms' stage-2 programs inside one big linear program with the stock, so the solver weighs every storm at once.

**4. Which storms each plan considers.** Plan B uses the 8 recorded storms at their recorded weights. Plans C and D also consider each recorded storm moved to every other landfall zone at the same severity: 5 zones × 3 severities = 15 distinct planning storms. Plan C guards against the worst of the 15; plan D lets nature move probability among them within the budget $\varepsilon$.

**5. Choosing how robust to be, with funders.** The case says the robustness level should be chosen with funders, since more protection costs more stock. The code shows the dial in two ways. With the 30,000 kits fixed, it reports what each $\varepsilon$ gives up on the recorded storms and gains on the unseen ones. With stock allowed to vary, it reports how many kits it takes to reach 90% of affected families on average, in every recorded storm, and wherever a recorded-strength storm could land. That second table is the one to put in front of a donor who asks why the plan holds "excess" inventory.

**6. Dispatch cards are stage-2 plans computed in advance.** During a response, staff often have no connectivity. So the model solves the stage-2 program ahead of time, for each landfall zone and each common pattern of road failure, and prints the answer as a laminated card per warehouse manager: "If landfall is in Z1 and bridge B12 is out, send these kits to these shelters." The card needs no phone and no spreadsheet.

**7. Stress testing out of sample.** Following the [case's pilot design](../cases/04-cyclone-prepositioning.md#follow-up-3-pilot-design), every plan is judged on two sets: the 8 recorded storms (the replay), and 10 workshop-style stress scenarios the models never saw: landfall at each end of the coast, storms stronger than any on file, the inland road washed out, an extra bridge down. A plan that only looks good on the storms it was built from has proved nothing.

---

## Code Implementation & Simulation

The full program is [`code/case4_robust_prepositioning.py`](code/case4_robust_prepositioning.py). It needs `numpy` and `pulp` (PuLP 3, which ships with the free CBC solver) and runs in a few seconds:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case4_robust_prepositioning.py
```

### Stage 2: dispatch over the surviving roads

```python
def add_dispatch(prob, x, sc, tag):
    """Stage 2 inside a planning model: ship kits over the surviving roads.
    Returns the unmet SHARE of affected families (0 = everyone reached)."""
    f = {lk: pulp.LpVariable(f"f_{tag}_{lk[0]}_{lk[1][0]}{lk[1][1]}", lowBound=0)
         for lk in sc["links"]}
    for w in WAREHOUSES:
        prob += pulp.lpSum(v for (ww, _), v in f.items() if ww == w) <= x[w]
    for a in AREAS:
        prob += pulp.lpSum(v for (_, aa), v in f.items() if aa == a) <= sc["need"][a]
    total = sum(sc["need"].values())
    return 1 - pulp.lpSum(f.values()) / total
```

Only the roads that survive the storm (`sc["links"]`) get a shipment variable, so a cut road simply can't carry kits.

### Stage 1: the three optimized plans in one function

```python
    if method == "expected":
        prob += avg_hist + tie * (avg_hist + worst)
    elif method == "robust":
        prob += worst + tie * (avg_hist + worst)
    elif method == "dro":
        lam = pulp.LpVariable("lam", lowBound=0)
        s = [pulp.LpVariable(f"s_{i}") for i in range(len(HISTORY))]
        for i, (lf, sev) in enumerate(HISTORY):
            for z in ZONES:
                prob += s[i] >= U[(z, sev)] - lam * abs(z - lf)
        prob += lam * eps + pulp.lpSum(s) / len(HISTORY) + tie * (avg_hist + worst)
```

`avg_hist` is the average unmet share over the 8 recorded storms, and `worst` the largest unmet share over the 15 planning storms. The DRO lines are the formula from [The Decision Engine](#the-decision-engine--four-ways-to-stock-three-warehouses), with `lam` as nature's moving price. Several stock layouts often score exactly the same, so a tiny weight (`tie = 0.01`) on the average and the worst case picks among them.

### Results

```
Simulation - full model: 6 warehouses, 30,000 kits, 10 shelter areas
  families needing a kit per recorded storm, by severity: [12000, 24000, 36000]
  planning storms for robust/DRO (zone, severity): 15

  Stock per warehouse (kits)
                         W1     W2     W3     W4     W5     W6
  A average storm      1875   8625  12000   6375   1125      0
  B expected value     4800      0      0   1200   4800  19200
  C robust             8677      0   4800      0   8677   7846
  D DRO eps=0.5        7543      0   1800      0   7543  13114

  Share of affected families reached within 2 days
                      8 storms: avg  worst   | 10 stress: avg  worst
  A average storm            0.772  0.492   |            0.407  0.195
  B expected value           0.942  0.700   |            0.497  0.167
  C robust                   0.826  0.551   |            0.532  0.263
  D DRO eps=0.5              0.884  0.614   |            0.521  0.250

  Stress scenarios one by one (share reached)
  west end, severe                  A=0.32  B=0.42  C=0.55  D=0.51
  east end, severe                  A=0.29  B=0.42  C=0.55  D=0.51
  west end, moderate                A=0.35  B=0.50  C=0.70  D=0.64
  east end, moderate                A=0.31  B=0.50  C=0.70  D=0.64
  center, stronger than record      A=0.56  B=0.43  C=0.26  D=0.31
  east end, stronger than record    A=0.20  B=0.38  C=0.43  D=0.45
  Z2 severe, inland road out        A=0.49  B=0.17  C=0.33  D=0.25
  Z4 severe, inland road out        A=0.41  B=0.17  C=0.33  D=0.25
  Z2 moderate, extra bridge out     A=0.64  B=1.00  C=0.73  D=0.82
  Z4 moderate, extra bridge out     A=0.51  B=1.00  C=0.73  D=0.82

  Choosing how robust to be: DRO radius eps (average zone-shift per storm)
  eps=0 (plan B)  W1= 4800 W3=    0 W5= 4800 W6=19200  8 storms avg=0.942 worst=0.700  any zone worst=0.417  stress avg=0.497 worst=0.167
  eps=0.25        W1= 7200 W3= 1800 W5= 7200 W6=13800  8 storms avg=0.896 worst=0.633  any zone worst=0.500  stress avg=0.521 worst=0.250
  eps=0.5         W1= 7543 W3= 1800 W5= 7543 W6=13114  8 storms avg=0.884 worst=0.614  any zone worst=0.512  stress avg=0.521 worst=0.250
  robust (plan C) W1= 8677 W3= 4800 W5= 8677 W6= 7846  8 storms avg=0.826 worst=0.551  any zone worst=0.551  stress avg=0.532 worst=0.263

  Price of robustness in kits: smallest stock reaching 90% ...
  average    :    24960 kits
  each storm :    34800 kits
  every zone :    62640 kits

  Dispatch card, plan D, landfall Z1 severity 3 (bridge B12 out)
    W1 -> zone 1 coast     7543 kits
    W3 -> zone 2 inland    1800 kits
    W6 -> zone 2 coast     5400 kits
    share reached within 2 days = 0.512
```

The same run first prints the intervals from [From Eight Storms to Estimates](#from-eight-storms-to-estimates--wide-intervals-and-a-plausible-set) and the toy tables from [The Decision Engine](#the-decision-engine--four-ways-to-stock-three-warehouses), matching the numbers above.

### Reading the results

**On the 8 recorded storms, plan B looks best**: it reaches 94.2% of affected families on average and 70.0% in the worst recorded storm. Of course it does; it was built from those storms. Plan A, the average-storm plan, reaches 77.2% on average and 49.2% in the worst recorded storm.

**On the 10 storms nobody planned for, the order changes.** Plan B's worst case falls to 16.7%. The robust plans hold up better: C reaches 26.3% in its worst stress scenario and D 25.0%, against 19.5% for A and 16.7% for B. The gain is clearest at the ends of the coast, where no recorded storm has landed. (Plans C and D did consider end-of-coast landfalls, because they moved recorded storms there; they never saw the workshop list itself.) In a severe west-end storm, C and D reach 55% and 51% of families against B's 42% and A's 32%. Plans C and D improve on A in all four summary numbers, so by the case's decision rule (adopt if worst-case reach improves on the current layout and the stock fits the budget), either would pass if A stands in for the current layout.

**The price of robustness is visible and moderate for D.** Moving from B to D gives up 5.8 points of average reach on the recorded storms (0.942 to 0.884) and raises the worst stress result from 16.7% to 25.0%. Plan C gives up 11.6 points (0.942 to 0.826) for a little more protection. The dial table shows the trade-off step by step: as $\varepsilon$ grows, average reach on the record falls (0.942, 0.896, 0.884, then 0.826 for C) while the worst case over every landfall zone rises (0.417, 0.500, 0.512, 0.551). (In the full model, plan C is the most protective setting rather than the literal end of the $\varepsilon$ dial: nature may move a storm's landfall but not make it stronger, so the DRO plan never reduces exactly to "guard against the single worst storm.")

**In kits, robustness is expensive.** Reaching 90% of families on average over the recorded storms takes 24,960 kits; reaching 90% in each recorded storm takes 34,800; reaching 90% wherever a storm of recorded strength could land takes 62,640, about two and a half times the first figure ($62{,}640 / 24{,}960 \approx 2.5$). That is the conversation to have with funders: which of these promises are they paying for?

**The dispatch card** for a severe west-end storm under plan D tells W1 to send all 7,543 of its kits to Zone 1's coastal shelters, W3 to send 1,800 to Zone 2 inland and W6 to send 5,400 to Zone 2's coast. That reaches 51.2% of the 28,800 affected families ($16{,}200 + 5{,}400$ in Zone 1, $5{,}400 + 1{,}800$ in Zone 2). Zone 1's 5,400 inland families get nothing within 2 days: with bridge B12 out, W1 is the only warehouse that can reach Zone 1 at all, and its stock is smaller than Zone 1's need. (The solver happened to send all of W1's kits to the coast; any split between Zone 1's two areas reaches the same number of families, so the card's author can choose.) A card like this also tells the planners where the plan is thin.

### Cautions

Four things the numbers do **not** show.

1. **A robust plan is only robust against what is in its set.** Plans C and D lean on the inland hub W6 because no planning storm cut the inland road. When the workshop scenarios cut it, C and D reach 33% and 25% of families against A's 49% and 41%. Likewise, the center storm stronger than any on record hurts C (26%) more than A (56%), which kept most stock in the center. This is why the workshop scenarios must come from local engineers, and why the plan should be rerun after they are added to the planning set (with a new stress set for testing).
2. **No layout of 30,000 kits handles the worst storms well.** Every plan's worst stress result is below 27%. The honest message is that stock placement can't substitute for more stock, faster routes or other measures in the worst cases.
3. **Out-of-sample results don't move smoothly with $\varepsilon$.** The stress columns improve from $\varepsilon = 0$ to $\varepsilon = 0.25$ and then barely change. The dial guarantees a trade-off only on the storms the model was given.
4. **Everything here is invented.** The coast, populations, storm effects and road rules are made up to teach the method; real gains depend on a real road map and real storm footprints. The model also ignores costs the case cares about, such as storage and the kits that expire unused in remote warehouses. A real version would add them; the pilot's harm measure tracks them.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Scenarios** | storm $k$ = (landfall, severity, needs $d_{ka}$, cut roads) | Describes each possible storm completely enough to plan a response to it |
| **Stage 1: stock** | $x_w \ge 0,\ \sum_w x_w = 30{,}000$ | The commitment made before the season, one number per warehouse |
| **Stage 2: dispatch** | $\max \sum f_{wa}$ s.t. $\sum_a f_{wa} \le x_w$, $\sum_w f_{wa} \le d_{ka}$, cut roads $= 0$ | Best response after landfall; printed in advance as dispatch cards |
| **Small-sample intervals** | Wilson interval; rule of three $\approx 3/n$ | Shows how little 8 storms say about each zone's odds |
| **Expected value (B)** | $\min_x \sum_k p_k\, U_k(x)$ | Best on average if the record's odds were exact |
| **Robust / minimax (C)** | $\min_x \max_k U_k(x)$, via $t \ge U_k$ | Best in the worst storm considered possible |
| **Plausible set** | Wasserstein ball: move storms, cost $= \tfrac1N \times$ zones moved $\le \varepsilon$ | All probability patterns close enough to the record to be credible |
| **DRO (D)** | $\min_{x,\lambda \ge 0} \lambda\varepsilon + \tfrac1N \sum_i \max_z [U_z - \lambda\lvert z - z_i\rvert]$ | Best average under the worst plausible pattern; $\varepsilon$ is the robustness dial |
| **Price of robustness** | average reach given up, or extra kits for the same target | What funders pay for protection; chosen with them, not for them |
| **Out-of-sample test** | replay 8 storms + ~10 workshop stress scenarios kept out of the model | Tells you whether the plan holds up on storms it never saw |

### Where to go next

- **Run the pilot** described in the [case's follow-ups](../cases/04-cyclone-prepositioning.md#after-the-recommendation): replay the recorded storms, stress-test with workshop scenarios kept out of the model, and run a tabletop exercise with the dispatch cards and no phones. The [playbook's pilot section](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) has the general rules.
- **Read** Rawls & Turnquist (2010) on pre-positioning emergency supplies first, then Rahimian & Mehrotra (2022), *Frameworks and Results in Distributionally Robust Optimization*, an [open-access review](https://doi.org/10.5802/ojmo.15). Delage & Ye (2010) and Mohajerin Esfahani & Kuhn (2018) are the foundational DRO papers. See the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Tools and help:** [RSOME](https://xiongpengnus.github.io/rsome/) writes robust and distributionally robust models in Python; Pyomo with the free HiGHS solver handles the stochastic version. This is the hardest class to model well, so look for an operations-research specialist, for example through INFORMS Pro Bono Analytics ([build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners)).
- **Other tutorials:** the [Case 2 tutorial](02-welfare-optimization-borehole-siting.md) covers the location model that this robustness layer sits on; the [Case 1 tutorial](01-restless-bandits-chw-visits.md) shows the opposite situation, where errors are cheap and learning by trial is the right approach; the [vehicle routing tutorial](10-vehicle-routing-food-delivery.md) ([Class 9](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics)) covers the case where moving the goods, not preparing for the storm, is the hard part; the [Case 6 tutorial](06-no-model-food-pantry.md) covers when no model is needed at all.
