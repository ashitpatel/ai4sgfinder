# Case 5: Matching young people to apprenticeships

| | |
|---|---|
| **Domain** | Youth employment and vocational training |
| **Intervention type** | Two-sided placement |
| **Expected class** | [Class 5: Strategic Matching Markets (stable matching)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) |
| **Most likely confusion** | Central assignment by an ML "best-fit" score |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/05-stable-matching-apprenticeships.md) |

## Scenario

A youth employment NGO places about 200 graduates of its vocational course into 6-month paid apprenticeships with 60 local employers each cohort. Employers offer 1–8 places each. Until now, staff assigned young people to employers by judgment.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> The resource is apprenticeship places, about 220 per cohort for 200 young people. The goal is to get them into a placement they finish, which usually leads to a job. Each cohort is placed once; a placement lasts 6 months. Whether it works depends a lot on whether both the young person and the employer wanted the match. Of your options, (a) is closest: each place is handed over once per cohort.

**Filter 2 — Choice and preferences.**
> Both sides choose. Young people have strong preferences about trade and location, and employers want to pick who they take. Last cohort, when we just assigned people, 30 young people turned down their placement or quit in the first month, and several employers refused candidates we sent and took someone from another program instead.

**Filter 3 — Environment dynamics.**
> Nobody avoids us, but some people game the system: young people sometimes list a less-wanted employer first because they think they have a better chance there.

**Filter 4 — Tolerance for being wrong.**
> A bad match costs a young person a placement and possibly their job prospects, and damages our employer relationships. It isn't life-threatening. We have records of past placements and completions, but no pilot or trial results.

**Filter 5 — Field data and workflow friction.**
> Placement happens twice a year. Young people can fill in a paper form; employers use email. Our placement officer uses Excel and would run it.

**Narrowing question — People choose.** *"Do individual people on both sides rank each other, such as students and schools, or does the community vote on how to split one budget among projects?"*
> Both sides rank each other. Each young person wants particular employers, and each employer wants particular young people. There's no vote and no shared budget.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> No. Training and stipends are the same for everyone placed.

## Why Class 5: Strategic Matching Markets

The assistant should select **[Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets)**, solved with deferred acceptance (stable matching).

- **Both sides hold preferences the planner must respect** (Filter 2 — Choice and preferences), with evidence that ignoring them causes refusals and dropouts. This overrides the *Who gets a limited resource* family suggested by Filter 1 and places the problem in the *People choose* family.
- **Both sides rank each other** (narrowing question), which is the decisive signal for Class 5: Strategic Matching Markets.
- The **strategic misreporting** in Filter 3 (Environment dynamics) is gaming, not an adversary, so the class stays the same and the rule must be hard to game. That is exactly what a well-designed matching mechanism provides: with young people proposing, honest ranking is their best strategy.
- Not [Class 6: Participatory Allocation](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation), the other *People choose* class: there is no community vote on how to split a shared budget among projects.
- Not [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists): the whole cohort is known at once, twice a year, rather than arriving one at a time, and both sides hold preferences over each other.
- No adversary, no catastrophic downside, and no repeated per-person decisions, so [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution), [Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) and [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) don't apply. [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) would impose a central assignment, which is what failed.

## What a good recommendation contains

**1. Class.** Deferred acceptance (Gale–Shapley), with young people proposing and employer capacities. It produces a *stable* match: no young person and employer both prefer each other over what they got, so there is nothing to defect to. With applicants proposing, it is safe for young people to rank honestly.

**2. Counterfactual warning.** A central assignment based on an ML "fit" score ignores what people actually want. It produces blocking pairs (a young person and an employer who would both rather be together), and those pairs leave the system: the refusals and early quits from last cohort. It also rewards gaming, because strategic ranking can pay off.

**3. Field pathway.** Young people rank up to 5 employers on a paper form; employers rank applicants or provide a scoring rule with a lottery for ties. The placement officer enters the lists into a spreadsheet and runs deferred acceptance (a short macro or a free online implementation; it runs in seconds). Publish the rules in plain language: "Rank employers in your true order of preference. Listing a popular employer first never hurts your chances."

**4. Evidence.** Deferred acceptance runs the US medical residency match (Roth & Peranson, AER 1999) and was adopted for New York City high-school admissions (Abdulkadiroğlu, Pathak & Roth, 2005) and Boston public schools (Abdulkadiroğlu, Pathak, Roth & Sönmez, 2005). The residency match is the closest parallel: workers and employers ranking each other, with employer capacities. Boston's switch is also the clearest documented case of replacing a mechanism that rewarded strategic ranking.

**5. Report card.**
- *Successes:* the NYC redesign substantially reduced the number of students assigned administratively to schools they had not ranked; the residency match has run stably for decades.
- *Challenges:* employers may need help producing rankings; staff must resist "fixing" results by hand after the match, which breaks the honesty guarantee.
- *Unknowns:* small markets with couples or linked requirements (e.g. two siblings needing the same town) can lack a stable match; check whether such constraints exist here.

**6. Simpler alternative.** Here the recommended method is itself the simple option: deferred acceptance can be run by hand, with one envelope per employer and rounds of proposals, or in a spreadsheet. The [tutorial's](../tutorials/05-stable-matching-apprenticeships.md#the-simpler-alternative-run-deferred-acceptance-by-hand) cohort of 200 young people and 60 employers needed 15 rounds. Check before running it by hand: employers' rankings (or scoring rules) are written down before the match; the tie-break lottery is drawn first, in public; no couples or linked placements. The tempting shortcut, "first choices first", is not close: it invites strategic ranking (Abdulkadiroğlu & Sönmez, 2003) and left dozens of blocking pairs per cohort in the tutorial.

**Next steps.** Draft the plain-language rules and the ranking forms; run the next cohort's match in parallel with staff assignment and compare; track refusals and first-month dropouts.

## What the assistant should *not* do

- Propose a welfare-maximizing central assignment (Class 2: Static Demographic Targeting) that ignores stated preferences.
- Claim that matching guarantees completion; it removes one cause of dropout, not all of them.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 5** in full: how deferred acceptance is set up for this program, and what to read before building it.

### Follow-up 1: Fit the model to your program

| Element | For this program | From |
|---|---|---|
| Two sides | About 200 graduates and 60 employers | Filter 2 — Choice and preferences |
| Capacities | 1–8 places per employer, about 220 in total | Filter 1 — The resource and its intent |
| Young people's preferences | Each ranks up to 5 employers on a paper form | Filter 5 — Field data and workflow friction |
| Employers' preferences | Each ranks only the applicants who listed it, or gives a scoring rule the placement officer applies | Filter 2 — Choice and preferences |
| Proposing side | **The young people.** With applicants proposing, ranking honestly is their best strategy, which removes the gaming described in Filter 3 — Environment dynamics | Filters 2 and 3 |
| Tie-breaking | One lottery number per young person, drawn in public | Filter 4 — Tolerance for being wrong |
| Special constraints | Ask: do any young people need placements in the same town (siblings), or near transport or accessible sites? | Filter 4 — Tolerance for being wrong |
| Rules to publish | "Rank employers in your true order of preference. Listing a popular employer first never hurts your chances." | Filter 4 — Tolerance for being wrong |

It should also flag a gap: there are more places (about 220) than young people (about 200), but anyone whose 5 choices all fill up stays unmatched. Plan a short second round in which unmatched young people rank the employers that still have places.

### Follow-up 5: Reading and people to contact

1. **Start with** Roth, *Who Gets What — and Why* (2015), a book for general readers by one of the designers of these matches. It explains stability and why honest ranking matters.
2. **Closest parallel:** Roth & Peranson (1999) on the redesign of the US medical residency match. Like apprenticeships, it matches workers to employers that have several places each.
3. **Switching from a gameable system:** Abdulkadiroğlu, Pathak & Roth (2005) on the New York City high-school match.
4. **For whoever builds it:** the documentation for the Python [matching](https://github.com/daffidwilde/matching) library, specifically its hospital–resident problem, which is this setup with employers as "hospitals."

**People to contact:** market-design economists publish widely on school choice and residency matching, and their papers name the organizations that ran each match. An economics department at a local university is the most practical first contact.

### The other follow-ups, in brief

- **2. Readiness checks:** confirm employers are willing to rank applicants; agree in writing that staff won't adjust results by hand after the match; check whether any placement involves a legal entitlement.
- **3. Pilot design:** run the match in shadow alongside staff assignment for one cohort, then compare refusals and first-month dropouts against last cohort's 30.
- **4. Build options:** the `matching` library's hospital–resident solver, or a short script; the placement officer keeps the lists in Excel. Among the twelve classes, this is one of the easiest to build.
- **6. Brief for a technical partner:** usually unnecessary here; a volunteer with basic Python can set it up from the table above.
