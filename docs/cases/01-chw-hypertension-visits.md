# Case 1: Community health worker visits for hypertension

| | |
|---|---|
| **Domain** | Primary health care |
| **Intervention type** | Recurring behavioral nudge (home visits) |
| **Expected class** | [Class 1: Dynamic State Evolution (restless bandits)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) |
| **Most likely confusion** | A standard risk-prediction model ranking "highest-risk" patients |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/01-restless-bandits-chw-visits.md) |

## Scenario

A county health NGO enrolls 1,200 adults with diagnosed hypertension. Its 10 community health workers (CHWs) can each make about 8 adherence-support home visits a week, so 80 of 1,200 patients can be visited in any given week. Every patient gets a weekly SMS reminder; the question is who gets the scarce in-person visit.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> Our resource is CHW home visits: about 80 per week across 1,200 patients. The goal is to keep people taking their blood-pressure medication. A visit isn't permanent: if we visit someone this week, that slot is free again next week. Whether it works depends entirely on the patient; some respond well to a visit, some would keep taking their pills anyway, and some won't change no matter what. Of your options, it's (b): given again and again, every week.

**Filter 2 — Choice and preferences.**
> We decide centrally who gets visited. Patients have consented to the program but don't choose their visit schedule, and they can't really "refuse" in a way that matters to planning.

**Filter 3 — Environment dynamics.**
> No. Patients aren't avoiding us, and there's nothing to game: they don't apply for visits. But their adherence changes over time on its own: people who are doing well tend to slip after a few weeks, and the effect of a visit fades.

**Filter 4 — Tolerance for being wrong.**
> A wrong choice in one week isn't catastrophic; the SMS still goes out and we can visit next week. Over months, though, poor targeting means more uncontrolled blood pressure and strokes. We have about 9 months of weekly adherence records, but no pilot or trial results.

**Filter 5 — Field data and workflow friction.**
> CHWs record a yes/no adherence check (pill count) at every contact on a phone app that syncs when they reach signal, roughly weekly. The M&E officer uses Excel and would run the tool. CHWs just want a list of who to see.

**Narrowing question — Repeated decisions that learn.** *"Which describes your uncertainty better: how each person's situation changes from week to week, or which of several program options works best?"*
> How each person's situation changes. We only have one option, a home visit. What we don't know is who is slipping this week and who a visit would bring back.

## Why Class 1: Dynamic State Evolution

The assistant should select **[Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution)**, solved with restless bandits.

**Stage 1 places the problem in the *Repeated decisions that learn* family.**
- **Given again and again** (Filter 1 — The resource and its intent): a visit is time, re-routable weekly, and its value depends on the patient's response. That is option (b), and it rules out [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting), which is for permanent transfers.
- **Central assignment** (Filter 2 — Choice and preferences) rules out [Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) and [Class 6: Participatory Allocation](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation). **No one avoids the program or games it** (Filter 3 — Environment dynamics), which rules out [Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search).
- **Exploration is tolerable** and there is history (Filter 4 — Tolerance for being wrong), so the worst-case protection of [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) isn't needed.
- **Weekly per-patient observations exist** (Filter 5 — Field data and workflow friction), which restless bandits require.

**Stage 2 picks Class 1 over Class 8.**
- The uncertainty is **how each patient's situation changes** (narrowing answer), not which option works. States drift whether or not you act, and the visit's effect decays (Filter 3 — Environment dynamics): this is the "restless" structure. Each patient is an arm whose state (adhering / lapsing) moves on its own and moves differently when visited.

**Closest neighbours ruled out.**
- [Class 8: Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) is for several options of unknown but stable value. Here there is one option, and what changes is each patient, which Class 8 assumes away.
- [Class 7: Effect-Based Targeting](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) also asks who a visit would change, but it needs a randomized pilot (there is none, Filter 4) and suits a program offered once, not a choice that repeats every week as people drift.
- [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection) is where a "highest-risk first" list belongs. It finds hidden problems; here the goal is to change behavior, and the patients most likely to lapse are not always the ones a visit helps.

## What a good recommendation contains

**1. Class.** Restless multi-armed bandit with a Whittle index policy. Each week, compute for every patient an index measuring how much a visit *now* improves their long-run adherence compared with waiting, and visit the top 80.

**2. Counterfactual warning.** A risk model ranks patients by how likely they are to lapse. That sends visits to people who will lapse whether visited or not, and to the same high-risk patients every week, where the effect of repeated visits fades. It ignores *who changes because of the visit*. A static spreadsheet rotation (everyone visited every 15 weeks) wastes visits on stable adherers.

**3. Field pathway.** The M&E officer runs the model weekly (a script or a hosted notebook) on the synced data and exports one sheet per CHW: "Visit these 8 patients this week," with village and phone number. CHWs never see an index. If the sync fails, CHWs use last week's printed list plus a standing rule: visit anyone who missed two consecutive pill counts.

**4. Evidence.** The closest parallel is the ARMMAN mMitra field study (Mate et al., AAAI 2022), which used a restless-bandit policy to choose which enrolled mothers received a live health-worker call; the structural match is direct (limited weekly contacts, drifting engagement, central choice). Collapsing Bandits (Mate et al., NeurIPS 2020) applies the same model to tuberculosis medication adherence. Both rest on Whittle (1988).

**5. Report card.**
- *Successes:* the mMitra study reported fewer engagement drops under the bandit policy than under the comparison groups.
- *Challenges:* per-patient transition probabilities must be estimated from little data, usually by grouping similar patients; staff need to trust a list they can't see the reasoning for.
- *Unknowns:* fairness. A pure index policy can leave some patients unvisited for months. Recommend a minimum-contact guarantee (e.g. everyone visited at least once a quarter) and monitor who is never chosen.

**Next steps.** Clean the 9 months of adherence data into a patient × week table; pilot the list in 2 of 10 CHW areas with the rest as comparison; agree the minimum-contact rule with the medical lead.

## What the assistant should *not* do

- Recommend a deep-learning model; the data volume doesn't support it and the problem is sequential decision-making, not prediction.
- Quote a specific percentage improvement from the mMitra study unless it is certain of the figure.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

A good answer maps every element of a restless bandit to this program, citing the interview answer it came from:

| Element | For this program | From |
|---|---|---|
| Arms | The 1,200 enrolled patients | Filter 1 — The resource and its intent |
| Action | One CHW home visit; at most one per patient per week | Filter 1 — The resource and its intent |
| Budget per round | 80 visits a week (10 CHWs × 8) | Filter 1 — The resource and its intent |
| States | *Adhering* or *lapsing*, read directly from the weekly yes/no pill count | Filter 1; Filter 5 — Field data and workflow friction |
| Round length | One week, matching how often the app syncs | Filter 5 — Field data and workflow friction |
| Reward | Number of patients adhering each week | Filter 1 — The resource and its intent |
| Transition estimates | From the 9 months (about 39 weeks) of records. That is too few per patient, so group patients with similar adherence histories and estimate per group | Filter 4 — Tolerance for being wrong |
| Fairness guard | Every patient visited at least once a quarter, agreed with the medical lead | Ethics |

It should also flag the one gap that matters most: **the model needs to know which weeks each patient was visited.** Without past visit records it can only learn how adherence drifts *without* a visit, not how a visit changes it. If visits weren't logged, start logging them now; the pilot will then supply the missing estimates.

### Follow-up 6: One-page brief for a technical partner

If the user picks **6**, a good answer fills the playbook template from the interview:

```
PROJECT BRIEF — County hypertension adherence program (illustrative)

The decision we need help with
  Each week, choose which 80 of 1,200 enrolled hypertension patients
  receive a community health worker (CHW) home visit.

Why it matters
  About 1,200 adults depend on daily blood-pressure medication. Poorly
  targeted visits mean more uncontrolled blood pressure and strokes.

Current approach
  CHWs visit by judgment and rotation. Visits go repeatedly to the same
  patients, and stable adherers get visits they don't need.

Recommended approach
  Class 1: Dynamic State Evolution: a restless multi-armed bandit with a
  Whittle index policy, because a visit is reclaimable weekly, its effect
  depends on the patient, adherence drifts over time, and we observe it weekly.

Data we have
  About 9 months of weekly yes/no adherence checks (pill counts) per
  patient, entered by CHWs on a phone app that syncs when in signal.

Constraints
  80 visits per week (10 CHWs x 8). Every patient must be visited at least
  once a quarter. CHWs often work without connectivity.

What success looks like
  Fewer patients moving from adhering to lapsing, compared with current
  practice. Harm measure: the number of patients unvisited for 90+ days.

How results must reach staff
  One printed or SMS list per CHW each Monday ("visit these 8"). The M&E
  officer reruns the model weekly in Excel or a notebook.

What we are asking for
  Help building a 3-month pilot in 2 of our 10 CHW areas, with the other
  areas as comparison.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** 9 months of history is just enough if patients are grouped; check that all CHWs record pill counts the same way; confirm patients' consent covers using adherence data to plan visits; name who reruns the list each Monday.
- **3. Pilot design:** randomly split the 10 CHW areas between the model's list and current practice for 8–12 weeks; compare how many patients move from adhering to lapsing; watch the number unvisited for 90+ days as the harm measure.
- **4. Build options:** there is no ready-made package for restless bandits, only research code (such as `online-rmab` from the playbook), so this needs a data scientist. DataKind, the Data Science for Social Good Fellowship, or a university computer-science or operations-research department are the realistic partners.
- **5. Reading and contacts:** start with Google Research's blog post on ARMMAN, then the AAAI 2022 field study (Mate et al.). Milind Tambe's Teamcore group at Harvard and Lily Xu at Columbia work on exactly this problem.
