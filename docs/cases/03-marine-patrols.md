# Case 3: Patrolling a marine protected area against illegal fishing

| | |
|---|---|
| **Domain** | Conservation and natural-resource protection |
| **Intervention type** | Mobile enforcement patrols |
| **Expected class** | [Class 3: Spatiotemporal Security & Adaptive Search (security games)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) |
| **Most likely confusion** | A hotspot map of past arrests |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/03-security-games-marine-patrols.md) |

## Scenario

A coastal conservation trust co-manages a marine protected area divided into 40 zones. It has 2 patrol boats, each able to cover about 3 zones per day. Illegal net fishing inside no-take zones is rising, and fishers clearly watch where the boats go.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> Our resource is boat patrol time: 2 boats, roughly 6 zone-visits a day. We want to deter illegal fishing in the no-take zones. Patrols are re-routed every day. Whether a patrol "works" depends on whether fishers are there and whether the threat of a patrol keeps them away. Of your options, (d) fits best: we're looking for illegal nets and boats that are hidden from us, though the boats do move around a lot.

**Filter 2 — Choice and preferences.**
> We decide the routes. Nobody else has a say, though the fishing community obviously cares.

**Filter 3 — Environment dynamics.**
> Yes, very much. Fishers watch the jetty. When we patrolled the northern reef every morning for a month, catches there dropped and the nets moved south. They adapt within days.

**Filter 4 — Tolerance for being wrong.**
> A bad week means more fish taken, not loss of life. We can experiment. We have 3 years of patrol logs with GPS tracks and about 400 recorded incidents (nets found, boats intercepted). We've never run a trial.

**Filter 5 — Field data and workflow friction.**
> Rangers log patrols and incidents on a handheld in SMART (the Spatial Monitoring and Reporting Tool); the data is uploaded monthly. Boat captains get a paper schedule on Mondays. Probably whoever handles the SMART uploads would run the tool, but nobody has been given that job yet.

**Narrowing question — Space, movement and risk.** *"What is the hardest part: outwitting people who avoid you, preparing for a rare disaster, moving goods to many places, or finding hidden problems?"*
> Outwitting the fishers. Finding nets is the job, but the hard part is that they move as soon as they see a pattern.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> No. We know roughly which zones matter; the question is how to patrol them.

## Why Class 3: Spatiotemporal Security & Adaptive Search

The assistant should select **[Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search)**, solved with a Stackelberg security game.

- **Patrols that search for something hidden** (Filter 1 — The resource and its intent) place the problem in the *Space, movement and risk* family. Decisively, there is **an adversary who adapts to your moves** (Filter 3 — Environment dynamics), and the narrowing answer confirms that outwitting them is the hard part. This is the defining signature of Class 3: Spatiotemporal Security & Adaptive Search.
- Not [Class 12: Risk-Based Inspection](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), its closest neighbor. Class 12 also sends limited checks to where problems are likely, but it assumes the hidden problem stays put. Here the fishers move when they see a pattern, so a ranked list of high-risk zones becomes predictable and is avoided. The risk model inside Class 3 plays the same role as a Class 12 model, inside a randomized plan.
- Not [Class 8: Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) or [Class 9: Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics): Class 8 learns which options pay off when nobody is evading you, and Class 9 minimizes travel cost, which isn't the problem here.
- Central routing (Filter 2 — Choice and preferences) rules out [Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) and [Class 6: Participatory Allocation](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation); exploration is tolerable (Filter 4 — Tolerance for being wrong), so a [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) layer isn't required.
- Not [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution): the "state" that matters is the fishers' strategic response to your pattern, not a recipient's independent drift.

## What a good recommendation contains

**1. Class.** A Stackelberg security game. The trust commits to a *randomized* patrol strategy (a probability of covering each zone), and fishers are modeled as observing those probabilities and responding. Combine it with a predictive model of where illegal fishing is likely given past patrol effort, as in PAWS.

**2. Counterfactual warning.** A hotspot map built from past arrests sends boats where they already patrol; fishers displace, and the data then "confirms" the old hotspots because arrests only happen where boats go (detection bias). A predictable rotation is worse: fishers learn it. Deterministic optimization of any kind is exploitable.

**3. Field pathway.** Each month, an analyst fits the model to the SMART export and computes zone coverage probabilities. A simple generator (a spreadsheet with random draws) turns those into a weekly paper calendar: "Boat A, Monday: zones 4, 11, 12." Captains see only the calendar. Keep the probabilities confidential; publish only that patrols are risk-based and randomized.

**4. Evidence.** PAWS was developed for wildlife protection and field-tested in Uganda and Cambodia (Fang et al., IAAI 2016; Xu et al., ICDE 2020). PROTECT is a game-theoretic patrol system deployed by the US Coast Guard for port and maritime security (Shieh et al., AAMAS 2012); its maritime setting maps directly onto boat patrols. ARMOR (Pita et al., AAMAS 2008) is the original deployed Stackelberg system, at LAX checkpoints.

**5. Report card.**
- *Successes:* field tests of PAWS reported finding more snares and signs of illegal activity in the areas the model prioritized than in comparison areas.
- *Challenges:* ranger and captain compliance with a randomized schedule ("why are we going to zone 12 again?"); fuel and weather constraints the model must include.
- *Unknowns:* how rational the fishers really are, and how badly detection bias distorts the risk model. Build in some patrols to low-information zones to keep learning.

**6. Simpler alternative.** Two, close in different ways. (a) A **weighted lottery**: each morning draw zones from a bag of slips, with each zone's slips in proportion to its estimated value; never a weekly rotation. (b) **Goal Seek**: the equilibrium has a closed form for a simple game, so one spreadsheet column (coverage = (value − U) ÷ (value + penalty), floored at 0 and capped at 1) and Excel's Goal Seek on U reproduce the game's plan. In the [tutorial](../tutorials/03-security-games-marine-patrols.md#the-simpler-alternative-goal-seek-in-a-spreadsheet) the lottery cut fish taken by about two-thirds as much as the game, and Goal Seek matched it exactly (illustrative data). Check before settling for Goal Seek: the trust's loss is the fishers' gain (catch value, not reef damage that differs by zone), one penalty applies everywhere, and any set of zones can be patrolled on a day. Once boats must follow connected routes, use the LP. Both still need zone values corrected for where the boats went; a simple rule fed hotspot counts fails the same way the hotspot plan did.

**Next steps.** Export the 3 years of SMART data and tabulate effort and incidents by zone and month; brief captains on why randomization matters; run the generated calendar for one quarter alongside the existing plan.

## What the assistant should *not* do

- Recommend "predictive policing"-style hotspot targeting alone.
- Ignore the fishing community: note that enforcement works best alongside community engagement and livelihood alternatives.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 2** in full, because this program's biggest risks are in its data and its people, not its math.

### Follow-up 2: Readiness checks

A good answer goes through the playbook checklist using this program's answers, marks each item, and says what to do:

| Check | Status | Why, and what to do |
|---|---|---|
| Decision owner | Partly ready | Captains get a schedule each Monday, but nobody is named as owning it. Name the person who signs off the weekly plan and handles captains' questions. |
| Patrol data | Ready | 3 years of SMART logs with GPS tracks and about 400 incidents (Filter 5 — Field data and workflow friction) is a strong base. |
| Detection bias | Not ready | Incidents were only recorded where boats went. Feed patrol *effort* into the risk model, and reserve some patrols for rarely visited zones so the data stops confirming old hotspots. |
| Randomized schedules accepted | Not ready | Captains will ask why they're sent to zone 12 again. Brief them on why predictability failed on the northern reef (Filter 3 — Environment dynamics) before the pilot starts. |
| Schedule confidentiality | Not ready | Fishers watch the jetty, so a weekly paper calendar that circulates can leak. Give each captain only that day's zones, on the day. |
| Privacy | Partly ready | Incident records may name fishers or boats. Keep identities out of the model; it needs locations and times only. |
| Do-no-harm and community voice | Partly ready | The trust co-manages the area with the community. Check that enforcement doesn't fall mainly on one community's fishing grounds, and discuss the approach with the fishing committees. |
| Maintenance | Partly ready | SMART data arrives monthly. Decide who refits the model each month and who covers when they're away. |
| Exit plan | Ready | The current schedule remains the fallback. |

Fix the three "not ready" items before the pilot; the "partly ready" items can be resolved during it.

### The other follow-ups, in brief

- **1. Fit the model:** targets = the 40 zones; defender = 2 boats covering about 3 zones each per day; adversary = net fishers who shift within days; inputs = SMART patrol tracks and incidents; limits = fuel, distance and weather.
- **3. Pilot design:** alternate model-generated and usual schedules by fortnight for one season; compare nets found per patrol hour, remembering that deterrence eventually shows up as *fewer* finds.
- **4. Build options:** the risk model and planner exist only as research code ([PAWS-public](https://github.com/lily-x/PAWS-public)), so this needs a data scientist with GIS skills; SMART, already in use, stays the data system.
- **5. Reading and contacts:** Fang, Stone and Tambe (2015), *When Security Games Go Green*, covers illegal fishing directly. Fei Fang (Carnegie Mellon) and Lily Xu (Columbia) work on green security.
- **6. Brief for a technical partner:** lead with the 3 years of SMART data and the displacement seen on the northern reef.
