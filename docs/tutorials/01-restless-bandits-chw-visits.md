# Restless Bandits Masterclass: Who Gets This Week's Home Visit

*An in-depth walkthrough of restless multi-armed bandits, the Whittle index and optimistic learning, built on [Case 1: Community health worker visits for hypertension](../cases/01-chw-hypertension-visits.md).*

**You need:** proportions, probabilities, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution). **Code:** [`code/case1_restless_bandits.py`](code/case1_restless_bandits.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A county health NGO has 1,200 enrolled adults with high blood pressure and 10 community health workers (CHWs) who can make 80 home visits a week between them. Every Monday someone has to decide **which 80 patients get a visit**.

The usual answers fail in instructive ways. A rotation visits everyone in turn, so a patient who is doing fine gets the same attention as one who has just stopped taking their pills. A risk score sends visits to the patients most likely to lapse, but some of those patients won't change no matter what, so the visits are spent where they can't help.

This tutorial builds the alternative step by step:

1. **[The Restless Leap](#the-restless-leap--from-a-ranked-list-to-a-moving-system)** describes each patient as a small chance process that keeps moving whether or not you visit: a *restless bandit*.
2. **[The Core Bottleneck](#the-core-bottleneck--unknown-patient-specific-odds)** names what we don't know: how much a visit changes each patient's chances.
3. **[From Records to Estimates](#from-records-to-estimates--plausible-ranges-then-optimism)** turns the CHWs' weekly records into estimates, with honest margins of error, and shows how to be *optimistic* about what we haven't tested.
4. **[The Decision Engine](#the-decision-engine--the-whittle-index)** computes a single priority score per patient, the **Whittle index**, and works one through by hand.
5. **[Scaling Up](#scaling-up--real-limits-on-who-can-be-visited)** handles the real-world limits: 80 visits in total, 8 per CHW, and a promise that nobody is ignored.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all in code and compares it with rotation and a risk score.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **visit where a visit changes the most, now and in the weeks that follow.**

---

## The Restless Leap – From a Ranked List to a Moving System

### What a bandit is

The name comes from slot machines, "one-armed bandits." Picture a row of machines, each paying out with an unknown probability. You have a limited number of pulls. A **multi-armed bandit** problem asks which arms to pull to win the most.

In the classic version, an arm you don't pull stays exactly as it was. That's a poor description of people.

### What makes it restless

A **restless** bandit adds three rules that match how patients behave:

1. **Every arm has a state.** Each patient, each week, is in one of a few conditions. Here there are two:
   - **State 0, lapsing:** missed pills at this week's pill count.
   - **State 1, adhering:** took their pills.
2. **Every arm moves every week, visited or not.** A patient who is adhering this week may slip next week even if nobody does anything. Not visiting does not freeze them.
3. **A visit changes the odds of moving.** A visited patient moves according to one set of probabilities (the **active** track); an unvisited one follows another (the **passive** track).

### Mapping it to the program

| Bandit term | In this program |
|---|---|
| Arm | One enrolled patient (1,200 arms) |
| State | Lapsing (0) or adhering (1), read from the weekly pill count |
| Action | Visit (active) or no visit (passive); every patient still gets the SMS |
| Round | One week |
| Budget | 80 visits per week |
| Reward | 1 point for every patient adhering each week |

The goal is to collect as many reward points as possible over the coming weeks: as many patient-weeks of adherence as the 80 visits can buy.

### Why this and not a neighboring class

In the AI4SG Finder interview this problem lands in the *Repeated decisions that learn* family, and one [narrowing answer](../cases/01-chw-hypertension-visits.md#why-class-1-dynamic-state-evolution) settles the class. [Class 8: Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) is for uncertainty about *which of several options works*, when each option's payoff stays put. Here there is one option, a home visit, and the uncertainty is *each patient's state, which drifts week to week*. Two other classes come close. [Class 7: Effect-Based Targeting](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) also asks who a visit would change, but it learns that from a randomized pilot (this program has none) and suits a program offered once, not a choice remade every Monday. The risk score from the overview belongs to [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), which finds hidden problems; the goal here is to change behavior, and the patients most likely to lapse are not always the ones a visit helps.

---

## The Core Bottleneck – Unknown, Patient-Specific Odds

Each patient's behavior is described by four probabilities: the chance of **adhering next week**, for each combination of this week's state and this week's action.

$$
P^{\text{passive}} = \begin{pmatrix} P(0 \to 0) & P(0 \to 1) \\ P(1 \to 0) & P(1 \to 1) \end{pmatrix}
\qquad
P^{\text{active}} = \text{same, if visited}
$$

Read $P(0 \to 1)$ as "the probability that a patient who is lapsing this week is adhering next week." Each row adds up to 1, so we only need the right-hand column: two numbers for passive, two for active.

### Three kinds of patient

Patients differ. To keep the tutorial concrete, the code uses three made-up groups:

| Group | $P(0\to1)$ no visit | $P(0\to1)$ visit | $P(1\to1)$ no visit | $P(1\to1)$ visit | In words |
|---|---|---|---|---|---|
| Steady | 0.30 | 0.40 | 0.95 | 0.97 | Mostly fine on their own; a visit adds a little |
| Responsive | 0.10 | 0.60 | 0.70 | 0.95 | Slip often, but a visit makes a big difference |
| Hard-to-move | 0.05 | 0.08 | 0.50 | 0.55 | Struggle, and a visit barely changes that |

Look at the hard-to-move group. Its lapsing patients have the **worst** odds of recovering (0.05), so a risk score puts them first. But a visit lifts their odds only from 0.05 to 0.08. The responsive group's lapsing patients look less alarming (0.10), yet a visit lifts them from 0.10 to 0.60. **What matters is the change a visit makes, not how bad things look.** A risk score can't see that difference.

### Two complications

1. **We don't know these probabilities.** They have to be estimated from the CHWs' records, and for some combinations, especially "lapsing and visited," there may be very little data. [From Records to Estimates](#from-records-to-estimates--plausible-ranges-then-optimism) deals with this.
2. **They drift.** Researchers call this the *novelty decay effect*: a patient visited week after week may stop responding to the visits. [From Records to Estimates](#from-records-to-estimates--plausible-ranges-then-optimism) also shows how to let old records fade.

---

## From Records to Estimates – Plausible Ranges, Then Optimism

### Step 1: Count transitions in a ledger

Every week, each patient contributes one record: *(state this week, visited or not, state next week)*. Tally them per group. For lapsing patients in the responsive group, after 39 weeks the ledger might show:

| Action | Lapsing patient-weeks ($n$) | Recovered next week ($k$) |
|---|---|---|
| No visit | 1,500 | 150 |
| Visit | 20 | 12 |

The natural estimate is the proportion $k/n$. The code adds half a success and half a failure first, which keeps the estimate sensible when $n$ is tiny or zero:

$$
\hat{p} = \frac{k + 0.5}{n + 1}
$$

That gives $\hat p = 0.100$ without a visit and $\hat p = 0.595$ with one.

**Why group patients?** One patient contributes at most 39 records over 9 months, and only a handful of those are lapsing weeks. Pooling similar patients into groups gives enough records to estimate anything at all. In practice groups are formed from patients' adherence histories.

### Step 2: Put a margin of error on each estimate

From basic statistics, a 95% confidence interval for a proportion is roughly

$$
\hat p \pm 1.96 \sqrt{\frac{\hat p (1-\hat p)}{n}}
$$

| Action | $\hat p$ | 95% interval | Width |
|---|---|---|---|
| No visit | 0.100 | 0.085 to 0.115 | narrow: 1,500 records |
| Visit | 0.595 | 0.380 to 0.810 | wide: only 20 records |

This is the typical situation in the field. **Visits are scarce, so the evidence about what visits do is thin**, and it is precisely what we most need to know.

### Step 3: Be optimistic about what you haven't tested

Suppose some group has only been visited a few times. If we trust the small sample, we might write off visits for that group after one unlucky week and never visit again, so we never learn we were wrong.

The fix is called **optimism in the face of uncertainty**: when deciding, use the *upper end* of a plausible range rather than the middle. Groups with little evidence get the benefit of the doubt, get tried, and their range narrows. Groups with lots of evidence are judged on it. This is the core of the **UCWhittle** method (Upper-Confidence Whittle) from Wang, Xu, Taneja and Tambe, *Optimistic Whittle Index Policy: Online Learning for Restless Bandits*, AAAI 2023.

UCWhittle uses a slightly different margin, which grows slowly with the number of weeks $t$ the program has run, so the program keeps checking its assumptions:

$$
\text{radius} = \sqrt{\frac{2 \ln t}{n}}, \qquad \text{optimistic } p = \min\left(1,\ \hat p + \text{radius}\right)
$$

At $t = 39$ weeks:

| Action | $\hat p$ | Radius | Optimistic $p$ |
|---|---|---|---|
| No visit | 0.100 | 0.070 | 0.170 |
| Visit | 0.595 | 0.591 | 1.000 (capped) |

With only 20 records, the optimistic estimate for visiting jumps to its maximum. That isn't a belief that visits always work; it's a decision to keep testing until the data say otherwise. As visits accumulate, $n$ grows, the radius shrinks like $1/\sqrt{n}$, and the optimistic value settles near the truth.

### Step 4: Let old records fade

If patients' responses drift, last year's records shouldn't count as much as last week's. Multiply every count in the ledger by a **forgetting factor** $\alpha$ each week, then add the new records:

$$
N_{t+1} = \alpha \cdot N_t + \text{(new records this week)}
$$

With $\alpha = 0.9$, a record's weight is 0.90 after one week, 0.35 after 10 weeks and 0.065 after 26 weeks. Over 39 weeks the weights add up to about **9.8**: the ledger behaves like roughly the last 10 weeks of data. That is the trade-off: a faster forgetting factor reacts to change sooner but leaves fewer effective records and wider margins.

The same idea handles *visit fatigue*: track how many weeks in a row a patient has been visited, and if that passes a threshold, use a lower estimate for the next visit.

---

## The Decision Engine – The Whittle Index

### The question it answers

We want one number per patient that says how urgently they need a visit this week. Then the rule is simple: **visit the 80 patients with the highest numbers.**

The statistician Peter Whittle (1988) found a principled way to define that number. Imagine we *paid* ourselves a small subsidy, $m$ points, every time we chose **not** to visit a patient. If $m$ is tiny, visiting still looks better. If $m$ is large, leaving the patient alone looks better. Somewhere in between is the subsidy at which we're exactly indifferent. That break-even subsidy is the patient's **Whittle index**:

$$
W(\text{state}) = \text{the subsidy } m \text{ at which "visit" and "don't visit" are equally good}
$$

A patient with a high index needs a large payment before we'd skip them: they benefit a lot from a visit. A patient with a low index is cheap to skip.

### Long-run value: counting future weeks

"Equally good" has to include the future, because a visit this week changes next week's state, which changes the week after. We count future reward but **discount** it: a point next week is worth $\beta = 0.9$ of a point this week, a point in two weeks $0.9^2 = 0.81$, and so on. The **value** $V(s)$ of a state is the total discounted reward expected from it.

For a patient who is **never visited**, the values satisfy two equations, one per state. Each says: *value now = this week's reward + 0.9 × expected value next week.*

$$
\begin{aligned}
V_0 &= 0 + 0.9\,\big(P(0\to1)\,V_1 + P(0\to0)\,V_0\big) \\
V_1 &= 1 + 0.9\,\big(P(1\to1)\,V_1 + P(1\to0)\,V_0\big)
\end{aligned}
$$

### Step-by-step concrete example: a lapsing patient in the responsive group

**Step A: Value of being left alone.** Using the responsive group's passive odds, $P(0\to1) = 0.10$ and $P(1\to1) = 0.70$:

$$
\begin{aligned}
V_0 &= 0.9\,(0.10\,V_1 + 0.90\,V_0) \;\Rightarrow\; V_0 = 0.4737\,V_1 \\
V_1 &= 1 + 0.9\,(0.70\,V_1 + 0.30\,V_0) \;\Rightarrow\; V_1 = 4.130,\quad V_0 = 1.957
\end{aligned}
$$

So an adhering patient is worth $4.130 - 1.957 = \mathbf{2.174}$ more points than a lapsing one over the long run.

**Step B: Compare "visit now" with "don't visit."** A visit this week changes only next week's odds of adhering, from 0.10 to 0.60. After that, assume the patient is left alone again:

$$
\begin{aligned}
\text{no visit} &= 0 + 0.9\,(0.10 \times 4.130 + 0.90 \times 1.957) = 1.957 \\
\text{visit} &= 0 + 0.9\,(0.60 \times 4.130 + 0.40 \times 1.957) = 2.935
\end{aligned}
$$

**Step C: The difference is the priority.**

$$
2.935 - 1.957 = 0.9 \times (0.60 - 0.10) \times 2.174 = \mathbf{0.978}
$$

In words: **discount × extra chance of adhering × how much adhering is worth.** For this patient the hand calculation equals the exact Whittle index the code finds by searching for the break-even subsidy.

### The index for every group and state

| Group | State | Whittle index | Hand calculation |
|---|---|---|---|
| Responsive | Lapsing | **0.978** | 0.978 |
| Responsive | Adhering | 0.328 | 0.489 |
| Steady | Lapsing | 0.217 | 0.217 |
| Hard-to-move | Adhering | 0.076 | 0.076 |
| Hard-to-move | Lapsing | 0.047 | 0.045 |
| Steady | Adhering | 0.037 | 0.043 |

Read down the list and the policy writes itself: lapsing responsive patients first, then adhering responsive patients (a visit keeps them from slipping), then lapsing steady patients. **Hard-to-move lapsing patients, the top of any risk list, come near the bottom.** That isn't giving up on them; it's recognizing that home visits aren't what they need, which is a finding worth taking to the program team.

The hand calculation is close but not identical in some rows. For an adhering responsive patient it says 0.489, but the exact index is 0.328. The difference: the hand calculation assumes the patient is never visited again, while the exact index knows that if they lapse later you can still visit then. That lowers the urgency of visiting today. This is why the method searches for the break-even subsidy rather than stopping at the one-step formula.

### Putting the estimates and the index together

In practice the probabilities come from [From Records to Estimates](#from-records-to-estimates--plausible-ranges-then-optimism), using the **optimistic** values for anything poorly measured. So each week:

1. Update the ledger with last week's records, with old records fading.
2. For each group, compute optimistic probabilities.
3. Compute each patient's Whittle index from their group's probabilities and their current state.
4. Visit the top 80.

Repeat every Monday. As evidence builds up, the optimism fades and the index converges on the true priorities.

---

## Scaling Up – Real Limits on Who Can Be Visited

The plain rule, "top 80 by index," needs three adjustments in the field.

**1. Each CHW has their own patients and 8 visits.** If the top 80 patients happen to cluster in two CHWs' areas, a single top-80 list is impossible to carry out. The fix is simple here: **rank within each CHW's area and take the top 8.** It gives up a little total benefit in exchange for a list each CHW can actually do.

**2. Nobody goes unvisited forever.** A pure index policy can leave hard-to-move or steady patients unvisited for months. The program promised every patient a visit at least once a quarter. Apply it first: any patient approaching 12 weeks without a visit is added to their CHW's list, and the remaining slots are filled by index.

**3. More than one kind of visit.** If the program later adds, say, a pharmacist visit costing 2 CHW-hours alongside a 1-hour CHW visit, choosing the best mix under hour limits becomes a *knapsack problem*: like packing the most valuable items into a bag with a weight limit. That is solved with integer programming, the tool explained in the [Case 2 tutorial](02-welfare-optimization-borehole-siting.md). With one kind of visit and a fixed number of slots, sorting is enough.

---

## Code Implementation & Simulation

The full program is [`code/case1_restless_bandits.py`](code/case1_restless_bandits.py). It needs only `numpy`:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case1_restless_bandits.py
```

### The Whittle index, found by bisection

```python
def whittle_index(p_passive, p_active, state, beta=BETA):
    """Smallest subsidy that makes 'don't visit' as good as 'visit' in this state."""
    lo, hi = -1.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        _, q_pas, q_act = values_with_subsidy(p_passive, p_active, mid, beta)
        if q_act[state] > q_pas[state]:
            lo = mid          # visiting still wins: the subsidy must be higher
        else:
            hi = mid          # skipping wins: the subsidy can be lower
    return (lo + hi) / 2
```

`values_with_subsidy` repeats the "value now = reward + 0.9 × expected value next week" calculation until the numbers stop changing, with the subsidy added to the no-visit choice. Bisection halves the search range each time, so 50 rounds pin the index down to far more decimal places than needed.

### The optimistic estimate

```python
def optimistic(successes, trials, week, prior=0.5):
    p_hat = (successes + prior) / (trials + 2 * prior)
    radius = np.sqrt(2 * np.log(week) / (trials + 2 * prior))
    return min(1.0, p_hat + radius), p_hat, radius
```

### Simulation: three policies, 12 weeks

The code simulates 1,200 patients, 400 in each group, starting with 60% adhering, and runs 12 weeks under three policies with 80 visits a week:

- **Rotation:** visit the next 80 patients on the list each week.
- **Risk score:** visit lapsing patients first, worst recovery odds first.
- **Whittle:** visit the 80 highest Whittle indices.

```
Simulation - 12-week simulation, average share adhering (1,200 patients, 80 visits/week)
  rotation   0.451
  risk score 0.422
  whittle    0.490
```

The **risk score does worse than simple rotation**: it pours visits into hard-to-move patients where they change little. The Whittle policy keeps about 4 more patients in every 100 adhering than rotation, with the same 80 visits. With 1,200 patients, that is roughly 47 more people taking their medication in an average week.

Two cautions. These groups and probabilities are invented to teach the method; real gains depend on real data. And this simulation gives the Whittle policy the true probabilities. In the field it would start from the estimates in [From Records to Estimates](#from-records-to-estimates--plausible-ranges-then-optimism) and learn, so early weeks would do somewhat worse, which is exactly what a pilot measures.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **States and actions** | state $\in \{0, 1\}$; action $\in$ {visit, no visit} | Turns each patient's weekly pill count into a simple, recordable condition |
| **Transition ledger** | $\hat p = \dfrac{k + 0.5}{n + 1}$ | Counts what happened to similar patients with and without visits |
| **Forgetting factor** | $N_{t+1} = \alpha N_t + \text{new}$ | Keeps estimates current when patients' responses drift; $\alpha = 0.9$ ≈ the last 10 weeks |
| **Optimism** | $p^{+} = \min(1, \hat p + \sqrt{2 \ln t / n})$ | Gives poorly tested groups the benefit of the doubt so the program keeps learning |
| **Long-run value** | $V(s) = r(s) + \beta \sum_{s'} P(s \to s')\,V(s')$ | Counts this week and future weeks, with $\beta = 0.9$ discounting |
| **Whittle index** | break-even subsidy $m$; ≈ $\beta\,\Delta p\,(V_1 - V_0)$ | One priority number per patient: how much a visit now is worth |
| **Weekly selection** | top 8 per CHW, after the quarterly-visit guarantee | Turns priorities into lists each CHW can carry out |

### Where to go next

- **Run the pilot** described in the [case's follow-ups](../cases/01-chw-hypertension-visits.md#after-the-recommendation): split CHW areas between the index list and current practice for 8–12 weeks.
- **Read** the Google Research post on ARMMAN and the AAAI 2022 field study (Mate et al.), listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Code to build on:** [lily-x/online-rmab](https://github.com/lily-x/online-rmab), research code for UCWhittle from the authors of the AAAI 2023 paper.
- **Other tutorials:** [adaptive experiments for SMS reminders](09-adaptive-experiments-sms-reminders.md) for when the open question is which of several options works rather than how each person drifts (Class 8); [policy learning for business grants](08-policy-learning-business-grants.md) for targeting a one-off program by its effect when trial data exist (Class 7); [risk-based inspection for lead pipes](13-risk-based-inspection-lead-pipes.md) for when the goal is to find hidden problems, not change behavior (Class 12); and [welfare optimization for borehole siting](02-welfare-optimization-borehole-siting.md), which explains the integer programming mentioned under [Scaling Up](#scaling-up--real-limits-on-who-can-be-visited).
