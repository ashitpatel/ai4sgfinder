# Case 17: Funder review of a risk-score home-visit proposal

| | |
|---|---|
| **Domain** | Primary health care |
| **Who is using the assistant** | A foundation program officer reviewing a proposal |
| **Expected verdict** | **Mismatch**: the decision is [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution); the proposal uses a risk score |
| **Most likely confusion** | Accepting the risk model because it predicts lapses accurately |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal) |

## Scenario

A regional health foundation has received a two-year proposal from a community health NGO. The NGO's 14 health workers can make about 110 home visits a week to 1,800 enrolled adults with diabetes. It wants funding to build a machine-learning model that predicts which patients are most likely to stop taking their medication, and to visit the 110 highest-risk patients each week.

*This is an illustrative scenario, not a real program or proposal.*

## What the funder pastes

**The proposal, summarized.**
> We will train a gradient-boosted model on 14 months of weekly adherence checks, clinic visits and demographics to predict each patient's risk of lapsing in the next month. Every Monday, health workers receive the 110 highest-risk names. Similar AI programs have cut hospital admissions by 40%. Budget: US$180,000 over two years, including a data scientist for 18 months. Success measure: the share of high-risk patients visited.

**The funder's answers.**
> We fund primary care in three districts. Grants are usually US$50,000–250,000 over one to three years. We'll fund an early pilot if it's well designed, but we want to see results before scaling.

## Why the verdict is Mismatch

Read against the filters, the proposal says enough to classify the decision:

- **Filter 1:** the visit is given again and again, every week (*repeated*).
- **Filter 3:** no one avoids the program; patients' adherence drifts on its own.
- **Filter 4:** a wrong week is fixable, but poor targeting over months costs health. There are 14 months of weekly records and no trial.
- **Filter 5:** weekly data on an app, and a data scientist who would run the model.
- **Narrowing question:** the uncertainty is how each patient's situation changes week to week, so the decision is Class 1.

The proposed method answers a different question. A risk score ranks who is likely to lapse, not whom a visit will bring back. Some high-risk patients lapse whatever happens; some low-risk patients slip only if no one visits. A restless bandit, or the simple table below, chooses by the expected *gain from a visit*. In the Class 1 tutorial's illustrative data, a risk score gained almost nothing over no targeting.

The success measure makes the problem worse: "share of high-risk patients visited" rewards following the list, not better adherence.

## What a good memo contains

1. **The decision:** which 110 of 1,800 patients get a home visit each week.
2. **Method fit:** *Mismatch.* Repeated visits to people whose state drifts is Class 1. A lapse-risk ranking measures need, not the effect of a visit, so it can send visits to people they won't help.
3. **The simpler option:** the six-cell table from [taxonomy Section 4](../../prompt/knowledge/taxonomy.md#4-simpler-alternatives-for-each-class): for each group and adherence state, the difference a visit makes, visiting the highest each week. The proposal compares against nothing.
4. **Questions for the NGO:**
   - What happens to adherence after a visit, compared with weeks without one? The 14 months of records can show this.
   - Will the success measure change to adherence or blood-sugar control, with a harm measure for patients never visited?
   - Will you replay last year's records under the risk list, the six-cell table and current practice before building?
   - Who maintains the model after the data scientist's 18 months?
   - Is there a minimum-contact rule, so no patient goes unvisited for months?
5. **Risks to people:** patients ranked low-risk may never be visited; a risk score can be less accurate for some groups. Check accuracy by group.
6. **Evidence check:** "cut hospital admissions by 40%" has no source and is not among the verified references: *unverified, ask for the citation*. The closest verified evidence is ARMMAN's restless-bandit field study (Mate et al., 2022), which used the effect of a call, not risk.
7. **Funding stages:**
   1. A small grant (about two months) to replay last year's records under the three options. Release stage 2 only if a targeted option clearly beats current practice on adherence.
   2. A six-month pilot in one district, randomizing patients between the chosen list and current practice.
   3. Scale to three districts with a named maintenance owner and a written fallback rule. At 1,800 patients with weekly records, the program could pass the three-part test for an evaluation later.

## What the assistant should not do

- Accept the method because the model would predict lapses accurately. Accuracy at predicting risk is not the question.
- Judge the NGO's capacity or say whether to fund it.
- Repeat the 40% figure as if it were evidence.
- Interview the funder through all five filters when the proposal already answers them.
