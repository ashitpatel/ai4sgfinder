# Case 10: Routing weekly food deliveries to distribution points

| | |
|---|---|
| **Domain** | Food security |
| **Intervention type** | Recurring in-kind delivery by truck |
| **Expected class** | [9 — Routing & Logistics (vehicle routing with capacities and time windows)](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics) |
| **Most likely confusion** | [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting), deciding *who* gets food rather than how it travels; or [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning), treating rainy-season road closures as the main risk |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/10-vehicle-routing-food-delivery.md) |

## Scenario

A regional food-assistance NGO delivers food every week to 140 distribution points (church halls, schools, community centers) from 3 warehouses, using 12 trucks. Each point is run by volunteers who open at set hours on a set day. Today each warehouse serves a fixed list of points inherited from years ago, and dispatchers build routes by hand in Excel. Trucks sometimes arrive after volunteers have gone home, and fuel is the second-largest cost after the food itself.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> We deliver food to 140 distribution points from 3 warehouses each week, using 12 trucks. We want everyone served on time at the lowest fuel cost. Of your options, it's (c): moved by vehicle to many sites. Who receives food at each point is already decided by the points themselves.

**Filter 2 — Choice and preferences.**
> We plan it centrally. The dispatchers decide which truck goes where; the points just tell us their opening hours.

**Filter 3 — Environment dynamics.**
> No one avoids us. Some roads close in the rainy season, mostly the same river crossings and dirt roads every year, for anything from a day to a few weeks.

**Filter 4 — Tolerance for being wrong.**
> A late delivery is serious, since families wait and sometimes go home without food, but it's recoverable within a day: we send a truck the next morning. We have two years of delivery records: date, truck, points visited, quantities, and the times drivers wrote down.

**Filter 5 — Field data and workflow friction.**
> Drivers have phones with GPS, though signal drops on the rural routes. Dispatchers use Excel. One of our two dispatchers is good with spreadsheets and would run the tool each week.

**Narrowing — Space, movement and risk.** The assistant asks: "What is the hardest part: outwitting people who avoid you, preparing for a rare disaster, moving goods to many places, or finding hidden problems?"
> Moving goods to many places. Getting 12 trucks to 140 points in their opening hours without burning fuel on long, overlapping routes.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> No. Which points get food and how much is decided by the food bank network; we just deliver.

## Why Class 9: Routing & Logistics

The assistant should select **[Class 9 (Routing & Logistics)](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics)**, solved as a capacitated vehicle routing problem with time windows, plus an assignment of distribution points to warehouses.

- **Moved by vehicle to many sites** (Filter 1 — The resource and its intent, option (c)) places the problem in the *Space, movement and risk* family. **Central planning** (Filter 2 — Choice and preferences) keeps it there and rules out [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) and [Class 6 (Participatory Allocation)](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation).
- **The narrowing answer**, "moving goods to many places," picks Class 9 (Routing & Logistics) within the family: the cost and delay are in the movement itself (fuel, trucks, travel time), across many sites with capacities and opening hours.
- **No one avoids them** (Filter 3 — Environment dynamics), so [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) doesn't apply. Road closures are a constraint on the network, not an adversary.
- **A late delivery is recoverable within a day** and there are two years of records (Filter 4 — Tolerance for being wrong), so the harm is not catastrophic and history is plentiful. That rules out [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) as the primary class. It becomes a layer only if closures turn out to be unpredictable *and* severe, for example a bridge out for weeks with no warning.
- **The question is how food travels, not who receives it** (Filter 1): recipients are chosen at the points. That rules out [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting).
- **GPS phones and two years of records** (Filter 5 — Field data and workflow friction) can supply what Class 9 needs: locations, travel times and quantities.

## What a good recommendation contains

**1. Class.** A capacitated vehicle routing problem with time windows: each truck has a load limit and a working day, each point has a demand and an opening window, and the model chooses which truck serves which points and in what order to minimize distance (fuel) while meeting every window. Underneath it, a warehouse-to-site assignment decides which of the 3 warehouses serves each point, instead of keeping the inherited lists. Rainy-season closures are handled as a second road network: the model is solved once for dry-season roads and once for wet-season roads, with alternative routes ready for the known closures.

**2. Counterfactual warning.** Hand-built routes in Excel drift toward habit: fixed warehouse lists, overlapping routes, and trucks that cross each other's paths. A machine-learning model that predicts delivery times does not fix this; it forecasts lateness on the same bad routes. Planning for dry-season roads only means the first heavy rain sends drivers improvising detours and missing windows, and that is when families go home empty-handed.

**3. Field pathway.** The dispatcher who is good with spreadsheets reruns the model weekly from an Excel sheet of demands and opening hours. Drivers get a printed **route sheet** per day: stop order, address, opening window, quantity, and a "wet-season alternative" line for any leg that crosses a known closure. The sheet works offline, since signal drops on rural routes. Drivers' phone GPS logs are collected each week to correct the travel times the model uses.

**4. Evidence.** WFP's Optimus model (Peters et al., 2021, INFORMS Journal on Optimization) plans food sourcing, delivery routes and the ration itself; in Iraq it cut costs by 12% at the same nutritional value, and WFP reports using it in 44 operations. It is a supply-chain network model rather than truck-by-truck routing, so it is a parallel at a larger scale, not the same tool. The 2021 Franz Edelman Award paper (Peters et al., 2022) describes WFP's analytics more broadly; its savings figure covers that work as a whole, not Optimus alone. The closest routing parallel is from another domain: Bertsimas, Delarue & Martin (2019, PNAS) routed Boston Public Schools' buses, saving about US$5 million a year and 50 buses, with stops, vehicle capacities and arrival windows that map directly onto distribution points, trucks and opening hours.

**5. Report card.**
- *Successes:* both deployments above reported large cost savings from routing and network models used in real operations.
- *Challenges:* route models are only as good as their travel times and locations; drivers know shortcuts and hazards the map doesn't, and will ignore sheets they don't trust. In Boston, the proposed school start-time changes were approved but not implemented after community opposition, though the bus routing went ahead: changing people's schedules is much harder than changing routes.
- *Unknowns:* how accurate the handwritten times in two years of records are; how predictable the rainy-season closures really are; whether points can widen their opening windows. Flag that documented food-NGO routing deployments are thinner than the operations-research literature.

**6. Simpler alternative.** The recommended method is already a rule of thumb, so the simpler options are about who runs it. A dispatcher can compute the Clarke–Wright savings table for one warehouse-day in a spreadsheet and join the largest savings first while the truck has room and the windows hold; or a volunteer can set up a free route planner (VROOM or OR-Tools) once. In the [tutorial](../tutorials/10-vehicle-routing-food-delivery.md#the-simpler-alternative-the-savings-method-by-hand-or-a-free-planner) the savings plan was 0–2.3% longer than the exact optimum, and most of the saving came from replacing habit with any systematic method (illustrative data). Check before doing it by hand: few, wide opening windows; one truck type; time for an hour or two per warehouse-day. What no shortcut replaces is the travel-time table from the GPS logs.

**Next steps.** Geocode all 140 points and check them with drivers; build a travel-time table from the GPS logs rather than the handwritten times; replan one past month of deliveries with the model and compare distance and on-time rate with what actually happened.

## What the assistant should *not* do

- Recommend Class 2 (Static Demographic Targeting) or a need-ranking model because the program is about food; the user asked how to deliver, not whom to serve.
- Make Class 4 (Robust Contingency Planning) the primary class because of the rainy season. Closures that recur on the same roads are a second network, not a rare disaster.
- Promise a fuel saving for this NGO, or present the Optimus or Boston figures as what it will achieve.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

A good answer maps every element of the routing model to this program, citing the interview answer it came from:

| Element | For this program | From |
|---|---|---|
| Network | 3 warehouses, 140 distribution points, and the roads between them, in a dry-season and a wet-season version | Filters 1 and 3 |
| Demand | Food quantity per point per week, and each point's opening window | Filters 1 and 2 |
| Fleet and capacity | 12 trucks, each with a load limit and a driver's working day; stock and loading bays at each warehouse | Filter 1 |
| Costs | Fuel per kilometre first, then driver hours | Filter 1 |
| Decisions | Which warehouse serves each point; which truck visits which points, and in what order | Filter 1 |
| Hard rules | Arrive within each opening window; avoid closed roads in the wet-season network | Filters 3 and 4 |
| Output format | A printed daily route sheet per truck, with wet-season alternatives, usable offline | Filter 5 |

It should also flag the gap that matters most: **travel times.** The handwritten times in the delivery records are likely rounded or filled in afterwards. The drivers' GPS logs give real travel times by road and season; start collecting them weekly now. Until then, use map distances and check the first route sheets with drivers before trusting them.

### Follow-up 6: One-page brief for a technical partner

If the user picks **6**, a good answer fills the playbook template from the interview:

```
PROJECT BRIEF — Regional food-assistance deliveries (illustrative)

The decision we need help with
  Each week, plan routes for 12 trucks delivering food from 3 warehouses
  to 140 distribution points, including which warehouse serves which point.

Why it matters
  Families wait at the points; when a truck misses the opening hours,
  some go home without food. Fuel is our second-largest cost.

Current approach
  Fixed warehouse lists inherited from years ago; dispatchers build routes
  by hand in Excel. Routes overlap and miss windows, worse in the rains.

Recommended approach
  Class 9 (Routing & Logistics): a vehicle routing model with truck
  capacities and opening-hour time windows, plus warehouse-to-point
  assignment, solved for dry-season and wet-season road networks.

Simpler option to beat
  The savings method run by the dispatcher in a spreadsheet, or a free route
  planner. Exact optimization adds a few percent at most.

Data we have
  Two years of delivery records (date, truck, points, quantities,
  handwritten times). Drivers' phones log GPS. Point addresses in Excel.

Constraints
  12 trucks; drivers' working hours; points' opening windows; recurring
  rainy-season road closures. Weak signal on rural routes.

What success looks like
  Lower fuel use and a higher share of deliveries inside opening hours.
  Harm measure: deliveries missed or moved to the next day.

How results must reach staff
  A printed route sheet per truck per day. One dispatcher reruns the
  model weekly from an Excel sheet.

What we are asking for
  Help building the model and a one-month trial of its routes from one
  warehouse, after replanning a past month to compare.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** accurate coordinates for all 140 points; travel times from GPS rather than handwritten logs; current fuel costs; drivers and warehouse staff involved in checking the first plans; a named dispatcher to rerun it each week.
- **3. Pilot design:** replan last quarter's deliveries with the model and compare distance and on-time rate with what happened; then run the model's routes from one warehouse for a month, with the other two as comparison. Harm measure: missed or next-day deliveries.
- **4. Build options:** [Google OR-Tools routing](https://developers.google.com/optimization/routing) handles capacities and time windows; [VROOM](https://github.com/VROOM-Project/vroom) is a fast alternative; PuLP or Pyomo with the free HiGHS solver for the warehouse assignment. An analyst comfortable with Python can build it; INFORMS Pro Bono Analytics is the best-fit partner. Confirm each tool or partner is still active before relying on it.
- **5. Reading and contacts:** start with the WFP Optimus project page and the OR-Tools routing guide, then Peters et al. (2021) and Bertsimas, Delarue & Martin (2019). Karen Smilowitz (Northwestern) studies food-bank distribution and nonprofit logistics; the Zero Hunger Lab at Tilburg University worked with WFP on Optimus.
