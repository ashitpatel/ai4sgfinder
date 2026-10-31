# Case 1: Community health worker visits for hypertension

| | |
|---|---|
| **Domain** | Primary health care |
| **Intervention type** | Recurring behavioral nudge (home visits) |
| **Expected class** | 1 — Dynamic State Evolution (restless bandits) |
| **Most likely confusion** | A standard risk-prediction model ranking "highest-risk" patients |

## Scenario

A county health NGO enrolls 1,200 adults with diagnosed hypertension. Its 10 community health workers (CHWs) can each make about 8 adherence-support home visits a week, so 80 of 1,200 patients can be visited in any given week. Every patient gets a weekly SMS reminder; the question is who gets the scarce in-person visit.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> Our resource is CHW home visits: about 80 per week across 1,200 patients. The goal is to keep people taking their blood-pressure medication. A visit isn't permanent: if we visit someone this week, that slot is free again next week. Whether it works depends entirely on the patient; some respond well to a visit, some would keep taking their pills anyway, and some won't change no matter what.

**Filter 2 — Choice and preferences.**
> We decide centrally who gets visited. Patients have consented to the program but don't choose their visit schedule, and they can't really "refuse" in a way that matters to planning.

**Filter 3 — Environment dynamics.**
> Cooperative. Patients aren't avoiding us. But their adherence changes over time on its own: people who are doing well tend to slip after a few weeks, and the effect of a visit fades.

**Filter 4 — Tolerance for being wrong.**
> A wrong choice in one week isn't catastrophic; the SMS still goes out and we can visit next week. Over months, though, poor targeting means more uncontrolled blood pressure and strokes. We have about 9 months of weekly adherence records.

**Filter 5 — Field data and workflow friction.**
> CHWs record a yes/no adherence check (pill count) at every contact on a phone app that syncs when they reach signal, roughly weekly. The M&E officer uses Excel. CHWs just want a list of who to see.

## Why Class 1: Dynamic State Evolution

The assistant should select **Class 1 (Dynamic State Evolution)**, solved with restless bandits.

- **Reclaimable, probabilistic resource** (Filter 1 — The resource and its intent): a visit is time, re-routable weekly, and its value depends on the patient's response. That rules out Class 2 (Static Demographic Targeting), which is for permanent transfers.
- **Central assignment** (Filter 2 — Choice and preferences) rules out Class 5 (Strategic Matching Markets). **No adversary** (Filter 3 — Environment dynamics) rules out Class 3 (Spatiotemporal Security & Adaptive Search).
- **Exploration is tolerable** and there is history (Filter 4 — Tolerance for being wrong), so the worst-case protection of Class 4 (Robust Contingency Planning) isn't needed.
- **States drift whether or not you act**, and the visit's effect decays (Filter 3 — Environment dynamics): this is the "restless" structure. Each patient is an arm whose state (adhering / lapsing) moves on its own and moves differently when visited.
- **Weekly per-patient observations exist** (Filter 5 — Field data and workflow friction), which restless bandits require.

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

## Follow-up example: brief for a technical partner

After the recommendation, the assistant offers six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md). If the user picks **6. One-page brief for a technical partner**, a good answer fills the template from the interview, like this:

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
  Class 1 (Dynamic State Evolution): a restless multi-armed bandit with a
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

The other five follow-ups would, for example, map arms to patients and states to adhering / lapsing (Fit the model), flag the 9 months of history as just sufficient if patients are grouped (Readiness checks), and recommend randomizing CHW areas between the model's list and current practice for 8–12 weeks (Pilot design).
