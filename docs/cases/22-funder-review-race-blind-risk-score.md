# Case 22: Funder review of a "race-blind" screening-outreach proposal

| | |
|---|---|
| **Domain** | Cancer screening |
| **Who is using the assistant** | A health foundation program officer reviewing a proposal |
| **Expected verdict** | **Fits**: [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), with conditions on how the score's fairness is checked |
| **Most likely confusion** | Accepting "we removed race, so the score is fair" |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal); [Fairness audit for a risk score](../../prompt/knowledge/playbook.md#fairness-audit-for-a-risk-score) |
| **Real-world pattern** | Emma Pierson and colleagues' work on race in risk prediction and on under-reported outcomes (see [Evidence check](#what-a-good-memo-contains)) |

## Scenario

A health foundation has a proposal from a (fictional) community health NGO. A partner hospital can give 2,000 free colonoscopies a year to uninsured adults over 45 in its county, and about 30,000 people are eligible. Today slots go first-come, first-served, mostly to people who already have a regular doctor. The NGO wants to build a risk score to decide whom its outreach workers call first.

*This is an illustrative scenario, not a real program or proposal. The fairness checks follow published work by Emma Pierson, Ziad Obermeyer and colleagues.*

## What the funder pastes

**The proposal, summarized.**
> A partner hospital will give 2,000 free colonoscopies a year to uninsured adults over 45 in our county; about 30,000 are eligible, and today slots go first-come, first-served. We will train a logistic regression on the hospital's records of past colonoscopy results (age, sex, family history, symptoms, BMI, smoking) to predict colorectal cancer risk. Outreach workers will call the 2,000 highest-risk people first. To make the model fair, we have removed race and ethnicity from it. Budget: US$90,000 over 18 months. Success measure: cancers and advanced polyps found per 100 colonoscopies.

**The funder's answers.**
> We fund health equity in one state. Grants are US$50,000–200,000 over one to two years. We fund early pilots if they are well designed. Equity across groups is a condition of every grant.

## Why the verdict is Fits, with conditions

Read against the filters:

- **Filter 1:** a test used to find something hidden (option (d)).
- **Filter 3:** no one evades it.
- **Filter 4:** a missed cancer is serious; past results exist, positives and negatives.
- **Filter 5:** hospital records; the NGO names a data analyst.
- **Narrowing question:** finding hidden problems, so Class 12. The method matches.

The method fits. The fairness claim does not follow from the design, for three reasons the memo should raise:

1. **Removing race doesn't make a score fair.** If a predictor works differently across groups, a race-blind model can under-predict risk for one of them. Zink, Obermeyer and Pierson (PNAS 2024) found this for colorectal cancer: family history predicted cancer for White participants but not for Black participants, probably because it was recorded less completely, and dropping race made the model under-predict risk for Black participants, sending them fewer referrals.
2. **The label may be biased.** "Cancer found at a past colonoscopy" exists only for people who got one. Groups with less access are under-diagnosed, so the model learns that they are low-risk. This is the label-choice problem of Obermeyer et al. (Science 2019), and the under-reporting problem Pierson's group addresses with positive-unlabeled methods.
3. **The success measure is blind to groups.** Finds per 100 can rise while one group's share of slots falls.

## What a good memo contains

1. **The decision:** which ~2,000 of ~30,000 eligible adults are called first for a free colonoscopy each year.
2. **Method fit:** *Fits* (Class 12). A risk ranking for a limited test with past results is the right class. Conditions: the fairness checks below, and a random share of outreach.
3. **The simpler option:** call in order of age (oldest first) plus anyone with symptoms, with a random share. Does the proposal plan to compare the score against it on past records, *for each group*?
4. **Questions for the NGO:**
   - Will you report the score's calibration (predicted against observed cancer rates) and its share of top-ranked slots separately by race, ethnicity, sex and insurance history? Race can be used to *check* the model even if it isn't an input.
   - Did you compare models with and without race, and with interactions such as race × family history, on calibration by group, not only overall accuracy?
   - Is family history recorded equally completely across groups? If not, how will the model avoid leaning on it?
   - The training labels come only from people who had a colonoscopy. How will you correct for groups who were rarely tested?
   - Will 10–20% of outreach go to people chosen at random, so the model can be checked against true rates?
5. **Risks to people:** under-referral of groups whose risk factors are poorly recorded; a score trained on who was tested repeats past gaps in access; people ranked low-risk may not be called at all, so keep first-come slots open alongside.
6. **Evidence check:** the proposal cites no deployment. Relevant verified research: Zink, Obermeyer and Pierson, *Race adjustments in clinical algorithms can help correct for racial disparities in data quality*, PNAS 2024 ([PMC11348319](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348319/)); Shanmugam, Hou and Pierson on correcting for under-reporting with positive-unlabeled learning ([arXiv 2110.04133](https://arxiv.org/abs/2110.04133)); Obermeyer et al. (Science 2019) on label choice.
7. **Funding stages:**
   1. A small grant to replay two years of records under the score (with and without race) and the age rule, reporting finds and calibration by group. Release stage 2 only if the chosen score is calibrated within each group.
   2. A one-year pilot with a random share and a group-level harm measure agreed in advance.
   3. Scale with an annual fairness audit and a named owner.

## What the assistant should not do

- Accept "race removed" as a fairness check, or insist race must be an input; the point is to *measure* by group either way.
- Recommend Class 7 (Effect-Based Targeting): a colonoscopy here is a test, not a treatment whose effect varies.
- Judge the NGO or say whether to fund it.
- Cite the PNAS finding as showing the same result would hold in this county.
