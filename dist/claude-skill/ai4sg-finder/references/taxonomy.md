# AI4SG Allocation Taxonomy

Reference material for the AI4SG Finder assistant. It holds the twelve allocation archetypes, the decision tree for choosing among them, and deployment examples graded by how well they are verified.

## 1. The twelve allocation archetypes

The classes are numbered in the order they were added. They fall into five families:

| Family | Classes |
|---|---|
| Who gets a limited resource | [2 Static Demographic Targeting](#class-2-static-demographic-targeting), [7 Effect-Based Targeting](#class-7-effect-based-targeting), [10 Online Assignment & Waitlists](#class-10-online-assignment--waitlists) |
| Repeated decisions that learn | [1 Dynamic State Evolution](#class-1-dynamic-state-evolution), [8 Learn-While-Allocating](#class-8-learn-while-allocating) |
| Space, movement and risk | [3 Spatiotemporal Security & Adaptive Search](#class-3-spatiotemporal-security--adaptive-search), [4 Robust Contingency Planning](#class-4-robust-contingency-planning), [9 Routing & Logistics](#class-9-routing--logistics), [12 Risk-Based Inspection](#class-12-risk-based-inspection) |
| People choose | [5 Strategic Matching Markets](#class-5-strategic-matching-markets), [6 Participatory Allocation](#class-6-participatory-allocation) |
| Spread through people | [11 Network Seeding](#class-11-network-seeding) |

| # | Class | Core mathematics | Best-suited problem space | Representative field deployments |
|---|-------|------------------|---------------------------|----------------------------------|
| 1 | [**Dynamic State Evolution**](#class-1-dynamic-state-evolution) (Restless Bandits) | Restless multi-armed bandits (RMAB), Markov decision processes (MDP), Whittle index policies | Probabilistic behavioral nudges; systems with novelty decay or passive state change over time; volatile environments | ARMMAN mMitra maternal-health call scheduling (India); tuberculosis medication-adherence interventions on 99DOTS data |
| 2 | [**Static Demographic Targeting**](#class-2-static-demographic-targeting) (Convex Welfare Optimization) | Integer linear programming (ILP), convex optimization, maximin / leximin fairness, welfare metrics | Distribution of irreversible, transactional capital; slow-moving, stable environments; strict legal auditability and democratic transparency | Fair selection of citizens' assemblies (leximin, Sortition Foundation); targeting of cash transfers; siting of schools and water points |
| 3 | [**Spatiotemporal Security & Adaptive Search**](#class-3-spatiotemporal-security--adaptive-search) (Predictive Patrol) | Stackelberg security games, spatial point processes, reinforcement learning (e.g. deep Q-networks) | Allocating mobile patrol assets over physical geography; adversarial or adaptive environments where the target reacts to your moves | PAWS anti-poaching patrol planning (Uganda, Cambodia); ARMOR airport checkpoints (LAX); PROTECT (US Coast Guard) |
| 4 | [**Robust Contingency Planning**](#class-4-robust-contingency-planning) (Robust / Distributionally Robust Optimization) | Distributionally robust optimization (DRO), stochastic programming, minimax over uncertainty sets | High uncertainty with severe downside (life-or-death outcomes); no historical data or adversarial shocks | Pre-positioning of emergency supplies before hurricanes and floods; vaccine and medicine stockpiling under unknown demand |
| 5 | [**Strategic Matching Markets**](#class-5-strategic-matching-markets) (Two-Sided Market Design) | Deferred acceptance (Gale–Shapley), stable matching, exchange mechanisms, network flow | Two-sided systems where individuals on both sides hold their own preferences; a planner who cannot dictate outcomes without respecting local choice | NYC and Boston public school choice; the US medical residency match (NRMP); kidney paired-donation exchange |
| 6 | [**Participatory Allocation**](#class-6-participatory-allocation) (Social-Choice Budgeting) | Voting and aggregation rules: knapsack voting, approval voting, the method of equal shares, proportionality (the core, justified representation) | A shared budget whose split the affected community decides by vote; legitimacy comes from a transparent rule rather than a planner's objective | Participatory budgeting in Boston (knapsack voting, 2016) and other US cities on the Stanford platform; method of equal shares in Aarau (Switzerland) and Wieliczka (Poland), 2023 |
| 7 | [**Effect-Based Targeting**](#class-7-effect-based-targeting) (Policy Learning) | Heterogeneous treatment effects (causal forests, CATE), empirical welfare maximization, policy learning, evaluation by rank-weighted treatment effects | A limited program that helps some people far more than others; pilot or randomized data show who responds; targeting by need would waste slots on people it won't help | Financial-aid renewal nudges for CUNY students (Athey, Keleher & Spiess); learning cash-transfer rules from survey and trial data |
| 8 | [**Learn-While-Allocating**](#class-8-learn-while-allocating) (Adaptive Experimentation / Bandits) | Stochastic and combinatorial multi-armed bandits, Thompson sampling, exploration sampling, adaptive experiments | Several options (programs, sites, messages) whose payoff is unknown but stable; nobody is evading you; learn which works while still serving people | Adaptive job-search assistance for refugees in Jordan (International Rescue Committee); agricultural-extension recruitment in Odisha, India; LIZARD patrol-effort planning tested on Cambodian poaching data |
| 9 | [**Routing & Logistics**](#class-9-routing--logistics) (Vehicle Routing / Network Design) | Vehicle routing with capacities and time windows, network flow, supply-chain network design, linear programming for ration composition | Moving goods or people through depots and routes at least cost, on time, under capacity and quality rules | WFP's Optimus for food-basket and sourcing design (2021 INFORMS Edelman Award); Boston Public Schools bus routing |
| 10 | [**Online Assignment & Waitlists**](#class-10-online-assignment--waitlists) (Online Allocation / Dynamic Rationing) | Online and two-stage stochastic assignment, dynamic rationing with fairness over time, priority categories and lotteries, credit-based auctions | People or items that arrive one at a time and must be placed now, with limited capacity over a season | Annie MOORE refugee placement at HIAS; Feeding America's food-bank "Choice System"; reserve categories for COVID-19 vaccines |
| 11 | [**Network Seeding**](#class-11-network-seeding) (Influence Maximization) | Influence maximization under independent-cascade and related models, greedy seed selection, sampling-based network discovery | Training or briefing a few people so information or behavior spreads through their social ties | Peer-leader selection for HIV prevention among homeless youth in Los Angeles; "gossip" seeding for immunization in Haryana, India |
| 12 | [**Risk-Based Inspection**](#class-12-risk-based-inspection) (Predictive Inspection / Active Search) | Supervised risk prediction, ranking under an inspection budget, active learning and bandits for search | Finding hidden hazards or cases with a limited number of inspections, tests or audits | Childhood lead-hazard inspections in Chicago; lead-pipe search in Flint, Michigan; Eva COVID-19 border testing in Greece |

### Class definitions

Each class below has a plain-language definition. Other documents in this project link here when they name a class.

#### Class 1: Dynamic State Evolution

*Restless bandits.* Decides, round after round, which few people or units receive a limited intervention when each one's condition keeps changing whether or not you act. Each recipient is an "arm" with a small number of states (for example, adhering or lapsing). The model estimates how likely each state is to change with and without the intervention, and each round it acts where acting now does the most long-run good. Whittle index policies make this tractable at scale.
- **Answers:** "Whom should we reach this week, given that our help wears off and people drift?"
- **Use when:** the resource is reusable each round (calls, visits, sessions), its effect depends on how people respond, and you observe each recipient regularly.
- **Avoid when:** the transfer is one-off and permanent, or you can't observe recipients at least as often as you decide.

#### Class 2: Static Demographic Targeting

*Welfare optimization.* Chooses, once and centrally, how to divide a fixed budget of permanent resources (cash, wells, schools) among people or places to maximize benefit, subject to explicit fairness and legal rules. It is usually written as an integer linear program: decision variables for each option, an objective such as people covered, and constraints for budget, capacity and equity (for example, maximin or leximin across groups).
- **Answers:** "Which options should we fund so the most need is met, fairly and defensibly?"
- **Use when:** the allocation is irreversible, the setting changes slowly, and the decision must be auditable.
- **Avoid when:** recipients choose among options themselves (see Class 5), or the decision repeats every week with feedback (see Class 1).
- **Variants:** the objective can come from a prediction model, as when refugee families are assigned to the locations where they are predicted to find work (see Class 10 for the version where families arrive over time). When eligibility depends on characteristics people report, expect some to change their answers to qualify, and prefer rules that are hard to game.

#### Class 3: Spatiotemporal Security & Adaptive Search

*Security games.* Plans where and when to send mobile patrols when an adversary watches and adapts. Modeled as a Stackelberg game: the defender commits to a randomized patrol strategy, and the adversary picks targets in response. Often combined with a predictive model of where illegal activity is likely, given past patrol effort.
- **Answers:** "How should we patrol so that poachers, loggers or smugglers can't simply avoid us?"
- **Use when:** assets move across geography and the target actively evades or reacts to your presence.
- **Avoid when:** the environment is passive (no one is avoiding you); a simpler routing or coverage model is enough.

#### Class 4: Robust Contingency Planning

*Robust and distributionally robust optimization.* Commits resources before an uncertain event, such as a flood, cyclone or outbreak, so the plan holds up in bad cases, not just the average one. Instead of trusting one forecast, it plans against the worst outcomes, or the worst probability distributions, within a plausible range around the evidence. Often two-stage: commit stock first, adjust dispatch after the event. A related design is *anticipatory action*: agree in advance on a forecast threshold, the action and its funding, so money or supplies are released automatically when the forecast crosses the threshold, before the disaster peaks.
- **Answers:** "How do we prepare when we can't forecast the event and getting it wrong costs lives?"
- **Use when:** the downside is catastrophic and there is little reliable history.
- **Avoid when:** errors are cheap and correctable (exploration is fine), or plentiful data supports an ordinary forecast. Robust plans cost more, by design.

#### Class 5: Strategic Matching Markets

*Stable matching.* Pairs two sides that both have preferences, such as students and schools or apprentices and employers, using a mechanism such as deferred acceptance (Gale–Shapley). The result is *stable*: no pair would both rather be matched with each other than with what they received. When the right side proposes, that side can rank its choices honestly without risk.
- **Answers:** "How do we place people when both sides choose, so placements stick and nobody gains by gaming the system?"
- **Use when:** both sides hold preferences or can refuse, and central assignment has led to refusals, dropouts or strategic ranking.
- **Avoid when:** the planner legitimately assigns centrally and recipients don't choose (see Class 2).

#### Class 6: Participatory Allocation

*Social-choice budgeting.* Splits a shared budget among projects according to the votes of the people affected, as in participatory budgeting. Each resident ranks, approves or builds a budget-feasible bundle of projects (knapsack voting), and a published rule turns the ballots into one funded portfolio. Good rules are proportional, so that a group of voters gets a share of the budget in line with its size (the method of equal shares, the core), and hard to game by strategic voting.
- **Answers:** "How do we let the community decide how the money is split, in a way that is fair to every group of voters?"
- **Use when:** the affected people have a recognized right to decide, there is a menu of costed projects, and legitimacy matters as much as efficiency.
- **Avoid when:** a single planner sets the objective and must defend it to auditors (see Class 2), or each side of a placement holds preferences over the other (see Class 5). Voting is not a substitute for need: pair it with minimum shares for groups with low turnout.

#### Class 7: Effect-Based Targeting

*Policy learning.* Gives a limited program to the people it will *change the most*, rather than to the people who look most in need. It uses data from a pilot or randomized trial to estimate how the program's effect varies across people (heterogeneous treatment effects, for example with causal forests), then learns a simple, auditable rule such as "offer it to households with these characteristics". The rule is checked on held-out data before use.
- **Answers:** "Who should get the program so it does the most good, given that it works much better for some people than for others?"
- **Use when:** you have, or can run, a randomized pilot with a few thousand participants; the effect plausibly varies; and the program is offered once or rarely.
- **Avoid when:** there is no experimental or credible quasi-experimental data, the goal is to reach the neediest as a matter of right (see Class 2), or the decision repeats each week as people's states change (see Class 1). Also check that people cannot easily change their characteristics to qualify.

#### Class 8: Learn-While-Allocating

*Adaptive experimentation.* Spreads effort across several options, such as program variants, messages or sites, when you don't yet know which works best, and shifts effort toward the better ones as results come in. Unlike Class 1, the options don't drift between rounds; unlike Class 3, nobody is adapting to evade you. Methods include Thompson sampling, exploration sampling, and combinatorial bandits when effort is split across many sites at once.
- **Answers:** "We have several options and no idea which works; how do we find out without wasting a whole year on the losers?"
- **Use when:** outcomes arrive quickly enough to adjust several times (weeks, not years), the options are stable, and serving some people with a weaker option while learning is acceptable.
- **Avoid when:** errors are catastrophic (see Class 4), outcomes take longer than the decision cycle, or a donor needs a clean, fixed-arm evaluation (run an ordinary randomized trial instead).

#### Class 9: Routing & Logistics

*Vehicle routing and supply-chain network design.* Decides how goods or people physically move: which depots to use, what to buy where, how much to ship along each route, and the order of stops for each vehicle. Written as a network-flow or vehicle-routing model with costs, capacities, time windows and delivery requirements. Some versions also choose what goes in the basket, such as a food ration that meets nutrition targets at least cost.
- **Answers:** "How do we get the right goods to the right places at least cost, on time?"
- **Use when:** the cost or delay is in the movement itself (fuel, trucks, warehouse space, travel time), with many sites and constraints.
- **Avoid when:** the question is *who* should receive help, not how to deliver it (see Class 2), or delivery is a handful of fixed runs a spreadsheet already handles.

#### Class 10: Online Assignment & Waitlists

*Online allocation and dynamic rationing.* Assigns people or items that arrive one at a time, each of which must be placed (or turned away) before you know what comes next: refugee families to local offices with yearly quotas, housing units to people on a waitlist, donated food to pantries, supplies to requests. The model reserves capacity for likely future arrivals and tracks fairness over the whole season, not just for each decision.
- **Answers:** "This family (or this donation) has arrived now; where should it go, given what is likely to arrive later?"
- **Use when:** arrivals are spread over time, assignments are hard to undo, and capacity used now is unavailable later.
- **Avoid when:** everyone is known up front (see Class 2), both sides hold preferences over each other (see Class 5), or the same people are revisited round after round (see Class 1). For scarce goods with no good outcome data, published priority categories and lotteries may be fairer and easier to defend than an optimizer.

#### Class 11: Network Seeding

*Influence maximization.* Chooses a small number of people to train, brief or recruit so that information or behavior spreads furthest through their social ties. It uses a map of who knows whom (or a cheap proxy, such as asking villagers who is good at spreading news) and a model of how influence passes along ties, then picks the set of people whose combined reach is greatest, avoiding several seeds in the same cluster.
- **Answers:** "We can train only 20 peer leaders; which 20 will reach the most people?"
- **Use when:** the benefit spreads from person to person (health information, a new practice, program awareness) and you can learn something about the social network.
- **Avoid when:** the benefit stays with the person who receives it (see Class 2 or 7), or mapping the network would intrude on people's privacy more than the program justifies.

#### Class 12: Risk-Based Inspection

*Predictive risk ranking and active search.* Decides where to send a limited number of inspections, tests or audits to find hidden problems: lead pipes, unsafe kitchens, infected travelers, at-risk cases. A model scores each home, site or person by the predicted chance of a problem, staff inspect the highest-risk ones, and each finding updates the model. Good designs keep a small random share of inspections, so the model can learn about places it would otherwise never check.
- **Answers:** "We can inspect only 200 of 10,000 homes this year; which ones?"
- **Use when:** the problem is hidden until someone looks, inspections are limited, and records of past inspections and their findings exist.
- **Avoid when:** the target adapts to avoid inspection (see Class 3), the goal is to deliver help rather than to find problems (see Class 2), or past inspections were so selective that the model would only repeat earlier choices.

## 2. The NGO decision tree

The interview runs in two stages. **Stage 1** asks the five filters, one question per turn, and places the problem in one of the five families. **Stage 2** asks at most two narrowing questions inside that family to pick the class. Skip any question the user has already answered, and confirm your reading instead.

### Stage 1: the five filters

| Filter | Ask (one per turn) | What the answer tells you |
|---|---|---|
| **1. The resource and its intent** | "What are you allocating, and what should it achieve?" If unclear, follow with: "Which fits it best: (a) handed over once and kept (cash, a well); (b) given again and again (visits, calls); (c) moved by vehicle to many sites (food, supplies); (d) used to look for something hidden (inspections, tests); (e) a message or practice people should pass on?" | (a) *Who gets a limited resource*. (b) *Repeated decisions that learn*. (c) and (d) *Space, movement and risk*. (e) *Spread through people*. |
| **2. Choice and preferences** | "Who decides who gets what: you, centrally; both sides, who choose and can refuse each other (students and schools); or the community, by voting on how to split a budget?" | Both sides choose, or a vote → *People choose*. Central → keep the family from Filter 1. |
| **3. Environment dynamics** | "Does anyone actively avoid you or adapt to your plans (poachers dodging patrols, applicants changing answers to qualify)?" | An adversary over territory → [**Class 3: Spatiotemporal Security & Adaptive Search**](#class-3-spatiotemporal-security--adaptive-search). Applicants gaming an eligibility rule → keep the class, but use a rule that is hard to game (see the Class 2 variants). |
| **4. Tolerance for being wrong** | "If an allocation turns out wrong, is it a small, fixable loss, or harm to lives or trust?" Then: "What records do you have: past years, pilot or trial results, or nothing yet?" | Catastrophic and little history → [**Class 4: Robust Contingency Planning**](#class-4-robust-contingency-planning), often as a layer on another class. Cheap, fixable errors allow learning (Classes 1 and 8). Trial results open Class 7. |
| **5. Field data and workflow friction** | "How often can staff record data, and with what (paper, Excel, an app; offline)?" Then: "Who would run the tool?" | Rules out classes whose data needs the field cannot meet (see the table below). |

### Stage 2: narrowing questions

Ask only the questions still open for the family, one per turn. If the answers point to two classes, name a primary class and a secondary layer.

**Who gets a limited resource** (Classes 2, 7, 10)
1. "Do you know everyone who could receive it before you decide, or do people or items arrive one at a time and need a decision on the spot?" Arrive one at a time → [**Class 10: Online Assignment & Waitlists**](#class-10-online-assignment--waitlists).
2. "Do you have pilot or trial results showing the program helps some kinds of people much more than others?" Yes → [**Class 7: Effect-Based Targeting**](#class-7-effect-based-targeting). No → [**Class 2: Static Demographic Targeting**](#class-2-static-demographic-targeting).

**Repeated decisions that learn** (Classes 1, 8)
- "Which describes your uncertainty better: how each person's situation changes from week to week, or which of several program options works best?" Each person's situation → [**Class 1: Dynamic State Evolution**](#class-1-dynamic-state-evolution), if staff can observe each person regularly. Which option works → [**Class 8: Learn-While-Allocating**](#class-8-learn-while-allocating).

**Space, movement and risk** (Classes 3, 4, 9, 12)
- "What is the hardest part: outwitting people who avoid you, preparing for a rare disaster, moving goods to many places, or finding hidden problems?" → Class 3, [**Class 4: Robust Contingency Planning**](#class-4-robust-contingency-planning), [**Class 9: Routing & Logistics**](#class-9-routing--logistics) or [**Class 12: Risk-Based Inspection**](#class-12-risk-based-inspection).

**People choose** (Classes 5, 6)
- "Do individual people on both sides rank each other, such as students and schools, or does the community vote on how to split one budget among projects?" → [**Class 5: Strategic Matching Markets**](#class-5-strategic-matching-markets) or [**Class 6: Participatory Allocation**](#class-6-participatory-allocation).

**Spread through people** (Class 11)
- "Do you know, even roughly, who talks to whom, or could people name the trusted messengers in their community?" Yes → [**Class 11: Network Seeding**](#class-11-network-seeding). No → a simpler rule, such as recruiting through existing community leaders, and say so.

### Data each class needs

If the field cannot supply it at the needed rate, choose a simpler class or no optimization at all, and say so.

| Class | Minimum data |
|---|---|
| 1 | Repeated observations of each recipient, weekly or better |
| 2 | A one-off census or survey of candidates and their needs |
| 3 | Incident or patrol logs with locations |
| 4 | Past events plus expert scenarios of worse ones |
| 5 | Ranked preferences from both sides |
| 6 | A costed project list and a voting process |
| 7 | A randomized pilot with outcomes and characteristics for each participant |
| 8 | Outcomes that arrive within weeks of each decision |
| 9 | Locations, travel times and quantities |
| 10 | A history of past arrivals to forecast future ones |
| 11 | At least a rough map of who knows whom |
| 12 | Past inspection records, including those that found nothing |

## 3. Deployment evidence

### Verified references

Well-documented, peer-reviewed sources the assistant may cite by name.

**Class 1 — Restless bandits**
- Whittle, P. (1988). *Restless bandits: Activity allocation in a changing world.* Journal of Applied Probability. — The originating framework and the Whittle index.
- Mate, A., et al. (2022). *Field Study in Deploying Restless Multi-Armed Bandits: Assisting Non-Profits in Improving Maternal and Child Health.* AAAI. — Harvard Teamcore (Milind Tambe's group) with Google Research India and the NGO ARMMAN; prioritizing live service calls in the mMitra program.
- Mate, A., Killian, J., Xu, H., Perrault, A., Tambe, M. (2020). *Collapsing Bandits and Their Application to Public Health Interventions.* NeurIPS. — Tuberculosis medication adherence.
- Killian, J., et al. (2019). *Learning to Prescribe Interventions for Tuberculosis Patients Using Digital Adherence Data.* KDD. — Predictive work on 99DOTS adherence data in India.

**Class 2 — Convex welfare / fairness**
- Church, R., ReVelle, C. (1974). *The maximal covering location problem.* Papers of the Regional Science Association. — The standard integer-programming model for siting facilities (clinics, schools, water points) to maximize population covered.
- Flanigan, B., Gölz, P., Gupta, A., Hennig, B., Procaccia, A. (2021). *Fair algorithms for selecting citizens' assemblies.* Nature. — Leximin-fair selection, adopted by the Sortition Foundation and other practitioners.
- Aiken, E., Bellue, S., Karlan, D., Udry, C., Blumenstock, J. (2022). *Machine learning and phone data can improve targeting of humanitarian aid.* Nature. — Togo's Novissi cash-transfer program with GiveDirectly. Note: this is ML-based *targeting* (predict poverty, then apply an eligibility rule), a useful contrast and complement to explicit welfare optimization.

**Class 3 — Security games and patrol planning**
- Pita, J., et al. (2008). *Deployed ARMOR protection: The application of a game-theoretic model for security at the Los Angeles International Airport.* AAMAS.
- Shieh, E., et al. (2012). *PROTECT: A deployed game-theoretic system to protect the ports of the United States.* AAMAS.
- Fang, F., et al. (2016). *Deploying PAWS: Field Optimization of the Protection Assistant for Wildlife Security.* IAAI.
- Xu, L., et al. (2020). *Stay Ahead of Poachers: Illegal Wildlife Poaching Prediction and Patrol Planning Under Uncertainty with Field Test Evaluations.* ICDE. — Field tests in Uganda and Cambodia.

**Class 4 — Robust and stochastic optimization**
- Rawls, C., Turnquist, M. (2010). *Pre-positioning of emergency supplies for disaster response.* Transportation Research Part B. — Two-stage stochastic programming for hurricane pre-positioning.
- Delage, E., Ye, Y. (2010). *Distributionally robust optimization under moment uncertainty with application to data-driven problems.* Operations Research. — Foundational DRO.
- Mohajerin Esfahani, P., Kuhn, D. (2018). *Data-driven distributionally robust optimization using the Wasserstein metric.* Mathematical Programming.

**Class 5 — Matching markets**
- Gale, D., Shapley, L. (1962). *College admissions and the stability of marriage.* American Mathematical Monthly.
- Roth, A., Peranson, E. (1999). *The redesign of the matching market for American physicians.* American Economic Review. — NRMP.
- Abdulkadiroğlu, A., Pathak, P., Roth, A. (2005). *The New York City High School Match.* AER Papers & Proceedings.
- Abdulkadiroğlu, A., Pathak, P., Roth, A., Sönmez, T. (2005). *The Boston Public School Match.* AER Papers & Proceedings.
- Roth, A., Sönmez, T., Ünver, M. U. (2004). *Kidney Exchange.* Quarterly Journal of Economics.

**Additions to Classes 2 and 4**
- Ahani, N., Andersson, T., Martinello, A., Teytelboym, A., Trapp, A. (2021). *Placement Optimization in Refugee Resettlement.* Operations Research. — Predicts each family's chance of employment in each location, then assigns with an integer program; the basis of Annie MOORE at HIAS. Backtests suggested a 22–38% gain in short-run employment (a backtest on past data, not a trial).
- Björkegren, D., Blumenstock, J., Knight, S. (2020). *Manipulation-Proof Machine Learning.* arXiv 2004.03865. — A field experiment in Nairobi showing how people change their behavior when a scoring rule is used, and a rule that holds up better. A revised version is reported as accepted at the American Economic Review (unverified — please confirm before citing the journal).
- OCHA and the Central Emergency Response Fund (CERF) activated an anticipatory-action pilot in Somalia in June 2020 with up to US$15 million, triggered by projected food insecurity ([Anticipation Hub](https://www.anticipation-hub.org/download/file-3500)).
- GiveDirectly, funded by Google.org, sent cash to about 3,250 households in Kogi State, Nigeria, in 2024 ahead of forecast peak flooding ([GiveDirectly](https://www.givedirectly.org/flood-forecast-ai)).

**Class 6 — Participatory allocation**
- Goel, A., Krishnaswamy, A. K., Sakshuwong, S., Aitamurto, T. (2019). *Knapsack Voting for Participatory Budgeting.* ACM Transactions on Economics and Computation. — Stanford Crowdsourced Democracy Team; used as the ballot in Boston's youth participatory budgeting in 2016.
- Peters, D., Pierczyński, G., Skowron, P. (2021). *Proportional Participatory Budgeting with Additive Utilities.* NeurIPS. — The method of equal shares, used in participatory budgeting votes in Aarau (Switzerland) and Wieliczka (Poland) in 2023.
- Pournaras, E., et al. (2025). *Upgrading Democracies with Fairer Voting Methods.* arXiv 2505.14349. — Aarau's 2023 vote: equal shares funded 17 projects where the standard greedy count would have funded 7 with the same budget.

**Class 7 — Effect-based targeting**
- Wager, S., Athey, S. (2018). *Estimation and Inference of Heterogeneous Treatment Effects using Random Forests.* Journal of the American Statistical Association. — Causal forests.
- Kitagawa, T., Tetenov, A. (2018). *Who Should Be Treated? Empirical Welfare Maximization Methods for Treatment Choice.* Econometrica.
- Athey, S., Wager, S. (2021). *Policy Learning with Observational Data.* Econometrica.
- Athey, S., Keleher, N., Spiess, J. (2025). *Machine Learning Who to Nudge: Causal vs Predictive Targeting in a Field Experiment on Student Financial Aid Renewal.* Journal of Econometrics. — More than 53,000 CUNY students; targeting by estimated effect beat targeting by predicted need.
- Sahoo, R., Blumenstock, J., Niehaus, P., Selker, L., Wager, S. (2025). *What Would it Cost to End Extreme Poverty?* NBER Working Paper 34583. — Learns cash-transfer amounts from household survey data under a budget; a Class 2 problem solved with the learning tools of Class 7.
- Sahoo, R., Lei, L., Wager, S. (2023). *Policy Learning under Biased Sample Selection.* arXiv 2304.11735. — Targeting rules when the trial population differs from the one being served.

**Class 8 — Learn-while-allocating**
- Kasy, M., Sautmann, A. (2021). *Adaptive Treatment Assignment in Experiments for Policy Choice.* Econometrica. — Exploration sampling, applied to recruitment strategies for an agricultural extension service in Odisha, India.
- Caria, A. S., Gordon, G., Kasy, M., Quinn, S., Shami, S. O., Teytelboym, A. (2024). *An Adaptive Targeted Field Experiment: Job Search Assistance for Refugees in Jordan.* Journal of the European Economic Association. — Funded by the International Rescue Committee; the targeting algorithm's gain was small (about 1 percentage point of employment), an honest data point.
- Xu, L., Bondi, E., Fang, F., Perrault, A., Wang, K., Tambe, M. (2021). *Dual-Mandate Patrols: Multi-Armed Bandits for Green Security.* AAAI. — LIZARD, evaluated on real poaching data from Cambodia (an evaluation on historical data, not a field deployment).

**Class 9 — Routing and logistics**
- Peters, K., Silva, S., Gonçalves, R., et al. (2021). *The Nutritious Supply Chain: Optimizing Humanitarian Food Assistance.* INFORMS Journal on Optimization. — WFP's Optimus model; in Iraq it cut costs by 12% at the same nutritional value. WFP reports using Optimus in 44 operations.
- Peters, K., Silva, S., Wolter, T. S., et al. (2022). *UN World Food Programme: Toward Zero Hunger with Analytics.* INFORMS Journal on Applied Analytics. — The 2021 Franz Edelman Award paper; its savings figure covers WFP's analytics work as a whole, not Optimus alone.
- Bertsimas, D., Delarue, A., Martin, S. (2019). *Optimizing schools' start time and bus routes.* PNAS. — Boston Public Schools' routing saved about US$5 million a year and 50 buses. The proposed start-time changes were approved but not implemented after community opposition.

**Class 10 — Online assignment and waitlists**
- Ahani, N., Gölz, P., Procaccia, A., Teytelboym, A., Trapp, A. (2024). *Dynamic Placement in Refugee Resettlement.* Operations Research. — Placement as families arrive through the year, evaluated on HIAS data and incorporated into Annie MOORE.
- Manshadi, V., Niazadeh, R., Rodilitz, S. (2023). *Fair Dynamic Rationing.* Management Science. — Allocating scarce supplies fairly to requests that arrive over time.
- Arnosti, N., Shi, P. (2020). *Design of Lotteries and Wait-Lists for Affordable Housing Allocation.* Management Science.
- Pathak, P., Sönmez, T., Ünver, M. U., Yenmez, M. B. (2024). *Fair Allocation of Vaccines, Ventilators and Antiviral Treatments: Leaving No Ethical Value Behind in Healthcare Rationing.* Management Science. — Reserve categories for scarce medical resources.
- Prendergast, C. (2022). *The Allocation of Food to Food Banks.* Journal of Political Economy. — Feeding America's "Choice System": food banks bid for donated loads as they arrive, using an internal currency. It is an auction with credits, not a two-sided stable match.

**Class 11 — Network seeding**
- Kempe, D., Kleinberg, J., Tardos, É. (2003). *Maximizing the Spread of Influence through a Social Network.* KDD. — The standard formulation and greedy method.
- Banerjee, A., Chandrasekhar, A., Duflo, E., Jackson, M. (2019). *Using Gossips to Spread Information: Theory and Evidence from Two Randomized Controlled Trials.* Review of Economic Studies. — In Haryana, India, seeding immunization reminders with villagers nominated as good spreaders of news raised vaccinations (about 22% in the paper's abstract; J-PAL's summary reports 27%).
- Yadav, A., Wilder, B., Rice, E., et al. (2018). *Bridging the Gap Between Theory and Practice in Influence Maximization: Raising Awareness about HIV among Homeless Youth.* IJCAI. — Pilots with 173 youth in Los Angeles shelters.
- Wilder, B., Onasch-Vera, L., Diguiseppi, G., et al. (2021). *Clinical Trial of an AI-Augmented Intervention for HIV Prevention in Youth Experiencing Homelessness.* AAAI. — 713 youth; risk behavior fell in the arm whose peer leaders the algorithm chose.

**Class 12 — Risk-based inspection**
- Potash, E., Brew, J., Loewi, A., et al. (2015). *Predictive Modeling for Public Health: Preventing Childhood Lead Poisoning.* KDD. — With the Chicago Department of Public Health.
- Abernethy, J., Chojnacki, A., Farahi, A., Schwartz, E., Webb, J. (2018). *ActiveRemediation: The Search for Lead Pipes in Flint, Michigan.* KDD.
- Carton, S., Helsby, J., Joseph, K., et al. (2016). *Identifying Police Officers at Risk of Adverse Events.* KDD. — With the Charlotte-Mecklenburg Police Department.
- Bastani, H., Drakopoulos, K., Gupta, V., et al. (2021). *Efficient and targeted COVID-19 border testing via reinforcement learning.* Nature. — Eva, deployed at Greek borders in 2020; found about 1.85 times as many asymptomatic infected travelers as random testing.
- Obermeyer, Z., Powers, B., Vogeli, C., Mullainathan, S. (2019). *Dissecting racial bias in an algorithm used to manage the health of populations.* Science. — A cautionary case: a risk score that predicted health costs rather than illness under-referred Black patients. Check what any risk score actually predicts.

### Unverified claims (do not cite without confirmation)

The original draft of this taxonomy included the examples below. They could not be confirmed against a primary source. The assistant must not present them as documented facts; if mentioned at all, label them *"(unverified — please confirm before citing)"*.

- **Mantra4Change** using RMABs to rotate physical student toolkits across school sections.
- **"Prof. Roshni Sahu / Data Science for Social Good"** and ILP-targeted cash transfers for extreme poverty. The researcher is Roshni Sahoo (Columbia Business School; see Class 7 for her verified papers). Her work learns transfer rules from survey data; an ILP deployment and a Data Science for Social Good link are not confirmed.
- **UN-OCHA** running DRO for monsoon pre-positioning. Humanitarian pre-positioning is well studied (see Class 4 above), but an OCHA DRO deployment is not confirmed.
- **"Prof. Lily Xu / Harvard Center for Health"** as the lead on tuberculosis adherence calls. Lily Xu is a co-author on related restless-bandit work, but she is best known for PAWS and green-security patrol planning. The TB and maternal-health RMAB deployments are led by Aditya Mate, Jackson Killian, and colleagues in Milind Tambe's Teamcore group.
- **Deceased-donor organ allocation** as stable matching. National organ registries generally allocate deceased-donor organs by priority rules, not a two-sided stable match. Kidney *paired exchange* is the matching-market example.
