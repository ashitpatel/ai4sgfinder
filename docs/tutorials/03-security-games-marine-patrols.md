# Security Games Masterclass: Where Should the Patrol Boats Go Today?

*An in-depth walkthrough of Stackelberg security games, randomized patrols and patrol-effort-aware risk estimates, built on [Case 3: Patrolling a marine protected area against illegal fishing](../cases/03-marine-patrols.md).*

**You need:** proportions, means, expected values and the idea of a confidence interval. **You don't need:** any machine learning, game theory or optimization background. Every term is explained when it first appears.

**Approach:** [Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search). **Code:** [`code/case3_security_game.py`](code/case3_security_game.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A coastal conservation trust co-manages a marine protected area divided into 40 zones. It has 2 patrol boats, and each can cover about 3 zones a day: **6 zone-visits a day for 40 zones.** Illegal net fishing in the no-take zones is rising. Every day someone has to decide **which 6 zones the boats visit.**

The usual answers fail in instructive ways. A fixed rotation is fair to every zone, but fishers watch the jetty and learn it within days. A hotspot map sends boats where past incidents were recorded, but incidents are only recorded where boats already go. When the trust patrolled the northern reef every morning for a month, catches there dropped and the nets moved south. A hotspot map would still have pointed north.

This tutorial builds the alternative step by step:

1. **[The Strategic Leap](#the-strategic-leap--from-a-patrol-map-to-a-game)** treats patrolling as a *game*: the trust commits to a plan, the fishers watch and respond. The answer is a **randomized** plan.
2. **[The Core Bottleneck](#the-core-bottleneck--unknown-payoffs-unknown-rationality-biased-data)** names what we don't know: what each zone is worth to the fishers, how carefully they choose, and how biased the patrol records are.
3. **[From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went)** turns three years of patrol logs into estimates of where fishing happens, correcting for where the boats went, with honest margins of error.
4. **[The Decision Engine](#the-decision-engine--the-stackelberg-equilibrium)** computes the best randomized plan for a 3-zone toy example by hand, then confirms it with a solver.
5. **[Scaling Up](#scaling-up--40-zones-2-boats-one-paper-schedule)** scales up to 40 zones and 2 boats and turns probabilities into a daily list a captain can follow.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all in code against fishers who learn from what they see, and compares it with rotation and hotspot patrols.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **be unpredictable on purpose, and put the unpredictability where it hurts the fishers most.**

---

## The Strategic Leap – From a Patrol Map to a Game

### Why a map isn't enough

A hotspot map, or a rotation, answers "where should we go?" as if the fish and the fishers stood still. They don't. The fishers are making their own decision, and they make it **after** watching ours. A plan that ignores this is a plan the other side can read.

That is also what separates this problem from its closest neighbor, [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection). Risk-based inspection ranks places by the predicted chance of a hidden problem and checks the top of the list, which works for lead pipes: they stay put whether or not you look. Illegal nets are a hidden problem that moves in response to your list, so a published ranking becomes a map of where not to fish. The risk estimates in [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went) do the same job as a Class 12 model, but here they feed a randomized plan. Two other neighbors fall away for the same reason: [Class 8: Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) learns where effort pays off when nobody is evading you, and [Class 9: Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics) minimizes travel cost. Neither plans against an opponent who reads the plan.

### What a game is

In game theory, a **game** is any situation where the outcome for each side depends on what the other side does. The sides are called **players**. Here there are two:

- the **defender**: the trust, choosing where the boats go;
- the **adversary**: the illegal fishers, choosing where to set nets.

A player's **payoff** is a number for how good an outcome is for them. For a fishing crew: the value of the catch if no boat comes, and a loss (nets confiscated, a fine) if one does.

### Who moves first: the Stackelberg setup

In many games both players move at once. Patrolling is different. The trust sets a pattern, and the fishers observe it over days and weeks before deciding. A game where one player **commits first** and the other **observes and responds** is called a **Stackelberg game**, after the economist Heinrich von Stackelberg. The player who commits first is the **leader**; the one who responds is the **follower**.

When the leader is protecting things from an adversary, this is a **Stackelberg security game**. It is the model behind ARMOR at Los Angeles airport checkpoints (Pita et al., AAMAS 2008), PROTECT for US Coast Guard port patrols (Shieh et al., AAMAS 2012), and PAWS for anti-poaching patrols (Fang et al., IAAI 2016). Fang, Stone and Tambe (IJCAI 2015) adapted it to protecting natural resources, including fisheries, under the name **green security games**.

### Pure and mixed strategies

A **strategy** is a complete plan of action. There are two kinds:

- A **pure strategy** is one fixed choice: "patrol zones 0, 1, 2, 3, 4, 5 today." A rotation is a sequence of pure strategies, and so is "always patrol the hotspots."
- A **mixed strategy** is a set of probabilities over pure strategies: "patrol zone 0 with probability 0.33, zone 1 with probability 0.39, …", with the actual zones drawn at random each day.

If the fishers can observe what you do, any pure strategy tells them exactly where you won't be. A mixed strategy tells them only the **odds**. The trust's real choice, then, is the **coverage probability** of each zone: the chance that a boat visits it on a given day. The game asks which coverage probabilities leave the fishers with the worst best option.

The key assumption, and the reason the leader commits first: **assume the fishers will eventually learn your coverage probabilities.** You can't hide the odds for long; you can only hide each day's draw.

### Mapping it to the program

| Game term | In this program |
|---|---|
| Targets | The 40 zones of the marine protected area, numbered 0 (north) to 39 (south) |
| Defender resources | 2 boats × about 3 zones a day = 6 zone-visits a day |
| Coverage probability $c_i$ | The chance that zone $i$ is patrolled on a given day; the 40 values add up to 6 |
| Adversary | Net-fishing crews who watch the jetty and shift within days |
| Adversary payoff, unprotected | The value of a night's illegal catch in that zone, $G_i$ |
| Adversary payoff, caught | A loss $P$: nets confiscated and a fine |
| Round | One day; the plan is refit monthly when the SMART data arrives |

---

## The Core Bottleneck – Unknown Payoffs, Unknown Rationality, Biased Data

The math of [The Decision Engine](#the-decision-engine--the-stackelberg-equilibrium) is exact once you know the payoffs. Three things make knowing them hard.

**1. What each zone is worth to the fishers.** $G_i$ depends on fish density, distance from the landing sites, sea conditions and market prices. None of it is written down. It has to be estimated from where fishing actually happens, which is [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went)'s job, together with local knowledge from rangers and the fishing committees.

**2. How carefully the fishers choose.** The textbook game assumes a perfectly **rational** adversary: one who always picks the zone with the highest expected payoff. Real crews make mistakes, have favorite spots and share rumors. Researchers call this **bounded rationality** and model it by letting crews pick better zones *more often*, not always. The simulation in [Code Implementation & Simulation](#code-implementation--simulation) uses fishers like this.

**3. Detection bias.** The trust's evidence comes from SMART (the Spatial Monitoring and Reporting Tool), where rangers log GPS tracks and incidents. An incident can only be recorded where a boat goes, and even there a net can be missed. So the records show **where the boats went at least as much as where the fishing is.** The [case's readiness check](../cases/03-marine-patrols.md#follow-up-2-readiness-checks) flags this as "not ready." [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went) is about fixing it.

---

## From Patrol Logs to Estimates – Correcting for Where the Boats Went

The code generates three years of made-up SMART logs for the 40 zones, built to resemble the case: the northern reef (zones 0–7) was patrolled heavily; five far zones (22, 27, 31, 35, 38) were rarely visited because of fuel; and the fishers have since moved toward the south and the far zones.

```
total patrol hours=12010, total incidents=419,
share of hours on northern reef (zones 0-7)=0.74, share of incidents there=0.55
```

### Step 1: Raw counts mislead

Over half the incidents are on the northern reef. A hotspot map built from counts says "patrol the north." Compare two zones:

| Zone | Patrol hours | Incidents |
|---|---|---|
| 3 (northern reef) | 1,106 | 42 |
| 31 (far south) | 33 | 7 |

Zone 3 has 6 times as many incidents. It also had 33 times as many hours of looking. Counts mix two things: how much fishing there is, and how hard you searched.

### Step 2: Incidents per patrol hour

Divide by effort. The **rate** is incidents per patrol hour:

$$
\text{rate}_i = \frac{\text{incidents}_i}{\text{patrol hours}_i}
$$

Zone 3: $42 / 1106 = 0.038$ per hour. Zone 31: $7 / 33 = 0.212$ per hour. Per hour of searching, **zone 31 turns up about 5.6 times as many nets**, the opposite of what the counts said.

### Step 3: Detection probability

Even in the right zone, a boat doesn't find every net. Call the chance of spotting a net that is there the **detection probability**, $d$. Then, on average,

$$
\text{expected incidents}_i = \text{patrol hours}_i \times \text{nets per hour}_i \times d
$$

so the rate per hour estimates $\text{nets per hour} \times d$, and dividing by $d$ recovers the fishing level itself. In the simulation $d = 0.5$: zone 3's estimate becomes $0.038 / 0.5 = 0.076$ nets per hour and zone 31's becomes $0.212 / 0.5 = 0.424$. (The true values built into the code are 0.054 and 0.306.)

If $d$ is the same everywhere, it doesn't change the ranking of zones. It matters when it differs, for example if nets are harder to spot in mangroves than in open water, or at night. Then each zone's rate should be divided by its own $d$, estimated by rangers or from test searches.

### Step 4: Margins of error, and why few hours mean wide ones

Counts of rare events follow what statisticians call a **Poisson** pattern: the spread of a count is about the square root of the count. That gives a rough 95% interval for the rate:

$$
\text{rate} \pm 1.96\,\frac{\sqrt{\text{incidents}}}{\text{hours}}
$$

| Zone | Hours | Incidents | Rate | 95% range | True value × $d$ |
|---|---|---|---|---|---|
| 3 | 1,106 | 42 | 0.038 | 0.026 to 0.049 | 0.027 |
| 31 | 33 | 7 | 0.212 | 0.055 to 0.369 | 0.153 |
| 38 | 33 | 4 | 0.121 | 0.002 to 0.240 | 0.153 |

(The last column is the true nets per hour, 0.054 and 0.306, times $d = 0.5$.) Zone 3's range is narrow; zones 31 and 38 have ranges several times wider. Zone 38 truly has as much fishing as zone 31, but with only 4 incidents in 33 hours its estimate came out low.

When a zone has **zero** incidents, the formula above gives a width of zero, which is wrong. Use the **rule of three** instead: with 0 events in $h$ hours, the 95% upper limit on the rate is about $3/h$. A zone with 0 incidents in 12 hours could still have a rate as high as $3/12 = 0.250$ per hour, higher than any estimated rate in the table. "No incidents recorded" in a rarely visited zone means "we don't know," not "safe."

### Step 5: Putting it together

Rank the 40 zones three ways:

```
top 5 by raw count : [1, 3, 4, 5, 7]
top 5 by rate/hour : [22, 31, 34, 35, 38]
top 5 by true risk : [22, 27, 31, 35, 38]
```

Raw counts point entirely at the northern reef, where the fishing is now *lowest*. Rates per hour find 4 of the 5 truly busiest zones. The one they miss, zone 27, is a rarely visited zone (33 hours, 3 incidents) whose few hours happened to be unlucky, which is exactly what the wide margins warn about.

Two practical conclusions, both from the [case's readiness checks](../cases/03-marine-patrols.md#follow-up-2-readiness-checks):

1. **Feed patrol effort into the risk model, not just incidents.** SMART already records GPS tracks, so hours per zone per month can be computed from the export.
2. **Send some patrols to low-information zones on purpose.** Without them, the margins there never narrow and the data keeps confirming old hotspots. [Scaling Up](#scaling-up--40-zones-2-boats-one-paper-schedule) shows what this costs.

Real systems such as PAWS go further: they predict risk from past patrol effort *and* features of each place (terrain, distance to roads or villages) with machine-learning models, then plan patrols that allow for the uncertainty in those predictions (Xu et al., ICDE 2020). The rate-per-hour table is the hand-sized version of the same idea.

---

## The Decision Engine – The Stackelberg Equilibrium

### The question it answers

Given each zone's value to the fishers, what coverage probabilities make **the fishers' best option as poor as possible**, knowing they will see the probabilities and pick their best zone?

### The fishers' expected payoff

If zone $i$ is patrolled with probability $c_i$, a crew fishing there keeps $G_i$ with probability $1 - c_i$ and loses $P$ with probability $c_i$. Its **expected payoff** (the probability-weighted average) is

$$
\text{EU}_i = (1 - c_i)\,G_i - c_i\,P = G_i - c_i\,(G_i + P)
$$

Every extra unit of coverage lowers that zone's payoff by $G_i + P$. The fishers pick the zone with the largest $\text{EU}_i$.

### Step-by-step concrete example: three zones, one boat

One boat patrols one zone a day, so the coverage probabilities add up to 1. A caught crew loses $P = 4$. The zones are worth:

| Zone | Value to fishers $G_i$ | $G_i + P$ |
|---|---|---|
| North reef | 8 | 12 |
| Central bank | 4 | 8 |
| South bay | 2 | 6 |

**Step A: Simple plans get exploited.** Compute each zone's $\text{EU}_i = G_i - c_i(G_i + 4)$ and see where the fishers go:

| Plan | Coverage (N, C, S) | Fishers' payoff (N, C, S) | Fishers' best |
|---|---|---|---|
| Always the North reef | 1, 0, 0 | −4, 4, 2 | **4** at Central bank |
| Uniform random | 1/3, 1/3, 1/3 | 4, 1.333, 0 | **4** at North reef |
| In proportion to value | 0.571, 0.286, 0.143 | 1.143, 1.714, 1.143 | **1.714** at Central bank |

Always guarding the north is the case's northern-reef story in miniature: the fishers simply move. Uniform random over-protects the South bay and leaves the reef too open. Coverage proportional to value is better but still leaves the Central bank as a soft spot.

A **predictable rotation** (North, Central, South, repeat) is worse than all of them. Fishers who know today's zone go to the best one that isn't covered: on a North day they fish the Central bank (4); on Central or South days they fish the North reef (8). On average they get $(4 + 8 + 8)/3 = 6.667$, more than under any plan in the table.

**Step B: Make the fishers indifferent.** Look at the last plan: one zone is a soft spot. If any zone gives the fishers more than the others, the trust can move a little coverage *to* it, from zones the fishers aren't choosing, and their best option gets worse. That stops only when every zone the fishers might pick gives them **the same** payoff, call it $U$. (This is the defining property of the best plan in these games: the follower is left **indifferent** among the targets it might attack.)

Set every zone's payoff equal to $U$ and solve for the coverage:

$$
G_i - c_i\,(G_i + 4) = U \quad\Longrightarrow\quad c_i = \frac{G_i - U}{G_i + 4}
$$

The coverages must add up to 1:

$$
\frac{8 - U}{12} + \frac{4 - U}{8} + \frac{2 - U}{6} = 1
$$

Split each fraction: $\left(\frac{8}{12} + \frac{4}{8} + \frac{2}{6}\right) - U\left(\frac{1}{12} + \frac{1}{8} + \frac{1}{6}\right) = 1$, which is $1.5 - 0.375\,U = 1$, so

$$
U = \frac{0.5}{0.375} = \frac{4}{3} \approx 1.333
$$

and the coverages are

$$
c_{\text{North}} = \frac{8 - 4/3}{12} = \frac{5}{9} \approx 0.556, \qquad
c_{\text{Central}} = \frac{4 - 4/3}{8} = \frac{1}{3} \approx 0.333, \qquad
c_{\text{South}} = \frac{2 - 4/3}{6} = \frac{1}{9} \approx 0.111
$$

They add up to $5/9 + 3/9 + 1/9 = 1$, and all are between 0 and 1, so the boat really can carry this plan out: on any given day, go North with probability 5/9, Central with probability 1/3, South with probability 1/9.

**Step C: Check it.** Each zone now pays the fishers $8 - \frac{5}{9} \cdot 12 = 4 - \frac{1}{3} \cdot 8 = 2 - \frac{1}{9} \cdot 6 = 1.333$. To push any one zone below 1.333, the boat would need more coverage there, which means less somewhere else, which pushes that zone *above* 1.333. So **1.333 is the lowest best option the trust can leave the fishers.** Compare: 4 for always-North, 1.714 for proportional coverage, 6.667 for a predictable rotation. Same single boat, same days at sea.

Notice what the plan does *not* do. It doesn't send the boat only to the richest zone, and it does visit the South bay, worth just 2, about one day in nine. Without that, the South bay would pay the fishers 2, more than 1.333, and they'd go there.

This pair of plan and response is called the **Stackelberg equilibrium**: the trust's best commitment, given that the fishers respond as well as they can to it.

### Confirming it with a solver: linear programs

The hand method works when you can guess which zones the fishers will consider. With 40 zones you can't, so we hand the problem to a **linear program** (LP). An LP is a recipe for choosing some numbers (here, the coverages) to make a quantity as large or as small as possible, where the quantity and every rule are sums of the numbers times fixed weights. Free solvers find the exact best answer in milliseconds. (The [Case 2 tutorial](02-welfare-optimization-borehole-siting.md) covers LPs and their whole-number cousins in more depth.)

The **multiple LPs** method, a standard way to solve these games, runs one LP per zone. For each zone $t$:

$$
\begin{aligned}
\text{maximize}\quad & \text{the trust's expected payoff if zone } t \text{ is fished} \\
\text{subject to}\quad & \text{EU}_t \ge \text{EU}_i \ \text{ for every zone } i \quad (\text{zone } t \text{ is a best choice for the fishers}) \\
& c_1 + c_2 + c_3 = 1, \qquad 0 \le c_i \le 1
\end{aligned}
$$

Then it keeps the best of the three plans. For the trust's payoffs the code uses the mirror image of the fishers': it loses $G_i$ if a zone is fished unprotected and gains 4 when it catches a crew. A game where one side's gain is exactly the other's loss is called **zero-sum**. The output:

```
hand solution: sum G/(G+4)=1.5000, sum 1/(G+4)=0.3750, U=1.3333, coverage=[0.556 0.333 0.111]
multiple LPs: coverage=[0.556 0.333 0.111]  defender payoff=-1.3333  fishers' payoff by zone=[1.333 1.333 1.333]
minimax LP  : coverage=[0.556 0.333 0.111]  fishers' best payoff U=1.3333
```

The solver agrees with the hand calculation. The last line shows a shortcut that works for zero-sum games: a single LP that directly **minimizes the fishers' best payoff** $U$:

$$
\text{minimize } U \quad \text{subject to} \quad G_i - c_i\,(G_i + P) \le U \ \text{ for every zone}, \qquad \sum_i c_i = \text{boats' zone-visits}, \qquad 0 \le c_i \le 1
$$

The multiple-LPs method is the one to keep when the trust's payoffs are **not** the mirror image of the fishers', for example if the trust cares about reef damage rather than catch value. One honest caution even in this example: the fishers are indifferent, so in fish terms the trust loses $(1 - c_i)\,G_i$, which is 3.556 if they pick the North reef, 2.667 for the Central bank and 1.778 for the South bay. The equilibrium guarantees the fishers' side of the ledger; which zone they actually pick still matters to the fish.

---

## Scaling Up – 40 Zones, 2 Boats, One Paper Schedule

### Coverage for the whole area

With 40 zones and 6 zone-visits a day, the coverages must add up to 6, and each must stay between 0 and 1 (a zone can't be visited "more than certainly"). The code gives each zone a made-up value between 1.1 and 9.4 (mean 5.37), with the northern reef and the five far zones among the richest, and solves the minimax LP:

```
equilibrium: fishers' best payoff U=4.207; zones with coverage > 0: 26; sum of coverage=6.00;
highest coverage=0.388 (zone 1)
zones never patrolled have value <= 4.0; lowest-value covered zone has value 4.3
    zone  0: value=8.3 coverage=0.333
    zone  3: value=8.0 coverage=0.316
    zone 22: value=6.0 coverage=0.179
    zone 31: value=6.3 coverage=0.203
    zone 12: value=3.6 coverage=0.000
```

The same indifference logic as the toy example, at scale. The 26 covered zones all pay the fishers 4.207; check zone 22: $(1 - 0.179) \times 6.0 - 0.179 \times 4 = 4.21$. The 14 zones worth 4.0 or less get no coverage, because even unguarded they pay less than 4.207: they aren't worth defending until the richer zones are. Even the richest zone is patrolled less than 4 days in 10.

### Fuel, weather and learning

Real limits enter the LP as extra rules on $c_i$:

- **Fuel and distance.** If the boats can reach the five far zones at most 15% of days, set $c_i \le 0.15$ there. Those zones are worth 6.0 to 8.8, so the fishers' best payoff rises from **4.207 to 6.880**, and only 17 zones get coverage. The far zones become safe havens, and the LP puts a number on what a fuel budget increase would buy.
- **Weather.** On days when some zones are unsafe, re-solve with those zones fixed at 0 and the day's zone-visits reduced. The LP takes milliseconds.
- **Learning.** [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went) said to keep some patrols in low-information zones. Requiring $c_i \ge 0.03$ everywhere raises the fishers' best payoff from **4.207 to 4.396**: a modest price for data that stops the risk model from going blind.

Operational limits like these, especially boats needing connected routes rather than any 3 zones, are why deployed systems such as PROTECT and PAWS plan over whole patrol routes instead of single zones. The idea is the same; the LP gets bigger.

### From probabilities to a daily schedule: comb sampling

A captain can't patrol "zone 1 with probability 0.388." Each day needs exactly 6 different zones, chosen so that over many days each zone comes up with its coverage probability. **Systematic sampling**, which we'll call the **comb**, does this:

1. Lay the 40 coverage values end to end along a line. It is 6 units long.
2. Pick one random starting point $u$ between 0 and 1.
3. Place 6 teeth at $u, u+1, u+2, \dots, u+5$. Each tooth lands inside one zone's stretch. Those are today's zones.

A hand example with 5 zones, A to E, and 2 visits a day: coverages 0.6, 0.6, 0.4, 0.2, 0.2 add up to 2 and occupy the stretches 0–0.6 (A), 0.6–1.2 (B), 1.2–1.6 (C), 1.6–1.8 (D) and 1.8–2.0 (E). With $u = 0.35$, the teeth fall at 0.35 and 1.35: today's zones are A and C.

Because no zone's stretch is longer than 1, no zone can catch two teeth, so every day has exactly the right number of *different* zones. And because $u$ is uniform, a zone with a stretch of length $c_i$ is hit with probability exactly $c_i$. The code checks both:

```
comb sampling, first three days: [[1, 4, 7, 15, 27, 36], [2, 5, 9, 22, 31, 39], [0, 3, 6, 13, 25, 35]]
over 20,000 sampled days: every day had exactly 6 different zones; largest gap between how often
a zone was picked and its coverage=0.005
```

Then split the 6 zones between the boats, for example the 3 northernmost to Boat A and the rest to Boat B, and let each captain order their own route.

This is the "spreadsheet with random draws" from the [case's field pathway](../cases/03-marine-patrols.md): one random number per day and a cumulative-sum column.

### Keeping it secret, keeping it current

- **Issue only the day's zones, on the day.** The equilibrium assumes the fishers know the *probabilities*, not the draws. A weekly paper calendar that circulates hands them the draws, which turns the mixed strategy back into a pure one. Generate a month of days in advance if needed, but give each captain only that morning's zones.
- **Keep the probabilities confidential** and publish only that patrols are risk-based and randomized, as the case recommends.
- **Refit monthly.** When the SMART export arrives, recompute rates per hour ([From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went)), update the zone values, and re-solve. Fishers adapt in days; the plan must keep up.

---

## Code Implementation & Simulation

The full program is [`code/case3_security_game.py`](code/case3_security_game.py). It needs `numpy` and PuLP 3, which includes the free CBC solver:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case3_security_game.py
```

### The multiple-LPs method

```python
for t in range(n):
    prob = pulp.LpProblem(f"target_{t}", pulp.LpMaximize)
    c = [pulp.LpVariable(f"c{i}", lowBound=0, upBound=1) for i in range(n)]

    def att_eu(i):
        return c[i] * att_loss[i] + (1 - c[i]) * att_gain[i]

    prob += c[t] * def_gain[t] + (1 - c[t]) * def_loss[t]     # defender's payoff if zone t is hit
    prob += pulp.lpSum(c) == resources                       # all patrol capacity is used
    for i in range(n):
        prob += att_eu(t) >= att_eu(i)                       # zone t is a best response
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
```

The first `prob +=` line sets what to maximize; the later ones add rules. Each line reads like the formulas in [The Decision Engine](#the-decision-engine--the-stackelberg-equilibrium).

### The comb

```python
def comb_sample(coverage, rng):
    edges = np.concatenate([[0.0], np.cumsum(coverage)])
    k = int(round(edges[-1]))
    teeth = rng.random() + np.arange(k)
    return np.searchsorted(edges, teeth, side="right") - 1
```

`np.cumsum` builds the line of stretches; `np.searchsorted` finds which stretch each tooth lands in.

### Simulation: six policies, one year, fishers who watch

The code simulates 364 days. Each day 5 crews choose a zone, or to stay home. Each crew estimates the chance that each zone is patrolled today from what it saw at the jetty: half from how often the zone was patrolled in the last 28 days, half from how often it was patrolled on **the same weekday** over the last 4 weeks, so a weekly pattern gets noticed. Crews pick zones with higher expected payoff more often but not always (bounded rationality). A crew in a patrolled zone is caught; otherwise it takes the zone's value in fish. The policies:

- **No patrols:** a reference point.
- **Fixed rotation:** the same weekly schedule every week, 6 zones a day, every zone covered at least once a week.
- **Hotspot:** the 6 zones with the most recorded incidents (starting from the three-year logs in [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went)), refreshed every 30 days with new incidents.
- **Uniform random:** 6 zones drawn at random each day, all zones equally likely.
- **Weighted lottery:** the paper version. Each zone's chance is in proportion to its value (capped at certain), drawn each day with the comb or with numbered slips in a bag.
- **Game (randomized):** the coverage from [Scaling Up](#scaling-up--40-zones-2-boats-one-paper-schedule), drawn each day with the comb.

```
Simulation - one-year simulation, 5 crews a day, fishers who watch and adapt
  policy             fish taken  vs no patrols  crews caught  stayed home
  no patrols              16084          +0.0%             0            0
  fixed rotation          15756          -2.0%             0            0
  hotspot                 15087          -6.2%             0            0
  uniform random          13446         -16.4%           268            0
  weighted lottery        11698         -27.3%           418            0
  game (randomized)        9608         -40.3%           509            0
  (5 crews x 364 days = 1820 fishing trips per policy)
```

**Reading the results:**

- **Fixed rotation and hotspot patrols catch nobody.** The fishers learn the weekly pattern, or the fixed hotspot list, and fish elsewhere. Fish taken falls only 2% and 6%, because the patrols merely push the nets into the next-best zones.
- **The hotspot policy traps itself.** It never records an incident outside its 6 zones, because it never goes there, so its monthly refresh keeps choosing the same northern zones. This is the detection-bias loop from [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went), running live.
- **Randomizing alone helps.** Uniform random patrols catch 268 crews and cut fish taken by 16%.
- **Weighting by value helps more.** The weighted lottery catches 418 crews and cuts fish taken by 27%, about two-thirds of the game's cut, with no model at all.
- **Randomizing in the right proportions helps most.** The game strategy catches 509 crews and cuts fish taken by 40%, with the same 6 zone-visits a day.
- **Nobody stays home.** With a penalty of 4 against zones worth up to 9.4, fishing pays somewhere under every policy. The equilibrium payoff of 4.207 is still positive. The game strategy changes *where* and *how profitably* crews fish, not *whether* they do. A real deterrent would need a larger penalty or more boats, which is a policy conversation, not a modeling one.

A consistency check you can do by hand: under the game strategy the crews' average payoff per trip is $(9608 - 4 \times 509) / 1820 = 4.160$, close to the equilibrium value $U = 4.207$ from [Scaling Up](#scaling-up--40-zones-2-boats-one-paper-schedule). The theory predicted what the simulated fishers would get.

Three cautions. First, everything here is invented to teach the method: zone values, patrol logs and fisher behavior are illustrative, and real gains depend on real data. Second, the game strategy is given the true zone values; in the field they come from the estimates in [From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went), with their margins of error. Third, the simulated fishers only see the jetty. If schedules leak, or crews can track boats at sea, the advantage shrinks, which is why issuing only the day's zones matters.

### The simpler alternative: Goal Seek in a spreadsheet

For a game this simple, the full equilibrium does not need a solver. The hand method from [The Decision Engine](#the-decision-engine--the-stackelberg-equilibrium) scales to 40 zones in one spreadsheet column: put $U$ in one cell, compute each zone's coverage as $\max\bigl(0, (G_i - U)/(G_i + 4)\bigr)$, capped at 1, and use Excel's **Goal Seek** to choose $U$ so the column adds up to 6. The code does the same with bisection:

```
weighted lottery (chance in proportion to value): fishers' best payoff U=5.882 (game 4.207); zones with coverage > 0: 40
spreadsheet goal seek: U=4.207; largest gap from the LP coverage=0.0000
```

So there are two simpler options, and they are close in different ways:

- **The weighted lottery** needs only the zone values and a bag of slips. It keeps the most important property, unpredictability, and gets about two-thirds of the game's effect here. It falls short because it spreads patrols over every zone, including the 14 low-value zones the fishers never bother with, and so leaves the richest zones softer (the fishers' best option pays 5.88 instead of 4.21).
- **Goal Seek** gives exactly the game's plan, but only while three assumptions hold. Check them before relying on it: (1) the trust's loss is the fishers' gain (zero-sum), so it cares about catch value and not, say, reef damage that differs by zone; (2) one penalty applies everywhere; (3) any 6 zones can be patrolled on a day, with no routes linking them. Fuel caps and learning floors can be added as limits on each cell, then Goal Seek again. Once boats must follow connected routes, or payoffs differ between the sides, use the LP.

Both rest on the same thing the game does: zone values estimated from patrol logs corrected for where the boats went ([From Patrol Logs to Estimates](#from-patrol-logs-to-estimates--correcting-for-where-the-boats-went)). A simple rule fed with biased hotspot counts will fail the same way the hotspot policy did.

For the pilot, the [playbook](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) suggests alternating model-generated and usual schedules and comparing **nets found per patrol hour**. Expect that number to rise at first and then fall: as deterrence works, there is less to find.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Effort-corrected risk** | $\text{rate}_i = \dfrac{\text{incidents}_i}{\text{patrol hours}_i}$, divided by detection $d$ | Separates "where fishing is" from "where we looked" in the SMART data |
| **Margins of error** | $\text{rate} \pm 1.96\sqrt{k}/h$; zero incidents: upper limit $3/h$ | Shows which zones are poorly known and need patrols for learning |
| **Fishers' payoff** | $\text{EU}_i = (1 - c_i)\,G_i - c_i\,P$ | What a crew expects from each zone, given the coverage they've learned |
| **Equilibrium coverage** | Minimize $U$ s.t. $\text{EU}_i \le U$, $\sum_i c_i = 6$, $0 \le c_i \le 1$ | The randomized plan that leaves the fishers the worst best option; general payoffs use multiple LPs |
| **Field limits** | $c_i \le$ cap (fuel), $c_i = 0$ (weather), $c_i \ge$ floor (learning) | Keeps the plan feasible and keeps the data honest; the LP shows what each limit costs |
| **Daily schedule** | Comb: teeth at $u, u+1, \dots, u+5$ on the cumulative coverages | Exactly 6 different zones a day, each with the right long-run frequency |
| **Operations** | Issue only the day's zones; refit monthly | Keeps the daily draw secret and the plan current as fishers adapt |

### Where to go next

- **Fix the readiness gaps and run the pilot** described in the [case's follow-ups](../cases/03-marine-patrols.md#after-the-recommendation): export the SMART data, tabulate hours and incidents by zone and month, brief captains on why randomization matters, and run the generated schedule for one quarter alongside the existing plan.
- **Read** Fang, Stone and Tambe (2015), *When Security Games Go Green* (IJCAI), which covers illegal fishing directly, and then Tambe (2011), *Security and Game Theory*, for the deployed systems. Both are listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Code and tools to build on:** [PAWS-public](https://github.com/lily-x/PAWS-public), research code for poaching risk prediction and patrol planning, and [SMART](https://smartconservationtools.org), which the trust already uses. See the playbook's [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) for the skills a partner needs.
- **Other tutorials in this series:** [risk-based inspection for lead pipes](13-risk-based-inspection-lead-pipes.md), the closest neighbor, for hidden problems that don't move when you look; [adaptive experiments for SMS reminders](09-adaptive-experiments-sms-reminders.md) for learning which option works when nobody is evading you; [vehicle routing for food delivery](10-vehicle-routing-food-delivery.md) for when the hard part is the travel itself; [welfare optimization for borehole siting](02-welfare-optimization-borehole-siting.md), which covers linear and integer programs in more depth; [restless bandits for home visits](01-restless-bandits-chw-visits.md); [robust optimization for cyclone pre-positioning](04-robust-optimization-cyclone-prepositioning.md); [stable matching for apprenticeships](05-stable-matching-apprenticeships.md); and [when no model is needed](06-no-model-food-pantry.md).
