"""Case 7 tutorial code: counting a participatory budget vote by the method of equal shares.

Every number quoted in docs/tutorials/07-participatory-budgeting-neighborhood-fund.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case7_equal_shares.py

It needs only numpy. The method of equal shares is written out from scratch so every
step is visible (in practice you would use pabutools or the tools at equalshares.net).
The neighborhood, projects and ballots are synthetic, generated with fixed random
seeds; they are made up for teaching. Only the run time changes from run to run.
"""

import time

import numpy as np

BUDGET = 250_000                     # the neighborhood fund, per year
AREAS = ["North", "West", "South", "East"]


# ------------------------------------------------------------- Counting rules ---
# A ballot sheet is a 0/1 matrix: one row per ballot, one column per project,
# 1 = "ticked". That is exactly the clerk's Excel sheet.

def greedy(approvals, costs, budget):
    """The standard count: most votes first, skip what no longer fits, stop when done."""
    votes = approvals.sum(axis=0)
    order = np.lexsort((costs, -votes))          # most votes first; ties -> cheaper first
    funded, left = [], budget
    for p in order:
        if votes[p] > 0 and costs[p] <= left:
            funded.append(int(p))
            left -= costs[p]
    return funded


def greedy_envelopes(approvals, costs, budget, area_of_project, envelope):
    """The spreadsheet guard: split the budget into one envelope per area, run the greedy
    count inside each area's envelope, then spend what is left by the greedy count overall."""
    funded = []
    for a, amount in enumerate(envelope):
        own = np.flatnonzero(area_of_project == a)
        funded += [int(own[p]) for p in greedy(approvals[:, own], costs[own], amount)]
    rest = approvals.copy()
    rest[:, funded] = False                            # already funded: take off the ballot
    return funded + greedy(rest, costs, budget - costs[funded].sum())


def price_per_supporter(money, cost):
    """Smallest rho such that each supporter pays min(their money, rho) and together they
    pay `cost`. Returns None if all their money together is not enough."""
    if money.sum() < cost - 1e-9:
        return None
    m = np.sort(money)
    k = len(m)
    # Try "the j poorest supporters pay everything they have, the other k-j split the
    # rest equally". The right j is the first one where that equal split is no more
    # than what the (j+1)-th poorest supporter can afford.
    paid_in_full = np.concatenate(([0.0], np.cumsum(m)[:-1]))
    rho = (cost - paid_in_full) / (k - np.arange(k))
    j = int(np.argmax(rho <= m + 1e-9))
    return float(rho[j])


def equal_shares(approvals, costs, budget, per_voter=None, trace=None):
    """Method of equal shares (approval ballots, one point per funded approved project).

    Each voter starts with an equal share of the budget. Repeatedly fund the project whose
    supporters can pay for it with the lowest price per supporter (rho); each supporter
    pays rho, or everything they have left if that is less. Stop when no project can be
    paid for by its own supporters."""
    n, m = approvals.shape
    money = np.full(n, budget / n if per_voter is None else per_voter, dtype=float)
    funded = []
    while True:
        best, best_rho = None, np.inf
        for p in range(m):
            if p in funded:
                continue
            sup = np.flatnonzero(approvals[:, p])
            if len(sup) == 0:
                continue
            rho = price_per_supporter(money[sup], costs[p])
            # lowest price wins; an exact tie goes to the lower project number here
            # (a real count should publish its tie-break, e.g. a lottery)
            if rho is not None and (rho < best_rho - 1e-9):
                best, best_rho = p, rho
        if best is None:
            return funded, money
        sup = np.flatnonzero(approvals[:, best])
        money[sup] -= np.minimum(money[sup], best_rho)
        funded.append(best)
        if trace is not None:
            trace.append((best, best_rho, money.copy()))


def equal_shares_completed(approvals, costs, budget):
    """Equal shares plus the two usual ways of spending what it leaves over:
    1. raise every voter's starting share and keep the largest raise whose result still
       fits the real budget (searched in 10% steps, then 1% steps);
    2. fill any remaining money greedily by votes.
    Returns the funded list and the raise used, in percent."""
    n = approvals.shape[0]
    fair = budget / n

    def fits(pct):
        trial, _ = equal_shares(approvals, costs, budget, per_voter=fair * (1 + pct / 100))
        return trial if costs[trial].sum() <= budget else None

    funded, raise_pct = equal_shares(approvals, costs, budget)[0], 0
    for step in (10, 1):                       # coarse search, then fine search
        while (trial := fits(raise_pct + step)) is not None:
            funded, raise_pct = trial, raise_pct + step
    left = budget - costs[funded].sum()
    votes = approvals.sum(axis=0)
    for p in np.lexsort((costs, -votes)):
        if p not in funded and votes[p] > 0 and costs[p] <= left:
            funded.append(int(p))
            left -= costs[p]
    return funded, raise_pct


def jr_failures(approvals, costs, budget, funded):
    """Fair-share test (justified representation). A failure is a project whose supporters
    who got NOTHING they voted for could, with their equal shares alone, pay for it."""
    n = approvals.shape[0]
    has_one = approvals[:, funded].any(axis=1) if funded else np.zeros(n, bool)
    fails = []
    for p in range(approvals.shape[1]):
        if p in funded:
            continue
        unserved = approvals[:, p] & ~has_one
        if unserved.sum() * budget / n >= costs[p]:
            fails.append(p)
    return fails


# ---------------------------------------------------------- Decision engine ---
# The toy vote: 10 voters in 3 groups, 6 projects, a $100,000 budget.

def toy():
    groups = ["North"] * 5 + ["West"] * 3 + ["East"] * 2
    names = ["A shared path (N+W)", "B playground (N)", "C lighting (N)",
             "D bike racks (W)", "E benches (E)", "F trees (E)"]
    costs = np.array([24_000, 40_000, 30_000, 21_000, 13_000, 20_000])
    ap = np.zeros((10, 6), dtype=bool)
    ap[0:8, 0] = True          # A: all of North and West
    ap[0:4, 1] = True          # B: four of the five North voters
    ap[0:5, 2] = True          # C: all of North
    ap[5:8, 3] = True          # D: all of West
    ap[8:10, 4] = True         # E: both East voters
    ap[8:10, 5] = True         # F: both East voters
    budget = 100_000
    print("Toy vote - 10 voters (North 5, West 3, East 2), budget $100,000, $10,000 each")
    for p, nm in enumerate(names):
        print(f"  {nm:<22} cost=${costs[p]:>6,}  votes={ap[:, p].sum():>2}  "
              f"first-round price per supporter=${costs[p] / ap[:, p].sum():,.0f}")
    g = greedy(ap, costs, budget)
    print("  greedy funds:", ", ".join(names[p][0] for p in g),
          f" spent=${costs[g].sum():,}")
    trace = []
    es, money = equal_shares(ap, costs, budget, trace=trace)
    for r, (p, rho, mon) in enumerate(trace, 1):
        print(f"  equal shares round {r}: fund {names[p]:<22} price per supporter=${rho:,.0f}"
              f"  money left N/W/E per voter = ${mon[0]:,.0f}/${mon[5]:,.0f}/${mon[8]:,.0f}")
    print("  equal shares funds:", ", ".join(names[p][0] for p in es),
          f" spent=${costs[es].sum():,}  left over=${budget - costs[es].sum():,}")
    for rule, f in (("greedy", g), ("equal shares", es)):
        spent = {a: 0 for a in ("North", "West", "East")}
        # money each group's projects received (A is shared: split by its supporters)
        for p in f:
            sup = np.flatnonzero(ap[:, p])
            for i in sup:
                spent[groups[i]] += costs[p] / len(sup)
        none = int((~ap[:, f].any(axis=1)).sum())
        fails = [names[p][0] for p in jr_failures(ap, costs, budget, f)]
        print(f"  {rule:<13} money per group N/W/E = ${spent['North']:,.0f}/"
              f"${spent['West']:,.0f}/${spent['East']:,.0f}  voters with nothing={none}"
              f"  fair-share failures={fails}")
    print()


# ---------------------------------------------------------- Synthetic vote ---

def make_neighborhood(seed=3):
    """40 costed projects (10 per area) and one approval ballot per voter."""
    rng = np.random.default_rng(seed)
    residents = np.array([3_000, 3_500, 3_000, 4_500])    # adults per area
    turnout = np.array([0.30, 0.14, 0.14, 0.05])          # north homeowners vote most
    n_voters = np.round(residents * turnout).astype(int)
    area_of_project = np.repeat(np.arange(4), 10)
    # costs between about $3,000 and $90,000, most of them small (log-uniform)
    costs = np.round(np.exp(rng.uniform(np.log(3_000), np.log(90_000), 40)), -2).astype(int)
    appeal = rng.uniform(0.15, 0.65, 40)                  # how popular each project is
    voter_area = np.repeat(np.arange(4), n_voters)
    # a voter ticks a home-area project with probability `appeal`, another area's with
    # a tenth of that (people mostly back what is near them)
    prob = np.where(voter_area[:, None] == area_of_project[None, :],
                    appeal[None, :], appeal[None, :] / 10)
    approvals = rng.random(prob.shape) < prob
    return dict(residents=residents, n_voters=n_voters, voter_area=voter_area,
                area_of_project=area_of_project, costs=costs, approvals=approvals)


def report(label, funded, nb, approvals=None):
    ap = nb["approvals"] if approvals is None else approvals
    costs, pa, va = nb["costs"], nb["area_of_project"], nb["voter_area"]
    f = np.array(funded, dtype=int)
    money = [costs[f[pa[f] == a]].sum() for a in range(4)]
    count = [int((pa[f] == a).sum()) for a in range(4)]
    has_one = ap[:, f].any(axis=1)
    pct_one = [100 * has_one[va == a].mean() for a in range(4)]
    print(f"  {label:<38} projects={len(f):>2}  spent=${costs[f].sum():>7,}  "
          f"share N/W/S/E=" + "/".join(f"{100 * m / BUDGET:.0f}%" for m in money)
          + "  projects N/W/S/E=" + "/".join(map(str, count))
          + f"  voters with >=1 funded={100 * has_one.mean():.0f}% (N/W/S/E="
          + "/".join(f"{x:.0f}" for x in pct_one) + "%)")
    return money


def main():
    t0 = time.perf_counter()
    toy()

    nb = make_neighborhood()
    ap, costs, va, pa = nb["approvals"], nb["costs"], nb["voter_area"], nb["area_of_project"]
    n = len(va)
    print(f"Synthetic neighborhood - {len(costs)} projects, budget ${BUDGET:,}, {n:,} ballots")
    for a, name in enumerate(AREAS):
        c = costs[pa == a]
        print(f"  {name:<6} adults={nb['residents'][a]:>5,}  ballots={nb['n_voters'][a]:>4}  "
              f"turnout={100 * nb['n_voters'][a] / nb['residents'][a]:.0f}%  "
              f"share of ballots={100 * nb['n_voters'][a] / n:.1f}%  "
              f"share of adults={100 * nb['residents'][a] / nb['residents'].sum():.1f}%  "
              f"its 10 projects cost ${c.sum():,} (${c.min():,}-${c.max():,})")
    print(f"  all 40 projects cost ${costs.sum():,}; cheapest ${costs.min():,}, "
          f"dearest ${costs.max():,}; average ticks per ballot={ap.sum(axis=1).mean():.1f}")
    print(f"  each voter's equal share = ${BUDGET / n:,.2f}")
    print()

    print("Simulation - greedy count vs equal shares")
    g = greedy(ap, costs, BUDGET)
    report("greedy (most votes first)", g, nb)
    es, money = equal_shares(ap, costs, BUDGET)
    report("equal shares (before completion)", es, nb)
    paid = [BUDGET / n * (va == a).sum() - money[va == a].sum() for a in range(4)]
    print("  equal shares: money paid by each area's voters N/W/S/E = "
          + "/".join(f"${x:,.0f}" for x in paid)
          + "  = " + "/".join(f"{100 * x / sum(paid):.0f}%" for x in paid) + " of what was spent")
    esc, raises = equal_shares_completed(ap, costs, BUDGET)
    report("equal shares + completion", esc, nb)
    print(f"  completion raised each share by {raises}% before filling the rest by votes")
    print(f"  fair-share failures: greedy={len(jr_failures(ap, costs, BUDGET, g))}  "
          f"equal shares={len(jr_failures(ap, costs, BUDGET, esc))}")
    for label, weight in (("ballots", nb["n_voters"]), ("adults", nb["residents"])):
        env = BUDGET * weight / weight.sum()
        ge = greedy_envelopes(ap, costs, BUDGET, pa, env)
        report(f"greedy in envelopes by {label}", ge, nb)
        print(f"    envelopes N/W/S/E=" + "/".join(f"${x:,.0f}" for x in env)
              + f"  fair-share failures={len(jr_failures(ap, costs, BUDGET, ge))}")
    top = np.argsort(-ap.sum(axis=0))[:12]
    print("  12 most-voted projects (area, votes):",
          ", ".join(f"{AREAS[pa[p]][0]}{ap[:, p].sum()}" for p in top))
    print()

    print("Minimum-share guard - East reserve counted on East ballots first")
    for reserve in (25_000, 37_500):
        east_p = np.flatnonzero(pa == 3)
        east_v = va == 3
        first, _ = equal_shares(ap[np.ix_(east_v, east_p)], costs[east_p], reserve)
        first = [int(east_p[p]) for p in first]
        rest_left = BUDGET - costs[first].sum()
        ap_rest = ap.copy()
        ap_rest[:, first] = False                   # already funded: take off the ballot
        second, _ = equal_shares_completed(ap_rest, costs, rest_left)
        report(f"reserve ${reserve:,} + equal shares", first + second, nb)
    print()

    print("Uncertainty - who turned out? Resample the ballots 100 times (bootstrap)")
    rng = np.random.default_rng(11)
    shares = {"greedy": [], "equal shares": []}
    in_count = {"greedy": np.zeros(40), "equal shares": np.zeros(40)}
    for _ in range(100):
        idx = rng.integers(0, n, n)
        b = ap[idx]
        for rule, f in (("greedy", greedy(b, costs, BUDGET)),
                        ("equal shares", equal_shares_completed(b, costs, BUDGET)[0])):
            f = np.array(f, dtype=int)
            shares[rule].append([100 * costs[f[pa[f] == a]].sum() / BUDGET for a in range(4)])
            in_count[rule][f] += 1
    for rule in shares:
        s = np.array(shares[rule])
        lo, hi = np.percentile(s, [2.5, 97.5], axis=0)
        edge = int(((in_count[rule] > 10) & (in_count[rule] < 90)).sum())
        print(f"  {rule:<13} " + "  ".join(
            f"{AREAS[a]} {s[:, a].mean():.0f}% ({lo[a]:.0f}-{hi[a]:.0f})" for a in range(4))
              + f"  projects on the edge (funded in 10-90% of resamples)={edge}")
    print()

    print("Bloc voting - North homeowners all tick the same list of 6 North projects")
    north_p = np.flatnonzero(pa == 0)
    bloc_list = north_p[np.argsort(-ap[:, north_p].sum(axis=0))][:6]
    ap_bloc = ap.copy()
    north_v = va == 0
    ap_bloc[np.ix_(north_v, north_p)] = False
    ap_bloc[np.ix_(north_v, bloc_list)] = True
    print(f"  the list costs ${costs[bloc_list].sum():,}")
    report("greedy, with bloc", greedy(ap_bloc, costs, BUDGET), nb, ap_bloc)
    report("equal shares before completion, bloc", equal_shares(ap_bloc, costs, BUDGET)[0],
           nb, ap_bloc)
    report("equal shares + completion, with bloc",
           equal_shares_completed(ap_bloc, costs, BUDGET)[0], nb, ap_bloc)
    env = BUDGET * nb["n_voters"] / nb["n_voters"].sum()
    report("greedy in ballot envelopes, with bloc",
           greedy_envelopes(ap_bloc, costs, BUDGET, pa, env), nb, ap_bloc)
    print()
    print(f"Run time: {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    main()
