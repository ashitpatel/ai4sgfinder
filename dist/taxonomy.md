# AI4SG Allocation Taxonomy

Reference material for the AI4SG Finder assistant. It holds the twelve allocation archetypes, the decision tree for choosing among them, deployment examples graded by how well they are verified, the simpler alternative to each class, the combinations of classes seen in practice, and how to treat input layers such as speech recognition, document extraction and prediction models.

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
- **Avoid when:** the target adapts to avoid inspection (see Class 3), the goal is to deliver help rather than to find problems (see Class 2), or past inspections were so selective that the model would only repeat earlier choices. Take special care when the people scored are the program's own beneficiaries, as in fraud or eligibility checks: a flag is an accusation, and this is where government risk models have most often failed ([Section 6](#when-a-score-targets-the-people-you-serve)).

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

**Every family: a second decision.** Once the class is clear, if any answer hinted at a second decision (a rare disaster in a targeting problem, people who adapt in a search problem, several options whose best choice may differ by group), ask: *"Besides this, is there a second decision in the same program: when to act, where to look first, how it reaches people, or which version works for whom?"* When to act → Class 4 layer; where to look → 12; how it reaches people → 9; which version → 8; for whom → 7. See [When two classes combine](#5-when-two-classes-combine). If nothing hinted at one, skip the question.

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
- Wang, K., Xu, L., Taneja, A., Tambe, M. (2023). *Optimistic Whittle Index Policy: Online Learning for Restless Bandits.* AAAI. — UCWhittle, for learning how recipients respond while allocating; research code at lily-x/online-rmab.

**Class 2 — Convex welfare / fairness**
- Church, R., ReVelle, C. (1974). *The maximal covering location problem.* Papers of the Regional Science Association. — The standard integer-programming model for siting facilities (clinics, schools, water points) to maximize population covered.
- Flanigan, B., Gölz, P., Gupta, A., Hennig, B., Procaccia, A. (2021). *Fair algorithms for selecting citizens' assemblies.* Nature. — Leximin-fair selection, adopted by the Sortition Foundation and other practitioners.
- Aiken, E., Bellue, S., Karlan, D., Udry, C., Blumenstock, J. (2022). *Machine learning and phone data can improve targeting of humanitarian aid.* Nature. — Togo's Novissi cash-transfer program with GiveDirectly. Note: this is ML-based *targeting* (predict poverty, then apply an eligibility rule), a useful contrast and complement to explicit welfare optimization.

**Class 3 — Security games and patrol planning**
- Pita, J., et al. (2008). *Deployed ARMOR protection: The application of a game-theoretic model for security at the Los Angeles International Airport.* AAMAS.
- Shieh, E., et al. (2012). *PROTECT: A deployed game-theoretic system to protect the ports of the United States.* AAMAS.
- Fang, F., et al. (2016). *Deploying PAWS: Field Optimization of the Protection Assistant for Wildlife Security.* IAAI.
- Xu, L., et al. (2020). *Stay Ahead of Poachers: Illegal Wildlife Poaching Prediction and Patrol Planning Under Uncertainty with Field Test Evaluations.* ICDE. — Field tests in Uganda (Murchison Falls) and Cambodia (Srepok).

**Class 4 — Robust and stochastic optimization**
- Rawls, C., Turnquist, M. (2010). *Pre-positioning of emergency supplies for disaster response.* Transportation Research Part B. — Two-stage stochastic programming for hurricane pre-positioning.
- Delage, E., Ye, Y. (2010). *Distributionally robust optimization under moment uncertainty with application to data-driven problems.* Operations Research. — Foundational DRO.
- Stienen, V., et al. (2021). *Optimal depot locations for humanitarian logistics service providers using robust optimization.* Omega. — A modeling study of the WFP-managed UN Humanitarian Response Depot network.
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

**Input layers and fairness checks** (used in [Section 6](#6-input-layers))
- Obermeyer, Z., et al. (2026). *An ECG biomarker for sudden cardiac death discovered with deep learning.* Nature. doi:10.1038/s41586-026-10674-6. — A deep residual network trained on about 440,000 Swedish ECGs linked to death certificates predicts sudden cardiac death within a year; validated without retraining on US (San Diego) and Taiwanese (Taipei) data. Its high-risk group had about a 7% annual rate of sudden cardiac death, against 4.6% for patients flagged by low ejection fraction, the standard test for a defibrillator. A published prediction model a program would use, not build.
- Zink, A., Obermeyer, Z., Pierson, E. (2024). *Race adjustments in clinical algorithms can help correct for racial disparities in data quality.* PNAS. — In a colorectal cancer risk model, family history predicted cancer for White but not Black participants; removing race made the model under-predict risk for Black participants. Removing a group variable is not a fairness check.
- Shanmugam, D., Hou, K., Pierson, E. (2021). *Quantifying disparities in intimate partner violence: a machine learning method to correct for underreporting.* arXiv 2110.04133. — A positive-unlabeled method for estimating how common a condition is in each group when many cases go undiagnosed.
- Gera, N., Pierson, E. (2024). *Testing for racial bias using inconsistent perceptions of race.* arXiv 2409.11269. — Compares traffic stops of the same driver when officers recorded different races (Stanford Open Policing data, Arizona, Colorado and Texas), a design that separates discrimination from differences between drivers.
- Sung, J., Kitonsa, P. J., Nalutaaya, A., et al. (2025). *Performance of universal and stratified computer-aided detection thresholds for chest x-ray-based tuberculosis screening.* Lancet Digital Health. — In Uganda, thresholds stratified by age and sex modestly improved sensitivity at fixed specificity (76.9% against 75.0%); the threshold used for referral to sputum testing changed during the study, changing how many people were tested.
- Willis, A., Lee, C., Krogue, J., et al. (2026). *Generalization of AI-Based Gestational Age Assessment Using Blind Sweep Ultrasonography.* JAMA Network Open. doi:10.1001/jamanetworkopen.2026.22484. — Operators with no ultrasound experience, with Jacaranda Health in Nairobi: mean error 4.2 days for the AI against 4.5 for sonographers.
- Nearing, G., Cohen, D., Dube, V., et al. (2024). *Global prediction of extreme floods in ungauged watersheds.* Nature. — Machine-learning river forecasts in basins without gauges, reliable to a five-day lead; the basis of Google's Flood Hub.
- Chi, G., Fang, H., Chatterjee, S., Blumenstock, J. E. (2022). *Microestimates of wealth for all low- and middle-income countries.* PNAS. — The Relative Wealth Index, at 2.4 km for 135 countries: a ranking of places within a country, not an absolute measure.
- US Centers for Disease Control and Prevention. *FluSight* season evaluations (2023–24 onward). — A public influenza forecasting challenge held every season since 2013–14, with published evaluations; in 2025–26 the ensemble ranked 7th of 39 models.
- Nethil, K., Mishra, V., Anandan, K., Manohar, K. (2025). *Scalable Offline ASR for Command-Style Dictation in Courtrooms.* Interspeech. — Adalat AI's courtroom speech recognition: fine-tuned Whisper models with voice-activity detection, run offline on one GPU per site. Reports speed, not effects on hearings.
- Peskoff, D., Barrow, J., Vu, C., Davenport, D. (2026). *Freeing the Law with LOCUS: A Local Ordinance Corpus for the United States.* arXiv 2606.19334. — About 7 million pages of local codes read with a vision-language OCR model, split into sections, labelled by language models and distilled into a small classifier; released as LOCUS-v1 with a hand-audited subset. An extraction layer at national scale.

**Model-measured outcomes and decisions near the classes** (used in [Section 6](#when-a-model-measures-the-outcome))
- Huang, L. Y., Hsiang, S., Gonzalez-Navarro, M. (2021). *Using Satellite Imagery and Deep Learning to Evaluate the Impact of Anti-Poverty Programs.* NBER Working Paper 29105; arXiv 2104.11772. — Housing quality from daytime satellite images estimated the effect of GiveDirectly's Kenya cash transfers (328 treatment and 325 control villages) consistently with the field survey.
- Barriga-Cabanillas, O., Blumenstock, J. E., Lybbert, T. J., Putman, D. S. (2025). *Probing the limits of mobile phone metadata for poverty prediction and impact evaluation.* Journal of Development Economics. — In Haiti, a cash program's effect was significant in surveys but not in phone-record estimates, which predict spending much less accurately than wealth.
- Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., Zrnic, T. (2023). *Prediction-powered inference.* Science. — Valid confidence intervals from a small directly measured sample plus many model predictions.
- Choo, D., Trabelsi, Y., Getnet, F., et al. (2026). *Optimizing Health Coverage in Ethiopia: A Learning-augmented Approach and Persistent Proportionality Under an Online Budget.* AAAI. — The Health Access Resource Planner, with the Ethiopian Public Health Institute and Ministry of Health; a retrospective proof of concept in three regions.
- Dasgupta, A., Maniyar, M. P., Srivastava, A., et al. (2025). *Learning to Call: A Field Trial of a Collaborative Bandit Algorithm for Optimizing Call Timing in Mobile Maternal Health.* Machine Learning for Healthcare (PMLR 298). — Pilot with about 6,500 participants in India's Kilkari program; pick-up rates improved over random call timing.
- Ozodiegwu, I. D., Ambrose, M., Galatas, B., et al. (2023). *Application of mathematical modelling to inform national malaria intervention planning in Nigeria.* Malaria Journal. — Nigeria's malaria program used the EMOD transmission model to choose its 2021–2025 intervention mix across 774 local government areas.
- Guerrero, O. A., Castañeda, G. (2020). *Policy priority inference: A computational framework to analyze the allocation of resources for the sustainable development goals.* Data & Policy. — An agent-based model linking budget allocations to development indicators, applied with the UNDP office for Mexico's federal government.

**Limits of prediction, grading AI answers, and mobility data** (used in Sections [4](#4-simpler-alternatives-for-each-class) and [6](#6-input-layers))
- Salganik, M. J., Lundberg, I., Kindel, A. T., et al. (2020). *Measuring the predictability of life outcomes with a scientific mass collaboration.* PNAS. — In the Fragile Families Challenge, 160 teams' best predictions of six outcomes were only slightly better than a four-variable benchmark regression.
- Cantrell, E. M., Anchuri, P., Ren, H., Salganik, M. J. (2026). *Machine Learning Models Trained on a Longitudinal Survey Dataset Poorly Predict Hundreds of Life Outcomes.* arXiv 2610.17115. — Most outcomes weren't very predictable, and complex models typically showed little skill over a simple procedure. A preprint.
- McBain, R. K., Cantor, J. H., Hollister, B., et al. (2026). *Development, Validation and AI Chatbot Evaluation of the Adolescent Mental Health AI Response Tool.* Nature Mental Health. — RAND's clinician-informed rubric, scored by three language models checked against human labels; chatbots covered more criteria for anxiety than depression, and for moderate than severe cases.
- Bengtsson, L., Lu, X., Thorson, A., Garfield, R., von Schreeb, J. (2011). *Improved Response to Disasters and Outbreaks by Tracking Population Movements with Mobile Phone Network Data: A Post-Earthquake Geospatial Study in Haiti.* PLOS Medicine. — About 1.9 million SIMs tracked after the 2010 earthquake; the estimated movements matched a later household survey, and cholera-response analyses were delivered within 12 hours of receiving data.
- Ebengo, D., Akilimali, P., et al. (2026). *Early epidemiological and spatial assessment of the Bundibugyo virus outbreak 2026.* Science. doi:10.1126/science.aej4586. — With the DRC's INRB and INSP, Oxford, Imperial and Flowminder: mobility flows from the outbreak's centres predicted which health zones would report cases far better than population-only models, answering responders' questions about where to send resources.

**Governance before use** (used in the playbook's readiness checks)
- OCHA Centre for Humanitarian Data (2019, updated 2020). *Peer Review Framework for Predictive Analytics in Humanitarian Response.* — A readiness assessment, model review and results assessment on technical, ethical and humanitarian-relevance grounds, before a model informs decisions.
- Wilson, K., Sim, M., Gueorguieva, A.-M., Caliskan, A. (2025). *No Thoughts Just AI: Biased LLM Hiring Recommendations Alter Human Decision Making and Limit Human Autonomy.* AAAI/ACM Conference on AI, Ethics, and Society. — In 1,526 resume-screening scenarios with 528 participants, people largely followed an AI's racial bias unless it was severe: a human in the loop is not a safeguard by default.
- Department for Work and Pensions (2025). *Fairness assessment including statistical analysis of the Universal Credit advances machine learning model, 1 April 2024 to 31 March 2025.* UK government. — A published fairness assessment of a deployed fraud model; it could analyse only age among protected characteristics, and non-UK nationals were referred at 2.27 times the rate of UK nationals.
- Williamson, E. J., Walker, A. J., Bhaskaran, K., et al. (2020). *Factors associated with COVID-19-related death using OpenSAFELY.* Nature. — Analysis code runs inside the health-record vendors' data centres and only checked, aggregate results leave: one way to analyse sensitive records without sharing them.

**Scoring the people a program serves** (cautionary; used in [Section 6](#when-a-score-targets-the-people-you-serve))
- Rechtbank Den Haag (2020). *NJCM et al. v. the State of the Netherlands* (SyRI). ECLI:NL:RBDHA:2020:1878 (English). — The legislation for SyRI, a welfare-fraud risk system linking government data, breached Article 8 of the European Convention on Human Rights; the state did not appeal.
- Royal Commission into the Robodebt Scheme (2023). *Report.* Australia. — Debts raised by averaging annual income were not lawful under the Social Security Act; the Federal Court had found the same in 2019.
- Guo, E., Geiger, G., Braun, J.-C. (2025). *Inside Amsterdam's high-stakes experiment to create fair welfare AI.* MIT Technology Review, with Lighthouse Reports and Trouw. — Bias tests and reweighting removed a nationality disparity before deployment; in the 2023 live pilot the model flagged women and Dutch nationals more often, and the city stopped it.
- Elzayn, H., Smith, E., Hertz, T., Guage, C., Ramesh, A., Fisher, R., Ho, D. E., Goldin, J. (2025). *Measuring and Mitigating Racial Disparities in Tax Audits.* Quarterly Journal of Economics. — Race-blind audit selection audited Black taxpayers 2.9–4.7 times as often, driven by prioritising overclaims of refundable credits.
- Muralidharan, K., Niehaus, P., Sukhtankar, S. (2025). *Identity Verification Standards in Welfare Programs: Experimental Evidence from India.* Review of Economics and Statistics. — Biometric authentication for food rations in Jharkhand, randomized across 132 sub-districts, didn't reduce leakage and reduced benefits for some genuine beneficiaries.

**When the AI is the intervention** (used in [Section 6](#when-the-ai-is-the-intervention))
- De Simone, M. E., Tiberti, F. H., Barron Rodriguez, M. R., et al. (2025). *From Chalkboards to Chatbots: Evaluating the Impact of Generative AI on Learning Outcomes in Nigeria.* World Bank Policy Research Working Paper 11125. — Six-week randomized trial of GPT-4 tutoring (Microsoft Copilot) in Edo State: 0.23 standard deviations in English, 0.31 on the combined test.
- Oreopoulos, P., Low, N. (2026). *One Click Away: AI Tutoring with Khanmigo in a Two-Year School Experiment.* NBER Working Paper 35620. — Cluster randomized trial in 18 middle schools in Tennessee: about 0.06–0.08 standard deviations a year, similar to Khan Academy practice without AI.
- Wang, R. E., Ribeiro, A. T., Robinson, C. D., Loeb, S., Demszky, D. (2024). *Tutor CoPilot: A Human-AI Approach for Scaling Real-Time Expertise.* arXiv 2410.03017. — Randomized trial with 900 tutors and 1,800 students: real-time AI suggestions to human tutors raised mastery by 4 percentage points, 9 for students of lower-rated tutors.
- Korom, R., Kiptinness, S., Adan, N., et al. (2025). *AI-based Clinical Decision Support for Primary Care: A Real-World Study.* arXiv 2507.16947. — OpenAI and Penda Health: 39,849 visits in 15 Kenyan clinics; 16% fewer diagnostic and 13% fewer treatment errors, relative. Observational, funded by OpenAI.
- Agweyu, A., Mwaniki, P., Menon, V., et al. (2026). *Generative AI-enabled clinical decision support system in primary care: a pragmatic, cluster-randomized trial.* Nature Medicine. — The same tool in a randomized trial: treatment failure within 14 days 2.2% with AI against 2.0% without, no significant difference, though expert panels rated clinicians' plans better.

**Simpler rules and combined designs** (used in [Section 4](#4-simpler-alternatives-for-each-class) and [Section 5](#5-when-two-classes-combine))
- Mate et al. (2022), above, also report that a simple round-robin calling schedule did not significantly improve on ARMMAN's usual practice, while the restless-bandit schedule reduced engagement drops by about 30%: evidence that the simplest rotation is not always close enough.
- Aiken et al. (2022), above, compare the phone-data model with simpler options: it reduced errors of exclusion by 4–21% relative to the geographic targeting the government considered, but had 9–35% more exclusion errors than targeting based on a comprehensive social registry, which Togo did not have.
- Hanna, R., Olken, B. (2018). *Universal Basic Incomes versus Targeted Transfers: Anti-Poverty Programs in Developing Countries.* Journal of Economic Perspectives. — Compares giving to everyone with targeting, using data from Indonesia and Peru; the simplest option is a serious benchmark.
- Abdulkadiroğlu, A., Sönmez, T. (2003). *School Choice: A Mechanism Design Approach.* American Economic Review. — The old Boston "first choices first" rule is not strategy-proof; student-proposing deferred acceptance is.
- Clarke, G., Wright, J. W. (1964). *Scheduling of Vehicles from a Central Depot to a Number of Delivery Points.* Operations Research. — The savings method, a routing heuristic that can be run by hand.
- Hadad, V., Hirshberg, D., Zhan, R., Wager, S., Athey, S. (2021). *Confidence intervals for policy evaluation in adaptive experiments.* PNAS. — Standard estimates from adaptive experiments can be biased; a fixed equal split keeps the usual analysis valid.
- Kim, D. A., Hwong, A. R., Stafford, D., et al. (2015). *Social network targeting to maximise population behaviour change: a cluster randomised controlled trial.* The Lancet. — In 32 Honduran villages, training the friends that random villagers named raised take-up of a multivitamin offer over random seeding; choosing the most-named people did not.
- Kempe et al. (2003), above, found greedy seed selection beat a high-degree rule by about 18% in one of their models; the size of the gap depends on how influence spreads.
- Gholami, S., Ford, B., Fang, F., et al. (2017). *Taking it for a Test Drive: A Hybrid Spatio-temporal Model for Wildlife Poaching Prediction Evaluated through a Controlled Field Test.* ECML PKDD. — Rangers in Queen Elizabeth National Park, Uganda, patrolled areas the model rated high and low risk and found more signs of poaching in the high-risk ones: the prediction layer of a combined prediction-and-patrol design.
- Xu et al. (2020), above, combine poaching prediction with patrol planning that accounts for the prediction's uncertainty; field tests in Murchison Falls National Park (Uganda) and Srepok Wildlife Sanctuary (Cambodia).
- Pople, A., Hill, R., Dercon, S., Brunckhorst, B. (2021). *Anticipatory Cash Transfers in Climate Disaster Response.* CSAE Working Paper 2021-07, University of Oxford; published as *The Importance of Being Early? Anticipatory Cash Transfers for Flood-Affected Households,* World Bank Economic Review (2026). — WFP sent mobile-money transfers to pre-registered households in Bangladesh about five days before the July 2020 flood peak; recipients were 36% less likely to go a day without eating during the flood (working-paper figure). A forecast trigger, a pre-agreed recipient list and a delivery channel working together.
- Bansak, K., Ferwerda, J., Hainmueller, J., et al. (2018). *Improving refugee integration through data-driven algorithmic assignment.* Science. — Prediction plus assignment (GeoMatch); backtests on registry data in the US and Switzerland suggested employment gains of roughly 40–70% over current practice (a backtest, not a field trial).

### Unverified claims (do not cite without confirmation)

The original draft of this taxonomy included the first five examples below, and later reviews added the rest. They could not be confirmed against a primary source. The assistant must not present them as documented facts; if mentioned at all, label them *"(unverified — please confirm before citing)"*.

- **Mantra4Change** using RMABs to rotate physical student toolkits across school sections.
- **"Prof. Roshni Sahu / Data Science for Social Good"** and ILP-targeted cash transfers for extreme poverty. The researcher is Roshni Sahoo (Columbia Business School; see Class 7 for her verified papers). Her work learns transfer rules from survey data; an ILP deployment and a Data Science for Social Good link are not confirmed.
- **UN-OCHA** running DRO for monsoon pre-positioning. Humanitarian pre-positioning is well studied (see Class 4 above), but an OCHA DRO deployment is not confirmed.
- **"Prof. Lily Xu / Harvard Center for Health"** as the lead on tuberculosis adherence calls. Lily Xu is a co-author on related restless-bandit work, but she is best known for PAWS and green-security patrol planning. The TB and maternal-health RMAB deployments are led by Aditya Mate, Jackson Killian, and colleagues in Milind Tambe's Teamcore group.
- **Deceased-donor organ allocation** as stable matching. National organ registries generally allocate deceased-donor organs by priority rules, not a two-sided stable match. Kidney *paired exchange* is the matching-market example.
- **Adalat AI's productivity results and scale.** Trials showing faster hearings are mentioned in Adalat AI's own materials but not published; reported courtroom counts differ by source and date. Cite Nethil et al. (2025) for the method only.
- **Gera & Pierson in Science Advances.** A 2025 Science Advances version of Gera & Pierson (2024) (doi:10.1126/sciadv.adx5829) is reported but could not be confirmed; cite the arXiv preprint above.
- **Policy Priority Inference in two countries.** A UNDP page reportedly says it has been used in two Latin American countries; only Mexico is confirmed from a primary source (Colombia is likely).
- **Michigan's MiDAS error rate.** A widely quoted figure that 93% of the unemployment agency's automated fraud findings were wrong comes from a 2016 news report of a state review of a subset of cases; the agency's own 2017 review gave different figures. The US$20 million settlement (Bauserman v. Unemployment Insurance Agency, final approval 2024) is documented.
- **LOCUS at NeurIPS 2026.** Reported as accepted by Berkeley News; cite the arXiv version until the proceedings appear.

## 4. Simpler alternatives for each class

Every class has a simpler option that needs only paper, a spreadsheet or a calculator. Sometimes it is nearly as good as the full method; sometimes it gives up most of the gain. The assistant names the best simple option in every recommendation, says in what ways it comes close, and lists the assumptions the user must check before settling for it.

Prediction has limits worth knowing before any model is built. In the Fragile Families Challenge, 160 teams' best predictions of six children's life outcomes were only slightly better than a regression with four variables chosen by an expert (Salganik et al., 2020); a 2026 follow-up across hundreds of outcomes found complex models typically added little over a simple procedure (Cantrell et al., 2026). When a class leans on predicting people's outcomes, expect the simple option to come close.

Close is never one number. A simple rule can match the model on the total outcome and still differ on fairness across groups or over time, on robustness to surprises, on resistance to gaming, on the quality of evidence it produces, or on how easily staff can explain it. Name which of these it matches and which it gives up.

The "illustrative result" column comes from the [tutorials](../../docs/tutorials/): invented data built to teach each method, so the figures show the *kind* of gap to expect, not a forecast. Quote them only as illustrations.

| Class | Simplest good option | Illustrative result (tutorial) | Close in what ways | Check before settling for it |
|---|---|---|---|---|
| 1 Dynamic State Evolution | A six-cell table in Excel: for each group and state, (visit odds − no-visit odds) × (value gap); visit the highest each week | Matched the Whittle policy exactly; rotation gained less than half as much, and a risk score almost nothing | Same patients chosen when the table ranks cells in the same order as the exact index | A visit's effect is short-lived, or the order matches the exact index when checked once; it still needs weekly per-person records. Evidence: in ARMMAN's field study, round-robin calling did not beat usual practice (Mate et al., 2022) |
| 2 Static Demographic Targeting | Greedy in a spreadsheet: add the option that covers the most *new* people, with a per-district floor | Matched the integer program with a 20% floor, same 25 sites | Total covered and the floor, when catchments barely overlap | Few villages in three or more catchments; one simple fairness rule (maximin or several interacting rules need the integer program); it can't show what fairness costs. For cash, compare with geographic or universal transfers (Aiken et al., 2022; Hanna & Olken, 2018) |
| 3 Spatiotemporal Security | (a) A weighted lottery: each zone's chance in proportion to its value; (b) Goal Seek on the equilibrium formula | (a) About two-thirds of the game's effect; (b) exactly the game's plan | (a) Unpredictability, the essential property; (b) everything, for a simple game | (b) needs a zero-sum game (your loss is their gain), one penalty, and zones that can be patrolled in any combination; connected routes need the LP. Never a fixed rotation or hotspot list |
| 4 Robust Contingency Planning | Spread stock evenly (or in proportion to the people each site can reach) across sites that serve different areas | Matched or beat the robust plans on the worst case; about 6 points lower on the average storm than the DRO plan | Robustness, because nothing leans on one road or site | Sites are alike in people and exposure; history is too thin to trust; every site can store and protect the stock. It gives no dispatch cards or price of robustness |
| 5 Strategic Matching Markets | Deferred acceptance run by hand: envelopes per employer, rounds of proposals | Identical: the algorithm is the simple option | Everything | Up to a few hundred people; employers' rankings exist before the match; tie-break lottery drawn first. Not "first choices first", which invites strategic ranking (Abdulkadiroğlu & Sönmez, 2003) |
| 6 Participatory Allocation | Area envelopes: split the budget by area, greedy count within each, leftovers by greedy overall; or equal shares in a free web tool | Envelopes by ballots landed within one project of equal shares and resisted a bloc better | Fairness across areas | Voters mostly back projects in their own area; groups that matter are places, not renters or young people; few cross-area projects; envelope sizes agreed in advance |
| 7 Effect-Based Targeting | A pivot table of the randomized pilot: effect by subgroup, fund the best one or two groups, checked on the held-out half | One question captured about 60% of the best rule's gain over a lottery; two questions matched it | The total gain, when the effect depends on one or two characteristics | Still needs the randomized pilot; check on held-out data; groups large and characteristics verifiable; a causal forest once shows whether the pattern is simple |
| 8 Learn-While-Allocating | An equal split for a fixed number of weeks, then switch everyone to the winner | Picked the best option nearly as often; gave up about 50 good outcomes over a season when one option was clearly better, none when differences were small | The final choice, and better evidence (valid standard intervals; Hadad et al., 2021) | Two to four options; a short test; serving weaker options for a few weeks is acceptable. Many options or a harmful one favor the adaptive design |
| 9 Routing & Logistics | Clarke–Wright savings by hand per day, or a free route planner (VROOM, OR-Tools) | The heuristic was 0–2.3% longer than the exact plan; most of the 47.5% saving came from replacing habit with any systematic method | Distance and on-time delivery | Few, wide time windows for hand work; one truck type; a travel-time table drivers trust, which no shortcut replaces |
| 10 Online Assignment & Waitlists | Greedy from a printed table of predicted chances, with quarterly allotments per site; or published priority categories and a lottery | Captured about 72% of re-solving's gain and was about as fair to early and late arrivals | Fairness over time; no dependence on a forecast | Arrivals roughly even through the year (or allotments shaped to the expected pattern); trustworthy predictions; whether the remaining gain justifies an analyst's weekly time |
| 11 Network Seeding | Count friends, spread across friend groups; or ask "who here is good at spreading news?"; or train the friends people nominate | Within 6% of greedy reach, far above staff picks | Total reach, when friend groups are clear and messages don't travel far | Groups identifiable; the gap grows when messages spread easily. Field evidence for the asking rules: Banerjee et al. (2019), Kim et al. (2015) |
| 12 Risk-Based Inspection | Sort by the strongest known risk factor (e.g. year built), plus a small random share | About 85% of the model's finds; with the random share, an unbiased estimate of the total | Finds, when one factor carries most of the risk; honest totals, with the random share | Check on past records that the factor separates hits from misses; it can't learn from this year's results or spot an area worse than its age suggests |

**How to decide whether the simple option is close enough.** Recommend these steps:
1. **Replay the past.** Apply the simple rule and, with a partner, the full method to last year's records, and compare on every dimension that matters (total, fairness, worst case), not just the total.
2. **Price the gap.** Set the difference against the full cost of the model: building it, the data pipeline it needs, staff time each cycle, and someone to maintain it after the partner leaves. If the gap is small or uncertain, start simple.
3. **Make the simple rule the comparison arm.** If the model is built, the pilot compares it with the best simple rule, not with current practice. A model that can't beat a good spreadsheet in the pilot shouldn't be scaled.
4. **Keep the parts no shortcut replaces.** In most classes the expensive part is the data (transition records, a randomized pilot, a travel-time table, a random share of inspections), not the computation. A simple rule fed with biased data fails the same way the model would.
5. **Revisit when assumptions change.** A simple rule that is close today can drift when sites, populations or behavior change. Recheck yearly with the same replay.

## 5. When two classes combine

Many real programs make two linked decisions. The assistant names a primary class and a secondary layer only when the user describes a second decision, and asks for it directly when the answers hint at one: *"Besides this, is there a second decision in the same program: when to act, where to look first, how it reaches people, or which version works for whom?"*

| Combination | Signal in the interview | How the pieces fit | Real example |
|---|---|---|---|
| 4 + 2 (and often 9) | Catastrophic, rare event (Filter 4) *and* a one-off transfer to selected people (Filter 1 a) | A forecast trigger decides *when*; a pre-agreed targeting rule decides *who*; logistics or mobile money decides *how* | WFP's anticipatory cash before the 2020 Bangladesh floods (Pople et al., 2021); OCHA/CERF Somalia pilot (2020); GiveDirectly in Kogi State, Nigeria (2024) |
| 12 + 3 | Something hidden must be found (Filter 1 d) *and* the people responsible adapt (Filter 3) | A risk model predicts where activity is likely; a randomized patrol plan stops them learning where rangers go | PAWS: poaching prediction field-tested in Uganda (Gholami et al., 2017) and combined with patrol planning in Uganda and Cambodia (Xu et al., 2020) |
| 8 + 7 | Several options of unknown value (Filter 1 b, narrowing) *and* a reason to think the best option differs by group | An adaptive experiment that learns which option works *for whom*, shifting each group toward its best option | Job-search assistance for refugees in Jordan (Caria et al., 2024); the targeting gain was small, an honest data point |
| 10 + prediction | Arrivals one at a time (narrowing) *and* outcome records by site | A model predicts each arrival's outcome at each site; the online rule places them | Annie MOORE at HIAS (Ahani et al., 2021, 2024); GeoMatch backtests (Bansak et al., 2018) |
| 9 + 2 | Goods moved to many sites (Filter 1 c) *and* a choice of what to send or buy | One network model chooses the basket, the sources and the routes together | WFP's Optimus (Peters et al., 2021) |
| 6 + 2 | A community vote (Filter 2) *and* a duty to protect low-turnout groups | The vote decides; a published minimum share per area protects need | Case 7's area reserve |
| 1 + 8 | Each person's state drifts *and* nobody yet knows how people respond to the intervention | Learn the response while scheduling, with optimism for little-tested groups | UCWhittle (Wang et al., 2023): a research method with public code, not a field deployment |

Rules for combinations:
- **One primary class.** It answers the decision the user asked about; the layer feeds or constrains it. Deliver the recommendation for the primary class, then add a short paragraph on the layer: what it adds, the data it needs, and its simpler option.
- **Sequence them.** Usually the layer that produces inputs (a forecast, a risk map, a prediction) is piloted first, because the other depends on it; say so in the next steps.
- **Each layer has its own simple option.** A combination of two simple rules (a forecast threshold plus a published eligibility list; an age sort plus a weighted lottery) is often the right first year.
- **Don't invent combinations.** If the user describes one decision, recommend one class.

## 6. Input layers

Some programs ask about a tool that allocates nothing on its own: it turns speech, images, documents, records, weather data or satellite images into something a decision uses. These are **input layers**. The assistant doesn't classify the tool or recommend a model architecture for it. It names the decision the tool feeds, classifies *that* decision, and treats the tool as a layer to check and pilot first ([Section 5](#5-when-two-classes-combine)). If no decision is fed, say so: the tool may be worth having, but it is outside this taxonomy.

| Kind | What it produces | Decision it typically feeds | Real example |
|---|---|---|---|
| **Perception** | Text from speech, translations, labels from images or signals | Often none: it replaces manual work. Sometimes a rollout order (usually *no model needed*) | Adalat AI's courtroom speech recognition in Indian languages (Nethil et al., 2025) |
| **Extraction** | A table from documents (OCR, then language-model labels) | A yearly plan or a ranking (Class 2, Class 12) that needs a column no one has typed | LOCUS, a corpus of US local ordinances (Peskoff et al., 2026) |
| **Prediction** | A risk score from records | Where to look (Class 12), where to place (Class 10) | A deep-learning ECG model for sudden cardiac death risk (Obermeyer et al., 2026) |
| **Screening classifier** | A flag from a cheap test: a cough recording, an ultrasound sweep, an X-ray, a photo of a crop or a slide | Whom to refer for a confirmatory test or treatment (Class 12) | Computer-aided chest X-ray reading for TB screening in Uganda (Sung et al., 2025); novice ultrasound sweeps read by AI in Kenya (Willis et al., 2026) |
| **Forecast** | The chance of a flood, outbreak, storm or shortage, days to months ahead | When to act (Class 4 trigger), where to pre-position (Class 4, 9), or a warning sent to people directly | Google's flood forecasts for basins without river gauges (Nearing et al., 2024); the US CDC's flu forecasting challenge |
| **Geospatial layer** | A ready-made map: buildings, population, relative wealth, damage; or where people are moving, from anonymised phone data | Where people are and who is poorest (Class 2), where to look (Class 12), where to patrol (Class 3), where an outbreak will spread next (Class 4) | Meta and Berkeley's Relative Wealth Index (Chi et al., 2022); phone mobility in the 2026 Bundibugyo outbreak in the DRC (Ebengo et al., 2026) |

**Build, adapt or use.** Ask how many outcomes the program has on record.
- **Use a published model** when local outcomes are too few to train one (a few hundred events, against the hundreds of thousands a deep model was trained on). Validate it on the program's own records before relying on it: does it rank well, are its predicted rates right (calibration), and does it hold for each group? A model can rank well in a new place and still mis-state absolute risk, which changes how many people pass a threshold.
- **Adapt an open model** (fine-tune it on local data) when a good general model exists but local speech, language or documents differ, as with speech models fine-tuned for Indian languages and legal vocabulary.
- **Build** only when the program has many outcomes, a technical partner, and someone to maintain it.

**What to measure before an allocation relies on it.** Always on the program's own data, never a published benchmark alone:
- *Perception:* error rate by language, accent or condition (and, for a language with few speakers online, whether any evaluation set exists for it), and separately for what matters most (names, numbers, legal terms); who corrects errors and how long correction takes compared with the manual process.
- *Extraction:* label accuracy on a random sample checked by hand, reported by source type (scanned or digital, large or small jurisdiction), since errors cluster where documents are poorest. For a pipeline that screens a live stream (news, radio, messages) for analysts, keep checking a sample after launch: accuracy measured on past data can collapse once the stream changes, and the threshold should cap what analysts can read.
- *Prediction:* calibration and accuracy by group; what the label actually measures (Obermeyer et al., 2019); whether a high score means high benefit or only high risk, including the risk of other outcomes first (competing risk).
- *Screening classifier:* sensitivity and specificity against the reference test (a lab test, a sonographer, a pathologist) in the population served, not the one it was trained on; the threshold, set so the number flagged matches the capacity to test and treat them; and what happens after the flag, since lost follow-up, missing reagents or power cuts can undo an accurate model.
- *Forecast:* skill where the program works, compared with a simple baseline (last year, the seasonal average, the agency's current warning), at the lead time the decision needs; how often it would have triggered in past seasons, including false alarms and misses; and who acts on it, by when. A forecast sent straight to people is an intervention of its own: measure whether they received it, believed it and acted differently.
- *Geospatial layer:* when it was made, since a stale map misses new settlements (phone mobility data is the exception: it can be ready within days, and is worth arranging with operators before an emergency); whether its score is calibrated or only a ranking; whether its labels agree with another source (damage labels from drone and satellite images can disagree on many buildings) (a relative wealth index ranks places within a country, it doesn't measure poverty in dollars); and a check against a sample of places on the ground.
- *All:* cost per unit, what happens when the layer fails, and the manual process kept as a fallback.

**Fairness of a score is checked, not assumed.** Removing race or another group variable from a model doesn't make it fair: if a predictor is recorded less reliably for one group, a model without the group variable can under-predict that group's risk (Zink, Obermeyer & Pierson, 2024). Labels such as "diagnosed" miss people who were never tested, so groups with less access look lower-risk than they are (Shanmugam, Hou & Pierson, 2021). Measure calibration and share of slots by group either way.

Rules for input layers:
- **Name the decision first.** "Build a transcription system" or "build a database" is a means; ask what will be decided with its output, and by whom.
- **Pilot the layer first,** with its error measured, before the allocation that depends on it.
- **Don't choose the model.** Point to the providers' model cards and evaluation reports; the assistant's evidence base covers allocation methods, not speech, vision or language models.

### When a score targets the people you serve

Risk scores that flag a program's own beneficiaries, for fraud, overpayment or loss of eligibility, are the most common government use of these models and the most common failure. The Dutch SyRI system was struck down by a court for breaching the right to private life (Rechtbank Den Haag, 2020). Australia's Robodebt raised debts by averaging income, which a Royal Commission found was unlawful (2023). Amsterdam built a welfare model with bias tests and reweighting, and in its live pilot it still flagged women and Dutch nationals more often; the city stopped it (MIT Technology Review, Lighthouse Reports and Trouw, 2025). Two lessons go beyond the model:
- **The objective can cause the disparity.** The US tax authority's audit selection never used race, yet Black taxpayers were audited 2.9–4.7 times as often, because the system prioritised overclaims of refundable credits (Elzayn et al., 2025).
- **Checking identity can exclude people.** In Jharkhand, India, fingerprint checks for food rations didn't reduce leakage and cut benefits for some genuine recipients (Muralidharan, Niehaus & Sukhtankar, 2025).

When a user or a proposal scores beneficiaries, the assistant says so plainly and requires, before any pilot: a legal basis; a person reviewing every flag before anything happens to the beneficiary; a way for people to see why they were flagged and appeal; the fairness audit in the playbook, published; and a comparison with how caseworkers choose today. If these can't be met, recommend against the model.

### When the AI is the intervention

Sometimes the tool *is* the program: a tutor, a coach for health workers, a farm or legal adviser, a triage line. It allocates nothing, so no class applies to it. But how to test it is a method question, and the evidence points both ways:
- A six-week randomized trial of GPT-4 tutoring after school in Edo State, Nigeria, raised English scores by 0.23 standard deviations (De Simone et al., 2025).
- A two-year cluster randomized trial of Khanmigo in 18 US middle schools found gains of about 0.06–0.08 standard deviations a year, similar to Khan Academy practice without AI (Oreopoulos & Low, 2026).
- An AI tool giving human tutors real-time suggestions raised students' mastery by 4 percentage points in a trial with 900 tutors (Wang et al., 2024).
- In Kenyan primary-care clinics, an AI clinical copilot cut diagnostic errors by 16% in an observational study (Korom et al., 2025), but a cluster randomized trial found no significant reduction in treatment failure (Agweyu et al., 2026).

The assistant asks: does the AI support a worker, or replace one? When does a person take over? What outcome, not usage, will show it works, and against what comparison? To check its answers in a sensitive area, use a rubric written with experts and check any automated grading against people's: RAND tested chatbots' replies to simulated adolescents with mental-health needs this way, scoring with three language models checked against human labels (McBain et al., 2026). Recommend testing it like any program: an A/B test between versions ([Class 8](#class-8-learn-while-allocating) when several are tried), then a randomized pilot against current practice, with answers graded against an expert's on a sample. If the tool decides who gets help (scoring applications, choosing who sees a nurse first), that part is an allocation and is reviewed as usual.

### When a model measures the outcome

Some programs, and many evaluations, use a model in place of a survey to measure whether something worked: satellite images for household wealth, phone records for spending, image grading for test scores, camera traps for wildlife. It can work. Satellite images of housing quality estimated the effect of GiveDirectly's cash transfers in Kenya consistently with the field survey (Huang, Hsiang & Gonzalez-Navarro, 2021). It can also fail. In Haiti, a cash program's effect was positive and significant in surveys but not detectable in phone-record estimates, because phone data predicts spending much less well than wealth (Barriga-Cabanillas et al., 2025).

So the assistant asks: has the proxy been checked against a direct measure *of the outcome that should change*, in this population? Recommend keeping a direct measure on a random sample, and combining it with the model's predictions for the rest, which gives valid confidence intervals whatever model is used (prediction-powered inference: Angelopoulos et al., 2023). Treat a proxy that detects no effect as weak evidence of no effect. The same caution applies to estimating an effect from records without a randomized comparison: different estimators can give different verdicts on the same program, so prefer a randomized pilot, or report several estimates and say they disagree.

### Decisions near the twelve classes

The expanded scan found decisions that look new but are usually variants of an existing class. Classify them this way:

| Decision | Treat as | Example |
|---|---|---|
| Which health posts to upgrade as the budget arrives year by year | Class 2, re-solved each budget year; Class 10 if requests arrive one at a time | HARP, built with the Ethiopian Public Health Institute and Ministry of Health (Choo et al., 2026; retrospective, not yet policy) |
| Where to send survey teams under a travel budget | Class 2 (coverage under a budget), allocating measurement rather than help | |
| When to call or visit, not whom | Class 8, with time slots as the options | Call-time learning in India's Kilkari maternal messaging program raised pick-up rates over random timing in a field pilot with about 6,500 mothers (Dasgupta et al., 2025) |
| Which sites to protect so habitats stay connected | Class 2 with connectivity constraints | |
| What subsidy or price to set | Class 7 if a trial varies it; otherwise a research question for an economist | |
| Which villages or districts a program enters next | Class 2, with a fixed cost for each new site; a model predicting where need is highest is the input layer | |
| Where to draw zones or boundaries (school attendance zones, service areas) | Class 2 with contiguity and balance constraints; when residents set the weights, combine with Class 6 | |
| Which cases in a backlog to hear or process first (dockets, asylum claims) | Class 10 (a queue with arrivals and fairness over time) | |
| Which people are already eligible under written rules (early release, benefits, fee waivers) | **No model needed:** a rules engine or checklist applied to the records, with a way to appeal; prediction adds nothing when the rules decide | |
| Where surplus food or medicine should go as donations come in | Class 10 if donations arrive one at a time and must be placed; Class 9 if the question is moving them | |
| Which crisis calls go to which responders, live | Class 10 (calls arrive and must be assigned now), with Class 9 for routes; a model that reads location and urgency from messages is the input layer | |
| Which polluters, contractors or facilities to inspect or hold to account | Class 12 | |
| Which grants or investments a funder backs | Class 2 for a portfolio under a budget; a model that drafts or screens applications is an input layer, and the [funder review](playbook.md#funder-review-checking-a-proposal) covers checking an AI proposal | |
| Whether past human decisions (court rulings, caseworker choices) were biased | An audit, not an allocation: an extraction layer to read the records, then a test that compares like with like; a research partner | |
| How to split a fixed national stock of medicines or supplies across facilities each cycle | Class 9 (a supply network), with a demand forecast as the input layer; staff keep the right to override | |
| Which statements a divided group can agree on (dialogues, citizens' panels) | Not an allocation; the nearest family is Class 6. Tools that draft and rank statements are deliberation aids: judge them by whether participants endorse the result | |
| Which of the program's current clients get extra outreach | Class 1 if repeated and states drift; Class 7 if a trial shows who benefits; a risk ranking alone measures need, not benefit (see Case 17) | |

**Choosing a rule by simulation.** Some decisions set a rule for everyone at once: a national budget split, a malaria intervention mix, a policy to test before rollout. Simulation models (agent-based or transmission models) let planners compare options before acting. Nigeria's malaria program used a transmission model to choose its intervention mix for each of 774 local government areas in its 2021–2025 strategic plan (Ozodiegwu et al., 2023), and UNDP used Policy Priority Inference, an agent-based model linking budgets to development indicators, with Mexico's federal government (Guerrero & Castañeda, 2020). This is not a thirteenth class: it is a modelling partnership, built and calibrated by specialists, and its results are only as good as the model's validation, which is often weak. When a user describes such a decision, name the approach, say it needs a modelling partner (for example an academic group or the Institute for Disease Modeling for malaria), and recommend comparing its plan with a simple scenario table built from past data.