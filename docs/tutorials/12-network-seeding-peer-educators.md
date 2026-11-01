# Network Seeding Masterclass: Choosing 25 Peer Educators Whose Message Travels Furthest

*An in-depth walkthrough of friendship networks, the independent cascade model, Monte Carlo reach estimates and greedy seed selection, built on [Case 12: Choosing peer educators for HIV prevention at a youth shelter](../cases/12-peer-educators-network-seeding.md).*

**You need:** proportions, probabilities, expected values and the idea of a confidence interval. **You don't need:** any machine learning, network science or optimization background. Every term is explained when it first appears.

**Approach:** [Class 11: Network Seeding](../../prompt/knowledge/taxonomy.md#class-11-network-seeding). **Code:** [`code/case12_network_seeding.py`](code/case12_network_seeding.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A city youth-services NGO runs a shelter and drop-in center used by about **400** young people aged 16–24. It has funding to train **25** of them as peer educators on HIV prevention (testing, PrEP, condom use) over a two-day course. The goal is for the message to reach as many residents as possible through conversations among the youth themselves. Until now, case workers have picked the trainees. Some invitees will say no. Nobody has data on who trained before or how far the message went, but staff could ask residents, on the check-in tablets, to name up to three closest friends at the shelter.

The usual answers are a ranked list: train the 25 most at-risk youth, or the 25 that staff know as "natural leaders," or the 25 with the most friends. All three treat the training as something that stays with the trainee. It doesn't: its value is in the conversations it starts. At-risk youth are often on the edge of the network, so the message stops with them. Leaders and popular youth tend to be friends of one another, so several trainees reach the same people while whole groups hear nothing.

This tutorial builds the alternative step by step:

1. **[The Seeding Leap](#the-seeding-leap--from-a-ranked-list-to-a-spread-model)** turns the friendship survey into a table and the "passing it on" into a simple probability model.
2. **[The Core Bottleneck](#the-core-bottleneck--overlap-an-unknown-p-and-refusals)** names what makes this hard: overlapping reach, a pass-on chance nobody knows, and refusals.
3. **[From Friendship Survey to Estimates](#from-friendship-survey-to-estimates--reach-by-simulation)** estimates a plan's reach by simulating the message many times, with a confidence interval.
4. **[The Decision Engine](#the-decision-engine--greedy-seed-selection)** picks seeds one at a time by their *extra* reach, on a 10-person example you can check by hand, and explains why that is guaranteed to be good.
5. **[Scaling Up](#scaling-up--400-residents-25-places-10-backups)** runs it on a 400-resident shelter, with backups, a check on the unknown pass-on chance, privacy and a way to measure spread.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** shows the program and what its results mean.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **a trainee's value depends on who else is trained, so choose people whose friends don't overlap.**

---

## The Seeding Leap – From a Ranked List to a Spread Model

### Why a ranked list is the wrong shape

A ranking scores each person on their own and takes the top 25. That works when each place's value stands alone. Here it doesn't. If two trainees share most of their friends, the second one adds little: the friends would probably have heard anyway. **The value of a trainee depends on which other trainees are chosen.** This is the same lesson as overlapping catchments in the [borehole tutorial](02-welfare-optimization-borehole-siting.md), except that here the overlap travels along friendships, and it is uncertain.

The people chosen to start the spread are called **seeds**. Choosing seeds so that a message reaches as many people as possible is called **influence maximization**, and the standard formulation is by Kempe, Kleinberg and Tardos (KDD, 2003).

### A network is a friendship table

A **network** is just a list of people and a list of who is linked to whom. The tablet survey produces it directly. Each answer "Maria names Jo" is a **nomination**. Turn nominations into **friendship pairs** by treating a pair as linked if either person named the other, and listing each pair once:

| Person 1 | Person 2 |
|---|---|
| 017 | 112 |
| 017 | 245 |
| 112 | 245 |
| … | … |

That two-column table, on pseudonymized IDs, is the whole network. A spreadsheet can hold it. Tools such as [NetworkX](https://networkx.org), the Python library the playbook recommends, store the same table and add ready-made functions; the tutorial's code uses plain arrays so every step is visible.

Two words recur. A person's **degree** is their number of friendship pairs: how many people they named plus how many named them. A **cluster** (or friend group) is a set of people with many links among themselves and few to the outside.

### The independent cascade

To compare plans we need a model of how a message passes from friend to friend. The **independent cascade** model, the simplest standard one, says:

1. On day one, the seeds know the message.
2. Whenever someone hears it for the first time, they get **one chance** to pass it to each friend who hasn't heard it yet. Each chance succeeds with probability $p$, independently of the others, like a separate coin flip for each friend.
3. People who hear it pass it on in the same way. The spread stops when a round produces no new listeners.

The **reach** of a set of seeds is the number of residents who end up hearing the message, seeds included. Because the coin flips are random, reach is random. What we compare is its **expected value**: the average reach over many repetitions.

A one-line check of the model: a seed with three friends who have no other friends reaches $1 + 3p$ people on average. With $p = 0.5$, that is 2.5.

### Mapping it to the program

| Model term | In this program |
|---|---|
| Population | The roughly 400 young people using the shelter |
| Network | Friendship pairs from the tablet survey: "Name up to three closest friends here" |
| Seeds | The 25 training places |
| Pass-on chance $p$ | The chance a trainee, or anyone who has heard, talks to a given friend about it; a rough guess, tested low and high |
| Reach | Residents who hear the message, including the trainees |
| Participation | Invitees may decline; 10 ranked backups refill the places |
| Outcome measure | A later tablet question: "Has another resident talked to you about HIV testing or PrEP?" |

### What the evidence says

The closest work is direct. Yadav and colleagues (IJCAI, 2018) ran pilots with 173 youth in Los Angeles shelters, using algorithm-chosen peer leaders to raise HIV awareness. Wilder and colleagues (AAAI, 2021) reported a trial with 713 youth experiencing homelessness in which risk behavior fell in the arm whose peer leaders the algorithm chose. These are research pilots and a trial, not routine deployments. Banerjee and colleagues (Review of Economic Studies, 2019) are a parallel from another domain: in Haryana, India, seeding immunization reminders with villagers nominated as good spreaders of news raised vaccinations (about 22% in the paper's abstract; J-PAL's summary reports 27%). It shows that the cheap fallback question "who here is good at spreading news?" can work when a full friendship survey can't be run.

---

## The Core Bottleneck – Overlap, an Unknown p and Refusals

### Overlapping reach

Add up what each of 25 seeds would reach *on their own* and you get a number that the 25 together never achieve, because their audiences overlap. In the 400-resident shelter of [Scaling Up](#scaling-up--400-residents-25-places-10-backups), the staff-style picks would reach 87.5 people if each worked alone, but together they reach only **51.3**. Most of the difference is the same friends being counted several times.

### Why popularity and risk mislead

- **The most popular** (highest degree) do reach many people each. But popular people cluster: they are often friends of one another, in the biggest groups. The second popular person in a group adds less than the first.
- **The most visible** to staff are usually the ones at the front desk most often: a handful of groups, not the whole shelter. In the synthetic shelter, 24 of the 25 staff-style picks come from the two "drop-in regular" groups.
- **The most at-risk** are a sensible target for *services*, but the training isn't the service; the conversations are. In the synthetic shelter, residents in the top 10% of the intake risk score name or are named by 3.15 friends on average, against 4.09 for everyone else. Seeds on the edge of the network start fewer conversations.

### Nobody knows p

The model needs $p$, the chance that a friend passes the message on. The NGO has no data on it (Filter 4 of the case: "Nothing useful"). Any value is a guess. The fix is not to pretend to know it but to check whether the *choice of seeds* depends on it: [Scaling Up](#scaling-up--400-residents-25-places-10-backups) tries a low and a high value.

### Refusals and a moving population

Invitees can say no, and some will. Residents arrive and leave every week, so the friendship map ages fast. Both argue for the same habits: rank backups in advance, and collect the survey in the two weeks before each training rather than once a year.

---

## From Friendship Survey to Estimates – Reach by Simulation

### Step 1: From nominations to a friendship table

In the synthetic shelter, 362 of the 400 residents answer the survey (10% skip it, though others can still name them). They make 827 nominations, which become **799 friendship pairs**; 28 nominations were mutual and are merged. Residents have 4.00 friends on average (median 4, most 18), and 7 have none listed. Because most friends are in the same group, 90% of pairs fall inside one of the 14 friend groups.

### Step 2: One cascade, acted out

Take the 10-person example of [The Decision Engine](#the-decision-engine--greedy-seed-selection) and seed person A, with $p = 0.5$. Flip a coin for each of A's four friends. Each friend who hears flips coins for their own friends who haven't heard yet, and so on. Count who has heard when it stops. That count is **one run**. Run it again and the coins come out differently: one run might reach 2 people, the next all 5 in A's group.

### Step 3: Monte Carlo: average many runs

Expected reach is the average over infinitely many runs. We can't do infinitely many, but we can do many, and basic statistics tells us how close we are. This is **Monte Carlo simulation**: estimate an average by repeating a random experiment and averaging.

The code runs the cascade from A 1,000 times:

| Runs | Mean reach | 95% confidence interval | Exact answer |
|---|---|---|---|
| 1,000 | 3.712 | 3.636 to 3.788 | 3.750 |

The interval is the usual $\bar x \pm 1.96\, s / \sqrt{n}$, where $s$ is the standard deviation of the 1,000 reach counts. It contains the exact answer, which the code can also compute for so small a network (Step 4 explains how). Only 30.2% of runs reached all five people in A's group: averages hide a lot of run-to-run variation, which is why one training cycle's result is noisy.

To halve the interval, multiply the runs by four. The full-size comparisons below use 2,000 runs per plan, which gives intervals under ±0.5 people wide.

### Step 4: The coin-flip shortcut

A friendship is only ever "tried" once: by whichever of the two friends hears first. (If the try fails and the other friend hears later by another route, they would try back, but the first one already knows.) So the whole cascade is the same as **flipping one coin per friendship in advance**, keeping the links that came up heads, and saying: everyone connected to a seed by a chain of kept links hears the message.

Each set of coin flips is called a **world**. This shortcut, from Kempe and colleagues, has two uses:

- **Speed.** Flip the coins for 2,000 worlds once, then score any set of seeds on the same worlds by looking up who is connected to whom. No need to rerun the cascade for every candidate plan.
- **Exact answers for small networks.** The 10-person example has 11 friendships, so there are only $2^{11} = 2{,}048$ possible worlds. The code scores every one, weighted by its probability, and gets the exact expected reach: 3.750 for seed A.

### Step 5: Score plans on fresh worlds

The program chooses seeds using one set of 2,000 worlds and scores every plan on a **different** 2,000. If you choose and grade on the same worlds, the chosen plan looks a little better than it is, because it was picked partly for that set's lucky coin flips. Here the effect is too small to see (greedy scores 77.5 on the worlds it was chosen with and 77.8 on fresh ones), but with fewer worlds or more candidates it grows, and the habit costs nothing.

---

## The Decision Engine – Greedy Seed Selection

### Step-by-step concrete example: 10 residents, 2 seeds

Here is a shelter small enough to check by hand. Ten residents, $p = 0.5$, and budget for **2** seeds.

- **Group 1:** A, B, C and D are all friends with each other; E is friends with A only.
- **Group 2:** H is friends with F, G and I; I is friends with J.
- No friendships between the groups.

| Person | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| Friends (degree) | 4 | 3 | 3 | 3 | 1 | 1 | 1 | 3 | 2 | 1 |
| Expected reach alone | 3.750 | 3.625 | 3.625 | 3.625 | 2.625 | 2.125 | 2.125 | 2.750 | 2.500 | 2.000 |

Check H by hand. H always counts (1). F, G and I each hear with probability 0.5. J hears only if I hears *and* passes it on: $0.5 \times 0.5 = 0.25$. So $1 + 0.5 + 0.5 + 0.5 + 0.25 = 2.75$. Check J the same way: $1 + 0.5\,(\text{I}) + 0.25\,(\text{H}) + 0.125 + 0.125\,(\text{F, G}) = 2.0$.

A's reach of 3.750 is harder by hand because of the extra routes inside Group 1: B can hear from A directly, or via C, or via D. The enumeration of all 2,048 worlds gives it exactly, and the Monte Carlo of Step 3 agrees.

**Step A: The ranked list's answer.** The two most-connected people are A (4 friends) and B (3). Together they reach **4.188** on average. Group 2 never hears anything.

**Step B: Greedy.** **Greedy seed selection** builds the set one person at a time. Each round, it adds the person with the largest **marginal gain**: the *extra* expected reach they add, given the seeds already chosen.

- *Round 1.* Nobody is chosen yet, so the gain is just each person's reach alone. A is largest at 3.750. Pick A.
- *Round 2.* Now recompute every gain, given A:

| Candidate | B | C | D | E | F | G | **H** | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Extra reach given A | 0.438 | 0.438 | 0.438 | 0.500 | 2.125 | 2.125 | **2.750** | 2.500 | 2.000 |

B was worth 3.625 alone, but only 0.438 once A is chosen: most of B's audience already hears from A. Everyone in Group 2 keeps their full value, because A can't reach them. Pick H. Total: $3.750 + 2.750 = $ **6.500**.

**Step C: Check against every pair.** With 10 people there are only 45 pairs, so the code tries all of them. The best is A + H at 6.500, the pair greedy found. The next best (B, C or D with H) reach 6.375. Seeding the two most popular people reaches $6.500 - 4.188 = 2.3$ fewer people on average, with the same two training places.

### Diminishing returns

The pattern in Round 2 has a name. Adding a person to a *smaller* seed set gains at least as much as adding them to a *larger* one: B adds 3.625 to an empty set but 0.438 to {A}. This is **diminishing returns** (mathematicians say the reach function is **submodular**). It holds for the independent cascade on any network, and it is the reason greedy works well.

The full-size run shows it round by round. The expected gain of the seed added in each round falls steadily:

| Round | 1 | 2 | 3 | 5 | 10 | 15 | 20 | 25 |
|---|---|---|---|---|---|---|---|---|
| Extra residents reached | 6.10 | 4.97 | 4.47 | 3.98 | 2.94 | 2.66 | 2.42 | 2.20 |

### The 1 − 1/e guarantee, plainly

Could greedy be fooled into a poor set? Kempe, Kleinberg and Tardos proved that it can't be fooled badly: **on any network, greedy's expected reach is at least $1 - 1/e \approx 63.2\%$ of the best possible set's.** ($e \approx 2.718$ is the base of natural logarithms.)

The argument, in words. Suppose the best possible set of 25 reaches some number of people more than greedy has so far: call it the gap. Because of diminishing returns, adding all 25 of the best set's members to greedy's current set would close that whole gap, so at least one of them, on its own, closes at least 1/25 of it. Greedy picks the person with the largest gain, so each round closes at least 1/25 of whatever gap is left. After 25 rounds, at most $(1 - 1/25)^{25} = 0.36$ of the original gap remains, which is less than $1/e \approx 0.37$. So greedy gets at least 63% of the way.

Three honest caveats. The guarantee is a floor; in practice greedy is usually much closer (it found the best pair in the toy example). It applies to the model, so it says nothing about whether $p$ or the friendship map is right. And it assumes expected reach is computed exactly; with simulated worlds it holds up to the simulation's small error.

### Why not just try every set?

For 2 seeds out of 10 people, 45 pairs is easy. For 25 seeds out of 400 residents, the number of possible sets is about $3.4 \times 10^{39}$. No computer could list them. Unlike the borehole problem, there is no practical way to prove the best set here; greedy's guarantee is the standard substitute. Greedy needs only 25 rounds of 400 candidates, which takes seconds.

---

## Scaling Up – 400 Residents, 25 Places, 10 Backups

### The synthetic shelter

The code builds an illustrative shelter that matches the case: 400 residents in 14 friend groups of sizes 60, 48, 40, 36, 32, 30, 28, 26, 24, 22, 20, 14, 12 and 8. Each resident who answers names 1 to 3 friends, mostly in their own group and preferring more sociable people. Each resident also has an intake risk score, and residents with higher risk are a little less social. Two groups are "drop-in regulars" who spend most time near the front desk; staff know them best. All of this is invented to teach the method.

Planning value: $p = 0.15$, a modest chance that any one friend passes the message on.

### Four plans compared

Each plan gets 25 seeds and is scored on 2,000 fresh worlds:

| Plan | Expected reach | 95% CI | Share of residents | Groups with a seed | Sum of solo reaches |
|---|---|---|---|---|---|
| Random (100 draws) | 53.2 | middle 90% of draws: 49.1 to 56.8 | | | |
| Most at-risk (intake score) | 50.1 | 49.7 to 50.5 | 12.5% | 10 of 14 | 54.3 |
| Staff picks (most visible) | 51.3 | 50.9 to 51.6 | 12.8% | 3 of 14 | 87.5 |
| Most friends (degree) | 71.9 | 71.5 to 72.3 | 18.0% | 10 of 14 | 100.9 |
| **Greedy** | **77.8** | **77.4 to 78.3** | **19.5%** | **13 of 14** | 92.5 |

The last column is what the seeds would reach if each worked alone. Comparing it with the combined reach shows the overlap.

- **Staff picks and the most at-risk do no better than random.** Staff picks have a large solo total (87.5) but cluster in 3 groups, so most of it is overlap. At-risk seeds spread out, but each starts few conversations.
- **Degree does well but wastes seeds on overlap.** Its solo total, 100.9, is the highest of any plan; its combined reach is 29 less.
- **Greedy reaches the most** by spreading seeds over 13 of the 14 groups. Its seeds still have many friends (8.8 on average, against 9.4 for the degree plan), and 15 of its 25 seeds are also on the degree list. It replaces the 10 popular people whose friends were already covered.

Because every plan is scored on the same worlds, the differences can be measured directly, world by world, which gives tight intervals:

| Greedy minus | Extra residents reached | 95% CI |
|---|---|---|
| Most at-risk | 27.7 | 27.3 to 28.2 |
| Staff picks | 26.6 | 26.1 to 27.0 |
| Most friends | 5.9 | 5.6 to 6.2 |

These intervals measure *simulation* uncertainty only: how sure we are about the model's answer, not whether the model is right. Against staff picks the gain is large (about half as many residents again). Against the degree list it is small, and the [pilot](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) is what would show whether it is real at this shelter.

### Sensitivity to the unknown p

The code reruns everything at a low and a high value of $p$. For each, it chooses greedy seeds afresh and also scores the original list chosen at $p = 0.15$. Every row uses new worlds, which is why the 0.15 row shows 77.7 rather than 77.8:

| $p$ | Greedy re-chosen for this $p$ | Original greedy list | Degree | Staff picks | Most at-risk | Seeds kept from original list |
|---|---|---|---|---|---|---|
| 0.08 | 47.6 | 47.6 | 45.5 | 36.7 | 33.9 | 22 of 25 |
| 0.15 | 77.7 | 77.7 | 71.8 | 51.1 | 50.5 | 24 of 25 |
| 0.25 | 144.6 | 143.8 | 129.4 | 88.7 | 105.3 | 17 of 25 |

Three things stand out:

- **The ranking of plans doesn't change.** Greedy beats degree, which beats staff picks and the at-risk list, at every value tried.
- **Guessing $p$ wrong costs almost nothing.** The list chosen at 0.15 reaches the same as the re-chosen list at 0.08, and 0.8 fewer residents (144.6 against 143.8) at 0.25, even though 8 of its seeds would change.
- **Reach itself depends heavily on $p$**, from 47.6 to 144.6. So don't promise the funder a number of residents; promise a comparison with staff picks, measured as described below.

The 0.15 row also shows Monte Carlo noise in the choice itself: with a different set of 2,000 worlds, greedy keeps 24 of its 25 seeds. Near-ties between candidates are broken by chance, which doesn't matter for reach.

### Refusals and backups

Suppose each invitee declines or leaves before training with probability 20% (an illustrative figure; record the real rate each cycle). The number of declines among 25 then follows a **binomial distribution**: expected value $25 \times 0.2 = 5$, standard deviation $\sqrt{25 \times 0.2 \times 0.8} = 2$.

The backups are rounds 26 to 35 of the same greedy run: the next 10 people with the most extra reach. Their gains (2.12 down to 1.84) are close to the 25th seed's 2.20, so a backup is nearly as good as the seed it replaces. When someone declines, staff invite the backup who adds the most *new* reach given those who have accepted (the code recomputes this each time). The code simulates 2,000 rounds of invitations:

| Situation | Expected reach | Trainees on average |
|---|---|---|
| All 25 accept | 77.8 | 25 |
| Declines, no backups | 64.3 | 20 |
| Declines, 10 ranked backups | 74.8 | 24.9 |

The backups recover most of the loss. They run out (fewer than 25 trainees after all 35 invitations) in 8.3% of simulated rounds; the exact binomial chance of fewer than 25 acceptances among 35 is 7.5%, and the two agree within simulation error. If the real decline rate turns out higher, extend the list.

### Consent, privacy and safe storage

A friendship map of homeless youth reveals who associates with whom in a vulnerable population. It must be handled as sensitive data:

- **Consent first.** Opt-in, on one screen drafted with the shelter's safeguarding lead; residents under 18 may need extra steps. Residents who decline still use every service.
- **Pseudonymized IDs.** The volunteer's script sees numbers, not names; only the program manager links IDs to names, and only for the 35 people to invite.
- **Minimal output.** Case workers see a list of names to invite, never the network or anyone's friends.
- **Storage and deletion.** The friendship file is encrypted, readable only by the program manager and the volunteer, and deleted after each cycle.

If residents are uneasy naming friends to staff, use the case's fallback question, "who here is good at spreading news?", the proxy that Banerjee and colleagues found effective in Haryana.

### Measuring spread later

The model's reach is a prediction. The real outcome is the share of residents who answer yes to a later tablet question: "Has another resident talked to you about HIV testing or PrEP?" The case's [pilot](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) alternates training cycles between greedy and staff-picked seeds and compares those shares.

How big a difference could one comparison detect? The model predicts 19.5% hearing it under greedy and 12.8% under staff picks, a difference of 6.6 percentage points. The 95% margin of error for a difference of two proportions is $1.96 \sqrt{p_1(1 - p_1)/n_1 + p_2(1 - p_2)/n_2}$. With 400 residents answering in each cycle, that is **±5.1** points; with 200, **±7.2** points, wider than the difference itself. And these margins are optimistic, because friends hear together (or not at all), so answers aren't independent. Expect to need several cycles, and plan the pilot for 2–6 months, as the playbook suggests.

---

## Code Implementation & Simulation

The full program is [`code/case12_network_seeding.py`](code/case12_network_seeding.py). It needs only `numpy`:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case12_network_seeding.py
```

### From survey answers to a friendship table

```python
pairs = sorted({(min(a, b), max(a, b)) for a, b in nominations})
U = np.array([a for a, b in pairs])
V = np.array([b for a, b in pairs])
degree = np.bincount(np.concatenate([U, V]), minlength=n)
```

`nominations` holds one (who answered, whom they named) entry per name given. Each pair is stored once, smallest ID first, so "Maria named Jo" and "Jo named Maria" become one friendship. `U` and `V` are the two columns of the friendship table.

### One cascade, step by step

```python
def toy_cascade(seeds, adj, p, rng):
    """One run of the independent cascade, step by step, as you would act it out."""
    heard, newly = set(seeds), list(seeds)
    while newly:
        nxt = []
        for person in newly:
            for friend in adj[person]:
                if friend not in heard and rng.random() < p:   # one try per friend
                    heard.add(friend)
                    nxt.append(friend)
        newly = nxt
    return len(heard)
```

This is the model of [The Seeding Leap](#the-seeding-leap--from-a-ranked-list-to-a-spread-model), line for line. The toy example runs it 1,000 times; the full-size runs use the faster coin-flip worlds of [Step 4](#step-4-the-coin-flip-shortcut).

### The greedy loop

```python
    def gains(self, seeds):
        """Expected extra people reached by adding each person to `seeds`."""
        covered = np.zeros(self.R * self.n, dtype=bool)
        if seeds:
            covered[self.gid[:, list(seeds)].ravel()] = True
        return (self.size[self.gid] * ~covered[self.gid]).mean(axis=0)

    def greedy(self, k):
        """Add one seed at a time, each time the person who adds the most expected reach."""
        seeds, gain_log = [], []
        for _ in range(k):
            g = self.gains(seeds)
            g[seeds] = -1                                   # already chosen
            best = int(np.argmax(g))
            seeds.append(best)
            gain_log.append(g[best])
        return seeds, gain_log
```

In each world, `gid` labels every resident with their **connected set**: everyone joined to them by kept friendships, who would all hear the message together. `size` is how many people are in each set. A candidate's gain in one world is the size of their set if no seed is in it yet, and zero if one is; `gains` averages that over all worlds. That single line is diminishing returns in code. `greedy(35)` returns the 25 seeds followed by the 10 backups.

### Simulation output

```
Plans for 25 seeds, scored on 2000 fresh worlds (p=0.15)
  random (100 draws)             reach=  53.2  middle 90% of draws 49.1 to 56.8
  most at-risk (intake score)    reach=  50.1  95% CI 49.7 to 50.5  (12.5%)  groups with a seed=10/14  seeds in groups 0-1= 6  sum of solo reaches=54.3
  staff picks (most visible)     reach=  51.3  95% CI 50.9 to 51.6  (12.8%)  groups with a seed= 3/14  seeds in groups 0-1=24  sum of solo reaches=87.5
  most friends (degree)          reach=  71.9  95% CI 71.5 to 72.3  (18.0%)  groups with a seed=10/14  seeds in groups 0-1=11  sum of solo reaches=100.9
  greedy (influence max.)        reach=  77.8  95% CI 77.4 to 78.3  (19.5%)  groups with a seed=13/14  seeds in groups 0-1= 7  sum of solo reaches=92.5
  greedy minus most at-risk (intake score)     27.7  95% CI 27.3 to 28.2
  greedy minus staff picks (most visible)      26.6  95% CI 26.1 to 27.0
  greedy minus most friends (degree)            5.9  95% CI 5.6 to 6.2
```

The whole program, including the toy example, the sensitivity check and the refusal simulation, runs in under a minute on a laptop. Its output is the same on every run, because every random step uses a fixed seed.

### What the results say

- **Spreading seeds out matters more than picking popular people.** Greedy reaches 77.8 residents on average, 26.6 more than staff-style picks with the same 25 places: about half as many residents again.
- **The popular-people list is a strong simple rule here,** within 5.9 residents of greedy. A shelter that can't run the script would do far better with "most friends, at most a few per group" than with staff picks. The greedy script does that balancing automatically.
- **The at-risk list does worst,** below even random seeds. The case's warning holds: the message stops with seeds on the edge of the network.
- **The choice is robust to $p$; the reach number isn't.** Report comparisons, not promises.
- **Backups matter.** Without them, a 20% decline rate costs 13.5 residents of reach; with 10 ranked backups, 3.0.

Two cautions. The shelter, friendships, risk scores and decline rate are invented to teach the method; the real gain depends on the real friendship map, especially how clustered it is. And "reach" means *hearing the message as modeled*, not getting tested or starting PrEP; the follow-up question measures the first, and the program's own records the rest.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Network** | friendship pairs from "name up to three closest friends" | A two-column table on pseudonymized IDs; a spreadsheet or NetworkX can hold it |
| **Spread model** | each new listener passes it to each friend once, with probability $p$ | The independent cascade; $p$ is a rough guess, tested low and high |
| **Reach estimate** | mean of many simulated runs $\pm 1.96\, s / \sqrt{n}$ | Monte Carlo; coin-flip worlds make it fast and exact for small examples |
| **Objective** | maximize expected reach of the seed set | Counts each resident once, however many trainees they know |
| **Greedy selection** | add the person with the largest marginal gain, 25 times | Spreads seeds across friend groups; at least $1 - 1/e \approx 63\%$ of the best possible |
| **Diminishing returns** | gain given a larger set $\le$ gain given a smaller set | Why the second seed in a group adds little, and why greedy is guaranteed |
| **Sensitivity** | re-choose at low and high $p$, compare | Shows the seed list barely depends on the guess |
| **Backups** | greedy rounds 26–35; refill with the largest new gain | Turns a refusal into the next name on an agreed list |
| **Privacy** | consent, pseudonyms, encryption, deletion each cycle | Protects a sensitive map of who knows whom |
| **Measurement** | share answering yes to the follow-up question, by arm | Tests the model against staff picks over several cycles |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/12-peer-educators-network-seeding.md#after-the-recommendation): draft the consent and friendship question with the safeguarding lead, collect two weeks of answers, and have the volunteer produce a seed list and a staff-picked list for comparison. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) sections of the playbook cover the Class 11 specifics.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section names NetworkX and partners; the volunteer graduate student can adapt this tutorial's program, which is short and uses only numpy.
- **Read** Banerjee et al. (2019), *Using Gossips to Spread Information*, then Wilder et al. (2021) on the HIV-prevention trial and Kempe, Kleinberg & Tardos (2003) on the greedy method, all listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact). Bryan Wilder (Carnegie Mellon) and Eric Rice (USC) work on peer-leader selection for this population.
- **Other tutorials:** [welfare optimization](02-welfare-optimization-borehole-siting.md) for benefits that stay with the person who receives them, the same overlap lesson without the spreading; [adaptive experiments](09-adaptive-experiments-sms-reminders.md) for learning which version of a message works while you send it; and [deciding without a model](06-no-model-food-pantry.md) for when the friendship survey can't be run and a written rule, such as staff nominating trusted messengers, has to do.
