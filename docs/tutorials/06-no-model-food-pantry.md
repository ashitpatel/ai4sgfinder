# No-Model Masterclass: When Is an Optimization Model Not Worth Building?

*An in-depth walkthrough of how to decide, with basic statistics, that an allocation model would not pay for itself, and how to tell when that answer should change, built on [Case 6: A neighborhood food pantry that doesn't need a model](../cases/06-food-pantry-no-model.md).*

**You need:** proportions, probabilities, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** no optimization model; the nearest alternative would be [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting). **Code:** [`code/case6_no_model_check.py`](code/case6_no_model_check.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A volunteer-run food pantry serves about 150 registered households with weekly grocery boxes. A local foundation has offered to fund "an AI tool to allocate food more fairly." The pantry's own record: in 49 of the last 52 weeks there were enough boxes for everyone who came; in the other 3 weeks it ran short by about 10–20 boxes. Volunteers tick names on a paper sign-in sheet, there is one laptop, and volunteers change every few months.

The other tutorials in this series each build a model. This one does something just as useful and less common: it **measures whether a model could help at all**, finds that it couldn't, and writes down the conditions under which it would. The tools are the statistics you already know.

1. **[The Measurement Leap](#the-measurement-leap--from-we-need-ai-to-how-much-is-there-to-gain)** turns "we need AI to allocate fairly" into three questions you can answer with counts: how often is there a shortfall, how big is it, and what is the most any allocation method could gain?
2. **[The Core Bottleneck](#the-core-bottleneck--a-tiny-problem-a-fragile-tool-and-demand-you-cant-see)** names the real bottleneck: a tiny problem next to a costly, fragile tool, plus demand nobody has recorded.
3. **[From Sign-In Sheets to Estimates](#from-sign-in-sheets-to-estimates--rates-intervals-and-hidden-demand)** turns the pantry's records into estimates with honest margins of error, and shows why the textbook interval breaks down at small counts.
4. **[The Decision Engine](#the-decision-engine--the-value-of-a-model)** computes the **value of a model** by hand and checks the pantry's written shortfall rule against it.
5. **[Scaling Up](#scaling-up--knowing-when-the-answer-should-change)** makes the "when to revisit" triggers precise, so they separate real change from bad luck.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all in code and simulates the pantry under today's demand and under growth.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **before optimizing who gets the scarce thing, measure how often it is scarce and by how much. If the answer is "rarely, and by little," fix the supply and write down a fair rule.**

---

## The Measurement Leap – From "We Need AI" to "How Much Is There to Gain?"

### What an allocation model would do

An **allocation model** (or *optimization model*) is a program that, given a limited supply and a list of people who need it, picks who gets what so that some score is as high as possible: most people served, most need met, fairest split. [Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) in this project's taxonomy is the static version; the [Case 2 tutorial](02-welfare-optimization-borehole-siting.md) builds one for siting boreholes.

Every such model has the same weak point: **it can only rearrange what is there.** It doesn't create boxes. So the most it could ever achieve is to change *who* goes without in the weeks when someone has to go without. If there are few such weeks, and few boxes missing in them, there is little for it to do, however clever it is.

### Three measurable questions

"Allocate more fairly" can't be checked. These can:

1. **How often is there a shortfall?** A proportion: short weeks out of all weeks.
2. **How big is a shortfall?** A count of boxes, and that count as a share of all boxes handed out.
3. **What is the most any allocation method could gain?** An upper bound, built from 1 and 2, on how many boxes a perfect allocator could move to the households that need them most.

If question 3 has a small answer, no model is worth its cost. That is the whole argument; the rest of the tutorial makes each number honest.

### Mapping it to the pantry

| Allocation term | In this pantry |
|---|---|
| Resource | Weekly grocery boxes, used up and resupplied every week |
| Demand | Registered households who come in a given week (and anyone turned away, who isn't recorded yet) |
| Shortfall | Demand minus boxes in a week when demand is larger; 3 of the last 52 weeks, about 10–20 boxes each |
| Allocation rule | The written shortfall rule: in a short week, households with children under 5 or no other support get a full box first; everyone else gets a smaller box |
| Data | A paper sign-in sheet with ticked names; one laptop; volunteers who change every few months |

---

## The Core Bottleneck – A Tiny Problem, a Fragile Tool, and Demand You Can't See

### Problem size versus tool cost

Some problems are too small to be worth a machine. The pantry hands out about $150 \times 52 = 7{,}800$ boxes a year. [From Sign-In Sheets to Estimates](#from-sign-in-sheets-to-estimates--rates-intervals-and-hidden-demand) will show that the boxes missing in short weeks add up to a fraction of one percent of that.

A tool, on the other hand, has costs that don't shrink with the problem:

- **Upkeep.** A scoring tool needs current data about every household, typed in every week by someone.
- **Fragility.** With volunteers changing every few months, the tool will soon depend on one person who understands it, and stop working when they leave.
- **Trust.** Ranking households can feel like surveillance or means-testing to the people being ranked. That cost lands on the households the tool was meant to help.

The comparison in [The Decision Engine](#the-decision-engine--the-value-of-a-model) is simple: the most the tool could gain, against what it costs to keep running.

### Absence of evidence is not evidence of absence

There is one gap in the pantry's record, and it matters. "Enough boxes for everyone who came" counts only **households who came and signed in**. It says nothing about:

- households who were turned away at the door before signing,
- households who stopped coming because they expected the shelves to be bare,
- people in the neighborhood who never registered.

This is **hidden demand**: need that exists but leaves no trace in the data. A record of 49 good weeks out of 52 is *not* evidence that hidden demand is zero; the sign-in sheet simply can't see it. The fix isn't a model; it's a new column on the sheet. [From Sign-In Sheets to Estimates](#from-sign-in-sheets-to-estimates--rates-intervals-and-hidden-demand) shows how to turn three months of that column into an estimate.

---

## From Sign-In Sheets to Estimates – Rates, Intervals and Hidden Demand

### Step 1: How often is the pantry short?

Treat each week as a yes/no trial: short or not. The natural estimate of the weekly shortfall chance is the proportion

$$
\hat p = \frac{k}{n} = \frac{3}{52} = 0.0577,
$$

with a **standard error** (the typical size of the estimate's random error) of $\sqrt{\hat p(1-\hat p)/n} = 0.0323$.

A 95% **confidence interval** is a range built so that, over many repetitions of the same data collection, 95% of such ranges would contain the true rate. The textbook version, called the **Wald** or normal-approximation interval, is

$$
\hat p \pm 1.96\,\sqrt{\frac{\hat p(1-\hat p)}{n}} \;=\; 0.0577 \pm 0.0634 \;=\; (-0.0057,\ 0.1211).
$$

**The lower end is negative.** A rate below zero is impossible, so the interval is plainly wrong. The reason: the formula assumes the count of short weeks is spread out like a symmetric bell curve. With only 3 events, the true spread is lopsided: the count can't go below 0 but can easily go up to 6 or 8. A rough rule of thumb is that the normal approximation needs at least 5 to 10 events *and* 5 to 10 non-events; 3 events doesn't qualify.

### Step 2: Intervals that behave at small counts

Two better intervals fix this.

**The Wilson interval** reverses the question. Instead of starting from $\hat p$ and spreading out, it asks: *for which true rates $p$ would seeing $\hat p$ be unsurprising?* Solving that gives

$$
\frac{\hat p + \dfrac{z^2}{2n}}{1 + \dfrac{z^2}{n}} \;\pm\; \frac{z}{1 + \dfrac{z^2}{n}}\sqrt{\frac{\hat p(1-\hat p)}{n} + \frac{z^2}{4n^2}}, \qquad z = 1.96.
$$

The centre is pulled slightly toward one half, and the width never pushes past 0 or 1. With $n = 52$: $z^2 = 3.8416$, the centre is $(0.0577 + 0.0369)/1.0739 = 0.0881$, and the half-width is $1.825 \times \sqrt{0.0010455 + 0.0003552} = 0.0683$.

**The exact (Clopper–Pearson) interval** uses the binomial distribution directly. The **binomial distribution** gives the chance of exactly $k$ "yes" results in $n$ independent trials that each say yes with probability $p$:

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}.
$$

The lower end of the interval is the rate at which seeing 3 or more short weeks is just 2.5% likely; the upper end is the rate at which seeing 3 or fewer is just 2.5% likely. The code finds both by trial and error (bisection).

| Interval | 95% range for the weekly rate | In short weeks per year |
|---|---|---|
| Wald (normal approximation) | −0.0057 to 0.1211 | −0.3 to 6.3 (impossible lower end) |
| Wilson | 0.0198 to 0.1564 | 1.0 to 8.1 |
| Exact (Clopper–Pearson) | 0.0121 to 0.1595 | 0.6 to 8.3 |

The honest summary: **the pantry is probably short somewhere between 1 and 8 weeks a year.** One year of records can't pin it down more tightly than that, and the decision in [The Decision Engine](#the-decision-engine--the-value-of-a-model) has to hold across that whole range.

### Step 3: How big is a shortfall?

The case gives "about 10–20 boxes" per short week. Multiply by 3 short weeks and compare with the $7{,}800$ boxes handed out in a year:

| Boxes short per short week | Boxes short per year | Share of all boxes |
|---|---|---|
| 10 | 30 | 0.38% |
| 15 (middle) | 45 | 0.58% |
| 20 | 60 | 0.77% |

Now be pessimistic on both counts at once: take the Wilson upper rate (0.1564, about 8 short weeks a year) and the largest shortfall (20 boxes). That gives $0.1564 \times 52 \times 20 = 163$ boxes a year, **2.09%** of all boxes. Even the worst plausible reading of the record leaves 98% of boxes unaffected by any allocation decision.

### Step 4: Is it an end-of-month problem?

The pantry says demand rises at the end of the month, and its note to the foundation describes the 3 short weeks as an end-of-month supply problem. Can a coincidence explain that?

A year has 12 end-of-month weeks out of 52. If short weeks fell at random, the chance that all 3 land in end-of-month weeks is the number of ways to pick 3 of the 12 end-of-month weeks over the number of ways to pick any 3 of the 52 weeks:

$$
\frac{\binom{12}{3}}{\binom{52}{3}} = \frac{220}{22{,}100} = 0.0100.
$$

About a 1% chance: the end-of-month pattern is very unlikely to be luck. Splitting the rate by week type:

| Week type | Short | Rate | Wilson 95% interval |
|---|---|---|---|
| End-of-month | 3 of 12 | 0.250 | 0.089 to 0.532 |
| Other | 0 of 40 | 0.000 | 0.000 to 0.088 |

This tells you what kind of problem it is. **The shortfall is predictable**: it comes at a known time of the month. A predictable shortfall calls for a standing order from the supplier for those weeks, not for a smarter way to split too few boxes.

### Step 5: Estimating hidden demand

To measure hidden demand, add a column to the sign-in sheet: *households turned away or told to come back*. After 3 months (13 weeks), count them. Counts of rare events over time follow the **Poisson distribution**, which describes how many times something happens in a fixed period when each occurrence is independent and the average rate is steady. From it come exact intervals for the weekly rate:

| Turn-aways recorded in 13 weeks | Weekly rate | 95% interval | Up to, per year |
|---|---|---|---|
| 0 | 0.00 | 0.00 to 0.23 (one-sided) | 12 households |
| 13 (illustrative) | 1.00 | 0.53 to 1.71 | 89 households |

The first row is worth remembering. Zero events in 13 weeks still allows a rate up to $-\ln(0.05)/13 = 2.996/13 = 0.23$ a week. This is the "rule of three": after $n$ periods with no events, the 95% upper bound is about $3/n$. **Seeing nothing for 3 months narrows hidden demand down; it doesn't prove it is zero.**

The second row is an illustrative scenario. One turn-away a week would be up to 89 households a year whose need never appeared on the sheet. That changes how many boxes to order, which is still a supply question. It becomes an allocation question only if supply can't grow to meet it.

---

## The Decision Engine – The Value of a Model

### The question it answers

The "engine" here is a short calculation called the **value of a model**: the most a perfect allocation method could improve outcomes, compared with what the pantry would do without it. If that value is smaller than the tool's cost and risk, don't build it.

It needs two numbers: an upper bound on the gain (Step A) and the cost of the tool (Step B). Then Step C checks that the pantry's simple rule is already close to the ceiling.

### Step-by-step concrete example

**Step A: The most any allocation method could gain.** In a short week with $D$ households and $S$ boxes, every method hands out the same $S$ boxes. All a method can change is *who* absorbs the $D - S$ missing boxes. So the gain from the best possible method, compared with the worst, is at most the number of boxes short:

$$
\text{maximum gain per year} \;\le\; (\text{short weeks per year}) \times (\text{boxes short per short week}).
$$

From the estimates in [From Sign-In Sheets to Estimates](#from-sign-in-sheets-to-estimates--rates-intervals-and-hidden-demand): $3 \times 15 = 45$ boxes a year, or **0.58%** of all boxes. In the pessimistic reading, 163 boxes, or 2.09%. That is the ceiling for *any* method, with perfect information.

**Step B: Compare with the cost of a tool.** The pantry hasn't priced a tool, so here is one illustrative cost that doesn't need prices. Keeping a household scoring tool current takes, say, one minute of data entry per household per week: $150 \times 1 \times 52 / 60 = 130$ volunteer-hours a year. That is time spent to rearrange, at most, 45 boxes, and it rests on one laptop and whichever volunteer understands the tool.

Compare the alternative the case recommends: a standing end-of-month top-up order. Shortfalls have been at most about 20 boxes, so an extra $20 \times 12 = 240$ boxes a year at month-end would have covered every short week on record. A tool **moves** the shortage onto different households; a buffer **removes** it. The foundation's money buys more good as storage and supply.

**Step C: Check the written rule.** Take one illustrative short week. 140 households come; there are 125 boxes; the pantry is 15 short. Say 30% of households have children under 5 or no other support (an illustrative share): that's 42 priority households.

- **No rule (first come, first served).** The last 15 arrivals go home with nothing. Arrival order has nothing to do with need, so on average 30% of them are priority households: $15 \times 0.30 = 4.5$ priority households go without.
- **The written rule.** The 42 priority households get full boxes. The other 98 share the remaining $125 - 42 = 83$ boxes: $83 / 98 = 0.847$ of a box each. Nobody goes home empty-handed, and no priority household goes without.

Over a year at 3 short weeks, the rule protects about $3 \times 4.5 = 13.5$ priority households who would otherwise have gone without. Averaged over all weeks, the expected number of households short in a week is $0.0577 \times 15 = 0.87$.

Now the key point. **A perfect allocator, one that knew every household's situation exactly, couldn't do better than the rule on this measure**, because the rule already gives every priority household a full box whenever there are enough boxes for them. The only thing left for a model to improve is the rule's mistakes: priority households the volunteer at the table doesn't recognize. [Code Implementation & Simulation](#code-implementation--simulation) sizes that gap, and it is tiny. Closing it would mean collecting more personal information about every household, which is exactly the surveillance cost from [The Core Bottleneck](#the-core-bottleneck--a-tiny-problem-a-fragile-tool-and-demand-you-cant-see).

### The decision

| Question | Answer from the data |
|---|---|
| How often short? | 3 of 52 weeks; 95% interval about 1 to 8 weeks a year |
| How big? | About 45 boxes a year (0.58%); at most about 163 (2.09%) |
| Predictable? | Yes: all 3 at month-end; about a 1% chance of that by luck |
| Most a model could gain over the written rule? | Close to zero; the rule already meets the ceiling for priority households |
| Cheapest fix | A month-end supplier top-up and storage to hold it |

**No model.** Write down the rule, fix the supply, and start recording turn-aways.

---

## Scaling Up – Knowing When the Answer Should Change

A "no" is only responsible if it says when it becomes a "maybe." The [case's follow-ups](../cases/06-food-pantry-no-model.md#after-the-recommendation) set three triggers for revisiting:

1. the pantry runs short in **more than one week a month for three months running**, or
2. recorded turn-aways show hidden demand, or
3. the pantry starts sharing supply with other pantries.

### Making trigger 1 precise: how unusual is it today?

A good trigger works like a **control chart**, the tool factories use to watch a process: it stays quiet while things vary by chance and speaks up when the process has truly changed. Raising the alarm when nothing has changed is a **false alarm**; the chance of raising it when something *has* changed is the trigger's **detection rate**.

At today's rate $p = 3/52 = 0.0577$, and with about 4 weeks per month, the number of short weeks in a month follows a binomial distribution with $n = 4$:

$$
\begin{aligned}
P(0 \text{ short}) &= (1-p)^4 = 0.7884 \\
P(1 \text{ short}) &= 4p(1-p)^3 = 0.1931 \\
P(\text{more than 1}) &= 1 - 0.7884 - 0.1931 = 0.0185
\end{aligned}
$$

If months are independent, three such months in a row has probability $0.0185^3 = 6.30 \times 10^{-6}$: about six in a million. Over a whole year, allowing the run to start in any month, the chance it fires is about 0.0001. **At today's rate, the trigger essentially never fires by chance.**

### What it takes to set it off

The same formula for higher weekly rates shows how much change the trigger needs before it notices:

| Weekly short rate | Short weeks a year (about) | P(month has >1 short week) | P(fires within a year) |
|---|---|---|---|
| 0.0577 (today) | 3 | 0.0185 | 0.0001 |
| 0.10 | 5 | 0.0523 | 0.0021 |
| 0.15 | 8 | 0.1095 | 0.0174 |
| 0.25 | 13 | 0.2617 | 0.1770 |
| 0.35 | 18 | 0.4370 | 0.5345 |
| 0.50 | 26 | 0.6875 | 0.9329 |

(The "fires within a year" column uses a 4-4-5 calendar, 12 months of 4, 4 and 5 weeks, so it adds up to 52 weeks.)

The case's trigger is **deliberately strict**: it ignores a bad month or two and fires reliably only once shortages are a regular, every-month event. It will almost never send the pantry chasing noise, but it is slow to notice moderate change. At 13 short weeks a year, four times today's rate, it fires within the year only 18% of the time.

### A more sensitive companion check (optional)

If the pantry wants earlier warning, a simple alternative is: **3 or more short weeks in any 13-week quarter**. At today's rate that happens in a given quarter with probability 0.0355, and in at least one quarter of the year with probability 0.1347. That's a false alarm about one year in seven, the price of sensitivity. In return, at 13 short weeks a year it fires within the year 98.8% of the time. Neither check is "right"; it's a choice between fewer false alarms and earlier warning, and the pantry can watch both on the same tally sheet.

The binomial calculation treats every week alike. The pantry's short weeks actually cluster at month-end, which makes the case's trigger even quieter under today's conditions: it needs a short week *outside* the month-end spike. [Code Implementation & Simulation](#code-implementation--simulation) simulates that.

### Triggers 2 and 3

**Turn-aways** (trigger 2) are measured as in [From Sign-In Sheets to Estimates](#from-sign-in-sheets-to-estimates--rates-intervals-and-hidden-demand), Step 5. If 3 months of records give an interval that sits clearly above zero, the pantry has more demand than its sign-in sheet shows. The first response is still to order more; allocation only matters if supply can't follow.

**Joining a regional network** (trigger 3) is where the answer genuinely changes. Once several pantries share one supply, the question becomes how to divide loads *across sites* with different needs. That is a real allocation problem:

- If a central coordinator divides supply by need, it is [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting), the welfare optimization built in the [Case 2 tutorial](02-welfare-optimization-borehole-siting.md).
- If donated loads arrive over time and each pantry says, or bids for, what it wants, it becomes an online allocation question, [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists). The best-known example in food is Feeding America's **Choice System**, which lets food banks bid for donated loads using an internal currency. Prendergast (2022, *Journal of Political Economy*) describes it and finds it improved allocation across food banks. That works at the scale of a national network of food banks, not a single pantry.

---

## Code Implementation & Simulation

The full program is [`code/case6_no_model_check.py`](code/case6_no_model_check.py). It needs only `numpy` and the standard library:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case6_no_model_check.py
```

### The Wilson interval

```python
def wilson_interval(k, n, z=Z):
    """Wilson score interval: the set of p for which k/n is not surprising."""
    p = k / n
    centre = (p + z**2 / (2 * n)) / (1 + z**2 / n)
    half = (z / (1 + z**2 / n)) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return centre - half, centre + half
```

### The trigger's monthly probability

```python
def p_month_flag(p, weeks=4):
    """Chance a month has MORE THAN ONE short week, if each week is short with chance p."""
    return 1 - (1 - p)**weeks - weeks * p * (1 - p)**(weeks - 1)
```

### The simulated pantry

The code simulates a pantry that matches the record. All of these settings are illustrative:

- 150 registered households, 30% of them priority households.
- Each household comes with probability 0.78 in an ordinary week and 0.95 in the end-of-month week.
- The pantry expects 150 boxes; in any week, with probability 0.25, the delivery comes up short by 18 to 26 boxes.

That combination produces about 3 short weeks a year, nearly all at month-end, short by about 14 boxes: close to the real record. The code then raises demand by 10% and 20% (165 and 180 households, supply unchanged) and runs 10,000 simulated years of each, with a fixed random seed so the output is the same every run.

In each short week it compares three ways to hand out boxes:

```python
# No rule: first come, first served; the last arrivals go home with nothing.
no_rule_priority = rng.hypergeometric(dp, d - dp, turned_away)
# Written rule, as applied: recognized priority households get full boxes first.
recognized = rng.binomial(dp, RECOGNIZED)
full = np.minimum(recognized, s)
smaller_box = (s - full) / (d - full)
rule_missed = (dp - full) * (1 - smaller_box)
# Perfect allocator: knows every household's status, but can't create boxes.
perfect_missed = np.maximum(0, dp - s)
```

The written rule is given a realistic flaw: the volunteer at the table recognizes only 90% of priority households (illustrative). The others get the smaller box like everyone else.

### Output

```
Simulation - simulated pantry (illustrative), 10,000 years each
  today (150 households)        short weeks/yr  3.20  (end-of-month share 0.94)  mean shortfall  13.8 boxes  case trigger fires 0.0000  quarter check fires 0.0878
  demand +10% (165 households)  short weeks/yr 17.00  (end-of-month share 0.70)  mean shortfall  10.3 boxes  case trigger fires 0.2975  quarter check fires 1.0000
  demand +20% (180 households)  short weeks/yr 22.63  (end-of-month share 0.53)  mean shortfall  19.7 boxes  case trigger fires 0.8370  quarter check fires 1.0000

Simulation - who bears a short week? (today, per year, illustrative)
  short weeks 3.20, boxes short 44.0
  households sent home with nothing: no rule 44.0 (of them priority 13.23), written rule 0
  average smaller box under the rule, in short weeks: 0.868 of a full box
  unrecognized priority households given a smaller box: 13.67
  boxes priority households went without: no rule 13.23, written rule 1.80, perfect allocator 0.00
  most a perfect allocator could add: over the written rule 1.80 boxes/year, over no rule 13.23
```

### Reading the results

**False alarms.** In 10,000 simulated years at today's demand, the case's trigger never fired. That's even quieter than the binomial estimate (0.0001), because today's short weeks are almost all at month-end (94% in the simulation), and the trigger needs two short weeks in the same month. The quarterly companion check fired falsely in 8.8% of years.

**Detection.** With 10% more households and the same supply, short weeks jump from about 3 to 17 a year, and shortages spread beyond month-end (70% now at month-end). The case's trigger fires in 30% of years; at 20% growth, in 84%. The quarterly check catches both every time. The jump from 3 to 17 short weeks shows why growth needs watching: with supply fixed, a modest rise in demand pushes ordinary weeks over the edge too.

**Allocation.** Under today's demand, about 44 boxes a year are short, matching the hand estimate of 45. With no rule, 44 households a year go home with nothing, 13.23 of them priority households. With the written rule, nobody goes home empty; others get 0.868 of a box in short weeks, and the only priority households who lose out are the ones the volunteer didn't recognize, who together go without 1.80 boxes a year. A perfect allocator would get that to zero. **So the most any model could add over a one-card rule is under 2 boxes a year.**

Two cautions. The turnout rates, disruption sizes and the 30% priority share are invented to match the pantry's record, not measured; the conclusions rest on the record itself (3 short weeks, 10–20 boxes), which [From Sign-In Sheets to Estimates](#from-sign-in-sheets-to-estimates--rates-intervals-and-hidden-demand) analyzed without the simulation. And the simulation can't see hidden demand: if turn-away records show it, rerun the numbers with the higher demand.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Shortfall rate** | $\hat p = k/n = 3/52$ | Turns the sign-in record into a weekly chance of running short |
| **Small-count interval** | Wilson or exact binomial, not $\hat p \pm 1.96\,\text{SE}$ | Gives an honest range (about 1 to 8 short weeks a year) where the textbook formula goes negative |
| **Shortfall size** | weeks × boxes ÷ $(150 \times 52)$ | Puts the problem in proportion: about 0.58% of boxes, 2.09% at worst |
| **Pattern check** | $\binom{12}{3}/\binom{52}{3} = 0.0100$ | Shows the shortfall is a predictable month-end supply problem |
| **Hidden demand** | Poisson interval; 0 events in $n$ weeks → rate $\le 3/n$ | Turns 3 months of turn-away records into a bound on unseen need |
| **Value of a model** | max gain $\le$ short weeks × boxes short | The ceiling for any allocation method; compare with a tool's upkeep and risk |
| **Shortfall rule** | priority first, others share $(S - P)/(D - P)$ | Reaches that ceiling with one laminated card |
| **Revisit trigger** | $P(X \ge 2 \mid n=4, p)^3$ | A control chart: about six in a million by chance today, fires once shortages become routine |

### Where to go next

- **Use the rule and start the tally**, as in the [case's follow-ups](../cases/06-food-pantry-no-model.md#after-the-recommendation): the shortfall rule on a card, a monthly count of short weeks and turn-aways, and the note to the foundation proposing storage and a month-end supplier order.
- **If the pantry joins a regional network**, read Prendergast (2022) on Feeding America's Choice System, listed in the [taxonomy's verified references](../../prompt/knowledge/taxonomy.md#3-deployment-evidence), and see the [implementation playbook](../../prompt/knowledge/playbook.md#no-model-needed) for what to track.
- **See what a model looks like when one is warranted**: [restless bandits](01-restless-bandits-chw-visits.md), [welfare optimization](02-welfare-optimization-borehole-siting.md), [security games](03-security-games-marine-patrols.md), [robust optimization](04-robust-optimization-cyclone-prepositioning.md) and [stable matching](05-stable-matching-apprenticeships.md).
