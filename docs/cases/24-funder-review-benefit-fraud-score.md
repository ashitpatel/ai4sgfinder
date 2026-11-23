# Case 24: Funder review of a benefit-fraud risk score

| | |
|---|---|
| **Domain** | Social protection |
| **Who is using the assistant** | A foundation program officer reviewing a proposal |
| **Expected verdict** | The memo's first line says the score targets the program's own beneficiaries. **Automatic payment pauses fail the safeguards required before any funding stage.** For the referral step, *Heavier than needed* (about 36 confirmed cases is too few for the model) or *Mismatch* are both defensible |
| **Most likely confusion** | Treating it as ordinary [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection) because investigators are limited |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal); readiness check *Scoring the people you serve* |
| **Real-world pattern** | Government welfare-fraud models: SyRI, Robodebt, Amsterdam's Smart Check, US tax-audit selection ([taxonomy, Section 6](../../prompt/knowledge/taxonomy.md#when-a-score-targets-the-people-you-serve)) |

## Scenario

A (fictional) civic-tech NGO has offered to build a fraud-risk model for a county's emergency cash benefit, paid monthly to about 6,000 households. The county's two investigators can review about 300 cases a year. The NGO asks a foundation to fund the build.

*This is an illustrative scenario, not a real program or proposal.*

## What the funder pastes

**The proposal, summarized.**
> The county pays an emergency cash benefit monthly to about 6,000 households, and its two investigators can review about 300 cases a year. We will train a gradient-boosted model on the county's 900 past fraud investigations (about 4% confirmed fraud) and 40 fields from the benefit application, linked to employment and housing records. Each month the model scores every recipient. The top 2% have payments paused until they bring documents to the office; the next 3% go to investigators. AI fraud detection has saved governments millions. Budget: US$140,000 over 18 months. Success measure: overpayments recovered.

**The funder's answers.**
> We fund economic security in one state. Grants are US$50,000–200,000 over one to two years. We fund early pilots if they're well designed. We'd want to know whether this is a good use of AI.

## Why the verdict rules out the pauses

Read against the filters, the shape is Class 12: investigations are limited and hidden fraud is to be found. Three facts change the verdict:

- **The people scored are the program's own beneficiaries.** A flag is an accusation, and here it pauses an emergency payment before anyone looks at the case. Government models of this kind have repeatedly been stopped or found unlawful: SyRI in the Netherlands (a court found it breached the right to private life), Robodebt in Australia (found unlawful by a Royal Commission), Amsterdam's model (biased in its live pilot despite bias testing).
- **The labels repeat past choices.** The 900 past investigations were chosen by tips and caseworkers, not at random, so the model learns who was investigated, not who commits fraud. With 4% confirmed, most flags will be wrong.
- **The objective can create the harm.** "Overpayments recovered" rewards flagging people whose payments are easy to claw back. In US tax audits, a race-blind model that prioritised one kind of error audited Black taxpayers 2.9–4.7 times as often (Elzayn et al., 2025).

What the county may actually need is to know why overpayments happen. If most come from agency errors or unclear rules, a model aimed at beneficiaries targets the wrong cause.

## What a good memo contains

1. **The decision:** which of about 6,000 recipient households have payments paused or are investigated each month. *The score targets the program's own beneficiaries.*
2. **Method fit:** a risk ranking for limited investigations is Class 12 in form, so the referral step is *Heavier than needed* (about 36 confirmed cases can't support a 40-field model, and a random-sample audit with caseworker referrals is likely as good) or a *Mismatch* (the labels record who was investigated, not who committed fraud). Either way, the automatic pause is an adverse action on a prediction, not an inspection, and fails the safeguards the playbook requires before any funding stage.
3. **The simpler option to beat:** a random sample of cases for review each month (which also measures how much fraud and error there really is), plus the caseworkers' current referrals. Any model must beat that, with a person reviewing every flag.
4. **Questions for the NGO:**
   - What share of past overpayments came from fraud, and what share from agency or applicant error?
   - What is the legal basis for pausing payments on a score, and how would a household see why it was flagged and appeal?
   - Will a person review every flag before any action? Will automatic pausing be dropped?
   - How were the 900 past cases chosen, and how will the model avoid repeating those choices?
   - Will you publish a fairness audit (flag rates and accuracy by group, by language and by household type) before and during any pilot?
5. **Risks to people:** families losing emergency income on a wrong flag; disparities by race, nationality, language or family type, as in Amsterdam and the US tax audits; linking employment and housing records without consent; a recovery target that rewards flagging the easiest cases.
6. **Evidence check:** "AI fraud detection has saved governments millions" has no source: *unverified*. The documented record for beneficiary fraud models is mostly of failures (the taxonomy's cautionary references).
7. **Funding stages:**
   1. A small grant for a random-sample review of past cases, to measure fraud against error and find where overpayments come from.
   2. Only if fraud is a large share, and with every safeguard in place (legal basis, human review, appeal, no automatic pausing, published audit): a pilot comparing a model's referrals with caseworkers' on the same sample.
   3. Scale only with an independent audit each year.

## What the assistant should not do

- Treat this as routine risk-based inspection because investigators are scarce, or fail to say in the first line that the score targets beneficiaries.
- Accept automatic payment pauses, or "overpayments recovered" as the success measure.
- Judge the NGO or the county, or say whether to fund.
- Cite savings figures from other governments as evidence for this proposal.
