# Replay kit and health check

Excel workbooks that replay a program's past records under its current practice, a simple rule and, if a partner built one, a model. They answer the question AI4SG Finder asks before any build: **does the model beat the simple option on our own records by enough to be worth its cost?**

The workbooks run on your own computer. Nothing is uploaded, and no names are needed: an ID that only your staff can link to a person is enough. Every result is a formula, so the sheets recalculate when you paste in your own records. They use only common functions (`COUNTIFS`, `SUMIFS`, `INDEX`, `MATCH`) and should open in Excel, Google Sheets, LibreOffice and Numbers. They were checked in Excel for Mac.

| Workbook | For | Classes | What it compares |
|---|---|---|---|
| [1. Pick N once](1-pick-n-once.xlsx) | A one-off choice of who or what gets something: transfers, filters, places, sites to inspect | [2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting), [12](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection) | How many of each rule's choices turned out to be in need (or to have the hazard), and what share of everyone in need each rule reached, overall and by group |
| [2. Weekly visit list](2-weekly-visit-list.xlsx) | A choice made again each week about the same people: home visits, calls, tutoring | [1](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) | The expected extra people on track the next week from each rule's visits, and how visits split across groups |
| [3. Waitlist](3-waitlist.xlsx) | People who arrive over time and wait for a fixed number of places each week | [10](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists) | Weeks waited under two ordering rules you set and under current practice: for the urgent, the longest-waiting and each group |
| [4. Monthly health check](4-monthly-health-check.xlsx) | After launch: any program choosing whom to serve with a model, score or ranked list | Any that rank people or places | Each month: whether staff follow the list, whether its picks beat a random share, whether its scores match outcomes, and how each group fares |

Download them from this folder or from the latest [release](https://github.com/ashitpatel/ai4sgfinder/releases/latest). Each workbook opens on a **Read me** sheet with the steps. Yellow cells with blue text are yours to edit; grey cells are calculated. The sample records are made up and only show the format: replace them with yours.

## How to use it

**1. Pick the workbook.** AI4SG Finder names it when your recommendation's class has one: *Pick N once* for Classes 2 and 12, *Weekly visit list* for Class 1, *Waitlist* for Class 10. You can also choose by the decision in the table above. For other classes there is no workbook yet; the playbook's [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) says how to make the comparison with a partner.

**2. Check you have the records.** Each workbook needs one row per person, site or applicant, with an ID rather than a name:

| Workbook | Columns you fill in | The one that matters most |
|---|---|---|
| 1. Pick N once | Group; up to three facts you could rank by; whether current practice chose them; a model's score (optional); the outcome learned later | The later outcome, for everyone on the list or a random sample of it |
| 2. Weekly visit list | Week; ID; group; on track this week; visited; on track next week; a risk score (optional) | Whether they were on track the *next* week, recorded the same way every week |
| 3. Waitlist | ID; group; arrival week; priority points; the week actually served | Arrival and service weeks for everyone, including those still waiting |
| 4. Monthly health check | Month; ID; group; picked by the tool; served; in the random share; score; outcome; simple-rule pick (optional) | The random share: a few served each month from those the tool didn't pick |

If the key column is missing, start recording it now; the replay can run next year.

**3. Run it.** Open the workbook. Set the numbers on *Settings* (slots, visits or places per round, any minimum per group, the simple rule's points or weights). Replace the sample rows on *Data* with yours, in the yellow columns only. Read *Results* (or *Report* for the health check). It takes an hour or two once the records are in one table.

**4. Decide.** Read the results overall and by group:
- **The simple rule comes within a few percent of the model:** use the simple rule. Write it down for staff and recheck it yearly.
- **The model is clearly better and the gap is worth its full cost** (building it, keeping the data flowing, staff time, maintenance): pilot it against current practice, as the playbook's pilot design describes.
- **Neither beats current practice:** keep it, and look again at what the decision is trying to achieve.
- **One rule leaves a group behind:** set a minimum for that group and run it again.

**5. Share the result.** Put the figures, not the records, in the partner brief (AI4SG Finder's Follow-up 6 asks for them), in a proposal, or in a report to a funder: the funder review's first funding stage is exactly this test. You can also paste the summary figures into a conversation with AI4SG Finder and ask what they mean.

**After launch,** use the monthly health check each month (see below).

## What AI4SG Finder does with the kit

The assistant points to the workbook for your class, by name and link, where it tells you to test on past records: in the recommendation's *simpler option*, the readiness check *Simpler option tested*, pilot design, the partner brief and a funder's review memo. Pilot design also asks for a random share and the monthly health check after launch. It never asks for your records in the chat; if you share a workbook's summary figures, it interprets them. The one-click links don't carry the playbook, so they won't mention the kit unless you ask.

## What a replay can and can't tell you

A replay shows what each rule would have chosen from the same records and compares those choices. It can't show what would have happened to people under a rule nobody used, because those outcomes were never recorded. Each workbook is built around what *can* be measured honestly:

- **Pick N once** needs an outcome learned later for **everyone on the list, or a random sample of it**, such as a survey of all applicant households. If you only learn the outcome for the people you chose (you only find lead in the homes you inspect), the replay will flatter your current rule. Add a small random share to next round's choice first.
- **Weekly visit list** estimates what a visit does from your past weeks: how often people in each group and situation were on track the next week with and without a visit. If staff chose whom to visit, that comparison can be off, so the workbook flags cells with few records; a small random share of visits each week makes next year's table trustworthy. It counts only the next week's gain.
- **Waitlist** assumes the same people arrive in the same weeks whatever the rule, the places are fixed and nobody leaves the list. When every place is filled every week, **every ordering gives the same average wait**: the rules differ only in *who* waits. The workbook therefore reports the urgent, the longest waits and the groups.

If the simple rule comes within a few percent of the model, it is usually the better choice: it costs less, staff can explain it, and it keeps working when a volunteer leaves.

## What the sample records show

The samples are illustrative, but each one shows a pattern the [taxonomy](../../prompt/knowledge/taxonomy.md#4-simpler-alternatives-for-each-class) describes.

**1. Pick N once.** 1,000 households in four districts, 200 transfers, at least 30 per district. A later survey found 237 in need.

| Rule | In need among the 200 chosen | Share of all in need reached |
|---|---|---|
| Current practice | 60 | 25% |
| Simple points rule (household size, no land, woman-headed) | 103 | 43% |
| A partner's model | 104 | 44% |
| Random choice | about 47 | 20% |

The points rule comes within one household of the model. The by-group table shows they differ in *where* they reach people: the model leaves the West district with 10 reached against the points rule's 15.

**2. Weekly visit list.** 150 patients in three groups over 12 weeks, 20 visits a week.

| Rule | Expected extra patients on track, per 100 visits |
|---|---|
| Current practice (highest risk first, plus some easy-to-reach) | 15.7 |
| Table rule (visit where a visit helped most) | 38.9 |
| Risk score alone | 15.4 |
| Random visits | 20.8 |

Ranking by risk does worse than random visits here, because it sends visits to people a visit barely moves; [Tutorial 1](../../docs/tutorials/01-restless-bandits-chw-visits.md) finds the same against simple rotation. The table rule also sends 93% of visits to one group, which is why the workbook shows the split.

**3. Waitlist.** 299 applicants over 26 weeks, 10 places a week.

| | Current practice | First come, first served | Urgent first, with waiting time |
|---|---|---|---|
| Average weeks waited | 1.7 | 1.7 | 1.7 |
| Urgent applicants | 2.1 | 1.8 | 0 |
| Longest wait | 5 | 4 | 9 |
| Waited more than 8 weeks | 0 | 0 | 11 |
| Town / villages | 1.2 / 2.4 | 1.6 / 1.8 | 1.7 / 1.8 |

The average doesn't move. Current practice favours the town, where people can call in; urgent-first serves the urgent at once but makes 11 others wait more than eight weeks.

## After launch: the monthly health check

The first three workbooks help decide whether to adopt a tool. The fourth checks, month by month, that a tool in use is still working. Add each month's records, set the month to report, and read one page with a status for each check:

| Check | Marked *Check* when |
|---|---|
| Records considered | They change by more than 25% from the month before, which often means a recording problem |
| Staff follow the list | Fewer than 80% of the tool's picks are served |
| Overrides | More than 20% of those served were neither picked nor in the random share |
| Random share | Under 5% of those served, too few to tell whether the tool beats chance |
| Outcomes recorded | Under 80% of those served |
| Tool's picks against the random share | The tool's hit rate is less than 5 points above the random share's, over up to three months; *Too few to tell* under 30 random-share outcomes |
| Calibration, overall and by group | The average score differs from the outcome rate by more than 5 points, over up to three months, once there are 30 outcomes |
| Group shares | A group's share of those served differs from its share of those considered by more than 10 points |
| Overlap with a simple rule | 90% or more, a *Note*: the tool may not be worth its cost |

Every threshold is a setting. *Check* means look and talk, not change the tool automatically. It pairs steps 2, 4, 5 and 6 of the playbook's [fairness audit](../../prompt/knowledge/playbook.md#fairness-audit-for-a-risk-score) with the playbook's readiness check on recorded overrides, and the one-page report can go to a funder or board as it is.

**The sample** is a home-inspection program: 400 homes considered a month, 50 picked, 12 inspected at random. From August a new hazard source the model never saw appears, mostly in the South; from October staff who know about it set aside about a third of the list for South homes. The November report marks *Check* on staff following the list (66% of picks served), overrides (27%), calibration (scores 13 points below the outcome rate, 22 points in the South) and the group shares (South +15 points). The tool's picks still find hazards far more often than the random share (57% against 30%). Read together, the checks say the overrides are information: the model needs recalibrating with the new source.

## For contributors

The workbooks are generated by [`scripts/build_replay_kit.py`](../../scripts/build_replay_kit.py), which needs `openpyxl` (`pip install openpyxl`); the sample data uses fixed seeds. The generated files carry no cached values, so Excel computes them on opening. Before committing a change, recalculate each workbook in Excel and compare its results with an independent recomputation in Python: all four matched exactly when they were made (2026-11-22), and the health check was also tested on its first month, when there is too little to judge. The kit is not part of `scripts/build.py --check`.
