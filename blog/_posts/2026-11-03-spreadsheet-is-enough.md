---
title: "When a spreadsheet is enough: 16 worked cases"
description: "Sixteen worked cases test when an AI method is worth it and when a spreadsheet rule comes close. In several, the simple rule matched the model; in others, the gap was large enough to matter."
layout: post
series: finder
date: 2026-11-03 00:03:00 +0000
---

*Part 4 of 11 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder).*

Recommending a method is the easy part. The hard part is showing why it fits, and being honest about when a spreadsheet would do almost as well.

That's what AI4SG Finder's [16 worked cases](https://github.com/ashitpatel/ai4sgfinder/tree/main/docs/cases) are for. They span health, water, conservation, disaster preparedness, youth employment, food security, civic participation, resettlement and environmental health. There is one case for each of the twelve kinds of decision, one where the right answer is "no model", and three where a program needs two methods together.

The organizations in the cases are fictional, so the details can be complete. The research they cite is real.

*Update, 22 November 2026: the folder now holds 25 cases. The nine added later are funder reviews ([Part 10]({{ site.baseurl }}/for-funders/)) and cases where a tool feeds the decision, such as a published ECG model or laws extracted from scanned documents.*

## What a case contains

Each case is written so you can follow the reasoning, not just the answer:

- **The scenario**: an organization and its constraint, in a few sentences.
- **Its answers** to the five questions, in the staff's own voice.
- **Why this method**, and why the closest alternatives were ruled out.
- **What a good recommendation contains**, and the most likely wrong answers.
- **The simpler alternative**: the best paper or spreadsheet rule, in what ways it comes close, and what to check before settling for it.
- **What comes next**: tools, partners and what it takes to run them, readiness checks, pilot design and a brief for a technical partner.

## The simpler alternative, measured

Every case names a simpler alternative, and the [tutorials](https://github.com/ashitpatel/ai4sgfinder/tree/main/docs/tutorials) put numbers on it. Each tutorial runs a short program that compares the method with current practice and with the simple rule. The data in the tutorials are illustrative, not from real programs, so these results show how the rules behave, not what a given program will gain. Still, the pattern is instructive.

**Sometimes the simple rule matched the method.**

- **Home visits** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/01-chw-hypertension-visits.md)): a six-cell table in Excel, grouping patients by how they respond and whether they're currently adhering, chose exactly the same patients as the full restless-bandit index. A plain rotation gained less than half as much.
- **Siting boreholes** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/02-borehole-siting.md)): a greedy rule with a minimum share per district picked the same 25 sites as the integer program.
- **Marine patrols** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/03-marine-patrols.md)): one spreadsheet column and Excel's Goal Seek reproduced the security game's patrol plan exactly.

**Sometimes it came close.**

- **Delivery routes** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/10-food-delivery-routing.md)): the classic savings method, workable by hand, produced routes 0–2.3% longer than the exact optimum. Most of the gain came from replacing habit with any systematic method.
- **Peer educators** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/12-peer-educators-network-seeding.md)): picking the most-named residents, spread across friend groups, reached about 94% as many people as the algorithm, and far more than staff picks.

**Sometimes the gap mattered.**

- **Lead pipes** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/13-lead-pipe-inspection.md)): digging the oldest homes first found about 85% as many lead pipes as the model. The model's extra finds came from using inspection records and neighborhood, about 34 more pipes a year in the tutorial.
- **Refugee placement** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/11-refugee-placement-online.md)): a printed table with quarterly quotas captured about 72% of the full method's gain, though it kept early and late arrivals treated alike.
- **Disaster stockpiles** ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/04-cyclone-prepositioning.md)): splitting kits equally across warehouses matched the robust plans in the worst scenarios but reached about 6 points fewer families in an average storm.

The point isn't that spreadsheets always win or always lose. It's that the comparison should be made, on your own records, before anyone builds a model. Every recommendation from AI4SG Finder includes that comparison and what to check first.

*Added 22 November 2026.* The tutorials make that comparison in Python, on made-up data. For three common decisions you can now make it in Excel, on your own records: the [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) has workbooks for a one-off choice of who gets something, a weekly visit list and a waitlist. Each compares your current practice, a simple rule and, if a partner built one, a model's scores, overall and by group. It runs on your own computer, needs no names, and says what a replay can't show. AI4SG Finder names the workbook for your class when it gives the simpler option, and again in the readiness checks, pilot design and the partner brief; the kit's guide explains [how to use it](https://github.com/ashitpatel/ai4sgfinder/blob/main/tools/replay-kit/README.md#how-to-use-it), from the records you need to deciding on the result. Its sample records make three points: a points rule came within one household of a model, a risk ranking did worse than random visits, and on a full waitlist every ordering gives the same average wait, so the question is who waits.

The comparison doesn't end at launch. A tool that beat the simple rule last year can drift as populations, hazards or recording change. A fourth workbook, a [monthly health check](https://github.com/ashitpatel/ai4sgfinder/blob/main/tools/replay-kit/README.md#after-launch-the-monthly-health-check), tracks a tool in use: whether staff follow its list, whether its picks still beat a small random share, whether its scores still match what happens, overall and by group. In its sample, a model goes stale when a new hazard appears; staff start overriding it, and the report reads those overrides as a sign the model needs updating, not as staff error.

The replays show what a model gains; a fifth workbook, [cost of ownership](https://github.com/ashitpatel/ai4sgfinder/blob/main/tools/replay-kit/README.md#before-deciding-the-cost-of-ownership), adds up what it costs. It lists about twenty lines, from cleaning the data to maintenance and cover when a volunteer leaves, in money and staff hours, for the model and the simple rule, and gives the cost of each extra person the model reaches. A blank line counts as not yet found out, so a total with blanks is a floor. In its made-up sample, each extra patient a model reaches costs fifteen times what the program spends per patient today.

Real figures are scarce. A search of published deployments found [twenty that report something](https://github.com/ashitpatel/ai4sgfinder/blob/main/prompt/knowledge/playbook.md#others-setups-what-has-been-published) about who built them, how long it took or what happened later, and none that reports what its model cost to build. The few costs published are for whole systems: Denver paid US$350,000 for a school-choice system that took four months to build and about US$575,000 a year to support, and the Swiss city of Aarau published every franc and staff hour of its participatory budget. The most telling setup is a warning: in Flint, model-guided digs found lead pipes at 70% of homes, and after a new contractor set the model aside, at 15%.

## When the answer is no model

One case is there to test the opposite temptation. A volunteer-run food pantry is offered funding for "an AI tool to allocate food more fairly" ([case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/06-food-pantry-no-model.md)). Supply meets demand in 94% of weeks. The right answer is two written rules: a regular top-up order, and a clear order of priority for the rare short week. Its [tutorial](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/tutorials/06-no-model-food-pantry.md) shows how to measure how much there is to gain before deciding, and when to revisit the decision as demand grows.

This case also tests the assistant itself. A change to the prompt that makes it more eager to recommend technology shows up there first.

## Learning the methods

The 14 tutorials explain each method step by step, assuming only basic statistics: what the method is, how it maps to the program, how to turn records into estimates, how the decision is made, and where it breaks down at scale. Each comes with a runnable Python program. You don't need to run the code to follow the argument, but a technical partner can use it as a starting point.

## Help make it better

AI4SG Finder is open source under the Apache 2.0 license and citable. It's a starting point, not the last word, and the cases are where it's easiest to see its gaps. I'd welcome help from three groups:

1. **NGO and public-sector teams:** try it on a real decision, and tell me where it gets it wrong.
2. **Researchers:** point me to methods or field deployments it's missing.
3. **Funders and capacity builders:** share it with grantees who face these decisions.

Corrections and suggestions are welcome as [issues on GitHub](https://github.com/ashitpatel/ai4sgfinder/issues).

{% include series.html %}
