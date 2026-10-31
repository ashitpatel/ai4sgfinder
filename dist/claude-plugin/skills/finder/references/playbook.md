# AI4SG Implementation Playbook

What to do after an approach has been chosen. The AI4SG Finder assistant uses this file for its six follow-ups; people can also read it directly.

Tools, organizations and links were last checked on **2026-10-30**. Services change: confirm that a tool or partner is still active before relying on it.

**For the assistant.** Offer the follow-ups after the recommendation and deliver one per turn, on request. Fill every template from the user's own interview answers, quoting their numbers and wording. Where an answer is missing, say what you need instead of guessing. Recommend only tools, partners and readings listed here, or ones you are certain exist; anything else must be labeled *"(unverified — please confirm)"*.

---

## Follow-up 1: Fit the model to your program

Translate the chosen class into the user's terms. Fill each row from the named filter, and flag any row the user hasn't answered.

The filters: **Filter 1** The resource and its intent · **Filter 2** Choice and preferences · **Filter 3** Environment dynamics · **Filter 4** Tolerance for being wrong · **Filter 5** Field data and workflow friction.

### Class 1 — Dynamic State Evolution (restless bandits)

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

### Class 2 — Static Demographic Targeting (welfare optimization)

| Element | Meaning | Comes from |
|---|---|---|
| Decision | What is being chosen (which sites, which households, how much each region gets) | Filter 1 |
| Candidates | The full list of options, with the data known about each | Filters 1 and 5 |
| Objective | What is maximized (people covered, welfare gain, need met) | Filter 1 |
| Budget and capacity limits | Total budget, number of units, per-site capacity | Filter 1 |
| Fairness rule | e.g. every district reaches at least X%, or maximize the worst-off group (maximin / leximin) | Filters 2 and 4 |
| Hard constraints | Legal, technical or political rules (drillable sites only, one per village) | Filter 4 |
| Audit output | What must be published to justify the choice | Filter 4 |

### Class 3 — Spatiotemporal Security & Adaptive Search (security games)

| Element | Meaning | Comes from |
|---|---|---|
| Targets | The grid cells, zones or sites to protect | Filter 3 |
| Defender resources | Patrol units and how many targets each can cover per period | Filter 1 |
| Adversary model | Who evades you, what they gain at each target, how quickly they adapt | Filter 3 |
| Risk model inputs | Past incidents, patrol effort, terrain, access points | Filter 5 |
| Detection bias | Where incidents are only recorded because you patrolled there | Filter 5 |
| Schedule format | How the randomized plan reaches staff (weekly paper calendar) | Filter 5 |
| Operational limits | Fuel, distance, weather, safety | Filter 4 |

### Class 4 — Robust Contingency Planning (robust optimization)

| Element | Meaning | Comes from |
|---|---|---|
| First-stage decision | What must be committed before the event (stock levels, locations) | Filter 1 |
| Second-stage decision | What can be adjusted after the event (dispatch, reallocation) | Filter 1 |
| Uncertainty | What is unknown (where it hits, how severe, which roads fail) | Filters 3 and 4 |
| Scenarios or uncertainty set | The historical events plus plausible unseen ones | Filter 4 |
| Robustness level | How far from history to protect (larger is safer but costlier) | Filter 4 |
| Cost of excess | Spoilage, storage and capital cost of over-preparing | Filter 4 |
| Offline outputs | Dispatch cards usable without connectivity | Filter 5 |

### Class 5 — Strategic Matching Markets (stable matching)

| Element | Meaning | Comes from |
|---|---|---|
| Two sides | Who is matched to whom (students and schools, youth and employers) | Filter 2 |
| Capacities | Places each provider offers | Filter 1 |
| Preferences | How each side ranks the other: ranked lists, scores, or priority rules | Filter 2 |
| Proposing side | Which side proposes in deferred acceptance; that side can rank honestly without risk | Filter 2 |
| Tie-breaking | Lottery or rule for equal priorities | Filters 2 and 4 |
| Special constraints | Couples, siblings, quotas, accessibility needs | Filter 4 |
| Rules to publish | Plain-language explanation that honest ranking is safe | Filter 4 |

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

**Class-specific**
- *Class 1 (restless bandits):* At least several months of per-person history at the planned round length; states recorded the same way by all staff; agreement on a minimum-contact rule.
- *Class 2 (welfare optimization):* Reliable location and population data; the fairness rule agreed by stakeholders **before** results are seen; backup options if a chosen site proves infeasible.
- *Class 3 (security games):* Patrol logs with location and effort, not just incidents; leadership accepts randomized schedules; sensitive schedules kept confidential.
- *Class 4 (robust optimization):* A scenario set reviewed by local experts, including events worse than any on record; funders accept that robust plans carry extra stock.
- *Class 5 (stable matching):* Both sides willing to submit rankings; a commitment not to override results by hand; legal review if placements involve public entitlements.

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
| 1 — Dynamic State Evolution | Randomly split beneficiaries (or field areas) between the model's list and the current method; compare outcomes such as engagement or adherence | 6–12 rounds (e.g. weeks) |
| 2 — Static Demographic Targeting | Usually a one-off decision, so compare plans rather than run a trial: model plan vs. current ranking on the same budget, scored on coverage and fairness, reviewed by stakeholders | 1–2 months of analysis |
| 3 — Spatiotemporal Security | Alternate model-generated and usual schedules by period or zone; compare detections per patrol hour, while noting that deterrence shows up as fewer detections over time | One season or 3+ months |
| 4 — Robust Contingency Planning | Backtest: replay past events and expert-designed "unseen" scenarios against the model's plan and the current plan; run a tabletop exercise with the dispatch cards | Before the risk season |
| 5 — Strategic Matching Markets | Run the match in shadow alongside the current process for one cohort, then compare refusals, early dropouts and satisfaction | One placement cycle |

---

## Follow-up 4: Build options — tools and partners

Be honest about maturity: Classes 2, 4 and 5 can be built with mature, free, general-purpose tools; Classes 1 and 3 have only research code, so they need a technical partner. Match the option to the user's staff skills from Filter 5.

### Software by class

| Class | Tools (all free and open source) | Maturity | Skills needed |
|---|---|---|---|
| 1 — Dynamic State Evolution | No ready-made package. Research code: [lily-x/online-rmab](https://github.com/lily-x/online-rmab) (Whittle-index planning, synthetic data only) | Research code | Python and a data scientist familiar with reinforcement learning or operations research |
| 2 — Static Demographic Targeting | [PuLP](https://coin-or.github.io/pulp/), [Pyomo](https://www.pyomo.org) or [Google OR-Tools](https://developers.google.com/optimization) to write the model; [HiGHS](https://highs.dev) as a free solver | Mature | Python and basic integer programming; a small model can be handed over as a script |
| 3 — Spatiotemporal Security | [PAWS-public](https://github.com/lily-x/PAWS-public) (poaching risk prediction and patrol planning, research code); [SMART](https://smartconservationtools.org) for recording patrols and incidents | Research code (model); mature (data collection) | Data scientist plus GIS skills; SMART needs only field training |
| 4 — Robust Contingency Planning | [RSOME](https://xiongpengnus.github.io/rsome/) (robust and distributionally robust models in Python); [CVXPY](https://www.cvxpy.org) or Pyomo for stochastic versions; HiGHS as solver | Mature libraries, specialist modeling | Operations-research skills; this is the hardest class to model well |
| 5 — Strategic Matching Markets | [matching](https://github.com/daffidwilde/matching) (Python: stable marriage, hospital–resident, student allocation); [matchingMarkets](https://cran.r-project.org/package=matchingMarkets) (R) | Mature algorithm; small libraries | Spreadsheet-level data prep; deferred acceptance can also be run by a short script |
| No model | A spreadsheet and a written rule | — | None |

Notes: the `matching` Python library's last release was in 2023 and RSOME's in 2024; both work, but check for updates. The research repositories above come from published papers and are not supported products.

### Partners who help nonprofits

| Partner | What they offer | Cost to the NGO | How to start |
|---|---|---|---|
| [INFORMS Pro Bono Analytics](https://connect.informs.org/probonoanalytics/nonprofits) | Volunteer operations-research and analytics experts, the best fit for optimization (Classes 2, 4, 5) | Free; the NGO commits staff time | Submit the project form on their site |
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
| 1 — Dynamic State Evolution | Google Research blog on ARMMAN: [Using ML to boost engagement with a maternal and child health program](https://research.google/blog/using-ml-to-boost-engagement-with-a-maternal-and-child-health-program-in-india/) | Mate et al. (2022), AAAI field study; Mate et al. (2020), *Collapsing Bandits*, NeurIPS |
| 2 — Static Demographic Targeting | Bradley, Hax, Magnanti, *Applied Mathematical Programming* — free from MIT at [web.mit.edu/15.053/www](https://web.mit.edu/15.053/www/) (integer programming chapters) | Church & ReVelle (1974) on covering location; Flanigan et al. (2021), Nature, on leximin fairness |
| 3 — Spatiotemporal Security | Fang, Stone, Tambe (2015), *When Security Games Go Green*, IJCAI — [free PDF](https://www.ijcai.org/proceedings/2015/0367.pdf) | Tambe (2011), *Security and Game Theory: Algorithms, Deployed Systems, Lessons Learned*, Cambridge University Press |
| 4 — Robust Contingency Planning | Rawls & Turnquist (2010) on pre-positioning emergency supplies | Rahimian & Mehrotra (2022), *Frameworks and Results in Distributionally Robust Optimization*, Open Journal of Mathematical Optimization — [open access](https://doi.org/10.5802/ojmo.15) |
| 5 — Strategic Matching Markets | Roth (2015), *Who Gets What — and Why*, a book for general readers | Abdulkadiroğlu, Pathak & Roth (2005) on the New York City high-school match |

### Research groups active in this area

Researchers rarely take on projects from cold emails, but a well-written brief that matches their published work is the best way in.

- **Teamcore and the Center for Research on Computation and Society, Harvard** — [Milind Tambe](https://teamcore.seas.harvard.edu): restless bandits for public health (Class 1) and security games (Class 3).
- **[Fei Fang](https://feifang.info), Carnegie Mellon University** — green security games and anti-poaching (Class 3), and food rescue logistics.
- **[Lily Xu](https://lily-x.github.io), Columbia University** — conservation and public-health planning under uncertainty (Classes 1, 3 and 4); author of the PAWS and restless-bandit research code above.
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
