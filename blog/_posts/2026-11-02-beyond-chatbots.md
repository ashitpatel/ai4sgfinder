---
title: "Beyond chatbots: the AI that helps nonprofits decide where help goes"
description: "Most nonprofit AI use is generative: chatbots, writing and summaries. A less visible kind of AI decides who gets a call, a patrol or a placement, and has a field record. Here's what it is and how to tell which one your program needs."
layout: post
date: 2026-11-02
---

*Part 1 of 6 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder), a free, open-source assistant that helps nonprofits choose an AI method for allocating scarce resources.*

When nonprofits talk about AI, they usually mean chatbots, faster grant writing or summarized reports. Those tools are useful, but they are one kind of AI, and they work on the words around the work.

The numbers show how lopsided this is. In a survey of 1,321 nonprofits run in mid-2024, 85.6% were exploring or working with generative AI tools. Only 12.8% were working with predictive analytics ([TechSoup and Tapp Network, *The State of AI in Nonprofits 2025*, pp. 11–13](https://message.techsoup.org/hubfs/Downloads/The%20State%20of%20AI%20in%20Nonprofits%202025.pdf)).

Meanwhile, the hardest decisions in social programs are about allocation. Budgets almost never cover the need. In 2025, humanitarian appeals met only 35% of their funding target ([ALNAP, 2026](https://alnap.org/help-library/resources/sohs-2026/chapter-1-prioritisation-under-pressure/1-1-the-reality-of-funding-gaps/)). Every program decides who gets the call, the well, the patrol or the place, usually with a ranked spreadsheet or a risk score.

## The other kind of AI

A different kind of AI works on those decisions directly. It predicts, optimizes and allocates, and it has been improving outcomes in the field for more than a decade:

- **Which mothers get a health call this week.** In ARMMAN's maternal-health program in India, a restless-bandit policy chose which of about 23,000 enrolled mothers received a live call. It led to 32% fewer drops in engagement than standard care ([Google Research](https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/)).
- **Where rangers patrol.** In Uganda's Queen Elizabeth National Park, rangers who patrolled two rarely visited areas flagged as high-risk by the PAWS model found numerous snares and other signs of poaching ([IEEE Spectrum](https://spectrum.ieee.org/this-ai-hunts-poachers)). The same family of game-theoretic models has scheduled US Coast Guard patrols in Boston since 2011 ([AI Magazine](https://ojs.aaai.org/index.php/aimagazine/article/view/2401)).
- **Which city a refugee family goes to.** The resettlement agency HIAS uses Annie MOORE, which predicts where each family is likely to find work and places families within each office's quota. Backtests suggested a 22–38% gain in short-run employment ([Ahani et al., *Operations Research* 2021](https://doi.org/10.1287/opre.2020.2093)).
- **How food reaches people.** The World Food Programme's Optimus model plans food baskets, sourcing and delivery together. In Iraq it cut costs by 12% for the same nutrition ([Peters et al., *INFORMS Journal on Optimization* 2021](https://doi.org/10.1287/ijoo.2019.0047)).

None of these are language models. They come from operations research, economics and machine learning, and they get far less attention than chatbots.

## Where this started

That gap ran through a lively audience discussion at a [round table on AI, planetary health and poverty alleviation](https://www.linkedin.com/posts/stanford-alumni-alliance-on-innovation-for-global-impact_sharing-invite-to-a-in-person-interactive-activity-7517089723962769408-0GU8) at Stanford, held on October 30, 2026 by the [Stanford Alumni Alliance on Innovation for Global Impact](https://www.linkedin.com/company/stanford-alumni-alliance-on-innovation-for-global-impact) as part of its Reimagining AI for the Sustainable Development Goals series. It was sparked by research presented there by Columbia professors Roshni Sahoo and Lily Xu. People in the room raised questions about how these kinds of AI methods could be applied to other impact areas.

## Why "use AI" is not one answer

The trouble is that different allocation problems need different methods, and the obvious choice is often the wrong one. Three examples:

**A risk score tells you who is at risk, not whom your visit will help.** Some people do well whether or not you visit; others only improve if you do. In a field experiment with more than 53,000 CUNY students, targeting financial-aid reminders by each student's estimated effect beat targeting by predicted need. Nudging the students with the lowest predicted outcomes actually hurt them ([Athey, Keleher & Spiess, *Journal of Econometrics* 2025](https://arxiv.org/abs/2310.08672)).

**A fixed patrol rota gets learned and avoided.** Poachers, smugglers and fraudsters adapt to your schedule. Security-game models randomize patrols so the pattern can't be learned and avoided; the Coast Guard schedules above come from this family.

**A plan built on last year's flood fails when the next one looks different.** When there are only a handful of past disasters and mistakes cost lives, robust optimization plans against the bad cases instead of the average one. This is the least field-proven of these methods; most of its evidence comes from models, not deployments, and an honest advisor should say so.

## What AI4SG Finder does

So I built [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder), a small attempt to help nonprofits and public agencies evaluate this other kind of AI for the resources they allocate.

It's a free, open-source prompt you paste into ChatGPT, Claude, Gemini or Google AI Mode. It interviews you with five core questions:

1. What are you allocating, and what should it achieve?
2. Who decides who gets what: you, both sides by choosing each other, or the community by vote?
3. Does anyone avoid you or adapt to your plans?
4. If an allocation turns out wrong, is it a fixable loss or harm to lives or trust? And what records do you have?
5. How do your staff record data, and who would run the tool?

A follow-up or two narrows the answer to one of twelve classes of method, from restless bandits and matching markets to vehicle routing and network seeding. Or it tells you plainly that you don't need a model at all.

Each recommendation explains why the method fits, what goes wrong with a naive model or spreadsheet, how staff could run it on paper or in Excel, what the published deployments show, and the best simpler alternative with how close it comes.

For example, a clinic with 10 health workers who can make about 80 home visits a week across 1,200 hypertension patients would be pointed to a restless bandit: each week, visit the patients a visit will help most. The workers never see a score, just a list of whom to visit.

## Yes, it runs on an LLM

That's the part large language models are good at: asking questions and explaining. What it recommends are the methods that do the deciding.

I wrote this series the same way. I set the direction and made the editorial calls, and an AI agent drafted it and checked the facts against primary sources.

## What's next

This series covers:

1. **Beyond chatbots: the AI that helps nonprofits decide where help goes** (this post)
2. Five questions that tell you which AI you need, if any
3. Which of these 12 decisions does your program make?
4. When a spreadsheet is enough: 16 worked cases
5. The missing step in AI for social good: choosing the method
6. Not the last word: adapt it to your field

**Try it now**, no setup needed: the [project page](https://github.com/ashitpatel/ai4sgfinder) has one-click links for ChatGPT, Claude and Google AI Mode.

Thank you to the Stanford Alumni Alliance on Innovation for Global Impact, its co-hosts and everyone at the round table for the discussion and questions that shaped it.
