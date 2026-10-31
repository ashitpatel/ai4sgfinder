# Case 3: Patrolling a marine protected area against illegal fishing

| | |
|---|---|
| **Domain** | Conservation and natural-resource protection |
| **Intervention type** | Mobile enforcement patrols |
| **Expected class** | [3 — Spatiotemporal Security & Adaptive Search (security games)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) |
| **Most likely confusion** | A hotspot map of past arrests |

## Scenario

A coastal conservation trust co-manages a marine protected area divided into 40 zones. It has 2 patrol boats, each able to cover about 3 zones per day. Illegal net fishing inside no-take zones is rising, and fishers clearly watch where the boats go.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> Our resource is boat patrol time: 2 boats, roughly 6 zone-visits a day. We want to deter illegal fishing in the no-take zones. Patrols are re-routed every day. Whether a patrol "works" depends on whether fishers are there and whether the threat of a patrol keeps them away.

**Filter 2 — Choice and preferences.**
> We decide the routes. Nobody else has a say, though the fishing community obviously cares.

**Filter 3 — Environment dynamics.**
> Adversarial. Fishers watch the jetty. When we patrolled the northern reef every morning for a month, catches there dropped and the nets moved south. They adapt within days.

**Filter 4 — Tolerance for being wrong.**
> A bad week means more fish taken, not loss of life. We can experiment. We have 3 years of patrol logs with GPS tracks and about 400 recorded incidents (nets found, boats intercepted).

**Filter 5 — Field data and workflow friction.**
> Rangers log patrols and incidents on a handheld in SMART (the Spatial Monitoring and Reporting Tool); the data is uploaded monthly. Boat captains get a paper schedule on Mondays.

## Why Class 3: Spatiotemporal Security & Adaptive Search

The assistant should select **[Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search)**, solved with a Stackelberg security game.

- **Mobile assets over geography** (Filter 1 — The resource and its intent) and, decisively, **an adversary who adapts to your moves** (Filter 3 — Environment dynamics). This is the defining signature of Class 3 (Spatiotemporal Security & Adaptive Search).
- Central routing (Filter 2 — Choice and preferences) rules out [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets); exploration is tolerable (Filter 4 — Tolerance for being wrong), so a [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) layer isn't required.
- Not [Class 1 (Dynamic State Evolution)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution): the "state" that matters is the fishers' strategic response to your pattern, not a recipient's independent drift.

## What a good recommendation contains

**1. Class.** A Stackelberg security game. The trust commits to a *randomized* patrol strategy (a probability of covering each zone), and fishers are modeled as observing those probabilities and responding. Combine it with a predictive model of where illegal fishing is likely given past patrol effort, as in PAWS.

**2. Counterfactual warning.** A hotspot map built from past arrests sends boats where they already patrol; fishers displace, and the data then "confirms" the old hotspots because arrests only happen where boats go (detection bias). A predictable rotation is worse: fishers learn it. Deterministic optimization of any kind is exploitable.

**3. Field pathway.** Each month, an analyst fits the model to the SMART export and computes zone coverage probabilities. A simple generator (a spreadsheet with random draws) turns those into a weekly paper calendar: "Boat A, Monday: zones 4, 11, 12." Captains see only the calendar. Keep the probabilities confidential; publish only that patrols are risk-based and randomized.

**4. Evidence.** PAWS was developed for wildlife protection and field-tested in Uganda and Cambodia (Fang et al., IAAI 2016; Xu et al., ICDE 2020). PROTECT is a game-theoretic patrol system deployed by the US Coast Guard for port and maritime security (Shieh et al., AAMAS 2012); its maritime setting maps directly onto boat patrols. ARMOR (Pita et al., AAMAS 2008) is the original deployed Stackelberg system, at LAX checkpoints.

**5. Report card.**
- *Successes:* field tests of PAWS reported finding more snares and signs of illegal activity in the areas the model prioritized than in comparison areas.
- *Challenges:* ranger and captain compliance with a randomized schedule ("why are we going to zone 12 again?"); fuel and weather constraints the model must include.
- *Unknowns:* how rational the fishers really are, and how badly detection bias distorts the risk model. Build in some patrols to low-information zones to keep learning.

**Next steps.** Export the 3 years of SMART data and tabulate effort and incidents by zone and month; brief captains on why randomization matters; run the generated calendar for one quarter alongside the existing plan.

## What the assistant should *not* do

- Recommend "predictive policing"-style hotspot targeting alone.
- Ignore the fishing community: note that enforcement works best alongside community engagement and livelihood alternatives.
