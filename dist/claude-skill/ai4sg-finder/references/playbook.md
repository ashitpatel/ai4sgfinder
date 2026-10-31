# AI4SG Implementation Playbook

What to do after an approach has been chosen. The AI4SG Finder assistant uses this file for its six follow-ups; people can also read it directly.

Tools, organizations and links were last checked on **2026-10-30**. Services change: confirm that a tool or partner is still active before relying on it.

**For the assistant.** Offer the follow-ups after the recommendation and deliver one per turn, on request. Fill every template from the user's own interview answers, quoting their numbers and wording. Where an answer is missing, say what you need instead of guessing. Recommend only tools, partners and readings listed here, or ones you are certain exist; anything else must be labeled *"(unverified — please confirm)"*.

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

---

## Follow-up 2: Readiness checks

Go through these with the user; mark each as ready, partly ready, or not ready, and say what to do about each gap.

**For every class**
- **Decision owner.** One named person or team will use the output and is authorized to act on it.
- **Data.** The required fields exist, are recorded consistently, and cover the people or places the model will decide about. Gaps fall unevenly on some groups?
- **Consent and privacy.** People whose data is used were told and agreed; personal data is stored securely; the model can run on pseudonymized IDs.
- **Fairness.** Decide in advance which groups must not be disadvantaged and how that will be measured.
- **Do-no-harm.** Who loses out under the new allocation compared with today, and is that acceptable and explainable?
- **Maintenance.** Someone can rerun the model, fix the data pipeline and answer staff questions a year from now, after the original builder leaves.
- **Exit plan.** If the model fails or the partner leaves, staff can fall back to a written simple rule.
- **Community voice.** Affected people or their representatives have seen and can question the approach.
- **Bias in risk scores.** If any step uses a predicted score, check what it actually predicts and whether it is equally accurate across groups. A health algorithm that predicted costs instead of illness under-referred Black patients (Obermeyer et al., Science 2019).
- **Human override.** Staff know when they may set the model's suggestion aside, and each override is recorded and reviewed.

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

---

## Follow-up 3: Pilot design

Recommend the smallest pilot that can show the approach works better than current practice.

**For every class**
- **Compare against current practice**, not against nothing.
- **Pick one or two success measures** agreed before the pilot starts, plus one harm measure (who might be worse off).
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
| [12 — Risk-Based Inspection](taxonomy.md#class-12-risk-based-inspection) | [scikit-learn](https://scikit-learn.org) for the risk model; a spreadsheet to rank and assign inspections | Mature | A data scientist for the model; inspectors need only a ranked list |
| No model | A spreadsheet and a written rule | — | None |

Notes: the `matching` Python library's last release was in 2023 and RSOME's in 2024; both work, but check for updates. The research repositories above come from published papers and are not supported products.

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

The brief from Follow-up 6 is the right document to send to any of these.

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

Fill this from the conversation so the user can send it to a volunteer data scientist, university group or pro bono service. Keep it to one page and in plain language.

```
PROJECT BRIEF — [Organization name]

The decision we need help with
  [One or two sentences: what is allocated, to whom, how often.]

Why it matters
  [Who is affected and what goes wrong today.]

Current approach
  [How the decision is made now, and its known problems.]

Recommended approach
  [Class number and name, and the method (e.g. restless bandits with a Whittle index),
   with one sentence on why it fits our answers.]

Data we have
  [Fields, how often recorded, how many records, format, known gaps.]

Constraints
  [Budget per round, capacities, fairness rules, legal limits, connectivity.]

What success looks like
  [One or two measures and the harm measure to watch.]

How results must reach staff
  [Paper list, Excel sheet, app; who runs it and how often.]

What we are asking for
  [e.g. a 3-month pilot build, a review of our data, or a one-off plan.]

Contact
  [Name, role, email.]
```
