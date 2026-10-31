# AI4SG Allocation Taxonomy

Reference material for the AI4SG Finder assistant. It holds the five allocation archetypes, the decision tree for choosing among them, and deployment examples graded by how well they are verified.

## 1. The five allocation archetypes

| # | Class | Core mathematics | Best-suited problem space | Representative field deployments |
|---|-------|------------------|---------------------------|----------------------------------|
| 1 | [**Dynamic State Evolution**](#class-1-dynamic-state-evolution) (Restless Bandits) | Restless multi-armed bandits (RMAB), Markov decision processes (MDP), Whittle index policies | Probabilistic behavioral nudges; systems with novelty decay or passive state change over time; volatile environments | ARMMAN mMitra maternal-health call scheduling (India); tuberculosis medication-adherence interventions on 99DOTS data |
| 2 | [**Static Demographic Targeting**](#class-2-static-demographic-targeting) (Convex Welfare Optimization) | Integer linear programming (ILP), convex optimization, maximin / leximin fairness, welfare metrics | Distribution of irreversible, transactional capital; slow-moving, stable environments; strict legal auditability and democratic transparency | Fair selection of citizens' assemblies (leximin, Sortition Foundation); targeting of cash transfers; siting of schools and water points |
| 3 | [**Spatiotemporal Security & Adaptive Search**](#class-3-spatiotemporal-security--adaptive-search) (Predictive Patrol) | Stackelberg security games, spatial point processes, reinforcement learning (e.g. deep Q-networks) | Allocating mobile patrol assets over physical geography; adversarial or adaptive environments where the target reacts to your moves | PAWS anti-poaching patrol planning (Uganda, Cambodia); ARMOR airport checkpoints (LAX); PROTECT (US Coast Guard) |
| 4 | [**Robust Contingency Planning**](#class-4-robust-contingency-planning) (Robust / Distributionally Robust Optimization) | Distributionally robust optimization (DRO), stochastic programming, minimax over uncertainty sets | High uncertainty with severe downside (life-or-death outcomes); no historical data or adversarial shocks | Pre-positioning of emergency supplies before hurricanes and floods; vaccine and medicine stockpiling under unknown demand |
| 5 | [**Strategic Matching Markets**](#class-5-strategic-matching-markets) (Two-Sided Market Design) | Deferred acceptance (Gale–Shapley), stable matching, exchange mechanisms, network flow | Two-sided systems where individuals on both sides hold their own preferences; a planner who cannot dictate outcomes without respecting local choice | NYC and Boston public school choice; the US medical residency match (NRMP); kidney paired-donation exchange; Feeding America's food-bank "Choice System" |

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

#### Class 3: Spatiotemporal Security & Adaptive Search

*Security games.* Plans where and when to send mobile patrols when an adversary watches and adapts. Modeled as a Stackelberg game: the defender commits to a randomized patrol strategy, and the adversary picks targets in response. Often combined with a predictive model of where illegal activity is likely, given past patrol effort.
- **Answers:** "How should we patrol so that poachers, loggers or smugglers can't simply avoid us?"
- **Use when:** assets move across geography and the target actively evades or reacts to your presence.
- **Avoid when:** the environment is passive (no one is avoiding you); a simpler routing or coverage model is enough.

#### Class 4: Robust Contingency Planning

*Robust and distributionally robust optimization.* Commits resources before an uncertain event, such as a flood, cyclone or outbreak, so the plan holds up in bad cases, not just the average one. Instead of trusting one forecast, it plans against the worst outcomes, or the worst probability distributions, within a plausible range around the evidence. Often two-stage: commit stock first, adjust dispatch after the event.
- **Answers:** "How do we prepare when we can't forecast the event and getting it wrong costs lives?"
- **Use when:** the downside is catastrophic and there is little reliable history.
- **Avoid when:** errors are cheap and correctable (exploration is fine), or plentiful data supports an ordinary forecast. Robust plans cost more, by design.

#### Class 5: Strategic Matching Markets

*Stable matching.* Pairs two sides that both have preferences, such as students and schools or apprentices and employers, using a mechanism such as deferred acceptance (Gale–Shapley). The result is *stable*: no pair would both rather be matched with each other than with what they received. When the right side proposes, that side can rank its choices honestly without risk.
- **Answers:** "How do we place people when both sides choose, so placements stick and nobody gains by gaming the system?"
- **Use when:** both sides hold preferences or can refuse, and central assignment has led to refusals, dropouts or strategic ranking.
- **Avoid when:** the planner legitimately assigns centrally and recipients don't choose (see Class 2).

## 2. The NGO decision tree

Filter the field reality through these questions, in order, to isolate the model class.

**Q1. Is the asset capital or a nudge?**
A permanent physical or financial transfer (funds, a well, a building) points to [**Static Convex Welfare (Class 2)**](#class-2-static-demographic-targeting). A recurring, probabilistic behavioral routine (remedial hours, wellness check-ins, reminder calls) points to [**Dynamic RMABs (Class 1)**](#class-1-dynamic-state-evolution).

**Q2. Do recipients (and providers) hold preferences the planner must respect?**
If both sides choose — students and schools, donors and hospitals, volunteers and shifts — and a central assignment would be refused, gamed, or illegitimate, use [**Strategic Matching Markets (Class 5)**](#class-5-strategic-matching-markets).

**Q3. Is the environment cooperative, passive, or adversarial?**
If the target environment does not react defensively, a passive Markov model handles it. If the target actively evades your resource (poachers, illegal loggers, adapting disease vectors), overlay [**Game-Theoretic Spatiotemporal Search (Class 3)**](#class-3-spatiotemporal-security--adaptive-search).

**Q4. What is the penalty for being wrong?**
If a wrong allocation means a classroom stays flat for a week, you can afford to explore (Class 1). If it means a displaced community goes without food during a flood because blankets went to the wrong valley, use [**Distributionally Robust Optimization (Class 4)**](#class-4-robust-contingency-planning) to protect against worst-case data and shocks. Class 4 is often a layer on top of Class 2 or 3 rather than a replacement.

**Q5. Can the field produce the data the model needs?**
Class 1 needs repeated observations of each recipient (weekly or better). Class 3 needs incident or patrol logs with locations. Class 2 can run from a one-off census or survey. If data cannot be collected at the needed rate, choose a simpler class or no optimization at all, and say so.

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
- Prendergast, C. (2022). *The Allocation of Food to Food Banks.* Journal of Political Economy. — Feeding America's "Choice System" auction.

### Unverified claims (do not cite without confirmation)

The original draft of this taxonomy included the examples below. They could not be confirmed against a primary source. The assistant must not present them as documented facts; if mentioned at all, label them *"(unverified — please confirm before citing)"*.

- **Mantra4Change** using RMABs to rotate physical student toolkits across school sections.
- **"Prof. Roshni Sahu / Data Science for Social Good"** and ILP-targeted cash transfers for extreme poverty. No such researcher could be confirmed; the Data Science for Social Good fellowship is real, but this attribution is not.
- **UN-OCHA** running DRO for monsoon pre-positioning. Humanitarian pre-positioning is well studied (see Class 4 above), but an OCHA DRO deployment is not confirmed.
- **"Prof. Lily Xu / Harvard Center for Health"** as the lead on tuberculosis adherence calls. Lily Xu is a co-author on related restless-bandit work, but she is best known for PAWS and green-security patrol planning. The TB and maternal-health RMAB deployments are led by Aditya Mate, Jackson Killian, and colleagues in Milind Tambe's Teamcore group.
- **Deceased-donor organ allocation** as stable matching. National organ registries generally allocate deceased-donor organs by priority rules, not a two-sided stable match. Kidney *paired exchange* is the matching-market example.
