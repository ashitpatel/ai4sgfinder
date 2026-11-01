# Case 4: Pre-positioning relief supplies before cyclone season

| | |
|---|---|
| **Domain** | Humanitarian response and disaster preparedness |
| **Intervention type** | Contingency stockpiling |
| **Expected class** | [Class 4: Robust Contingency Planning (DRO), layered over a location model](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) |
| **Most likely confusion** | Planning for the "average" storm from historical data |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/04-robust-optimization-cyclone-prepositioning.md) |

## Scenario

A humanitarian NGO serves a low-lying coastal delta. Before each cyclone season it must decide how many family kits (water purification tablets, tarpaulins, dry food for 5 days) to store in each of 6 warehouses. After landfall, roads flood and some warehouses can be cut off for days.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> 30,000 family kits to pre-position across 6 warehouses before the season. Once a storm hits, we can move kits from warehouses to affected areas, but only over whatever roads still work. Handing over a kit meets the immediate need directly. Of your options, it's (c): goods moved by truck to many sites.

**Filter 2 — Choice and preferences.**
> We decide the stock levels and the dispatch, coordinating with the district disaster office.

**Filter 3 — Environment dynamics.**
> No one. Nature isn't trying to evade us, but it's very unpredictable. Each storm hits a different part of the coast.

**Filter 4 — Tolerance for being wrong.**
> Zero tolerance in practice. If kits are in the wrong warehouse and the bridge is out, families go without clean water for days and children get sick. We have detailed records for only 8 severe cyclones in the last 25 years, and there's no way to run a trial.

**Filter 5 — Field data and workflow friction.**
> Planning happens once a year, before the season. During a response our staff often have no connectivity at all. Logistics uses Excel, and our logistics team would run the tool.

**Narrowing question — Space, movement and risk.** *"What is the hardest part: outwitting people who avoid you, preparing for a rare disaster, moving goods to many places, or finding hidden problems?"*
> Preparing for the storm. Trucking kits out is something we know how to do; the problem is that we don't know where the next one will hit or which roads will survive.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> Getting kits from the warehouses to shelters after landfall, but that's part of the same plan.

## Why Class 4: Robust Contingency Planning

The assistant should select **[Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning)**, solved with distributionally robust optimization layered over a location model from [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting).

- **Goods moved by vehicle to many sites** (Filter 1 — The resource and its intent) place the problem in the *Space, movement and risk* family, and the narrowing answer, **preparing for a rare disaster**, picks Class 4 within it.
- **Catastrophic downside** and **almost no history** (Filter 4 — Tolerance for being wrong) are the two triggers for Class 4: Robust Contingency Planning. Eight storms are far too few to estimate a reliable probability distribution of landfall and damage.
- The underlying decision is a **one-off central allocation of supplies to locations** (Filter 1 — The resource and its intent; Filter 2 — Choice and preferences), which is Class 2: Static Demographic Targeting in structure; Class 4: Robust Contingency Planning is the robustness layer on top of it.
- No adversary (Filter 3 — Environment dynamics), no drifting recipients, and no two-sided preferences, so [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution), [Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) and [Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) don't apply.
- Not [Class 9: Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics), its closest neighbor. Class 9 minimizes the cost of moving goods over a known network. Here the hard part is not route efficiency but not knowing where the storm will land or which roads will survive. The stage-2 dispatch is a small routing problem inside the robust plan, not the main decision.
- Not an *anticipatory action* trigger on its own. Within Class 4, a trigger agrees in advance to release money or supplies when a forecast crosses a threshold. That suits cases where forecasts give a few days' warning and the action is fixed. It could later sit alongside this plan, for example to move stock forward when a storm is forecast, but it doesn't decide how much to hold in each warehouse before the season.
- **The second decision is part of the same model** (second-decision question). Moving kits after landfall is the plan's second stage, the dispatch cards, not a separate [Class 9 (Routing & Logistics)](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics) layer. Routing would become a layer only if the organization also ran the trucks' multi-stop routes after a storm.

## What a good recommendation contains

**1. Class.** A two-stage distributionally robust optimization. Stage 1 (before the season) chooses stock per warehouse; stage 2 (after landfall) ships kits over the surviving roads. Instead of trusting the 8 historical storms as *the* distribution, the model protects against the worst distribution within a plausible neighborhood of them (for example a Wasserstein ball).

**2. Counterfactual warning.** Optimizing for the average of past storms produces a plan for a storm that never happens: stock is centralized where the "average" landfall would be, and the first storm that hits an end of the coast finds the nearest warehouse empty or cut off. A forecasting model trained on 8 events would overfit badly and give false confidence.

**3. Field pathway.** The model runs once a year, centrally. Its outputs are (a) a stock table per warehouse and (b) a laminated **dispatch card** for each warehouse manager, prepared in advance for every landfall zone: "If landfall is in Zone C and Bridge 2 is out, send 4,000 kits to Shelters 7–12 by Road B." The card works with no connectivity.

**4. Evidence.** Rawls & Turnquist (2010) formulated hurricane pre-positioning as a two-stage stochastic program with uncertain demand and damaged transport links; it is the structural template here. Delage & Ye (2010) and Mohajerin Esfahani & Kuhn (2018) provide the distributionally robust machinery for when the scenario probabilities themselves can't be trusted, as with 8 storms.

**5. Report card.**
- *Successes:* in published modeling studies, stochastic and robust plans hold up better than average-case plans on adverse scenarios; that is what they are designed to do.
- *Challenges:* building credible road-failure scenarios needs local engineers; robust plans hold more stock, and donors may question "excess" inventory.
- *Unknowns:* how large the uncertainty set should be. Too small and it isn't robust; too large and the plan is wastefully conservative. Note that much of this evidence is from modeling studies; flag that operational deployments by NGOs are less documented.

**6. Simpler alternative.** An equal split: the same number of kits in each warehouse, or in proportion to the people each warehouse can reach. In the [tutorial](../tutorials/04-robust-optimization-cyclone-prepositioning.md#the-simpler-alternative-an-equal-split) an equal split matched or beat the robust plans on the worst stress scenarios, because it leans on no single road or warehouse, while reaching about 6 points fewer families than the DRO plan in an average recorded storm and doing worse at the ends of the coast (illustrative data). It is close on robustness; it gives up average performance, dispatch cards and the price of robustness for funders. Check before settling for it: the districts are similar in population and exposure; eight storms are too few to trust; every warehouse can store and protect the stock. A sensible first season is an equal or population-proportional split, with dispatch cards drawn up for it, while the model is built.

**Next steps.** Compile the 8 storm footprints and the road network with known failure points; workshop extra "plausible but unseen" landfall scenarios with the district disaster office; draft dispatch cards for the current stock layout as an immediate improvement.

## What the assistant should *not* do

- Name a specific humanitarian agency as running DRO operationally unless it is sure; this is an area where real deployments are thinner than the modeling literature.
- Recommend learning by trial and error, as it might for Case 1.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 3** in full, because a live trial is impossible here and the assistant has to explain how to test the plan anyway.

### Follow-up 3: Pilot design

A good answer starts by saying why the usual pilot doesn't work: you can't wait for, or schedule, a cyclone, and testing a plan in a real storm is exactly the risk you're trying to avoid (Filter 4 — Tolerance for being wrong). Instead, it tests the plan three ways before the season, each comparing the model's stock layout against the current one:

1. **Replay the 8 recorded cyclones.** For each storm, using its known landfall and road damage, compute how many families each plan could reach with a kit within 2 days.
2. **Stress-test with storms that haven't happened.** In a workshop, the district disaster office and local engineers design about 10 plausible scenarios that are worse than the record: landfall at each end of the coast, two bridges out at once, a stronger storm than any on file. Keep these out of the model's inputs so they are a fair test.
3. **Run a tabletop exercise.** Warehouse managers respond to a simulated landfall with the dispatch cards and no phones (Filter 5 — Field data and workflow friction). Measure time to first dispatch and the number of wrong shipments.

**Success measure:** the share of affected families reached with a kit within 2 days, in the *worst* scenario and on average.
**Harm measure:** the cost of extra stock and the number of kits that would expire unused.
**Decision rule, set in advance:** adopt the model's plan if it improves worst-case reach and the extra stock fits the budget. Move part of the stock first if funders are cautious; the change is reversible between seasons.

### The other follow-ups, in brief

- **1. Fit the model:** first stage = how many of the 30,000 kits go to each of the 6 warehouses; second stage = dispatch over the roads that survive; uncertainty = landfall, severity and road failures; scenarios = the 8 storms plus the workshop set; robustness level = chosen with funders, since more protection costs more stock.
- **2. Readiness checks:** a road map with known failure points, reviewed by local engineers; funders' agreement that robust plans hold extra stock; a named owner for the dispatch cards.
- **4. Build options:** [RSOME](https://xiongpengnus.github.io/rsome/) or Pyomo with the free HiGHS solver; this is the hardest class to model well, so look for an operations-research specialist, for example through INFORMS Pro Bono Analytics.
- **5. Reading and contacts:** Rawls & Turnquist (2010) on hurricane pre-positioning first, then Rahimian & Mehrotra's open-access review of distributionally robust optimization.
- **6. Brief for a technical partner:** stress the 8-storm history and the no-connectivity constraint; both shape the model.
