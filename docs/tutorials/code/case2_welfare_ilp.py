"""Case 2 tutorial code: a covering integer program with a district fairness rule.

Every number quoted in docs/tutorials/02-welfare-optimization-borehole-siting.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case2_welfare_ilp.py

It needs numpy and PuLP 3 (which ships with the free CBC solver). The villages,
populations and sites are synthetic, generated with fixed random seeds; they are
made up for teaching. Only the solve times change from run to run.
"""

import time
from math import comb

import numpy as np
import pulp

BUDGET = 25              # boreholes the grant pays for
WALK_LIMIT_MIN = 30      # a village is "covered" if a borehole is within a 30-minute walk
WALK_SPEED_KMH = 4.0     # walking speed used to turn distance into minutes
DISTRICTS = ["A", "B", "C", "D"]
# Paths are longer than straight lines. Detour factor = walking distance / straight-line
# distance. District D is hilly, so its paths wind more.
DETOUR = {"A": 1.3, "B": 1.3, "C": 1.3, "D": 1.6}


def solve(prob):
    """Solve with the free CBC solver that ships with PuLP; return seconds taken."""
    start = time.perf_counter()
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    assert pulp.LpStatus[prob.status] == "Optimal", pulp.LpStatus[prob.status]
    return time.perf_counter() - start


# ---------------------------------------------------------- Decision engine ---
# The toy example: 6 villages, 4 candidate sites, 2 districts, budget of 2.

TOY_POP = {"A": 1000, "B": 800, "C": 600, "D": 500, "E": 150, "F": 200}
TOY_DISTRICT = {"A": "North", "B": "North", "C": "North", "D": "North",
                "E": "South", "F": "South"}
# Which villages each candidate site can reach within a 30-minute walk.
TOY_REACH = {"S1": ["A", "B"], "S2": ["A", "B", "C"], "S3": ["D"], "S4": ["E", "F"]}
# The site nearest each village (what a spreadsheet would pick for that village).
TOY_NEAREST = {"A": "S1", "B": "S2", "C": "S2", "D": "S3", "E": "S4", "F": "S4"}


def toy_shares(sites):
    """People covered and each district's covered share, for a set of sites."""
    covered = {v for s in sites for v in TOY_REACH[s]}
    total = sum(TOY_POP[v] for v in covered)
    shares = {}
    for d in ("North", "South"):
        d_pop = sum(p for v, p in TOY_POP.items() if TOY_DISTRICT[v] == d)
        shares[d] = sum(TOY_POP[v] for v in covered if TOY_DISTRICT[v] == d) / d_pop
    return total, shares


def toy_model(fair=False, relax=False, fix=None):
    """The toy as an integer program.

    fair=False: maximize people covered.
    fair=True:  maximize the worst district's covered share (maximin).
    relax=True: allow fractional boreholes (the 'LP relaxation').
    fix:        dict like {"S3": 0} to force a site in or out (a branch).
    """
    cat = "Continuous" if relax else "Binary"
    prob = pulp.LpProblem("toy", pulp.LpMaximize)
    x = {s: pulp.LpVariable(f"drill_{s}", 0, 1, cat=cat) for s in TOY_REACH}
    y = {v: pulp.LpVariable(f"covered_{v}", 0, 1, cat=cat) for v in TOY_POP}
    total = pulp.lpSum(TOY_POP[v] * y[v] for v in TOY_POP)
    if fair:
        t = pulp.LpVariable("worst_share", 0, 1)
        prob += t
        for d in ("North", "South"):
            vs = [v for v in TOY_POP if TOY_DISTRICT[v] == d]
            prob += pulp.lpSum(TOY_POP[v] * y[v] for v in vs) >= t * sum(TOY_POP[v] for v in vs)
    else:
        prob += total
    prob += pulp.lpSum(x.values()) == 2                       # budget
    for v in TOY_POP:                                          # covered only if a chosen site reaches it
        prob += y[v] <= pulp.lpSum(x[s] for s in TOY_REACH if v in TOY_REACH[s])
    for s, val in (fix or {}).items():
        prob += x[s] == val
    solve(prob)
    return {s: round(x[s].value(), 3) for s in x}, pulp.value(prob.objective)


# ------------------------------------------------------ Synthetic full case ---

def make_region(seed=2023):
    """300 villages in 4 districts, plus candidate borehole sites from a survey.

    Returns a dict of numpy arrays. All of it is invented for teaching.
    """
    rng = np.random.default_rng(seed)
    # district: (number of villages, market-town centers (km), median village size)
    layout = {"A": (95, [(10, 38), (16, 30), (6, 28)], 900),   # river valley: big, dense villages
              "B": (80, [(34, 38), (40, 30)], 650),
              "C": (70, [(12, 12), (20, 6)], 600),
              "D": (55, [(34, 14), (42, 6), (30, 4)], 380)}    # hills: small, scattered villages
    xy, pop, dist = [], [], []
    for d, (n, centers, median) in layout.items():
        spread = 4.0 if d == "D" else 2.5
        for i in range(n):
            cx, cy = centers[i % len(centers)]
            xy.append((cx + rng.normal(0, spread), cy + rng.normal(0, spread)))
            pop.append(int(round(median * rng.lognormal(0, 0.5))))
            dist.append(d)
    xy, pop, dist = np.array(xy), np.array(pop), np.array(dist)

    # Hydrogeology survey: candidate points next to most villages, plus some between them.
    near = rng.choice(len(xy), size=150, replace=False)
    cand = np.vstack([xy[near] + rng.normal(0, 0.4, (150, 2)),
                      rng.uniform(0, 48, (30, 2))])
    cand_dist = np.concatenate([dist[near], np.array([nearest_district(p, xy, dist) for p in cand[150:]])])
    # Some ground is dry rock: fewer candidate points are drillable in hilly District D.
    p_drill = np.where(cand_dist == "D", 0.55, 0.7)
    drillable = rng.random(len(cand)) < p_drill
    return {"xy": xy, "pop": pop, "district": dist,
            "site_xy": cand[drillable], "site_district": cand_dist[drillable],
            "n_candidates": len(cand)}


def nearest_district(point, xy, dist):
    return dist[np.argmin(((xy - point) ** 2).sum(axis=1))]


# ---------------------------------------------------------------- Estimates ---

def walk_minutes(region, detour=DETOUR):
    """Village x site table of estimated walking minutes.

    straight-line km x detour factor (of the village's district) / speed x 60.
    """
    diff = region["xy"][:, None, :] - region["site_xy"][None, :, :]
    straight_km = np.sqrt((diff ** 2).sum(axis=2))
    factor = np.array([detour[d] for d in region["district"]])[:, None]
    return straight_km * factor / WALK_SPEED_KMH * 60


def coverage_table(region, limit=WALK_LIMIT_MIN, detour=DETOUR):
    """reach[i, j] = True if site j is within the walking limit of village i."""
    return walk_minutes(region, detour) <= limit


# --------------------------------------------------------------- Scaling up ---

def covered_by(reach, chosen):
    """Boolean per village: is at least one chosen site within reach?"""
    return reach[:, sorted(chosen)].any(axis=1) if chosen else np.zeros(reach.shape[0], bool)


def district_shares(region, covered, pop=None):
    pop = region["pop"] if pop is None else pop
    return {d: pop[covered & (region["district"] == d)].sum() / pop[region["district"] == d].sum()
            for d in DISTRICTS}


def need_ranking(region, reach):
    """The spreadsheet approach: sort villages by need score (here: population),
    and drill the nearest drillable site that reaches each one, until 25 are chosen."""
    minutes = walk_minutes(region)
    chosen = []
    for i in np.argsort(-region["pop"], kind="stable"):
        if not reach[i].any():
            continue                                  # no drillable site within reach
        j = int(np.argmin(minutes[i]))
        if j not in chosen:
            chosen.append(j)
        if len(chosen) == BUDGET:
            break
    return set(chosen)


def greedy(region, reach):
    """A smarter spreadsheet: each round, add the site that covers the most NEW people."""
    chosen, covered = set(), np.zeros(reach.shape[0], bool)
    for _ in range(BUDGET):
        gains = (reach & ~covered[:, None]).T @ region["pop"]
        gains[list(chosen)] = -1
        j = int(np.argmax(gains))
        chosen.add(j)
        covered |= reach[:, j]
    return chosen


def covering_model(region, reach, pop=None, mode="coverage", floor=0.0, worst=None):
    """The maximal covering model (Church & ReVelle 1974) with a district fairness rule.

    mode="coverage": maximize people covered; every district must reach `floor` share.
    mode="maximin":  maximize the worst district's share.
    worst=t:         also require every district >= t (used to break maximin ties
                     in favor of more people covered).
    Returns (chosen sites, seconds, number of decision variables).
    """
    pop = region["pop"] if pop is None else pop
    n_v, n_s = reach.shape
    prob = pulp.LpProblem("boreholes", pulp.LpMaximize)
    x = [pulp.LpVariable(f"drill_{j}", cat="Binary") for j in range(n_s)]
    y = [pulp.LpVariable(f"covered_{i}", cat="Binary") for i in range(n_v)]
    t = pulp.LpVariable("worst_share", 0, 1)
    if mode == "maximin":
        prob += t
    else:
        prob += pulp.lpSum(int(pop[i]) * y[i] for i in range(n_v))
    prob += pulp.lpSum(x) == BUDGET
    for i in range(n_v):
        prob += y[i] <= pulp.lpSum(x[j] for j in np.flatnonzero(reach[i]))
    for d in DISTRICTS:
        members = np.flatnonzero(region["district"] == d)
        d_pop = int(pop[members].sum())
        prob += pulp.lpSum(int(pop[i]) * y[i] for i in members) >= max(floor, worst or 0) * d_pop
        prob += pulp.lpSum(int(pop[i]) * y[i] for i in members) >= t * d_pop
    secs = solve(prob)
    chosen = {j for j in range(n_s) if x[j].value() > 0.5}
    return chosen, secs, n_v + n_s


def maximin_then_coverage(region, reach):
    """Step 1: the best possible worst-district share. Step 2: among plans that achieve it,
    the one covering the most people."""
    chosen, s1, _ = covering_model(region, reach, mode="maximin")
    best_worst = min(district_shares(region, covered_by(reach, chosen)).values())
    # Round down a hair so step 2 is never blocked by floating-point rounding.
    chosen, s2, _ = covering_model(region, reach, worst=best_worst - 1e-6)
    return chosen, s1 + s2, best_worst


def summarize(region, reach, chosen, pop=None):
    pop = region["pop"] if pop is None else pop
    cov = covered_by(reach, chosen)
    shares = district_shares(region, cov, pop)
    per_district = {d: sum(region["site_district"][j] == d for j in chosen) for d in DISTRICTS}
    return int(pop[cov].sum()), shares, per_district


def backup_sites(region, reach, chosen):
    """For each chosen site: if it comes up dry, which unchosen drillable site in the
    SAME district replaces it best? (Same district, so the fairness promise still holds.)"""
    base = region["pop"][covered_by(reach, chosen)].sum()
    lost, recovered, worst = [], [], []
    for j in sorted(chosen):
        rest = chosen - {j}
        without = region["pop"][covered_by(reach, rest)].sum()
        options = [k for k in range(reach.shape[1])
                   if k not in chosen and region["site_district"][k] == region["site_district"][j]]
        best = max(options, key=lambda k: region["pop"][covered_by(reach, rest | {k})].sum())
        lost.append(base - without)
        recovered.append(region["pop"][covered_by(reach, rest | {best})].sum() - without)
        worst.append(min(district_shares(region, covered_by(reach, rest | {best})).values()))
    return np.array(lost), np.array(recovered), np.array(worst)


# --------------------------------------------------------------------- main ---

def main():
    print("Decision engine - toy example: every pair of sites (budget 2)")
    pairs = [(a, b) for i, a in enumerate(TOY_REACH) for b in list(TOY_REACH)[i + 1:]]
    for pair in pairs:
        total, sh = toy_shares(pair)
        print(f"  {pair[0]}+{pair[1]}  covered={total:5d}  North={sh['North']:.1%}  "
              f"South={sh['South']:.1%}  worst={min(sh.values()):.1%}")
    ranked = sorted(TOY_POP, key=TOY_POP.get, reverse=True)
    naive = []
    for v in ranked:
        if TOY_NEAREST[v] not in naive:
            naive.append(TOY_NEAREST[v])
        if len(naive) == 2:
            break
    print(f"  need ranking picks {naive}: covered={toy_shares(naive)[0]}")
    x, obj = toy_model()
    print(f"  integer program, max coverage: {x}  covered={obj:.0f}")
    x, obj = toy_model(fair=True)
    print(f"  integer program, maximin:      {x}  worst share={obj:.1%}")

    print("\nDecision engine - toy maximin: LP relaxation and branch and bound")
    for label, fix in (("relaxation (no branch)", None), ("branch S3 = 0", {"S3": 0}),
                       ("branch S3 = 1", {"S3": 1})):
        x, obj = toy_model(fair=True, relax=True, fix=fix)
        print(f"  {label:24s} {x}  worst share bound={obj:.1%}")

    region = make_region()
    reach = coverage_table(region)
    pop = region["pop"]
    n_sites = reach.shape[1]
    print("\nScaling up - the synthetic region")
    print(f"  villages={len(pop)}  people={pop.sum():,}  candidate points surveyed="
          f"{region['n_candidates']}  drillable={n_sites}")
    for d in DISTRICTS:
        m = region["district"] == d
        print(f"  district {d}: villages={m.sum():3d}  people={pop[m].sum():7,}  "
              f"median village={int(np.median(pop[m])):4d}  drillable sites="
              f"{(region['site_district'] == d).sum()}")
    reachable = reach.any(axis=1)
    print(f"  villages with at least one drillable site within 30 min: {reachable.sum()} "
          f"({pop[reachable].sum():,} people)")
    print(f"  decision variables: {n_sites} sites + {len(pop)} villages = {n_sites + len(pop)}"
          f"  (Excel's standard Solver allows 200)")
    print(f"  even dropping unreachable villages: {n_sites + reachable.sum()}")
    print(f"  ways to choose {BUDGET} of {n_sites} sites: {comb(n_sites, BUDGET):.2e}")

    print("\nEstimates - from GPS to walking minutes (one village-site pair)")
    km = 1.2
    print(f"  {km} km straight line x detour 1.3 = {km * 1.3:.2f} km of path "
          f"-> {km * 1.3 / WALK_SPEED_KMH * 60:.1f} minutes at {WALK_SPEED_KMH:.0f} km/h; "
          f"in hilly District D (x1.6): {km * 1.6 / WALK_SPEED_KMH * 60:.1f} minutes")
    print(f"  30 minutes reaches {WALK_LIMIT_MIN / 60 * WALK_SPEED_KMH / 1.3:.2f} km straight-line "
          f"(detour 1.3) or {WALK_LIMIT_MIN / 60 * WALK_SPEED_KMH / 1.6:.2f} km (detour 1.6)")

    print("\nEstimates - checking District D's detour factor: staff walk 30 village-site pairs")
    rng = np.random.default_rng(11)
    ratios = 1.6 * rng.lognormal(0, 0.15, 30)          # true paths, unknown to the planner
    mean, sd = ratios.mean(), ratios.std(ddof=1)
    half = 1.96 * sd / np.sqrt(len(ratios))
    print(f"  sample mean={mean:.2f}  sd={sd:.2f}  95% CI={mean - half:.2f} to {mean + half:.2f}")

    print("\nSimulation - five plans for 25 boreholes")
    plans = {}
    plans["need ranking"] = (need_ranking(region, reach), 0.0)
    start = time.perf_counter()
    plans["greedy (most new people)"] = (greedy(region, reach), time.perf_counter() - start)
    chosen, secs, _ = covering_model(region, reach)
    plans["max coverage (ILP)"] = (chosen, secs)
    chosen, secs, best_worst = maximin_then_coverage(region, reach)
    plans["maximin fair (ILP)"] = (chosen, secs)
    middle = 0.20     # a middle ground the councils might choose: every district >= 20%
    chosen, secs, _ = covering_model(region, reach, floor=middle)
    plans[f"middle ground (ILP, floor {middle:.0%})"] = (chosen, secs)
    for name, (chosen, secs) in plans.items():
        total, sh, per_d = summarize(region, reach, chosen)
        print(f"  {name:32s} covered={total:7,} ({total / pop.sum():.1%})  "
              + "  ".join(f"{d}={sh[d]:.0%}" for d in DISTRICTS)
              + f"  worst={min(sh.values()):.1%}  sites/district={[per_d[d] for d in DISTRICTS]}"
              + (f"  {secs:.2f}s" if name.endswith(")") and "ILP" in name else ""))
    naive = plans["need ranking"][0]
    cov = covered_by(reach, naive)
    raw = sum(pop[reach[:, j]].sum() for j in naive)
    print(f"  need ranking: sum of each site's catchment={raw:,} vs people actually covered="
          f"{pop[cov].sum():,} (double counted={raw - pop[cov].sum():,})")

    print("\nScaling up - price of fairness: minimum share every district must reach")
    for floor in (0.0, 0.10, 0.20, 0.30, best_worst - 1e-6):
        chosen, secs, _ = covering_model(region, reach, floor=floor)
        total, sh, per_d = summarize(region, reach, chosen)
        print(f"  floor={floor:5.1%}  covered={total:7,}  worst={min(sh.values()):.1%}  "
              f"sites/district={[per_d[d] for d in DISTRICTS]}  {secs:.2f}s")

    print("\nEstimates - population uncertainty: covered total for the maximin-fair plan")
    fair = plans["maximin fair (ILP)"][0]
    cov = covered_by(reach, fair)
    sd_total = np.sqrt(((0.05 * pop[cov]) ** 2).sum())
    print(f"  covered={pop[cov].sum():,}; if each village count has a 5% standard error "
          f"(about +/-10%), sd of the total={sd_total:,.0f} "
          f"-> 95% CI {pop[cov].sum() - 1.96 * sd_total:,.0f} to {pop[cov].sum() + 1.96 * sd_total:,.0f}")

    print("\nEstimates - sensitivity: re-plan under changed assumptions and compare with the "
          "original plan")
    print("  kept = original sites still chosen; loss = people the original plan misses vs re-plan;")
    print("  worst-share gap = re-planned worst district share minus the original plan's")
    base_cov = plans["max coverage (ILP)"][0]
    base_fair = plans["maximin fair (ILP)"][0]

    def compare(reach2, pop2):
        new_cov, _, _ = covering_model(region, reach2, pop=pop2)
        old_n, new_n = pop2[covered_by(reach2, base_cov)].sum(), pop2[covered_by(reach2, new_cov)].sum()
        region2 = {**region, "pop": pop2}
        new_fair, _, new_worst = maximin_then_coverage(region2, reach2)
        old_worst = min(district_shares(region2, covered_by(reach2, base_fair)).values())
        return (len(base_cov & new_cov), (new_n - old_n) / new_n,
                len(base_fair & new_fair), new_worst - old_worst)

    def show(label, r):
        print(f"  {label:30s} max coverage: kept={r[0]:2d}/25 loss={r[1]:5.1%} | "
              f"maximin fair: kept={r[2]:2d}/25 worst-share gap={r[3]:.1%}")

    for minutes in (25, 35):
        show(f"walking limit {minutes} min", compare(coverage_table(region, limit=minutes), pop))
    for factor in (round(mean - half, 2), round(mean + half, 2)):
        show(f"District D detour {factor}",
             compare(coverage_table(region, detour={**DETOUR, "D": factor}), pop))
    rng = np.random.default_rng(5)
    results = []
    for _ in range(20):
        pop2 = np.round(pop * rng.uniform(0.9, 1.1, len(pop))).astype(int)
        results.append(compare(reach, pop2))
    r = np.array(results)
    print(f"  populations each moved up to 10% (20 draws), averages: max coverage: kept="
          f"{r[:, 0].mean():.1f}/25 (min {r[:, 0].min():.0f}) loss={r[:, 1].mean():.2%} "
          f"(max {r[:, 1].max():.2%}) | maximin fair: kept={r[:, 2].mean():.1f}/25 "
          f"(min {r[:, 2].min():.0f}) worst-share gap={r[:, 3].mean():.2%} "
          f"(max {r[:, 3].max():.2%})")

    print("\nScaling up - dry boreholes and backup sites (maximin-fair plan)")
    lost, recovered, worst = backup_sites(region, reach, fair)
    print(f"  if one chosen site is dry: people lost on average={lost.mean():,.0f} "
          f"(largest {lost.max():,}); best same-district backup recovers on average="
          f"{recovered.mean():,.0f} ({recovered.sum() / lost.sum():.0%} of the loss); "
          f"worst share after the swap: lowest={worst.min():.1%}")
    p_dry = 0.2
    k = np.arange(BUDGET + 1)
    pmf = np.array([comb(BUDGET, i) * p_dry ** i * (1 - p_dry) ** (BUDGET - i) for i in k])
    print(f"  if each borehole has a {p_dry:.0%} chance of coming up dry: expected dry="
          f"{BUDGET * p_dry:.1f}  sd={np.sqrt(BUDGET * p_dry * (1 - p_dry)):.1f}  "
          f"P(8 or more dry)={pmf[8:].sum():.1%}")


if __name__ == "__main__":
    main()
