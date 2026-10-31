# Case 4: Pre-positioning relief supplies before cyclone season

| | |
|---|---|
| **Domain** | Humanitarian response and disaster preparedness |
| **Intervention type** | Contingency stockpiling |
| **Expected class** | 4 — Robust Contingency Planning (DRO), layered over a location model |
| **Most likely confusion** | Planning for the "average" storm from historical data |

## Scenario

A humanitarian NGO serves a low-lying coastal delta. Before each cyclone season it must decide how many family kits (water purification tablets, tarpaulins, dry food for 5 days) to store in each of 6 warehouses. After landfall, roads flood and some warehouses can be cut off for days.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> 30,000 family kits to pre-position across 6 warehouses before the season. Once a storm hits, we can move kits from warehouses to affected areas, but only over whatever roads still work. Handing over a kit meets the immediate need directly.

**Filter 2 — Choice and preferences.**
> We decide the stock levels and the dispatch, coordinating with the district disaster office.

**Filter 3 — Environment dynamics.**
> Nature isn't trying to evade us, but it's very unpredictable. Each storm hits a different part of the coast.

**Filter 4 — Tolerance for being wrong.**
> Zero tolerance in practice. If kits are in the wrong warehouse and the bridge is out, families go without clean water for days and children get sick. We have detailed records for only 8 severe cyclones in the last 25 years.

**Filter 5 — Field data and workflow friction.**
> Planning happens once a year, before the season. During a response our staff often have no connectivity at all. Logistics uses Excel.

## Why Class 4: Robust Contingency Planning

The assistant should select **Class 4 (Robust Contingency Planning)**, solved with distributionally robust optimization layered over a location model from Class 2 (Static Demographic Targeting).

- **Catastrophic downside** and **almost no history** (Filter 4 — Tolerance for being wrong) are the two triggers for Class 4 (Robust Contingency Planning). Eight storms are far too few to estimate a reliable probability distribution of landfall and damage.
- The underlying decision is a **one-off central allocation of supplies to locations** (Filter 1 — The resource and its intent; Filter 2 — Choice and preferences), which is Class 2 (Static Demographic Targeting) in structure; Class 4 (Robust Contingency Planning) is the robustness layer on top of it.
- No adversary (Filter 3 — Environment dynamics), no drifting recipients, and no two-sided preferences, so Class 1 (Dynamic State Evolution), Class 3 (Spatiotemporal Security & Adaptive Search) and Class 5 (Strategic Matching Markets) don't apply.

## What a good recommendation contains

**1. Class.** A two-stage distributionally robust optimization. Stage 1 (before the season) chooses stock per warehouse; stage 2 (after landfall) ships kits over the surviving roads. Instead of trusting the 8 historical storms as *the* distribution, the model protects against the worst distribution within a plausible neighborhood of them (for example a Wasserstein ball).

**2. Counterfactual warning.** Optimizing for the average of past storms produces a plan for a storm that never happens: stock is centralized where the "average" landfall would be, and the first storm that hits an end of the coast finds the nearest warehouse empty or cut off. A forecasting model trained on 8 events would overfit badly and give false confidence.

**3. Field pathway.** The model runs once a year, centrally. Its outputs are (a) a stock table per warehouse and (b) a laminated **dispatch card** for each warehouse manager, prepared in advance for every landfall zone: "If landfall is in Zone C and Bridge 2 is out, send 4,000 kits to Shelters 7–12 by Road B." The card works with no connectivity.

**4. Evidence.** Rawls & Turnquist (2010) formulated hurricane pre-positioning as a two-stage stochastic program with uncertain demand and damaged transport links; it is the structural template here. Delage & Ye (2010) and Mohajerin Esfahani & Kuhn (2018) provide the distributionally robust machinery for when the scenario probabilities themselves can't be trusted, as with 8 storms.

**5. Report card.**
- *Successes:* in published modeling studies, stochastic and robust plans hold up better than average-case plans on adverse scenarios; that is what they are designed to do.
- *Challenges:* building credible road-failure scenarios needs local engineers; robust plans hold more stock, and donors may question "excess" inventory.
- *Unknowns:* how large the uncertainty set should be. Too small and it isn't robust; too large and the plan is wastefully conservative. Note that much of this evidence is from modeling studies; flag that operational deployments by NGOs are less documented.

**Next steps.** Compile the 8 storm footprints and the road network with known failure points; workshop extra "plausible but unseen" landfall scenarios with the district disaster office; draft dispatch cards for the current stock layout as an immediate improvement.

## What the assistant should *not* do

- Name a specific humanitarian agency as running DRO operationally unless it is sure; this is an area where real deployments are thinner than the modeling literature.
- Recommend learning by trial and error, as it might for Case 1.
