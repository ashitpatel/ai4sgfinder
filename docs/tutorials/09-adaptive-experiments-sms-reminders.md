# Adaptive Experiments Masterclass: Finding the Best Vaccination Reminder While Still Sending It

*An in-depth walkthrough of adaptive experiments, Beta–Binomial updating, Thompson sampling and exploration sampling, built on [Case 9: Choosing the best vaccination-reminder SMS while still sending it](../cases/09-sms-reminders-adaptive-experiment.md).*

**You need:** proportions, probabilities, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 8: Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating). **Code:** [`code/case9_thompson_sampling.py`](code/case9_thompson_sampling.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A district immunization NGO sends an SMS reminder to parents a few days before each child's vaccination date. About **400 new parents** join the reminder list every week. The team has written four wordings: the current plain reminder (**A**), one that names the child (**B**), one that stresses protection from disease (**C**), and one that says most parents in the area vaccinate on time (**D**). Nobody knows which gets more children vaccinated on time. The clinic system records each vaccination within a week, and the M&E analyst can change the message mix every Monday.

The usual answer is a fixed randomized trial: send each wording to 25% of parents for ten weeks, then compare. It gives a clean comparison, but it keeps sending three quarters of parents a weaker message long after the data show which ones are weaker. The other usual answer, a staff vote on which wording "sounds best", locks in a guess.

This tutorial builds the alternative step by step:

1. **[The Adaptive Leap](#the-adaptive-leap--from-a-fixed-ab-test-to-learning-while-sending)** names the trade-off between learning and doing well now, and maps an *adaptive experiment* onto the reminder program.
2. **[The Core Bottleneck](#the-core-bottleneck--small-differences-noisy-weeks-and-late-records)** names what makes it hard: small differences, noisy weekly counts and late records.
3. **[From Outcomes to Estimates](#from-outcomes-to-estimates--beta-posteriors-for-on-time-rates)** turns on-time counts into a range of plausible rates for each wording, and into the probability that each one is best.
4. **[The Decision Engine](#the-decision-engine--thompson-sampling-and-exploration-sampling)** turns those probabilities into next week's shares with **Thompson sampling** or **exploration sampling**, and works two weeks through by hand.
5. **[Scaling Up](#scaling-up--ten-weeks-4000-parents-one-spreadsheet)** adds the weekly routine, the stopping rule in practice, the field evidence, and when a fixed trial is still the better choice.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs 2,000 simulated ten-week experiments and compares the designs.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **send each wording in proportion to how likely it is to be the best, and let that likelihood sharpen week by week.**

---

## The Adaptive Leap – From a Fixed A/B Test to Learning While Sending

### Explore or exploit

Every week the analyst faces the same tension. **Exploiting** means sending the wording that looks best so far, to get as many children vaccinated on time as possible *this week*. **Exploring** means sending the other wordings too, to find out whether one of them is actually better. Exploit too early and you may lock in a wording that only looked good by luck. Explore too long and you keep paying for messages you already know are weaker.

This is the classic **multi-armed bandit** problem. The name comes from slot machines, "one-armed bandits": picture four machines, each paying out with an unknown probability, and a fixed number of pulls. Each wording is an **arm**; each parent who gets it is a **pull**; a child vaccinated on time is a **win**. A design that shifts pulls toward the better arms as results come in is an **adaptive experiment**.

### Why an equal split sends many parents weak messages

Suppose, for illustration, that the true on-time rates were A = 0.60, B = 0.67, C = 0.62 and D = 0.64. Nobody knows these numbers; the simulation in [Code Implementation & Simulation](#code-implementation--simulation) uses them to score each design.

With a fixed equal split, each week's 400 parents produce on average $400 \times (0.60 + 0.67 + 0.62 + 0.64)/4 = 253$ on-time vaccinations. If every parent got B, it would be $400 \times 0.67 = 268$. The shortfall is **15 children per week, 150 over 10 weeks**. That is the price of learning with fixed shares. The equal split pays it in full every week, even in week 9, when the data have long shown that A and C are weaker. An adaptive design pays it mostly in the early weeks, while the data are still thin.

The case's own judgment (Filter 4) is what makes this acceptable at all: a weaker message costs a few late vaccinations, which clinics catch up at the next visit. If a wrong message could do lasting harm, learning on people would need a different design.

### Mapping it to the program

| Adaptive-experiment term | In this program |
|---|---|
| Arm (option) | One of four wordings: A (current), B (child's name), C (protection), D (most parents vaccinate on time) |
| Pull | One parent receiving one wording |
| Outcome | Child vaccinated within 7 days of the due date (yes/no), from the clinic system |
| Round (batch) | One week, about 400 new parents |
| Delay | Outcomes known one to two weeks after the reminder |
| Assignment rule | Thompson sampling, or exploration sampling if the main goal is to pick one wording at the end |
| Guards | At least 10% per wording; 20% always on A, the current message, as the control |
| Stopping rule | One wording at least 95% likely to be best, or 10 weeks, whichever comes first |

### Why this is not a restless bandit

The [Case 1 tutorial](01-restless-bandits-chw-visits.md) also uses bandits, but there each arm is a *patient* whose condition changes every week, and the job is to track each one. Here each arm is a *wording*, and its on-time rate doesn't drift from week to week. Each parent receives one or two reminders and then leaves the list. There is no per-parent state to track, so Class 1 machinery would build something the program has no use for. The case's narrowing answer says exactly this: the uncertainty is which wording works best, not how each parent's situation changes.

---

## The Core Bottleneck – Small Differences, Noisy Weeks and Late Records

### The differences are small and the weekly counts are noisy

Reminder wordings rarely differ by more than a few percentage points. With 100 parents on a wording in one week and a rate near 0.6, the usual 95% margin of error is about $1.96 \times \sqrt{0.6 \times 0.4 / 100} \approx 0.096$: almost 10 points, bigger than any plausible difference. One week's ranking means little. The design has to pool weeks, and it has to be honest about how sure it is.

### There is no history to start from

The NGO has only ever sent wording A. It knows roughly A's on-time rate, but nothing about B, C or D. Every comparison has to come from the experiment itself.

### The records arrive late

A parent reminded this week has a due date a few days later, the outcome window is 7 days after that, and the clinic record takes up to a week to enter. So the shares for week $t$ can use only results from week $t-2$ and earlier. The case flags the trap: **update only on parents whose due date has passed by at least 7 days**, or records not yet entered will look like failures and make every wording look worse.

### Some losses are not acceptable at any price

Two guards are fixed in advance, whatever the data say:

- **A floor share per wording (10%).** No wording is starved of parents, so the comparison at the end stays valid and a wording that started badly by luck can recover.
- **A fixed control share on A (20%).** The current message keeps a steady benchmark group. "No SMS" is never a control: it would withhold a reminder parents already get.

---

## From Outcomes to Estimates – Beta Posteriors for On-Time Rates

### Step 1: From a proportion to a range of beliefs

You already know how to estimate a proportion: if 78 of 130 children reminded with A were vaccinated on time, the estimate is $78/130 = 0.600$, and the usual 95% confidence interval is $0.600 \pm 1.96\sqrt{0.6 \times 0.4/130}$, or 0.516 to 0.684.

An adaptive experiment needs one more thing: a statement like "there is a 59% chance that B is the best wording." A confidence interval can't give that. A **Bayesian** estimate can. It describes what we believe about the true rate as a **probability distribution**: a curve over all rates from 0 to 1, high where the rate is plausible and low where it isn't.

### Step 2: The prior: what we believe before any data

The belief before any data is the **prior**. The standard choice for a rate is a **Beta distribution**, written Beta($a$, $b$). Its mean is $a/(a+b)$. A handy way to read it: it behaves like having already seen $a - 1$ successes and $b - 1$ failures.

The code uses **Beta(1, 1)**, which is flat: every rate from 0 to 1 is equally plausible. It is worth only two imaginary parents, so the data take over almost at once. (A team that trusts A's long-run rate could start A from a stronger prior; with hundreds of parents a week, it makes little difference.)

### Step 3: Updating: add the counts

Here is why the Beta is used. If the prior is Beta($a$, $b$) and you then see $s$ on-time and $f$ late, the updated belief, the **posterior**, is simply

$$
\text{Beta}(a + s,\ b + f).
$$

Add successes to the first number and failures to the second. That is the whole update, and it is called **Beta–Binomial updating** (the "binomial" is the count of on-time children out of those sent). For A after week 1: prior Beta(1, 1), then 78 on time and 52 late, gives **Beta(79, 53)**, with mean $79/132 = 0.598$.

### Step 4: A credible interval, and how it compares

The posterior's middle 95% is a **credible interval**: there is a 95% probability the true rate lies inside it, given the data and the prior. For Beta(79, 53) the code reads it off the curve as **0.514 to 0.680**. The usual confidence interval was 0.516 to 0.684. With this much data and a flat prior they almost coincide, so nothing you know about proportions is lost. What is gained is the right to make probability statements about the rates themselves.

### Step 5: The probability that each wording is best

With a posterior for each wording, we can ask: **what is the probability that wording $k$ has the highest true rate?** One way to see it: draw one plausible rate for each wording from its posterior, note which draw is highest, and repeat thousands of times. The share of repetitions that B wins is P(B is best). The code computes the same quantity exactly by adding up, over every possible rate $x$, the chance that B's rate is $x$ times the chance that all three others are below $x$.

This one number per wording, P(best), drives everything that follows.

---

## The Decision Engine – Thompson Sampling and Exploration Sampling

### Thompson sampling: draw, then send the winner

**Thompson sampling** is the simplest good answer to explore-or-exploit. For each parent:

1. Draw one plausible rate for each wording from its posterior.
2. Send that parent the wording whose draw is highest.

A wording that is clearly better wins most draws and gets most parents. A wording that is uncertain sometimes draws high and gets some parents, which is exactly the exploring it needs. A wording that is clearly worse almost never wins.

### The same thing, as shares

Since each parent goes to wording $k$ with probability P($k$ is best), Thompson sampling is the same as giving each wording **a share of the week's parents equal to its probability of being best**. The share version suits a weekly spreadsheet: compute four shares, randomly assign the 400 parents in those shares, upload. The code checks the equivalence: after week 1 of the example below, 400 one-draw-per-parent assignments give B 233 parents, against $400 \times$ P(B best) = 235.

### Adding the guards

With the 20% control on A and the 10% floors on B, C and D, half the parents are fixed. Only the other half moves with the data:

$$
\text{share}_k = \text{floor}_k + 0.5 \times w_k, \qquad \text{floor} = (0.20,\ 0.10,\ 0.10,\ 0.10),
$$

where $w_k$ is the assignment rule's weight: $w_k = $ P($k$ best) for Thompson sampling. Before any data, every P(best) is 0.25, so the starting shares are **A 32.5%, B, C and D 22.5% each**: 130, 90, 90 and 90 parents a week.

### Exploration sampling: aimed at picking the best at the end

Thompson sampling chases the most on-time vaccinations *during* the experiment. Once one wording is fairly likely to be best, it pours parents into it, and the close runner-up gets few, so the final choice between them stays shaky. Kasy and Sautmann (Econometrica, 2021) designed **exploration sampling** for the case where the main goal is to **pick the best option at the end**. It replaces the weight with

$$
w_k = \frac{p_k (1 - p_k)}{\sum_j p_j (1 - p_j)}, \qquad p_k = \text{P}(k \text{ is best}).
$$

$p(1-p)$ is largest at $p = 0.5$ and small near 0 or 1. So a wording that is almost surely best, or almost surely not, gets little extra; the **close contenders** get the most, because that is where more data most improves the final choice.

### Step-by-step concrete example: two weeks of results

The first two weeks both go out at the starting shares, because no outcomes are in yet. Here are illustrative results, with the posteriors the code computes from a Beta(1, 1) prior:

**After week 1** (these shape week 3):

| Wording | On time / sent | Rate | Posterior | 95% credible interval | P(best) | Thompson share | Exploration share |
|---|---|---|---|---|---|---|---|
| A | 78 / 130 | 0.600 | Beta(79, 53) | 0.514 to 0.680 | 0.049 | 22.5% | 24.1% |
| B | 61 / 90 | 0.678 | Beta(62, 30) | 0.576 to 0.766 | 0.588 | 39.4% | 31.1% |
| C | 55 / 90 | 0.611 | Beta(56, 36) | 0.508 to 0.706 | 0.100 | 15.0% | 17.9% |
| D | 58 / 90 | 0.644 | Beta(59, 33) | 0.541 to 0.736 | 0.262 | 23.1% | 26.9% |

Check two shares by hand. Thompson, B: $0.10 + 0.5 \times 0.588 = 0.394$, or 39.4%. A: $0.20 + 0.5 \times 0.049 = 0.2245$, or 22.5%. For exploration sampling, the $p(1-p)$ values are $0.047, 0.242, 0.090, 0.193$, summing to $0.572$; B's weight is $0.242/0.572 = 0.423$, so its share is $0.10 + 0.5 \times 0.423 = 31.1\%$. Exploration sampling gives B less than Thompson does and gives D, the runner-up, more.

Note that all four credible intervals still overlap heavily. The design doesn't wait for them to separate; it shifts parents gradually, in proportion to the evidence.

**After week 2** (cumulative; these shape week 4):

| Wording | On time / sent | Rate | Posterior | 95% credible interval | P(best) | Thompson share | Exploration share |
|---|---|---|---|---|---|---|---|
| A | 158 / 260 | 0.608 | Beta(159, 103) | 0.547 to 0.665 | 0.029 | 21.4% | 24.0% |
| B | 123 / 180 | 0.683 | Beta(124, 58) | 0.612 to 0.747 | 0.791 | 49.5% | 33.5% |
| C | 109 / 180 | 0.606 | Beta(110, 72) | 0.533 to 0.674 | 0.039 | 12.0% | 15.4% |
| D | 114 / 180 | 0.633 | Beta(115, 67) | 0.561 to 0.701 | 0.141 | 17.0% | 27.2% |

Under Thompson sampling B now gets nearly half the parents (198 of 400). Under exploration sampling the two contenders, B and D, get 134 and 109.

P(B best) rose from 0.588 to 0.791 as the data doubled. It has not reached 0.95, so the experiment continues. Separately, P(B beats A) is now 0.947: B is very probably better than the current message, even though it is not yet clear that it beats D.

### The stopping rule

Agreed before week 1, as the case requires:

- **Stop early** when one wording is at least **95% likely to be best**. From then on, every parent gets that wording.
- **Otherwise stop at 10 weeks** (4,000 parents) and decide from the data in hand. The code's rule at the cap: take a wording that is 95% likely best; failing that, switch to the leading wording only if it is at least 95% likely to beat A; otherwise **"no clear winner, keep A."**

The second test at the cap is a small refinement of the case's rule: it lets the program adopt a wording that is clearly better than the current message even when two challengers can't be separated from each other.

---

## Scaling Up – Ten Weeks, 4,000 Parents, One Spreadsheet

### The Monday routine

The case's field pathway needs nothing the analyst doesn't already have:

1. Paste last week's newly complete outcomes (wording sent, vaccinated within 7 days yes/no), only for parents whose due date passed at least 7 days ago and whose records are entered.
2. The spreadsheet adds them to four running totals of on-time and late, giving Beta($1 + s$, $1 + f$) per wording.
3. It estimates P(best) by simulation: 10,000 rows, each drawing `=BETA.INV(RAND(), a, b)` for the four wordings and recording which is highest. The share of rows each wording wins is its P(best). (In R, `rbeta` does the same in one line.)
4. Apply the guards, check the stopping rule, and randomly assign this week's 400 parents in the resulting shares.
5. Upload the file to the bulk-SMS platform. Clinic staff see nothing different.

If the analyst is away, the written fallback is to send the current shares unchanged. Because of the delay, weeks 1 and 2 always go out at the starting shares, and the first stopping check is before week 3.

### Groups

The best wording might differ between first-time and returning parents. Running a separate experiment per group halves the data in each, so the case starts with one group and splits only if numbers allow.

### What the field evidence says

- **Kasy and Sautmann (Econometrica, 2021)** introduced exploration sampling and applied it to recruitment strategies for an agricultural extension service in Odisha, India. It is a different domain, but the same structure: several outreach options, outcomes within weeks, assignment shifted between waves.
- **Caria et al. (Journal of the European Economic Association, 2024)** ran an adaptive targeted field experiment on job-search assistance for refugees in Jordan, funded by the International Rescue Committee. It shows a real organization can run adaptive assignment wave by wave. Its honest lesson: the targeting algorithm's gain was **small, about 1 percentage point of employment**. An adaptive design mainly avoids waste while learning; it does not make a weak option strong.
- **Xu et al. (AAAI, 2021)** on LIZARD is a bandit method for planning patrol effort, **evaluated on historical poaching data from Cambodia**, not run in the field. It is a distant parallel at most.

### When a fixed randomized trial is still better

A fixed equal split is the right choice, not a failure, when:

- **A donor or the ministry needs a clean, precise effect estimate for every wording.** Adaptive designs give the weaker wordings fewer parents, so their estimates are less precise. The floor limits this but doesn't remove it. In the simulation below, wording C's 95% margin of error at the decision is ±0.043 under Thompson sampling against ±0.032 under the equal split.
- **Outcomes arrive slower than decisions.** If records took two months, there would be few chances to adapt within 10 weeks.
- **The team can't run the weekly routine reliably.** A fixed design that is carried out beats an adaptive one that is not.

Say which you are choosing, and why. The case asks for exactly that.

---

## Code Implementation & Simulation

The full program is [`code/case9_thompson_sampling.py`](code/case9_thompson_sampling.py). It needs only `numpy`:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case9_thompson_sampling.py
```

### The probability each wording is best

```python
def prob_best(succ, fail):
    w, cdf = posterior_grid(succ, fail)     # each Beta posterior on a grid of 2,000 rates
    out = []
    for k in range(4):
        others = np.prod(np.delete(cdf, k, axis=-2), axis=-2)   # P(all others below x)
        out.append((w[..., k, :] * others).sum(axis=-1))        # sum over x of P(k at x) x that
    p = np.stack(out, axis=-1)
    return p / p.sum(axis=-1, keepdims=True)
```

This is Step 5 of [From Outcomes to Estimates](#from-outcomes-to-estimates--beta-posteriors-for-on-time-rates), computed on a grid instead of with random draws, so the output is the same on every run.

### The two assignment rules and the guards

```python
def exploration_weights(p_best):
    q = p_best * (1 - p_best)
    return q / q.sum(axis=-1, keepdims=True)

def shares_with_guards(weights):
    return FLOOR + ADAPTIVE * weights      # FLOOR = (0.20, 0.10, 0.10, 0.10), ADAPTIVE = 0.5
```

For Thompson sampling the weights are just `p_best`.

### Simulation: three designs, 2,000 ten-week experiments

The code fixes the true rates at A = 0.60, B = 0.67, C = 0.62, D = 0.64, then runs each design 2,000 times with fresh random outcomes, 400 parents a week and the two-week delay:

- **Equal split:** 25% to each wording for all 10 weeks, then the cap rule.
- **Thompson + guards:** Thompson shares with the 20% control and 10% floors, and the stopping rule.
- **Exploration sampling + guards:** the same, with exploration-sampling weights.

After the experiment, the chosen wording goes to everyone; the code also counts a 26-week season (10,400 parents) to show what the final choice is worth.

```
Simulation 1 - wordings differ (B is best)
  benchmarks over 10 weeks (4,000 parents): all-A = 2,400 on time,  all-best = 2,680,  equal split = 2,530
  design                          on-time,10wk  extra vs equal  on-time,26wk  extra vs equal  pick best  keep A  stop<10wk  mean weeks
  equal split 25% each                 2,530            +0         6,773            +0      85.4%    6.3%      0.0%       10.0
  Thompson + guards                    2,569           +39         6,823           +50      88.4%    4.3%     37.2%        8.4
  exploration sampling + guards        2,562           +32         6,816           +43      87.8%    3.6%     41.4%        8.3
  parents sent each wording over 10 weeks (average), and 95% CI half-width for wording C at the decision:
    equal split 25% each            A=1,000  B=1,000  C=1,000  D=1,000   C: +/-0.032
    Thompson + guards               A=824  B=1,790  C=599  D=787   C: +/-0.043
    exploration sampling + guards   A=841  B=1,619  C=663  D=878   C: +/-0.041
```

"On-time" counts are expected vaccinations (true rate × parents sent), averaged over the 2,000 runs. "Mean weeks" is how many weeks ran with experimental shares before stopping.

### What the results say

- **Adaptive designs vaccinate more children on time during the experiment.** Thompson sampling adds 39 on-time vaccinations over 10 weeks compared with the equal split, and 50 over the 26-week season. That is real but modest: about a quarter of the 150 the equal split gives up against an all-B oracle. The guards are why: half the parents are fixed at 20/10/10/10, so even with perfect knowledge a guarded design would reach only $400 \times (0.20 \times 0.60 + 0.10 \times (0.67 + 0.62 + 0.64) + 0.5 \times 0.67) \approx 259$ a week, not 268, until it stops.
- **They pick the right wording at least as often.** The equal split ends on B in 85.4% of runs, Thompson in 88.4%, exploration sampling in 87.8%. Most wrong picks are D, the close runner-up.
- **They often finish early.** Thompson stops before the 10-week cap in 37.2% of runs, after 8.4 weeks of experimenting on average.
- **Exploration sampling did not beat Thompson here.** It gave the runner-up more parents (D 878 against 787), but with the 50% guard and the stopping rule, the two rules end up close. Differences of a point or less between them are within simulation noise.
- **The price is precision on the weaker wordings.** C gets 599 parents under Thompson instead of 1,000, and its margin of error widens from ±0.032 to ±0.043. This is the cost named in [When a fixed randomized trial is still better](#when-a-fixed-randomized-trial-is-still-better).

### Two harder scenarios

The code reruns everything with no real difference (all four at 0.60) and with differences of 1–2 points (A 0.60, B 0.62, C 0.61, D 0.61):

```
Simulation 2 - no real difference (all four equal)
  equal split 25% each            A=87.8%  B=4.7%  C=3.7%  D=3.9%
  Thompson + guards               A=86.5%  B=5.2%  C=4.0%  D=4.2%
  exploration sampling + guards   A=85.9%  B=4.7%  C=4.6%  D=4.9%
Simulation 3 - small differences (B best by 1-2 points)
  equal split 25% each            A=68.3%  B=17.7%  C=7.2%  D=6.8%
  Thompson + guards               A=67.6%  B=19.6%  C=6.0%  D=6.8%
  exploration sampling + guards   A=65.2%  B=19.9%  C=7.8%  D=7.1%
```

These rows are the share of runs ending on each wording.

- **With no real difference, the rule keeps A most of the time, but not 95% of the time.** Thompson switches away from A in $100\% - 86.5\% = 13.5\%$ of runs. A 95% threshold, checked every week and across three challengers, gives more than 5% false alarms. Here a false switch costs nothing, since all wordings are equal; but if the switch had a cost, the threshold would need to be stricter.
- **With 1–2 point differences, the usual answer is "no clear winner, keep A".** All three designs keep A in about two thirds of runs and find B in under 20%, and the adaptive designs gain almost nothing (+2 on-time vaccinations over the season for Thompson). This is the case's warning: with about 4,000 parents, wordings that differ by a point or two may never separate. The experiment is still worth running, because it tells the team that no wording is much better than A.

### The simpler alternative: an equal split, then switch

The equal split is itself the simple option: four wordings, 100 parents each a week, a spreadsheet of on-time counts, and after 10 weeks a comparison of the four rates with their margins of error. It is how most organizations already test messages. How close does it come?

| Scenario | Equal split, on time over the season | Thompson + guards | Equal split picks the best | Thompson picks the best |
|---|---|---|---|---|
| Wordings differ (B best by 7 points) | 6,773 | 6,823 (+50) | 85.4% | 88.4% |
| Small differences (1–2 points) | 6,312 | 6,313 (+2) | 17.7% | 19.6% |
| No difference | 6,240 | 6,240 (+0) | n/a | n/a |

- **Close on the final choice.** It picks the best wording nearly as often as the adaptive designs in every scenario. Most of what the experiment is worth comes from switching everyone to the winner afterwards, and both designs do that.
- **Less close during the experiment, when one option is much better.** The adaptive design's extra 50 on-time vaccinations come from moving parents off weak wordings while the test runs. With small or no differences, there is nothing to gain.
- **Better on the evidence.** Fixed shares give every wording the same sample and a narrower margin of error (±0.032 for C, against ±0.043 under Thompson), and the usual difference-in-means and confidence intervals are valid. Adaptive designs need adjusted methods for that (Hadad and colleagues, PNAS, 2021). A donor asking "how much better is B, and how sure are you?" is better served by the equal split.

What to check before settling for it: a few options (two to four), not dozens, where an equal split spreads too thin; a test short enough that serving the weaker wordings for 10 weeks costs little; and outcomes that arrive weekly, so a fixed end date is natural. If there are many options, or one option may be clearly harmful, or the test must run for a long season, the adaptive design earns its complexity.

Two cautions. The true rates are invented to teach the method; the real gain depends on how different the wordings really are, which is what the experiment finds out. And the simulation assumes the outcome records are complete and correctly matched to phone numbers, which the case lists as the main practical friction.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Arms and outcome** | 4 wordings; on time within 7 days (yes/no) | Turns the reminder program into a four-armed bandit with a weekly batch of 400 |
| **Prior** | Beta(1, 1) | Starts every wording with an open mind, worth two imaginary parents |
| **Update** | Beta($1 + s$, $1 + f$) | Adds each week's on-time and late counts; uses only parents whose 7-day window has closed |
| **Credible interval** | middle 95% of the posterior | A range for each wording's rate; close to the usual confidence interval with this much data |
| **P(best)** | $\sum_x P(k \text{ at } x) \prod_{j \ne k} P(j < x)$ | The probability each wording is the best one; drives assignment and stopping |
| **Thompson sampling** | $w_k = $ P($k$ best) | Sends more parents to wordings that look better; most on-time vaccinations while learning |
| **Exploration sampling** | $w_k \propto p_k(1 - p_k)$ | Favors close contenders; aimed at picking the best at the end (Kasy & Sautmann) |
| **Guards** | share$_k$ = floor$_k$ + 0.5 $w_k$; floors 20/10/10/10 | Keeps A as a 20% control and every wording at 10% or more |
| **Stopping rule** | max P(best) ≥ 0.95, or 10 weeks | Ends the experiment on evidence or on schedule; "no clear winner, keep A" is an allowed ending |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/09-sms-reminders-adaptive-experiment.md#after-the-recommendation): write down the outcome, shares, floor, control and stopping rule before week 1, and test the weekly spreadsheet on last month's wording-A data. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) cover record matching and ethics approval; the [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) section explains why the adaptive experiment is itself the pilot.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section notes that no package is needed for Class 8; a statistician comfortable with basic Bayesian statistics can review the design.
- **Read** Caria et al. (2024) on the Jordan refugee experiment first, then Kasy & Sautmann (2021) for exploration sampling, both listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Other tutorials:** [restless bandits](01-restless-bandits-chw-visits.md) for when each person's situation changes week to week; [policy learning](08-policy-learning-business-grants.md) for using trial results to decide *who* should get which option; and [deciding without a model](06-no-model-food-pantry.md) for when a written rule is enough.
