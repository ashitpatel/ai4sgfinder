# Case 23: Choosing where to campaign from a database of local laws

| | |
|---|---|
| **Domain** | Housing and tenant rights |
| **Intervention type** | Limited advocacy campaigns across many municipalities |
| **Expected outcome** | [**Class 2** Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) (yearly plan), fed by a **document-extraction input layer** (OCR and language-model labels) |
| **Most likely confusion** | Treating the database as the project, or recommending an allocation model for the extraction itself |
| **In-depth tutorial** | [Class 2 tutorial](../tutorials/02-welfare-optimization-borehole-siting.md) (the greedy rule with a floor carries over) |
| **Real-world pattern** | The Local Law Observatory and its LOCUS-v1 dataset (UC Berkeley, 2026) (see [Evidence](#what-a-good-recommendation-contains)) |

## Scenario

A (fictional) state tenant-rights coalition has six organizers and two staff attorneys. Each year they can run about 12 local campaigns: helping tenants push a city council to pass protections (notice before rent increases, just-cause eviction, a rental registry). The state has about 400 municipalities. Nobody knows which already have which protections: local codes are scattered across city websites and code-publisher sites, many as scanned PDFs.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We're allocating campaigns: about 12 a year, among 400 municipalities. A campaign is our organizers' and attorneys' time for six months.
>
> *Next turn (which fits best):* (a), handed over once a year. We plan the year's 12 in January.

**Filter 2 — Choice and preferences.**
> We choose, with our tenant-member groups. Cities don't apply for campaigns.

**Filter 3 — Environment dynamics.**
> Councils react to campaigns, but they don't move to avoid us. Laws change slowly.

**Filter 4 — Tolerance for being wrong.**
> A campaign in the wrong city wastes six months but harms no one directly. We have no history of which campaigns succeeded beyond our own 20 or so.
>
> *Next turn (data):* We know renter counts and eviction filings by city. We don't know what each city's code already says. A volunteer read 30 codes by hand last year; it took months.

**Filter 5 — Field data and workflow friction.**
> Spreadsheets. A volunteer data scientist offered to "use AI to read all the codes."

**Narrowing question — Who gets a limited resource.**
> Everyone is known up front: all 400 cities. We have no trial data on which campaigns work.

**Second decision.**
> Before we can choose, we need to know which cities lack each protection. That's the data problem.

## Why Class 2, with an extraction layer

- **Handed over once a year** (Filter 1 (a)), **central choice** (Filter 2), and **everyone known up front with no trial data** (narrowing) give [Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting): a yearly plan to divide 12 campaigns among 400 cities to reach the most renters lacking a protection, with a floor so rural regions aren't skipped.
- **The second decision is an input layer, not an allocation.** Reading 400 codes is document extraction: optical character recognition (OCR) on the PDFs, then a language model labelling each section by topic (does this section require notice before a rent increase?). It decides nothing; it produces the column the plan needs. Like a forecast in [Case 14](14-anticipatory-cash-floods.md), it is piloted and checked first.
- Not [Class 7](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting): 20 past campaigns are not a randomized pilot, so there's no basis for predicting where a campaign *works* best.
- Not [Class 12](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection): once the codes are read, nothing stays hidden; the campaign is a benefit, not a test.

## What a good recommendation contains

**1. Class.** A yearly Class 2 plan: rank cities by renters who lack the target protection, pick 12 with at least one per region, adjusted for where tenant-member groups exist. Its input is a table of cities × protections built by an extraction pipeline: download each code, OCR it, split it into sections, have a language model label each section, and **check a random sample of labels by hand** before trusting the table.

**2. Counterfactual warning.** Labels from a language model are guesses with an error rate, and the error is not even: scanned PDFs, unusual drafting and older codes fail more often, and those are often in smaller, poorer towns. A plan built on unchecked labels will send campaigns to cities that already have a protection and skip ones that don't. Choosing cities by the coalition's existing contacts or the largest cities alone misses where renters lack protection most.

**3. Field pathway.** The volunteer runs the pipeline once, producing a spreadsheet: city, protection, yes/no, the section text and a link, so organizers can confirm any entry in a minute. Attorneys check a random 100 entries. In January, the plan is a sorted sheet with the regional floor; the coalition adjusts by hand and records why.

**4. Evidence.**
- *Same input problem, at national scale:* the Local Law Observatory built a database of millions of US local ordinances from about 7 million pages ([Berkeley News, October 2026](https://news.berkeley.edu/2026/10/02/to-decipher-local-laws-researchers-used-ai-to-build-a-database-of-millions-of-them/); [arXiv 2606.19334](https://arxiv.org/abs/2606.19334)). Its pipeline: automated downloads from code-publisher sites; a vision-language OCR model (LightOnOCR); splitting by section headers; labelling a sample with a small OpenAI model, with a larger model re-checking the hardest cases; then training a small classifier (ModernBERT) on those labels to label every section cheaply. The released dataset, [LOCUS-v1](https://huggingface.co/datasets/LocalLaws/LOCUS-v1), includes a hand-audited subset, which is the check above. The dataset's licence is non-commercial; check it fits the coalition's use, and check whether it already covers the state before building anything.
- *Same allocation design:* the Class 2 references in the taxonomy.

**5. Report card.**
- *Successes:* the Observatory shows extraction at scale is cheap (cents per thousand pages for OCR) and that labels can be checked against a hand-coded sample.
- *Challenges:* codes that are only on paper; amendments not yet in the published code; labels for legal meaning ("just cause") are harder than for topic.
- *Unknowns:* the label error rate for *these* protections in *this* state; whether passed protections are enforced.

**6. Simpler alternative.** Skip the pipeline: have volunteers hand-code the 60 cities with the most renters, using a one-page checklist, and plan within those. It is close if most renters live in a few large cities. It gives up the small and rural towns where no one has looked. Check before settling: what share of the state's renters live in the 60 largest cities?

**Next steps.** Check whether LOCUS-v1 or a code publisher's search already answers the question for this state; if building, hand-code 50 sections per protection first, so the language model's labels can be scored against them.

## What the assistant should not do

- Treat building the database as the goal; it is the input to a decision.
- Recommend a classification or allocation "class" for the OCR and labelling steps.
- Accept language-model labels without a hand-checked sample and a measured error rate.
- Recommend effect-based targeting from 20 non-randomized campaigns.
