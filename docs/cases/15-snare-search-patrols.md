# Case 15: Finding snares in a wildlife reserve

| | |
|---|---|
| **Domain** | Wildlife conservation |
| **Intervention type** | Ranger foot patrols that remove snares |
| **Expected class** | [12 — Risk-Based Inspection (poaching-risk prediction)](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), with a [Class 3 — Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) layer that randomizes patrols |
| **Combination** | [12 + 3: where to look, then patrol unpredictably](../../prompt/knowledge/taxonomy.md#5-when-two-classes-combine) |
| **Most likely confusion** | [Case 3](03-marine-patrols.md), where the game is primary; or a hotspot map with no randomization |
| **In-depth tutorials** | No separate tutorial. The two layers are taught in [risk-based inspection](../tutorials/13-risk-based-inspection-lead-pipes.md) (ranking hidden problems, with a random share) and [security games](../tutorials/03-security-games-marine-patrols.md) (correcting patrol logs for effort, and randomized plans) |

## Scenario

A conservation trust co-manages a 1,200 km² savanna reserve with the wildlife authority. Wire snares set for bushmeat kill and maim elephants, giraffes and antelope; a snare is hidden in grass and found only by a ranger who walks close to it. Eight ranger teams can each walk about 15 km a day, covering a small fraction of the reserve each month. The rangers have four years of patrol logs in SMART, the free patrol-monitoring tool used in many protected areas: GPS tracks and every snare found. The trust has noticed that snares turn up wherever patrols *aren't* that week, and that local poachers seem to know the teams' usual routes.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> Ranger patrol days, about 8 teams a day. The goal is to find and remove snares before animals are caught, and to make setting snares not worth it.

*Next turn, which fits best:*
> (d), used to look for something hidden. Snares are invisible until you're on top of them.

**Filter 2 — Choice and preferences.**
> We decide, with the park warden. Rangers follow the plan, though team leaders pick the exact path.

**Filter 3 — Environment dynamics.**
> Yes. Poachers watch where the rangers' vehicles go and set snares where we haven't been lately. Some of them live in villages next to the ranger posts.

**Filter 4 — Tolerance for being wrong.**
> A missed snare can kill an elephant, but no single patrol day is catastrophic; we can adjust month to month.

*Next turn, what records:*
> Four years of SMART patrol tracks and snare finds, about 9,000 patrol days. Most patrols stayed near roads and posts.

**Filter 5 — Field data and workflow friction.**
> Rangers record on SMART phones every patrol, uploaded at the post each evening. The trust has one GIS officer.

*Next turn, who would run it:*
> The GIS officer, monthly. A university group has offered help for a year.

**Narrowing question — Space, movement and risk.** *"What is the hardest part: outwitting people who avoid you, preparing for a rare disaster, moving goods to many places, or finding hidden problems?"*
> Finding the snares. We only find what we walk past, and we walk past the same places. But the poachers also move when they see a pattern.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> Two, really: where snares are likely to be, and how to send patrols so the poachers can't read our routine.

## Why Class 12 with a Class 3 layer

The assistant should select **[Class 12 (Risk-Based Inspection)](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection)** as the primary class, a poaching-risk model that corrects for where rangers walked, with **[Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search)** as the layer that turns the risk map into randomized patrol plans.

- **Patrols are used to find something hidden** (Filter 1 d, narrowing): the *Space, movement and risk* family, and the user names finding as the hardest part. That is Class 12.
- **The records are badly selective** (Filter 4): four years of patrols mostly near roads. A raw "snares found per cell" map shows where rangers went, not where snares are. Correcting for patrol effort and imperfect detection is the core of the problem, as it was in the PAWS work.
- **Poachers adapt** (Filter 3): the reason for the Class 3 layer. Sending every team to the top-risk cells each month would be a predictable hotspot plan, and poachers would move, which is what the trust already sees.
- **Why not Class 3 primary, as in [Case 3](03-marine-patrols.md)?** There, the zones' values were roughly known and the hard part was the strategic response. Here, the risk itself is unknown and hidden, and the data to estimate it are biased. The order of work follows: the prediction comes first, and the game uses it.
- **Not [Class 8 (Learn-While-Allocating)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating)** alone: learning which areas pay off is part of the design (keep exploring under-patrolled cells), but an adaptive bandit ignores that the poachers respond.

## What a good recommendation contains

**1. Class.** A poaching-risk model per 1 km² cell and month, fitted to the SMART logs with patrol effort as an input, so cells walked rarely aren't mistaken for safe ones (the PAWS approach from Milind Tambe's group). Then a randomized plan: each cell gets a probability of being patrolled, higher where risk is higher but never certain or zero, drawn fresh each day. Keep a share of patrols in rarely visited cells so the model learns where it is blind.

**2. Counterfactual warning.** A hotspot map from raw finds sends rangers back where they already go, finds there go up, and the map "confirms" itself while snares spread to the cells nobody walks. A fixed weekly schedule, however well chosen, hands poachers the pattern. And a black-box risk score that rangers don't trust will be quietly ignored.

**3. Field pathway.** Each evening the GIS officer prints, for each post, tomorrow's assigned cells for each team: a map sheet with three to five cells circled, drawn from the month's probabilities. Team leaders choose their own path inside the circled cells and record as usual in SMART. Monthly, the officer refits the model with the new tracks and finds and recomputes the probabilities. Only the day's cells are issued, on the day.

**4. Evidence.** PAWS was field-tested in Queen Elizabeth National Park, Uganda, where rangers patrolled cells the model rated high and low risk and found more signs of poaching in the high-risk ones (Gholami et al., ECML PKDD 2017). Later work combined prediction with patrol planning that accounts for the model's uncertainty, with field tests in Murchison Falls (Uganda) and Srepok (Cambodia) (Xu et al., ICDE 2020). The randomized-schedule idea comes from deployed security games such as ARMOR and PROTECT. These are field tests, not years of routine use; say so.

**5. Report card.**
- *Successes:* field tests found more snares where the model pointed, in two countries.
- *Challenges:* rangers' trust in assigned cells; GPS gaps; a model that needs refitting monthly by one GIS officer; vehicle access limiting which cells are reachable.
- *Unknowns:* how much snaring moves in response to patrols in this reserve; whether finds rise or fall as deterrence works (fewer snares to find is success, but looks like failure on a "finds" chart).

**6. Simpler alternative.** Each layer has one.
- *Risk map:* a spreadsheet of snares found **per patrol-kilometer** in each cell over four years, with cells walked less than a few kilometers marked "unknown" rather than "safe", then each unknown cell scored by its neighbors and by rangers' knowledge in a workshop. This keeps the most important idea, correcting for effort, without a model. It falls short on imperfect detection (thick grass hides snares even on patrolled cells), on seasonality and on learning month to month. Check: how many cells are "unknown"? If most of the reserve is, the model's effect correction and exploration share matter more.
- *Patrol plan:* a weighted lottery, slips in a bag with each cell's share proportional to its risk score, drawn each morning; in the [marine-patrol tutorial](../tutorials/03-security-games-marine-patrols.md#the-simpler-alternative-goal-seek-in-a-spreadsheet) this gave about two-thirds of the game's effect, and Goal Seek on the equilibrium formula gave all of it when the game was simple. Check: whether teams can patrol any combination of cells (if posts and roads constrain them, plan whole routes).
- Together, an effort-corrected spreadsheet map and a weighted lottery capture the two essential ideas and are a defensible first year while the university partner builds the model.

**Next steps.** Export four years of SMART tracks and finds and compute patrol-kilometers and finds per cell; hold a workshop with team leaders to score cells the logs barely cover; agree with the warden that daily cells will be drawn at random from the plan and issued only on the day.

## What the assistant should *not* do

- Recommend a hotspot map of raw snare finds, or any fixed schedule.
- Treat the problem as a pure security game ([Class 3](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search)) with risk values taken from raw finds.
- Describe the field tests as routine deployments, or promise a number of snares found.
- Measure success by snares found alone; add animals found snared and, where possible, snaring signs on random checks.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 3** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

| Element | For this program | From |
|---|---|---|
| Unit | 1 km² cells, by month | Filter 1 |
| Outcome | Snares found per cell-visit, with patrol kilometers in the cell as effort | Filter 4 |
| Risk inputs | Distance to villages, roads, water and boundary; habitat; season; past finds | Filter 4; Filter 5 |
| Bias correction | Effort as an input, and a share of patrols in cells rarely visited | Filter 4 |
| Patrol capacity | 8 teams × about 15 km a day, from fixed posts | Filter 1 |
| Randomization (layer) | Each cell's daily probability from the risk map, never 0 or 1; drawn each morning | Filter 3 |
| Reachability | Cells each post can reach in a day on foot or by vehicle | Filter 1 |
| Secrecy | Only the day's cells issued, on the day | Filter 3 |
| Refit | Monthly by the GIS officer, with the university group's script | Filter 5 |

Gap to flag: **"no snares found" in the logs mixes "no snares" with "didn't look hard".** Ask team leaders to record when a cell was searched thoroughly versus passed through, so the model can tell them apart.

### Follow-up 3: Pilot design

The layers are piloted in order, because the patrol plan is only as good as the map:

1. **Months 1–3, test the map.** Each week, send some teams to cells the map rates high and some to cells it rates low but that are similar in access, choosing which cells by lottery. Compare snares found per patrol-kilometer. This is the design of the Uganda field test, and it shows whether the map beats rangers' current choices before anything else changes.
2. **Months 4–9, test the randomization.** Alternate posts, month by month, between the model's randomized plan and the usual routes. Compare snares found per patrol-kilometer and, on a small number of random check walks, snares present. Expect finds to rise at first and then fall if deterrence works; the random checks are what show the difference.
3. **Harm measure:** cells left unpatrolled for more than two months, and ranger safety incidents in newly assigned remote cells.

### The other follow-ups, in brief

- **2. Readiness checks:** SMART tracks complete and uploaded daily; the warden's approval for randomized, day-of assignments; a safety review for remote cells; the GIS officer's time protected for the monthly refit.
- **4. Build options:** SMART for data; Python or R with the university group for the risk model; PuLP if the patrol plan needs an LP over routes. PAWS research code may help a technical partner. Confirm each tool and partner is still active before relying on it.
- **5. Reading and contacts:** Gholami et al. (2017) and Xu et al. (2020); Fang et al. (2016) on deploying PAWS. Milind Tambe's group (Harvard Teamcore) and Lily Xu's group work on green-security planning.
- **6. Brief:** the decision is where to look; the layer is how to patrol unpredictably; under "Simpler option to beat", the effort-corrected spreadsheet map and the weighted lottery.
