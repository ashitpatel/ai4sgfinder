"""Case 11 tutorial code: predicting employment, then placing families as they arrive.

Every number quoted in docs/tutorials/11-online-assignment-refugee-placement.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case11_online_assignment.py

It needs numpy and PuLP 3 (which ships with the free CBC solver). The cities,
families, arrivals and employment outcomes are synthetic, generated with fixed
random seeds; they are made up for teaching. The program runs in well under a
minute; only the timing line changes from run to run.

Steps:
  1. Prediction: estimate each family type x city employment chance from five
     years of records (group rates shrunk toward a simpler estimate, with CIs).
  2. Offline benchmark: the "hindsight best" integer program, as if the whole
     year's families were known up front.
  3. Online rules: first-available, greedy, bid prices and weekly re-solving with
     a forecast, on a 6-family hand example and then a simulated year.
"""

import time

import numpy as np
import pulp

N_CITIES = 30
TOTAL_QUOTA = 1050       # yearly places agreed across the 30 cities
ARRIVALS_PER_YEAR = 960   # expected referrals per year (families)
WEEKS = 52
HISTORY_YEARS = 5
TRADES = ["skilled trade", "service work", "no prior work"]
# A family "type" is (trade, some English?, large family?): 3 x 2 x 2 = 12 types.
TYPES = [(t, e, s) for t in range(3) for e in (1, 0) for s in (0, 1)]
N_TYPES = len(TYPES)


def solve(prob):
    """Solve with the free CBC solver that ships with PuLP."""
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    assert pulp.LpStatus[prob.status] == "Optimal", pulp.LpStatus[prob.status]


# --------------------------------------------------------- Decision engine ---
# Hand example: 3 cities, 6 families arriving one after another.

TOY_P = {  # chance someone in the family is working at six months, by city
    "service": {"A": 0.50, "B": 0.30, "C": 0.45},
    "trade": {"A": 0.60, "B": 0.55, "C": 0.20},
    "no prior work": {"A": 0.55, "B": 0.25, "C": 0.15},
}
TOY_QUOTA = {"A": 2, "B": 2, "C": 3}
TOY_ORDER = ["service", "service", "trade", "trade", "no prior work", "no prior work"]
TOY_FORECAST = {"service": 2, "trade": 2, "no prior work": 2}  # from past seasons


def toy_best(families, quota, fixed=None, relax=False):
    """Best assignment of a list of family kinds to cities under the quotas.

    `fixed` forces the first family to a city. Returns (value, cities, duals)."""
    prob = pulp.LpProblem("toy", pulp.LpMaximize)
    cat = "Continuous" if relax else "Binary"
    x = {(i, c): pulp.LpVariable(f"x_{i}_{c}", 0, 1, cat=cat)
         for i in range(len(families)) for c in quota}
    prob += pulp.lpSum(TOY_P[families[i]][c] * x[i, c] for (i, c) in x)
    for i in range(len(families)):
        prob += pulp.lpSum(x[i, c] for c in quota) == 1
    for c in quota:
        prob += (pulp.lpSum(x[i, c] for i in range(len(families))) <= quota[c], f"q_{c}")
    if fixed is not None:
        prob += x[0, fixed] == 1
    solve(prob)
    cities = [max(quota, key=lambda c: x[i, c].value()) for i in range(len(families))]
    duals = {c: prob.constraints[f"q_{c}"].pi for c in quota} if relax else None
    return pulp.value(prob.objective), cities, duals


def toy_online(order, rule):
    """Place families one at a time: 'greedy', 'resolve' (re-solve with the forecast)
    or 'bid price' (chance minus the city's price; ties go to the higher chance)."""
    room = dict(TOY_QUOTA)
    forecast_families = [k for k, n in TOY_FORECAST.items() for _ in range(n)]
    prices = toy_best(forecast_families, TOY_QUOTA, relax=True)[2]
    left = dict(TOY_FORECAST)  # forecast of who is still to come, including this family
    total, placed = 0.0, []
    for kind in order:
        open_c = {c: q for c, q in room.items() if q > 0}
        if rule == "greedy":
            city = max(open_c, key=lambda c: TOY_P[kind][c])
        elif rule == "bid price":
            city = max(open_c, key=lambda c: (round(TOY_P[kind][c] - prices[c], 6),
                                              TOY_P[kind][c]))
        else:
            # Pretend the forecast families are real, solve, keep only this family's city.
            left[kind] = max(left[kind] - 1, 0)
            future = [k for k, n in left.items() for _ in range(n)]
            future = future[: sum(open_c.values()) - 1]  # forecast can't exceed the room
            _, cities, _ = toy_best([kind] + future, open_c)
            city = cities[0]
        room[city] -= 1
        total += TOY_P[kind][city]
        placed.append(city)
    return total, placed


def hand_example():
    print("Decision engine - hand example: 3 cities (quotas A=2, B=2, C=3), 6 families in order")
    for rule in ("greedy", "resolve", "bid price"):
        val, placed = toy_online(TOY_ORDER, rule)
        print(f"  {rule:8s} placements={placed}  expected employed={val:.2f}")
    val, cities, _ = toy_best(TOY_ORDER, TOY_QUOTA)
    print(f"  hindsight best placements={cities}  expected employed={val:.2f}")
    _, _, duals = toy_best(TOY_ORDER, TOY_QUOTA, relax=True)
    print(f"  bid prices (LP shadow prices of the quotas) = "
          + "  ".join(f"{c}={v:.2f}" for c, v in duals.items()))
    for kind in TOY_P:
        scores = {c: TOY_P[kind][c] - duals[c] for c in TOY_QUOTA}
        print(f"    {kind:14s} chance - price: "
              + "  ".join(f"{c}={s:.2f}" for c, s in scores.items()))
    # Forecast wrong: the last two families are service, not 'no prior work'.
    wrong = ["service", "service", "trade", "trade", "service", "service"]
    for rule in ("greedy", "resolve", "bid price"):
        val, placed = toy_online(wrong, rule)
        print(f"  forecast wrong ({rule}): placements={placed}  expected employed={val:.2f}")
    val, _, _ = toy_best(wrong, TOY_QUOTA)
    print(f"  forecast wrong (hindsight best): expected employed={val:.2f}")


# ------------------------------------------------------------- Synthetic world ---

def make_world(seed=11):
    """True employment chances by type x city, city quotas, and the arrival pattern."""
    rng = np.random.default_rng(seed)
    city_base = rng.normal(-0.7, 0.45, N_CITIES)            # local labour market
    demand = rng.normal(0.0, 0.45, (N_CITIES, 3))            # demand for each trade
    trade_eff = np.array([0.6, 0.2, -0.5])
    logit = np.zeros((N_TYPES, N_CITIES))
    for k, (t, e, s) in enumerate(TYPES):
        logit[k] = city_base + trade_eff[t] + 0.5 * e - 0.15 * s + demand[:, t]
    p_true = 1 / (1 + np.exp(-logit))
    raw = rng.uniform(15, 60, N_CITIES)
    quota = np.floor(raw / raw.sum() * TOTAL_QUOTA).astype(int)
    quota[np.argsort(-raw)[: TOTAL_QUOTA - quota.sum()]] += 1  # sum exactly 1,050
    # Arrivals: weekly volume is seasonal; the share with no prior work rises
    # through the year (18% in January to 50% in December).
    week = np.arange(WEEKS)
    volume = 1 + 0.25 * np.sin(2 * np.pi * (week - 10) / WEEKS)
    volume = volume / volume.sum() * ARRIVALS_PER_YEAR
    no_work = 0.18 + 0.32 * week / (WEEKS - 1)
    trade_mix = np.column_stack([(1 - no_work) * 0.45, (1 - no_work) * 0.55, no_work])
    return dict(p_true=p_true, quota=quota, volume=volume, trade_mix=trade_mix,
                demand=demand)


def draw_year(world, rng, trade_mix=None):
    """One year of arrivals: a list per week of family type indices."""
    mix = world["trade_mix"] if trade_mix is None else trade_mix
    year = []
    for w in range(WEEKS):
        n = rng.poisson(world["volume"][w])
        t = rng.choice(3, n, p=mix[w])
        e = rng.random(n) < 0.45
        s = rng.random(n) < 0.40
        year.append([TYPES.index((ti, int(ei), int(si))) for ti, ei, si in zip(t, e, s)])
    return year


# ------------------------------------------------------- Step 1: prediction ---

def history(world, rng):
    """Five years of records placed by caseworkers (first-available), with outcomes."""
    rows = []  # (year, week, type, city, employed)
    for y in range(HISTORY_YEARS):
        year = draw_year(world, rng)
        room = world["quota"].copy()
        for w, fams in enumerate(year):
            for k in fams:
                c = first_available(room, rng)
                room[c] -= 1
                rows.append((y, w, k, c, int(rng.random() < world["p_true"][k, c])))
    return np.array(rows)


def estimate(rows, k_shrink):
    """Group rates per type x city, shrunk toward city rate + type rate - overall rate."""
    n = np.zeros((N_TYPES, N_CITIES))
    s = np.zeros((N_TYPES, N_CITIES))
    np.add.at(n, (rows[:, 2], rows[:, 3]), 1)
    np.add.at(s, (rows[:, 2], rows[:, 3]), rows[:, 4])
    overall = s.sum() / n.sum()
    city_rate = s.sum(0) / n.sum(0)
    type_rate = s.sum(1) / n.sum(1)
    prior = np.clip(city_rate[None, :] + type_rate[:, None] - overall, 0.02, 0.98)
    est = (s + k_shrink * prior) / (n + k_shrink) if k_shrink < np.inf else prior
    return est, n, s, prior


def prediction_step(world, rows):
    print("Step 1 - prediction from five years of records")
    print(f"  records={len(rows):,}  employed at six months={rows[:, 4].mean():.1%}  "
          f"type x city cells={N_TYPES * N_CITIES}")
    n_all = estimate(rows, 0.001)[1]
    print(f"  families per cell: median={np.median(n_all):.0f}  "
          f"cells with fewer than 5={int((n_all < 5).sum())}  empty={int((n_all == 0).sum())}")
    train, test = rows[rows[:, 0] < 4], rows[rows[:, 0] == 4]
    print("  choose the shrinkage strength k on year 5 held out (fit on years 1-4):")
    for k in (0.001, 5, 10, 20, 40, np.inf):
        est = estimate(train, k)[0]
        brier = np.mean((est[test[:, 2], test[:, 3]] - test[:, 4]) ** 2)
        full = estimate(rows, k)[0]
        mae = np.abs(full - world["p_true"]).mean()
        label = "raw cell rates" if k < 1 else ("prior only" if k == np.inf else f"k={k}")
        print(f"    {label:15s} held-out Brier score={brier:.4f}   "
              f"mean error vs truth (synthetic only)={mae:.3f}")
    est, n, s, prior = estimate(rows, 20)
    print("  example cells (k=20): raw rate with 95% CI -> shrunk estimate (truth)")
    order = np.argsort(n.ravel())
    for idx in [order[40], order[180], order[340]]:
        k, c = divmod(idx, N_CITIES)
        raw = s[k, c] / n[k, c]
        half = 1.96 * np.sqrt(raw * (1 - raw) / n[k, c])
        half_s = 1.96 * np.sqrt(est[k, c] * (1 - est[k, c]) / (n[k, c] + 20))
        print(f"    {TRADES[TYPES[k][0]]:13s} city {c + 1:2d}: {int(s[k, c])}/{int(n[k, c])} = "
              f"{raw:.0%} ({max(raw - half, 0):.0%} to {min(raw + half, 1):.0%}), prior "
              f"{prior[k, c]:.0%} -> {est[k, c]:.0%} ({est[k, c] - half_s:.0%} to "
              f"{est[k, c] + half_s:.0%}); truth {world['p_true'][k, c]:.0%}")
    return est


# ---------------------------------------------- Step 2: hindsight benchmark ---

def hindsight(p, counts, quota):
    """The best plan if the year's families were known in advance (types x cities ILP)."""
    prob = pulp.LpProblem("hindsight", pulp.LpMaximize)
    x = [[pulp.LpVariable(f"x_{k}_{c}", 0, cat="Integer") for c in range(N_CITIES)]
         for k in range(N_TYPES)]
    prob += pulp.lpSum(p[k, c] * x[k][c] for k in range(N_TYPES) for c in range(N_CITIES))
    for k in range(N_TYPES):
        prob += pulp.lpSum(x[k]) == int(counts[k])
    for c in range(N_CITIES):
        prob += pulp.lpSum(x[k][c] for k in range(N_TYPES)) <= int(quota[c])
    solve(prob)
    return np.array([[x[k][c].value() for c in range(N_CITIES)] for k in range(N_TYPES)])


# ---------------------------------------------------- Step 3: online rules ---

def first_available(room, rng):
    """Proxy for current practice: a city with room, more likely the more room it has."""
    return rng.choice(N_CITIES, p=room / room.sum())


def plan_with_forecast(p, fams, future, room):
    """Place this week's families, pretending the forecast future families are real.

    x: this week's real families (yes/no per city); y: forecast families (fractions
    allowed). Returns the city chosen for each of this week's families."""
    prob = pulp.LpProblem("week", pulp.LpMaximize)
    x = [[pulp.LpVariable(f"x_{i}_{c}", 0, 1, cat="Binary") for c in range(N_CITIES)]
         for i in range(len(fams))]
    y = [[pulp.LpVariable(f"y_{k}_{c}", 0) for c in range(N_CITIES)] for k in range(N_TYPES)]
    prob += (pulp.lpSum(p[k, c] * x[i][c] for i, k in enumerate(fams) for c in range(N_CITIES))
             + pulp.lpSum(p[k, c] * y[k][c] for k in range(N_TYPES) for c in range(N_CITIES)))
    for i in range(len(fams)):
        prob += pulp.lpSum(x[i]) == 1
    for k in range(N_TYPES):
        prob += pulp.lpSum(y[k]) == float(future[k])
    for c in range(N_CITIES):
        prob += (pulp.lpSum(x[i][c] for i in range(len(fams)))
                 + pulp.lpSum(y[k][c] for k in range(N_TYPES)) <= float(room[c]), f"q{c}")
    solve(prob)
    cities = [int(np.argmax([v.value() for v in x[i]])) for i in range(len(fams))]
    return cities


def bid_prices(p, future, room):
    """Shadow price of one more place in each city, from the forecast LP."""
    prob = pulp.LpProblem("bid", pulp.LpMaximize)
    y = [[pulp.LpVariable(f"y_{k}_{c}", 0) for c in range(N_CITIES)] for k in range(N_TYPES)]
    prob += pulp.lpSum(p[k, c] * y[k][c] for k in range(N_TYPES) for c in range(N_CITIES))
    for k in range(N_TYPES):
        prob += pulp.lpSum(y[k]) == float(future[k])
    for c in range(N_CITIES):
        prob += (pulp.lpSum(y[k][c] for k in range(N_TYPES)) <= float(room[c]), f"q{c}")
    solve(prob)
    return np.array([prob.constraints[f"q{c}"].pi for c in range(N_CITIES)])


def run_year(policy, year, est, world, forecast, rng, override=0.0, explain=False):
    """Place one year's arrivals. Returns per-family (week, type, city) array."""
    room = world["quota"].astype(float).copy()
    out, prices = [], None
    for w, fams in enumerate(year):
        future = forecast[w + 1:].sum(0)  # expected arrivals by type after this week
        if policy == "bid price" and w % 4 == 0:
            # Re-compute prices every four weeks, without this month's families.
            prices = bid_prices(est, forecast[w:].sum(0) * room.sum() /
                                max(forecast[w:].sum(), room.sum()), room)
        if policy == "re-solve" and fams:
            planned = plan_with_forecast(est, fams, future * min(1, (room.sum() - len(fams))
                                         / max(future.sum(), 1)), room)
        for i, k in enumerate(fams):
            open_c = np.flatnonzero(room > 0)
            if policy == "first-available":
                c = first_available(room, rng)
            elif policy == "greedy":
                c = open_c[np.argmax(est[k, open_c])]
            elif policy == "bid price":
                c = open_c[np.argmax(est[k, open_c] - prices[open_c])]
            else:
                c = planned[i] if room[planned[i]] > 0 else open_c[np.argmax(est[k, open_c])]
                if override and rng.random() < override:
                    # The caseworker sets the suggestion aside and picks the 2nd or 3rd
                    # of the top-3 cities with room by predicted chance.
                    top = [j for j in open_c[np.argsort(-est[k, open_c])] if j != c][:2]
                    c = top[rng.integers(len(top))]
            if explain and w >= 26 and i == 0:
                fut = future * min(1, (room.sum() - len(fams)) / max(future.sum(), 1))
                week_price = bid_prices(est, fut, room)
            if explain and w >= 26:
                g = open_c[np.argmax(est[k, open_c])]  # greedy's pick
                net = est[k] - week_price
                if g != c and net[c] - net[g] >= 0.03:
                    show_explanation(w, k, c, g, est, room, world, week_price)
                    explain = False
            room[c] -= 1
            out.append((w, k, c))
    return np.array(out)


def show_explanation(w, k, c, g, est, room, world, price):
    """What a caseworker would see: the suggestion and greedy's pick, with reasons."""
    t, e, s = TYPES[k]
    print(f"  explaining one placement: week {w + 1} family ({TRADES[t]}, "
          f"{'some' if e else 'no'} English, {'large' if s else 'small'} family)")
    for j, tag in ((c, "SUGGESTED"), (g, "greedy pick")):
        used = 1 - room[j] / world["quota"][j]
        print(f"    {tag:11s} city {j + 1:2d}: predicted chance {est[k, j]:.1%}, quota "
              f"{used:.0%} used, bid price {price[j]:.2f}, chance - price "
              f"{est[k, j] - price[j]:+.2f}")
    others = [q for q in range(N_TYPES) if TYPES[q][0] != t]
    q = max(others, key=lambda q: est[q, g] - est[q, c])
    print(f"    expected later arrivals such as {TRADES[TYPES[q][0]]} families gain "
          f"{est[q, g] - est[q, c]:+.1%} in city {g + 1} vs city {c + 1}; this family "
          f"gains {est[k, g] - est[k, c]:+.1%}")


def summarise(name, placed, world, counts_hind=None):
    p = world["p_true"]
    val = p[placed[:, 1], placed[:, 2]]
    q = placed[:, 0] // 13
    by_q = [val[q == j].mean() if (q == j).any() else np.nan for j in range(4)]
    nw = np.array([TYPES[k][0] == 2 for k in placed[:, 1]])
    used = np.bincount(placed[:, 2], minlength=N_CITIES)
    full26 = int((np.bincount(placed[placed[:, 0] < 26, 2], minlength=N_CITIES)
                  >= world["quota"]).sum())
    return dict(name=name, employed=val.sum(), by_q=by_q, nw=val[nw].mean(),
                other=val[~nw].mean(), use=used.sum() / world["quota"].sum(), full26=full26)


def simulate(world, est, forecast, years, label, override_run=True, explain=False):
    policies = ["first-available", "greedy", "bid price", "re-solve"]
    res = {pol: [] for pol in policies + ["re-solve + 15% overrides", "hindsight best",
                                          "hindsight, true chances"]}
    for y, year in enumerate(years):
        for pol in policies:
            rng = np.random.default_rng(1000 + y)
            exp = explain and y == 0 and pol == "re-solve"
            res[pol].append(summarise(pol, run_year(pol, year, est, world, forecast, rng,
                                                    explain=exp), world))
        if override_run:
            rng = np.random.default_rng(2000 + y)
            res["re-solve + 15% overrides"].append(summarise("", run_year(
                "re-solve", year, est, world, forecast, rng, override=0.15), world))
        counts = np.bincount([k for f in year for k in f], minlength=N_TYPES)
        for name, p in (("hindsight best", est), ("hindsight, true chances", world["p_true"])):
            x = np.rint(hindsight(p, counts, world["quota"])).astype(int)
            rows = [(26, k, c) for k in range(N_TYPES) for c in range(N_CITIES)
                    for _ in range(x[k, c])]
            r = summarise(name, np.array(rows), world)
            r["by_q"] = [np.nan] * 4
            res[name].append(r)
    base = np.array([r["employed"] for r in res["first-available"]])
    n_fam = np.mean([sum(len(f) for f in yr) for yr in years])
    print(f"Simulation - {label}: {len(years)} years, {n_fam:.0f} families a year on average")
    print(f"  {'policy':26s} {'employed':>8s} {'vs current (95% CI)':>22s} "
          f"{'quota use':>9s} {'Q1':>5s} {'Q2':>5s} {'Q3':>5s} {'Q4':>5s} "
          f"{'no-prior':>8s} {'others':>6s} {'full by June':>12s}")
    for name, rs in res.items():
        if not rs:
            continue
        emp = np.array([r["employed"] for r in rs])
        d = emp - base
        half = 1.96 * d.std(ddof=1) / np.sqrt(len(d)) if len(d) > 1 else 0
        bq = np.array([r["by_q"] for r in rs]).mean(0)
        qs = " ".join("  -  " if np.isnan(v) else f"{v:5.1%}" for v in bq)
        full = "-" if name.startswith("hindsight") else f"{np.mean([r['full26'] for r in rs]):.1f}"
        print(f"  {name:26s} {emp.mean():8.1f} {d.mean():+9.1f} ({d.mean() - half:+5.1f} to "
              f"{d.mean() + half:+5.1f}) {np.mean([r['use'] for r in rs]):9.1%} {qs} "
              f"{np.mean([r['nw'] for r in rs]):8.1%} {np.mean([r['other'] for r in rs]):6.1%} "
              f"{full:>12s}")
    return res


def main():
    start = time.perf_counter()
    hand_example()
    print()

    world = make_world()
    print(f"Synthetic world: {N_CITIES} cities, yearly quotas {world['quota'].min()} to "
          f"{world['quota'].max()} (total {world['quota'].sum():,}); about "
          f"{ARRIVALS_PER_YEAR:,} families referred a year")
    best = world["p_true"].mean(0)
    print(f"  true chance averaged over family types: best city {best.max():.0%}, "
          f"median {np.median(best):.0%}, worst {best.min():.0%}")
    rng = np.random.default_rng(5)
    rows = history(world, rng)
    est = prediction_step(world, rows)
    # Forecast: average arrivals by week and type over the five past years.
    forecast = np.zeros((WEEKS, N_TYPES))
    np.add.at(forecast, (rows[:, 1], rows[:, 2]), 1 / HISTORY_YEARS)
    print(f"  forecast from past arrivals: {forecast.sum():.0f} families a year, "
          f"no prior work {forecast[:13, 8:].sum() / forecast[:13].sum():.0%} of Q1 arrivals "
          f"vs {forecast[39:, 8:].sum() / forecast[39:].sum():.0%} of Q4")
    print()

    rng = np.random.default_rng(77)
    years = [draw_year(world, rng) for _ in range(6)]
    simulate(world, est, forecast, years, "typical years", explain=True)
    print()
    # Robustness: this year's mix runs the other way (no-prior-work families arrive
    # early), so the forecast drawn from past years is wrong.
    flipped = world["trade_mix"][::-1]
    years = [draw_year(world, rng, trade_mix=flipped) for _ in range(4)]
    simulate(world, est, forecast, years, "forecast wrong (arrival mix reversed)",
             override_run=False)
    print(f"\nTotal run time {time.perf_counter() - start:.0f}s")


if __name__ == "__main__":
    main()
