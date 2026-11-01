# Policy Learning Masterclass: Which 600 Shopkeepers Should Get a Grant

*An in-depth walkthrough of treatment effects, subgroup estimates, learned targeting rules and held-out validation, built on [Case 8: Business grants for women shopkeepers](../cases/08-business-grants-effect-targeting.md).*

**You need:** proportions, means, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 7: Effect-Based Targeting](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting). **Code:** [`code/case8_policy_learning.py`](code/case8_policy_learning.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A women's enterprise NGO has money for **600 one-off grants**, each paired with a short business-training course, for women who run small shops. The goal is higher household income a year later. Last year it ran a randomized pilot: of **3,000 applicants**, some were offered the grant by lottery and the rest were not, and income was measured for both groups a year later. This year's call is open, applications come in through a phone app, and the question is **which 600 applicants to fund**.

The usual answer is to rank applicants by poverty and fund the poorest 600. It fails in two ways. The pilot showed big income gains for women whose shops had been open two years or more, and little for very new businesses; the poorest applicants are mostly the new businesses, so the same money buys much less income. And the ranking uses self-reported income, which applicants have every reason to understate.

This tutorial builds the alternative step by step:

1. **[The Effect Leap](#the-effect-leap--from-who-needs-it-most-to-who-gains-most)** separates two questions people often blur: *how poor is she?* and *how much would the grant change her income?*
2. **[The Core Bottleneck](#the-core-bottleneck--nobody-is-both-funded-and-unfunded)** explains why that second question can't be answered for any one person, and why the pilot's lottery rescues us.
3. **[From Pilot Data to Estimates](#from-pilot-data-to-estimates--effects-intervals-and-subgroups)** estimates the average effect, the effect in each subgroup, and a simple model of who gains most, each with a margin of error.
4. **[The Decision Engine](#the-decision-engine--learning-a-short-rule)** learns a short, explainable rule, then checks it on half of the pilot it never saw.
5. **[Scaling Up](#scaling-up--600-grants-a-need-floor-gaming-and-a-new-pool)** applies the rule to this year's 600 grants, adds a floor for the poorest, and tests what happens when applicants game the rule or the pool changes.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all in code and compares five ways of choosing.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **fund the people the grant will change the most, not the people who look most in need, and prove it on data the rule never saw.**

---

## The Effect Leap – From Who Needs It Most to Who Gains Most

### Two different numbers

For each applicant there are two numbers worth knowing:

- **Her outcome level:** her household income a year from now. Low income means high need.
- **The treatment effect:** how much *higher* her income will be a year from now *because* she got the grant, compared with the income she would have had without it. "Treatment" is the statistician's word for the program, whatever it is.

These are different numbers, and they can point in opposite directions. A woman who opened her shop three months ago may be very poor, but if she doesn't yet have regular customers, extra stock sits on the shelf: her need is high and her effect is small. A woman whose shop has run for five years may be less poor, but a grant lets her buy in bulk at a lower price: her need is lower and her effect is large.

A poverty ranking sorts on the first number. A model that predicts "who will earn most next year" also sorts on the first number, from the other end: it picks women who would have done well anyway. **Only the second number tells you what the grant buys.**

### What "effect-based targeting" means

**Effect-based targeting**, also called **policy learning**, gives a limited program to the people it will change the most. A **policy** here just means a rule for deciding who gets the program, like "shops open two years or more, in town." Policy learning uses data from a randomized pilot to estimate how the effect varies across kinds of people, then picks the rule that is expected to produce the most total gain within the budget.

### Mapping it to the program

| Model term | In this program |
|---|---|
| Treatment | A one-off grant with business training |
| Outcome | Monthly household income a year after the grant (the code uses the change from application to a year later; see [Step 2](#step-2-a-confidence-interval-and-a-cheaper-one)) |
| Treatment effect | Extra monthly income caused by the grant |
| Characteristics | App fields known at application: location, shop age, what it sells, household size, income and assets |
| Pilot | Last year's 3,000 applicants, half offered the grant by lottery |
| Policy (rule) | A short checklist that decides who is funded |
| Budget | 600 grants |
| Need floor | A share of grants reserved for the poorest, judged by verifiable indicators |

The decision is made **once a year, with all applicants known** after the call closes. That places it in Class 7 rather than the waitlist models of Class 10. And the pilot shows the effect varies sharply by shop age, which is what moves it from need ranking ([Class 2](02-welfare-optimization-borehole-siting.md)) to effect-based targeting.

---

## The Core Bottleneck – Nobody Is Both Funded and Unfunded

### The missing number

Here is the difficulty. For any one woman, we only ever see **one** of her two possible futures. If she got the grant, we see her income with it, never her income without it. If she didn't, the reverse. Her personal effect is the difference between a number we saw and a number we can never see. Statisticians call the unseen one the **counterfactual**: what would have happened in the world that didn't occur.

So no data set, however large, contains anyone's individual effect. That sounds fatal. It isn't, thanks to the lottery.

### Why randomization rescues us

In the pilot, a lottery decided who was offered the grant. A lottery doesn't care whether a shop is old or new, urban or rural, run by a hard worker or not. So the offered group and the not-offered group are, on average, **alike in every way, measured or not**, except for the grant. Any difference in their average income a year later must be caused by the grant (plus chance, which a confidence interval handles).

The same logic holds inside any subgroup defined by characteristics recorded *before* the lottery. Among women with shops open two years or more, the lottery still split them at random, so comparing offered and not-offered women in that subgroup estimates the effect *for that subgroup*. That is the whole trick: **we can't see one woman's effect, but we can see the average effect for any group of similar women.**

Two rules follow. First, the rule may only use characteristics recorded **before** the lottery: anything measured afterwards may itself have been changed by the grant. Second, without a lottery (say, if staff had picked who got grants last year), the funded and unfunded would differ in ways we can't see, and none of this would be trustworthy.

### Two more problems for later

- **Gaming.** The interview says applicants may exaggerate how poor they are. Any rule built on something applicants can change will be gamed once it is known. [Scaling Up](#scaling-up--600-grants-a-need-floor-gaming-and-a-new-pool) tests this.
- **A changing pool.** This year's applicants may not look like last year's. A rule learned on one pool can lose value on another. [Scaling Up](#scaling-up--600-grants-a-need-floor-gaming-and-a-new-pool) tests this too.

---

## From Pilot Data to Estimates – Effects, Intervals and Subgroups

The program in [Code Implementation & Simulation](#code-implementation--simulation) generates an illustrative pilot that matches the case: 3,000 applicants, exactly 1,500 offered the grant by lottery. 1,138 of them (38%) had shops open less than two years. Money is in illustrative dollars per month.

### Step 1: The average effect is a difference in means

The **average treatment effect** is the average, over everyone, of how much the grant raises income. With a lottery, it is estimated by the simplest formula in statistics:

$$
\widehat{\text{effect}} = \bar y_{\text{offered}} - \bar y_{\text{not offered}}
$$

In the pilot, mean income a year later was **$288.0** for the offered group and **$266.5** for the rest: an average effect of **$21.5 a month**.

### Step 2: A confidence interval, and a cheaper one

The margin of error for a difference of two independent means is

$$
\text{SE} = \sqrt{\frac{s_1^2}{n_1} + \frac{s_0^2}{n_0}}, \qquad \text{95\% CI} = \widehat{\text{effect}} \pm 1.96 \times \text{SE},
$$

where $s_1, s_0$ are the standard deviations and $n_1, n_0$ the group sizes. For income a year later this gives **$14.4 to $28.5**.

A simple improvement narrows it. Incomes differ a lot between women for reasons that have nothing to do with the grant: a market-town shop earns more than a village one. That variation is noise for our purpose. The app recorded each woman's income at application, before the lottery, so we can measure the outcome as the **change** in income instead: income a year later minus income at application. Subtracting a number fixed before the lottery can't bias the comparison, but it removes much of the noise. Measured as the change, the average effect is **$23.3, with a 95% interval of $18.7 to $27.8**: about two-thirds as wide. The rest of this tutorial uses the change.

### Step 3: Effects by subgroup

Now the same calculation inside subgroups. These are the **heterogeneous treatment effects**: "heterogeneous" just means "varying."

| Subgroup | Effect ($/month) | 95% CI | Offered + not offered |
|---|---|---|---|
| Shop open < 2 years | 2.9 | −4.1 to 10.0 | 563 + 575 |
| Shop open ≥ 2 years | **35.3** | 29.7 to 41.0 | 937 + 925 |
| Rural | 17.2 | 11.2 to 23.2 | 824 + 815 |
| Urban | 30.6 | 23.8 to 37.5 | 676 + 685 |
| Sells food | 28.3 | 21.9 to 34.7 | 716 + 731 |
| Sells other goods | 18.5 | 12.2 to 24.9 | 784 + 769 |
| Poorest 20% by income | 10.8 | 1.0 to 20.6 | 303 + 307 |
| Other 80% | 26.4 | 21.3 to 31.5 | 1,197 + 1,193 |
| ≥ 2 years and urban | **44.9** | 36.4 to 53.4 | 431 + 421 |
| ≥ 2 years and rural | 27.2 | 19.7 to 34.6 | 506 + 504 |

Three lessons:

- **Shop age matters most.** New shops gain almost nothing (the interval includes zero); established shops gain about $35. That matches what the NGO saw in its pilot.
- **Need and effect point opposite ways.** The poorest 20% gain only $10.8, because 78% of them run shops under two years old. Their *income level* a year later is also lower: among offered women, $217 for new shops versus $331 for established ones. A need ranking would send most grants to the group the grant helps least.
- **Beware lucky subgroups.** Food sellers seem to gain $9.8 more than other sellers, and the intervals barely overlap. But this is a simulation, and in it the true effect **does not depend on what the shop sells at all**. The gap is chance. Look at ten subgroups and, by luck alone, one or two will look different. Only differences that are large, make sense, and survive a check on fresh data ([The Decision Engine](#the-decision-engine--learning-a-short-rule)) should drive a rule. With 3,000 applicants, only big, simple differences like shop age can be estimated reliably.

### Step 4: A simple model of who gains most

Subgroup tables get unwieldy beyond two characteristics. A model can look at all of them at once. The simplest is a **T-learner** ("T" for two): fit one model predicting the outcome for offered women, a second for women not offered, and take the difference of the two predictions as each applicant's estimated effect. Here each model is an ordinary linear regression, fitted on half of the pilot (the other half is kept back, as [The Decision Engine](#the-decision-engine--learning-a-short-rule) explains). The difference of the two sets of coefficients reads as "how the effect changes with each characteristic":

| Characteristic | Change in estimated effect |
|---|---|
| Shop age, per year | +3.38 |
| Urban | +10.17 |
| Sells food | +12.28 |
| Household size, per person | +0.58 |
| Income, per $100 | +7.38 |

It finds the urban gap and that older shops gain more. But a straight line can't show that the effect *jumps* at about two years; it spreads that jump across all ages and partly blames income, which rises with shop age. It also picks up the lucky food gap from Step 3.

A **causal forest** (Wager & Athey, 2018) is the more flexible tool. It grows many small decision trees, each splitting applicants into groups whose effects differ most, and averages them. It finds jumps and interactions on its own and comes with confidence intervals. In R, the analyst's language, it is one call in the [grf](https://cran.r-project.org/package=grf) package. This tutorial sticks to subgroups and the T-learner so every step can be checked by hand, but the logic of everything that follows is the same.

---

## The Decision Engine – Learning a Short Rule

Staff can't apply a forest or a regression at the counter, and applicants who are turned down deserve a reason. So the final product is a **short rule**: a decision tree of one or two questions, written as a checklist. **Empirical welfare maximization** (Kitagawa & Tetenov, 2018) and **policy learning** (Athey & Wager, 2021) are the formal versions of the idea: among all rules of a simple form, pick the one with the largest estimated total gain.

### Step-by-step concrete example: 8 applicants

Eight pilot applicants, four offered by lottery. The outcome is the change in monthly income.

| Applicant | Shop age (years) | Offered? | Change in income ($) |
|---|---|---|---|
| 1 | 0.5 | yes | 12 |
| 2 | 1.0 | no | 8 |
| 3 | 3.0 | yes | 70 |
| 4 | 4.0 | no | 25 |
| 5 | 0.8 | no | 10 |
| 6 | 1.5 | yes | 15 |
| 7 | 5.0 | yes | 60 |
| 8 | 2.5 | no | 20 |

**Average effect.** Offered mean $(12 + 70 + 15 + 60)/4 = 39.25$; not-offered mean $(8 + 25 + 10 + 20)/4 = 15.75$. Effect: **$23.50**.

**One question: "Has the shop been open 2 years or more?"** That splits the eight into two groups.

- No (applicants 1, 2, 5, 6): offered mean $(12 + 15)/2 = 13.50$, not offered $(8 + 10)/2 = 9.00$. Effect **$4.50**.
- Yes (applicants 3, 4, 7, 8): offered mean $(70 + 60)/2 = 65.00$, not offered $(25 + 20)/2 = 22.50$. Effect **$42.50**.

With a budget for four grants, the rule "fund shops open 2 years or more" expects $4 \times 42.50 = \$170$ a month of extra income. A rule that funds the four newest (and probably poorest) shops expects $4 \times 4.50 = \$18$. Learning a rule means doing this for every candidate question and keeping the best.

### Checking a rule fairly: inverse-probability weighting

How do we estimate the value of a rule on pilot data, when the rule picks people the lottery may or may not have funded? Use **inverse-probability weighting (IPW)**. Each applicant had a known 50% chance of being offered. So each offered person stands in for $1/0.5 = 2$ people like her "if everyone got it," and each person not offered stands in for 2 "if nobody did." Give each picked applicant a score:

$$
\text{score}_i = \frac{\text{offered}_i}{0.5}\, y_i \;-\; \frac{1 - \text{offered}_i}{0.5}\, y_i
$$

that is, $+2y$ if offered and $-2y$ if not. The average score over the people a rule picks is an **unbiased** estimate of the effect among them: right on average, because the lottery, not the rule, decided who was offered. For "shop open 2 years or more," the scores are $140, -50, 120, -40$; their sum is 170, and $170/4 = \mathbf{42.50}$, the same as the difference in means. When the counts of offered and not offered among the picked aren't exactly equal, the two differ slightly; the code uses the version that rescales the weights within each group, which is exactly "offered mean minus not-offered mean among the picked" and is less noisy.

### Learning the rule on half the pilot

The code splits the pilot at random into a **training half** (1,500 applicants) to learn from and a **test half** (1,500) held back. On the training half it tries every rule of one question, then every rule of two questions, using only fields that are **hard to fake**: shop age (checkable against a licence or the market committee), location, and what the shop sells. Self-reported income and assets are left out on purpose ([Scaling Up](#scaling-up--600-grants-a-need-floor-gaming-and-a-new-pool) shows why). That is 10 one-question rules and 34 two-question rules.

The budget changes what "best" means. 600 grants for 3,000 applicants is **20%**. A rule splits applicants into groups; the grants go to the group with the highest estimated effect first, then the next, with a lottery inside the last group reached. A rule is scored by the total estimated gain of filling 20% this way. Each group must contain at least 40 offered and 40 not-offered applicants, so no estimate rests on a handful of people.

| Rule | Groups' estimated effects ($/month) | Estimated gain per grant |
|---|---|---|
| Best one question: shop open ≥ 3 years? | yes 38.1; no 12.2 | 38.1 |
| Best two questions: shop open ≥ 2.5 years? then urban? | ≥ 2.5 & urban 50.2; ≥ 2.5 & rural 27.3; < 2.5 & urban 8.2; < 2.5 & rural 9.1 | **50.2** |

In the training half, the "≥ 2.5 years and urban" group holds 361 applicants, more than the 300 the 20% budget allows, so all grants go there, chosen by lottery within it. As a checklist:

> **Fund if the shop has been open at least 2½ years (verified) and is in town. If there are more such applicants than grants, draw lots among them.**

The search found 2.5 years rather than the true break at 2, because a half-pilot is noisy near the line; the cost is small, since few shops sit between 2 and 2.5 years.

### The held-out check

The rule was picked as the best of 34, so its estimate of $50.2 is probably lucky: the winner of any contest tends to have had a good day. This is the **winner's curse**, and it is why the case insists on checking the rule on data held back from fitting. On the test half, each rule funds 300 applicants (20%) and its value is estimated by IPW:

| Rule (test half, 300 funded) | Estimated gain per grant | 95% CI | True gain (simulation only) |
|---|---|---|---|
| Random lottery | 20.2 | 5.7 to 34.7 | 25.7 |
| Poorest first (reported income) | 12.6 | −1.6 to 26.7 | 10.7 |
| Effect rule, one question | 35.1 | 20.7 to 49.6 | 37.0 |
| **Effect rule, two questions** | **43.4** | **28.5 to 58.3** | 45.0 |
| T-learner ranking (linear) | 35.8 | 21.3 to 50.4 | 40.3 |
| Effect rule + need floor | 38.7 | 23.7 to 53.7 | 37.8 |

Read it this way:

- **The rule survives.** $43.4 on fresh data, down from the training estimate of $50.2: the winner's curse, measured. Its interval lies entirely above the poorest-first interval.
- **The intervals are wide**, about ±$15, because each rule's estimate rests on about 150 offered and 150 not-offered people. That is the honest price of holding back half a 3,000-person pilot. It is enough to tell a good rule from a poor one; not enough to rank two good ones.
- **The two-question rule beat the linear T-learner**, which can't see the jump at two years and also uses self-reported income. A short rule loses little here, because the real pattern is simple.

The "true gain" column exists only because the data are simulated; a real program sees only the estimates. Here they agree within their intervals, which is what an unbiased estimator promises.

---

## Scaling Up – 600 Grants, a Need Floor, Gaming and a New Pool

### This year's applicants

The code simulates 3,000 applicants for this year (the case gives no figure; 3,000 is illustrative) and funds 600 with each rule. The pool has shifted: **49%** of shops are under two years old (38% in the pilot) and **35%** are urban (45%). Because the data are synthetic, the code knows each applicant's true effect and reports what each rule really delivers:

| Rule (600 grants) | Gain per grant ($/month) | Total extra income ($/month) | Share in the poorest 20% | Share new shops |
|---|---|---|---|---|
| Random lottery | 20.1 | 12,080 | 23% | 50% |
| Poorest first | 8.5 | 5,090 | 100% | 87% |
| **Effect rule (two questions)** | **41.5** | **24,900** | 1% | 0% |
| T-learner ranking (linear) | 38.0 | 22,780 | 0% | 1% |
| Effect rule + need floor | 36.8 | 22,090 | 21% | 19% |

The effect rule produces $24{,}900 - 5{,}090 = \$19{,}810$ a month more household income than funding the poorest: **about 4.9 times as much** from the same 600 grants. Even a plain lottery beats the poverty ranking, because the ranking concentrates grants on new shops.

### The need floor

The table also shows the ethical cost: the effect rule turns away almost all of the very poorest. The case recommends a **need floor**: reserve a share of grants for the poorest applicants, judged by indicators that can be verified, and offer training alone or a later round to new businesses. The code reserves 120 of the 600 grants (20%) for the poorest by an asset score checked on a field visit, and gives the other 480 by the rule.

The floor costs $24{,}900 - 22{,}090 = \$2{,}810$ a month, **11.3%** of the gain, and lifts the poorest-20% share from 1% to 21%. Like the fairness rules in the [borehole tutorial](02-welfare-optimization-borehole-siting.md), the size of the floor is a value judgment for the board and funder. The case's advice is to agree it **before** seeing results, so no one tunes it to favor particular applicants.

### Gaming: build the rule from what can't be faked

Filter 3 warns that applicants may exaggerate how poor they are. The code tests two kinds of gaming.

**Under-reported income.** If 30% of applicants report 40% less income than they have, the poorest-first ranking is captured by them: under-reporters get **73%** of the grants although they are 30% of applicants, and only **58%** of grants reach the truly poorest 20%, down from 100%. The ranking rewards exactly the behavior it should discourage. This is why self-reported income and assets are kept out of the rule, and why the need floor uses a field-verified asset score instead.

**Inflated shop age.** Once it is known that shops open 2½ years or more are funded, some newer shops will claim to be older. If 40% of owners of shops under two years old claim 2–3 years and nobody checks, **21%** of grants go to new shops, and the gain per grant falls from **$41.5 to $36.3** ($24,900 to $21,800 a month). Checking shop age against a licence or the market committee before paying removes the loss. Björkegren, Blumenstock & Knight (arXiv 2020) document this behavior change in a field experiment in Nairobi: people shifted their behavior once a scoring rule was in use, and they design rules that hold up better. A revised version is reported as accepted at the American Economic Review (unverified; confirm before citing the journal).

The general lesson: **prefer characteristics that are hard to fake and cheap to verify, and verify the ones the rule uses before paying.**

### A different pool from the pilot

A rule learned on last year's applicants is applied to this year's. That works only if the effect for a given kind of applicant is the same in both years, even if the mix of applicants differs. Here the mix shifted: the rule's best group (≥ 2.5 years, urban) is **24%** of the pilot but only **15%** of this year's pool, less than the 20% budget. So the rule must reach into its second group (≥ 2.5 years, rural), and the gain per grant drops from about $45 in the pilot-like test half to **$41.5**. The rule still works because it depends on who the applicant is, not on the mix.

Two checks belong in every rerun. Compare the share of this year's applicants in each of the rule's groups with the pilot's; a group that was rare in the pilot has a shaky estimate. And ask whether anything changed the program itself (a new region, a new trainer, a price shock), because then even the effect for a given kind of applicant may differ. Sahoo, Lei & Wager (2023) treat this problem formally: learning rules when the trial population differs from the one being served.

### The evidence, honestly

The closest real parallel is Athey, Keleher & Spiess (Journal of Econometrics, 2025). In a field experiment with more than 53,000 CUNY students, targeting a financial-aid renewal nudge by **estimated effect** beat targeting by **predicted need**. It is a parallel, not a deployment of business grants: the structural match is a limited offer, randomized data, and need-based versus effect-based targeting. No documented NGO deployment of a learned rule for business grants is known. The [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) section suggests how to generate that evidence: within this year's round, randomly assign applicants to selection by the learned rule or by the current need ranking, and compare income a year later per grant.

---

## Code Implementation & Simulation

The full program is [`code/case8_policy_learning.py`](code/case8_policy_learning.py). It needs only `numpy` and runs in well under a second:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case8_policy_learning.py
```

The true effect in the simulation is $5 a month for shops under two years old, $30 for older rural shops and $45 for older urban shops. The code never uses these numbers to choose; it only uses them to report the "true" columns.

### The effect estimate with its interval

```python
def diff_in_means(y, w):
    """Effect estimate with its 95% CI: mean(offered) - mean(not offered)."""
    y1, y0 = y[w == 1], y[w == 0]
    est = y1.mean() - y0.mean()
    se = np.sqrt(y1.var(ddof=1) / len(y1) + y0.var(ddof=1) / len(y0))
    return est, est - Z * se, est + Z * se, len(y1), len(y0)
```

This one function does all the estimation in the tutorial: the average effect, every subgroup, every group of a rule, and the held-out check (where it is the rescaled IPW estimate among the people a rule picks).

### Scoring a rule under the budget

```python
def budget_value(effects, sizes, share):
    order = np.argsort(effects)[::-1]            # best group first
    left, total, n = share * sizes.sum(), 0.0, sizes.sum()
    for k in order:
        take = min(left, sizes[k])               # lottery inside the last group reached
        total += take * effects[k]
        left -= take
    return total / n
```

`fit_rule` calls this for each of the 10 one-question and 34 two-question rules on the training half and keeps the best. The [policytree](https://cran.r-project.org/package=policytree) package in R does the same search more thoroughly: it allows a different second question on each branch, deeper trees, and uses corrected effect scores from a causal forest instead of raw group differences.

### Output

```
Learning a short rule on the training half (budget = 20% of applicants)
  best depth-1 rule: shop open >= 3 yrs  groups' effects=[38.1, 12.2]  estimated gain per grant=38.1
  best depth-2 rule: shop open >= 2.5 yrs / urban  groups' effects=[50.2, 27.3, 8.2, 9.1]  estimated gain per grant=50.2
  depth-2 group sizes in training half: [361, 415, 325, 399]

Held-out check - test half (1,500), each rule funds 300 (20%), IPW estimate
  random lottery                       20.2  (95% CI    5.7 to   34.7)  n=147+153  true= 25.7
  poorest first (reported income)      12.6  (95% CI   -1.6 to   26.7)  n=147+153  true= 10.7
  effect rule (depth 2)                43.4  (95% CI   28.5 to   58.3)  n=152+148  true= 45.0
  effect rule (depth 1)                35.1  (95% CI   20.7 to   49.6)  n=159+141  true= 37.0
  T-learner ranking (linear)           35.8  (95% CI   21.3 to   50.4)  n=155+145  true= 40.3
  effect rule + need floor             38.7  (95% CI   23.7 to   53.7)  n=148+152  true= 37.8
  (estimated gain on the training half was 50.2 per grant)

This year's applicants - 3,000, 600 grants (true effects known in simulation)
  shops under 2 years: pilot 38%, this year 49%; urban: pilot 45%, this year 35%
  depth-2 group shares: pilot ['24%', '28%', '21%', '27%'], this year ['15%', '28%', '19%', '38%']
  random lottery                     gain/grant=$ 20.1  total=$ 12,080/month  poorest-20% share= 23%  new shops= 50%
  poorest first (reported income)    gain/grant=$  8.5  total=$  5,090/month  poorest-20% share=100%  new shops= 87%
  effect rule (depth 2)              gain/grant=$ 41.5  total=$ 24,900/month  poorest-20% share=  1%  new shops=  0%
  T-learner ranking (linear)         gain/grant=$ 38.0  total=$ 22,780/month  poorest-20% share=  0%  new shops=  1%
  effect rule + need floor           gain/grant=$ 36.8  total=$ 22,090/month  poorest-20% share= 21%  new shops= 19%
```

The program also prints the toy example, the pilot summary, the subgroup table, the T-learner coefficients and the two gaming tests quoted above.

### What the results say

- **Targeting the effect, not the need, roughly doubles to quintuples the income bought.** The two-question rule delivers about twice a lottery and 4.9 times the poverty ranking, with the same 600 grants.
- **The held-out check is not optional.** The training estimate ($50.2) overstated the rule's value; the test-half estimate ($43.4) was close to the truth ($45.0).
- **A two-question checklist loses nothing here** to a model that uses every field, because the true pattern is simple. A causal forest is still the right first step on real data, to find out whether the pattern *is* simple.
- **The floor and the gaming checks are where the real decisions sit.** A 20% need floor costs 11.3% of the gain; unverified shop ages would cost about 12%.

### The simpler alternative: a pivot table of the pilot

Most of what policy learning does here can be done with a pivot table. Split the pilot by one characteristic at a time (shop age bands, urban or rural, sells food), compute the difference in average income between offered and not offered within each group, and fund the group with the largest difference. That is the one-question rule, "shop open 3 years or more", and on the held-out half it delivers a true $37.0 per grant against $45.0 for the two-question rule, $25.7 for a lottery and $10.7 for poorest-first. One question captures about 60% of the two-question rule's advantage over a lottery; adding the second question in the pivot table (shop age, then urban or rural) captures all of it.

In what ways it is close, and what to check before settling for it:

- **It still needs the randomized pilot.** The pivot table saves the modeling, not the experiment. Without a lottery between offered and not-offered applicants, differences between groups are differences in who applied, not in what the grant did.
- **Close when the pattern is simple.** Here the true effect depends on two characteristics, so a two-way table finds it. If the effect depends on many characteristics in small ways, a table misses it and a causal forest earns its place. Run the forest once with a partner to learn which case you are in.
- **The held-out check is the part people skip.** Pick the groups on half the pilot and check them on the other half. Comparing many subgroups in one table guarantees that some look good by chance, which is why the training estimate here ($50.2) overstated the truth.
- **Keep the groups large and the questions verifiable.** A rule based on a group of 40 people or on an answer applicants can fake will not hold up when the program scales.

Two cautions. The applicants, effects and gaming rates are invented to teach the method; real gains depend on how sharply the real effect varies, which only the real pilot can show. And the outcome is income a year later, not five years later; a grant that pays off slowly for new shops would look worse here than it is.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Effect vs level** | effect $=$ income with grant $-$ income without | Separates "how poor" from "how much the grant helps" |
| **Randomization** | lottery makes offered and not-offered groups alike | The only reason a difference in means is a causal effect |
| **Average effect** | $\bar y_1 - \bar y_0 \pm 1.96\sqrt{s_1^2/n_1 + s_0^2/n_0}$ | Did the grant work overall, and how surely |
| **Subgroup effects** | the same formula inside each group | Shows who gains most; watch for lucky subgroups |
| **T-learner / causal forest** | effect $=$ model$_{\text{offered}}(x) -$ model$_{\text{not}}(x)$ | Estimates the effect for every kind of applicant at once |
| **Short rule** | best 1–2 question tree by gain under a 20% budget | A checklist staff can apply and explain |
| **Held-out check** | IPW: score $= \pm 2y$, averaged over those picked | An unbiased value for the rule on data it never saw |
| **Need floor** | reserve 120 of 600 grants by verified assets | Limits harm to the poorest at a known price |
| **Gaming check** | rule inputs only from hard-to-fake, verified fields | Keeps the rule's value once applicants know it |
| **Pool check** | compare group shares, pilot vs this year | Flags when a rule rests on groups rare in the pilot |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/08-business-grants-effect-targeting.md#after-the-recommendation): split the pilot and hold back a part for validation, list which app fields can be verified and drop the rest from the rule, and agree the need floor with the board and funder before seeing results. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) sections of the playbook cover the Class 7 specifics.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section lists the tools: grf and policytree in R suit the NGO's analyst; EconML is the Python alternative. Statistics Without Borders or a university economics department suits a trial-data problem.
- **Read** Athey, Keleher & Spiess (free at arXiv 2310.08672), then Athey & Wager (2021) on policy learning, Wager & Athey (2018) on causal forests and Kitagawa & Tetenov (2018) on empirical welfare maximization, listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact) with researchers to contact.
- **Other tutorials:** [welfare optimization](02-welfare-optimization-borehole-siting.md) for when there is no trial data and need is the right target; [adaptive experiments](09-adaptive-experiments-sms-reminders.md) for when outcomes arrive in weeks and you can learn while allocating; and [restless bandits](01-restless-bandits-chw-visits.md) for when the decision repeats every week as people's situations change.
