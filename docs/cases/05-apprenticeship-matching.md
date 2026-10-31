# Case 5: Matching young people to apprenticeships

| | |
|---|---|
| **Domain** | Youth employment and vocational training |
| **Intervention type** | Two-sided placement |
| **Expected class** | 5 — Strategic Matching Markets (stable matching) |
| **Most likely confusion** | Central assignment by an ML "best-fit" score |

## Scenario

A youth employment NGO places about 200 graduates of its vocational course into 6-month paid apprenticeships with 60 local employers each cohort. Employers offer 1–8 places each. Until now, staff assigned young people to employers by judgment.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — Resource and intent.**
> The resource is apprenticeship places, about 220 per cohort for 200 young people. The goal is to get them into a placement they finish, which usually leads to a job. Each cohort is placed once; a placement lasts 6 months. Whether it works depends a lot on whether both the young person and the employer wanted the match.

**Filter 2 — Choice and preferences.**
> Both sides choose. Young people have strong preferences about trade and location, and employers want to pick who they take. Last cohort, when we just assigned people, 30 young people turned down their placement or quit in the first month, and several employers refused candidates we sent and took someone from another program instead.

**Filter 3 — Environment dynamics.**
> Cooperative, but strategic: young people sometimes list a less-wanted employer first because they think they have a better chance there.

**Filter 4 — Tolerance for being wrong.**
> A bad match costs a young person a placement and possibly their job prospects, and damages our employer relationships. It isn't life-threatening. We have records of past placements and completions.

**Filter 5 — Field data and workflow.**
> Placement happens twice a year. Young people can fill in a paper form; employers use email. Our placement officer uses Excel.

## Why this class

- **Both sides hold preferences the planner must respect** (Filter 2), with evidence that ignoring them causes refusals and dropouts. This is the decisive signal for Class 5.
- The **strategic misreporting** in Filter 3 is exactly what a well-designed matching mechanism removes.
- No adversary, no catastrophic downside, and no repeated per-person decisions, so Classes 1, 3 and 4 don't apply. Class 2 would impose a central assignment, which is what failed.

## What a good recommendation contains

**1. Class.** Deferred acceptance (Gale–Shapley), with young people proposing and employer capacities. It produces a *stable* match: no young person and employer both prefer each other over what they got, so there is nothing to defect to. With applicants proposing, it is safe for young people to rank honestly.

**2. Counterfactual warning.** A central assignment based on an ML "fit" score ignores what people actually want. It produces blocking pairs (a young person and an employer who would both rather be together), and those pairs leave the system: the refusals and early quits from last cohort. It also rewards gaming, because strategic ranking can pay off.

**3. Field pathway.** Young people rank up to 5 employers on a paper form; employers rank applicants or provide a scoring rule with a lottery for ties. The placement officer enters the lists into a spreadsheet and runs deferred acceptance (a short macro or a free online implementation; it runs in seconds). Publish the rules in plain language: "Rank employers in your true order of preference. Listing a popular employer first never hurts your chances."

**4. Evidence.** Deferred acceptance runs the US medical residency match (Roth & Peranson, AER 1999) and was adopted for New York City high-school admissions (Abdulkadiroğlu, Pathak & Roth, 2005) and Boston public schools (Abdulkadiroğlu, Pathak, Roth & Sönmez, 2005). The residency match is the closest parallel: workers and employers ranking each other, with employer capacities. Boston's switch is also the clearest documented case of replacing a mechanism that rewarded strategic ranking.

**5. Report card.**
- *Successes:* the NYC redesign substantially reduced the number of students assigned administratively to schools they had not ranked; the residency match has run stably for decades.
- *Challenges:* employers may need help producing rankings; staff must resist "fixing" results by hand after the match, which breaks the honesty guarantee.
- *Unknowns:* small markets with couples or linked requirements (e.g. two siblings needing the same town) can lack a stable match; check whether such constraints exist here.

**Next steps.** Draft the plain-language rules and the ranking forms; run the next cohort's match in parallel with staff assignment and compare; track refusals and first-month dropouts.

## What the assistant should *not* do

- Propose a welfare-maximizing central assignment (Class 2) that ignores stated preferences.
- Claim that matching guarantees completion; it removes one cause of dropout, not all of them.
