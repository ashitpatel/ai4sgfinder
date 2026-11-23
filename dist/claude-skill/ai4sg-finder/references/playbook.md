# AI4SG Implementation Playbook

What to do after an approach has been chosen. The AI4SG Finder assistant uses this file for its six follow-ups and for the funder review at the end; people can also read it directly.

**Reading this yourself?** Each follow-up starts with what it gives you: [1. Fit the model to your program](#follow-up-1-fit-the-model-to-your-program), [2. Readiness checks](#follow-up-2-readiness-checks) (including the [fairness audit for a risk score](#fairness-audit-for-a-risk-score)), [3. Pilot design](#follow-up-3-pilot-design), [4. Tools and partners](#follow-up-4-build-options--tools-and-partners) (including [what it takes](#what-it-takes-effort-costs-roles-and-timeline): effort, costs, roles and timeline), [5. Reading and people to contact](#follow-up-5-reading-and-people-to-contact), [6. A brief for a technical partner](#follow-up-6-one-page-brief-for-a-technical-partner). Before a session: [questions to settle before you start](#questions-to-settle-before-you-start). Testing a simple rule on your own records: [the replay kit](#the-replay-kit-testing-the-simple-option-on-the-programs-own-records). Funders, or an NGO checking its own proposal: see [Funder review](#funder-review-checking-a-proposal). Paragraphs headed *For the assistant* or *Rules for the assistant* are instructions to the model.

Tools, organizations and links were last checked on **2026-10-30**; a few, such as Fairlearn and OpenSAFELY, were added in November 2026. Services change: confirm that a tool or partner is still active before relying on it.

**For the assistant.** Offer the follow-ups after the recommendation and deliver one per turn, on request. Fill every template from the user's own interview answers, quoting their numbers and wording. Where an answer is missing, say what you need instead of guessing. Recommend only tools, partners and readings listed here, or ones you are certain exist; anything else must be labeled *"(unverified — please confirm)"*.

**When the user can't answer a question,** state a reasonable assumption, mark it *[to check]*, and carry on rather than stalling. If several key facts are missing, offer the *questions to settle before you start* below as a short list they can take to colleagues, and say the recommendation can be revisited once they have the answers.

**Never ask for, or work on, records about named people.** If a user pastes names, phone numbers, IDs or case notes, don't repeat or analyse them; say briefly why (the chat sends them to an outside service), and ask instead for counts, the fields that exist and how often they are recorded. Comparisons on past records (the simpler option against the model, the fairness audit) run on the program's own computer, in a spreadsheet or with a partner under a data agreement, never inside the chat. For three common decisions, a one-off choice of who gets something, a weekly visit list and a waitlist, point users to the [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit): Excel workbooks that do the comparison on their own computer.

### The replay kit: testing the simple option on the program's own records

The [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) is four free Excel workbooks a program runs on its own computer. Point to the one that matches the class, by name and link, wherever these instructions say to test on past records: in the recommendation's *Simpler option*, the readiness check *Simpler option tested*, pilot design, the partner brief and the funder memo's funding stages. Never ask for the records in the chat; if the user later shares the summary figures from a workbook, interpret them.

| Class | Workbook | What the program needs |
|---|---|---|
| 2 Static Demographic Targeting, 12 Risk-Based Inspection, and one-off choices in 7 | *1. Pick N once* | One row per person or site considered, with an outcome learned later for everyone or a random sample of them |
| 1 Dynamic State Evolution | *2. Weekly visit list* | One row per person per week: whether they were on track, visited, and on track the next week |
| 10 Online Assignment & Waitlists, when people wait for a fixed number of places | *3. Waitlist* | One row per applicant: arrival week, priority points, the week actually served |
| Any class whose tool ranks people or places, once it is in use | *4. Monthly health check* | Each month's records, including a random share served from those the tool didn't pick |

For other classes there is no workbook: the comparison is done with a partner ([Follow-up 3](#follow-up-3-pilot-design) lists how for each class). The one-click links don't carry this file, so users of those links won't hear of the kit unless they ask.

### Questions to settle before you start

The interview goes faster, and lands on the right class, when a program has these answers ready. They are worth settling with the people who run the work day to day, not only the person who will use the assistant.

1. **The decision.** What is handed out or scheduled, to whom, how often, and who decides today? Write it as one sentence: "Each week we choose which 80 of 1,200 patients get a home visit."
2. **The numbers.** How many people, sites or items are eligible, and how many can be served each round?
3. **The records.** Which facts are recorded about each person or site, how often, on what (paper, Excel, an app), and for how many past rounds? Is the outcome you care about recorded, and when?
4. **The current rule and its problems.** How the decision is made now, what goes wrong, and who complains.
5. **The stakes.** What harm a wrong choice causes, and which groups must be treated fairly.
6. **Who would run it.** Who would update a list or sheet each round, with what skills and time, and who maintains it after a partner leaves.
7. **Who wants it.** Whether a funder, a board or a vendor is asking for AI, and what they expect.

Answer what you can; "we don't know" is a useful answer, because it shows what the first month should find out.

---

## Follow-up 1: Fit the model to your program

Translate the chosen class into the user's terms. Fill each row from the named filter, and flag any row the user hasn't answered.

The filters: **Filter 1** The resource and its intent · **Filter 2** Choice and preferences · **Filter 3** Environment dynamics · **Filter 4** Tolerance for being wrong · **Filter 5** Field data and workflow friction.

### Class 1 — [Dynamic State Evolution](taxonomy.md#class-1-dynamic-state-evolution) (restless bandits)

| Element | Meaning | Comes from |
|---|---|---|
| Arms | The individuals or units who could receive the intervention (each beneficiary, household, classroom) | Filter 1 |
| Action | What "acting on" an arm means (a visit, a call, a session) and how many actions per round | Filter 1 |
| Budget per round | How many arms can be acted on each round (e.g. 80 visits a week) | Filter 1 |
| States | The few observable conditions an arm can be in (e.g. adhering / lapsing; engaged / disengaged). Keep it to 2–3. | Filters 1 and 5 |
| Round length | How often the decision is remade; must match how often states can be observed | Filter 5 |
| Reward | What counts as success each round (e.g. number of people in the "good" state) | Filter 1 |
| Transition estimates | How likely each state is to change with and without action, estimated from history, usually by grouping similar people | Filters 4 and 5 |
| Fairness guard | A minimum-contact rule so no one is ignored indefinitely | Ethics |

### Class 2 — [Static Demographic Targeting](taxonomy.md#class-2-static-demographic-targeting) (welfare optimization)

| Element | Meaning | Comes from |
|---|---|---|
| Decision | What is being chosen (which sites, which households, how much each region gets) | Filter 1 |
| Candidates | The full list of options, with the data known about each | Filters 1 and 5 |
| Objective | What is maximized (people covered, welfare gain, need met) | Filter 1 |
| Budget and capacity limits | Total budget, number of units, per-site capacity | Filter 1 |
| Fairness rule | e.g. every district reaches at least X%, or maximize the worst-off group (maximin / leximin) | Filters 2 and 4 |
| Hard constraints | Legal, technical or political rules (drillable sites only, one per village) | Filter 4 |
| Audit output | What must be published to justify the choice | Filter 4 |

### Class 3 — [Spatiotemporal Security & Adaptive Search](taxonomy.md#class-3-spatiotemporal-security--adaptive-search) (security games)

| Element | Meaning | Comes from |
|---|---|---|
| Targets | The grid cells, zones or sites to protect | Filter 3 |
| Defender resources | Patrol units and how many targets each can cover per period | Filter 1 |
| Adversary model | Who evades you, what they gain at each target, how quickly they adapt | Filter 3 |
| Risk model inputs | Past incidents, patrol effort, terrain, access points | Filter 5 |
| Detection bias | Where incidents are only recorded because you patrolled there | Filter 5 |
| Schedule format | How the randomized plan reaches staff (weekly paper calendar) | Filter 5 |
| Operational limits | Fuel, distance, weather, safety | Filter 4 |

### Class 4 — [Robust Contingency Planning](taxonomy.md#class-4-robust-contingency-planning) (robust optimization)

| Element | Meaning | Comes from |
|---|---|---|
| First-stage decision | What must be committed before the event (stock levels, locations) | Filter 1 |
| Second-stage decision | What can be adjusted after the event (dispatch, reallocation) | Filter 1 |
| Uncertainty | What is unknown (where it hits, how severe, which roads fail) | Filters 3 and 4 |
| Scenarios or uncertainty set | The historical events plus plausible unseen ones | Filter 4 |
| Robustness level | How far from history to protect (larger is safer but costlier) | Filter 4 |
| Cost of excess | Spoilage, storage and capital cost of over-preparing | Filter 4 |
| Offline outputs | Dispatch cards usable without connectivity | Filter 5 |

### Class 5 — [Strategic Matching Markets](taxonomy.md#class-5-strategic-matching-markets) (stable matching)

| Element | Meaning | Comes from |
|---|---|---|
| Two sides | Who is matched to whom (students and schools, youth and employers) | Filter 2 |
| Capacities | Places each provider offers | Filter 1 |
| Preferences | How each side ranks the other: ranked lists, scores, or priority rules | Filter 2 |
| Proposing side | Which side proposes in deferred acceptance; that side can rank honestly without risk | Filter 2 |
| Tie-breaking | Lottery or rule for equal priorities | Filters 2 and 4 |
| Special constraints | Couples, siblings, quotas, accessibility needs | Filter 4 |
| Rules to publish | Plain-language explanation that honest ranking is safe | Filter 4 |

### Class 6 — [Participatory Allocation](taxonomy.md#class-6-participatory-allocation) (participatory budgeting)

| Element | Meaning | Comes from |
|---|---|---|
| Budget | The amount the community decides on, and who guarantees it will be spent as voted | Filter 1 |
| Project list | Costed, feasible proposals, vetted by staff before the vote | Filters 1 and 4 |
| Electorate | Who may vote (residents, youth, members) and how identity is checked | Filter 2 |
| Ballot format | Approval (tick any), ranking, or knapsack (build a bundle within the budget) | Filters 2 and 5 |
| Aggregation rule | How ballots become funded projects: greedy by votes, or proportional (method of equal shares) | Filter 2 |
| Fairness guard | Minimum shares for districts or groups with low turnout | Ethics |
| Voting channel | Paper ballots, kiosks, SMS or web, matched to connectivity | Filter 5 |

### Class 7 — [Effect-Based Targeting](taxonomy.md#class-7-effect-based-targeting) (policy learning)

| Element | Meaning | Comes from |
|---|---|---|
| Program | The one-off or rare offer (a grant, a training place, a nudge) and how many can receive it | Filter 1 |
| Trial data | The randomized pilot or past trial: who was offered it, their characteristics, their outcomes | Filter 4 |
| Outcome | The single measure the program should move, and when it is measured | Filter 1 |
| Characteristics | What is known about each applicant at decision time, and only that | Filter 5 |
| Rule form | A short, explainable rule (a small decision tree or score cut-off) staff can apply | Filter 5 |
| Need floor | Any group that must be served regardless of estimated effect | Filters 2 and 4 |
| Gaming check | Characteristics that applicants could change or misreport to qualify | Filter 3 |

### Class 8 — [Learn-While-Allocating](taxonomy.md#class-8-learn-while-allocating) (adaptive experimentation)

| Element | Meaning | Comes from |
|---|---|---|
| Options | The program variants, messages or sites being compared (keep it to 2–6) | Filter 1 |
| Outcome and delay | What counts as success and how soon after each decision it is known | Filters 1 and 5 |
| Batch size | How many people or sites are assigned per round | Filter 1 |
| Assignment rule | Thompson sampling or exploration sampling; how much effort the weaker options keep | Filter 4 |
| Groups | Subgroups whose best option may differ (refugees and locals, districts) | Filter 2 |
| Stopping rule | When to stop learning and commit to the best option | Filter 4 |
| Floor per option | A minimum share for every option, so the final comparison stays valid | Ethics |

### Class 9 — [Routing & Logistics](taxonomy.md#class-9-routing--logistics) (vehicle routing and network design)

| Element | Meaning | Comes from |
|---|---|---|
| Network | Sources, warehouses, delivery points and the roads or routes between them | Filters 1 and 5 |
| Demand | How much each point needs, and when (time windows) | Filter 1 |
| Fleet and capacity | Vehicles, their loads, warehouse space, working hours | Filter 1 |
| Costs | Fuel, purchase prices, driver time, storage, spoilage | Filter 1 |
| Decisions | Which depots, what to buy where, how much on each route, stop order | Filter 1 |
| Hard rules | Delivery deadlines, nutrition or quality standards, road or security closures | Filters 3 and 4 |
| Output format | Daily route sheets or a weekly plan staff can follow offline | Filter 5 |

### Class 10 — [Online Assignment & Waitlists](taxonomy.md#class-10-online-assignment--waitlists) (online allocation)

| Element | Meaning | Comes from |
|---|---|---|
| Arrivals | Who or what arrives (families, housing units, donations), and how often | Filter 2 |
| Destinations | Where each can go, and each one's capacity for the season or year | Filter 1 |
| Value of a placement | The outcome that matters (employment, stable housing, food used before it spoils), predicted if possible | Filters 1 and 4 |
| Forecast | Expected future arrivals, from past records, so capacity is not used up too early | Filter 4 |
| Fairness over time | Rules that must hold across the whole season (shares by group or region) | Filter 2 and ethics |
| Decision speed | How quickly each placement must be made, and by whom | Filter 5 |
| Override | When staff may set the suggestion aside, and how that is recorded | Ethics |

### Class 11 — [Network Seeding](taxonomy.md#class-11-network-seeding) (influence maximization)

| Element | Meaning | Comes from |
|---|---|---|
| Population | The community in which the message or behavior should spread | Filter 1 |
| Network data | Who knows whom: a survey, a cheap proxy (asking who spreads news well), or existing records | Filter 5 |
| Seeds | How many people you can train or brief | Filter 1 |
| Spread model | How likely a contact is to pass it on; usually estimated roughly | Filter 4 |
| Participation | Chance that an invited seed agrees and attends; plan backups | Filter 4 |
| Outcome | What spreading should change (awareness, testing, a farming practice) | Filter 1 |
| Privacy | How network data is collected, stored and kept from misuse | Ethics |

### Class 12 — [Risk-Based Inspection](taxonomy.md#class-12-risk-based-inspection) (predictive inspection)

| Element | Meaning | Comes from |
|---|---|---|
| Units | The homes, sites, businesses or people that could be inspected | Filter 1 |
| Hidden problem | What an inspection finds (lead pipe, violation, infection) | Filter 3 |
| Inspection budget | How many inspections per period | Filter 1 |
| Risk features | What is known about each unit before inspection (age of building, past findings, location) | Filter 5 |
| Past inspections | Every past inspection with its result, including those that found nothing | Filter 5 |
| Exploration share | A small random share of inspections, so the model also learns about rarely checked places | Filter 4 |
| Action on findings | What happens when a problem is found, and who pays for it | Filter 1 |

### No model needed

Write down the simple rule, who applies it, and the one or two numbers to track monthly that would show a model has become worthwhile.

### Simpler option, for any class

When the user would rather start with the simpler option from the [taxonomy's Section 4](taxonomy.md#4-simpler-alternatives-for-each-class), fit it the same way: write the rule in the user's terms (the columns of their spreadsheet, or the steps on paper), name who applies it and how often, list the assumptions it rests on with how each will be checked, and name the sign that it has stopped being close enough (for example, a district left with nothing, or last year's replay showing a growing gap).

---

## Follow-up 2: Readiness checks

Go through these with the user; mark each as ready, partly ready, or not ready, and say what to do about each gap.

**For every class**
- **Decision owner.** One named person or team will use the output and is authorized to act on it.
- **Data.** The required fields exist, are recorded consistently, and cover the people or places the model will decide about. Gaps fall unevenly on some groups?
- **Consent and privacy.** People whose data is used were told, in words they understand, and agreed; personal data is stored securely; the model can run on pseudonymized IDs. Before data goes to an outside partner, replace names and phone numbers with random IDs (hashing phone numbers is not enough, since they are easy to guess) and coarsen exact GPS points to village or grid cell. Put in writing that scores are used only to direct help, never to deny entitlements, trigger enforcement or penalize people who don't respond.
- **Fairness.** Decide in advance which groups must not be disadvantaged and how that will be measured.
- **Do-no-harm.** Who loses out under the new allocation compared with today, and is that acceptable and explainable?
- **Maintenance.** Someone can rerun the model, fix the data pipeline and answer staff questions a year from now, after the original builder leaves.
- **Exit plan.** If the model fails or the partner leaves, staff can fall back to a written simple rule.
- **Simpler option tested.** The best simple option for the class ([taxonomy, Section 4](taxonomy.md#4-simpler-alternatives-for-each-class)) has been replayed on past records alongside the model, and the gap is worth the model's full cost: building it, the data pipeline, staff time each cycle and maintenance. The [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) does this in Excel for a one-off choice of N (Classes 2 and 12), a weekly visit list (Class 1) and a waitlist (Class 10).
- **Community voice.** Affected people or their representatives have seen and can question the approach.
- **Bias in risk scores.** If any step uses a predicted score, run the [fairness audit for a risk score](#fairness-audit-for-a-risk-score) below. A health algorithm that predicted costs instead of illness under-referred Black patients (Obermeyer et al., Science 2019).
- **Scoring the people you serve.** If a score flags beneficiaries for fraud, overpayment or loss of eligibility, the program has a legal basis, a person reviews every flag before anything happens, flagged people can see why and appeal, the fairness audit is published, and the score has been compared with how caseworkers choose today ([taxonomy, Section 7](taxonomy.md#when-a-score-targets-the-people-you-serve)). If not, don't pilot it.
- **Input layers.** If the program relies on speech recognition, document extraction, a screening classifier, a forecast, a ready-made map or a published prediction model, its error has been measured on the program's own data, by language or group, and there is a manual fallback ([taxonomy, Section 6](taxonomy.md#6-input-layers)).
- **Human override.** Staff know when they may set the model's suggestion aside, and each override is recorded and reviewed. Overrides are information about where the tool is wrong or unworkable; count them monthly.
- **Advisory or binding.** Decide whether the output advises a person or decides on its own, and write it down. A person in the loop isn't a safeguard by default: in an experiment, people largely followed an AI's biased hiring recommendations unless the bias was severe (Wilson et al., 2025). Show staff the reason for each suggestion, and check how often they disagree.
- **Threshold matched to capacity.** Where a score or alert sends people or cases to staff, set the threshold from how many staff can act on, not from the score alone, and track how many flags go unanswered.
- **Review before use.** Someone outside the build team reviews the model's data, accuracy and ethics before it informs a decision, as in OCHA's peer review framework for humanitarian predictive models. For a public agency, publish the assessment, including what it couldn't check (the UK DWP's published fraud-model fairness assessment could analyse only one protected characteristic).
- **Contract terms.** If a vendor builds or runs the model, the contract says who owns the data and the model, gives the program the right to audit it and see its accuracy by group, and lets the program leave with its data.
- **Analyse where the data lives.** If records are too sensitive to share, prefer a partner who runs approved code inside the record holder's systems and takes out only aggregate results (OpenSAFELY in England) over copying the data.

**Class-specific**
- *[Class 1: Dynamic State Evolution](taxonomy.md#class-1-dynamic-state-evolution) (restless bandits):* At least several months of per-person history at the planned round length; states recorded the same way by all staff; agreement on a minimum-contact rule.
- *[Class 2: Static Demographic Targeting](taxonomy.md#class-2-static-demographic-targeting) (welfare optimization):* Reliable location and population data; the fairness rule agreed by stakeholders **before** results are seen; backup options if a chosen site proves infeasible.
- *[Class 3: Spatiotemporal Security & Adaptive Search](taxonomy.md#class-3-spatiotemporal-security--adaptive-search) (security games):* Patrol logs with location and effort, not just incidents; leadership accepts randomized schedules; sensitive schedules kept confidential.
- *[Class 4: Robust Contingency Planning](taxonomy.md#class-4-robust-contingency-planning) (robust optimization):* A scenario set reviewed by local experts, including events worse than any on record; funders accept that robust plans carry extra stock.
- *[Class 5: Strategic Matching Markets](taxonomy.md#class-5-strategic-matching-markets) (stable matching):* Both sides willing to submit rankings; a commitment not to override results by hand; legal review if placements involve public entitlements.
- *[Class 6: Participatory Allocation](taxonomy.md#class-6-participatory-allocation) (participatory budgeting):* A budget formally committed to the vote's outcome; the aggregation rule published before voting opens; outreach to groups that rarely vote.
- *[Class 7: Effect-Based Targeting](taxonomy.md#class-7-effect-based-targeting) (policy learning):* Randomized pilot data with at least a few thousand participants; the characteristics used are available for new applicants; stakeholders accept not serving some needy people who are unlikely to benefit.
- *[Class 8: Learn-While-Allocating](taxonomy.md#class-8-learn-while-allocating) (adaptive experimentation):* Outcomes recorded within weeks; staff able to switch options between rounds; ethics approval if the options are research treatments.
- *[Class 9: Routing & Logistics](taxonomy.md#class-9-routing--logistics) (vehicle routing):* Accurate locations and travel times; current costs; drivers and warehouse staff involved in checking the plan.
- *[Class 10: Online Assignment & Waitlists](taxonomy.md#class-10-online-assignment--waitlists) (online allocation):* At least a year of arrival records; agreed fairness rules for the season; a way to explain each placement to the person affected.
- *[Class 11: Network Seeding](taxonomy.md#class-11-network-seeding) (influence maximization):* Consent for collecting network data; enough staff to train the chosen seeds; a measure of spread that can be collected later.
- *[Class 12: Risk-Based Inspection](taxonomy.md#class-12-risk-based-inspection) (predictive inspection):* Records of past inspections including negative results; a plan to act on what is found; a check that the risk score does not simply send inspectors back to the neighborhoods they already over-inspect.

### Fairness audit for a risk score

For any step that ranks or screens people by a predicted score (Classes 2, 10 and 12 most often), and for any proposal a funder reviews that uses one. Work through it with the user on past records, before the pilot; mark each item as done, partly done or not done.

1. **What the label measures.** Name the outcome the score was trained on and ask whether it is the thing that matters. Cost is not illness (Obermeyer et al., 2019). "Diagnosed" or "found at a past inspection" is not "has it": groups who were tested less look lower-risk than they are, and methods for under-reported outcomes exist (Shanmugam, Hou & Pierson, 2021). If the label is biased, fix the label before the model.
2. **Calibration by group.** For each group that must not be disadvantaged, compare predicted rates with observed rates. A score can rank well overall and still under-predict for one group, which sends that group fewer slots.
3. **With and without group variables.** Removing race, sex or another group variable is not a fairness check. If a predictor is recorded less reliably for one group (family history, past diagnoses), a model without the group variable can under-predict that group's risk (Zink, Obermeyer & Pierson, 2024). Compare both versions, and interactions between the group and that predictor, on step 2. Whether a group variable may legally be an input differs by country and sector: check, but use it to *measure* either way.
4. **Share of slots by group.** Under the score, under the simpler rule and under current practice, what share of slots does each group get, against its share of the need?
5. **A random share.** Keep 10–20% of slots chosen at random among those the score would not pick, so its misses can be measured, by group, after the pilot.
6. **Recheck after the pilot and yearly.** Repeat steps 2 and 4 on new results; populations and recording practices change. Once a tool is in use, the [monthly health check](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) tracks steps 2, 4 and 5 each month, with overrides and whether the tool still beats its random share.

If the program asks whether past *decisions* were discriminatory (for example in enforcement or service records), that is a research question for a partner, not part of this audit. Point to outcome and threshold tests, and to designs comparing the same person recorded differently (Gera & Pierson, 2024, arXiv 2409.11269), and suggest an academic partner.

**Tools.** [scikit-learn](https://scikit-learn.org/stable/modules/calibration.html) draws calibration curves; [Fairlearn](https://fairlearn.org) reports accuracy and selection rates by group. Both are free; a spreadsheet pivot table of predicted against observed rates by group does steps 2 and 4 for a small program.

---

## Follow-up 3: Pilot design

Recommend the smallest pilot that can show the approach works better than current practice.

**For every class**
- **Compare against current practice**, not against nothing, and where possible also against the best simple option for the class ([taxonomy, Section 4](taxonomy.md#4-simpler-alternatives-for-each-class)). A model that can't beat a good spreadsheet rule in the pilot shouldn't be scaled.
- **For combined classes, pilot the input layer first.** A forecast trigger, risk map or outcome prediction is tested before the decision that depends on it ([taxonomy, Section 5](taxonomy.md#5-when-two-classes-combine)).
- **Pick one or two success measures** agreed before the pilot starts, plus one harm measure (who might be worse off).
- **If the AI is the intervention** (a tutor, a coach, an adviser), measure an outcome, not usage: learning, health, income, not messages sent. Compare it with current practice, or with the same support without AI, and grade a sample of its answers against an expert's ([taxonomy, Section 7](taxonomy.md#when-the-ai-is-the-intervention)).
- **If a model measures the outcome** (satellite images, phone data, image grading), check it against a direct measure on a sample first: a proxy can miss an effect a survey finds. Keep the direct measure on a random sample throughout, so the estimate stays valid ([taxonomy, Section 7](taxonomy.md#when-a-model-measures-the-outcome)).
- **Replay first.** Before the pilot, run the simple option, current practice and the model on last year's records: with the [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) for Classes 1, 2, 10 and 12 (see *The replay kit* above), or with a partner for the others.
- **Plan the check after launch.** Keep a random share of slots chosen from those the tool doesn't pick, record overrides, and review the kit's monthly health check each month, so drift and unfairness show up early.
- **Fix the duration** up front and the conditions for stopping early.
- **Keep it reversible.** The old process stays available.

| Class | Practical comparison | Typical duration |
|---|---|---|
| [1 — Dynamic State Evolution](taxonomy.md#class-1-dynamic-state-evolution) | Randomly split beneficiaries (or field areas) between the model's list and the current method; compare outcomes such as engagement or adherence | 6–12 rounds (e.g. weeks) |
| [2 — Static Demographic Targeting](taxonomy.md#class-2-static-demographic-targeting) | Usually a one-off decision, so compare plans rather than run a trial: model plan vs. current ranking on the same budget, scored on coverage and fairness, reviewed by stakeholders | 1–2 months of analysis |
| [3 — Spatiotemporal Security & Adaptive Search](taxonomy.md#class-3-spatiotemporal-security--adaptive-search) | Alternate model-generated and usual schedules by period or zone; compare detections per patrol hour, while noting that deterrence shows up as fewer detections over time | One season or 3+ months |
| [4 — Robust Contingency Planning](taxonomy.md#class-4-robust-contingency-planning) | Backtest: replay past events and expert-designed "unseen" scenarios against the model's plan and the current plan; run a tabletop exercise with the dispatch cards | Before the risk season |
| [5 — Strategic Matching Markets](taxonomy.md#class-5-strategic-matching-markets) | Run the match in shadow alongside the current process for one cohort, then compare refusals, early dropouts and satisfaction | One placement cycle |
| [6 — Participatory Allocation](taxonomy.md#class-6-participatory-allocation) | Run one cycle and count the ballots under both the current rule and the proposed one; compare which groups' projects win and survey voters on fairness | One budgeting cycle |
| [7 — Effect-Based Targeting](taxonomy.md#class-7-effect-based-targeting) | Within the next cohort, randomly assign applicants to selection by the learned rule or by the current need ranking; compare outcomes per person served | One program cohort |
| [8 — Learn-While-Allocating](taxonomy.md#class-8-learn-while-allocating) | The adaptive design is itself the pilot; keep a fixed share on the current option as a benchmark | 4–10 rounds |
| [9 — Routing & Logistics](taxonomy.md#class-9-routing--logistics) | Replan last quarter's deliveries with the model and compare cost and on-time rate; then run the model's routes in one region for a month | 1–3 months |
| [10 — Online Assignment & Waitlists](taxonomy.md#class-10-online-assignment--waitlists) | Replay last year's arrivals through the model and the current rule; then run it in shadow, with staff seeing its suggestion before deciding | One season |
| [11 — Network Seeding](taxonomy.md#class-11-network-seeding) | Randomly assign villages or sites to model-chosen seeds or the usual choice (staff picks or random); compare how far the message reached | 2–6 months |
| [12 — Risk-Based Inspection](taxonomy.md#class-12-risk-based-inspection) | Split the next batch of inspections between the model's list and the current method; compare problems found per inspection | 1–3 months |

---

## Follow-up 4: Build options — tools and partners

Be honest about maturity: Classes 2, 4, 5, 6, 7, 9 and 12 can be built with mature, free tools; Classes 1 and 3 have only research code, so they need a technical partner; Classes 8, 10 and 11 need only short scripts but careful design. Match the option to the user's staff skills from Filter 5.

### Software by class

| Class | Tools (all free and open source) | Maturity | Skills needed |
|---|---|---|---|
| [1 — Dynamic State Evolution](taxonomy.md#class-1-dynamic-state-evolution) | No ready-made package. Research code: [lily-x/online-rmab](https://github.com/lily-x/online-rmab) (Whittle-index planning, synthetic data only) | Research code | Python and a data scientist familiar with reinforcement learning or operations research |
| [2 — Static Demographic Targeting](taxonomy.md#class-2-static-demographic-targeting) | [PuLP](https://coin-or.github.io/pulp/), [Pyomo](https://www.pyomo.org) or [Google OR-Tools](https://developers.google.com/optimization) to write the model; [HiGHS](https://highs.dev) as a free solver | Mature | Python and basic integer programming; a small model can be handed over as a script |
| [3 — Spatiotemporal Security & Adaptive Search](taxonomy.md#class-3-spatiotemporal-security--adaptive-search) | [PAWS-public](https://github.com/lily-x/PAWS-public) (poaching risk prediction and patrol planning, research code); [SMART](https://smartconservationtools.org) for recording patrols and incidents | Research code (model); mature (data collection) | Data scientist plus GIS skills; SMART needs only field training |
| [4 — Robust Contingency Planning](taxonomy.md#class-4-robust-contingency-planning) | [RSOME](https://xiongpengnus.github.io/rsome/) (robust and distributionally robust models in Python); [CVXPY](https://www.cvxpy.org) or Pyomo for stochastic versions; HiGHS as solver | Mature libraries, specialist modeling | Operations-research skills; this is the hardest class to model well |
| [5 — Strategic Matching Markets](taxonomy.md#class-5-strategic-matching-markets) | [matching](https://github.com/daffidwilde/matching) (Python: stable marriage, hospital–resident, student allocation); [matchingMarkets](https://cran.r-project.org/package=matchingMarkets) (R) | Mature algorithm; small libraries | Spreadsheet-level data prep; deferred acceptance can also be run by a short script |
| [6 — Participatory Allocation](taxonomy.md#class-6-participatory-allocation) | [Stanford Participatory Budgeting Platform](https://pbstanford.org) (online ballots); [pabutools](https://github.com/comsoc-community/pabutools) (Python: equal shares and other rules); [equalshares.net](https://equalshares.net) (explanations and tools for the method of equal shares) | Platform used by cities; libraries maintained by researchers | Process design and outreach matter more than code; counting can be done by a script |
| [7 — Effect-Based Targeting](taxonomy.md#class-7-effect-based-targeting) | [grf](https://cran.r-project.org/package=grf) (R: causal forests); [policytree](https://cran.r-project.org/package=policytree) (R: short targeting rules); [EconML](https://github.com/py-why/EconML) (Python) | Mature | A statistician or economist familiar with randomized trials |
| [8 — Learn-While-Allocating](taxonomy.md#class-8-learn-while-allocating) | No package needed: Thompson sampling is a few lines of Python or R and can run in a spreadsheet | Simple code, careful design | Someone comfortable with basic Bayesian statistics |
| [9 — Routing & Logistics](taxonomy.md#class-9-routing--logistics) | [Google OR-Tools routing](https://developers.google.com/optimization/routing) (vehicle routing with capacities and time windows); [VROOM](https://github.com/VROOM-Project/vroom) (fast route optimization); PuLP or Pyomo with HiGHS for network design | Mature | An analyst comfortable with Python; good data on locations and travel times matters most |
| [10 — Online Assignment & Waitlists](taxonomy.md#class-10-online-assignment--waitlists) | No dedicated package: usually a prediction model plus an assignment model re-solved as people arrive (PuLP or OR-Tools), or a published priority-and-lottery rule | Methods mature; tools custom | Operations-research skills; one staff member to run it at each arrival |
| [11 — Network Seeding](taxonomy.md#class-11-network-seeding) | [NetworkX](https://networkx.org) (Python) to store the network and compute reach; the standard greedy seed-selection method takes a short script | Simple code; research methods | A data scientist; the hard part is collecting network data ethically |
| [12 — Risk-Based Inspection](taxonomy.md#class-12-risk-based-inspection) | [scikit-learn](https://scikit-learn.org) for the risk model; [Fairlearn](https://fairlearn.org) for the fairness audit; a spreadsheet to rank and assign inspections | Mature | A data scientist for the model; inspectors need only a ranked list |
| No model | A spreadsheet and a written rule | — | None |

Notes: the `matching` Python library's last release was in 2023 and RSOME's in 2024; both work, but check for updates. The research repositories above come from published papers and are not supported products.

**Input layers** ([taxonomy, Section 6](taxonomy.md#6-input-layers)). The playbook doesn't recommend speech, vision, OCR or language models: they change too fast for a fixed list. Point the user to where they can compare them on their own terms: the model's card on [Hugging Face](https://huggingface.co/models) (languages covered, training data, licence, reported error rates), the provider's own evaluation reports, and for Indian languages the open models and benchmarks from [AI4Bharat](https://ai4bharat.iitm.ac.in/). Whatever the source, the deciding test is the error rate on 50–100 of the program's own recordings, documents or records, checked by hand, by language or group. Check the licence too: some models and datasets are for non-commercial use only.

### Partners who help nonprofits

| Partner | What they offer | Cost to the NGO | How to start |
|---|---|---|---|
| [INFORMS Pro Bono Analytics](https://connect.informs.org/probonoanalytics/nonprofits) | Volunteer operations-research and analytics experts, the best fit for optimization (Classes 2, 4, 5, 6, 9, 10) | Free; the NGO commits staff time | Submit the project form on their site |
| [DataKind](https://www.datakind.org/partner/) | Volunteer data-science teams for social-sector organizations | Not stated on the site; ask | Apply through the partner form; not every application gets a reply |
| [Statistics Without Borders](https://statisticswithoutborders.org) | Pro bono statistics and data-science help, with priority to nonprofits | Free (pro bono) | New Client Questionnaire on their site |
| [Data Science for Social Good Fellowship](https://dssgfellowship.org) | Summer fellows build a project with a partner organization; run by Carnegie Mellon and the DSSG Foundation (2026 edition hosted at Johns Hopkins) | Not stated; ask | Check the site for the partner call ahead of each summer |
| [Wadhwani AI](https://www.wadhwaniai.org) | Builds AI for health, education and agriculture with governments and NGOs, mainly in India | Not stated | "Partner with us" contact |
| [Omdena](https://www.omdena.com) | Commercial AI project delivery for NGOs and UN agencies | Paid | Book a consultation |
| Local universities | Operations research, industrial engineering, economics or computer science departments often take capstone or thesis projects | Usually free | Email the department or a faculty member working on the relevant class |
| [CEGA (UC Berkeley)](https://cega.berkeley.edu/engage/for-partners/) | Matches programs in low- and middle-income countries with affiliated researchers for impact evaluations, new uses of existing data (including mobile-phone and satellite data) and monitoring help | Not stated; ask | Research Collaboration Form on the For Partners page |
| [J-PAL](https://www.povertyactionlab.org/j-pal-offices) | Network of affiliated professors who run randomized evaluations of poverty programs; affiliates raise their own research funding | Not stated; ask | Contact the regional office for your country |
| [Innovations for Poverty Action (IPA)](https://poverty-action.org/Partner-With-Us) | Runs randomized evaluations and field data collection through 15 country offices, mainly in Africa, Latin America and the Philippines | Not stated; ask | Contact form on the Partner With Us page |

CEGA, J-PAL and IPA evaluate programs; they don't build tools. Suggest them only when the user can say yes to all three: the program reaches at least several hundred people or sites; it can be randomized or rolled out in stages (a lottery or waitlist); and it already records the outcome that matters (attendance, repayment, test scores). Otherwise a build partner above, plus the pilot from Follow-up 3, comes first.

The brief from Follow-up 6 is the right document to send to any of these.

### What it takes: effort, costs, roles and timeline

**For the assistant.** Include this in Follow-up 4, filled from the user's answers: their class, data, staff and Filter 5. It is a list of what to find out, not an estimate. **Never give a cost, a number of hours or a duration as a fact**: costs vary by country, the state of the data and whether a partner is paid. Quote a figure only from the reference files, with its source; otherwise say who could tell them (the partners above, or the people in Follow-up 5 who ran a similar program). Offer the cost worksheet in the [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) (*5. Cost of ownership*) to add up the answers.

**The shape of the work, by tier.** The tier follows from the class's tools (table above). Durations are a rough guide from that maturity, not measured; a partner's own estimate replaces them.

| Tier | Classes | Who builds it | Rough shape | What keeps it running |
|---|---|---|---|---|
| A. A written rule or spreadsheet | No model; the simpler option for any class | Program staff | Days to write and test on past records | The person who updates the sheet each round |
| B. A mature free tool | 2, 4, 5, 6, 7, 9, 12 | An analyst, a volunteer or a university project | Weeks to a few months, most of it on the data | Someone who can rerun it, fix the data feed, and recheck it yearly |
| C. Short scripts, careful design | 8, 10, 11 | A data scientist with the program's M&E lead | Weeks to build; the design and its safeguards take longer | Someone who understands the design, since the code alone won't show when it goes wrong |
| D. Research code | 1, 3 | A technical partner with research experience | Several months, adapted from published code | A partner or in-house specialist for as long as it runs |

**What it costs: the lines to put a figure on.** For each, ask who will pay, in money or in staff time, for the model and for the simple option:
- **One-off:** gathering, cleaning and linking the data; the build; the test on past records ([replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit)); connecting it to the forms or systems staff use; training staff; consent and legal review; explaining it to the community; the fairness audit, if it ranks people.
- **Every round:** entering the data; running it and checking the output; staff time to act on it.
- **Every year:** hosting or software, if any; maintenance and fixes when data formats change; recalibrating on new records; the monthly health check and the yearly fairness recheck.
- **Often missed:** the contingency when a volunteer or partner leaves; running the old process alongside during the pilot; the time of managers who must approve and explain it.

**Who is needed.** Check each role has a named person:

| Role | Does | Can a volunteer or partner do it? |
|---|---|---|
| Data owner | Keeps the records complete and consistent each round | No: it has to sit inside the program |
| Operator | Runs the sheet or tool each round and passes on the list | Rarely: it is a weekly job |
| Builder | Builds and tests the model | Yes, for Tiers B to D |
| Maintainer | Fixes it when data or rules change, and recalibrates | Only with a written commitment for a set period |
| Reviewer | Reads the health check, approves overrides, answers complaints | No: a manager accountable for the program |

**Phases, and what ends each one.** Funders can release money phase by phase ([Funder review](#funder-review-checking-a-proposal)):
1. **Test on past records:** the replay kit or a partner's replay. Ends with a decision: simple rule, model, or neither.
2. **Build:** only if the model's gap is worth its full cost. Ends when it runs on last round's data and staff can read its output.
3. **Pilot** ([Follow-up 3](#follow-up-3-pilot-design)): ends at the agreed date, with the success and harm measures.
4. **Scale:** ends when the old process is retired, with a written fallback rule.
5. **Run:** the monthly health check, a yearly recheck, and a date to decide whether to keep it.

**Questions to ask a partner or vendor**
- What will it cost each year to run after you leave, and who will do that work?
- How long do you expect the build to take, and what would make it longer?
- What do you need from our staff, and for how many hours a week?
- What happens when our data format or the rules change?
- Will we get the code, the data and the documentation, and can someone else maintain it?
- What did a similar project of yours take, and can we speak to that organization?
- The *Contract terms* check in Follow-up 2 covers ownership, audit and leaving.

**Red flags.** A budget with no recurring costs after launch; one named volunteer as builder and maintainer; Tier D research code with no partner committed beyond the build; no money for the test on past records or for staff time; a timeline with no pilot.

### Others' setups: what has been published

Few deployments publish what they cost or how long they took. These publish at least some of it: who built them, how long, what it cost, or what happened later. Cite only what is written here, with its source; for anything else, suggest asking the people involved (Follow-up 5). Checked on **2026-11-23**: every figure below was read in the linked source.

| Class | Setup | What is published |
|---|---|---|
| 1 | ARMMAN's weekly call list, India ([pilot](https://arxiv.org/abs/2109.08075), [deployment](https://arxiv.org/abs/2604.07384), [Google Research](https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/)) | Led by Google Research India with Harvard researchers. A 7-week pilot from 26 April 2021 with 23,003 mothers; in use from April 2022 and reaching over 350,000 mothers by the end of a five-year research project (2020 to summer 2025). Being transitioned to ARMMAN, which holds the data. No costs, team size or later status published. |
| 8 | Job-search help for refugees, Jordan ([Caria et al.](https://warwick.ac.uk/fac/soc/economics/research/workingpapers/2021/twerp_1335_-_caria.pdf), [CEGA](https://cega.berkeley.edu/impact/jordan-invests-in-better-employment-matching-for-job-seekers)) | An adaptive experiment with 3,770 people, intake mid-February to December 2019; academics with the International Rescue Committee's employment staff, who recruited and followed up. Jordan's Ministry of Labor and the World Bank later built a national programme on the project's registration and matching approach, not on the adaptive algorithm. |
| 8 | ARMMAN's call timing ([Dasgupta et al.](https://arxiv.org/abs/2507.16356)) | A pilot with about 6,500 participants in early 2025. Google DeepMind advised; the experimental infrastructure was managed by ARMMAN's own team. |
| 11 | HIV prevention with youth experiencing homelessness, Los Angeles ([Wilder et al.](https://arxiv.org/abs/2009.09559)) | A trial with 713 youth over two years at three sites. Training took about 4 hours, run by the social-work research team. Mapping each network took the team a week or more, which the authors call unsustainable for an agency deploying it alone. |
| 2 | Novissi cash transfers, Togo ([Aiken et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8967719/)) | The government with UC Berkeley researchers and GiveDirectly. A phone survey over two weeks in September 2020 trained the targeting; the expansion began in November 2020, about US$4 million to 154,238 registrants. No cost of building the targeting published. |
| 3 | PAWS ranger patrols, Uganda and Cambodia ([Xu et al.](https://arxiv.org/abs/1903.06669)) | Field tests: 5 months at Murchison Falls, and 4 months at Srepok, where 72 rangers cover the area. University researchers with WWF, WCS and the Uganda Wildlife Authority. Integration into the SMART patrol software was planned; whether it happened isn't published. No costs. |
| 3 | PROTECT port patrols, US Coast Guard ([AI Magazine, 2012](https://personal.ntu.edu.sg/boan/papers/protect_aim.pdf)) | In use in Boston from April 2011, built by university researchers with Coast Guard planners and operators; reported no increase in resources or operating costs; then being extended to New York. |
| 4 | OCHA/CERF anticipatory-action pilots ([Frontiers, 2022](https://www.frontiersin.org/journals/climate/articles/10.3389/fclim.2022.932336/full)) | Up to US$140 million committed for 12 pilot frameworks; just over US$60 million spent; 2.2 million people reached in Somalia, Ethiopia and Bangladesh. Setting up a framework is described as time-consuming. Written by OCHA staff. |
| 4 | GiveDirectly flood cash, Nigeria 2024 ([GiveDirectly](https://www.givedirectly.org/flood-forecast-ai)) | Two weeks of pre-enrolment by a phone text menu (USSD), which saved at least US$80,000 in field staff; 3,250 people paid before the flood peak. Partners included Google Research and Nigeria's hydrological agency. The page was revised in July 2026 to describe the pilot's trade-offs. |
| 9 | WFP's Optimus ([WFP](https://innovation.wfp.org/project/optimus)) | Development began in 2014, run in-house by WFP with university partners; used in 44 operations. No costs published. |
| 9 | Boston school buses ([INFORMS](https://www.informs.org/Impact/O.R.-Analytics-Success-Stories/Optimized-school-bus-routing-helps-school-districts-design-better-policies)) | Routing used to take a team of 10 working overtime for two months; MIT's algorithm does it in 30 minutes. 50 fewer buses and about US$5 million a year saved. |
| 5 | Denver school choice ([Chalkbeat, 2013](https://www.chalkbeat.org/philadelphia/2013/12/5/22181092/custom-software-helps-cities-manage-school-choice)) | Denver paid the nonprofit IIPSC US$350,000 (2011). Four months for IIPSC and district technology staff to build the algorithm and software, then a month of testing; about US$575,000 a year to support. |
| 5 | New England kidney exchange ([poster, 2010](https://stanford.edu/~alroth/papers/NEPKE.TTS%20eposterJune%202010.pdf)) | Started with an Excel spreadsheet for data entry, a web system from 2007; matches ran about every 45 days, then every 2 weeks from 2010. |
| 6 | Aarau's participatory budget, Switzerland ([city report](https://www.stadtidee.aarau.ch/public/upload/assets/31299/Abschlussbericht%20zur%20Stadtidee%202023-2024_final_neu.pdf?fp=2), in German) | Budget CHF 105,000, of which CHF 50,000 for projects and CHF 30,000 for outside support; actual cost just under CHF 88,500. A three-person city team put in about 50–70% of a full-time post in the busiest phase (December 2022 to July 2023) and about 10–20% otherwise; preparation ran February to November 2022. About 1,700 people voted, against a target of 5,000. |
| 6 | Wieliczka's Green Million, Poland ([equalshares.net](https://equalshares.net/elections/zielony-milion)) | 1 million złoty decided by equal shares; 6,586 residents voted. |
| 10 | Annie MOORE refugee placement, HIAS ([HIAS letter, 2020](https://www.oecd-opsi.org/wp-content/uploads/2020/02/2020-02-20-Support-Letter-for-OECD-FINAL.pdf)) | Built by a university research team with foundation support from late 2017; first version May 2018; rolled out to all HIAS staff in August 2018. HIAS's Karen Monken reported spending 80% less time on routine matching. Later status not published. |
| 10 | Feeding America's Choice System ([Conversable Economist](https://conversableeconomist.com/2017/11/03/how-food-banks-use-markets/), [Works in Progress](https://worksinprogress.co/issue/how-market-design-can-feed-the-poor/)) | Designed by eight food bank directors, three Feeding America staff and four University of Chicago faculty; the task force spent over a year on it. A fairness committee it created never convened. |
| 12 | Flint lead pipes ([Nextgov, 2019](https://www.nextgov.com/artificial-intelligence/2019/01/how-ai-found-flints-lead-pipes-and-then-humans-lost-them/153905/)) | Volunteer researchers' model guided digs through 2017: 6,228 of 8,833 homes had lead pipes replaced. A contractor on a US$5 million contract then set the model aside; by mid-December 2018 only 1,567 of 10,531 digs found lead. |
| 12 | Chicago food inspections ([city evaluation](https://chicago.github.io/food-inspections-evaluation)) | A two-month pilot found establishments with violations 7.5 days earlier on average; the code is open. |
| 12 | Eva, COVID-19 border testing, Greece ([Bastani et al.](https://faculty.marshall.usc.edu/Vishal-Gupta/Papers/GreeceCovid.pdf)) | All 40 points of entry, 6 August to 1 November 2020. The researchers met the national COVID-19 committee twice a week; a development team from the company Cytech is credited. |

**What these show.** Durations and team shapes are published far more often than costs; no setup above publishes what its model cost to build. Several depended on a research team, and what happened after it left is the least documented part (ARMMAN after 2025, Annie MOORE after 2020, PAWS and SMART). Flint shows that a working model can be dropped when a contract changes hands. Class 7 has no published standing use by an NGO or agency, only trials. Use these to ask better questions, not as estimates.

---

## Follow-up 5: Reading and people to contact

Give the user two or three items for their class, starting with the most accessible. Full citations for the deployment papers are in the taxonomy reference.

### Start here (any class)
- Perrault, A., Fang, F., Sinha, A., Tambe, M. (2020). *AI for Social Impact: Learning and Planning in the Data-to-Deployment Pipeline.* AI Magazine 41(4). Free copy: [arXiv 2001.00088](https://arxiv.org/abs/2001.00088). An overview of how these projects go from data to deployment, written by practitioners.

### By class

| Class | Accessible start | Deeper |
|---|---|---|
| [1 — Dynamic State Evolution](taxonomy.md#class-1-dynamic-state-evolution) | Google Research blog on ARMMAN: [Using ML to boost engagement with a maternal and child health program](https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/) | Mate et al. (2022), AAAI field study; Mate et al. (2020), *Collapsing Bandits*, NeurIPS |
| [2 — Static Demographic Targeting](taxonomy.md#class-2-static-demographic-targeting) | Bradley, Hax, Magnanti, *Applied Mathematical Programming* — free from MIT at [web.mit.edu/15.053/www](https://web.mit.edu/15.053/www/) (integer programming chapters) | Church & ReVelle (1974) on covering location; Flanigan et al. (2021), Nature, on leximin fairness |
| [3 — Spatiotemporal Security & Adaptive Search](taxonomy.md#class-3-spatiotemporal-security--adaptive-search) | Fang, Stone, Tambe (2015), *When Security Games Go Green*, IJCAI — [free PDF](https://www.ijcai.org/proceedings/2015/0367.pdf) | Tambe (2011), *Security and Game Theory: Algorithms, Deployed Systems, Lessons Learned*, Cambridge University Press |
| [4 — Robust Contingency Planning](taxonomy.md#class-4-robust-contingency-planning) | Rawls & Turnquist (2010) on pre-positioning emergency supplies | Rahimian & Mehrotra (2022), *Frameworks and Results in Distributionally Robust Optimization*, Open Journal of Mathematical Optimization — [open access](https://doi.org/10.5802/ojmo.15) |
| [5 — Strategic Matching Markets](taxonomy.md#class-5-strategic-matching-markets) | Roth (2015), *Who Gets What — and Why*, a book for general readers | Abdulkadiroğlu, Pathak & Roth (2005) on the New York City high-school match |
| [6 — Participatory Allocation](taxonomy.md#class-6-participatory-allocation) | [equalshares.net](https://equalshares.net), a plain-language guide to proportional participatory budgeting | Goel et al. (2019) on knapsack voting; Peters, Pierczyński & Skowron (2021) on equal shares |
| [7 — Effect-Based Targeting](taxonomy.md#class-7-effect-based-targeting) | Athey, Keleher & Spiess (2025) on causal vs predictive targeting — free at [arXiv 2310.08672](https://arxiv.org/abs/2310.08672) | Athey & Wager (2021), *Policy Learning with Observational Data*, Econometrica |
| [8 — Learn-While-Allocating](taxonomy.md#class-8-learn-while-allocating) | Caria et al. (2024), the refugee job-search experiment in Jordan | Kasy & Sautmann (2021), *Adaptive Treatment Assignment in Experiments for Policy Choice*, Econometrica |
| [9 — Routing & Logistics](taxonomy.md#class-9-routing--logistics) | [WFP Optimus project page](https://innovation.wfp.org/project/optimus); Google OR-Tools [routing guide](https://developers.google.com/optimization/routing) | Peters et al. (2021), *The Nutritious Supply Chain*, INFORMS Journal on Optimization; Bertsimas, Delarue & Martin (2019), PNAS |
| [10 — Online Assignment & Waitlists](taxonomy.md#class-10-online-assignment--waitlists) | Ahani et al. (2021) on Annie MOORE refugee placement, Operations Research | Manshadi, Niazadeh & Rodilitz (2023), *Fair Dynamic Rationing*, Management Science; Arnosti & Shi (2020) on housing lotteries |
| [11 — Network Seeding](taxonomy.md#class-11-network-seeding) | Banerjee et al. (2019), *Using Gossips to Spread Information*, Review of Economic Studies | Kempe, Kleinberg & Tardos (2003), KDD; Wilder et al. (2021), AAAI, on the HIV-prevention trial |
| [12 — Risk-Based Inspection](taxonomy.md#class-12-risk-based-inspection) | Abernethy et al. (2018), *ActiveRemediation*, the Flint lead-pipe search — free at [arXiv 1806.10692](https://arxiv.org/abs/1806.10692) | Potash et al. (2015), KDD, on lead-hazard inspections in Chicago; Bastani et al. (2021), Nature, on Eva |

### Research groups active in this area

Researchers rarely take on projects from cold emails, but a well-written brief that matches their published work is the best way in.

- **Teamcore and the Center for Research on Computation and Society, Harvard** — [Milind Tambe](https://teamcore.seas.harvard.edu): restless bandits for public health (Class 1) and security games (Class 3).
- **[Fei Fang](https://feifang.info), Carnegie Mellon University** — green security games and anti-poaching (Class 3), and food rescue logistics.
- **[Lily Xu](https://lily-x.github.io), Columbia University** — conservation and public-health planning under uncertainty (Classes 1, 3, 4 and 8); author of the PAWS and restless-bandit research code above.
- **[Roshni Sahoo](https://roshni714.github.io), Columbia Business School** — learning targeting and cash-transfer rules from data, including when the data under-represents some groups (Classes 2 and 7).
- **Stanford Crowdsourced Democracy Team ([Ashish Goel](https://web.stanford.edu/~ashishg/))** — participatory budgeting and online deliberation platforms used by cities (Class 6).
- **Humanitarian operations research (Class 9)** — the Zero Hunger Lab at Tilburg University (Hein Fleuren) and Dick den Hertog (University of Amsterdam) worked with WFP on Optimus; Karen Smilowitz (Northwestern) studies food-bank distribution and nonprofit logistics.
- **Refugee and waitlist allocation (Class 10)** — Alex Teytelboym (Oxford) and Andrew Trapp (WPI) on Annie MOORE; Vahideh Manshadi (Yale) on fair dynamic rationing.
- **Network interventions (Class 11)** — Bryan Wilder (Carnegie Mellon) and Eric Rice (USC) on peer-leader selection; Abhijit Banerjee and Esther Duflo (MIT, J-PAL) on seeding information in villages.
- **Predictive inspection (Class 12)** — Rayid Ghani (Carnegie Mellon, Data Science for Social Good) on public-health and police early-warning models; Jacob Abernethy (Georgia Tech) on the Flint lead-pipe search.
- **[Stefan Wager](https://web.stanford.edu/~swager/), Stanford, and [Susan Athey](https://www.gsb.stanford.edu/faculty-research/faculty/susan-athey), Stanford** — causal forests and policy learning (Class 7).
- **Market design (Class 5)** — the economists behind school-choice and kidney-exchange matching, including Alvin Roth (Stanford) and Parag Pathak (MIT), publish widely; their papers name the organizations that ran each match.

---

## Follow-up 6: One-page brief for a technical partner

Fill this from the conversation so the user can send it to a volunteer data scientist, university group, pro bono service or research evaluator. Keep it to about one page and in plain language.

**Before drafting**, check which of these the interview has not covered, and ask for all of them in one turn: what the program delivers and the change it aims for; where it runs (country or region, urban or rural, how many sites and how far apart); the timeline (when a decision is due, seasons or funding cycles, how soon a pilot must start); and resources (staff who would work on this, their skills, budget for a build and for running it). Draft once the user answers; mark anything still unknown as *[to confirm]* rather than guessing.

```
PROJECT BRIEF — [Organization name]

The program
  [What we deliver, to whom, and the change it aims for (e.g. better attendance,
   fewer missed doses, higher incomes).]

The decision we need help with
  [One or two sentences: what is allocated, to whom, how often.]

Why it matters
  [Who is affected and what goes wrong today.]

Current approach
  [How the decision is made now, and its known problems.]

Recommended approach
  [Class number and name, and the method (e.g. restless bandits with a Whittle index),
   with one sentence on why it fits our answers.]

Simpler option to beat
  [The best paper or spreadsheet rule, and the assumptions it rests on. Any build
   must beat it on last year's records before the pilot. If the program has run
   the replay kit's workbook for its class, give the result; if not, say which
   workbook to run first.]

Data we have
  [Fields, how often recorded, how many records, format, known gaps.]

Where we work
  [Country or region; urban or rural; number of sites and distances between them;
   connectivity and any seasonal access problems.]

Timeline
  [When the next decision is due; seasons, funding or school cycles that fix the
   dates; when a pilot could start and must finish.]

Resources
  [Staff who would work on this and their skills; budget for a build and for
   running it each cycle; who maintains it after the partner leaves.]

Other constraints
  [Budget per round, capacities, fairness rules, legal or data-protection limits.]

What success looks like
  [One or two measures and the harm measure to watch.]

How results must reach staff
  [Paper list, Excel sheet, app; who runs it and how often.]

Where a partner can help
  Build: [what a technical partner would do, e.g. clean the data, build the model,
   test it against the simpler option, set up the staff sheet; the scope, e.g. a
   3-month pilot build, a review of our data, or a one-off plan.]
  Evaluation: [only if the program reaches several hundred people or sites, can be
   randomized or rolled out in stages, and already records the outcome (see
   Follow-up 4): what an evaluator such as CEGA, J-PAL or IPA would measure.
   Otherwise write "Not yet: the pilot in Follow-up 3 comes first."]

Contact
  [Name, role, email.]
```

**After the brief, offer a session record:** a short block the user can save and paste into a new conversation to pick up where they left off, or share with colleagues to check. Keep it under about 200 words, in one block that copies cleanly:

- **Answers so far**, one line per filter and narrowing question, in the user's words.
- **Recommendation:** the class, any layer, and the simpler option to beat.
- **Assumptions** made where the user didn't know, each marked *[to check]*.
- **Open questions** and who in the organization could answer them.
- **Next steps** agreed for the month.

When a user pastes a session record, confirm it in a sentence, ask only about what has changed, and restate only the parts of the recommendation that change.

---

## Funder review: checking a proposal

For a funder, by default a foundation program officer, reviewing an NGO's proposal to use a model or AI to allocate something (visits, patrols, transfers, places, supplies), to feed such a decision, or as the intervention itself. It replaces the interview: the proposal supplies the answers.

**Rules for the assistant**
- **Review the method, never the organization.** Don't score, rank or judge the NGO's capacity, leadership or trustworthiness, and don't suggest other NGOs.
- **Give questions and conditions, not a decision.** Never say whether to fund or decline.
- **Use only the proposal and the funder's answers.** Anything the proposal doesn't say is a question for the NGO, never a guess.
- **Check the proposal's evidence** under the evidence integrity rules: compare each cited deployment or figure with the verified references in the taxonomy, and say whether it is a field deployment, a pilot, a simulation or a proposal.
- **If nothing is allocated** (a chatbot that only answers questions, a dashboard), say this review doesn't apply, and point out any allocation decision hidden inside the proposal.
- **If the proposal is an input layer** (speech recognition, document extraction, a screening classifier, a forecast, a ready-made map, a prediction model: [taxonomy, Section 6](taxonomy.md#6-input-layers)), don't classify or judge the model itself, and don't suggest a different one. Review the decision it feeds, if any, as usual, and ask three questions in the memo either way: what is its error rate on the program's own data, by language or group; who corrects its errors, and how long that takes compared with the manual process; and what decision will its output feed, and who makes it.
- **If the AI is the intervention** (a tutor, a coach for health workers, an adviser), review how it will be tested, not the model: does it support a worker or replace one, when does a person take over, and which outcome, against which comparison, will show it works ([taxonomy, Section 7](taxonomy.md#when-the-ai-is-the-intervention)). Use the verdicts below for the test plan: *Fits* when a randomized or A/B comparison on an outcome is planned; *Mismatch* when success is measured by usage. Any part that decides who gets help is reviewed as an allocation.
- **If a score targets the people served** (fraud, overpayment, eligibility), say so in the memo's first line, and list the safeguards in the readiness check *Scoring the people you serve* as conditions for any funding stage.
- **Check the budget against *What it takes*** ([Follow-up 4](#what-it-takes-effort-costs-roles-and-timeline)). Under *Suggested funding stages*, name any line the budget leaves out, especially running costs after launch, a maintenance owner and staff time; ask about them in *Questions for the NGO*. Don't judge whether a figure is too high or low; ask how it was estimated.
- **For an individual donor**, use simpler language and leave out the funding stages unless asked.
- **For an NGO checking its own proposal** before sending it, run the same review without asking for the funder's context (use it if they know the funder's priorities). Title the memo for the NGO, and turn *Questions for the NGO* into the questions a funder is likely to ask, with what would answer each.

**Steps**
1. **In one turn, ask for:** the proposal text, or a summary of its decision, method, data and budget; what the funder supports and where; the grant size and period; and how much risk the funder accepts (early pilots, or only proven programs). If any of the funder's context is missing, ask for it and stop: don't write the memo in the same turn. You may list what the proposal says for each filter while you ask.
2. **Read the proposal against the five filters**, in a short list: what it says for each, and what is missing. If the decision itself is unclear, ask the funder the matching narrowing question; otherwise don't interview.
3. **Deliver the memo below** in one response, then offer to turn the questions into an email to the NGO.

**Choosing the verdict**

| Verdict | When | Common examples |
|---|---|---|
| **Fits** | The proposed method belongs to the class the decision falls in, and the data it needs exists at the needed rate ([taxonomy, Data each class needs](taxonomy.md#data-each-class-needs)) | Vehicle routing for weekly deliveries to many sites, with locations and travel times on record |
| **Heavier than needed** | Right class, but the simpler option ([taxonomy, Section 4](taxonomy.md#4-simpler-alternatives-for-each-class)) is likely close: few people or sites, thin data, a decision that rarely changes; or research-code methods (Classes 1 and 3) with no technical partner named | A custom optimizer for 20 boreholes that a sorted list with a district floor would match |
| **Mismatch** | The method belongs to a different class from the decision | A risk score ranking the "highest-need" where the real question is whom the help changes (Class 7, or Class 1 if repeated); a fixed or predicted patrol schedule against people who adapt (Class 3); a plan built on average years for rare disasters (Class 4); central assignment where both sides choose (Class 5); a chatbot proposed for what is really an allocation decision |
| **No model needed** | Supply roughly meets demand, few decisions are made, or a written rule captures most of the value | An AI system to decide pantry quantities when every household already gets served |

**Funding stages.** Suggest stages that release money as the evidence comes in, matched to the funder's risk appetite; if they fund only proven programs, say which stage the proposal has reached.
1. **Test on past records** (small grant, weeks): replay last year's decisions under the proposed model and under the simpler option, counting the model's full cost. For one-off decisions (Classes 2 and 4), compare plans instead. Release the next stage only if the gap is worth that cost. For Classes 1, 2, 10 and 12, the NGO can run this test itself, before any build money, with the [replay kit](https://github.com/ashitpatel/ai4sgfinder/tree/main/tools/replay-kit) workbook for the class; say which.
2. **Pilot** ([Follow-up 3](#follow-up-3-pilot-design)): against current practice, with one or two success measures and a harm measure agreed in advance, a fixed duration, and the old process kept available.
3. **Scale**: with a named maintenance owner, a written fallback rule, and the replay kit's monthly health check (or the same measures) reported at each review: whether staff follow the tool, whether it beats a random share, and how each group fares. Suggest an evaluation only if the program passes the three-part test in [Follow-up 4](#follow-up-4-build-options--tools-and-partners); evaluation funding from J-PAL, CEGA or IPA goes through their researchers, so the NGO approaches them with a researcher.

**The memo.** Write it as ordinary text with short headings, not in a code block, so it pastes cleanly into an email or document. Keep the whole reply under about 800 words: one to three sentences under each heading, questions and risks as one-line bullets, and the filter reading before it (step 2) as five short lines. Use these seven headings in order:

**Proposal review — [NGO name]: [proposal title].** *For [funder]. Based only on the proposal and the funder's answers; it reviews the proposed method, not the organization.*

1. **The decision.** One line: what is allocated, to whom, how often.
2. **Method fit.** *Verdict: Fits / Heavier than needed / Mismatch / No model needed.* The class the decision falls in, the method proposed, and why they do or don't match, in two or three sentences.
3. **The simpler option to beat.** The best paper or spreadsheet rule for the class. Does the proposal plan to compare against it on past records, counting the model's full cost?
4. **Questions for the NGO.** Up to five, most important first: missing filter answers, then the readiness checks (Follow-up 2) most at risk, such as who maintains it after the builder leaves.
5. **Risks to people.** Only those that apply: fairness across groups, consent and privacy, surveillance, biased risk scores, withdrawing help from people scored "low benefit". If a score ranks people, ask for the fairness audit (Follow-up 2): what the label measures, calibration by group, share of slots by group.
6. **Evidence check.** Each deployment or figure the proposal cites: verified, unverified, or overstated (for example a simulation described as a deployment, or accuracy on a published benchmark presented as accuracy on the program's own data).
7. **Suggested funding stages.** The stages above, with the milestone that releases each one.
