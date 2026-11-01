# Case 7: A neighborhood participatory budget

| | |
|---|---|
| **Domain** | Local government and civic participation |
| **Intervention type** | Shared community budget for small public works |
| **Expected class** | [6 — Participatory Allocation (method of equal shares)](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation) |
| **Most likely confusion** | A planner ranking the projects ([Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)), or treating the vote as a matching problem ([Class 5](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets)) |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/07-participatory-budgeting-neighborhood-fund.md) |

## Scenario

A residents' association runs a city neighborhood fund of $250,000 a year for small improvements: playground repairs, street lighting, bike racks, benches, tree planting. This year residents proposed 40 projects, costed by city staff at between about $3,000 and $90,000 each. The city council has committed to fund whatever the vote chooses. The neighborhood has four areas; last year most funded projects went to the north end, where homeowners turn out heavily, and almost none to the east-side apartment blocks, where turnout is low.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> We have $250,000 a year for small neighborhood improvements: playgrounds, lighting, bike racks. Residents have proposed 40 projects, all costed by city staff. The goal is improvements people actually want, chosen in a way the whole neighborhood accepts as fair.

*Next turn, which fits best:*
> (a), handed over once and kept. Once a light or a playground is built, it stays.

**Filter 2 — Choice and preferences.**
> The residents decide. The city council promised to fund whatever the vote chooses. Our association just runs the process.

**Filter 3 — Environment dynamics.**
> No one is avoiding us. Some groups might organize to vote as a bloc; last year a homeowners' group circulated a list of "our" projects.

**Filter 4 — Tolerance for being wrong.**
> A poor choice is disappointing but fixable next year; nobody is harmed by a missing bike rack. The real risk is trust: if one area wins everything again, people stop voting.

*Next turn, what records:*
> We have last year's vote counts, the number of votes each project got, and the list of what was funded.

**Filter 5 — Field data and workflow friction.**
> Voting happens once a year over two weeks. Volunteers run paper ballots at the library and the community center, plus a simple website. The city clerk counts votes in Excel.

*Next turn, who would run it:*
> The clerk does the count. One of our volunteers is a retired engineer who can run a short script if someone sets it up.

**Narrowing (People choose).** *"Do individual people on both sides rank each other, such as students and schools, or does the community vote on how to split one budget among projects?"*
> The community votes on one budget. The projects don't rank anyone.

## Why Class 6: Participatory Allocation

The assistant should select **[Class 6 (Participatory Allocation)](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation)**, counted with the method of equal shares.

- **The community votes on how to split a budget** (Filter 2 — Choice and preferences). That moves the problem into the *People choose* family, even though Filter 1 (a) on its own would have pointed to *Who gets a limited resource*.
- **One budget, no two-sided ranking** (narrowing question). Projects have no preferences over voters, so this is [Class 6 (Participatory Allocation)](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation), not [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets).
- **The decision right belongs to residents**, with the council committed to the outcome (Filter 2). That rules out [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting): there is no planner's objective to optimize, and an optimized plan that overrode the vote would break the council's promise.
- **Bloc voting is not an adversary** (Filter 3 — Environment dynamics). Nobody evades anyone over territory, so [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) is out. A proportional rule limits what a bloc can win, though the step that spends leftover money can still favor it (see the tutorial).
- **Errors are fixable yearly** (Filter 4 — Tolerance for being wrong), so [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) isn't needed; the stake is trust, which a fair, published rule protects. A costed project list and a voting process (Filters 1 and 5) are the data Class 6 needs.

## What a good recommendation contains

**1. Class.** Participatory budgeting with an approval ballot (residents tick every project they support; each project's cost is printed beside it) and the **method of equal shares** to turn ballots into funded projects. Each voter gets an equal share of the $250,000; a project is funded when its supporters can jointly pay for it from their shares, with projects that cost each supporter least funded first. A group of voters then wins a share of the budget roughly in line with its size. The rule and its fairness properties come from Peters, Pierczyński & Skowron; the knapsack ballot from the Stanford Crowdsourced Democracy Team (Goel et al.).

**2. Counterfactual warning.** The standard greedy count, funding the most-voted projects in order until the money runs out, is what the clerk's spreadsheet does now. Under it, any group that is a majority, or simply turns out most, can win almost every project, which is how the north end won last year. A well-organized bloc can do the same. Expensive popular projects also crowd out several cheap ones that more people wanted in total. A planner-built "optimal" portfolio (Class 2) or a model predicting popular projects would be worse still: it replaces the vote the council promised to honor.

**3. Field pathway.** Voters see only a ballot: the 40 projects grouped by area, each with its cost, and "tick every project you support." Paper and website use the same ballot. The clerk enters each paper ballot as one row in Excel (one column per project, 1 = ticked) and merges the website export into the same sheet. The volunteer runs the count with pabutools or the tools at equalshares.net and gives the clerk a list of winners plus a plain-language explanation of each. The rule, the minimum shares and the tie-break are published **before voting opens**; afterwards, the anonymized ballot sheet is published so anyone can recount.

**4. Evidence.** The method of equal shares (Peters, Pierczyński & Skowron, NeurIPS 2021) was used in participatory budgeting votes in Aarau (Switzerland) and Wieliczka (Poland) in 2023. In Aarau, equal shares funded 17 projects where the standard greedy count would have funded 7 with the same budget (Pournaras et al., 2025). Knapsack voting (Goel et al., ACM Transactions on Economics and Computation, 2019) was used as the ballot in Boston's youth participatory budgeting in 2016. These are city-run votes, the closest parallel to this fund; none is a neighborhood association like this one.

**5. Report card.**
- *Successes:* in Aarau, 17 projects funded instead of 7 from the same budget; equal shares has moved from research into real city votes in two countries.
- *Challenges:* equal shares is harder to explain than "most votes wins," so the explanation must be ready before the vote; the count needs every individual ballot, not just totals per project; equal shares can leave part of the budget unallocated, so the published rule must say how leftover money is spent.
- *Unknowns:* proportionality protects groups that vote, not groups that don't. Whether the east side's projects win depends on east-side turnout, so pair the rule with a minimum share for low-turnout areas and outreach there. Whether results hold for a 40-project neighborhood vote is untested here; the pilot will show it.

**Next steps.** Agree the counting rule, the minimum shares and the tie-break with the council and publish them before the ballot is printed; redesign the ballot as an approval ballot with costs; plan outreach in the east-side blocks with the volunteers.

## What the assistant should *not* do

- Rank or optimize the projects centrally ([Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)), or frame the vote as matching residents to projects ([Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets)).
- Promise that this neighborhood will see Aarau's 17 versus 7; that is one city's result.
- Suggest choosing or changing the counting rule after the ballots are in. The rule must be fixed and published first, or the result loses its legitimacy.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

| Element | For this program | From |
|---|---|---|
| Budget | $250,000 a year, guaranteed by the council's commitment to fund the vote's outcome | Filters 1 and 2 |
| Project list | The 40 resident proposals, costed by city staff (about $3,000–$90,000) and checked as feasible before the ballot is printed | Filters 1 and 4 |
| Electorate | Residents of the four areas; decide the minimum age and how addresses are checked at the library, the center and online, so nobody votes twice | Filter 2 — Choice and preferences |
| Ballot format | Approval with costs printed, the same on paper and web. A knapsack ballot (build a bundle within $250,000) fits the website but is hard to add up on paper; don't mix formats in one count | Filters 2 and 5 |
| Aggregation rule | Method of equal shares, replacing the greedy "most votes first" count; it limits how much any bloc can take to its share of voters | Filters 2 and 3 |
| Fairness guard | A minimum share for each area, e.g. a reserve for east-side projects funded from east-side ballots first, then the rest counted neighborhood-wide; the amount agreed and published before voting | Filter 4; ethics |
| Voting channel | Paper ballots at two sites plus the website, entered by the clerk into one Excel sheet, one row per ballot | Filter 5 — Field data and workflow friction |
| Tie-break and leftovers | A published lottery for ties, and a stated rule for any money equal shares leaves unspent | Filter 4 — Tolerance for being wrong |

It should also flag the gap that matters most: **equal shares needs each voter's full ballot, but last year's records are vote totals per project.** If last year's paper ballots were kept, enter them now so last year can be recounted under both rules; if not, this year's count will be the first comparison.

### Follow-up 6: One-page brief for a technical partner

If the user picks **6**, a good answer fills the playbook template from the interview:

```
PROJECT BRIEF — Neighborhood participatory budget (illustrative)

The decision we need help with
  Each year, turn residents' votes into a funded list of small
  improvements from 40 costed proposals, within a $250,000 budget.

Why it matters
  The council funds whatever the vote chooses. Last year most projects
  went to the area that votes most; if one area wins everything again,
  residents elsewhere will stop taking part.

Current approach
  Paper and web ballots; the clerk counts in Excel and funds the most-voted
  projects in order until the money runs out.

Recommended approach
  Class 6 (Participatory Allocation): approval ballots counted by the method
  of equal shares, because residents decide one shared budget and a
  proportional rule stops any bloc or high-turnout area taking it all.

Data we have
  Last year's vote totals per project and the funded list. This year:
  one row per ballot in Excel, from paper and the website.

Constraints
  $250,000 a year; a minimum share for low-turnout areas; the rule must be
  published before voting opens; counting stays with the city clerk.

What success looks like
  Projects funded in more of the four areas, and residents rating the
  result as fair. Harm measure: any area receiving nothing.

How results must reach staff
  The clerk keeps the Excel sheet; a volunteer runs the count once a year
  and hands over the winners with a plain-language explanation.

What we are asking for
  Help setting up and checking the count script, and drafting the
  published rule, before this year's ballot is printed.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** the council's commitment is on paper; the rule, minimum shares and tie-break are published before voting opens; outreach is planned for the east-side blocks and other groups that rarely vote; individual ballots are kept, not just totals.
- **3. Pilot design:** run one cycle and count the ballots under both the greedy rule and equal shares, publishing in advance which one is binding; compare which areas' projects win under each and survey voters on fairness.
- **4. Build options:** pabutools (Python) or the tools at equalshares.net for the count; the Stanford Participatory Budgeting Platform if the website needs replacing. Process design and outreach matter more than code. INFORMS Pro Bono Analytics or a local university's operations-research or economics department can check the setup. Confirm each tool and partner is still active before relying on it.
- **5. Reading and contacts:** start with equalshares.net, then Peters, Pierczyński & Skowron (2021) on equal shares and Goel et al. (2019) on knapsack voting. The Stanford Crowdsourced Democracy Team (Ashish Goel) works on participatory budgeting platforms used by cities.
