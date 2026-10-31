"""Case 3 tutorial code: a Stackelberg security game for marine patrols.

Every number quoted in docs/tutorials/03-security-games-marine-patrols.md comes from
running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case3_security_game.py

Needs numpy and PuLP 3 (PuLP ships with the free CBC solver). The program is
illustrative: the zones, fish values, patrol logs and fisher behavior are made up
for teaching. It runs in a few seconds and gives the same output every time.
"""

import numpy as np
import pulp

N_ZONES = 40        # zones in the marine protected area, numbered north (0) to south (39)
ZONES_PER_DAY = 6   # 2 boats x 3 zones each
PENALTY = 4.0       # what a crew loses if caught: nets confiscated plus a fine (in fish-value units)


# ---------------------------------------------------------------- Chapter 3 ---

def rate_with_margin(incidents, hours):
    """Incidents per patrol hour, with a rough 95% margin of error.

    Counts of rare events behave like a Poisson count, whose spread is about
    sqrt(count). So the margin on the rate is 1.96 * sqrt(k) / hours.
    For a zone with zero incidents, the "rule of three" gives an upper bound of 3 / hours.
    """
    rate = incidents / hours
    if incidents == 0:
        return rate, 0.0, 3.0 / hours
    margin = 1.96 * np.sqrt(incidents) / hours
    return rate, max(0.0, rate - margin), rate + margin


def make_patrol_history(seed=11):
    """Three years of made-up SMART logs: patrol hours and recorded incidents per zone.

    The trust patrolled the northern reef (zones 0-7) heavily. Fishers moved south,
    so the true activity is now LOW in the north and HIGHER in the south. Incidents
    are only recorded where boats go, and a boat in the zone spots a net only half
    the time (detection probability 0.5).
    """
    rng = np.random.default_rng(seed)
    total_hours = 12_000
    effort_weight = np.ones(N_ZONES)
    effort_weight[:8] = 10.0                   # the northern reef, patrolled every morning
    effort_weight[[22, 27, 31, 35, 38]] = 0.3  # far zones, rarely visited (fuel)
    hours = np.round(total_hours * effort_weight / effort_weight.sum())

    # True nets present per hour of searching (unknown to the trust).
    activity = np.full(N_ZONES, 0.108)
    activity[:8] = 0.054                       # deterred by heavy patrols
    activity[[22, 27, 31, 35, 38]] = 0.252     # nets moved to where boats rarely go
    activity[30:] += 0.054                     # the south generally busier
    detection = 0.5
    incidents = rng.poisson(hours * activity * detection)
    return hours, incidents, activity, detection


# ---------------------------------------------------------------- Chapter 4 ---

def attacker_utility(coverage, gain, penalty=PENALTY):
    """Fishers' expected payoff in each zone: keep `gain` if unpatrolled, lose `penalty` if caught."""
    coverage = np.asarray(coverage, dtype=float)
    return (1 - coverage) * gain - coverage * penalty


def multiple_lps(att_gain, att_loss, def_gain, def_loss, resources):
    """Strong Stackelberg equilibrium by the 'multiple LPs' method.

    For each zone t: find the coverage that is best for the defender, subject to
    zone t being (one of) the fishers' best choices. Keep the best of those plans.
    att_loss and def_loss are negative numbers (losses).
    """
    n = len(att_gain)
    best = None
    for t in range(n):
        prob = pulp.LpProblem(f"target_{t}", pulp.LpMaximize)
        c = [pulp.LpVariable(f"c{i}", lowBound=0, upBound=1) for i in range(n)]

        def att_eu(i):
            return c[i] * att_loss[i] + (1 - c[i]) * att_gain[i]

        prob += c[t] * def_gain[t] + (1 - c[t]) * def_loss[t]     # defender's payoff if zone t is hit
        prob += pulp.lpSum(c) == resources                       # all patrol capacity is used
        for i in range(n):
            prob += att_eu(t) >= att_eu(i)                       # zone t is a best response
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[status] != "Optimal":
            continue
        value = pulp.value(prob.objective)
        if best is None or value > best[0] + 1e-9:
            best = (value, t, [c[i].value() for i in range(n)])
    return best


def minimax_coverage(gain, resources, penalty=PENALTY, upper=None, lower=None):
    """Zero-sum version: choose coverage to make the fishers' BEST zone as poor as possible.

    minimize U  subject to  (1 - c_i) * gain_i - c_i * penalty <= U  for every zone,
                            sum(c) = resources,  lower_i <= c_i <= upper_i.
    """
    n = len(gain)
    upper = np.ones(n) if upper is None else upper
    lower = np.zeros(n) if lower is None else lower
    prob = pulp.LpProblem("minimax", pulp.LpMinimize)
    c = [pulp.LpVariable(f"c{i}", lowBound=float(lower[i]), upBound=float(upper[i])) for i in range(n)]
    U = pulp.LpVariable("U")
    prob += U
    prob += pulp.lpSum(c) == resources
    for i in range(n):
        prob += (1 - c[i]) * float(gain[i]) - c[i] * penalty <= U
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    return np.array([ci.value() for ci in c]), U.value()


# -------------------------------------------------------------- Chapter 4.5 ---

def zone_values(seed=5):
    """Made-up value of a night's illegal catch in each zone (fish-value units)."""
    rng = np.random.default_rng(seed)
    gain = np.round(rng.uniform(1.0, 7.0, N_ZONES), 1)
    gain[:8] = np.round(rng.uniform(7.0, 10.0, 8), 1)          # the northern reef is richest
    gain[[22, 27, 31, 35, 38]] = np.round(rng.uniform(6.0, 9.0, 5), 1)  # rich but far
    return gain


def comb_sample(coverage, rng):
    """Pick exactly round(sum(coverage)) zones so zone i is picked with probability coverage[i].

    Lay the probabilities end to end on a line of length 6. Drop a comb with 6 teeth
    one unit apart, starting at a random point in [0, 1). Each tooth lands in one zone.
    Because no coverage exceeds 1, no zone can be hit by two teeth.
    """
    edges = np.concatenate([[0.0], np.cumsum(coverage)])
    k = int(round(edges[-1]))
    teeth = rng.random() + np.arange(k)
    return np.searchsorted(edges, teeth, side="right") - 1


# ---------------------------------------------------------------- Chapter 5 ---

def simulate(policy, gain, coverage, hist_incidents, days=364, crews=5,
             rationality=1.5, seed=21):
    """One year of patrols against fishers who learn from what they see at the jetty.

    Each day 5 crews decide where to set nets, or to stay home (payoff 0). Each crew's
    belief that zone i is patrolled today = half the share of the last 28 days the zone
    was patrolled, plus half the share of the same weekday over the last 4 weeks (so a
    weekly pattern is spotted). Crews pick zones with higher expected payoff more often
    (a 'softmax' choice with the given rationality). A crew in a patrolled zone is caught;
    otherwise it takes the zone's fish value.
    """
    rng = np.random.default_rng(seed)
    warmup = 28
    seen = np.zeros((days + warmup, N_ZONES))        # 1 if the zone was patrolled that day
    incidents = hist_incidents.astype(float).copy()  # for the hotspot policy
    hotspot = np.argsort(-incidents, kind="stable")[:ZONES_PER_DAY]
    fish_taken = caught = stayed_home = 0.0

    for day in range(days + warmup):
        if policy == "fixed rotation":               # same weekly paper schedule every week
            w = day % 7
            zones = np.arange(6 * w, 6 * w + 6) % N_ZONES
        elif policy == "hotspot":                    # most recorded incidents, refreshed monthly
            if day % 30 == 0:
                hotspot = np.argsort(-incidents, kind="stable")[:ZONES_PER_DAY]
            zones = hotspot
        elif policy == "uniform random":
            zones = rng.choice(N_ZONES, ZONES_PER_DAY, replace=False)
        elif policy == "game (randomized)":
            zones = comb_sample(coverage, rng)
        else:                                        # "no patrols"
            zones = np.array([], dtype=int)
        seen[day, zones] = 1

        if day < warmup:
            continue
        recent = seen[day - 28:day].mean(axis=0)
        same_weekday = seen[[day - 7, day - 14, day - 21, day - 28]].mean(axis=0)
        belief = 0.5 * recent + 0.5 * same_weekday
        eu = np.concatenate([[0.0], attacker_utility(belief, gain)])   # option 0 = stay home
        p = np.exp(rationality * (eu - eu.max()))
        p /= p.sum()
        choices = rng.choice(N_ZONES + 1, crews, p=p)
        for ch in choices:
            if ch == 0:
                stayed_home += 1
            elif seen[day, ch - 1]:
                caught += 1
                incidents[ch - 1] += 1
            else:
                fish_taken += gain[ch - 1]
    return fish_taken, caught, stayed_home


def main():
    np.set_printoptions(precision=3, suppress=True)

    # ---------------- Chapter 3
    hours, inc, activity, d = make_patrol_history()
    rate = inc / hours
    print("Chapter 3 - simulated 3 years of SMART logs, 40 zones")
    print(f"  total patrol hours={hours.sum():.0f}, total incidents={inc.sum()}, "
          f"share of hours on northern reef (zones 0-7)={hours[:8].sum() / hours.sum():.2f}, "
          f"share of incidents there={inc[:8].sum() / inc.sum():.2f}")
    top = 5
    by_count = np.argsort(-inc, kind="stable")[:top]
    by_rate = np.argsort(-rate, kind="stable")[:top]
    by_truth = np.argsort(-activity, kind="stable")[:top]
    print(f"  top {top} by raw count : {sorted(by_count.tolist())}")
    print(f"  top {top} by rate/hour : {sorted(by_rate.tolist())}")
    print(f"  top {top} by true risk : {sorted(by_truth.tolist())}")
    for z in (3, 27, 31, 38):
        r, lo, hi = rate_with_margin(inc[z], hours[z])
        print(f"  zone {z:2d}: hours={hours[z]:5.0f} incidents={inc[z]:3d} rate={r:.3f} "
              f"95% range=({lo:.3f}, {hi:.3f})  divided by detection 0.5={r / d:.3f}  "
              f"true nets/hour={activity[z]:.3f}")
    r, lo, hi = rate_with_margin(0, 12)
    print(f"  a zone with 0 incidents in 12 hours: rate={r:.3f}, rule-of-three upper bound={hi:.3f}")

    # ---------------- Chapter 4: toy game
    print("\nChapter 4 - toy game: 3 zones, 1 boat (coverage sums to 1), penalty if caught = 4")
    names = ["North reef", "Central bank", "South bay"]
    toy_gain = np.array([8.0, 4.0, 2.0])
    plans = {
        "always North reef": [1, 0, 0],
        "uniform random": [1 / 3, 1 / 3, 1 / 3],
        "proportional to value": toy_gain / toy_gain.sum(),
    }
    for label, cov in plans.items():
        eu = attacker_utility(cov, toy_gain)
        print(f"  {label:22s} coverage={np.round(cov, 3)}  fishers' payoff by zone={np.round(eu, 3)}  "
              f"best={eu.max():.3f} at {names[int(np.argmax(eu))]}")
    # Predictable rotation: fishers know today's zone and pick the best uncovered one.
    rot = [float(max(toy_gain[j] for j in range(3) if j != today)) for today in range(3)]
    print(f"  {'predictable rotation':22s} fishers' best payoff each day={rot}  average={np.mean(rot):.3f}")

    # Hand solution: c_i = (G_i - U) / (G_i + 4), sum c_i = 1  ->  U = (sum G/(G+4) - 1) / sum 1/(G+4)
    a = (toy_gain / (toy_gain + PENALTY)).sum()
    b = (1 / (toy_gain + PENALTY)).sum()
    U = (a - 1) / b
    hand = (toy_gain - U) / (toy_gain + PENALTY)
    print(f"  hand solution: sum G/(G+4)={a:.4f}, sum 1/(G+4)={b:.4f}, U={U:.4f}, coverage={np.round(hand, 4)}")
    print(f"  fish lost by the trust if fishers hit each zone: {np.round((1 - hand) * toy_gain, 3)}")

    value, target, cov = multiple_lps(att_gain=toy_gain, att_loss=-PENALTY * np.ones(3),
                                      def_gain=PENALTY * np.ones(3), def_loss=-toy_gain, resources=1)
    print(f"  multiple LPs: coverage={np.round(cov, 4)}  defender payoff={value:.4f}  "
          f"fishers' payoff by zone={np.round(attacker_utility(cov, toy_gain), 4)}")
    cov2, U2 = minimax_coverage(toy_gain, 1)
    print(f"  minimax LP  : coverage={np.round(cov2, 4)}  fishers' best payoff U={U2:.4f}")

    # ---------------- Chapter 4.5: 40 zones
    gain = zone_values()
    print("\nChapter 4.5 - 40 zones, 6 zone-visits per day")
    print(f"  zone values: min={gain.min():.1f} max={gain.max():.1f} mean={gain.mean():.2f}")
    coverage, U40 = minimax_coverage(gain, ZONES_PER_DAY)
    covered = coverage > 1e-6
    print(f"  equilibrium: fishers' best payoff U={U40:.3f}; zones with coverage > 0: {covered.sum()}; "
          f"sum of coverage={coverage.sum():.2f}; highest coverage={coverage.max():.3f} (zone {int(np.argmax(coverage))})")
    print(f"  zones never patrolled have value <= {gain[~covered].max():.1f}; "
          f"lowest-value covered zone has value {gain[covered].min():.1f}")
    for z in (0, 3, 22, 31, 12):
        print(f"    zone {z:2d}: value={gain[z]:.1f} coverage={coverage[z]:.3f}")

    far = np.array([22, 27, 31, 35, 38])
    cap = np.ones(N_ZONES)
    cap[far] = 0.15
    cov_cap, U_cap = minimax_coverage(gain, ZONES_PER_DAY, upper=cap)
    print(f"  far zones {far.tolist()} have values {gain[far].tolist()}")
    print(f"  with a fuel cap of 0.15 on the 5 far zones: U={U_cap:.3f} (was {U40:.3f}); "
          f"zones with coverage > 0: {(cov_cap > 1e-6).sum()}")
    floor = np.full(N_ZONES, 0.03)
    cov_floor, U_floor = minimax_coverage(gain, ZONES_PER_DAY, lower=floor)
    print(f"  with a learning floor of 0.03 in every zone: U={U_floor:.3f} (was {U40:.3f})")

    rng = np.random.default_rng(1)
    first_days = [sorted(comb_sample(coverage, rng).tolist()) for _ in range(3)]
    print(f"  comb sampling, first three days: {first_days}")
    counts = np.zeros(N_ZONES)
    n_days = 20_000
    for _ in range(n_days):
        picked = comb_sample(coverage, rng)
        assert len(picked) == ZONES_PER_DAY and len(set(picked.tolist())) == ZONES_PER_DAY
        counts[picked] += 1
    print(f"  over {n_days:,} sampled days: every day had exactly 6 different zones; "
          f"largest gap between how often a zone was picked and its coverage={np.abs(counts / n_days - coverage).max():.3f}")

    # ---------------- Chapter 5
    print("\nChapter 5 - one-year simulation, 5 crews a day, fishers who watch and adapt")
    print(f"  {'policy':18s} {'fish taken':>10s} {'vs no patrols':>14s} {'crews caught':>13s} {'stayed home':>12s}")
    baseline = None
    for policy in ("no patrols", "fixed rotation", "hotspot", "uniform random", "game (randomized)"):
        f, c, s = simulate(policy, gain, coverage, inc)
        baseline = f if baseline is None else baseline
        print(f"  {policy:18s} {f:10.0f} {f / baseline - 1:+14.1%} {c:13.0f} {s:12.0f}")
    print(f"  (5 crews x 364 days = {5 * 364} fishing trips per policy)")


if __name__ == "__main__":
    main()
