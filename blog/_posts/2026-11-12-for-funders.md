---
title: "For funders: checking the method in an AI proposal"
description: "Program officers increasingly receive proposals that use AI to decide who gets help, and most don't feel equipped to judge them. AI4SG Finder now has a funder review: paste a proposal and get a memo on whether the method fits the decision, what it should beat, and what to ask the NGO."
layout: post
series: finder
date: 2026-11-12 00:03:00 +0000
---

*Part 10 of 10 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder).*

The series so far has been written for the people who run programs. This post is for the people who fund them.

## The person on the other side of the proposal

Picture a program officer at a foundation that funds primary care in three districts. A proposal arrives: a community health NGO wants US$180,000 to build a machine-learning model that tells its health workers which patients to visit each week. It cites a 40% cut in hospital admissions from "similar AI programs." The budget looks reasonable, and the NGO is one the foundation knows.

What the program officer usually can't tell is whether the method fits the problem. Is a risk model the right tool for choosing whom to visit? Would a spreadsheet do as well? Where does the 40% come from?

They aren't alone. In a March 2025 study of 38 large philanthropies by Project Evident, only 36% of program officers surveyed felt confident judging the technical feasibility of AI proposals ([Chronicle of Philanthropy](https://www.philanthropy.com/news/even-tech-savvy-foundations-are-uncertain-how-to-fund-ai/)). And as [Part 5]({{ site.baseurl }}/missing-step/) found, none of the fourteen organizations we reviewed publishes a way to choose which kind of AI fits a program's problem. A funder can find out whether AI is worth considering at all, but not whether the particular method proposed is the right one.

## What the funder review does

AI4SG Finder now has a second way in. Instead of answering the interview, a funder pastes a proposal and says they're reviewing it. The assistant first asks for the funder's own context: what they fund and where, the grant size and period, and how much risk they accept. Then it writes a one-page memo with seven parts:

1. **The decision**, in one line: what is allocated, to whom, how often.
2. **Method fit**, with one of four verdicts: *fits*, *heavier than needed*, *mismatch*, or *no model needed*.
3. **The simpler option to beat**, and whether the proposal plans to compare against it on past records, counting the model's full cost.
4. **Up to five questions for the NGO**, from what the proposal leaves out and the readiness checks most at risk.
5. **Risks to people**, such as biased scores or patients who are never visited.
6. **An evidence check** of every figure the proposal cites: verified, unverified, or overstated.
7. **Suggested funding stages**: a test on past records, then a pilot, then scale, with the milestone that releases each.

## Three use cases

The project's worked cases include three funder reviews, one for each of the main verdicts.

**A mismatch: home visits chosen by a risk score** ([Case 17](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/17-funder-review-risk-score-visits.md)). This is the proposal above. The decision, which patients get a visit each week, is a repeated one where each patient's situation drifts: a restless-bandit problem ([Part 3]({{ site.baseurl }}/twelve-decisions/)). A risk score answers a different question. It finds the patients most likely to lapse, not the ones a visit will bring back. The memo also flags the success measure, "share of high-risk patients visited," which rewards following the list rather than better health, and marks the 40% figure as unverified. Its first funding stage is a small grant to replay last year's records under the risk list, a simple table and current practice.

**A fit: delivery routing** ([Case 18](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/18-funder-review-delivery-routing.md)). A food bank wants to plan its three trucks' weekly routes to 62 pantries with a free routing tool. The method matches the decision and the data exists. The memo's main caution is about evidence: the proposal cites the World Food Programme's 12% saving, which is real but comes from planning food baskets, sourcing and delivery together, so it isn't a forecast for truck routes. It doesn't suggest an outside evaluation, because miles driven measure the result directly.

**No model needed: a screening chatbot** ([Case 19](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/cases/19-funder-review-screening-chatbot.md)). An emergency-rent fund wants a chatbot that helps applicants and scores applications for approval. It gets about 40 applications a month and can pay about 35. The memo finds the allocation decision hidden inside the chatbot, and points out that with supply so close to demand, a published eligibility rule does almost all the work. The bilingual help with the form may be worth funding; the scoring probably isn't.

## What it won't do

Three limits are deliberate.

- **It reviews the method, never the organization.** It won't score an NGO, judge its leadership or capacity, or say whether to fund. Those judgments need knowledge of the organization that a proposal doesn't contain.
- **It won't suggest other NGOs.** I looked into whether an assistant could scout for organizations working in a region. Public data on small local groups is thin and often out of date, and a language model can name organizations that don't exist. A scouting tool would also favor large international NGOs with English websites, at a time when little funding reaches local organizations directly: in 2025, local and national groups received 4.3% of humanitarian funding directly ([ALNAP](https://alnap.org/help-library/resources/sohs-2026/chapter-4-power-imbalances-and-improving-accountability/4-1-funding-pathways-and-the-politics-behind-the-numbers/)). Funders' referral networks and local partners do that job better.
- **It gives questions and conditions, not a decision.** The memo is meant to make the conversation with the NGO sharper, not to replace it.

## How it connects to research partners

The funding stages link to [Part 9]({{ site.baseurl }}/research-partners/). A proposal that reaches several hundred people, can be rolled out in stages and already records its outcome may be ready for an evaluation. Then the memo suggests the NGO approach [J-PAL]({{ site.baseurl }}/j-pal/), [CEGA]({{ site.baseurl }}/cega/) or IPA with a researcher. Most proposals aren't there yet, and the memo says so: the first money should buy a test on past records.

## How I checked it

Before writing this post, I ran Case 17's proposal through the assistant on two different models, with no access to the expected answers. Both reached the right verdict, rejected the 40% figure, named the simpler option and stayed off the question of the NGO itself. One wrote its memo before asking the funder for their context, so I tightened the instructions, and on a second run it asked first.

## Try it

The funder review needs the full assistant with its playbook: the Custom GPT, the Claude skill or plugin, or the [all-in-one file](https://github.com/ashitpatel/ai4sgfinder/blob/main/dist/all-in-one.md) pasted as instructions ([setup](https://github.com/ashitpatel/ai4sgfinder#quick-start)). The one-click chat links carry only the interview, so they won't run it. Paste a proposal, say you're a funder reviewing it, and answer its three questions about your foundation.

If you're a funder and try it on a real proposal, I'd like to know what the memo missed. Tell me through an [issue on GitHub](https://github.com/ashitpatel/ai4sgfinder/issues).

{% include series.html %}
