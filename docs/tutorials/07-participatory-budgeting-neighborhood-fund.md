# Participatory Budgeting Masterclass: Splitting a Neighborhood Fund So No Area Wins Everything

*An in-depth walkthrough of approval and knapsack ballots, the greedy count and the method of equal shares, built on [Case 7: A neighborhood participatory budget](../cases/07-neighborhood-participatory-budget.md).*

**You need:** proportions, averages and the idea of a confidence interval. **You don't need:** any machine learning, voting theory or optimization background. Every term is explained when it first appears.

**Approach:** [Class 6: Participatory Allocation](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation). **Code:** [`code/case7_equal_shares.py`](code/case7_equal_shares.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A residents' association runs a neighborhood fund of **$250,000 a year** for small improvements: playground repairs, street lighting, bike racks, benches, trees. This year residents proposed **40 projects**, costed by city staff at between about $3,000 and $90,000 each. The city council has promised to fund whatever the vote chooses. The neighborhood has four areas. Last year most funded projects went to the north end, where homeowners turn out heavily, and almost none to the east-side apartment blocks, where turnout is low.

The clerk counts the vote in Excel the usual way: sort projects by votes and fund them in order until the money runs out. That count is simple and looks neutral, but it hands almost everything to whichever group casts the most ballots. The association's real risk is not a missing bike rack; it is trust. If one area wins everything again, people elsewhere stop voting.

This tutorial builds the alternative step by step:

1. **[The Proportional Leap](#the-proportional-leap--from-most-votes-wins-to-fair-shares-of-the-budget)** sets out the ballots (approval and knapsack), the greedy count, and what it means for a count to be *proportional*.
2. **[The Core Bottleneck](#the-core-bottleneck--majorities-turnout-and-blocs)** shows how a majority, a high-turnout area or an organized bloc can win everything under the greedy count.
3. **[From Ballots to Estimates](#from-ballots-to-estimates--what-the-count-needs-and-how-sure-it-is)** covers the data the count needs (every ballot, not just totals) and how sure we can be of the result, using a resampling check.
4. **[The Decision Engine](#the-decision-engine--the-method-of-equal-shares)** works the **method of equal shares** by hand on 10 voters, 3 groups and 6 projects, and checks it against a fairness test.
5. **[Scaling Up](#scaling-up--40-projects-four-areas-one-fund)** runs the full-size vote, adds a minimum share for the low-turnout east side, and looks at bloc voting.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** implements equal shares from scratch and compares it with the greedy count.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **give every voter an equal share of the budget, and let groups of voters spend their shares together.**

---

## The Proportional Leap – From Most Votes Wins to Fair Shares of the Budget

### Who decides, and why that changes the method

In most allocation problems a planner picks the plan that scores best on some goal: most people covered, most lives saved. Here there is no planner's goal. **The residents decide**, and the council has promised to fund their choice. The job of the method is not to find the "best" projects but to turn many individual ballots into one funded list by a rule everyone can accept as fair. This is **participatory budgeting**: a community votes on how to split a shared budget among proposed projects. Choosing a rule for turning votes into an outcome is the subject of **social choice**, the branch of economics that studies voting.

### Two kinds of ballot

A **ballot** is what each voter fills in. Two formats matter here:

- **Approval ballot.** Each project is listed with its cost; the voter ticks every project they support, as many or as few as they like. A tick is an **approval**. This is the format the case recommends, the same on paper and on the website.
- **Knapsack ballot.** The voter builds their own bundle of projects whose costs add up to no more than the budget, as if they were the city. The name comes from the "knapsack problem": packing the most value into a bag of fixed size. Goel and colleagues at Stanford's Crowdsourced Democracy Team introduced **knapsack voting** (ACM Transactions on Economics and Computation, 2019); it was used as the ballot in Boston's youth participatory budgeting in 2016. It makes voters face the budget, but it is hard to add up on paper.

Both ballots record the same kind of information: **which projects each voter supports**. The counting rules below work with either. Don't mix formats in one count; pick one and print it the same way everywhere.

### The standard greedy count

The clerk's spreadsheet uses the **greedy count**: add up the ticks for each project, sort from most to fewest, then go down the list funding each project that still fits in the remaining money, until nothing more fits. "Greedy" means it takes the best-looking option at each step without looking ahead.

It sounds fair: the most popular projects win. The trouble is *whose* votes make a project popular. If 900 north residents vote and 225 east residents vote, every north project starts with a four-to-one advantage over every east project. The north's projects fill the top of the list, and the money runs out before the list reaches anyone else. Nothing in the rule asks how many *different* voters got something they wanted.

### What "proportional" means

A rule is **proportional** if a group of voters wins a share of the budget roughly in line with its size. If 20% of voters all want the same projects, they should get about 20% of the money for them, not 0% because they are a minority and not 100% because they are well organized.

Social choice researchers made this precise with a test called **justified representation**. In plain words, for budgets:

> If a group of voters who got *nothing* they voted for all support the same project, and their equal shares of the budget added together would pay for it, the rule has treated them unfairly.

The code calls a breach of this test a **fair-share failure**. It is a minimum standard, not the whole of fairness, but the greedy count fails it routinely and the method of equal shares never does.

### Mapping it to the program

| Social-choice term | In this program |
|---|---|
| Budget | $250,000 a year, guaranteed by the council |
| Projects | The 40 resident proposals, each with a city-staff cost |
| Voters | Residents of the four areas who cast a ballot |
| Ballot | Approval: tick every project you support, cost printed beside each |
| Ballot sheet | The clerk's Excel sheet: one row per ballot, one column per project, 1 = ticked |
| Aggregation rule | Method of equal shares, replacing "most votes first" |
| Each voter's share | $250,000 divided by the number of ballots |
| Fairness guard | An optional minimum share for low-turnout areas ([Scaling Up](#scaling-up--40-projects-four-areas-one-fund)) |
| Published rules | The counting rule, minimum shares, tie-break and leftover rule, fixed before voting opens |

This is not a planner's targeting problem like the [borehole siting tutorial](02-welfare-optimization-borehole-siting.md), and it is not a matching market like the [apprenticeship tutorial](05-stable-matching-apprenticeships.md): projects have no preferences over voters. It is one budget split by a vote.

---

## The Core Bottleneck – Majorities, Turnout and Blocs

### A toy vote to keep in mind

Ten voters in three groups share a **$100,000** budget. Six projects are on the ballot:

| Project | Cost | Supported by | Votes |
|---|---|---|---|
| A shared path | $24,000 | all 5 North + all 3 West | 8 |
| B playground | $40,000 | 4 of the 5 North | 4 |
| C lighting | $30,000 | all 5 North | 5 |
| D bike racks | $21,000 | all 3 West | 3 |
| E benches | $13,000 | both East | 2 |
| F trees | $20,000 | both East | 2 |

North is half the voters, West 30%, East 20%. A proportional split would give them roughly $50,000, $30,000 and $20,000.

### A majority can win everything

Run the greedy count. A has the most votes (8): fund it, $76,000 left. C (5 votes): fund it, $46,000 left. B (4 votes): fund it, $6,000 left. D, E and F don't fit. Done: **A, C and B, $94,000 spent.**

Split each project's cost among the people who voted for it (the shared path counts $3,000 for each of its 8 supporters). North's projects get **$85,000**, West's $9,000, East's **$0**. Both East voters got nothing at all, though together they are a fifth of the electorate and their cheapest project, E, costs only 13% of the budget.

Apply the fair-share test. The two East voters got nothing, both support E, and their equal shares add up to $2 \times \$10{,}000 = \$20{,}000 \ge \$13{,}000$. **That is a fair-share failure**, and F ($20,000) fails the same way. North didn't cheat; the rule simply lets any group that supplies the most votes take everything.

### Turnout is not population

In the case, the north end is not a majority of *residents*. In the synthetic neighborhood of [Scaling Up](#scaling-up--40-projects-four-areas-one-fund), north holds 21.4% of adults but casts 44.2% of ballots, because 30% of its adults vote against 5% in the east. Every rule, proportional or not, counts ballots, not residents. Proportionality protects **groups that vote**, not groups that don't. That is why the case pairs the rule with outreach and a minimum share for low-turnout areas.

### Blocs

Last year a homeowners' group circulated a list of "our" projects. A **bloc** is a group that votes together on an agreed list. Under the greedy count, a bloc concentrates its votes and can push its whole list to the top. A proportional rule limits a bloc to its share of the voters, though, as [Scaling Up](#scaling-up--40-projects-four-areas-one-fund) shows, not perfectly.

### The rule must be fixed before the vote

Once ballots are in, anyone can compute which rule favors whom. Choosing or changing the rule afterwards turns a count into an argument, and the result loses its legitimacy. The counting rule, the minimum shares, the tie-break and what happens to leftover money all have to be **published before voting opens**.

---

## From Ballots to Estimates – What the Count Needs and How Sure It Is

### Step 1: The count needs every ballot, not just totals

The greedy count only needs one number per project: its total votes. Equal shares needs to know **who** voted for what, because it tracks how much of each voter's share has been spent. Two projects with 300 votes each look identical in the totals; equal shares treats them very differently if the same 300 people voted for both (they share one pot of money) or 600 different people did (two pots).

So the clerk's sheet must have **one row per ballot**: paper ballots typed in, the website export pasted below, one column per project, 1 for a tick. Last year's records are totals per project, which is the gap the case flags: if last year's paper ballots were kept, type them in now and recount last year under both rules.

### Step 2: Describe the electorate with simple proportions

Before counting, compare who voted with who lives there. For the synthetic neighborhood:

| Area | Adults | Ballots | Turnout | Share of ballots | Share of adults |
|---|---|---|---|---|---|
| North (homeowners) | 3,000 | 900 | 30% | 44.2% | 21.4% |
| West | 3,500 | 490 | 14% | 24.1% | 25.0% |
| South | 3,000 | 420 | 14% | 20.6% | 21.4% |
| East (apartment blocks) | 4,500 | 225 | 5% | 11.1% | 32.1% |
| **Total** | **14,000** | **2,035** | | | |

Under equal shares, each ballot carries $250{,}000 / 2{,}035 = \$122.85$. So north voters together hold $900 \times \$122.85$, about 44% of the fund, and east voters about 11%. Those are the shares a proportional rule aims for. They come from turnout, which is why the table belongs in the published results.

### Step 3: How sure is the result? Resample the ballots

The ballots are one turnout on one fortnight. A slightly different set of residents could have voted. How much would the outcome move?

A **bootstrap** answers this without any formula. Treat the 2,035 ballots as a sample, and draw a new sample of 2,035 from them *with replacement* (some ballots are drawn twice, some not at all). Count it. Repeat 100 times. The spread of results across the resamples shows how much the outcome depends on exactly who turned up. The middle 95% of the resamples gives a range that works like a confidence interval.

Each area's share of the budget, average and 95% range over 100 resamples:

| Rule | North | West | South | East | Projects "on the edge" |
|---|---|---|---|---|---|
| Greedy | 60% (59–63) | 18% (4–28) | 21% (11–34) | 1% (0–4) | 10 |
| Equal shares | 44% (44–44) | 25% (16–31) | 19% (15–29) | 11% (8–14) | 5 |

A project is "on the edge" if it was funded in more than 10% but fewer than 90% of resamples: its fate depends on who happened to vote. Two lessons. Under greedy, **West's and South's shares swing wildly** (West anywhere from 4% to 28%) because one expensive project crossing the line changes everything, while East stays near zero in every resample. Under equal shares every area's share stays near its share of ballots, and half as many projects sit on the edge. The bootstrap is cheap to run and worth publishing alongside the result.

---

## The Decision Engine – The Method of Equal Shares

### The idea

The **method of equal shares** (Peters, Pierczyński & Skowron, NeurIPS 2021) turns the budget into money in voters' hands:

1. **Give every voter an equal share** of the budget. In the toy vote, $100,000 / 10 = \$10,000 each.
2. **A project can be funded only if its own supporters can pay for it** from what they have left.
3. Among the projects that can be paid for, **fund the one that costs each supporter least**. That cost is the **price per supporter**: the amount $\rho$ (the Greek letter *rho*) each supporter pays. Supporters with less than $\rho$ left pay everything they have, and the others pay $\rho$.
4. Take the payments out of the supporters' shares and repeat. **Stop when no project's supporters can pay for it.**

Step 3 is what makes it proportional. Popular projects are cheap per supporter, so they still go first. But a group that has spent its shares can't fund anything more, however many votes it has, and a small group that hasn't spent yet keeps its money for its own projects.

When nobody is short of money, $\rho$ is just the cost divided by the number of supporters. When some supporters are short, they pay all they have and the rest split the remainder: for a cost $c$ with supporters holding $m_1 \le m_2 \le \dots$, find the smallest $\rho$ with

$$
\sum_{\text{supporters } i} \min(m_i,\ \rho) = c .
$$

### Step-by-step concrete example: 10 voters, 3 groups, 6 projects

Everyone starts with $10,000.

**Round 1.** Prices per supporter: A $24{,}000/8 = \$3{,}000$; C $30{,}000/5 = \$6{,}000$; E $13{,}000/2 = \$6{,}500$; D $21{,}000/3 = \$7{,}000$; B $40{,}000/4 = \$10{,}000$; F $20{,}000/2 = \$10{,}000$. Everyone can afford these, so the cheapest wins: **fund A.** Each North and West voter pays $3,000 and has $7,000 left. East still has $10,000 each.

**Round 2.** C: the 5 North voters hold $5 \times 7{,}000 = \$35{,}000 \ge \$30{,}000$, price $6,000. E: $6,500. D: the 3 West voters hold exactly $21,000, price $7,000. F: $10,000. B: its 4 supporters hold only $28,000, less than $40,000, so **B can no longer be paid for**. Cheapest: **fund C.** North voters drop to $1,000 each.

**Round 3.** E at $6,500 beats D at $7,000: **fund E.** East voters drop to $3,500 each.

**Round 4.** D at $7,000: **fund D.** West voters drop to $0. F's supporters hold $2 \times 3{,}500 = \$7{,}000$, less than $20,000; B's hold $4 \times 1{,}000 = \$4{,}000$. Nothing else can be paid for. **Stop.**

| | Greedy count | Equal shares |
|---|---|---|
| Funded | A, C, B | A, C, E, D |
| Spent | $94,000 | $88,000 ($12,000 left over) |
| Money to North / West / East | $85,000 / $9,000 / $0 | $45,000 / $30,000 / $13,000 |
| Voters with nothing they voted for | 2 | 0 |
| Fair-share failures | E, F | none |

Every group now gets close to its proportional share ($50,000 / $30,000 / $20,000), and all ten voters have at least one project they asked for. North still gets the most, because it is the largest group. What it loses is project B, which only 4 voters wanted and which would have cost each of them their whole share.

### Why equal shares passes the fair-share test

The fair-share test asks about a group that got nothing and could afford a project from its own shares. Under equal shares, a group that got nothing has spent nothing. Its members still hold their full shares, enough by assumption to pay for the project, so the method would fund it before stopping. Peters, Pierczyński & Skowron prove that equal shares meets a much stronger version of this guarantee, for groups of every size and for getting more than one project, up to a margin of one project.

### Leftover money: completing the budget

Equal shares stopped with $12,000 unspent. That is normal: it stops when no group can pay for another project on its own, and leftover money is common. Real votes add a **completion** step, and the published rule must say which one. The code uses the two that are common in practice:

1. **Raise everyone's share** a little at a time (here 10% steps, then 1% steps) and re-run equal shares, keeping the largest raise whose result still fits in the real budget.
2. **Fill any remaining money** greedily by votes.

In the toy vote neither step helps: the cheapest unfunded project, F, costs $20,000, more than the $12,000 left. The published rule then decides where that money goes, for example rolling it over to next year.

---

## Scaling Up – 40 Projects, Four Areas, One Fund

### The synthetic neighborhood

The code builds an illustrative neighborhood that matches the case: four areas with the turnout in the table of [From Ballots to Estimates](#from-ballots-to-estimates--what-the-count-needs-and-how-sure-it-is), and 10 projects per area costing from $3,000 to $82,200 (all 40 together cost $923,100, nearly four times the fund). Each voter ticks projects in their own area with a probability that depends on how appealing the project is, and other areas' projects with a tenth of that probability. Voters tick 5.6 projects on average.

Those are made-up behaviors chosen to teach the method. Real voters may back projects across the neighborhood more or less than this, which changes the size of the gap between the rules.

### Greedy versus equal shares

| | Greedy | Equal shares (no completion) | Equal shares + completion |
|---|---|---|---|
| Projects funded | 11 | 19 | **23** |
| Money spent | $249,700 | $166,100 | $248,800 |
| Share of budget N / W / S / E | 59% / 15% / 26% / **0%** | 30% / 13% / 15% / 8% | 44% / 29% / 15% / **11%** |
| Projects N / W / S / E | 8 / 1 / 2 / 0 | 8 / 3 / 5 / 3 | 9 / 5 / 5 / 4 |
| Voters with at least one funded project | 87% | 97% | **98%** |
| East voters with at least one | 45% | 95% | 96% |
| Fair-share failures | 2 | — | 0 |

The greedy count reproduces last year: north takes 59% of the money and the east nothing. The seven most-voted projects are all in the north. Equal shares funds more than twice as many projects, because it reaches for cheap projects that matter to smaller groups, and gives each area close to its share of ballots (north 44.2%, east 11.1%). Before completion, it spent only $166,100; completion raised each voter's share by 52% and then filled the rest by votes. Of the money spent before completion, north voters paid 48%, west 21%, south 21% and east 10%, close to each area's share of ballots.

### A minimum share for low-turnout areas

Equal shares gives the east 11% because the east cast 11% of ballots, though it has 32% of the adults. If the association wants a floor for the east, the case suggests a **reserve**: a set amount counted on east ballots for east projects first, with the rest of the fund then counted neighborhood-wide by equal shares.

| East reserve | Projects funded | Share N / W / S / E | East projects |
|---|---|---|---|
| none | 23 | 44% / 29% / 15% / 11% | 4 |
| $25,000 (10%) | 23 | 44% / 29% / 15% / 11% | 4 |
| $37,500 (15%) | 24 | 44% / 25% / 15% / 14% | 5 |

A $25,000 reserve changes nothing: east voters' equal shares already come to about that much ($225 \times \$122.85$). A reserve only bites when it exceeds what an area's turnout already earns. At $37,500, the east gets a fifth project and the money comes mostly from the west. How large the reserve should be is a value judgment for the association and the council, agreed and published before voting. The reserve does not replace outreach in the east-side blocks; turnout is what drives every number above.

### Bloc voting

Suppose the homeowners' group gets every north voter to tick the same list of 6 north projects (costing $136,400, 55% of the fund) and nothing else in the north.

| Rule | North's share, sincere ballots | North's share, bloc list |
|---|---|---|
| Greedy | 59% | 55% |
| Equal shares, no completion | 30% | 36% |
| Equal shares + completion | 44% | **56%** |

Under greedy, the bloc changes little: north already wins. Under equal shares, the main count holds the bloc below north's 44% share of ballots: concentrating on fewer projects only helps north spend more of the shares it already has. **Completion is where the bloc gains.** Raising everyone's share helps most the group that can actually spend the extra, and the bloc's list is designed to be spendable. Here, it lifts north to 56%.

This is an honest limit, not a reason to go back to greedy, where the bloc dominates anyway. It means:

- Proportionality is guaranteed for the main count, not for whatever completion rule is chosen. Check the completion rule on last year's ballots (or simulated ones) before publishing it.
- Publish the anonymized ballot sheet afterwards, so anyone can recount, and the effect of organized lists is visible.
- No counting rule is fully immune to strategy. Equal shares limits what a bloc can take; it doesn't stop people organizing.

### Publish the rule before the ballot is printed

The case's field pathway, in order: agree with the council the counting rule (equal shares), the completion rule, any minimum shares, and a published lottery for ties; publish them before voting opens; print one approval ballot with costs, the same on paper and on the website; enter every ballot as one row; run the count; give the clerk the winners with a plain-language explanation; publish the anonymized sheet.

---

## Code Implementation & Simulation

The full program is [`code/case7_equal_shares.py`](code/case7_equal_shares.py). It needs only `numpy`, and runs in about 10 seconds:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case7_equal_shares.py
```

Equal shares is written out from scratch so every step is visible. For the real count, use a maintained library such as pabutools or the tools at equalshares.net, and check it against this program on the toy vote.

### The price per supporter

```python
def price_per_supporter(money, cost):
    if money.sum() < cost - 1e-9:
        return None                                   # supporters can't afford it
    m = np.sort(money)
    k = len(m)
    paid_in_full = np.concatenate(([0.0], np.cumsum(m)[:-1]))
    rho = (cost - paid_in_full) / (k - np.arange(k))
    j = int(np.argmax(rho <= m + 1e-9))
    return float(rho[j])
```

This solves the formula in [The Decision Engine](#the-decision-engine--the-method-of-equal-shares). It sorts supporters from poorest to richest and tries "the $j$ poorest pay everything they have, the rest split what's left equally"; the right $j$ is the first where that equal split is no more than the next supporter can afford.

### The main loop

```python
money = np.full(n, budget / n)                        # equal shares
while True:
    best, best_rho = None, np.inf
    for p in unfunded projects:
        rho = price_per_supporter(money[supporters of p], costs[p])
        if rho is not None and rho < best_rho:
            best, best_rho = p, rho                   # cheapest per supporter so far
    if best is None:
        break                                         # no group can pay: stop
    money[supporters of best] -= np.minimum(money[supporters of best], best_rho)
    funded.append(best)
```

(Shown in outline; the program has the full version.) Ties go to the lower project number in the code; a real count should use the published lottery.

### Simulation output

```
Toy vote - 10 voters (North 5, West 3, East 2), budget $100,000, $10,000 each
  greedy funds: A, C, B  spent=$94,000
  equal shares round 1: fund A shared path (N+W)    price per supporter=$3,000  money left N/W/E per voter = $7,000/$7,000/$10,000
  equal shares round 2: fund C lighting (N)         price per supporter=$6,000  money left N/W/E per voter = $1,000/$7,000/$10,000
  equal shares round 3: fund E benches (E)          price per supporter=$6,500  money left N/W/E per voter = $1,000/$7,000/$3,500
  equal shares round 4: fund D bike racks (W)       price per supporter=$7,000  money left N/W/E per voter = $1,000/$0/$3,500
  greedy        money per group N/W/E = $85,000/$9,000/$0  voters with nothing=2  fair-share failures=['E', 'F']
  equal shares  money per group N/W/E = $45,000/$30,000/$13,000  voters with nothing=0  fair-share failures=[]

Simulation - greedy count vs equal shares
  greedy (most votes first)              projects=11  spent=$249,700  share N/W/S/E=59%/15%/26%/0%  ...
  equal shares (before completion)       projects=19  spent=$166,100  share N/W/S/E=30%/13%/15%/8%  ...
  equal shares + completion              projects=23  spent=$248,800  share N/W/S/E=44%/29%/15%/11%  ...
  completion raised each share by 52% before filling the rest by votes
  fair-share failures: greedy=2  equal shares=0
```

(Some lines are shortened; the program prints the full table, the reserve options, the bootstrap and the bloc test quoted above.)

### What the results say

- **Equal shares funds more projects and reaches more people.** 23 projects instead of 11 with the same $250,000; 98% of voters have at least one funded project instead of 87%, and among east voters 96% instead of 45%.
- **Each area gets about its share of ballots.** North 44%, east 11%, against 44.2% and 11.1% of ballots. Greedy gave north 59% and the east nothing.
- **Proportional to ballots is not proportional to residents.** The east has 32% of adults. Only turnout, or a published reserve, changes that.
- **It is the same pattern as the real evidence, not a forecast of it.** In Aarau, Switzerland, equal shares funded 17 projects where the standard greedy count would have funded 7 with the same budget (Pournaras et al., 2025); equal shares was also used in Wieliczka, Poland, in 2023. Those are city-run votes, the closest parallel to this fund; none is a neighborhood association. This neighborhood's numbers are invented, and its real result will depend on its real ballots.

The cautions from earlier stand: the count needs individual ballots, completion can favor a well-organized bloc, and every rule must be published before voting. The case's pilot is the right test: one cycle, counted under both rules, with the binding rule announced in advance and a fairness survey afterwards.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Ballot** | approval: tick any; knapsack: bundle with total cost $\le$ budget | One row per ballot in the clerk's sheet, same on paper and web |
| **Greedy count** | sort by votes, fund in order while it fits | Today's count; lets the group with the most ballots take nearly everything |
| **Equal shares** | each voter holds budget $/\,n$ | Turns the budget into money in voters' hands |
| **Price per supporter** | smallest $\rho$ with $\sum_i \min(m_i, \rho) = c$ | Fund the project that costs its supporters least; stop when no group can pay |
| **Fair-share test** | unserved supporters $\times$ budget$/n \ge$ cost $\Rightarrow$ failure | Justified representation; greedy fails it, equal shares never does |
| **Completion** | raise shares in steps, then fill by votes | Spends the leftover; must be published, and can favor organized blocs |
| **Minimum share** | reserve $R$ counted on one area's ballots first | Protects low-turnout areas; only bites above what turnout already earns |
| **Bootstrap** | recount 100 resamples of the ballots | Shows how much the result depends on who happened to vote |
| **Publication** | rule, reserve, tie-break, leftover rule before voting; ballot sheet after | What makes the result legitimate |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/07-neighborhood-participatory-budget.md#after-the-recommendation): agree the rule, minimum shares and tie-break with the council and publish them before the ballot is printed; redesign the ballot as approval with costs; plan outreach in the east-side blocks. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) sections of the playbook cover the Class 6 specifics.
- **Find help and tools:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section lists pabutools, equalshares.net and the Stanford Participatory Budgeting Platform, and partners who can check the setup.
- **Read** equalshares.net first, then Peters, Pierczyński & Skowron (2021) on equal shares and Goel et al. (2019) on knapsack voting, listed in the [playbook's reading list](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Other tutorials:** [stable matching for apprenticeships](05-stable-matching-apprenticeships.md), the other "people choose" class, where both sides rank each other; [welfare optimization for borehole siting](02-welfare-optimization-borehole-siting.md), for when a planner, not a vote, decides and fairness is written as a constraint; and [deciding without a model](06-no-model-food-pantry.md), for when a written rule is enough.
