# Anticipatory Action Masterclass: When Should the Cash Go Out Before a Flood?

*An in-depth walkthrough of forecast triggers, the cost-loss rule and choosing a threshold that holds up when the record is thin, with a targeting list as the second layer, built on [Case 14: Cash before a river flood](../cases/14-anticipatory-cash-floods.md).*

**You need:** proportions, averages, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning), in its anticipatory-action form, with a [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) layer ([combination 4 + 2](../../prompt/knowledge/taxonomy.md#5-when-two-classes-combine)). **Code:** [`code/case14_flood_trigger.py`](code/case14_flood_trigger.py). Every number in this tutorial comes from running that file. The river, the twelve seasons, the forecast errors, the value of a transfer and the 40,000 households in it are made up for teaching.

---

## Executive Overview

A humanitarian NGO has **$500,000** for the coming monsoon: **$50 each for 10,000 households** out of 40,000 it surveyed in 2024. Last year it paid three weeks after the flood peak, by which time families had skipped meals and sold animals cheaply. A donor will now let it pay **before** the peak, on a forecast, if the rule is agreed in advance. The national service emails a 5-day forecast of the river level at the main gauge every morning. The NGO has twelve seasons of forecasts and actual levels, and **three severe floods** among them.

Two decisions follow, and they are not equally hard:

- **Who** gets the transfer is decided once, before the season, from the survey. It is a Class 2 problem, and it turns out to be close to a sorted spreadsheet.
- **When** to pay is decided on the day, from one number in the morning bulletin. Pay too early and the flood may not come; too late and it is last year again. This is the primary decision and the subject of most of this tutorial.

The usual answers both fail. Paying after the flood is safe and late. Paying as soon as any forecast reaches the danger level pays almost every year, mostly for floods that never become severe.

This tutorial builds the alternative step by step:

1. **[The Trigger Leap](#the-trigger-leap--from-paying-after-to-paying-on-a-forecast)** names the four things a trigger can do (hit, too soon, miss, false alarm) and the **cost-loss rule** that says how sure you must be before acting.
2. **[The Core Bottleneck](#the-core-bottleneck--three-floods-and-a-forecast-you-cant-fully-check)** shows why twelve seasons with three severe floods can't settle the question on their own.
3. **[From Twelve Seasons to Estimates](#from-twelve-seasons-to-estimates--the-record-and-its-margins)** turns the record into estimates with honest margins of error, and finds the break-even forecast by hand.
4. **[The Decision Engine](#the-decision-engine--three-ways-to-choose-the-threshold)** chooses the threshold three ways: a calculator table, the best average under a fitted forecast model, and the choice that is never far from best across every model the record can't rule out.
5. **[The Second Layer](#the-second-layer--choosing-the-10000)** chooses the 10,000 households, and shows why the integer program here is a sorted list.
6. **[Scaling Up](#scaling-up--the-trigger-card-lists-a-and-b-and-real-world-limits)** turns both into a trigger card and two lists.
7. **[Code Implementation & Simulation](#code-implementation--simulation)** tests every rule on 50,000 simulated monsoons under seven versions of the river, ending with **the simpler alternative**.
8. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **agree in advance how sure the forecast must be, and check that the answer survives the forecasts and floods your record doesn't contain.**

A word of honesty before we start. Anticipatory cash has field evidence of a kind most methods here lack. WFP sent mobile-money transfers to pre-registered households in Bangladesh about five days before the July 2020 flood peak, and recipients were 36% less likely to go a day without eating during the flood (Pople, Hill, Dercon & Brunckhorst, 2021; working-paper figure). OCHA and the CERF activated a pre-agreed trigger in Somalia in 2020, and GiveDirectly sent cash ahead of forecast floods in Kogi State, Nigeria, in 2024. What is *not* documented is how much a carefully chosen threshold gains over a reasonable one chosen by hand. The values in this tutorial are invented to show the method, not estimates from those programs.

---

## The Trigger Leap – From Paying After to Paying on a Forecast

### Two decisions, made at different times

1. **Before the season**, the NGO fixes **List A**, the 10,000 households, and sends it to the mobile-money provider, which needs it two days ahead. It also signs a **trigger card** with the donor: the forecast level that releases the money.
2. **During the season**, each morning, the country director reads one number, the 5-day forecast at the main gauge, and either releases the transfer or doesn't. The card allows **one release per season**. If no release has happened when a severe flood passes, List A is paid afterwards, as last year.

The river here rises in **three flood waves** each monsoon. Levels are measured in cm above the gauge's **danger level**; a wave that peaks at **+100 cm or more** is a **severe flood**.

### What a trigger can do

A threshold $T$ means: release on the first morning a forecast reaches $T$. Across a season, four things can happen:

| Outcome | What happened | Value of each transfer (illustrative) |
|---|---|---|
| **Hit** | The release came on the forecast of the first severe wave, before its peak | 1.00 |
| **Too soon** | It came on an earlier, smaller wave; the money was spent before the severe one | 0.30 |
| **Miss** | No release before the first severe peak; paid after it | 0.35 |
| **False alarm** | A release, and no severe flood all season | 0.10 |
| No release, no severe flood | The money goes back to the donor for another use | 0.35 |

The values are on one scale: **1 means a transfer that arrived before a severe peak**. The rest are invented but follow the case's logic. A late transfer is worth about a third of an early one (the Bangladesh study's finding is that timing matters; it doesn't give this number). A false alarm still helps a little in a moderate flood, but the money is gone. Money not spent goes back to the donor and is worth the same as a late payment.

These five numbers are **the most important inputs in the whole tutorial**, and they are not data. They are a judgment the donor, the district committee and the NGO should make together, before the season. Everything below shows how the threshold follows from them.

### The cost-loss rule

Suppose a morning forecast gives a chance $p$ that this wave will be severe. Compare the two choices:

| | Severe flood comes (chance $p$) | It doesn't (chance $1-p$) |
|---|---|---|
| **Release now** | 1.00 | 0.10 |
| **Wait** | 0.35 (paid late) | 0.35 (money returned) |

Releasing gains $1.00 - 0.35 = 0.65$ if the flood comes and loses $0.35 - 0.10 = 0.25$ if it doesn't. Release when the expected gain beats the expected loss:

$$p \times 0.65 > (1 - p) \times 0.25 \quad\Longleftrightarrow\quad p > \frac{0.25}{0.25 + 0.65} = 0.278$$

So **release when the chance of a severe flood is above about 28%.** This is the **cost-loss rule**, a standard way of deciding when a warning is worth acting on: act when the probability exceeds the cost of acting in vain divided by that cost plus the loss avoided. Two things follow:

- **You don't need to be sure.** With these values, a forecast that is right only one time in three is already worth acting on.
- **The values set the threshold.** If the committee judges a late payment worse (say a quarter of an early one rather than a third), the gain from acting grows, the break-even chance falls, and the threshold moves down. That is the right conversation to have; the method only makes it explicit.

The rule needs one thing the program doesn't have: a trustworthy $p$ for each forecast. That is where the record comes in, and where it runs short.

### Mapping it to the program

| Term | In this program |
|---|---|
| Trigger variable | The 5-day forecast of the peak at the main gauge, from the morning bulletin |
| Threshold $T$ | The forecast level that releases the money, in cm above danger level |
| Hit, too soon, miss, false alarm | What a threshold does in one season (table above) |
| Value | The average worth of the 10,000 transfers in a season, on the 0-to-1 scale above |
| Break-even chance | 0.278: release when $P(\text{severe}) > 0.278$ |
| Reserve | A share of the fund held back and paid after a severe flood, whatever the trigger does |
| List A (the layer) | The 10,000 households, chosen before the season |

### Why this method and not another

- **[Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) alone.** Choosing the 10,000 is real work, but a perfect list paid three weeks late is last year's program. The case's second-decision answer, "when to pay, that's the hardest part," is what makes the trigger primary.
- **A machine-learning flood model.** Fitting a model to twelve seasons means fitting to three severe floods. It would look accurate and say nothing reliable about the fourth. The national forecasting service already does the hydrology; the NGO's job is to decide what to do with its forecast.
- **[Class 9 (Routing)](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics).** The money moves by mobile phone. The 30% without accounts need cash points, an operations plan rather than a model.
- **The [cyclone tutorial's](04-robust-optimization-cyclone-prepositioning.md) stocking model.** Same class, different decision: there, how much to hold where, months ahead; here, when to act on a forecast, days ahead. The robustness idea is shared: plan against what the thin record can't rule out.

---

## The Core Bottleneck – Three Floods and a Forecast You Can't Fully Check

### Problem 1: Three severe seasons

The record has 12 seasons and 3 severe floods. The true share of severe seasons could be well below or well above 25%, and every count of hits and misses rests on three events.

### Problem 2: The forecast is checked mostly on ordinary waves

The record has 36 waves, and only 4 of them were severe. The forecast's errors on ordinary waves say little about how it behaves on the big ones, which are what the trigger is for. Hydrologists know that forecasts can under-predict extreme floods, when the river leaves its usual channel.

### Problem 3: Misses and false alarms pull in opposite directions

A lower threshold catches more floods and pays for more that never come. A higher one wastes less and misses more. No threshold avoids both; the values above decide the balance.

### What the method must do

1. Use the record for what it can say, with honest margins of error.
2. Choose a threshold that stays near the best across every version of the river and forecast that the record can't rule out, plus the cases experts warn about.
3. Show the donor what each choice costs in misses and false alarms, before the season.

---

## From Twelve Seasons to Estimates – The Record and Its Margins

### Step 1: The record

```
The record - twelve monsoons at the main gauge (cm above danger level)
  season   5-day forecasts (wave 1, 2, 3)   actual peaks (wave 1, 2, 3)   severe?
  2013       -51    -5  -110                  -18     4   -71
  2014       -12   -71   -21                   -9   -32    20
  2015        -2   -46    -4                  -61   -42   -19
  2016        94   -25    18                   23   -43    27
  2017       -82  -110   -52                  -78   -82   -80
  2018        14     6    60                   29   -42    76
  2019       -59  -109    -2                  -43   -92   -16
  2020       122    88   103                  121    52   125                yes
  2021       131    96   -25                  128    43   -13                yes
  2022        60   176    76                   49   134    64                yes
  2023       -12   -49   131                   12    18    65
  2024        35    91    43                   27    58    62
  forecast error (forecast - actual), 36 waves: mean=+2.8 cm, sd=32.8 cm
```

Read 2023 across: the third wave was forecast at +131 cm and peaked at +65. A trigger at +100 would have paid for a flood that never became severe. In 2022 the first wave was forecast at +60, the second at +176; it peaked at +134.

### Step 2: How often severe floods come

Three of twelve is 25%. With so few seasons, use the **Wilson interval**, which behaves well for small counts:

```
  severe seasons: 3 of 12 = 25%, 95% Wilson interval 9% to 53%
```

Anything from about one season in eleven to one in two fits the record. That range matters: in a wetter world triggers pay off more often; in a drier one, most releases are false alarms.

### Step 3: How good the forecast is

The **forecast error** is the forecast minus the actual peak. Over the 36 waves:

```
  forecast bias: +2.8 cm, 95% interval -7.9 to +13.6
  forecast error sd: 32.8 cm, 95% interval 26.6 to 42.8
  errors on the 4 severe waves alone: +1, -22, +4, +42
```

The bias interval uses the usual standard error ($32.8/\sqrt{36}$). The interval for the standard deviation comes from the chi-square distribution with 35 degrees of freedom; it is asymmetric because a spread can't be negative. The four severe-wave errors are too few to say whether the forecast behaves differently on big floods. Ask the forecasting service for its own verification statistics; it has far more than twelve seasons.

### Step 4: The break-even forecast, by hand

If the forecast says $f$ and its error is roughly normal with mean +2.8 and standard deviation 32.8, the chance that the actual peak reaches +100 is the chance that the error is at most $f - 100$:

$$P(\text{severe} \mid f) \approx \Phi\!\left(\frac{f - 100 - 2.8}{32.8}\right)$$

where $\Phi$ is the standard normal table (`NORM.S.DIST(z, TRUE)` in Excel). At $f = 84$: $z = (84 - 102.8)/32.8 = -0.57$, and $\Phi(-0.57) \approx 0.28$, the break-even chance. So, **taken at face value, a forecast of about +84 cm is already worth acting on.**

That calculation leaves out one thing: big waves are rare. A forecast of +84 is more often an ordinary wave forecast too high than a big wave forecast right, so the true chance behind it is lower than 0.28, and the threshold should be somewhat higher. Getting that correction right needs the full record, which is what the decision engine does.

---

## The Decision Engine – Three Ways to Choose the Threshold

### Way 1: The calculator table

For each candidate threshold, replay the twelve seasons and count what would have happened:

```
Decision engine - the calculator table over the twelve seasons
     T   fired  hits  too soon  missed  false alarms  value/season
     0       7     2         1       0             4         0.371
    20       7     2         1       0             4         0.371
    40       7     2         1       0             4         0.371
    60       7     2         1       0             4         0.371
    80       6     3         0       0             3         0.450
   100       4     3         0       0             1         0.492
   120       4     3         0       0             1         0.492
   140       1     1         0       2             0         0.404
   160       1     1         0       2             0         0.404
   180       0     0         0       3             0         0.350
  calculator choice (fewest misses + too-soon with <= 3 false alarms): T = 100  (the record can't tell apart: [100, 120])
```

Check the $T = 100$ row by hand. It fires in 2020 (wave 1, forecast +122, peak +121: a hit), 2021 (+131, peak +128: a hit), 2022 (wave 2, +176, peak +134: a hit) and 2023 (+131, peak +65: a false alarm). The other eight seasons have no release and no severe flood. Value per season:

$$\frac{3 \times 1.00 + 1 \times 0.10 + 8 \times 0.35}{12} = \frac{5.90}{12} = 0.492$$

The rule on the card: the donor accepts about one false alarm in four seasons (at most 3 in 12); among the thresholds that meet it, take the fewest misses and too-soon releases, then the fewest false alarms. **Thresholds of 100 and 120 have identical records.** Twelve seasons can't tell them apart; the program breaks the tie toward the lower one, because it gives more warning of a flood the record lacks. Keep that tie in mind: it matters later.

### Way 2: Best average under a fitted forecast model

The table uses each season's actual forecasts once. A fitted model asks what *would* happen over many seasons like these: resample the twelve seasons' actual peaks, add forecast errors drawn from the fitted normal distribution (mean +2.8, sd 32.8), and average each threshold's value over 20,000 such seasons:

```
  expected value under the fitted model: T=0:0.323  T=20:0.353  T=40:0.390  T=60:0.429  T=80:0.460  T=100:0.467  T=120:0.446  T=140:0.412  T=160:0.381  T=180:0.362
  expected-value choice: T = 100
```

This breaks the tie: 100 beats 120 (0.467 against 0.446) once forecast errors vary from season to season. It also confirms the hand calculation's direction: the best threshold sits above the face-value +84, because ordinary waves forecast too high are the main source of false alarms.

But the fitted model treats the record's climate and the fitted error as exact. They aren't.

### Way 3: Never far from the best, whatever the river turns out to be

Build a **planning set**: every combination the record can't rule out, plus what experts warn about.

- **Climate:** shift every peak so that the share of severe seasons sits at the Wilson bounds (9% and 53%), or leave it as recorded. That needs shifts of about −28 cm and +73 cm.
- **Forecast bias:** the bottom, middle and top of its interval (−7.9, +2.8, +13.6 cm).
- **Forecast spread:** the bottom, middle and top of its interval (26.6, 32.8, 42.8 cm).
- **Expert scenarios:** forecasts that fall short on big floods (by 40% of the peak above +50 cm), at the recorded climate and in the wettest one.

That is $3 \times 3 \times 3 = 27$ plausible models and 2 expert scenarios. For each model $k$, find the best threshold's value, $V_k^\ast$. A threshold's **regret** in that model is how far it falls short: $V_k^\ast - V_k(T)$. The robust choice minimizes the largest regret:

$$T_{\text{robust}} = \arg\min_T \; \max_k \; \big[\,V_k^\ast - V_k(T)\,\big]$$

```
  best threshold, model by model: ranges from T=60 to T=120
  largest shortfall from each model's best threshold (max regret): T=0:0.168  T=20:0.141  T=40:0.107  T=60:0.093  T=80:0.065  T=100:0.031  T=120:0.050  T=140:0.092  T=160:0.131  T=180:0.153
  robust choice (smallest max regret): T = 100
```

The best threshold moves from 60 to 120 depending on which plausible model is true, but **100 is never more than 0.031 below the best**, against 0.050 for 120 and 0.065 for 80. That is the robust answer's real contribution here: not a different threshold, but evidence that this one is safe across everything the record allows.

**Why regret and not the worst value?** The same output prints each threshold's worst value over the set:

```
  worst-case value over the set: T=0:0.270  T=20:0.304  T=40:0.337  T=60:0.366  T=80:0.384  T=100:0.380  T=120:0.365  T=140:0.354  T=160:0.351  T=180:0.350
```

The worst case is always the driest plausible river, where few floods come and nothing does much better than paying after. Maximizing the worst value lets that one world choose for all of them. Regret compares each threshold with what was possible *in the same world*, so every world has a say.

### The reserve

A reserve holds part of the fund back and pays it after a severe flood, whatever the trigger did. It protects against releasing too soon or for nothing. Here it costs more than it saves:

```
  robust T=100 with 10% reserve: max regret 0.045
  robust T=100 with 20% reserve: max regret 0.065
  robust T=100 with 30% reserve: max regret 0.084
```

With these values, the reserve turns some of the hits (worth 1.00) into late payments (0.35) to protect against too-soon releases (0.30) and false alarms (0.10), which are rarer. A reserve earns its place if a false alarm costs more than money, for example the donor's or the community's trust. That is a judgment for the card's signatories; the numbers show its price.

---

## The Second Layer – Choosing the 10,000

### The score: exposure times need

For each surveyed household, the program has:

- the village's height above the river (from an elevation map);
- the household's distance from the bank, and whether the house stands on a raised plinth (from the survey);
- two need markers: a child under 5, and no regular income.

The **exposure** of household $i$ is the chance its home floods in a severe flood, $\hat p_i$, from a flood-depth model of height, distance and plinth (in the program, a logistic formula standing in for an engineer's flood map). The **need** is $1 + \text{child} + \text{no income}$, from 1 to 3. The score is $\hat p_i \times \text{need}_i$.

The **floor**: each of the six areas gets at least 60% of its share of expected flooding, so that no area is left out because its villages sit slightly higher.

```
  households per area: [9000, 8000, 7000, 6500, 5500, 4000]  mean village height (m): [1.6, 1.3, 1.1, 0.9, 1.2, 0.6]
  expected flooded households in a severe flood, by area: [2397, 2550, 2619, 3003, 2117, 1956]  total=14,641
  floor: each area gets at least 60% of its share of expected flooding: [982, 1044, 1073, 1230, 867, 801]
```

### The integer program is a sorted list

Written as an integer program: $x_i = 1$ if household $i$ is on List A,

$$\max \sum_i \hat p_i\,\text{need}_i\, x_i \quad \text{s.t.} \quad \sum_i x_i = 10{,}000, \quad \sum_{i \in \text{area } a} x_i \ge \text{floor}_a, \quad x_i \in \{0, 1\}$$

Every household costs the same $50, so the best list is simply: fill each area's floor with its highest-scoring households, then take the highest scores overall. That is the [borehole tutorial's](02-welfare-optimization-borehole-siting.md#the-simpler-alternative-greedy-with-a-floor-in-a-spreadsheet) greedy-with-a-floor rule, and here it is exact:

```
  integer program: 40,000 yes/no variables, solved in 11.1s, score=12,892.5
  greedy with floor on the same score: score=12,892.5  households that differ: 0
```

(The solve time will vary by machine.) The optimization is not where the work is. The work is in the exposure score: whether the survey and the map say who will actually flood. Section 7 tests that.

### Why not target by predicted benefit

[Class 7](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) would target the households who gain most from early cash. That needs a trial, and the NGO has never paid before a flood. Target by exposure and need now; record outcomes (the case's follow-up 3 phones 300 recipients and 300 non-recipients) so a later season can ask the effect question.

---

## Scaling Up – The Trigger Card, Lists A and B, and Real-World Limits

The full program is small. What makes it work is the paperwork:

```
Field pathway - the trigger card
  If the morning bulletin forecasts the main gauge at +100 cm or more above danger level
  within 5 days, release the transfer to List A today (10,000 households, $50 each).
  One release per season. If no release has happened when a severe flood passes, pay List A then.
```

- **List A** goes to the mobile-money provider at the start of the season, not on the day, so its two-day lead time doesn't eat into the forecast's five.
- **List B**, the next 2,000 by score, is ready for a partial trigger: if the forecasting service can say which areas will flood, pay List A in those areas, then List B there.
- **Households without mobile money** (30% of the survey, often the poorest) need cash points agreed in advance. Check List A's share of them; if it is lower than the survey's, the list is quietly excluding them.

Real-world limits the program leaves out:

- **One gauge.** Real rivers have several gauges and forecasts by area; a trigger can be set per area, with the same method applied to each.
- **One forecast per wave.** Real bulletins update daily. A rule that waits for two consecutive mornings above the threshold trades a day of lead time for fewer false alarms; replay it on the record the same way.
- **A fixed season.** If floods come early, List A must already be with the provider; the readiness check in the case's follow-ups covers this.

---

## Code Implementation & Simulation

The full program is [`code/case14_flood_trigger.py`](code/case14_flood_trigger.py). It needs `numpy` and `pulp` (PuLP 3, which ships with the free CBC solver) and runs in under a minute:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case14_flood_trigger.py
```

### Scoring a threshold

```python
def outcomes(h, f, T, reserve=0.0):
    sev = h >= SEVERE
    any_sev = sev.any(axis=1)
    first_sev = np.where(any_sev, sev.argmax(axis=1), WAVES)
    fired = f >= T
    any_fire = fired.any(axis=1)
    first_fire = np.where(any_fire, fired.argmax(axis=1), WAVES)

    hit = any_sev & (first_fire == first_sev)
    too_soon = any_sev & (first_fire < first_sev)
    missed = any_sev & (first_fire > first_sev)
    false_alarm = any_fire & ~any_sev

    early = np.select([hit, too_soon, false_alarm], [V_EARLY, V_TOO_SOON, V_FALSE], V_LATE)
    early = np.where(~any_fire & ~any_sev, V_HELD, early)
    value = (1 - reserve) * early + reserve * V_LATE
    return value, hit, too_soon, missed, false_alarm
```

`h` and `f` hold each season's three actual peaks and three forecasts. The release happens on the first wave whose forecast reaches `T`; the season's outcome depends on whether that wave comes before, at or after the first severe one. The same function scores the record (the calculator table) and 50,000 simulated seasons.

### The robust choice

```python
PV = plan_values()
BEST = PV.max(axis=1, keepdims=True)          # the best threshold's value, model by model
REGRET = BEST - PV                            # how far each threshold falls short of it
rob = dict(zip(THRESHOLDS, REGRET.max(axis=0)))
T_ROB = min(rob, key=rob.get)
```

`PV` has one row per model in the planning set and one column per threshold. Nothing more is needed: with ten candidate thresholds, checking each against every model is faster and clearer than an optimization solver.

### Results: the trigger

Seven rules are tested on 50,000 simulated monsoons from the "true" river (which the planner never sees; severe seasons 22%), then on six stress versions kept out of the planning: a wetter and a drier decade, forecasts that under-predict big floods, noisier forecasts, forecasts that run 35 cm high (outside the bias interval), and fast floods where 30% of severe waves are missing from the 5-day forecast. Rule C' is the calculator with the tie broken the other way.

```
  typical (the true river)  (severe seasons 22%)
    A pay after              T=  -  value=0.350  paid before the peak= 0.0%  too soon= 0.0%  false alarms= 0.0%
    B danger level           T=  0  value=0.256  paid before the peak=53.3%  too soon=46.7%  false alarms=83.4%
    C calculator             T=100  value=0.417  paid before the peak=63.7%  too soon= 9.1%  false alarms=10.8%
    C' calculator, other tie T=120  value=0.407  paid before the peak=46.1%  too soon= 3.7%  false alarms= 3.8%
    D expected value         T=100  value=0.417  paid before the peak=63.7%  too soon= 9.1%  false alarms=10.8%
    E robust                 T=100  value=0.417  paid before the peak=63.7%  too soon= 9.1%  false alarms=10.8%
    F robust + 20% reserve   T=100  value=0.404  paid before the peak=63.7%  too soon= 9.1%  false alarms=10.8%
  forecasts under-predict big floods  (severe seasons 22%)
    A pay after              T=  -  value=0.350  paid before the peak= 0.0%  too soon= 0.0%  false alarms= 0.0%
    B danger level           T=  0  value=0.257  paid before the peak=53.4%  too soon=46.4%  false alarms=83.4%
    C calculator             T=100  value=0.385  paid before the peak=34.8%  too soon= 5.4%  false alarms= 6.8%
    C' calculator, other tie T=120  value=0.370  paid before the peak=16.8%  too soon= 1.6%  false alarms= 1.9%
    D expected value         T=100  value=0.385  paid before the peak=34.8%  too soon= 5.4%  false alarms= 6.8%
    E robust                 T=100  value=0.385  paid before the peak=34.8%  too soon= 5.4%  false alarms= 6.8%
    F robust + 20% reserve   T=100  value=0.378  paid before the peak=34.8%  too soon= 5.4%  false alarms= 6.8%
  forecasts run high (+35 cm)  (severe seasons 22%)
    A pay after              T=  -  value=0.350  paid before the peak= 0.0%  too soon= 0.0%  false alarms= 0.0%
    B danger level           T=  0  value=0.228  paid before the peak=50.4%  too soon=49.6%  false alarms=95.8%
    C calculator             T=100  value=0.366  paid before the peak=69.0%  too soon=27.7%  false alarms=39.7%
    C' calculator, other tie T=120  value=0.402  paid before the peak=71.2%  too soon=17.9%  false alarms=23.3%
    D expected value         T=100  value=0.366  paid before the peak=69.0%  too soon=27.7%  false alarms=39.7%
    E robust                 T=100  value=0.366  paid before the peak=69.0%  too soon=27.7%  false alarms=39.7%
    F robust + 20% reserve   T=100  value=0.363  paid before the peak=69.0%  too soon=27.7%  false alarms=39.7%
  best value any threshold reaches, scenario by scenario: 0.417  0.545  0.362  0.388  0.381  0.417  0.391
  across the seven scenarios: average value, worst value, largest shortfall from the best
    A pay after              avg=0.350  worst=0.350  largest shortfall=0.195
    B danger level           avg=0.268  worst=0.217  largest shortfall=0.190
    C calculator             avg=0.406  worst=0.361  largest shortfall=0.051
    C' calculator, other tie avg=0.403  worst=0.362  largest shortfall=0.033
    D expected value         avg=0.406  worst=0.361  largest shortfall=0.051
    E robust                 avg=0.406  worst=0.361  largest shortfall=0.051
    F robust + 20% reserve   avg=0.394  worst=0.359  largest shortfall=0.054
```

The program prints all seven scenarios; three are shown here. The "best value" line lists, in order: typical, wetter, drier, under-predict, noisier, run high, fast floods.

### Results: the list

```
  replay of 1,000 severe floods - survey fields explain most exposure (plinth effect -1.0)
    random 10,000 of the survey    flooded households on the list=25.1%  need-weighted=25.0%  worst area=24.2%  per area=[2285, 1962, 1739, 1654, 1368, 992]
    geographic rule                flooded households on the list=37.2%  need-weighted=38.7%  worst area= 6.1%  per area=[268, 1381, 2132, 3005, 1307, 1907]
    geographic rule + floor        flooded households on the list=37.1%  need-weighted=38.2%  worst area=18.4%  per area=[982, 1381, 1823, 2605, 1302, 1907]
    exposure model + floor (ILP)   flooded households on the list=36.7%  need-weighted=48.2%  worst area=22.4%  per area=[1172, 1501, 1826, 2397, 1499, 1605]
  replay of 1,000 severe floods - household detail matters more (plinth effect -2.5)
    random 10,000 of the survey    flooded households on the list=25.1%  need-weighted=24.9%  worst area=23.9%  per area=[2285, 1962, 1739, 1654, 1368, 992]
    geographic rule                flooded households on the list=37.2%  need-weighted=38.6%  worst area= 6.0%  per area=[268, 1381, 2132, 3005, 1307, 1907]
    geographic rule + floor        flooded households on the list=37.0%  need-weighted=38.2%  worst area=18.4%  per area=[982, 1381, 1823, 2605, 1302, 1907]
    exposure model + floor (ILP)   flooded households on the list=42.2%  need-weighted=54.0%  worst area=29.0%  per area=[1354, 1577, 1792, 2265, 1542, 1470]
```

Each replay floods homes at random from each household's true chance, which includes village-level luck in each flood and household detail the survey doesn't record. "Need-weighted" counts a flooded household with a child under 5 and no income three times as heavily as one with neither. "Worst area" is the lowest share of flooded households reached in any of the six areas.

### Reading the results

**A trigger beats both usual answers.** In the typical river, a threshold of +100 raises the fund's average value from 0.350 (paying after) to 0.417, about a fifth more, and pays before the peak in 64% of severe seasons. Releasing at the danger level does worse than paying after (0.256): it pays in 83% of seasons with no severe flood.

**All three methods chose the same threshold.** The calculator table, the fitted model and the robust choice all landed on +100, and in every scenario they score identically. What the models added was not a different answer but two things the table can't give: they broke the tie between 100 and 120, and they showed that 100 is never far from the best across everything the record allows (largest regret 0.031 in the planning set).

**The tie mattered, though not always the way the planning set predicted.** Rule C', which broke the tie upward, pays before the peak far less often: in the typical river 46% against 64%, and when forecasts under-predict big floods only 17% against 35%. But when forecasts run 35 cm high, a bias outside the record's interval, 120 does better (0.402 against 0.366), because 100 then fires on too many ordinary waves. Across the seven stress scenarios C' has the smaller largest shortfall (0.033 against 0.051). A robust choice is only robust against what is in its set; the planning set didn't include a bias that large.

**The value differences are small; the miss and false-alarm differences are not.** Between 100 and 120, average value differs by 0.003 across the scenarios. Paying before the peak in 64% versus 46% of severe seasons is a difference families feel. If the committee's real concern is "harm to lives" (Filter 4 of the case), its values should weight a late payment lower than 0.35, which moves the best threshold down and makes the lower of the tied thresholds the clearer choice.

**The reserve cost a little everywhere.** Holding back 20% lowered value in every scenario, by 0.002 (drier decade) to 0.039 (wetter decade): the more often floods come, the more hits it turns into late payments. It is insurance against false alarms that these values don't price highly.

**On the list, location does most of the work.** The geographic rule (lowest villages first, neediest first within each) puts 37.2% of flooded households on the list, against 25.1% for a random draw and 36.7% for the exposure model. But without a floor it reaches only 6.1% of flooded households in the worst-off area, because area 1's villages sit higher on average and it gets 268 places. The floor fixes that (18.4%) at almost no cost. The exposure model reaches far more of the *neediest* flooded households (48.2% against 38.2% need-weighted), because it weighs need against exposure instead of using need only to break ties within a village. When household detail matters more than the survey assumes (a raised plinth halving the risk again), the model's advantage grows: 42.2% of flooded households and 54.0% need-weighted, against 37.0% and 38.2%.

### The simpler alternative: a calculator table and a geographic list

The case's simpler option has two parts, one per layer, and both hold up.

**The trigger: the calculator table.** Replay the record for each candidate threshold, count hits, misses, too-soon releases and false alarms, and pick by the donor's false-alarm tolerance. Here it chose +100, the same threshold as both models, and scored identically in every scenario. In what ways it is close:

- **Same threshold, same results**, when the record covers the kinds of flood that matter and the tie goes to the lower threshold.
- **It makes the trade-off visible** in terms the donor and the committee understand: hits, misses and false alarms by year, checkable by hand.

What it gives up, and what to check before settling for it:

1. **Ties.** Twelve seasons can't tell some thresholds apart (here 100 and 120). Break ties toward the lower threshold unless false alarms are costly beyond money, and write the reason on the card. Or fit the forecast error once (mean and spread, as in Step 3) and redo the table with simulated seasons: that is Way 2, and it fits in a spreadsheet.
2. **Floods the record lacks.** Ask older staff and the forecasting service whether the worst floods they remember look like the record's three. If big floods rise faster or the forecast falls short on them, the threshold should be lower than the table says.
3. **The forecast's track record.** Get the service's own verification statistics for the 5-day forecast at this gauge. If its error spread is much larger than the record's 33 cm, every rule loses value and the table's choice shifts.
4. **The values.** The table's choice depends on how the committee weighs a miss against a false alarm. Agree those weights before the season, not after the first false alarm.

**The list: the geographic rule with a floor.** Every surveyed household in the lowest villages first, neediest first within each village, with each area's floor filled from its own households. It reaches as many flooded households as the exposure model (37.1% against 36.7%) and needs nothing beyond the survey and a village elevation list. In what ways it is close: total coverage, and fairness across areas once the floor is added. What it gives up: the neediest households (38.2% against 48.2% need-weighted), and more when household detail (plinths, distance) matters. Check before settling for it:

1. **Is there a floor?** Without one, the highest area got 268 places for 2,397 expected flooded households.
2. **Does need vary a lot within villages?** If it does, rank by exposure × need, which is still a sort in Excel, not a model.
3. **Does the survey record what makes a house flood?** If household features matter (plinth height, distance from the bank), the geographic rule's gap grows. An engineer's flood map plus the survey fields is the upgrade, and it is still a sorted list.

Together, the calculator table and the geographic list with a floor are a sound first season, as the case says. In this simulation they matched the full method on the trigger; the list's gap was about need, not coverage. The model's value is in what the table can't show: which thresholds are safe across the floods the record lacks, and how the choice moves if the forecast is worse than the record suggests.

### Cautions

1. **The values are invented.** Every threshold here follows from five numbers set for teaching. A real program should set its own with the donor and the committee, and rerun the table and the planning set with them.
2. **The robust choice is only robust against its set.** Forecasts that ran 35 cm high, outside the record's bias interval, favored the other tied threshold. Add the forecasting service's worst known errors to the planning set before choosing.
3. **Three severe floods can't validate anything.** The calculator table's "3 hits, 0 misses" at +100 is three events. Treat it as consistent with the method, not as proof.
4. **The list replay assumes the flood map is right on average.** If the map misses whole villages (new channels, embankment breaches), no ranking fixes that; the follow-up check of 300 recipients and 300 non-recipients after the first flood is how you would find out.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Outcomes** | hit, too soon, miss, false alarm, each with a value | Turns one season's forecasts and peaks into what the trigger did |
| **Cost-loss rule** | act if $p > \dfrac{C}{C + L}$; here $\dfrac{0.25}{0.25 + 0.65} = 0.278$ | How sure the forecast must be before releasing the money |
| **Small-sample intervals** | Wilson interval for 3 of 12; chi-square interval for the error spread | Shows how little twelve seasons say about flood frequency and forecast quality |
| **Calculator table** | replay the record for each threshold; count the four outcomes | The simple option; chooses by the donor's false-alarm tolerance |
| **Expected value** | $\max_T \; \mathbb{E}[V(T)]$ under a fitted forecast model | Breaks ties the record can't; assumes the fitted model is exact |
| **Robust (minimax regret)** | $\min_T \max_k [V_k^\ast - V_k(T)]$ over 27 plausible models + expert scenarios | A threshold that is never far from the best, whatever the river turns out to be |
| **Reserve** | share $r$ always paid late | Insurance against false alarms; its price is shown in value |
| **List (Class 2 layer)** | $\max \sum_i \hat p_i\, \text{need}_i\, x_i$, $\sum x_i = 10{,}000$, area floors | With equal transfers, a sorted list with floors; the work is in the exposure score |
| **Trigger card** | "release to List A if the 5-day forecast $\ge$ +100 cm" | The decision made and funded before the season, honored on the day |
| **Out-of-sample test** | 50,000 seasons under the true river and six stress versions | Tells you whether the threshold holds up on rivers and forecasts it never saw |

### Where to go next

- **Run the pilot** described in the [case's follow-ups](../cases/14-anticipatory-cash-floods.md#after-the-recommendation): backtest the trigger on the record, run a tabletop exercise with the card, then check the list after the first flood. The [playbook's pilot section](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) has the general rules.
- **Read** Pople et al. (2021) on the Bangladesh transfers, then the OCHA lessons from the 2020 Somalia pilot. For targeting, Aiken et al. (2022) and Hanna & Olken (2018). See the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Tools and help:** Excel for the calculator table and the list; this tutorial's program for the planning set; PuLP only if the list gains rules beyond floors. The Anticipation Hub collects trigger designs and lessons. A partner with forecast expertise (the national service, a university hydrology group) matters more than software ([build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners)).
- **Other tutorials:** the [cyclone tutorial](04-robust-optimization-cyclone-prepositioning.md) applies the same robustness idea to stocking warehouses months ahead; the [borehole tutorial](02-welfare-optimization-borehole-siting.md) covers the targeting layer when costs and coverage overlap make it a true integer program; the [grants tutorial](08-policy-learning-business-grants.md) shows what targeting by effect needs, once a trial exists; the [Case 6 tutorial](06-no-model-food-pantry.md) covers when no model is needed at all.
