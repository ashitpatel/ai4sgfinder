# Case 16: Which job-search support works, and for whom

| | |
|---|---|
| **Domain** | Youth employment |
| **Intervention type** | One of three job-search supports per participant |
| **Expected class** | [8 — Learn-While-Allocating (adaptive experiment)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating), with a [Class 7 — Effect-Based Targeting](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) layer that learns which support suits which group |
| **Combination** | [8 + 7: which option works, and for whom](../../prompt/knowledge/taxonomy.md#5-when-two-classes-combine) |
| **Most likely confusion** | [Case 9](09-sms-reminders-adaptive-experiment.md) (one best option for everyone) or [Case 8](08-business-grants-effect-targeting.md) (targeting from a finished trial) |
| **In-depth tutorials** | No separate tutorial. The two layers are taught in [adaptive experiments](../tutorials/09-adaptive-experiments-sms-reminders.md) (Thompson sampling with guards) and [policy learning](../tutorials/08-policy-learning-business-grants.md) (effects by subgroup, checked on held-out data) |

## Scenario

A youth-employment NGO in a large city enrolls about 160 young jobseekers a month. It can offer each one of three supports of similar cost: a **transport stipend** for six weeks of job hunting, a **CV-and-interview workshop**, or a **mentor** who meets them weekly. Nobody knows which works best, and staff have strong opinions that differ: some think the stipend matters most for people living far from the business district, others that the workshop only helps those who finished secondary school. The funder wants to know what to scale next year. Staff phone each participant six weeks after enrollment and record whether they have paid work.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> One of three supports for each young person we enroll: a transport stipend, a CV workshop or a mentor. The goal is paid work within six weeks.

*Next turn, which fits best:*
> (b), given again and again. Every month a new group enrolls and we decide what each gets.

**Filter 2 — Choice and preferences.**
> We assign it. Participants accept whatever support they're offered; almost nobody refuses.

**Filter 3 — Environment dynamics.**
> No one is avoiding us. Some might say they live farther away if they knew it meant a stipend, but we take addresses from their ID.

**Filter 4 — Tolerance for being wrong.**
> A weaker support for a month is a loss, not a disaster; they still get help.

*Next turn, what records:*
> Two years of enrollment forms (age, sex, education, neighborhood) and the six-week phone check. But until now staff chose the support, so we don't know what caused what.

**Filter 5 — Field data and workflow friction.**
> Enrollment is on a tablet form; the phone check happens six weeks later and goes into the same spreadsheet. Monthly cohorts.

*Next turn, who would run it:*
> Our M&E officer, who is comfortable with Excel and a little R.

**Narrowing — "Which describes your uncertainty better: how each person's situation changes from week to week, or which of several program options works best?"**
> Which option works best. Each person gets one support once.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> For whom. We suspect the best support is different for people far from the center, and for those without secondary school.

## Why Class 8 with a Class 7 layer

The assistant should select **[Class 8 (Learn-While-Allocating)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating)** as the primary class, an adaptive experiment across the three supports, with a **[Class 7 (Effect-Based Targeting)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting)** layer that lets the best support differ by group.

- **Several options of unknown value, outcomes in six weeks, monthly cohorts** (Filters 1, 4 and 5, narrowing). That is Class 8: learn which works while still serving people, shifting toward better options as results arrive.
- **The user expects the answer to differ by group** (second-decision question). That is the Class 7 question. But Class 7 needs randomized data, and the two years of records have none: staff chose the supports (Filter 4). The adaptive experiment *produces* the randomized data the targeting needs, which is why the two belong together, as in the refugee job-search experiment in Jordan (Caria et al., 2024).
- **Why Class 8 primary?** The funder's first question is which support to scale. Targeting is worth adding only if the groups really differ, which the experiment will show.
- **Not [Class 1 (Dynamic State Evolution)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution):** each person gets one support once; there is no state to track week to week (narrowing).
- **Gaming is limited** (Filter 3) because group membership comes from ID and the enrollment form, not from what a participant claims to qualify.

## What a good recommendation contains

**1. Class.** An adaptive experiment with a small number of groups, for example four (near or far from the center × with or without secondary school). Each month, every new participant is randomly assigned a support, with the chances in each group shifted toward the support doing best *in that group so far* (Thompson sampling within groups, or exploration sampling if the priority is choosing correctly at the end; Kasy & Sautmann, 2021). Guards: every support keeps at least 15% of each group, so learning continues, and the current most-used support stays as the comparison.

**2. Counterfactual warning.** Comparing past participants by the support staff gave them would mostly measure staff judgment: the people sent to mentors were chosen for a reason. A model trained on those records would learn the selection, not the effect. Picking one support for everyone on staff opinion risks scaling the wrong one, and slicing a small fixed trial into many subgroups would find "effects" that are noise.

**3. Field pathway.** The M&E officer keeps a sheet with each group's results by support (participants and number in work at six weeks) and, at the start of each month, a table of assignment shares per group. The enrollment tablet draws the support at random from the participant's group's shares, so staff never choose. A one-page monthly summary goes to the program manager.

**4. Evidence.** Caria, Gordon, Kasy, Quinn, Shami and Teytelboym (Journal of the European Economic Association, 2024) ran an adaptive, targeted experiment for job-search support among refugees and Jordanians with the International Rescue Committee, assigning treatments by group and shifting shares over time. It is the closest parallel. Its honest result matters as much: the targeting itself added little, about one percentage point of employment. Kasy and Sautmann (Econometrica, 2021) applied exploration sampling to choosing recruitment strategies for agricultural extension in India.

**5. Report card.**
- *Successes:* adaptive designs have been run by real organizations on monthly cycles, and they move participants toward better options during the experiment.
- *Challenges:* with about 160 people a month, four groups and three supports leaves around 13 people per cell per month; differences between groups take many months to show. Staff must accept that the tablet, not they, chooses the support.
- *Unknowns:* whether the supports differ much at all; whether they differ by group (Jordan suggests the gains from targeting can be small); whether six-week employment reflects lasting work.

**6. Simpler alternative.** A **fixed, stratified trial**: within each of the four groups, assign a third of participants to each support by lottery for nine months, then compare the share in work by support within each group in a spreadsheet, with margins of error, and choose. This is the equal split from the [adaptive-experiments tutorial](../tutorials/09-adaptive-experiments-sms-reminders.md#the-simpler-alternative-an-equal-split-then-switch) run separately in each group, and the subgroup comparison from the [policy-learning tutorial](../tutorials/08-policy-learning-business-grants.md#the-simpler-alternative-a-pivot-table-of-the-pilot). In what ways it is close: in the tutorial's simulations the equal split chose the best option nearly as often as the adaptive design; it gives the funder clean estimates with standard confidence intervals; and it is far easier to explain. What it gives up: some participants get a weaker support for the whole trial instead of a few months, which matters most if one support turns out much better. Check before settling for it: the number of groups stays at four or fewer (each extra group halves the sample per comparison); the groups are decided now, before any results; and the program can wait nine months for an answer. Given the Jordan result, a fixed stratified trial with a planned look at group differences is a strong first choice; the adaptive design earns its complexity if one support is likely to be clearly worse.

**Next steps.** Agree the four groups, the outcome and the trial length with the funder before enrollment opens; set the enrollment tablet to assign supports by lottery within groups; check whether the evaluation needs ethics approval.

## What the assistant should *not* do

- Train a model on the two years of staff-chosen records and call it the effect of each support.
- Promise that targeting will add much: cite the Jordan result.
- Split into many small groups, or choose the groups after seeing results.
- Let staff override the assignment case by case, which breaks the randomization both layers rely on.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 3** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

| Element | For this program | From |
|---|---|---|
| Options | Transport stipend, CV-and-interview workshop, mentor; similar cost | Filter 1 |
| Outcome | Paid work at the six-week phone check (yes/no) | Filters 1 and 5 |
| Batch | Monthly cohort of about 160 | Filter 5 |
| Groups (layer) | 4: near or far from the center × with or without secondary school, from ID and the enrollment form | Second decision; Filter 3 |
| Assignment rule | Random draw within each group from that group's shares; Thompson sampling updates the shares monthly | Filter 2 |
| Guards | At least 15% of each group on every support; the most-used current support as comparison | Filter 4 |
| Stopping | Fixed review at month 9; earlier only if one support is clearly worse in every group | Filter 4 |
| Analysis | Within-group comparisons with methods valid for adaptive data (Hadad et al., 2021), or the fixed trial's ordinary estimates | Filter 5 |

Gap to flag: **six-week outcomes arrive after the next two cohorts have enrolled.** Each month's shares can only use cohorts whose phone check is done, as in the [SMS tutorial's](../tutorials/09-adaptive-experiments-sms-reminders.md) two-week delay.

### Follow-up 3: Pilot design

The layers are piloted in order: first which support works, then for whom.

1. **Months 1–4: equal shares within groups.** Every group gets a third on each support. This gives clean early estimates and checks that random assignment works in practice: the tablet draws, staff accept the result, the phone check reaches people.
2. **Months 5–9: adapt if warranted.** If one support is clearly behind overall, start shifting shares (with the guards); if not, keep equal shares. Look at group differences only at month 9, with the comparisons agreed in advance.
3. **Decision rule for the funder:** scale one support for everyone unless a group difference is larger than its margin of error and makes sense to staff; then scale the group-specific rule and keep a 10% random share to keep checking it.
4. **Harm measure:** any group whose share in work falls below the program's past average.

### The other follow-ups, in brief

- **2. Readiness checks:** the tablet can assign by lottery; staff agree not to override; phone-check completion above 80% in every group; consent wording covers random assignment.
- **4. Build options:** Excel for the fixed trial; a short R or Python script for Thompson sampling, as in the [SMS tutorial](../tutorials/09-adaptive-experiments-sms-reminders.md). University economists or J-PAL-affiliated researchers often help design such trials. Confirm each tool and partner is still active before relying on it.
- **5. Reading and contacts:** Caria et al. (2024); Kasy & Sautmann (2021); Hadad et al. (2021) on analysis after adaptive assignment.
- **6. Brief:** the decision is which support to scale; the layer is for whom; under "Simpler option to beat", the fixed stratified trial.
