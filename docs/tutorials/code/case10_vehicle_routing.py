"""Case 10 tutorial code: vehicle routing with capacities and time windows.

Every number quoted in docs/tutorials/10-vehicle-routing-food-delivery.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case10_vehicle_routing.py

It needs numpy and PuLP 3 (which ships with the free CBC solver). The region,
roads, distribution points, GPS logs and opening hours are synthetic, generated
with fixed random seeds; they are made up for teaching. Only the solve times
change from run to run.
"""

import itertools
import math
import time

import numpy as np
import pulp

N_POINTS = 140           # distribution points
N_WAREHOUSES = 3
N_TRUCKS = 12            # 4 per warehouse
TRUCKS_PER_WH = 4
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]   # each point opens on one day a week
CAPACITY_KG = 6000       # load limit per truck
DAY_START = 7 * 60       # trucks leave the warehouse from 07:00 (minutes after midnight)
DAY_END = 18 * 60        # and must be back by 18:00
BUFFER_MIN = 15          # the planner aims to arrive 15 minutes before a point closes
FUEL_COST_PER_KM = 0.42  # US$ per km: about 0.30 litres/km at US$1.40 a litre (illustrative)
WEEKS_SIMULATED = 200    # weeks of random travel times used to measure on-time share

RIVER_X = 50.0           # a river runs north-south through the region at x = 50 km
CROSSINGS = {"North bridge": (50, 58), "Ford 2": (50, 42),
             "Ford 1": (50, 25), "South bridge": (50, 8)}
WET_CLOSED = {"Ford 1", "Ford 2"}   # the fords close every rainy season
WH_XY = np.array([(22, 48), (78, 40), (26, 14)], float)
WH_NAMES = ["W1", "W2", "W3"]
WH_STOCK_KG = [110000, 40000, 70000]  # food each warehouse can send out per week (W2 is small)


def solve(prob, limit=None):
    """Solve with the free CBC solver that ships with PuLP; return seconds taken."""
    start = time.perf_counter()
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=limit))
    return time.perf_counter() - start


def hhmm(minutes):
    return f"{int(minutes) // 60:02d}:{int(minutes) % 60:02d}"


# ------------------------------------------------------------ Shared routing ---

def schedule(route, T, depot, open_, close_, service, buffer=0.0):
    """Drive a route (list of stops) from `depot`, waiting if a point is not open yet.

    Returns (arrival time at each stop, time back at the depot, feasible?).
    Feasible means every arrival is at least `buffer` minutes before closing and
    the truck is back by DAY_END.
    """
    t, here, arrivals, ok = DAY_START, depot, [], True
    for s in route:
        t += T[here, s]
        arrivals.append(t)
        if t > close_[s] - buffer:
            ok = False
        t = max(t, open_[s]) + service[s]
        here = s
    back = t + T[here, depot]
    return arrivals, back, ok and back <= DAY_END


def route_km(route, D, depot):
    stops = [depot] + list(route) + [depot]
    return sum(D[a, b] for a, b in zip(stops, stops[1:]))


def exact_vrptw(stops, depot, D, T, demand, open_, close_, service, trucks, limit=60,
                cap=CAPACITY_KG):
    """The exact model: one yes/no variable x[i,j] per possible leg i -> j.

    Constraints: every stop entered and left once; at most `trucks` routes; loads
    and arrival times carried along each used leg (this also rules out loops that
    never visit the depot). Minimize total km.
    """
    nodes = [depot] + list(stops)
    prob = pulp.LpProblem("vrptw", pulp.LpMinimize)
    x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", cat="Binary")
         for i in nodes for j in nodes if i != j}
    load = {i: pulp.LpVariable(f"load_{i}", demand[i], cap) for i in stops}
    arr = {i: pulp.LpVariable(f"arr_{i}", DAY_START, close_[i]) for i in stops}
    prob += pulp.lpSum(D[i, j] * x[i, j] for (i, j) in x)
    for i in stops:
        prob += pulp.lpSum(x[i, j] for j in nodes if j != i) == 1     # leave once
        prob += pulp.lpSum(x[j, i] for j in nodes if j != i) == 1     # enter once
    prob += pulp.lpSum(x[depot, j] for j in stops) <= trucks
    prob += pulp.lpSum(x[depot, j] for j in stops) == pulp.lpSum(x[j, depot] for j in stops)
    big = 2000
    for i in stops:
        prob += arr[i] >= DAY_START + T[depot, i]                      # can't arrive earlier
        prob += arr[i] + service[i] + T[i, depot] <= DAY_END           # back in time
        for j in stops:
            if i != j:
                prob += load[j] >= load[i] + demand[j] - cap * (1 - x[i, j])
                # arrival at j >= (arrival at i, or opening time if later) + service + drive
                prob += arr[j] >= arr[i] + service[i] + T[i, j] - big * (1 - x[i, j])
                prob += arr[j] >= open_[i] + service[i] + T[i, j] - big * (1 - x[i, j])
    secs = solve(prob, limit)
    status = pulp.LpStatus[prob.status]
    succ = {i: j for (i, j), v in x.items() if v.value() > 0.5 and i != depot}
    routes = []
    for j in (j for j in stops if x[depot, j].value() > 0.5):   # follow each truck's legs
        r = [j]
        while succ[r[-1]] != depot:
            r.append(succ[r[-1]])
        routes.append(r)
    return routes, pulp.value(prob.objective), secs, status


def clarke_wright(stops, depot, D, T, demand, open_, close_, service, buffer=0.0,
                  cap=CAPACITY_KG):
    """Clarke-Wright savings: start with one truck per stop, then join routes
    end-to-start in order of the km each join saves, if the joined route still fits
    the truck and every opening window."""
    routes = {s: [s] for s in stops}          # route id -> list of stops
    where = {s: s for s in stops}             # stop -> route id
    savings = sorted(((D[depot, i] + D[depot, j] - D[i, j], i, j)
                      for i in stops for j in stops if i < j), reverse=True)
    for sav, i, j in savings:
        ri, rj = where[i], where[j]
        if ri == rj or sav <= 0:
            continue
        a, b = routes[ri], routes[rj]
        options = []
        if a[-1] == i and b[0] == j: options.append(a + b)
        if b[-1] == j and a[0] == i: options.append(b + a)
        if a[0] == i and b[0] == j: options.append(a[::-1] + b)
        if a[-1] == i and b[-1] == j: options.append(a + b[::-1])
        for cand in options:
            if sum(demand[s] for s in cand) > cap:
                continue
            if schedule(cand, T, depot, open_, close_, service, buffer)[2]:
                routes[ri] = cand
                del routes[rj]
                for s in cand:
                    where[s] = ri
                break
    return list(routes.values())


def relocate(routes, D, T, depot, demand, open_, close_, service, buffer=0.0):
    """Move single stops between trucks while that saves km and keeps every window and
    load limit. A truck whose last stop moves away is no longer needed."""
    routes = [list(r) for r in routes]
    while True:
        best_gain, best_move = 1e-9, None
        for a, ra in enumerate(routes):
            for i, s in enumerate(ra):
                rest = ra[:i] + ra[i + 1:]
                saved = route_km(ra, D, depot) - route_km(rest, D, depot)
                for b, rb in enumerate(routes):
                    if b == a or sum(demand[x] for x in rb) + demand[s] > CAPACITY_KG:
                        continue
                    for k in range(len(rb) + 1):
                        cand = rb[:k] + [s] + rb[k:]
                        gain = saved - (route_km(cand, D, depot) - route_km(rb, D, depot))
                        if gain > best_gain and \
                                schedule(cand, T, depot, open_, close_, service, buffer)[2] and \
                                schedule(rest, T, depot, open_, close_, service, buffer)[2]:
                            best_gain, best_move = gain, (a, rest, b, cand)
        if best_move is None:
            return [r for r in routes if r]
        a, rest, b, cand = best_move
        routes[a], routes[b] = rest, cand
        routes = [r for r in routes if r]


def two_opt(route, D, T, depot, open_, close_, service, buffer=0.0):
    """Reverse a stretch of the route whenever that shortens it and keeps every window."""
    best = list(route)
    improved = True
    while improved:
        improved = False
        for i in range(len(best) - 1):
            for j in range(i + 1, len(best)):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                if (route_km(cand, D, depot) < route_km(best, D, depot) - 1e-9
                        and schedule(cand, T, depot, open_, close_, service, buffer)[2]):
                    best, improved = cand, True
    return best


# ------------------------------------------------------------- Toy example ---
# 1 depot, 7 stops, 2 trucks of 10 tonnes. Coordinates in km; trucks average 40 km/h,
# so each km takes 1.5 minutes. Service takes 20 minutes at every stop.

TOY_XY = {"Depot": (0, 0), "A": (0, 12), "B": (12, -4), "C": (-8, -6), "D": (8, 14),
          "E": (4, -10), "F": (-10, 6), "G": (14, 6)}
TOY_DEMAND = {"A": 3, "B": 2, "C": 4, "D": 3, "E": 2, "F": 3, "G": 2}   # tonnes
TOY_CAP = 10


def toy_data(window_g=None):
    names = list(TOY_XY)
    xy = np.array([TOY_XY[n] for n in names], float)
    D = np.round(np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(2)), 1)
    T = D * 1.5
    n = len(names)
    demand = np.array([0] + [TOY_DEMAND[s] * 1000 for s in names[1:]])
    open_ = np.full(n, DAY_START, float)
    close_ = np.full(n, DAY_END, float)
    if window_g:                             # point G opens only in this window
        g = names.index("G")
        open_[g], close_[g] = window_g
    service = np.full(n, 20.0)
    return names, D, T, demand, open_, close_, service


def toy_brute_force(D, T, demand, open_, close_, service):
    """List every way to split the 7 stops into at most 2 ordered routes."""
    stops = list(range(1, 8))
    plans = set()
    for perm in itertools.permutations(stops):
        for k in range(1, 8):
            r1, r2 = perm[:k], perm[k:]
            plans.add(frozenset(r for r in (r1, r2) if r))
    feasible, best = 0, (math.inf, None)
    for plan in plans:
        ok = all(sum(demand[s] for s in r) <= TOY_CAP * 1000
                 and schedule(list(r), T, 0, open_, close_, service)[2] for r in plan)
        if ok:
            feasible += 1
            km = sum(route_km(r, D, 0) for r in plan)
            best = min(best, (round(km, 1), sorted(plan)))
    return len(plans), feasible, best


# ------------------------------------------------------ Synthetic full case ---

def make_region(seed=10):
    """140 distribution points around market towns, on both sides of a river.

    Returns a dict of numpy arrays. Index 0-2 are the warehouses, 3-142 the points.
    All of it is invented for teaching.
    """
    rng = np.random.default_rng(seed)
    towns = [((15, 55), 18), ((30, 40), 16), ((12, 28), 14), ((32, 10), 16), ((42, 52), 12),
             ((62, 55), 16), ((80, 52), 14), ((70, 30), 16), ((88, 22), 10), ((60, 12), 8)]
    xy = []
    for (cx, cy), n in towns:
        for _ in range(n):
            xy.append((cx + rng.normal(0, 4.5), cy + rng.normal(0, 4.5)))
    xy = np.clip(np.array(xy), 1, 99)
    xy[:, 0] = np.where(np.abs(xy[:, 0] - RIVER_X) < 1, RIVER_X + 1.5, xy[:, 0])
    n = len(xy)
    demand = (np.round(rng.uniform(600, 1800, n) / 50) * 50).astype(int)   # kg per week
    day = rng.permutation(np.repeat(np.arange(len(DAYS)), n // len(DAYS)))   # 28 a day
    open_ = rng.choice([8, 9, 10, 11, 13, 14], n) * 60.0
    close_ = open_ + rng.choice([2, 2.5, 3], n) * 60
    dirt = rng.random(n) < 0.3                           # reached by a dirt road
    washout = dirt & (rng.random(n) < 0.4)               # its track floods in the rains
    all_xy = np.vstack([WH_XY, xy])
    m = len(all_xy)
    # Roads wind: road km = straight-line km x 1.3 x a pair-specific factor.
    f = np.exp(rng.normal(0, 0.08, (m, m)))
    pair = np.triu(f, 1) + np.triu(f, 1).T + np.eye(m)
    # Real speeds vary by road in ways a map doesn't show (hills, potholes, markets).
    g = np.exp(rng.normal(0, 0.12, (m, m)))
    speedf = np.triu(g, 1) + np.triu(g, 1).T + np.eye(m)
    return {"xy": all_xy, "demand": np.concatenate([[0, 0, 0], demand]),
            "day": np.concatenate([[-1] * 3, day]),
            "open": np.concatenate([[DAY_START] * 3, open_]),
            "close": np.concatenate([[DAY_END] * 3, close_]),
            "dirt": np.concatenate([[False] * 3, dirt]), "pair": pair, "speedf": speedf,
            "washout": np.concatenate([[False] * 3, washout]),
            "service": np.concatenate([[0, 0, 0], 15 + demand / 200])}


def road_km(region, closed=(), wet=False):
    """Road km between every pair; crossing the river must go through an open crossing.
    In the rains, a point whose track floods is reached by a 12 km longer way round."""
    xy = region["xy"]
    straight = np.sqrt(((xy[:, None] - xy[None]) ** 2).sum(2))
    west = xy[:, 0] < RIVER_X
    cross = west[:, None] != west[None, :]
    via = np.full(straight.shape, np.inf)
    for name, c in CROSSINGS.items():
        if name in closed:
            continue
        dc = np.sqrt(((xy - np.array(c)) ** 2).sum(1))
        via = np.minimum(via, dc[:, None] + dc[None, :])
    base = np.where(cross, via, straight)
    km = base * 1.3 * region["pair"]
    if wet:
        w = region["washout"].astype(float)
        km = km + 12 * (w[:, None] + w[None, :]) * (1 - np.eye(len(km)))
    return km


def true_minutes(region, D, wet=False):
    """Median driving minutes: 45 km/h on sealed roads, 30 km/h if either end is on a
    dirt road (20 km/h in the rainy season)."""
    dirt = region["dirt"][:, None] | region["dirt"][None, :]
    speed = np.where(dirt, 20.0 if wet else 30.0, 45.0)
    return D / (speed * region["speedf"]) * 60


def legs(routes_by_key):
    """Every (from, to) leg driven by a set of routes, depot legs included."""
    out = set()
    for (w, _), routes in routes_by_key.items():
        for r in routes:
            stops = [w] + list(r) + [w]
            out |= set(zip(stops, stops[1:]))
    return out


def plan_routes(region, assign, D, T, method, buffer=BUFFER_MIN):
    """Route every warehouse-day. Returns {(warehouse, day): [routes]}."""
    plan = {}
    args = (region["demand"], region["open"], region["close"], region["service"])
    for w in range(N_WAREHOUSES):
        for d in range(len(DAYS)):
            stops = [p for p in range(3, len(D)) if assign[p] == w and region["day"][p] == d]
            if not stops:
                continue
            if method == "current":
                plan[w, d] = current_routes(region, stops)
            else:                            # Clarke-Wright, then the two improvement moves
                routes = clarke_wright(stops, w, D, T, *args, buffer)
                routes = relocate(routes, D, T, w, *args, buffer)
                plan[w, d] = [two_opt(r, D, T, w, *args[1:], buffer) for r in routes]
    return plan


def current_routes(region, stops):
    """The dispatcher's habit: list the day's points by opening hour and fill one
    truck after another to its load limit, visiting them in that order."""
    order = sorted(stops, key=lambda s: (region["open"][s], s))
    routes, r = [], []
    for s in order:
        if sum(region["demand"][x] for x in r) + region["demand"][s] > CAPACITY_KG:
            routes.append(r)
            r = []
        r.append(s)
    return routes + [r]


def evaluate(region, plan, D, T_true, rng):
    """Weekly km, fuel, trucks, and on-time share over simulated weeks.

    Each leg's driving time = its median x random variation (most legs within about
    +/-30%), plus a 5% chance of a 20-60 minute hold-up (a puncture, a herd on the road).
    """
    km = sum(route_km(r, D, w) for (w, _), rs in plan.items() for r in rs)
    per_day = [sum(len(rs) for (w, d), rs in plan.items() if d == day) for day in range(len(DAYS))]
    on_time = total = 0
    for _ in range(WEEKS_SIMULATED):
        for (w, _), routes in plan.items():
            for r in routes:
                t, here = DAY_START, w
                for s in r:
                    drive = T_true[here, s] * rng.lognormal(0, 0.15)
                    if rng.random() < 0.05:
                        drive += rng.uniform(20, 60)
                    t += drive
                    on_time += t <= region["close"][s]
                    total += 1
                    t = max(t, region["open"][s]) + region["service"][s]
                    here = s
    return {"km": km, "fuel": km * FUEL_COST_PER_KM, "truck_days": sum(per_day),
            "peak": max(per_day), "on_time": on_time / total}


def assign_ilp(region, D):
    """Which warehouse serves each point: minimize out-and-back km, within each
    warehouse's weekly stock and daily truck capacity (4 trucks x 6 t, kept to 85% for
    slack). Out-and-back km is only a stand-in for route km, but a cheap and decent one."""
    pts = range(3, len(D))
    prob = pulp.LpProblem("assign", pulp.LpMinimize)
    z = {(p, w): pulp.LpVariable(f"z_{p}_{w}", cat="Binary") for p in pts for w in range(3)}
    prob += pulp.lpSum(2 * D[w, p] * z[p, w] for (p, w) in z)
    for p in pts:
        prob += pulp.lpSum(z[p, w] for w in range(3)) == 1
    for w in range(3):
        prob += pulp.lpSum(region["demand"][p] * z[p, w] for p in pts) <= WH_STOCK_KG[w]
        for d in range(len(DAYS)):
            prob += pulp.lpSum(region["demand"][p] * z[p, w] for p in pts
                               if region["day"][p] == d) <= 0.85 * TRUCKS_PER_WH * CAPACITY_KG
    secs = solve(prob)
    return {p: w for (p, w), v in z.items() if v.value() > 0.5}, secs


# --------------------------------------------------------------------- main ---

def main():
    print("Decision engine - toy: 1 depot, 7 stops, 2 trucks of 10 t (km between points)")
    names, D, T, dem, op, cl, sv = toy_data()
    print("        " + " ".join(f"{n[:5]:>5s}" for n in names))
    for i, n in enumerate(names):
        print(f"  {n:5s} " + " ".join(f"{D[i, j]:5.1f}" for j in range(len(names))))
    print("  demand (t): " + ", ".join(f"{k}={v}" for k, v in TOY_DEMAND.items())
          + f"  total={sum(TOY_DEMAND.values())}")
    hand = [[1, 2, 3], [4, 5, 6, 7]]            # A-B-C and D-E-F-G, alphabetical lists
    print(f"  hand plan A-B-C | D-E-F-G: km={sum(route_km(r, D, 0) for r in hand):.1f}  "
          f"loads={[int(sum(dem[s] for s in r)) // 1000 for r in hand]}")
    for label, window in (("capacity only", None), ("G open 07:00-07:30 only", (420, 450))):
        names, D, T, dem, op, cl, sv = toy_data(window)
        routes, obj, secs, status = exact_vrptw(range(1, 8), 0, D, T, dem, op, cl, sv, 2,
                                                cap=TOY_CAP * 1000)
        n_plans, n_feas, best = toy_brute_force(D, T, dem, op, cl, sv)
        show = " | ".join("-".join(names[s] for s in r) for r in routes)
        print(f"  [{label}] PuLP: {show}  km={obj:.1f}  ({status}, {secs:.2f}s)")
        print(f"  [{label}] brute force: {n_plans:,} possible plans, {n_feas:,} feasible, "
              f"best km={best[0]}")
        cw = clarke_wright(list(range(1, 8)), 0, D, T, dem, op, cl, sv, cap=TOY_CAP * 1000)
        show = " | ".join("-".join(names[s] for s in r) for r in cw)
        print(f"  [{label}] Clarke-Wright: {show}  km={sum(route_km(r, D, 0) for r in cw):.1f}")
    names, D, T, dem, op, cl, sv = toy_data()                 # back to capacity only
    sav = sorted(((D[0, i] + D[0, j] - D[i, j], names[i], names[j])
                  for i in range(1, 8) for j in range(i + 1, 8)), reverse=True)
    print("  top savings s(i,j) = d(depot,i) + d(depot,j) - d(i,j): "
          + ", ".join(f"{a}-{b} {s:.1f}" for s, a, b in sav[:6]))

    print("\nCore bottleneck - how fast the number of possible routes grows")
    for n in (7, 10, 28, 140):
        print(f"  {n:3d} stops: orderings for one truck = {n}! = 10^{math.lgamma(n + 1) / math.log(10):.1f}")

    region = make_region()
    D_dry = road_km(region)
    T_dry = true_minutes(region, D_dry)
    D_wet = road_km(region, WET_CLOSED, wet=True)
    T_wet = true_minutes(region, D_wet, wet=True)
    xy = region["xy"]
    print("\nScaling up - the synthetic region")
    print(f"  points={N_POINTS}  warehouses={N_WAREHOUSES}  trucks={N_TRUCKS} "
          f"({TRUCKS_PER_WH} per warehouse, {CAPACITY_KG:,} kg each)")
    print(f"  weekly demand={region['demand'].sum():,} kg  points per day="
          f"{[int((region['day'] == d).sum()) for d in range(5)]}  east of river="
          f"{int((xy[3:, 0] > RIVER_X).sum())}  on dirt roads={int(region['dirt'].sum())}  "
          f"tracks that flood in the rains={int(region['washout'].sum())}")

    # The inherited lists: W1 is the oldest warehouse and served everyone. When W3 opened
    # it took the points within 20 km of it; small W2 took the points within 17 km of it.
    dist_wh = np.sqrt(((xy[3:, None] - WH_XY[None]) ** 2).sum(2))
    inherited = {p: (2 if dist_wh[p - 3, 2] < 20 else 1 if dist_wh[p - 3, 1] < 17 else 0)
                 for p in range(3, len(xy))}

    print("\nEstimates - travel times from two years of GPS logs (on the current routes)")
    rng = np.random.default_rng(7)
    current = plan_routes(region, inherited, D_dry, T_dry, "current")
    driven = sorted(legs(current))
    gps_med, hand_med = {}, {}
    example = None
    for (a, b) in driven:
        trips = T_dry[a, b] * rng.lognormal(0, 0.15, 74)               # 74 dry-season weeks
        trips += np.where(rng.random(74) < 0.05, rng.uniform(20, 60, 74), 0)
        logged = trips[rng.random(74) > 0.25]                           # 25% lost: no signal
        gps_med[a, b] = np.median(logged)
        # Handwritten: rounded to 15 minutes; 30% are the 'usual' figure written afterwards.
        usual = np.round(D_dry[a, b] / 50 * 60 / 15) * 15
        written = np.where(rng.random(74) < 0.3, usual, np.round(trips / 15) * 15)
        hand_med[a, b] = np.median(written)
        if example is None and region["dirt"][b] and T_dry[a, b] > 40:
            example = (a, b, logged)
    a, b, logged = example
    boots = np.median(rng.choice(logged, (2000, len(logged))), axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    print(f"  legs driven by current routes={len(driven)} of {len(xy) * (len(xy) - 1):,} possible")
    print(f"  example leg ({D_dry[a, b]:.1f} road km, dirt road): {len(logged)} GPS trips of 74 "
          f"(rest lost to signal); median={np.median(logged):.1f} min, mean={logged.mean():.1f} min, "
          f"bootstrap 95% CI for median={lo:.1f} to {hi:.1f}; true median={T_dry[a, b]:.1f}")
    err_gps = np.array([abs(gps_med[k] - T_dry[k]) for k in driven])
    err_hand = np.array([abs(hand_med[k] - T_dry[k]) for k in driven])
    print(f"  error of each leg's median vs truth: GPS median abs error={np.median(err_gps):.1f} min, "
          f"off by >10 min: {np.mean(err_gps > 10):.0%} | handwritten: {np.median(err_hand):.1f} min, "
          f"off by >10 min: {np.mean(err_hand > 10):.0%}")
    # Legs nobody has driven: map km / speed, with speeds estimated from the logged legs.
    dirt_leg = region["dirt"][:, None] | region["dirt"][None, :]
    speeds = {}
    for label, mask in (("sealed", False), ("dirt", True)):
        ks = [k for k in driven if dirt_leg[k] == mask]
        sp = np.array([D_dry[k] / gps_med[k] * 60 for k in ks])
        speeds[mask] = np.median(sp)
        print(f"  {label} legs: {len(ks)} logged, median speed={speeds[mask]:.1f} km/h")
    T_hat = np.where(dirt_leg, D_dry / speeds[True] * 60, D_dry / speeds[False] * 60)
    for k, v in gps_med.items():
        T_hat[k] = v
    off = np.abs(T_hat - T_dry) / np.maximum(T_dry, 1e-9)
    print(f"  estimated travel-time table: median error={np.median(off[~np.eye(len(xy), dtype=bool)]):.1%}")

    print("\nScaling up - which warehouse serves each point")
    assign, secs = assign_ilp(region, D_dry)
    moved = sum(assign[p] != inherited[p] for p in assign)
    for label, a in (("inherited lists", inherited), ("assignment ILP", assign)):
        oab = sum(2 * D_dry[a[p], p] for p in a)
        kg = [int(sum(region["demand"][p] for p in a if a[p] == w)) for w in range(3)]
        print(f"  {label:16s} points per warehouse={[sum(v == w for v in a.values()) for w in range(3)]}"
              f"  kg per week={kg}  out-and-back km={oab:,.0f}")
    print(f"  points that change warehouse={moved}  ({secs:.2f}s)")

    print("\nSimulation - one week of routes, evaluated over "
          f"{WEEKS_SIMULATED} weeks of random travel times (dry season)")
    plans = {"current fixed routes": current,
             "new lists + Clarke-Wright + 2-opt": plan_routes(region, assign, D_dry, T_hat, "cw")}
    results = {}
    for name, plan in plans.items():
        r = evaluate(region, plan, D_dry, T_dry, np.random.default_rng(1))
        results[name] = r
        print(f"  {name:38s} km/week={r['km']:6,.0f}  fuel/week=${r['fuel']:5,.0f}  "
              f"fuel/year=${r['fuel'] * 52:7,.0f}  truck-days={r['truck_days']:2d}  "
              f"peak trucks={r['peak']:2d}  on time={r['on_time']:.1%}")
    over = sum(len(rs) > TRUCKS_PER_WH for k, rs in plans["new lists + Clarke-Wright + 2-opt"].items())
    print(f"  warehouse-days needing more than {TRUCKS_PER_WH} trucks (Clarke-Wright plan): {over}")
    cur, cw = results["current fixed routes"], results["new lists + Clarke-Wright + 2-opt"]
    print(f"  Clarke-Wright vs current: km/week {cw['km'] - cur['km']:+,.0f} "
          f"({cw['km'] / cur['km'] - 1:+.1%}), fuel/year -${(cur['fuel'] - cw['fuel']) * 52:,.0f}")
    cw_old = plan_routes(region, inherited, D_dry, T_hat, "cw")
    r = evaluate(region, cw_old, D_dry, T_dry, np.random.default_rng(1))
    print(f"  (Clarke-Wright on the inherited lists: km/week={r['km']:,.0f}, on time={r['on_time']:.1%})")

    print("\nDecision engine check - exact PuLP model vs the heuristic on two warehouse-days")
    cw_plan = plans["new lists + Clarke-Wright + 2-opt"]
    sizes = {k: sum(len(r) for r in rs) for k, rs in cw_plan.items()}
    print(f"  warehouse-days={len(sizes)}; stops per warehouse-day: smallest={min(sizes.values())}, median="
          f"{int(np.median(list(sizes.values())))}, largest={max(sizes.values())}")
    typical = max((k for k in sizes if sizes[k] <= 12), key=lambda k: (sizes[k], k))
    busiest = max(sizes, key=lambda k: (sizes[k], k))
    cl_buf = region["close"] - BUFFER_MIN
    for key in (typical, busiest):
        w, d = key
        stops = [s for r in cw_plan[key] for s in r]
        routes, obj, secs, status = exact_vrptw(stops, w, D_dry, T_hat, region["demand"],
                                                region["open"], cl_buf, region["service"],
                                                TRUCKS_PER_WH, limit=90)
        heur = sum(route_km(r, D_dry, w) for r in cw_plan[key])
        print(f"  {WH_NAMES[w]} on {DAYS[d]}: {len(stops)} stops; Clarke-Wright+2-opt={heur:.1f} km "
              f"in {len(cw_plan[key])} trucks; exact={obj:.1f} km in {len(routes)} trucks "
              f"({status}, {secs:.1f}s); heuristic above exact by {max(heur / obj - 1, 0):.1%}")

    print("\nScaling up - rainy season: Ford 1 and Ford 2 closed, dirt roads slower")
    wet_rows = {"dry-season plan driven in the rains":
                evaluate(region, cw_plan, D_wet, T_wet, np.random.default_rng(1))}
    # Planner's wet table: map km with the fords closed / estimated speeds, dirt legs
    # slowed by the wet/dry ratio seen in rainy-season logs (here, 30/20 = 1.5).
    T_hat_wet = np.where(dirt_leg, D_wet / speeds[True] * 60 * 1.5, D_wet / speeds[False] * 60)
    assign_wet, _ = assign_ilp(region, D_wet)
    print(f"  points that change warehouse in the wet-season assignment="
          f"{sum(assign_wet[p] != assign[p] for p in assign)}")
    wet_plan = plan_routes(region, assign_wet, D_wet, T_hat_wet, "cw")
    wet_rows["wet-season plan (re-solved)"] = evaluate(region, wet_plan, D_wet, T_wet,
                                                       np.random.default_rng(1))
    for name, r in wet_rows.items():
        print(f"  {name:38s} km/week={r['km']:6,.0f}  fuel/week=${r['fuel']:5,.0f}  "
              f"truck-days={r['truck_days']:2d}  peak trucks={r['peak']:2d}  on time={r['on_time']:.1%}")
    D_ford = road_km(region, WET_CLOSED)            # dry roads, fords closed
    uses_ford = [(a, b) for a, b in legs(cw_plan) if D_ford[a, b] > D_dry[a, b] + 0.5]
    flooded = [(a, b) for a, b in legs(cw_plan) if region["washout"][a] or region["washout"][b]]
    print(f"  legs in the dry plan that use a ford={len(uses_ford)} (extra km when closed: median="
          f"{np.median([D_ford[k] - D_dry[k] for k in uses_ford]):.1f}); legs on a track that "
          f"floods={len(flooded)} (+12 km each); legs in the plan={len(legs(cw_plan))}")

    print("\nField pathway - a printed route sheet (dry plan, one truck)")
    key, r = next((k, r) for k, rs in sorted(cw_plan.items()) for r in rs
                  if any(D_ford[a, b] > D_dry[a, b] + 0.5 for a, b in zip([k[0]] + r, r + [k[0]])))
    w, d = key
    arr, back, _ = schedule(r, T_hat, w, region["open"], region["close"], region["service"])
    print(f"  Truck from {WH_NAMES[w]}, {DAYS[d]}. Leave {hhmm(DAY_START)}. "
          f"Load {sum(region['demand'][s] for s in r):,} kg.")
    for i, (s, t) in enumerate(zip(r, arr), 1):
        print(f"  {i}. Point P{s - 2:03d}  open {hhmm(region['open'][s])}-{hhmm(region['close'][s])}"
              f"  plan {hhmm(t)}  {region['demand'][s]:,} kg")
    print(f"  Back at {WH_NAMES[w]} about {hhmm(back)}")
    stops = [w] + r + [w]
    for a, b in zip(stops, stops[1:]):
        if D_wet[a, b] > D_dry[a, b] + 0.5:
            why = ("track floods" if region["washout"][a] or region["washout"][b] else "")
            if D_ford[a, b] > D_dry[a, b] + 0.5:
                why = "fords closed, cross by bridge" + (" + " + why if why else "")
            name = lambda n: WH_NAMES[n] if n < 3 else f"P{n - 2:03d}"
            print(f"  WET-SEASON ALTERNATIVE {name(a)} -> {name(b)}: {why}, "
                  f"+{D_wet[a, b] - D_dry[a, b]:.0f} km")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f"\n(total run time {time.perf_counter() - start:.1f}s)")
