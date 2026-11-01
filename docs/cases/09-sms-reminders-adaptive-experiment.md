# Case 9: Choosing the best vaccination-reminder SMS while still sending it

| | |
|---|---|
| **Domain** | Child immunization |
| **Intervention type** | Repeated message to new recipients (SMS reminder wording) |
| **Expected class** | [8 — Learn-While-Allocating (adaptive experimentation)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) |
| **Most likely confusion** | [Class 1 (Dynamic State Evolution)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution), because the reminders go out every week; or "no model needed, just run a four-arm randomized trial" |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/09-adaptive-experiments-sms-reminders.md) |

## Scenario

A district immunization NGO sends an SMS reminder to parents a few days before each child's vaccination date. About 400 new parents enter the reminder list every week as their children reach a due date. The team has written four wordings: the current plain reminder (A), one that names the child (B), one that stresses protection from disease (C), and one that says most parents in the area vaccinate on time (D). Nobody knows which gets more children vaccinated on time, and there is no data comparing them.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We send an SMS reminder to parents before each child's vaccination date. We have four different wordings and don't know which gets more children vaccinated on time. Every parent gets a reminder; the question is which one.

*Next turn (which fits it best):*
> (b), given again and again. A new group of about 400 parents gets it every week.

**Filter 2 — Choice and preferences.**
> We decide which message each parent gets. Parents don't choose a wording.

**Filter 3 — Environment dynamics.**
> No one avoids us. Parents aren't gaming anything; they just forget or get busy.

**Filter 4 — Tolerance for being wrong.**
> A weaker message costs a few late vaccinations, which clinics catch up later at the next visit or outreach day. It's a small, fixable loss.

*Next turn (records):*
> We have no data comparing the wordings. We've only ever sent wording A, and we know roughly what share of children are vaccinated on time with it.

**Filter 5 — Field data and workflow friction.**
> The clinic system records each vaccination within a week, and we can match it to the phone number on our list. Messages go out through a bulk-SMS platform where we upload a spreadsheet.

*Next turn (who runs it):*
> Our M&E analyst. She can change the message mix every week; she uses Excel and some R.

**Narrowing — "Which describes your uncertainty better: how each person's situation changes from week to week, or which of several program options works best?"**
> Which wording works best. Each parent only gets one or two reminders for a given vaccination, so there's no week-to-week situation to track.

## Why Class 8: Learn-While-Allocating

The assistant should select **[Class 8 (Learn-While-Allocating)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating)**, solved with an adaptive experiment (Thompson sampling or exploration sampling).

- **Given again and again** (Filter 1 — The resource and its intent), **decided centrally** (Filter 2 — Choice and preferences) and **no one avoiding the program** (Filter 3 — Environment dynamics) place the problem in the *Repeated decisions that learn* family. That rules out [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets), [Class 6 (Participatory Allocation)](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation) and [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search).
- **Small, fixable errors and no history** (Filter 4 — Tolerance for being wrong) make learning acceptable, so the worst-case protection of [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) isn't needed. With no trial results, [Class 7 (Effect-Based Targeting)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) has nothing to learn *who* responds from.
- **Outcomes arrive within about a week** and the mix can change weekly (Filter 5 — Field data and workflow friction), which is the minimum data Class 8 needs.
- **The narrowing answer decides it:** the uncertainty is which of four stable options works best, not how each parent's situation drifts. [Class 1 (Dynamic State Evolution)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) would need repeated observations of each parent over many weeks; here each parent receives one or two reminders and leaves the list.

## What a good recommendation contains

**1. Class.** An adaptive experiment across the four wordings. Each week, the analyst updates how likely each wording is to be the best, using the on-time vaccination results so far, and sends more of the next week's reminders with the wordings that look better. Thompson sampling gives each wording a share equal to its probability of being best; exploration sampling (Kasy & Sautmann) shifts some of that share back toward close contenders so the final choice is more reliable. Two guards stay fixed: a **floor share for every wording** (e.g. 10%) and a **fixed control share on wording A** (e.g. 20%), the current message. A **stopping rule** is agreed in advance: stop when one wording has at least a 95% probability of being best, or after 10 weeks, whichever comes first.

**2. Counterfactual warning.** A plain A/B test with fixed equal shares sends 25% of parents to each wording for the whole trial, so three quarters of parents keep getting a weaker message long after the data show it is weaker. The adaptive design spends fewer reminders on the losers. Picking a wording by staff vote, or by which one "sounds best", locks in a guess. A restless-bandit model (Class 1) would build per-parent state tracking that this program has no use for.

But be honest about when a **fixed randomized trial is still better**: if a donor or the ministry needs a clean evaluation with a precise effect estimate for every wording, a fixed-arm trial gives that more simply. Adaptive designs collect fewer observations on the weaker wordings, so their effects are estimated less precisely; the floor share limits this but does not remove it.

**3. Field pathway.** Each Monday the analyst pastes last week's matched outcomes (sent wording, vaccinated on time yes/no) into a spreadsheet that recomputes the four shares, then randomly assigns the week's 400 parents to wordings in those shares and uploads the file to the SMS platform. Clinic staff see nothing different. If the analyst is away, the fallback is a written rule: send the current shares unchanged.

**4. Evidence.** Kasy & Sautmann (Econometrica, 2021) introduced exploration sampling and applied it to recruitment strategies for an agricultural extension service in Odisha, India: a different domain, but the same structure (several outreach options, outcomes within weeks, assignment shifted between waves). Caria et al. (Journal of the European Economic Association, 2024) ran an adaptive targeted field experiment on job-search assistance for refugees in Jordan, funded by the International Rescue Committee. Xu et al. (AAAI, 2021) on LIZARD is a bandit method evaluated on historical poaching data from Cambodia, not a field deployment, and is a distant parallel at most.

**5. Report card.**
- *Successes:* both field experiments show adaptive assignment can be run by real organizations on a weekly or wave-by-wave cycle.
- *Challenges:* in the Jordan experiment the targeting algorithm's gain was small, about 1 percentage point of employment. Say so plainly: the adaptive design mainly avoids waste during learning; it does not make a weak message strong. Matching vaccination records to phone numbers, and the one-to-two-week outcome delay, are the practical friction here.
- *Unknowns:* whether the four wordings differ much at all. With about 4,000 parents over 10 weeks, wordings that differ by a point or two may never separate; the stopping rule should then end with "no clear winner, keep A". Whether the best wording differs between groups (first-time parents, rural areas) is also open.

**Next steps.** Write down the outcome (vaccinated within 7 days of the due date), the shares, the floor, the control and the stopping rule before the first week; check whether the evaluation needs ethics approval and whether parents' enrolment covers using their records this way; build and test the weekly spreadsheet on last month's wording-A data.

## What the assistant should *not* do

- Recommend restless bandits (Class 1) because the reminders are weekly; nothing about each parent is tracked over time.
- Say "no model needed, just run a four-arm randomized trial" without explaining the trade-off. A fixed trial is a fair choice if a clean evaluation is required, but it should be named as a choice, not the default.
- Drop the floor share or the fixed control on wording A, or use "no SMS" as a control, which would withhold a reminder parents currently get.
- Quote an effect size from the Odisha study, or present the Jordan result as a large gain, or call LIZARD a deployment.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

A good answer maps every element of an adaptive experiment to this program, citing the interview answer it came from:

| Element | For this program | From |
|---|---|---|
| Options | Four wordings: A (current), B (child's name), C (protection), D (most parents vaccinate on time) | Filter 1 — The resource and its intent |
| Outcome and delay | Child vaccinated within 7 days of the due date; known about one to two weeks after the reminder | Filters 1 and 5 — Field data and workflow friction |
| Batch size | About 400 new parents per week | Filter 1 — The resource and its intent |
| Assignment rule | Thompson sampling, or exploration sampling if the main goal is to pick one wording at the end | Filter 4 — Tolerance for being wrong |
| Groups | One group to start; first-time vs. returning parents only if numbers allow | Filter 2 — Choice and preferences |
| Stopping rule | One wording at least 95% likely to be best, or 10 weeks | Filter 4 — Tolerance for being wrong |
| Floor per option | At least 10% per wording, plus 20% fixed on wording A as control | Ethics |

It should also flag the gap that matters most: **outcomes lag the decision.** A parent reminded this week is recorded next week or the week after, so each update uses results from two weeks earlier. That is fine, but the analyst must update only on parents whose due date has passed by at least 7 days, or late records will look like failures.

### Follow-up 6: One-page brief for a technical partner

If the user picks **6**, a good answer fills the playbook template from the interview:

```
PROJECT BRIEF — District vaccination reminder program (illustrative)

The decision we need help with
  Each week, decide which of four SMS reminder wordings each of about
  400 new parents receives before their child's vaccination date.

Why it matters
  Late vaccinations leave children unprotected for longer. We don't know
  which wording gets the most children vaccinated on time.

Current approach
  Everyone gets wording A. We have no data comparing wordings.

Recommended approach
  Class 8 (Learn-While-Allocating): an adaptive experiment using Thompson
  sampling or exploration sampling, because the options are stable,
  outcomes arrive within weeks, and a weaker message costs little.

Data we have
  Clinic records of each vaccination, entered within a week, matched to
  the phone numbers on our reminder list. No past comparison data.

Constraints
  About 400 parents per week; one or two reminders per parent. At least
  10% per wording, 20% fixed on wording A. At most 10 weeks.

What success looks like
  Share vaccinated within 7 days of the due date, by wording. Harm
  measure: on-time rate in any week falling below wording A's usual rate.

How results must reach staff
  The M&E analyst updates a spreadsheet each Monday and uploads the
  assignment file to our bulk-SMS platform. Clinic staff see no change.

What we are asking for
  Review of our design and stopping rule, and help building the weekly
  spreadsheet before a 10-week run.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** outcomes are recorded within a week (ready); the analyst can switch shares weekly (ready); the phone-number-to-clinic-record match needs testing on past data (partly ready); ethics approval if the wordings are treated as research and results will be published, and confirmation that enrolment covers this use of records (not yet checked).
- **3. Pilot design:** the adaptive experiment is itself the pilot, with the fixed share on wording A as the benchmark; run 4–10 weekly rounds, as the playbook suggests.
- **4. Build options:** no package needed; Thompson sampling is a few lines of R or a spreadsheet, which matches the analyst's skills. For a design review, Statistics Without Borders or a local university statistics or economics department are realistic partners. Confirm any partner is still active before relying on it.
- **5. Reading and contacts:** start with Caria et al. (2024) on the Jordan refugee experiment, then Kasy & Sautmann (2021) for exploration sampling. Lily Xu at Columbia works on bandit methods for public health and conservation.
