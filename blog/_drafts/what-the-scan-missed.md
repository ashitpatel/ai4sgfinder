---
title: "What the first scan missed, and what it changed"
description: "AI4SG Finder was built from one research community's work on allocation. Four outside sources showed what that missed: tools that feed a decision, risk scores aimed at a program's own beneficiaries, and AI that is itself the program. Here is how a wider scan found more, and what changed."
layout: post
series: finder
---

*Part 11 in a series on [AI4SG Finder](https://github.com/ashitpatel/ai4sgfinder).*

AI4SG Finder helps a program choose a method for an allocation decision: who gets a visit, a well, a patrol or a place. Its twelve classes came from a careful reading of one research community. This post is about what that reading missed, how a wider scan of the field found more, and what changed as a result.

## Four sources that didn't fit

Four pieces of work arrived that the finder had no good answer for:

- **Courtroom transcription in India.** [Adalat AI](https://adalat.ai) fine-tunes speech-recognition models for Indian languages and runs them offline in courtrooms ([Nethil et al., Interspeech 2025](https://arxiv.org/abs/2507.01021)).
- **Sudden cardiac death from routine ECGs.** A deep-learning model trained on about 440,000 Swedish ECGs flagged a high-risk group with about a 7% annual rate of sudden cardiac death, against 4.6% for the standard test, and held up in San Diego and Taipei without retraining ([Berkeley News](https://news.berkeley.edu/2026/06/24/with-ai-researchers-discover-new-way-to-detect-sudden-cardiac-death-risk/)).
- **Race in risk scores.** Emma Pierson and colleagues showed that removing race from a colorectal-cancer risk model made it under-predict risk for Black patients, because a key predictor was recorded less reliably for them ([Zink, Obermeyer and Pierson, PNAS 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348319/)).
- **A database of local laws.** Berkeley researchers read about 7 million pages of scanned local codes with OCR and language models, and checked a sample by hand ([Peskoff et al., 2026](https://arxiv.org/abs/2606.19334)).

None of them allocates anything. Each produces something a decision uses: a transcript, a risk score, a fairness check, a table of laws.

## Five blind spots

Looking back, the first scans had five blind spots:

1. **One research community.** The classes came from a few AI-for-social-good optimization researchers and their co-authors. The four sources sit in medicine, fairness research, computational law and speech technology.
2. **The question set the answer.** Looking only for allocation methods left out, by design, anything that doesn't allocate.
3. **Counting, not reading.** The [landscape review]({{ site.baseurl }}/missing-step/) counted about 190 projects by kind of AI, but didn't ask what decision each one feeds. Adalat AI's funders include two of the fourteen organizations it reviewed.
4. **One kind of source.** University news offices, which translate papers from every department, weren't used. Three of the four sources came from one.
5. **Missing sectors.** Justice and law weren't sampled at all.

## A wider scan

So I ran a [wider scan](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/plans/expanded-scan.md): universities beyond computer science, institutes outside the US, funders' grantees, frontier labs and companies, conference tracks, operating NGOs and governments, and two years of university news. Three passes covered several hundred items.

The shape of the field was the first finding. In a sample of 97 conference papers, about one in seven allocates anything. Over 40% are inputs to a decision: forecasts, maps, screening tests, extracted records. Governance and audit work is as common as allocation.

## Tools that feed a decision

The finder now treats these as *input layers*. It names the decision the tool feeds, classifies that, and asks how well the tool works on the program's own data, not a benchmark. The checks differ by kind:

- **Screening tests** (a cough recording, an ultrasound sweep, an X-ray read by a model): accuracy against the confirmatory test in the population served, and a threshold set by how many people can be tested and treated.
- **Forecasts** (floods, outbreaks, crop failure): skill against a simple baseline where the program works, at the lead time the decision needs.
- **Ready-made maps** (buildings, relative wealth, damage): how old they are, and whether a score is a ranking or a real measure.

## The most common failure: scoring your own beneficiaries

The sharpest finding was about risk scores aimed at the people a program serves, to flag fraud or overpayment. It is the most common government use of these models, and the most common failure. The Dutch SyRI system was struck down by a court. Australia's Robodebt was found unlawful by a Royal Commission. Amsterdam built a welfare model with bias tests and reweighting, and in its live pilot it still flagged women and Dutch nationals more often. In US tax audits, a selection system that never used race audited Black taxpayers 2.9 to 4.7 times as often, because of what it was told to look for ([Elzayn et al., QJE 2025](https://doi.org/10.1093/qje/qjae027)).

The finder now says plainly when a score targets beneficiaries, and requires a legal basis, a person reviewing every flag, a way to appeal and a published fairness audit before any pilot. If those can't be met, it recommends against the model.

## When the AI is the program

Some tools *are* the program: a tutor, a coach for health workers, an adviser. The evidence on them points both ways. A six-week randomized trial of GPT-4 tutoring in Edo State, Nigeria, raised English scores by 0.23 standard deviations. A two-year trial of Khanmigo in US middle schools found gains similar to practice without AI. In Kenyan clinics, an AI copilot cut diagnostic errors in an observational study, but a randomized trial found no significant gain in patient outcomes. The finder now reviews how such a tool will be tested: an outcome, not usage, against a comparison.

## No thirteenth class

Many decisions looked new: drawing school zones, clearing a case backlog, choosing which villages to enter next, finding people already eligible under written rules. Almost all turned out to be variants of an existing class, or to need no model at all; a rules engine is enough when the rules decide. The taxonomy now has a [table of decisions near the twelve classes](https://github.com/ashitpatel/ai4sgfinder/blob/main/prompt/knowledge/taxonomy.md#decisions-near-the-twelve-classes).

The scan also strengthened a point the finder already made. In the Fragile Families Challenge, 160 teams' best predictions of children's life outcomes were only slightly better than a four-variable regression ([Salganik et al., PNAS 2020](https://doi.org/10.1073/pnas.1915006117)). When a method leans on predicting people's outcomes, expect the simple option to come close.

## How you can help

The scan is now a [quarterly recipe](https://github.com/ashitpatel/ai4sgfinder/blob/main/docs/scanning.md). If you know of a deployment, a failure or a trial it missed, especially from outside the US, tell me through an [issue on GitHub](https://github.com/ashitpatel/ai4sgfinder/issues).

{% include series.html %}
