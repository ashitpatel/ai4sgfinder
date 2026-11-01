# Vehicle Routing Masterclass: Getting 12 Trucks to 140 Food Points on Time

*An in-depth walkthrough of travel-time estimation, warehouse assignment and vehicle routing with capacities and time windows, built on [Case 10: Routing weekly food deliveries to distribution points](../cases/10-food-delivery-routing.md).*

**You need:** proportions, medians, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class 9: Routing & Logistics](../../prompt/knowledge/taxonomy.md#class-9-routing--logistics). **Code:** [`code/case10_vehicle_routing.py`](code/case10_vehicle_routing.py). Every number in this tutorial comes from running that file. The region, roads, opening hours and GPS logs in it are made up for teaching; all results are illustrative.

---

## Executive Overview

A regional food-assistance NGO delivers food **every week to 140 distribution points** (church halls, schools, community centers) from **3 warehouses**, using **12 trucks**. Volunteers open each point at set hours on a set day. Each warehouse serves a fixed list of points inherited from years ago, and two dispatchers build routes by hand in Excel. Trucks sometimes arrive after the volunteers have gone home, and fuel is the second-largest cost after the food itself.

The usual answer is to keep the lists and polish the spreadsheet. It fails in two ways. The inherited lists send trucks past a nearer warehouse to reach "their" points, so routes from different warehouses overlap. And a route built by hand follows habit, often the order of the list or of opening hours, so trucks zigzag across the district. A model that predicts which deliveries will be late doesn't help either: it forecasts lateness on the same bad routes.

This tutorial builds the alternative step by step:

1. **[The Routing Leap](#the-routing-leap--from-fixed-lists-to-a-vehicle-routing-model)** writes the weekly plan as a *vehicle routing problem*: trucks with load limits, points with opening windows, and a goal of fewest kilometres.
2. **[The Core Bottleneck](#the-core-bottleneck--too-many-routes-to-check)** shows why this is hard: the number of possible routes explodes, so no one can list them all.
3. **[From GPS Logs to Estimates](#from-gps-logs-to-estimates--the-travel-time-table)** turns two years of driver records into a table of travel times, with honest margins of error, and shows why the handwritten times are the weak link.
4. **[The Decision Engine](#the-decision-engine--an-exact-model-then-savings)** solves a 7-stop example exactly with PuLP, checks it against every possible plan, and then introduces the **Clarke–Wright savings** method that scales.
5. **[Scaling Up](#scaling-up--140-points-3-warehouses-two-seasons)** assigns the 140 points to warehouses, routes the full week, plans a second road network for the rainy season, and prints offline route sheets.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** runs it all and compares it with the current fixed routes.
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **choose every truck's stops and their order together, using measured travel times, so that the plan is short *and* keeps every opening window.**

---

## The Routing Leap – From Fixed Lists to a Vehicle Routing Model

### Why a list of points is the wrong shape

A dispatcher's spreadsheet treats each warehouse's list as fixed and each truck's route as a sequence typed in by hand. Two things are missing. First, the cost of a stop depends on its neighbors in the route: a point 3 km from the previous stop is cheap, the same point 40 km away is not. Second, the routes compete for the same trucks and the same hours: putting one more stop on truck 1 might make it late for the next point, or free up truck 2 for the day. A model that looks at all stops, all trucks and all windows at once can weigh these; a list can't.

### The vehicle routing problem

The **vehicle routing problem** (VRP) is the standard model for this. It always has the three parts of any optimization model:

1. **Decisions:** for every pair of places $i$ and $j$, does some truck drive straight from $i$ to $j$? Write $x_{ij} = 1$ for yes and $x_{ij} = 0$ for no. A variable that can only be 0 or 1 is called **binary**. Together these yes/no choices spell out every truck's route.
2. **Objective:** the single number to make as small as possible. Here, total kilometres, because fuel is paid by the kilometre: $\sum_{i,j} d_{ij}\, x_{ij}$, where $d_{ij}$ is the road distance.
3. **Constraints:** the rules every acceptable plan must obey.

The version with load limits is called **capacitated**, and the version with opening hours has **time windows**, so the full name is the *capacitated vehicle routing problem with time windows* (CVRPTW). Its rules, in words:

- **Every point is visited exactly once:** one truck arrives, the same truck leaves.
- **No more trucks than you have:** at most 4 routes leave each warehouse on a day (12 trucks, 4 per warehouse).
- **Load limit:** the food on one truck adds up to at most its capacity, $Q$ (6,000 kg in the code).
- **Opening window:** a truck reaching point $j$ must arrive no later than its closing time $l_j$. If it arrives before opening time $e_j$, it waits.
- **Working day:** every truck is back at the warehouse by 18:00.

The time rule is where the arithmetic lives. If a truck goes from $i$ to $j$, it arrives at $j$ after starting service at $i$ (on arrival, or at opening time if it had to wait), unloading for $s_i$ minutes, and driving $t_{ij}$ minutes:

$$
a_j \ \ge\ \max(a_i,\ e_i) + s_i + t_{ij} \quad \text{if } x_{ij} = 1, \qquad a_j \le l_j .
$$

Here $a_j$ is the arrival time. The load rule works the same way: the load delivered by the time the truck leaves $j$ is at least the load delivered when it left $i$, plus $j$'s demand $q_j$. Carrying time and load forward along each route has a useful side effect: it rules out a "route" that loops between points without ever leaving the warehouse, because time can't go round in a circle.

### Two decisions, not one

Underneath the routing sits a simpler question: **which warehouse serves each point?** The case asks for this explicitly instead of keeping the inherited lists. It is an **assignment model**: one yes/no choice per point and warehouse, each point assigned to exactly one warehouse, within each warehouse's stock and truck capacity, at the lowest total distance. [Scaling Up](#scaling-up--140-points-3-warehouses-two-seasons) solves it first, then routes each warehouse's points.

### Mapping it to the program

| Model term | In this program |
|---|---|
| Depot | Each of the 3 warehouses |
| Stops | The 140 distribution points, each open on one day a week |
| Demand $q_j$ | Kilograms of food per point per week, from the delivery records |
| Time window $[e_j, l_j]$ | The hours the volunteers are there (2 to 3 hours in the code) |
| Capacity $Q$ and fleet | 12 trucks, 4 per warehouse, each with a load limit and a working day |
| Travel distances and times $d_{ij}$, $t_{ij}$ | Road km from a map; minutes from the drivers' GPS logs ([From GPS Logs to Estimates](#from-gps-logs-to-estimates--the-travel-time-table)) |
| Objective | Total km per week, which sets the fuel bill |
| Second network | Wet-season road distances, with the known closures |
| Output | A printed route sheet per truck per day, usable offline |

The model is solved **every week**, from the dispatcher's Excel sheet of demands and opening hours. Nothing in it is uncertain in the way a cyclone is: roads, points and windows are mostly known in advance. That is what makes it Class 9 rather than the robust planning of [Class 4](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning).

---

## The Core Bottleneck – Too Many Routes to Check

### The number of routes explodes

For a single truck visiting $n$ points, the number of possible orders is $n!$ ("$n$ factorial": $n \times (n-1) \times \dots \times 1$). It grows absurdly fast. From the code:

| Stops | Orders for one truck |
|---|---|
| 7 | $7! = 5{,}040$, about $10^{3.7}$ |
| 10 | about $10^{6.6}$ |
| 28 (one day's points) | about $10^{29.5}$ |
| 140 (the whole week) | about $10^{241.1}$ |

And that's one truck. With several trucks you must also choose who gets which stops. Even the 7-stop example of [The Decision Engine](#the-decision-engine--an-exact-model-then-savings), with just 2 trucks, has 20,160 different plans. No computer can list the options for a full week, and no clever trick is known that solves every large routing problem quickly. Mathematicians call problems like this **NP-hard**.

### Three ways out

- **Exact methods** use the same branch-and-bound search a solver uses for any integer program: solve an easier version with fractional choices, split on a fractional variable, and discard any branch that can't beat the best plan found so far. They **prove** the answer is the best, but the time they need can grow very quickly with the number of stops.
- **Heuristics** are rules of thumb that build a good plan fast, with no proof that it is the best. Clarke–Wright savings and "nearest neighbor" are two classics.
- **Improvement moves** take any plan and repeatedly make small changes that shorten it: reverse a stretch of a route (**2-opt**), or move one stop to another truck (**relocate**).

The practical recipe, used below, is: build with a heuristic, polish with improvement moves, and **check the result against an exact solve on days small enough to solve exactly**.

### The data are the other bottleneck

A routing model is only as good as its travel times. If it thinks a leg takes 40 minutes and it takes 60, every arrival after it is late. The case is blunt about this: the handwritten times are probably rounded or filled in afterwards. That is the subject of the next section.

---

## From GPS Logs to Estimates – The Travel-Time Table

The model needs two tables: **road kilometres** between every pair of places (for fuel), and **driving minutes** (for the windows). For 3 warehouses and 140 points that's $143 \times 142 = 20{,}306$ ordered pairs.

### Step 1: Kilometres from a map

Road distances come from a map service or OpenStreetMap after geocoding each point (turning its address into GPS coordinates). They're mostly reliable, provided the coordinates are right. A point placed on the wrong side of a river is a classic error, so **check every location with the drivers** before the first plan.

### Step 2: Minutes from GPS logs, using the median

Times vary from trip to trip: traffic, weather, a herd of goats, a puncture. So a leg's travel time is an **estimate**, not a fixed number. The code simulates two years of GPS logs from the drivers' phones on the legs the current routes actually drive: 177 of the 20,306 pairs, 74 dry-season weeks each, with 25% of trips lost because signal dropped on rural roads.

For each leg, use the **median** logged time, the middle value. Unlike the average, it isn't dragged up by the occasional 45-minute hold-up. For one example leg (41.8 road km, on a dirt road):

| Trips logged | Median | Mean | 95% interval for the median | True median (known only in the simulation) |
|---|---|---|---|---|
| 54 of 74 | 82.0 min | 82.3 min | 77.1 to 85.7 min | 80.0 min |

The interval comes from the **bootstrap**: resample the 54 trips with replacement 2,000 times, take each resample's median, and keep the middle 95% of those medians. It needs no formula and works for medians, where the familiar $\bar x \pm 1.96\, s/\sqrt{n}$ does not directly apply. An interval about ±4 minutes wide on an 82-minute leg is good enough to plan with, especially with the 15-minute safety buffer the planner adds before each closing time.

### Step 3: Why not the handwritten times?

The code also simulates the drivers' handwritten records: rounded to the nearest 15 minutes, and 30% of entries are the "usual" figure written in afterwards rather than the real time. Comparing each leg's median against the truth:

| Source | Typical error per leg (median) | Legs off by more than 10 minutes |
|---|---|---|
| GPS logs | 0.6 min | 0% |
| Handwritten records | 4.8 min | 18% |

Almost one leg in five off by more than 10 minutes is enough to make a tight window look safe when it isn't. **Build the table from the GPS logs, not the handwritten times**, as the case recommends, and start collecting them weekly now. These error rates are invented for the simulation; the real ones are an [unknown the case flags](../cases/10-food-delivery-routing.md#what-a-good-recommendation-contains), and the first pilot should measure them.

### Step 4: Legs nobody has driven

The current routes cover under 1% of all pairs. A new plan will use legs no one has logged. For those, estimate minutes as map km divided by a typical speed, and estimate the speed from the logged legs, separately by road type:

| Road type | Legs logged | Median speed |
|---|---|---|
| Sealed | 117 | 44.8 km/h |
| Dirt (either end on a dirt road) | 60 | 30.0 km/h |

Across the whole table, the estimates are off from the true times by a median of **7.9%**, mostly on the unlogged legs, where real speeds vary with hills and road condition in ways a map doesn't show. That is why the plan keeps a buffer, why the first route sheets should be checked with drivers, and why the GPS logs should be **collected every week**: each new route driven fills more of the table with measured times.

---

## The Decision Engine – An Exact Model, Then Savings

### Step-by-step concrete example: 1 depot, 7 stops, 2 trucks

Here is a problem small enough to check by hand. One warehouse ("Depot"), seven points A to G, and two trucks that each carry **10 tonnes**. Trucks average 40 km/h (1.5 minutes per km), leave at 07:00, and spend 20 minutes unloading at each stop.

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Demand (tonnes) | 3 | 2 | 4 | 3 | 2 | 3 | 2 |
| km from Depot | 12.0 | 12.6 | 10.0 | 16.1 | 10.8 | 11.7 | 15.2 |

Total demand is 19 tonnes, so both trucks are needed. The program prints the full table of road km between every pair; the ones used below are A–D 8.2, A–F 11.7, B–E 10.0, B–G 10.2, C–E 12.6, C–F 12.2, D–G 10.0, A–B 20.0, B–C 20.1, D–E 24.3, E–F 21.3, F–G 24.0.

**Step A: The hand plan.** The dispatcher splits the list in alphabetical order: truck 1 takes A, B, C (9 t); truck 2 takes D, E, F, G (10 t). Both fit. Distance:

- Depot–A–B–C–Depot: $12.0 + 20.0 + 20.1 + 10.0 = 62.1$ km
- Depot–D–E–F–G–Depot: $16.1 + 24.3 + 21.3 + 24.0 + 15.2 = 100.9$ km

Total **163.0 km**. The trucks criss-cross the map.

**Step B: The exact model in PuLP.** The routing model above, with 56 yes/no leg variables, solves in under a second:

- Truck 1: Depot–B–G–D–A–Depot, $12.6 + 10.2 + 10.0 + 8.2 + 12.0 = 53.0$ km, load $2 + 2 + 3 + 3 = 10$ t
- Truck 2: Depot–F–C–E–Depot, $11.7 + 12.2 + 12.6 + 10.8 = 47.3$ km, load $3 + 4 + 2 = 9$ t

Total **100.3 km**, 38% less than the hand plan, with the same two trucks. You can check it: the program also lists all **20,160** ways to split the 7 stops into at most two ordered routes, keeps the **1,872** that respect the load limit, and confirms that none is shorter than 100.3 km.

**Step C: Add a time window.** Now suppose point G's volunteers can only be there from **07:00 to 07:30**. In the plan above, G is the second stop: the truck reaches B at about 07:19, unloads until 07:39, and reaches G at about 07:54. Too late. The only way to reach G in time is to make it the **first** stop: $15.2 \times 1.5 = 22.8$ minutes from the depot, arriving at 07:23.

Re-solving with the window, only **504** of the 20,160 plans are feasible, and the best is:

- Truck 1: Depot–F–A–D–Depot, $11.7 + 11.7 + 8.2 + 16.1 = 47.7$ km, 9 t
- Truck 2: Depot–G–B–E–C–Depot, $15.2 + 10.2 + 10.0 + 12.6 + 10.0 = 58.0$ km, 10 t

Total **105.7 km**. The window costs 5.4 km, and the routes change completely: a reminder that one point's hours affect everyone's route. This is why asking points whether they can **widen their opening windows** (one of the case's unknowns) can be worth more than any algorithm.

### Clarke–Wright savings: a heuristic you can run by hand

The exact model works for 7 stops. For a full day, use a heuristic. The best-known is **Clarke–Wright savings**, named after its two inventors. Start with the worst possible plan: one truck per point, each driving out and back. Then ask, for every pair of points $i$ and $j$: how many km would I save by serving both on one trip instead of two?

$$
s_{ij} = d_{0i} + d_{0j} - d_{ij}
$$

where $0$ is the depot. Two separate trips drive $0 \to i \to 0$ and $0 \to j \to 0$; joining them replaces the two legs back to and out of the depot ($d_{i0} + d_{0j}$) with the single leg $d_{ij}$. For D and G: $16.1 + 15.2 - 10.0 = 21.3$ km saved.

The largest savings in the toy are D–G 21.3, A–D 19.9, B–G 17.6, B–E 13.4, then A–G and A–F at 12.0. The method works down this list, joining the two routes at the ends of each pair **if the joined route still fits the truck and every window**. On the capacity-only toy, it finds Depot–A–D–G–B–Depot and Depot–E–C–F–Depot: the same two routes as the exact model, driven in the opposite direction, **100.3 km**.

### Where heuristics go wrong

With G's 07:00–07:30 window, Clarke–Wright ends with **three** routes, G–D–A (7 t), B–E (4 t) and C–F (7 t), totalling 112.7 km. Any further join breaks the 10-tonne limit, and it has only two trucks. Its early, greedy joins locked it in. The exact model found a two-truck plan at 105.7 km.

That is the honest trade-off. Heuristics are fast and usually good, but they carry no guarantee. The full-size program therefore adds the two **improvement moves** (relocate a stop to another truck, reverse a stretch of a route), **checks that no warehouse ever needs more than its 4 trucks**, and compares its plans with an exact solve on real days small enough to solve exactly.

---

## Scaling Up – 140 Points, 3 Warehouses, Two Seasons

### The illustrative region

The code builds a region that matches the case: **140 points** around ten market towns, **3 warehouses**, **12 trucks** (4 per warehouse, 6,000 kg each), and points that each open on one weekday, 28 a day. Weekly demand is 168,800 kg. A river runs through the middle, with two bridges open all year and two fords that close every rainy season; 63 points are east of it, and 32 are reached by dirt roads. W2, the eastern warehouse, is small: it can send out at most 40,000 kg a week.

### Step 1: Assign points to warehouses

The inherited lists come from history. W1 is the oldest warehouse and once served everyone; when W3 opened it took the points within 20 km of it, and small W2 took those within 17 km. The assignment model instead minimizes total out-and-back distance, subject to each warehouse's weekly stock and to its daily truck capacity (kept to 85% of 4 × 6,000 kg, for slack).

| Lists | Points per warehouse (W1, W2, W3) | Out-and-back km |
|---|---|---|
| Inherited | 85, 29, 26 | 8,194 |
| Assignment model | 62, 36, 42 | 6,713 |

**29 points change warehouse.** W2 ends at 39,950 kg, just under its 40,000 kg limit: the stock rule is what stops the model sending every eastern point there. Out-and-back distance is only a stand-in for the real route length, but it is cheap to compute and points the right way. (The model has 420 yes/no variables, more than Excel's standard Solver allows, which is why the case suggests PuLP with a free solver for this step.)

### Step 2: Route each warehouse-day

For each warehouse and weekday, the program runs Clarke–Wright savings with capacity and window checks, then the relocate and 2-opt moves, using the estimated travel-time table. It aims to arrive at least **15 minutes before closing**, a buffer against ordinary delays. The result is 15 small problems (3 warehouses × 5 days) with a median of 9 stops each and at most 16.

### Step 3: Is the heuristic close to the best?

On two of those days, the program also runs the exact PuLP model:

| Warehouse-day | Stops | Heuristic | Exact | Gap | Exact solve time |
|---|---|---|---|---|---|
| W3, Friday | 12 | 286.7 km, 3 trucks | 286.7 km, 3 trucks | 0.0% | under a second |
| W1, Thursday (busiest) | 16 | 286.3 km, 4 trucks | 279.8 km, 4 trucks | 2.3% | 14 to 21 seconds in our runs |

On a 12-stop day the heuristic found the best plan; on the busiest day it was 2.3% longer. The exact time jumped from under a second to 14–21 seconds for four more stops, which is the explosion from [The Core Bottleneck](#the-core-bottleneck--too-many-routes-to-check) in action. Production tools use stronger improvement searches to narrow gaps like this (see [Production tools](#production-tools)).

### Step 4: The rainy season is a second network, not a disaster

Filter 3 of the interview says the closures are **mostly the same river crossings and dirt roads every year**. That makes them a known, recurring change to the network, not a surprise. So the program builds a **wet-season road table**: both fords closed (crossing traffic must use a bridge), dirt roads slower (20 instead of 30 km/h), and tracks to 17 points that flood each year reached by a 12 km longer way round. It then re-solves both the assignment and the routes on that table.

| Plan, in the rainy season | km/week | Fuel/week | Truck-days | Peak trucks | On time |
|---|---|---|---|---|---|
| Dry-season plan, drivers detour as needed | 3,557 | $1,494 | 40 | 9 | 96.5% |
| Wet-season plan, re-solved | 3,593 | $1,509 | 43 | 10 | 99.2% |

Of the dry plan's 180 legs, 8 use a ford (a median of 13.5 km extra once it closes) and 32 touch a flooding track. Driving the dry plan with improvised detours keeps the km similar but misses more windows. The re-solved plan uses three more truck-days and slightly more km, chosen in advance, and gets back to 99.2% on time. In the rains, that is the trade the dispatcher wants: **spend a little more fuel to keep families from going home empty-handed.** Four points also move warehouse in the wet-season assignment.

**When Class 4 enters.** If closures turned out to be **unpredictable and severe**, say a bridge out for weeks with no warning, a single wet network would not be enough. Then a [robust planning layer](04-robust-optimization-cyclone-prepositioning.md) would help: plans that hold up across many closure scenarios, or extra stock pre-positioned east of the river. The case is clear that this is a layer to add only if the records show it is needed, not the main model.

### Step 5: Offline route sheets

Signal drops on rural routes, so the plan must work on paper. The program prints one route sheet per truck per day:

```
Truck from W1, Wed. Leave 07:00. Load 5,400 kg.
1. Point P078  open 08:00-11:00  plan 08:04  1,300 kg
2. Point P082  open 09:00-11:30  plan 08:32  700 kg
3. Point P090  open 08:00-10:00  plan 09:28  1,350 kg
4. Point P092  open 10:00-13:00  plan 09:54  1,400 kg
5. Point P019  open 10:00-12:00  plan 11:15  650 kg
Back at W1 about 11:53
WET-SEASON ALTERNATIVE P092 -> P019: fords closed, cross by bridge, +9 km
```

The truck reaches P082 at 08:32 and waits until 09:00; the plan allows for that. The last line is the case's "wet-season alternative": if a ford closes early in the week, the driver knows the detour and its cost without calling in. A real sheet would add addresses and a contact number for each point.

### Production tools

The program's heuristic is written in plain numpy so you can read every line. For real use, mature free tools do the same job better and faster: [Google OR-Tools routing](https://developers.google.com/optimization/routing) handles capacities, time windows and multiple depots, and [VROOM](https://github.com/VROOM-Project/vroom) is a fast alternative. They combine construction heuristics with stronger improvement searches. Neither is used in the tutorial's code. Confirm either is still maintained before relying on it.

### What the evidence says

Two deployments are the closest parallels. Neither is the same tool, and neither tells you what this NGO will save.

- **WFP's Optimus** (Peters et al., 2021, *INFORMS Journal on Optimization*) plans food sourcing, delivery routes and the ration itself; in Iraq it cut costs by 12% at the same nutritional value, and WFP reports using it in 44 operations. It is a **supply-chain network model**, not truck-by-truck routing: a parallel at a larger scale.
- **Boston Public Schools** (Bertsimas, Delarue & Martin, 2019, *PNAS*) used routing with stops, vehicle capacities and arrival windows, which map directly onto distribution points, trucks and opening hours. It saved about **US$5 million a year and 50 buses**. The proposed school start-time changes were approved but **not implemented** after community opposition, while the bus routing went ahead: changing routes is easier than changing people's schedules.

The case also flags that documented food-NGO routing deployments are thinner than the operations-research literature.

---

## Code Implementation & Simulation

The full program is [`code/case10_vehicle_routing.py`](code/case10_vehicle_routing.py). It needs `numpy` and PuLP 3, which includes the free CBC solver:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case10_vehicle_routing.py
```

It runs in 15 to 25 seconds, most of it the exact solve of the busiest day; only the times change between runs.

### The exact model in PuLP

```python
x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", cat="Binary")
     for i in nodes for j in nodes if i != j}
load = {i: pulp.LpVariable(f"load_{i}", demand[i], cap) for i in stops}
arr = {i: pulp.LpVariable(f"arr_{i}", DAY_START, close_[i]) for i in stops}
prob += pulp.lpSum(D[i, j] * x[i, j] for (i, j) in x)
for i in stops:
    prob += pulp.lpSum(x[i, j] for j in nodes if j != i) == 1     # leave once
    prob += pulp.lpSum(x[j, i] for j in nodes if j != i) == 1     # enter once
prob += pulp.lpSum(x[depot, j] for j in stops) <= trucks
...
            prob += load[j] >= load[i] + demand[j] - cap * (1 - x[i, j])
            # arrival at j >= (arrival at i, or opening time if later) + service + drive
            prob += arr[j] >= arr[i] + service[i] + T[i, j] - big * (1 - x[i, j])
            prob += arr[j] >= open_[i] + service[i] + T[i, j] - big * (1 - x[i, j])
```

Each line matches a rule in [The Routing Leap](#the-routing-leap--from-fixed-lists-to-a-vehicle-routing-model). The upper bound on `arr` is the closing time; the upper bound on `load` is the truck's capacity. The `big * (1 - x[i, j])` term switches a rule off when the leg $i \to j$ isn't used: subtracting a large number makes it always true.

### The savings heuristic

```python
savings = sorted(((D[depot, i] + D[depot, j] - D[i, j], i, j)
                  for i in stops for j in stops if i < j), reverse=True)
for sav, i, j in savings:
    ...
    for cand in options:
        if sum(demand[s] for s in cand) > cap:
            continue
        if schedule(cand, T, depot, open_, close_, service, buffer)[2]:
```

`options` holds the ways to join the route ending in $i$ to the route starting with $j$ (reversing one if needed). `schedule` drives the joined route minute by minute and says whether every window and the working day are kept.

### Simulation: current routes against the new plan

The **current fixed routes** follow a dispatcher's habit on the inherited lists: list the day's points by opening hour and fill one truck after another to its load limit, visiting them in that order. The **new plan** uses the assignment model and Clarke–Wright with both improvement moves. Each plan is driven over **200 simulated weeks**, where every leg's time varies randomly around its true median and has a 5% chance of a 20–60 minute hold-up. "On time" means arriving before the point closes. Fuel is costed at an illustrative US$0.42 per km (about 0.30 litres per km at US$1.40 a litre).

```
Simulation - one week of routes, evaluated over 200 weeks of random travel times (dry season)
  current fixed routes                   km/week= 5,794  fuel/week=$2,434  fuel/year=$126,544  truck-days=37  peak trucks= 8  on time=79.3%
  new lists + Clarke-Wright + 2-opt      km/week= 3,042  fuel/week=$1,277  fuel/year=$ 66,429  truck-days=40  peak trucks= 9  on time=99.7%
  warehouse-days needing more than 4 trucks (Clarke-Wright plan): 0
  Clarke-Wright vs current: km/week -2,753 (-47.5%), fuel/year -$60,115
  (Clarke-Wright on the inherited lists: km/week=3,381, on time=99.3%)
```

"Truck-days" counts one truck working one day; "peak trucks" is the most trucks out on any single day, out of 12.

### What the results say

- **Most of the saving comes from routing, not reassignment.** Routing alone, on the inherited lists, cuts the week from 5,794 to 3,381 km. The new lists cut another $3{,}381 - 3{,}042 = 339$ km a week.
- **On time rises from 79.3% to 99.7%.** The current routes never check the windows; the model plans every arrival 15 minutes before closing.
- **Keeping the windows costs trucks.** The new plan uses 40 truck-days a week instead of 37, and 9 trucks on its busiest day instead of 8. The current routes fill trucks to capacity regardless of time; the model sometimes sends a part-full truck because a fuller one would arrive late. Both stay well within the 12-truck fleet.
- **The size of the saving is not a forecast.** The 47.5% cut is against a deliberately simple "current" plan in an invented region. Real dispatchers are better than this habit rule, and real roads are messier. The case is explicit: **don't promise a fuel saving.** The way to find the real number is the case's first step: replan a past month with the model and compare it with what actually happened.

### The simpler alternative: the savings method by hand, or a free planner

In routing, the simple method and the good method are close relatives. The plan above *is* a rule of thumb: Clarke–Wright savings (Clarke and Wright, Operations Research, 1964) plus 2-opt, the method worked [by hand](#clarkewright-savings-a-heuristic-you-can-run-by-hand) for seven points. On the two warehouse-days checked against the exact model it was 0.0% and 2.3% longer. Exact optimization would add at most a few percent; the 47.5% came from replacing habit with any systematic method.

So the options, simplest first, and how close each is:

- **Savings by hand, per warehouse-day.** For a day with 10 to 15 stops, a dispatcher can compute the savings table in a spreadsheet (distance to $i$ + distance to $j$ − distance between them), join the largest savings first while the truck has room and the windows hold, then try swapping stop order. It reaches roughly what the code does, at an hour or two per warehouse-day. Check: few, wide time windows (tight windows make hand-checking slow and errors likely), and one truck type.
- **A free route planner.** VROOM or OR-Tools, set up once by a volunteer, does the same in seconds for every day, with windows and capacities. This is the realistic "simple" option for 140 points; it is software, but not a model anyone has to build or maintain.
- **Fixing assignment by map.** Sending each point to its nearest warehouse with room is a calculator job. Here it would be worth less than routing (339 of the 2,753 km saved came from new lists).

What all of them need, and what no shortcut replaces: a travel-time table drivers trust. With that in hand, the gap between a spreadsheet savings plan and an optimized one is small; without it, both promise arrivals that won't happen.

### Cautions

1. **The travel-time table is the foundation.** In the simulation, the planner's times are off by a median of 7.9% and the buffer absorbs it. With handwritten times, or wrong coordinates, the same model would promise arrivals it can't deliver. Drivers know shortcuts and hazards the map doesn't, and will ignore sheets they don't trust; check the first sheets with them.
2. **Everything here is invented.** The region, roads, windows, speeds, closures and fuel price are made up to teach the method.
3. **The model ignores some real costs:** driver overtime, loading-bay queues at the warehouse, and the cost of a next-morning redelivery. A production version would add them.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Decisions** | $x_{ij} \in \{0, 1\}$: a truck drives $i \to j$ | Spells out every truck's stops and their order |
| **Objective** | minimize $\sum_{i,j} d_{ij}\, x_{ij}$ | Total km, so total fuel |
| **Visit rule** | each point entered once and left once | Every point gets its delivery |
| **Capacity** | load on each truck $\le Q$ | No overloaded trucks (6,000 kg each in the code) |
| **Time windows** | $a_j \ge \max(a_i, e_i) + s_i + t_{ij}$, $a_j \le l_j$ | Arrive while the volunteers are there; wait if early |
| **Travel-time table** | median of GPS-logged times; map km ÷ estimated speed for unlogged legs | Measured times with bootstrap intervals, not handwritten guesses |
| **Warehouse assignment** | minimize out-and-back km within stock and truck capacity | Replaces the inherited lists (29 points move in the example) |
| **Heuristic** | Clarke–Wright savings $s_{ij} = d_{0i} + d_{0j} - d_{ij}$, then relocate and 2-opt | Plans the full week in seconds |
| **Exact check** | the same model solved by branch and bound on small days | Shows how far the heuristic is from the best (0% and 2.3% here) |
| **Wet-season network** | the same model on a second road table with known closures | Ready-made rainy-season plan and per-leg alternatives |
| **Route sheet** | stop order, window, planned arrival, kg, wet alternative | Works offline on rural routes |

### Where to go next

- **Follow the case's next steps** in its [follow-ups](../cases/10-food-delivery-routing.md#after-the-recommendation): geocode the 140 points and check them with drivers, build the travel-time table from GPS logs, and replan a past month to compare km and on-time rate with what happened. The [readiness checks](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks) and [pilot design](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design) sections of the playbook cover the Class 9 specifics.
- **Find help:** the [build options](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners) section lists OR-Tools, VROOM and PuLP with HiGHS; INFORMS Pro Bono Analytics is the case's best-fit partner.
- **Read** the OR-Tools routing guide and the WFP Optimus project page, then Peters et al. (2021) and Bertsimas, Delarue & Martin (2019), all listed in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact).
- **Other tutorials:** [robust optimization](04-robust-optimization-cyclone-prepositioning.md) for when road closures become unpredictable and severe; [welfare optimization](02-welfare-optimization-borehole-siting.md) for deciding *who* gets a resource rather than how it travels, the confusion this case warns against; and [security games](03-security-games-marine-patrols.md) for movement over territory when someone is actively avoiding you.
