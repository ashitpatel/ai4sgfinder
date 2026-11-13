---
title: "Which of these 12 decisions does your program make?"
description: "Twelve kinds of allocation decision that social programs face, from who gets a reminder call to where to dig for lead pipes, each with the method that fits it and the field evidence behind it."
layout: post
series: finder
date: 2026-11-03 00:02:00 +0000
---

*Part 3 of 10 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder).*

The [last post]({{ site.baseurl }}/five-questions/) described the five questions AI4SG Finder asks. Here is where they lead: twelve kinds of decision, grouped in five families. Each comes with the method that fits it and an example of that method at work in the field.

Most programs recognize one or two of their own decisions in the list. Some recognize none, which is useful to know too.

## Who gets a limited resource

**Which villages get the new wells?** When something is handed over once and kept, an integer program with explicit fairness rules makes the choice auditable: you can show why each village was or wasn't chosen. Panelot, a selection algorithm from Carnegie Mellon and Harvard researchers that evens out each volunteer's chance of being chosen, had been used to select more than 40 citizens' assemblies by 2021 ([Hertz Foundation](https://www.hertzfoundation.org/news/a-better-citizens-assembly-bailey-flanigan/)). A related approach, targeting with machine learning on phone data, cut the number of eligible poor people left out of Togo's emergency cash transfers by 4–21% compared with geographic targeting ([Aiken et al., *Nature* 2022](https://poverty-action.org/publication/machine-learning-and-phone-data-can-improve-targeting-humanitarian-aid)).

**Who should get the nudge, the grant or the training place?** The neediest are not always the people a program helps most. If a randomized pilot shows who benefits, effect-based targeting serves them first. In a field experiment with more than 53,000 CUNY students, targeting financial-aid reminders by estimated effect beat targeting by predicted need, and nudging the students with the lowest predicted outcomes actually hurt ([Athey, Keleher & Spiess, *Journal of Econometrics* 2025](https://arxiv.org/abs/2310.08672)).

**A refugee family arrives today: which city should it go to, when more families are coming?** When people arrive one at a time, each placement uses up capacity a later family might need. The resettlement agency HIAS uses Annie MOORE, which predicts where each family is likely to find work and places families within each office's yearly quota; backtests suggested a 22–38% gain in short-run employment ([Ahani et al., *Operations Research* 2021](https://doi.org/10.1287/opre.2020.2093)).

## Repeated decisions that learn

**Which beneficiaries get a reminder call this week?** When contact time is scarce and people's engagement drifts, restless bandits send it where it changes behavior. In ARMMAN's maternal-health program in India, a restless-bandit policy choosing which of about 23,000 enrolled mothers received a live call led to 32% fewer drops in engagement than standard care ([Google Research](https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/)).

**Which of three job-search supports should we offer?** Instead of splitting people evenly for a year, an adaptive experiment shifts people toward the options that are working while still serving everyone. The International Rescue Committee funded such an experiment for Syrian refugees and Jordanian jobseekers. The gain from adapting was small, about one percentage point of employment, but it showed that cash grants mattered most for refugees ([Caria et al., *JEEA* 2024](https://doi.org/10.1093/jeea/jvad067)).

## Space, movement and risk

**Where should rangers patrol when poachers move?** Randomized, game-theoretic schedules stay effective because they can't be learned and avoided. In Uganda's Queen Elizabeth National Park, rangers who patrolled two rarely visited areas that the PAWS model flagged as high-risk found numerous snares and other signs of poaching ([IEEE Spectrum](https://spectrum.ieee.org/this-ai-hunts-poachers)). The same family of models has scheduled US Coast Guard patrols in Boston since 2011 ([AI Magazine](https://ojs.aaai.org/index.php/aimagazine/article/view/2401)).

**Where should supplies wait before a flood nobody can forecast?** When there are only a handful of past disasters and getting it wrong costs lives, robust optimization plans against the bad cases instead of the average one. This is the least field-proven of the twelve: the evidence is mostly in models, including studies of the WFP-managed UN Humanitarian Response Depot network ([Stienen et al., *Omega* 2021](https://pure.uva.nl/ws/files/67452240/1_s2.0_S0305048321001031_main.pdf)).

**Which warehouse should supply which camp, and by which route?** Vehicle routing moves goods at least cost. The World Food Programme's Optimus model designs food baskets, sourcing and delivery together; in Iraq it cut costs by 12% for the same nutrition ([Peters et al., *INFORMS Journal on Optimization* 2021](https://doi.org/10.1287/ijoo.2019.0047)). Optimized school-bus routes saved Boston Public Schools about $5 million a year ([Bertsimas, Delarue & Martin, *PNAS* 2019](https://doi.org/10.1073/pnas.1811462116)).

**Which homes should we check for lead pipes?** Risk-based inspection looks where hidden problems are most likely, and learns from each inspection. Models of this kind guided the search for lead service lines in Flint, Michigan ([Abernethy et al., KDD 2018](https://arxiv.org/abs/1806.10692)). Greece's Eva system chose which arriving travelers to test for COVID-19 and found about 1.85 times as many asymptomatic infections as random testing ([Bastani et al., *Nature* 2021](https://doi.org/10.1038/s41586-021-04014-z)).

## People choose

**How should students be assigned to schools when families and schools both have preferences?** Matching markets respect choice on both sides. When New York City redesigned its high-school admissions around deferred acceptance, the number of students assigned to a school they had not chosen fell from about 30,000 to about 3,000 in the first year ([Abdulkadiroğlu, Pathak & Roth, *AER* 2005](https://stanford.edu/~alroth/papers/nycAEAPP.pdf)). The National Kidney Registry's paired-exchange matching had facilitated more than 4,600 living-donor kidney transplants by 2021 ([Osbun et al., *American Journal of Transplantation*](https://pmc.ncbi.nlm.nih.gov/articles/PMC8720056)).

**How should a neighborhood fund decide which projects get built?** In participatory budgeting, the voting rule decides whose priorities win. Boston's 2016 youth participatory budget used knapsack voting, in which each voter builds a bundle that fits the budget ([Goel et al., *ACM TEAC* 2019](https://arxiv.org/abs/2009.06856)). In Aarau, Switzerland, counting the 2023 vote by the method of equal shares funded 17 projects instead of the 7 a standard count would have chosen with the same budget ([Pournaras et al., 2025](https://arxiv.org/abs/2505.14349)).

## Spread through people

**We can train 20 peer leaders: which 20?** Network seeding picks the people who will spread a message furthest. In a trial with 713 homeless youth in Los Angeles, HIV risk behavior fell in the group whose peer leaders were chosen by an algorithm that maps who knows whom ([Wilder et al., AAAI 2021](https://doi.org/10.1609/aaai.v35i17.17754)). In Haryana, India, sending immunization reminders through villagers nominated as good spreaders of news raised vaccinations ([Banerjee et al., *Review of Economic Studies* 2019](https://doi.org/10.1093/restud/rdz008)).

## Predicting need is only one of these

Many programs reach for a risk or poverty score whatever the decision. A score like that is the right tool for some jobs, such as deciding who is eligible or where to inspect first. But it tells you who is poor or at risk, not whom a visit will help, where a poacher will go next, or how to split a budget the community voted on. Using it for those decisions can send help to people who would have done fine anyway.

Two more outcomes matter as much as the twelve:

- **Sometimes no model is needed.** If supply already meets demand most weeks, a written rule beats any tool. AI4SG Finder will say so.
- **Sometimes a program makes two decisions at once.** An NGO paying cash before a flood has to decide *when* to pay, on which forecast, and *who* gets paid. The finder names a main method and a second one layered on top.

## Which one is yours?

If one of these questions sounds like your program, [try AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder) on it. It takes a few questions to get from your situation to a recommendation, with the evidence and a simpler alternative. And if your decision isn't on this list, I'd like to hear about it: that's how the list gets better.

{% include series.html %}
