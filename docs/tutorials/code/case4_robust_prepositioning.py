"""Case 4 tutorial code: two-stage robust pre-positioning of cyclone relief kits.

Every number quoted in docs/tutorials/04-robust-optimization-cyclone-prepositioning.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case4_robust_prepositioning.py

It needs numpy and PuLP 3 (which ships with the free CBC solver). The program is
illustrative: the coast, the populations, the 8 "historical" storms, the road rules
and the 10 stress scenarios are all made up for teaching.

Four ways to decide how many kits each warehouse holds before the season:
  A. average storm   - stock in proportion to the average storm's damage
  B. expected value  - best average over the 8 recorded storms (stochastic programming)
  C. robust          - best worst case over every storm we consider possible (minimax)
  D. distributionally robust (DRO) - best average under the least favorable
     re-weighting of history that stays "close" to the 8 storms
"""

import numpy as np
import pulp


def solve(prob):
    """Solve a PuLP problem with the bundled CBC solver and insist on an optimum."""
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    assert pulp.LpStatus[prob.status] == "Optimal", pulp.LpStatus[prob.status]
    return pulp.value(prob.objective)


# ===================================================== Decision engine: toy ===
# Three zones on the coast, one warehouse in each. 120 kits in total.
# Every storm leaves 80 families needing a kit in the zone where it lands, and it
# floods the coastal road on both sides, so only that zone's own warehouse can
# reach them within 2 days. Of 8 recorded storms: 1 North, 5 Center, 2 South.

TOY_ZONES = ["North", "Center", "South"]
TOY_KITS, TOY_NEED = 120, 80
TOY_COUNTS = np.array([1, 5, 2])
TOY_P = TOY_COUNTS / TOY_COUNTS.sum()


def toy_unmet(x):
    """Families left without a kit in each landfall zone, for stock x."""
    return np.maximum(0, TOY_NEED - np.asarray(x, dtype=float))


def toy_worst_reweighting(unmet, eps):
    """Worst average unmet need when up to eps of probability may move, at a cost of
    one 'zone-step' per zone moved (eps = 0.25 means two of eight storms moved one zone).

    Small linear program: how much of zone i's history moves to zone j.
    """
    prob = pulp.LpProblem("toy_worst_reweighting", pulp.LpMaximize)
    move = {(i, j): pulp.LpVariable(f"m_{i}_{j}", lowBound=0) for i in range(3) for j in range(3)}
    prob += pulp.lpSum(move[i, j] * unmet[j] for i in range(3) for j in range(3))
    for i in range(3):
        prob += pulp.lpSum(move[i, j] for j in range(3)) == TOY_P[i]
    prob += pulp.lpSum(move[i, j] * abs(i - j) for i in range(3) for j in range(3)) <= eps
    value = solve(prob)
    q = [sum(move[i, j].value() for i in range(3)) for j in range(3)]
    return value, np.array(q)


def toy_plan(method, eps=0.25):
    """Stock for the three warehouses under each method, as a small linear program."""
    prob = pulp.LpProblem(f"toy_{method}", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{z}", lowBound=0) for z in range(3)]
    u = [pulp.LpVariable(f"unmet_{z}", lowBound=0) for z in range(3)]
    prob += pulp.lpSum(x) == TOY_KITS
    for z in range(3):
        prob += u[z] >= TOY_NEED - x[z]               # unmet = need - stock, if positive
    if method == "expected":
        prob += pulp.lpSum(TOY_P[z] * u[z] for z in range(3))
    elif method == "robust":
        t = pulp.LpVariable("worst")
        for z in range(3):
            prob += t >= u[z]
        prob += t
    elif method == "dro":
        # Worst case over re-weightings, rewritten (by LP duality) as a minimization:
        # lam = price of one zone-step of moved probability, s[i] = worst loss that
        # history in zone i can be moved to, after paying for the move.
        lam = pulp.LpVariable("lam", lowBound=0)
        s = [pulp.LpVariable(f"s_{i}") for i in range(3)]
        for i in range(3):
            for j in range(3):
                prob += s[i] >= u[j] - lam * abs(i - j)
        prob += lam * eps + pulp.lpSum(TOY_P[i] * s[i] for i in range(3))
    solve(prob)
    return np.array([v.value() for v in x])


# =================================================== Simulation: full model ===
# Five coastal zones, west (Z1) to east (Z5). Each zone has a coastal and an inland
# shelter area. Warehouses W1..W5 sit one per zone; W6 is an inland hub behind Z3.

ZONES = [1, 2, 3, 4, 5]
AREAS = [(z, kind) for z in ZONES for kind in ("coast", "inland")]      # 10 areas
POP = {"coast": 45_000, "inland": 30_000}           # families living in each area
EXPOSURE = {"coast": 1.0, "inland": 0.5}            # inland areas are hit half as hard
HIT = {0: 0.12, 1: 0.04}                            # share hit per severity point, by distance
WAREHOUSES = ["W1", "W2", "W3", "W4", "W5", "W6"]
HOME = {"W1": 1, "W2": 2, "W3": 3, "W4": 4, "W5": 5}  # W6 is inland, not on the coast
TOTAL_KITS = 30_000

# Illustrative record of 8 severe storms: (landfall zone, severity 1-3).
HISTORY = [(3, 2), (2, 3), (3, 1), (4, 2), (3, 3), (2, 2), (4, 1), (3, 2)]

# Illustrative workshop stress set, never shown to the planning models:
# (name, landfall, severity, extra failures)
STRESS = [
    ("west end, severe",            1, 3, []),
    ("east end, severe",            5, 3, []),
    ("west end, moderate",          1, 2, []),
    ("east end, moderate",          5, 2, []),
    ("center, stronger than record", 3, 4, []),
    ("east end, stronger than record", 5, 4, []),
    ("Z2 severe, inland road out",  2, 3, ["inland"]),
    ("Z4 severe, inland road out",  4, 3, ["inland"]),
    ("Z2 moderate, extra bridge out", 2, 2, ["B34"]),
    ("Z4 moderate, extra bridge out", 4, 2, ["B12"]),
]


def affected(landfall, severity):
    """Families needing a kit in each area for a storm: population x share hit."""
    need = {}
    for z, kind in AREAS:
        d = abs(z - landfall)
        share = HIT.get(d, 0.0) * severity * EXPOSURE[kind]
        need[(z, kind)] = POP[kind] * min(1.0, share)
    return need


def failed_bridges(landfall, severity, extra=()):
    """Bridge 'B23' joins zones 2 and 3. Severity 2+ cuts the bridges on both sides of
    landfall; severity 4 also cuts the next ones out. 'inland' = the inland road."""
    out = set(extra)
    reach = 0 if severity < 2 else (1 if severity < 4 else 2)
    for k in range(1, 5):                    # bridge between zone k and k+1
        if (landfall - reach <= k < landfall + reach):
            out.add(f"B{k}{k + 1}")
    return out


def usable_links(failed):
    """(warehouse, area) pairs a truck can cover within 2 days on the surviving roads."""
    links = []
    for w in WAREHOUSES:
        for z, kind in AREAS:
            if w == "W6":                      # inland hub: zones 2-4 by the inland road
                ok = 2 <= z <= 4 and "inland" not in failed
            else:                              # coastal: own zone and next zones, via a bridge
                h = HOME[w]
                lo, hi = min(h, z), max(h, z)
                ok = hi - lo <= 1 and all(f"B{k}{k + 1}" not in failed for k in range(lo, hi))
            if ok:
                links.append((w, (z, kind)))
    return links


def scenario(landfall, severity, extra=()):
    return {"need": affected(landfall, severity),
            "links": usable_links(failed_bridges(landfall, severity, extra)),
            "landfall": landfall, "severity": severity}


def add_dispatch(prob, x, sc, tag):
    """Stage 2 inside a planning model: ship kits over the surviving roads.
    Returns the unmet SHARE of affected families (0 = everyone reached)."""
    f = {lk: pulp.LpVariable(f"f_{tag}_{lk[0]}_{lk[1][0]}{lk[1][1]}", lowBound=0)
         for lk in sc["links"]}
    for w in WAREHOUSES:
        prob += pulp.lpSum(v for (ww, _), v in f.items() if ww == w) <= x[w]
    for a in AREAS:
        prob += pulp.lpSum(v for (_, aa), v in f.items() if aa == a) <= sc["need"][a]
    total = sum(sc["need"].values())
    return 1 - pulp.lpSum(f.values()) / total


def reach(stock, sc):
    """Evaluate a fixed stock layout on one storm: best dispatch, share reached in 2 days.
    Also returns the shipments (the 'dispatch card')."""
    prob = pulp.LpProblem("dispatch", pulp.LpMinimize)
    unmet = add_dispatch(prob, stock, sc, "e")
    prob += unmet
    solve(prob)
    ships = {(v.name): v.value() for v in prob.variables() if v.value() and v.value() > 0.5}
    return 1 - pulp.value(unmet), ships


def planning_support():
    """Every storm the robust models may consider: each recorded storm moved to every
    landfall zone (same severity). Key = (landfall, severity)."""
    return sorted({(z, s) for _, s in HISTORY for z in ZONES})


def average_storm_plan(total=TOTAL_KITS):
    """A: average the 8 storms' damage per zone, stock each zone's warehouse in proportion."""
    avg = np.zeros(5)
    for lf, sev in HISTORY:
        need = affected(lf, sev)
        for (z, _), n in need.items():
            avg[z - 1] += n / len(HISTORY)
    stock = {w: 0.0 for w in WAREHOUSES}
    for w, z in HOME.items():
        stock[w] = total * avg[z - 1] / avg.sum()
    return stock


def plan(method, eps=0.5, total=TOTAL_KITS, tie=0.01):
    """B, C or D as one linear program. Stage 1 = stock x[w]; stage 2 = dispatch per storm.
    Several layouts often score exactly the same; `tie` adds a tiny weight on the
    average and the worst case over the planning storms to choose among them."""
    prob = pulp.LpProblem(f"plan_{method}", pulp.LpMinimize)
    x = {w: pulp.LpVariable(f"x_{w}", lowBound=0) for w in WAREHOUSES}
    prob += pulp.lpSum(x.values()) == total
    keys = planning_support()
    U = {k: add_dispatch(prob, x, scenario(*k), f"{k[0]}{k[1]}") for k in keys}
    avg_hist = pulp.lpSum(U[h] for h in HISTORY) / len(HISTORY)
    worst = pulp.LpVariable("worst")
    for k in keys:
        prob += worst >= U[k]
    if method == "expected":
        prob += avg_hist + tie * (avg_hist + worst)
    elif method == "robust":
        prob += worst + tie * (avg_hist + worst)
    elif method == "dro":
        # Wasserstein ball: probability may move between landfall zones at a cost of
        # |zones moved|; eps is the average shift allowed per storm. Dual form:
        lam = pulp.LpVariable("lam", lowBound=0)
        s = [pulp.LpVariable(f"s_{i}") for i in range(len(HISTORY))]
        for i, (lf, sev) in enumerate(HISTORY):
            for z in ZONES:
                prob += s[i] >= U[(z, sev)] - lam * abs(z - lf)
        prob += lam * eps + pulp.lpSum(s) / len(HISTORY) + tie * (avg_hist + worst)
    solve(prob)
    return {w: max(0.0, x[w].value()) for w in WAREHOUSES}


def min_kits(target, which):
    """Smallest total stock reaching `target` share: on average over the 8 storms,
    in each of the 8 storms, or in every planning storm (any landfall zone)."""
    prob = pulp.LpProblem(f"min_kits_{which.replace(' ', '_')}", pulp.LpMinimize)
    x = {w: pulp.LpVariable(f"x_{w}", lowBound=0) for w in WAREHOUSES}
    prob += pulp.lpSum(x.values())
    keys = HISTORY if which != "every zone" else planning_support()
    U = {k: add_dispatch(prob, x, scenario(*k), f"{k[0]}{k[1]}") for k in sorted(set(keys))}
    if which == "average":
        prob += pulp.lpSum(U[h] for h in HISTORY) / len(HISTORY) <= 1 - target
    else:
        for k in sorted(set(keys)):
            prob += U[k] <= 1 - target
    return solve(prob)


def evaluate(stock):
    hist = [reach(stock, scenario(*h))[0] for h in HISTORY]
    stress = [reach(stock, scenario(lf, sev, extra))[0] for _, lf, sev, extra in STRESS]
    return np.array(hist), np.array(stress)


def wilson(k, n, z=1.96):
    """95% Wilson interval for a proportion; behaves sensibly when k = 0 or n is small."""
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, center - half), min(1.0, center + half)


def main():
    # ------------------------------------------------------------ Estimates ---
    print("Estimates - landfall zones of the 8 recorded storms")
    counts = [sum(1 for lf, _ in HISTORY if lf == z) for z in ZONES]
    for z, k in zip(ZONES, counts):
        lo, hi = wilson(k, 8)
        wald = 1.96 * np.sqrt((k / 8) * (1 - k / 8) / 8)
        print(f"  Z{z}: {k}/8 = {k / 8:.3f}   Wald 95% CI=({max(0, k / 8 - wald):.3f}, "
              f"{min(1, k / 8 + wald):.3f})   Wilson 95% CI=({lo:.3f}, {hi:.3f})")
    print(f"  rule of three for a zone never hit: upper bound ~ 3/8 = {3 / 8:.3f}")

    # ------------------------------------------------------ Decision engine ---
    print("\nDecision engine - toy: 3 warehouses, 120 kits, 80 families per storm, "
          "history N/C/S = 1/5/2 of 8")
    avg_need = TOY_P * TOY_NEED
    toy = {
        "A average storm": TOY_KITS * avg_need / avg_need.sum(),
        "B expected value": toy_plan("expected"),
        "C robust (minimax)": toy_plan("robust"),
        "D DRO (eps=0.25)": toy_plan("dro", 0.25),
    }
    print(f"  average storm needs N/C/S = {np.round(avg_need, 2)}")
    for name, x in toy.items():
        u = toy_unmet(x)
        dro_val, q = toy_worst_reweighting(u, 0.25)
        print(f"  {name:20s} stock={np.round(x, 1)}  unmet by landfall={np.round(u, 1)}  "
              f"expected={TOY_P @ u:6.2f}  worst={u.max():5.1f}  "
              f"worst re-weighted avg={dro_val:6.2f} (q={np.round(q * 8, 2)}/8)")

    # ----------------------------------------------------------- Simulation ---
    print("\nSimulation - full model: 6 warehouses, 30,000 kits, 10 shelter areas")
    sizes = sorted({round(sum(affected(lf, s).values())) for lf, s in HISTORY})
    print(f"  families needing a kit per recorded storm, by severity: {sizes}")
    print(f"  planning storms for robust/DRO (zone, severity): {len(planning_support())}")

    plans = {
        "A average storm": average_storm_plan(),
        "B expected value": plan("expected"),
        "C robust": plan("robust"),
        "D DRO eps=0.5": plan("dro", eps=0.5),
    }
    print("\n  Stock per warehouse (kits)")
    print("  " + " " * 18 + "".join(f"{w:>7s}" for w in WAREHOUSES))
    for name, st in plans.items():
        print(f"  {name:18s}" + "".join(f"{st[w]:7.0f}" for w in WAREHOUSES))

    print("\n  Share of affected families reached within 2 days")
    print("  " + " " * 18 + "  8 storms: avg  worst   | 10 stress: avg  worst")
    for name, st in plans.items():
        h, s = evaluate(st)
        print(f"  {name:18s}         {h.mean():.3f}  {h.min():.3f}   |            "
              f"{s.mean():.3f}  {s.min():.3f}")

    print("\n  Stress scenarios one by one (share reached)")
    evals = {name: evaluate(st)[1] for name, st in plans.items()}
    for i, (label, lf, sev, extra) in enumerate(STRESS):
        print(f"  {label:32s}" + "".join(f"  {name[0]}={evals[name][i]:.2f}" for name in plans))

    print("\n  Choosing how robust to be: DRO radius eps (average zone-shift per storm)")
    dial = [("eps=0 (plan B)", plans["B expected value"])]          # eps = 0 is plan B
    dial += [(f"eps={eps}", plan("dro", eps=eps)) for eps in (0.25, 0.5)]
    dial += [("robust (plan C)", plans["C robust"])]                 # most protective setting
    for label, st in dial:
        h, s = evaluate(st)
        any_zone = min(reach(st, scenario(*k))[0] for k in planning_support())
        print(f"  {label:15s} W1={st['W1']:5.0f} W3={st['W3']:5.0f} W5={st['W5']:5.0f} "
              f"W6={st['W6']:5.0f}  8 storms avg={h.mean():.3f} worst={h.min():.3f}  "
              f"any zone worst={any_zone:.3f}  stress avg={s.mean():.3f} worst={s.min():.3f}")

    print("\n  Price of robustness in kits: smallest stock reaching 90% ...")
    for which in ("average", "each storm", "every zone"):
        print(f"  {which:11s}: {min_kits(0.90, which):8.0f} kits")

    print("\n  Dispatch card, plan D, landfall Z1 severity 3 (bridge B12 out)")
    share, ships = reach(plans["D DRO eps=0.5"], scenario(1, 3))
    for name, q in sorted(ships.items()):
        _, _, w, area = name.split("_")
        print(f"    {w} -> zone {area[0]} {area[1:]:6s} {q:7.0f} kits")
    print(f"    share reached within 2 days = {share:.3f}")


if __name__ == "__main__":
    main()
