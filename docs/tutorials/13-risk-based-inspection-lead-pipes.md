# Risk-Based Inspection Masterclass: Which 300 Homes to Dig for Lead Pipes

*An in-depth walkthrough of risk scores, logistic regression, calibration and exploration with a random share, built on [Case 13: Finding lead service lines with a limited number of digs](../cases/13-lead-pipe-inspection.md).*

**You need:** proportions, probabilities, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection). **Code:** [`code/case13_risk_inspection.py`](code/case13_risk_inspection.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A children's environmental-health NGO in the fictional city of Millbrook works with the water utility to find **lead service lines**, the pipes that connect each home to the water main. About **20,000 older homes** might have one. The utility's records are incomplete, and the only sure way to check is to dig. Crews can dig **300 service lines this year**, about **25 a month**. The utility has the results of about **1,500 past digs**, lead and not lead, but most were chosen because a resident complained or a street was being repaved. One analyst can rerun a model once a month.

The usual answer is to keep doing what the crews have always done: dig where people complain and where streets are open anyway, or go back to the streets where lead was found before. It fails in two ways. It finds fewer lead pipes per dig than it could, because complaints and repaving are only loosely related to lead. And it never looks in neighborhoods where few people complain, which are often not the ones with the least lead.

This tutorial builds the alternative step by step:

1. **[The Inspection Leap](#the-inspection-leap--from-complaints-to-a-risk-ranking)** turns the question into a *risk ranking*: score every home by its chance of a lead line and dig the highest scores.
2. **[The Core Bottleneck](#the-core-bottleneck--past-digs-were-not-chosen-at-random)** names what makes this hard: the 1,500 past digs are not a fair sample of the city.
3. **[From Dig Records to Estimates](#from-dig-records-to-estimates--hit-rates-risk-scores-and-calibration)** puts a confidence interval on the hit rate, builds a risk model from house age, records and neighborhood, and checks whether its probabilities can be trusted.
4. **[The Decision Engine](#the-decision-engine--rank-dig-learn-repeat)** ranks homes under the budget, keeps a random share of digs, and updates the model every month.
5. **[Scaling Up](#scaling-up--20000-homes-one-analyst-monthly-reruns)** covers the full city, the equity check, and the limits of one analyst and an Excel sheet.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** compares four ways of choosing the 300 digs in a synthetic city.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **dig where lead is most likely, but keep a few digs random, because the model only learns about the places you look.**

---

## The Inspection Leap – From Complaints to a Risk Ranking

### Why "dig where we dug before" is the wrong rule

A dig doesn't help a household by itself. It answers a question: *is there a lead pipe under this home?* The value of a dig is the chance that the answer is yes, because a "yes" puts the home on the replacement list. So the question for each month is: **which 25 homes are most likely to have lead?**

Complaints and repaving answer a different question: *where is it convenient or requested to dig?* Re-digging the streets where lead was found before answers a third: *where have we already looked?* None of them is "where is lead likely?"

### Risk scores

A **risk score** is a number for each home: the estimated probability that it has a lead line. A home with a score of 0.8 is expected to have lead 8 times in 10 among homes like it. If you dig a set of homes, the **expected number of lead pipes found** is the sum of their scores, the same expected-value arithmetic as adding up coin-flip probabilities.

That makes the best rule simple, *if* the scores are right: **sort all undug homes by score and dig the top 25.** No other 25 homes have a larger expected total. This is called **risk-based inspection**, or **predictive inspection**.

The scores come from a **model**: a formula that turns what is known about a home before digging (when it was built, what the utility's records say, which neighborhood it is in) into a probability. The model is fitted to past digs, where both the features and the answer are known. Learning a formula from examples with known answers is called **supervised learning**; the known answer (lead or not) is the **label**.

### Mapping it to the program

| Model term | In this program |
|---|---|
| Unit | Each of the ~20,000 older homes that could have a lead service line |
| Hidden problem (the label) | A lead service line, on either side of the meter, found by digging |
| Features | Year built (property records), what the utility's records say (lead, not lead, or nothing), neighborhood |
| Training data | The ~1,500 past digs with results, logged in the crews' Excel sheet |
| Risk score | The model's probability of lead for each undug home |
| Budget | 300 digs this year, about 25 a month |
| Exploration share | A random share of each month's digs (the case says 10–20%; the code uses 4 of 25, 16%) |
| Update | The analyst refits the model once a month with the new results |

The problem is **hidden** (nobody knows until a crew digs), **budget-limited** (300 of 20,000) and **has records including negatives** (past digs that found nothing). Those are the three conditions for Class 12 in the [taxonomy](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection).

### Why not a security game, and why not fair shares

It is not [Class 3 (security games)](03-security-games-marine-patrols.md). Security games are for opponents who watch your patrols and move: poachers, illegal fishers. Pipes don't move and nobody hides them. Randomizing to stay unpredictable would only waste digs.

It is not [Class 2 (static targeting)](02-welfare-optimization-borehole-siting.md) either. Class 2 hands out a benefit fairly, like boreholes across districts. A dig isn't a benefit; it is a search. Spreading digs evenly across neighborhoods would dig many homes that almost certainly have copper. Fairness still matters here, but in a different form: the [equity check](#the-equity-check) asks whether any neighborhood with high risk is being skipped.

---

## The Core Bottleneck – Past Digs Were Not Chosen at Random

### Where the past digs went

The code builds a synthetic Millbrook with eight neighborhoods. Each home secretly has lead or not; the program knows the truth, the utility does not. It then simulates the 1,500 past digs the way the case describes: 60% following resident complaints and 40% following street repaving. Complaints are more common in some neighborhoods, and more common where there is lead (residents worried about their water).

| Neighborhood | Homes | Median year built | No utility record | True lead rate (hidden) | Past digs | Past hit rate |
|---|---|---|---|---|---|---|
| Old Town | 2,433 | 1915 | 32% | 0.54 | 326 | 0.68 |
| Northgate | 3,009 | 1935 | 15% | 0.19 | 392 | 0.29 |
| Westbury | 2,904 | 1940 | 15% | 0.12 | 324 | 0.12 |
| Riverside | 2,575 | 1925 | 31% | 0.36 | 214 | 0.53 |
| Eastfield | 2,557 | 1945 | 20% | 0.11 | 99 | 0.29 |
| Mill Hill | 2,380 | 1930 | 41% | 0.34 | 102 | 0.60 |
| Southbank | 2,143 | 1928 | 48% | 0.43 | 27 | 0.74 |
| Lowmoor | 1,999 | 1920 | 58% | 0.65 | 16 | 0.81 |

The whole city has **6,471 lead lines among 20,000 homes (0.324)**. Nobody at the utility can see that number; it is what the program hides.

Look at the "Past digs" column. Northgate and Westbury, with some of the *lowest* lead rates, got 392 and 324 digs. Lowmoor, with the *highest* rate, got 16. That is the case's warning made concrete: past digs follow who complains and which streets are open, not where lead is.

### Two kinds of bias

**Selection bias** means the homes you have data on differ systematically from the homes you want to learn about. Here it comes in two forms:

- **Where:** some neighborhoods were dug a lot, others hardly at all. With 16 digs, nobody can say much about Lowmoor.
- **Which homes:** inside every neighborhood, complaints pull digs toward homes that *do* have lead. That is why every past hit rate in the table is higher than the true rate: Eastfield's past digs found lead 29% of the time, but only 11% of its homes have it.

A model trained on these digs learns "where the utility chose to dig, and what it found there", not "where lead is." The case puts it plainly: re-digging the streets where lead was found before has the same flaw, because it only confirms what the crews already looked at.

### What a score actually predicts

Obermeyer and colleagues (Science, 2019) studied a widely used health algorithm that ranked patients by predicted health-care *costs*, as a stand-in for illness. Because less was spent on Black patients with the same level of illness, the score under-referred them for extra care. The lesson for any risk score: **check what the label really measures.** A score trained on "was dug" or "complained" is not a score for "has lead." Even a score trained on "found lead when dug" carries the selection of which homes were dug, as the next section shows.

---

## From Dig Records to Estimates – Hit Rates, Risk Scores and Calibration

### Step 1: The hit rate, with a confidence interval

The **hit rate** is the share of digs that found lead, a proportion. In the past digs: lead in **613 of 1,500**, so $\hat p = 0.409$. Its standard error is

$$
\text{SE} = \sqrt{\frac{\hat p\,(1 - \hat p)}{n}} = \sqrt{\frac{0.409 \times 0.591}{1500}} = 0.0127,
$$

and the 95% confidence interval is $0.409 \pm 1.96 \times 0.0127$: **0.384 to 0.434**.

Now multiply by 20,000 to estimate the city's lead lines: $0.409 \times 20{,}000 \approx 8{,}173$. The true number is 6,471. The estimate is about 1,700 too high, and the true city rate of 0.324 lies **far outside** the interval.

This is the most important statistics lesson in the tutorial. **A confidence interval measures the noise of random sampling, not the bias of how the sample was chosen.** With 1,500 digs, the interval is narrow; it tells you precisely what the hit rate is *among homes like the ones the utility chose to dig*. It says nothing about the rest of the city. Only a random sample gives an interval for the whole city, which is why the random share in [The Decision Engine](#the-decision-engine--rank-dig-learn-repeat) matters.

For small samples, such as a few dozen random digs, the code uses the **Wilson interval**, a version of the same interval that behaves better when $n$ is small or $\hat p$ is near 0 or 1. For 1,500 digs, the two versions agree to three decimals.

### Step 2: A risk model with logistic regression

A probability must lie between 0 and 1, but adding up feature effects can give any number. **Logistic regression** handles this in two steps. First it adds up a **score** $z$ from the features, each with a weight called a **coefficient**:

$$
z = b_0 + b_1 \times (\text{decades before 1940}) + b_2 \times [\text{record says lead}] + b_3 \times [\text{record says not lead}] + b_{\text{hood}}
$$

The square brackets are 1 if true and 0 if not; $b_{\text{hood}}$ is a separate coefficient for each neighborhood. Then it squeezes $z$ into a probability with the **logistic function**:

$$
\text{risk} = \frac{1}{1 + e^{-z}}
$$

A score of 0 gives 0.5; large positive scores approach 1; large negative ones approach 0.

The coefficients are chosen to make the past digs' actual results as likely as possible (**maximum likelihood**). The code does this with Newton's method, a standard way to find the top of a smooth curve by repeated small corrections, in about 15 lines of numpy. Fitted to the 1,500 past digs:

| Feature | Coefficient | Odds multiplied by |
|---|---|---|
| Intercept ($b_0$) | −0.46 | |
| Each decade built before 1940 | +0.58 | 1.79 |
| Record says lead | +1.55 | 4.71 |
| Record says not lead | −1.49 | 0.22 |
| Old Town | +0.19 | 1.21 |
| Westbury | −1.19 | 0.30 |
| Lowmoor | +0.59 | 1.81 |

(The code prints all eight neighborhoods.) The **odds** of lead are $p / (1-p)$; a probability of 0.5 is odds of 1, a probability of 0.8 is odds of 4. Each coefficient is the change in the log of the odds, so $e^{b}$ is what the odds are multiplied by. Read the second row as: **each decade older multiplies the odds of lead by 1.79.** The records help a lot, in both directions, but they are missing for 58% of Lowmoor's homes.

**Shrinkage.** Lowmoor's coefficient rests on 16 digs. Left alone, a handful of digs can produce a wild estimate. The code adds a **ridge penalty** to the neighborhood coefficients: a cost for moving them away from zero (the city average), so a neighborhood's estimate moves only as far as its data justify. With hundreds of digs the penalty barely matters; with 16 it pulls the estimate toward the average.

### Step 3: Three homes by hand

Take a home built in 1915 (2.5 decades before 1940), with no utility record, in Old Town:

$$
z = -0.46 + 0.58 \times 2.5 + 0.19 = 1.18, \qquad \text{risk} = \frac{1}{1 + e^{-1.18}} \approx 0.77
$$

The code, with unrounded coefficients, gets $z = +1.19$ and risk **0.767**.

| Home | Score $z$ | Risk |
|---|---|---|
| 1915, no record, Old Town | +1.19 | 0.767 |
| 1945, record says not lead, Westbury | −3.44 | 0.031 |
| 1920, no record, Lowmoor | +1.30 | 0.786 |

Check the second one: $-0.46 + 0.58 \times (-0.5) - 1.49 - 1.19 = -3.43$, risk about 0.03. A 1945 Westbury home recorded as copper is almost never worth a dig.

### Step 4: Calibration – can the probabilities be trusted?

A model is **calibrated** if, among homes it scores at about 0.3, about 30% really have lead. Ranking only needs the *order* of the scores to be right. But two things need the probabilities themselves: the expected number of finds (to plan replacements), and any estimate of the city's total.

To check calibration, group homes into bands by predicted risk and compare the average prediction in each band with the share that actually has lead:

| Predicted risk band | Homes | Mean predicted | Past digs in band: observed | All homes in band: observed (hidden) |
|---|---|---|---|---|
| 0.0–0.1 | 4,222 | 0.05 | 0.05 (385 digs) | 0.04 |
| 0.1–0.2 | 2,788 | 0.15 | 0.16 (205 digs) | 0.07 |
| 0.2–0.4 | 3,579 | 0.29 | 0.25 (234 digs) | 0.18 |
| 0.4–0.6 | 2,718 | 0.50 | 0.50 (173 digs) | 0.31 |
| 0.6–1.0 | 6,693 | 0.81 | 0.82 (503 digs) | 0.69 |

Checked against the past digs (the fourth column), the model looks almost perfect. Checked against the whole city (the last column, which only the simulation can see), **it predicts too high in every band above 0.1**, by as much as 0.19 in the middle. Added up over all homes, the model expects 8,458 lead lines; the truth is 6,471.

The reason is Step 1 again: the past digs over-represent homes with lead, so a model fitted to them learns inflated probabilities. **Checking a model on the same kind of selected data it was trained on can't reveal this.** The only honest check is on homes chosen at random. In practice, that means the random-share digs: the analyst compares the model's average prediction for those homes with the share that actually had lead.

The ordering survives better than the probabilities. For the 300 undug homes with the highest starting scores, the expected number of lead lines (the sum of their risks) is 293, and 289 actually have lead. At the very top of the list, the model is useful from day one.

---

## The Decision Engine – Rank, Dig, Learn, Repeat

### The monthly cycle

Once a month, the analyst:

1. **Appends** the crews' latest results to the dig sheet.
2. **Refits** the model on every dig so far: the 1,500 past digs plus this year's.
3. **Scores** every undug home.
4. **Takes the top 21** by risk, marked "risk-ranked."
5. **Draws 4 more at random** from the undug homes not on that list, marked "random check."
6. **Exports** the 25 addresses for the crews.

Choosing which homes to check partly so that the model learns more is called **active learning**: the model helps pick its own next examples. It is the same idea as the [Class 8 tutorial](09-adaptive-experiments-sms-reminders.md)'s *explore and exploit*: mostly use what you know, but spend a small, fixed share learning about what you don't. Here there are no program options to compare, so it stays a layer inside Class 12 rather than a Class 8 problem.

### Why keep a random share

A model that only digs its top-ranked homes only learns about top-ranked homes. If it underestimates a neighborhood, it never sends a crew there, so it never finds out. Random checks fix three things that ranking can't:

- **Blind spots.** Every undug home has some chance of being checked, so a neighborhood the model underrates eventually shows up in the results.
- **Calibration.** Random checks are the only digs on which the model's probabilities can be honestly tested ([Step 4](#step-4-calibration--can-the-probabilities-be-trusted)).
- **The city total.** A random sample gives an estimate of the remaining lead lines with a real confidence interval ([Step 1](#step-1-the-hit-rate-with-a-confidence-interval)).

### The cost of exploring, by hand

Random checks find less lead than ranked digs. In the simulated year of [Code Implementation & Simulation](#code-implementation--simulation), the 252 ranked digs found lead 241 times (95.6%), and the 48 random checks found lead 12 times (25%). Each random check therefore costs about $0.956 - 0.25 = 0.706$ expected finds, and 48 of them cost about $48 \times 0.706 \approx 34$. The model-only rule found exactly 34 more lead pipes that year (287 against 253). Over 30 synthetic cities the cost averages 30 pipes a year, about 10% of what the model-only rule finds.

That is the trade the utility and NGO must agree on *before* the first list goes out: about one lead pipe in ten found later, in exchange for knowing where the model is wrong and how many lead lines remain.

### Estimating the city's total from random checks

Every home is in one of two groups: those the utility *chose* to dig (past digs and ranked digs), whose status is known; and the rest, sampled by the random checks. So:

$$
\text{estimated total} = \text{lead found in chosen digs} + \hat p_{\text{random}} \times \text{homes not chosen}
$$

In the simulated year: $613 + 241 = 854$ lead lines found in chosen digs; $20{,}000 - 1{,}500 - 252 = 18{,}248$ homes not chosen; $\hat p_{\text{random}} = 12/48 = 0.25$. So the estimate is $854 + 0.25 \times 18{,}248 = 5{,}416$, with a 95% interval of **3,577 to 7,931** from the Wilson interval for 12 of 48. The truth, 6,471, is inside it. The interval is wide because 48 random digs is a small sample; it narrows as random checks accumulate year on year. Crucially, it is *honest*: across 30 synthetic cities it contained the truth in 28.

---

## Scaling Up – 20,000 Homes, One Analyst, Monthly Reruns

### The full-size problem is small for a computer

Fitting the model on about 1,800 digs and scoring 20,000 homes takes a fraction of a second. The program refits it 12 times a year for two rules, in 31 cities, in a few seconds. The case suggests scikit-learn, a free Python library, for the analyst's version; its logistic regression does exactly what the code's 15 lines do. The real constraints are not computing but data and people.

### The equity check

The **equity check** looks at each neighborhood's predicted risk, past digs, digs this year and lead found, side by side. For the model-plus-random rule at the end of the simulated year:

| Neighborhood | Mean predicted risk | Past digs | Digs this year | Lead found |
|---|---|---|---|---|
| Old Town | 0.63 | 326 | 90 | 79 |
| Northgate | 0.25 | 392 | 4 | 0 |
| Westbury | 0.13 | 324 | 7 | 1 |
| Riverside | 0.47 | 214 | 11 | 5 |
| Eastfield | 0.23 | 99 | 11 | 1 |
| Mill Hill | 0.52 | 102 | 23 | 20 |
| Southbank | 0.55 | 27 | 20 | 16 |
| Lowmoor | 0.75 | 16 | 134 | 131 |

Three things to look for each month:

- **High risk, few digs.** The case's harm measure: neighborhoods with high predicted risk but no digs. Here there are none; Lowmoor and Southbank, nearly ignored by past practice, get 154 of the 300 digs.
- **No digs at all.** A neighborhood with zero digs gets no new information. The model-only rule left 3 neighborhoods with no digs this year; the random share left none.
- **Predictions out of line with random checks.** Eastfield's predicted 0.23 is still about double its true rate (0.11, hidden). Its 1 lead pipe in 11 digs is a first hint; as random checks accumulate per neighborhood, the analyst can compare each neighborhood's predicted risk with its random-check hit rate.

A caution from the case's unknowns: if records are *worse* in poorer neighborhoods, the model may under-score them. In this simulated city, records are most often missing in Lowmoor and Southbank, and the complaint bias happened to push their scores up rather than down. A real city may not be so lucky, which is why the check is a monthly habit, not a one-off.

### Real-world limits

- **How each past dig was chosen.** The single most useful column the utility doesn't have. Add it now (complaint, repaving, other) and backfill what you can; it lets the analyst see the bias, and correct for it with methods such as weighting.
- **One analyst, monthly.** The monthly cycle is six steps in a script plus an Excel export. Daily updates would add little: 25 digs a month barely move the model in a day.
- **Explaining the list.** Crews and residents will ask why one street is dug and the next isn't. "Highest predicted risk" and "random check" are both short, true answers.
- **Finding faster than fixing.** Every find goes on a replacement list with a date, and high-risk and confirmed homes get filters and flushing guidance right away. A search that outpaces replacement still needs that interim protection.

---

## Code Implementation & Simulation

The full program is [`code/case13_risk_inspection.py`](code/case13_risk_inspection.py). It needs only `numpy`:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case13_risk_inspection.py
```

### Logistic regression in numpy

```python
def fit_logistic(X, y, ridge=RIDGE):
    penalty = np.zeros(X.shape[1])
    penalty[4:] = ridge                       # shrink only the neighborhood columns
    beta = np.zeros(X.shape[1])
    for _ in range(50):
        p = sigmoid(X @ beta)                 # current risk for every dug home
        grad = X.T @ (y - p) - penalty * beta # which way improves the fit
        hess = X.T @ (X * (p * (1 - p))[:, None]) + np.diag(penalty + 1e-9)
        step = np.linalg.solve(hess, grad)    # Newton's step
        beta += step
        if np.max(np.abs(step)) < 1e-8:
            break
    return beta
```

Each row of `X` is one home's features from [Step 2](#step-2-a-risk-model-with-logistic-regression); `y` is 1 for lead and 0 for not. Each round compares the current predictions `p` with the actual results and moves the coefficients toward a better fit.

### The monthly loop

```python
beta = fit_logistic(X[dug], city["lead"][dug].astype(float))   # monthly refit
risk = np.where(avail, sigmoid(X @ beta), -1.0)                # undug homes only
pick = np.argsort(-risk, kind="stable")[:21]                   # top 21 by risk
rest = avail.copy(); rest[pick] = False
rand = rng.choice(np.flatnonzero(rest), 4, replace=False)      # 4 random checks
```

### Simulation: four rules, 300 digs

The code runs one year (12 months of 25 digs) under four rules, starting from the same city and the same 1,500 past digs:

- **Current practice:** 60% of digs follow complaints, 40% follow repaving, as before.
- **Oldest first:** dig the oldest undug homes, a simple rule needing no model.
- **Model, no random:** dig the top 25 by risk each month, refitting monthly.
- **Model + random:** dig the top 21 by risk plus 4 random checks, refitting monthly.

For the city in the tables above:

```
One year in Millbrook - 300 digs (12 months x 25), four rules
  current practice  lead found 118/300 (39%)  neighborhoods with no digs: 0  estimated total 8,122
  oldest first      lead found 242/300 (81%)  neighborhoods with no digs: 1  estimated total 9,500
  model, no random  lead found 287/300 (96%)  neighborhoods with no digs: 3  estimated total 8,498
  model + random    lead found 253/300 (84%)  neighborhoods with no digs: 0  estimated total 5,416 (95% CI 3,577 to 7,931)
  true total: 6,471
```

Each rule's "estimated total" is the estimate it naturally produces: for current practice and oldest first, the hit rate of all digs so far times 20,000; for the model-only rule, lead found plus the model's summed risks for undug homes; for the random share, the formula in [The Decision Engine](#estimating-the-citys-total-from-random-checks).

One city could be lucky, so the code repeats the year in 30 synthetic cities, each with its own homes and past digs:

```
Average over 30 synthetic cities (each with its own past digs)
  rule               lead found per 300 (min-max)  hit rate  hoods w/o digs  Lowmoor digs  total estimate error (mean, typical size)
  current practice    120.8 (103-141)            40%        0.1            3.4         +1,752,  1,760
  oldest first        246.5 (235-260)            82%        1.3           70.7         +3,148,  3,153
  model, no random    289.6 (283-295)            97%        2.5          134.8         +1,748,  1,761
  model + random      259.3 (252-269)            86%        0.0          124.3           +209,  1,113
  model + random: 95% CI for the total contained the truth in 28 of 30 cities
```

"Typical size" is the root-mean-square error: roughly, how far off the estimate usually is.

### What the results say

- **Any sensible ranking beats current practice by a wide margin.** The model with a random share finds 259.3 lead pipes per 300 digs against 120.8, about 2.1 times as many. Even oldest-first finds 246.5. Most of the gain comes from no longer digging where people complain.
- **The model beats oldest-first** because it also uses the records and the neighborhood: 259.3 against 246.5 with the random share, 289.6 without.
- **The random share costs about 30 pipes a year** (259.3 against 289.6) and buys three things the model-only rule can't give: every neighborhood checked (0.0 neighborhoods without digs, against 2.5), a total estimate that is right on average (error +209 against +1,748), and an honest interval for it (28 of 30).
- **The selected rules over-estimate the total badly.** Current practice and the model-only rule are both about 1,750 too high; oldest-first, about 3,150. A replacement budget planned on those numbers would be wrong from the start.

Two cautions. The city, its neighborhoods and the way complaints follow lead are invented to teach the method; the real gain depends on how well age and records predict lead in Millbrook, which only a pilot shows. And the 30-city averages show how much one year can vary: a single city's estimate (5,416 here) can be more than 1,000 off, so report the interval, not just the number.

### What the evidence shows

The design is not new. Abernethy and colleagues (KDD 2018), *ActiveRemediation*, describe the search for lead service lines in Flint, Michigan, using predictive modeling to guide where to dig; read the paper for its results. Potash and colleagues (KDD 2015) worked with the Chicago Department of Public Health on predictive models to target lead-hazard inspections and prevent childhood lead poisoning. Carton and colleagues (KDD 2016) built a risk-ranking early-warning model with the Charlotte-Mecklenburg Police Department, a parallel in a different public agency. The closest parallel for the explore-and-target design is Eva (Bastani and colleagues, Nature 2021), which chose which travellers to test at Greek borders in 2020 and found about 1.85 times as many asymptomatic infections as random testing. That is a parallel in design (limited tests, learning as results arrive), not a forecast of what a lead-pipe model would achieve.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Hit rate** | $\hat p \pm 1.96\sqrt{\hat p(1-\hat p)/n}$ | Measures digs that found lead; the interval covers sampling noise, not selection bias |
| **Risk score** | $\text{risk} = 1 / (1 + e^{-z})$, $z = b_0 + \sum b_k x_k$ | One probability per home from year built, records and neighborhood |
| **Fitting** | maximum likelihood by Newton's method, ridge on neighborhoods | Learns the coefficients from past digs; shrinks thinly dug neighborhoods toward the average |
| **Calibration** | mean predicted vs observed, by risk band, **on random digs** | Shows whether the probabilities can be trusted; selected digs hide the problem |
| **Ranking** | dig the top $k$; expected finds $= \sum$ risk | 21 risk-ranked addresses a month |
| **Random share** | 4 of 25 digs at random (16%) | Finds blind spots, tests calibration, costs about 10% of finds |
| **Total estimate** | found in chosen digs $+ \hat p_{\text{random}} \times$ homes not chosen | Honest count of remaining lead lines, with an interval, for planning replacements |
| **Monthly update** | refit on all digs so far | Active learning at the pace one analyst can run |
| **Equity check** | per neighborhood: risk, past digs, digs, finds | Flags high-risk neighborhoods with no digs, and predictions out of line with random checks |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/13-lead-pipe-inspection.md#after-the-recommendation): clean the 1,500 past dig records, add a column for how each dig was chosen, join them to year built and neighborhood, and agree the random share, equity check, and replacement and filter plan before the first list goes out. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) sections of the playbook cover the Class 12 specifics: split the next 1–3 months of digs between the model's list and current practice, and compare lead found per dig.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section lists the tools and partners; DataKind, Statistics Without Borders or the Data Science for Social Good Fellowship fit a first model plus a handover to the analyst.
- **Read** Abernethy et al. (2018), free at [arXiv 1806.10692](https://arxiv.org/abs/1806.10692), then Potash et al. (2015) and Bastani et al. (2021), and Obermeyer et al. (2019) before trusting any score, all listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Other tutorials:** [adaptive experiments](09-adaptive-experiments-sms-reminders.md) for the explore-and-exploit idea when the choice is between program options; [security games](03-security-games-marine-patrols.md) for when the hidden problem moves to avoid you; and [welfare optimization](02-welfare-optimization-borehole-siting.md) for when the resource is a benefit to share fairly rather than a search.
