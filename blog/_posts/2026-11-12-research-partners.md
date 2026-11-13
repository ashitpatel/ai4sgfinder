---
title: "Using AI4SG Finder to work with research partners like J-PAL and CEGA"
description: "Research partners can help a program before it builds anything and after it has something to test. Here's how to use AI4SG Finder's follow-ups to draw on J-PAL and CEGA upstream, check whether you're ready for an evaluation, and write the brief that starts the conversation."
layout: post
series: finder
date: 2026-11-12 00:02:00 +0000
---

*Part 9 of 10 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder).*

The last two posts described [J-PAL]({{ site.baseurl }}/j-pal/) and [CEGA]({{ site.baseurl }}/cega/). This one is practical: how a program can use AI4SG Finder to work with them, or with a similar research group, at the right moment.

## Upstream and downstream

It helps to separate two kinds of help.

**Upstream** help comes before you build: evidence on what has been tried, guidance on data and privacy, tools for estimating cost, and training. Most of it is free to read and needs no partnership.

**Downstream** help comes once you have a program or tool to test: a researcher who designs and runs an evaluation, often with research funding they raise. This needs a partnership, and researchers are selective about which programs they take on.

It's easy to get the timing backwards: to look for an evaluator before there is anything to evaluate, and to find the free guidance only after the data pipeline is built. AI4SG Finder's follow-ups help with both.

## Step 1: Name the decision

Run the [interview]({{ site.data.try_links.claude }}). It asks five questions about the resource you allocate and recommends one of twelve kinds of method, or no model at all. It also names the best simpler option, such as a sorted list or a spreadsheet rule.

That recommendation is your starting point with any partner. "We want to use AI" gives a researcher little to work with. "We decide each week which of 1,200 patients get a home visit, and a restless bandit may beat our current risk ranking" is a research question.

## Step 2: Use upstream resources alongside the follow-ups

After the recommendation, AI4SG Finder offers six follow-ups. Several line up with free resources from J-PAL and CEGA:

| Follow-up | What it covers | Upstream resources to use with it |
|---|---|---|
| 1. Fit the model to your program | How the method works for your case | J-PAL's [evaluations database](https://www.povertyactionlab.org/evaluations) and [Policy Insights](https://www.povertyactionlab.org/policy-insights): has a similar rule been tested? |
| 2. Readiness checks | Data, consent and privacy, fairness, do-no-harm | CEGA's [Data Privacy Lab](https://cega.berkeley.edu/collection/data-privacy-lab/); J-PAL's [IDEA handbook](https://www.povertyactionlab.org/initiative/idea-handbook) on administrative data; CEGA's [brief on explaining AI targeting](https://cega.berkeley.edu/document/improving-the-transparency-and-explainability-of-ai-in-the-targeting-of-aid/) |
| 3. Pilot design | The smallest test that shows the approach beats current practice | J-PAL's [research resources](https://www.povertyactionlab.org/research-resources) on randomization and sample size; CEGA's [toolkits](https://cega.berkeley.edu/our-resources/data/), including a cost reporting table |
| 4. Build options | Tools and partners | J-PAL's [AI Evidence Playbook](https://www.povertyactionlab.org/ai-evidence-playbook), especially its section on targeting |

Two points from these resources are worth carrying into every allocation project. J-PAL's playbook asks what a program would do without AI, such as a simple decision rule; AI4SG Finder's simpler option answers exactly that. And CEGA notes that fewer than one in five impact evaluations include cost evidence. Record what the model costs to build and run from the start, so the comparison with the simple rule is fair.

## Step 3: Check whether you're ready for an evaluator

Follow-up 4 now includes a three-part test for when to approach an evaluator such as J-PAL, CEGA or [Innovations for Poverty Action](https://poverty-action.org/Partner-With-Us). You should be able to say yes to all three:

1. **Scale.** The program reaches at least several hundred people or sites.
2. **A comparison.** It can be randomized or rolled out in stages, for example by lottery or a waitlist, so some people or places get the new approach first.
3. **Outcome data.** It already records the outcome that matters, such as attendance, repayment or test scores.

This matches what J-PAL tells its own researchers to look for in a partner: enough participants, data capacity, willingness to build random assignment into operations, and a champion inside the organization ([J-PAL](https://www.povertyactionlab.org/resource/assessing-viability-and-building-relationships)). CEGA adds a preference for partners with flexible scale-up plans, so researchers can help decide when and where a program grows ([CEGA](https://cega.berkeley.edu/engage/for-partners/)).

If the answer to any of the three is no, an evaluator is not the next step. Run the pilot from Follow-up 3 with a build partner, start recording the outcome, and plan the next expansion so it can be staged. That work is what makes a program ready later.

## Step 4: Write the brief

Follow-up 6 drafts a one-page brief. Ask for it after the recommendation; it will first ask, in one turn, for anything the interview didn't cover. The brief now includes:

- **The program**: what you deliver and the change you want.
- **The decision** and the **recommended approach**, with the simpler option it must beat.
- **Where you work, your timeline and your resources**: geography and connectivity, the dates that can't move, and the staff and budget you have.
- **Where a partner can help**, split into two parts: what a **build** partner would do, and what an **evaluator** would measure. The evaluation part is filled in only if the program passes the three-part test; otherwise it says the pilot comes first.

Anything still unknown is marked *[to confirm]* rather than guessed. Fill those gaps before you send it.

## Step 5: Send it to the right place

- **J-PAL**: contact the [regional office](https://www.povertyactionlab.org/j-pal-offices) for your country. Its staff connect programs with affiliated researchers.
- **CEGA**: use the Research Collaboration Form on its [For Partners](https://cega.berkeley.edu/engage/for-partners/) page. CEGA shares it with its network and sets up a call if there's a match.
- **IPA**: use the contact form on its [Partner With Us](https://poverty-action.org/Partner-With-Us) page.

A few expectations to set:

- **Research funding goes to researchers.** At both J-PAL and CEGA, calls for proposals are open to affiliated researchers, who apply with an implementing partner. Your brief helps a researcher decide whether to apply with you.
- **Timing follows funding calls.** A researcher may need to wait for the next call, so share your timeline early.
- **They may say no, or not yet.** Researchers choose projects that answer a question their field cares about. A no is not a verdict on your program.
- **They don't build the tool.** Pair an evaluator with a build partner from [Follow-up 4](https://github.com/ashitpatel/ai4sgfinder/blob/main/prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners).

## Where this leaves the series

The first six posts were about choosing a method. These three are about what comes before and after: learning from what others have already tested, and, once a program is ready, finding out whether the method actually helped. The [last post]({{ site.baseurl }}/for-funders/) turns to the people on the other side of the proposal: funders.

If you take a brief from AI4SG Finder to a research partner, I'd like to hear how it went, including what was missing. Tell me through an [issue on GitHub](https://github.com/ashitpatel/ai4sgfinder/issues).

{% include series.html %}
