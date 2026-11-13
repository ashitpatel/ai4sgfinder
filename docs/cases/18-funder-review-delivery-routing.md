# Case 18: Funder review of a delivery-routing proposal

| | |
|---|---|
| **Domain** | Food assistance |
| **Who is using the assistant** | A foundation program officer reviewing a proposal |
| **Expected verdict** | **Fits**: the decision is [Class 9: Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics), and so is the method |
| **Most likely confusion** | Marking it "heavier than needed" because a free route planner exists, or letting a cited example stand for a different problem |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal) |

## Scenario

A family foundation that funds food security has a one-year proposal from a regional food bank. The food bank's three refrigerated trucks deliver to 62 partner pantries each week, on routes the drivers have planned by habit for years. It wants funding to plan routes with an open-source vehicle-routing tool.

*This is an illustrative scenario, not a real program or proposal.*

## What the funder pastes

**The proposal, summarized.**
> We will use Google OR-Tools to plan weekly routes for our three trucks across 62 pantries, respecting each pantry's two-hour receiving window and truck capacity. We have two years of GPS logs and delivery records. A volunteer analyst from a local university will set it up; our logistics coordinator will run it each week. Optimization cut the World Food Programme's costs by 12%. Budget: US$40,000 for one year. Success measures: miles driven and on-time deliveries.

**The funder's answers.**
> We fund food banks and pantries in one state. Grants are US$10,000–75,000 for a year. We're comfortable funding operational improvements, but we want a clear measure of savings.

## Why the verdict is Fits

- **Filter 1:** the resource is moved by vehicle to many sites, which points to the *space and risk* family; the narrowing answer is moving goods to many places, so Class 9.
- **Filter 3:** no one avoids the trucks.
- **Filter 4:** a bad route wastes fuel and time; it doesn't endanger lives. There are two years of records.
- **Filter 5:** GPS logs, a coordinator who would run the tool, and drivers who need a route sheet.

The proposed method is vehicle routing with time windows and capacities, which is the standard Class 9 tool, and the data it needs exists ([taxonomy, Data each class needs](../../prompt/knowledge/taxonomy.md#data-each-class-needs)). It isn't heavier than needed: OR-Tools *is* the free route planner the simpler option names, and 62 stops with time windows is beyond comfortable hand planning.

## What a good memo contains

1. **The decision:** each week, which pantries each of three trucks visits, in what order.
2. **Method fit:** *Fits.* Vehicle routing with capacities and time windows matches the decision, and the GPS logs supply locations and travel times.
3. **The simpler option:** Clarke–Wright savings by hand, or the free planner itself ([taxonomy Section 4](../../prompt/knowledge/taxonomy.md#4-simpler-alternatives-for-each-class)). In the routing tutorial's illustrative data, most of the saving came from replacing habit with *any* systematic method. Ask the food bank to report the saving against current routes, not just against hand planning.
4. **Questions for the NGO:**
   - Will you replan last quarter's deliveries and compare miles and on-time rate with what actually happened, before changing anything?
   - How will drivers check and correct the routes? Their knowledge of loading docks and road closures matters.
   - Who runs the tool if the volunteer analyst leaves?
   - How will the travel-time table be kept current?
5. **Risks to people:** few. Check that pantries serving remote areas don't end up with the worst delivery windows.
6. **Evidence check:** WFP's Optimus cut costs by 12% in Iraq (Peters et al., 2021) is *verified*, but it plans food baskets, sourcing and delivery together. It supports optimization in food assistance generally, not this saving for truck routing.
7. **Funding stages:**
   1. Replan last quarter's deliveries (a few weeks of the analyst's time). Release the rest if the saving in miles covers the year's cost.
   2. Run the new routes in one month of real deliveries, keeping the old routes as a fallback.
   3. Continue with the coordinator running it weekly. An evaluation is not needed: the replay and the month's mileage measure the result directly.

## What the assistant should not do

- Call it "heavier than needed" because a free tool exists: the free tool is what is proposed.
- Let the WFP figure stand as a forecast of this project's saving.
- Suggest an evaluator such as J-PAL; this is an operational improvement measured directly.
- Judge the food bank's capacity or say whether to fund it.
