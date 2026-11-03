---
title: "Five questions that tell you which AI you need, if any"
description: "Most nonprofits don't have an AI strategy yet. A strategy starts with the decision you want to improve, not the tool. These five questions, and a few follow-ups, point a program to the right kind of AI, or to a simple rule."
layout: post
date: 2026-11-11
---

*Part 2 of 6 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder). Previous: [Beyond chatbots: the AI that helps nonprofits decide where help goes]({{ site.baseurl }}/beyond-chatbots/).*

Three in four nonprofits don't yet have an AI strategy ([TechSoup, 2025](https://blog.techsoup.org/posts/what-ai-means-for-nonprofits-in-2025-insights-from-the-ai-benchmark-report)). Most conversations about one start from a tool: should we use ChatGPT, build a chatbot, buy an AI product? A more useful starting point is a plainer question: **which decision are we trying to improve?**

For programs that hand out something scarce, such as visits, cash, patrols, places or supplies, the answer depends on the shape of that decision. AI4SG Finder finds the shape with five core questions. Here is what each one asks, and why it matters.

## 1. What are you allocating, and what should it achieve?

This question sorts problems into families. A resource can be:

- **handed over once and kept**, like cash or a well, which raises the question of *who gets it*;
- **given again and again**, like home visits or reminder calls, where you can learn and adjust each round;
- **moved by vehicle** to many sites, like food or medical supplies;
- **used to look for something hidden**, like inspections, tests or patrols;
- **a message or practice** people should pass on to others.

Each shape points to a different family of methods. A well that lasts twenty years calls for a careful, auditable one-time choice. A weekly visit calls for a method that updates as people's situations change.

## 2. Who decides who gets what?

Usually the program decides centrally. But sometimes **both sides choose and can refuse each other**, as with apprentices and employers, or students and schools. Then the right tool is a matching mechanism that respects both sides' preferences, not a ranking. And sometimes **the community votes** on how to split a budget, which calls for a voting rule rather than an optimizer.

## 3. Does anyone avoid you or adapt to your plans?

If poachers, smugglers or fraudsters learn your schedule, a fixed plan stops working. That is the territory of security games, which randomize patrols so they can't be predicted. If instead applicants change their answers to qualify, the method usually stays the same, but the eligibility rule needs to be hard to game.

## 4. If an allocation turns out wrong, how bad is it, and what records do you have?

A wrong choice can be a small, fixable loss, such as a visit that could have gone to someone else this week, or harm to lives or trust. And the records you have decide what's possible:

- With only a handful of past disasters and lives at stake, you plan against the bad cases instead of the average one (robust optimization).
- With results from a randomized pilot, you can target people by how much the program helps them, not by how needy they look.
- With no records yet, you need methods that learn as they go.

## 5. How do your staff record data, and who would run the tool?

A method is only as good as the data your field teams can actually collect. Some methods need regular observations of every person; if staff record on paper once a month, those are out. And someone has to run the tool. In practice, the math should stay hidden: field workers get a list, a paper grid or a simple spreadsheet, not a model.

## Narrowing it down

The five questions place a problem in a family. A follow-up or two then picks one of twelve classes of method. For example:

- Do you know everyone before deciding, or do people arrive one at a time, like refugee families or waitlist applicants?
- Is the uncertainty how each person's situation changes week to week, or which of several program options works best?
- Do people on both sides rank each other, or does the community vote on one budget?
- Do you roughly know who talks to whom, so you could pick the best messengers?

Last comes a question many programs skip: **is there a second decision hiding inside this one?** Take an NGO that wants to pay cash to families before a river floods ([worked case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/14-anticipatory-cash-floods.md)). Choosing who gets the cash is one decision. Choosing *when* to release it, on which forecast, is another, and it's the one the director has to get right under pressure. The finder names both: a forecast trigger as the main method, and a targeting rule as a layer.

## A worked example

Here is how the questions play out for an illustrative program ([full case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/01-chw-hypertension-visits.md)). A county health NGO has 1,200 patients with hypertension and 10 community health workers, who can make about 80 home visits a week between them. Who should get a visit?

1. **The resource** is a home visit, given again and again: a slot used this week is free again next week.
2. **The NGO decides** who is visited.
3. **No one is avoiding the program**, but patients' adherence drifts on its own, and the effect of a visit fades.
4. **A wrong week is fixable**, and there are nine months of weekly adherence records, but no trial.
5. **Health workers record a pill count** at every contact on a phone app, and an M&E officer who uses Excel would run the tool.

The follow-up asks whether the uncertainty is how each patient changes or which option works. It's how each patient changes: there's only one option, a visit.

That points to a **restless bandit**. Each week it scores every patient by how much a visit *now* improves their adherence over the coming weeks, and the top 80 get a visit. A risk score would do worse: it sends visits to people who will lapse whether visited or not, and to the same patients every week. The health workers never see a score, just a list of whom to visit.

## What you get

Every recommendation has the same six parts:

1. **The method**, and why your answers point there.
2. **What goes wrong** with a naive model or a static spreadsheet instead.
3. **How it runs in the field**, on paper or in Excel: who runs it, how often, and what field workers see.
4. **Real deployments**, preferring NGO and public-sector cases, mapped to your program.
5. **A report card** from the published evidence: successes, field challenges and unknowns.
6. **The simpler alternative**: the best paper or spreadsheet option, how close it comes, and what to check before settling for it.

Then it offers follow-ups, one at a time: fitting the model to your program, readiness checks, pilot design, tools and partners, reading and people to contact, and a one-page brief for a technical partner.

## Sometimes the answer is no model

The questions can also show that you don't need AI at all. In another worked case, a volunteer-run food pantry is offered funding for "an AI tool to allocate food more fairly" ([full case](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/06-food-pantry-no-model.md)). Supply meets demand in 94% of weeks, and volunteers change often. The honest recommendation is two written rules: a regular top-up order, and a clear rule for who is served first in the rare short week. An AI tool would add cost and a dependency on one technical volunteer to solve a problem that comes up three weeks a year.

## Try it

AI4SG Finder is free and open source. The [project page](https://github.com/ashitpatel/ai4sgfinder) has one-click links for ChatGPT, Claude and Google AI Mode, so you can try it on a real decision in your program. If it gets something wrong, I'd like to hear about it.

*Next in the series: Which of these 12 decisions does your program make?*
