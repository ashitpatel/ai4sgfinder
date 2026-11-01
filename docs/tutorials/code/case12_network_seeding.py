"""Case 12 tutorial code: choosing 25 peer educators by greedy influence maximization.

Every number quoted in docs/tutorials/12-network-seeding-peer-educators.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case12_network_seeding.py

It needs only numpy. The friendship network is stored as a plain table of pairs
(no NetworkX needed). The shelter, its residents, their friendships, risk scores
and refusals are synthetic, generated with fixed random seeds; they are made up
for teaching. The output is the same on every run.

The spread model is the independent cascade: once a resident hears the message,
each friend who hasn't heard it yet hears it from them with probability p. A
friendship is only ever "tried" once (by whichever of the two hears first), so the
cascade is the same as flipping one coin per friendship in advance and keeping the
links that came up heads: everyone connected to a seed by kept links hears the
message. The code uses that coin-flipping view for speed.
"""

from itertools import combinations, product
from math import comb

import numpy as np

N_RESIDENTS = 400        # young people using the shelter
N_SEEDS = 25             # training places
N_BACKUPS = 10           # ranked backups for refusals
P_BASE = 0.15            # assumed chance a friend passes the message on (a rough guess)
P_SENSITIVITY = [0.08, 0.15, 0.25]
P_DECLINE = 0.20         # illustrative chance an invitee declines or leaves before training
R_SELECT = 2000          # coin-flip "worlds" used to choose seeds
R_EVAL = 2000            # fresh worlds used to score plans (so plans are not graded on their own exam)


def ci95(per_world):
    """Mean and 95% confidence interval: mean +/- 1.96 * sd / sqrt(number of worlds)."""
    m = per_world.mean()
    half = 1.96 * per_world.std(ddof=1) / np.sqrt(len(per_world))
    return m, m - half, m + half


# ------------------------------------------------- Reach in "coin-flip worlds" ---
def component_labels(n, U, V, live):
    """For each world (row of `live`), label every person with the smallest ID in
    their connected set: everyone joined to them by a chain of kept friendships.
    live has shape (worlds, pairs)."""
    R = live.shape[0]
    lab = np.tile(np.arange(n), (R, 1))
    r_idx, e_idx = np.nonzero(live)
    u, v = U[e_idx], V[e_idx]
    while True:
        m = np.minimum(lab[r_idx, u], lab[r_idx, v])
        new = lab.copy()
        np.minimum.at(new, (r_idx, u), m)
        np.minimum.at(new, (r_idx, v), m)
        new = np.take_along_axis(new, new, axis=1)        # jump to the label's label
        if np.array_equal(new, lab):
            return lab
        lab = new


class Worlds:
    """Many coin-flip worlds for one network and one p, ready to score seed sets."""

    def __init__(self, n, U, V, p, n_worlds, rng=None, live=None):
        if live is None:
            live = rng.random((n_worlds, len(U))) < p
        self.n, self.R = n, live.shape[0]
        lab = component_labels(n, U, V, live)
        self.gid = lab + (np.arange(self.R) * n)[:, None]  # connected-set ID, unique across worlds
        self.size = np.bincount(self.gid.ravel(), minlength=self.R * n)

    def reach_per_world(self, seeds):
        """Number of people who hear the message in each world."""
        g = np.sort(self.gid[:, list(seeds)], axis=1)
        first = np.ones(g.shape, dtype=bool)               # count each connected set once
        first[:, 1:] = g[:, 1:] != g[:, :-1]
        return (self.size[g] * first).sum(axis=1)

    def gains(self, seeds):
        """Expected extra people reached by adding each person to `seeds`."""
        covered = np.zeros(self.R * self.n, dtype=bool)
        if seeds:
            covered[self.gid[:, list(seeds)].ravel()] = True
        return (self.size[self.gid] * ~covered[self.gid]).mean(axis=0)

    def greedy(self, k):
        """Add one seed at a time, each time the person who adds the most expected reach."""
        seeds, gain_log = [], []
        for _ in range(k):
            g = self.gains(seeds)
            g[seeds] = -1                                   # already chosen
            best = int(np.argmax(g))
            seeds.append(best)
            gain_log.append(g[best])
        return seeds, gain_log


# --------------------------------------------------------------- Toy example ---
TOY_NAMES = list("ABCDEFGHIJ")
# Friend group 1: A, B, C, D all friends with each other, and E is friends with A only.
# Friend group 2: H is friends with F, G and I; I is friends with J. No links between groups.
TOY_PAIRS = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D"),
             ("A", "E"), ("H", "F"), ("H", "G"), ("H", "I"), ("I", "J")]
TOY_P = 0.5


def toy_cascade(seeds, adj, p, rng):
    """One run of the independent cascade, step by step, as you would act it out."""
    heard, newly = set(seeds), list(seeds)
    while newly:
        nxt = []
        for person in newly:
            for friend in adj[person]:
                if friend not in heard and rng.random() < p:   # one try per friend
                    heard.add(friend)
                    nxt.append(friend)
        newly = nxt
    return len(heard)


def toy_example():
    idx = {c: i for i, c in enumerate(TOY_NAMES)}
    U = np.array([idx[a] for a, b in TOY_PAIRS])
    V = np.array([idx[b] for a, b in TOY_PAIRS])
    E = len(TOY_PAIRS)
    # Every one of the 2^11 = 2,048 coin-flip outcomes, with its probability: exact answers.
    live = np.array(list(product([False, True], repeat=E)))
    prob = TOY_P ** live.sum(1) * (1 - TOY_P) ** (E - live.sum(1))
    W = Worlds(10, U, V, TOY_P, None, live=live)

    def exact(seeds):
        return float((W.reach_per_world([idx[s] for s in seeds]) * prob).sum())

    print("Toy example - 10 residents, 11 friendships, p = 0.5, 2 seeds")
    deg = {c: sum(c in pr for pr in TOY_PAIRS) for c in TOY_NAMES}
    print("  friends per person: " + "  ".join(f"{c}={deg[c]}" for c in TOY_NAMES))
    print("  exact expected reach of one seed:")
    print("    " + "  ".join(f"{c}={exact([c]):.3f}" for c in TOY_NAMES))
    adj = {c: [b if a == c else a for a, b in TOY_PAIRS if c in (a, b)] for c in TOY_NAMES}
    rng = np.random.default_rng(12)
    runs = np.array([toy_cascade(["A"], adj, TOY_P, rng) for _ in range(1000)])
    m, lo, hi = ci95(runs)
    print(f"  Monte Carlo, seed A, 1,000 step-by-step runs: mean={m:.3f}  95% CI {lo:.3f} to {hi:.3f}"
          f"  (exact {exact(['A']):.3f}); runs reaching all 5 of A's group: {np.mean(runs == 5):.1%}")
    pairs = sorted(((exact(list(pr)), pr) for pr in combinations(TOY_NAMES, 2)), reverse=True)
    print("  best pairs (exact expected reach):")
    for val, pr in pairs[:4]:
        print(f"    {pr[0]}+{pr[1]}: {val:.3f}")
    print(f"  two most-connected (A+B): {exact(['A', 'B']):.3f}")
    first = max(TOY_NAMES, key=lambda c: exact([c]))
    gains = {c: exact([first, c]) - exact([first]) for c in TOY_NAMES if c != first}
    second = max(gains, key=gains.get)
    print(f"  greedy round 1 picks {first} ({exact([first]):.3f});"
          f" round 2 gains given {first}: " + "  ".join(f"{c}={g:.3f}" for c, g in gains.items()))
    print(f"  greedy picks {first}+{second}: {exact([first, second]):.3f}"
          f"   (B alone {exact(['B']):.3f}, B added after A only +{gains['B']:.3f})")
    print()


# ----------------------------------------------------- The synthetic shelter ---
GROUP_SIZES = [60, 48, 40, 36, 32, 30, 28, 26, 24, 22, 20, 14, 12, 8]   # friend groups, 400 in all
DROP_IN_REGULARS = {0, 1}   # the groups that spend most time around the front desk


def make_shelter(rng):
    """Friend groups, a 'name up to three closest friends' survey, risk scores, staff visibility."""
    group = np.repeat(np.arange(len(GROUP_SIZES)), GROUP_SIZES)
    n = len(group)
    risk_z = rng.normal(size=n)                    # intake risk score (standardized)
    social = np.exp(0.5 * rng.normal(size=n) - 0.35 * risk_z)   # at-risk youth a bit less social
    answered = rng.random(n) < 0.90                # 10% skip the survey (others can still name them)
    nominations = []
    for i in np.flatnonzero(answered):
        k = rng.choice([1, 2, 3], p=[0.2, 0.3, 0.5])
        same = group == group[i]
        weight = social * np.where(same, 0.92 / same.sum(), 0.08 / (~same).sum())
        weight[i] = 0
        for j in rng.choice(n, size=k, replace=False, p=weight / weight.sum()):
            nominations.append((i, int(j)))
    pairs = sorted({(min(a, b), max(a, b)) for a, b in nominations})
    U = np.array([a for a, b in pairs])
    V = np.array([b for a, b in pairs])
    degree = np.bincount(np.concatenate([U, V]), minlength=n)
    visibility = (np.log1p(degree) + 0.8 * np.isin(group, list(DROP_IN_REGULARS))
                  + 0.3 * rng.normal(size=n))
    return dict(n=n, group=group, risk=risk_z, U=U, V=V, degree=degree,
                visibility=visibility, answered=answered, nominations=len(nominations))


def top(score, k):
    return [int(i) for i in np.argsort(-score, kind="stable")[:k]]


def spread_by_group(deg, group, k):
    """The paper rule: give each friend group seeds in proportion to its size (at least one),
    then pick the people with the most friends inside each group."""
    sizes = np.bincount(group)
    share = k * sizes / sizes.sum()
    quota = np.maximum(1, np.floor(share)).astype(int)
    for g in np.argsort(-(share - np.floor(share)), kind="stable"):   # largest remainders first
        if quota.sum() >= k:
            break
        quota[g] += 1
    seeds = []
    for g, q in enumerate(quota):
        members = np.flatnonzero(group == g)
        seeds += [int(i) for i in members[np.argsort(-deg[members], kind="stable")[:q]]]
    return seeds


def main():
    toy_example()
    rng = np.random.default_rng(2026)
    sh = make_shelter(rng)
    n, group, U, V, deg = sh["n"], sh["group"], sh["U"], sh["V"], sh["degree"]
    within = np.mean(group[U] == group[V])
    print("Synthetic shelter network")
    print(f"  residents={n}  answered survey={sh['answered'].sum()}  nominations={sh['nominations']}"
          f"  friendship pairs={len(U)}  ({within:.0%} inside a friend group)")
    print(f"  friends per resident: mean={deg.mean():.2f}  median={np.median(deg):.0f}  max={deg.max()}"
          f"  with no friends listed={np.sum(deg == 0)}")
    print(f"  friend groups={len(GROUP_SIZES)}  sizes={GROUP_SIZES}")
    hi_risk = sh["risk"] > np.quantile(sh["risk"], 0.9)
    print(f"  mean friends: top-10% risk={deg[hi_risk].mean():.2f}  everyone else={deg[~hi_risk].mean():.2f}")
    print()

    sel = Worlds(n, U, V, P_BASE, R_SELECT, np.random.default_rng(1))
    ev = Worlds(n, U, V, P_BASE, R_EVAL, np.random.default_rng(2))

    # --- Greedy seed selection, with the backups as rounds 26-35.
    order, gain_log = sel.greedy(N_SEEDS + N_BACKUPS)
    greedy, backups = order[:N_SEEDS], order[N_SEEDS:]
    print(f"Greedy selection (p={P_BASE}, {R_SELECT} worlds)")
    print("  expected gain by round: " + "  ".join(
        f"{r}:{gain_log[r - 1]:.2f}" for r in (1, 2, 3, 5, 10, 15, 20, 25)))
    print("  backup gains (rounds 26-35): " + " ".join(f"{g:.2f}" for g in gain_log[N_SEEDS:]))
    print(f"  greedy reach on the worlds it was chosen with={sel.reach_per_world(greedy).mean():.1f}"
          f"  (guarantee: at least 1 - 1/e = {1 - 1 / np.e:.1%} of the best possible)")
    print()

    # --- Compare plans on fresh worlds.
    plans = {
        "most at-risk (intake score)": top(sh["risk"], N_SEEDS),
        "staff picks (most visible)": top(sh["visibility"], N_SEEDS),
        "most friends (degree)": top(deg + 1e-3 * sh["visibility"], N_SEEDS),
        "most friends, by group": spread_by_group(deg, group, N_SEEDS),
        "greedy (influence max.)": greedy,
    }
    rng_rand = np.random.default_rng(3)
    rand_means = np.array([ev.reach_per_world(rng_rand.choice(n, N_SEEDS, replace=False)).mean()
                           for _ in range(100)])
    print(f"Plans for 25 seeds, scored on {R_EVAL} fresh worlds (p={P_BASE})")
    print(f"  {'random (100 draws)':30s} reach={rand_means.mean():6.1f}  "
          f"middle 90% of draws {np.quantile(rand_means, 0.05):.1f} to {np.quantile(rand_means, 0.95):.1f}")
    per_world = {}
    for name, seeds in plans.items():
        pw = ev.reach_per_world(seeds)
        per_world[name] = pw
        m, lo, hi = ci95(pw)
        n_groups = len(set(group[seeds]))
        solo = sum(ev.reach_per_world([s]).mean() for s in seeds)
        print(f"  {name:30s} reach={m:6.1f}  95% CI {lo:.1f} to {hi:.1f}  ({m / n:.1%})"
              f"  groups with a seed={n_groups:2d}/14  seeds in groups 0-1={np.isin(group[seeds], [0, 1]).sum():2d}"
              f"  sum of solo reaches={solo:.1f}")
    for name in list(plans)[:-1]:
        d = per_world["greedy (influence max.)"] - per_world[name]
        m, lo, hi = ci95(d)
        print(f"  greedy minus {name:30s} {m:5.1f}  95% CI {lo:.1f} to {hi:.1f}")
    print(f"  seeds shared: greedy & degree={len(set(greedy) & set(plans['most friends (degree)']))}"
          f"  greedy & staff={len(set(greedy) & set(plans['staff picks (most visible)']))}"
          f"  greedy & at-risk={len(set(greedy) & set(plans['most at-risk (intake score)']))}")
    print(f"  friends of greedy seeds: mean={deg[greedy].mean():.1f}  (degree plan {deg[plans['most friends (degree)']].mean():.1f})")
    print()

    # --- Sensitivity to the unknown p.
    print("Sensitivity to p (each p: fresh selection and scoring worlds)")
    for p in P_SENSITIVITY:
        s_w = Worlds(n, U, V, p, R_SELECT, np.random.default_rng(10 + int(p * 100)))
        e_w = Worlds(n, U, V, p, R_EVAL, np.random.default_rng(20 + int(p * 100)))
        re_opt, _ = s_w.greedy(N_SEEDS)
        line = f"  p={p:.2f}  greedy re-chosen={e_w.reach_per_world(re_opt).mean():6.1f}"
        line += f"  base-p greedy list={e_w.reach_per_world(greedy).mean():6.1f}"
        line += f"  degree={e_w.reach_per_world(plans['most friends (degree)']).mean():6.1f}"
        line += f"  by group={e_w.reach_per_world(plans['most friends, by group']).mean():6.1f}"
        line += f"  staff={e_w.reach_per_world(plans['staff picks (most visible)']).mean():6.1f}"
        line += f"  at-risk={e_w.reach_per_world(plans['most at-risk (intake score)']).mean():6.1f}"
        line += f"  seeds kept from base list={len(set(re_opt) & set(greedy))}/25"
        print(line)
    print()

    # --- Refusals and backups.
    rng_dec = np.random.default_rng(4)
    full = per_world["greedy (influence max.)"].mean()
    no_backup, with_backup, trained, ran_out = [], [], [], 0
    for _ in range(2000):
        accepted = [s for s in greedy if rng_dec.random() >= P_DECLINE]
        no_backup.append(ev.reach_per_world(accepted).mean())
        pool = list(backups)
        while len(accepted) < N_SEEDS and pool:
            g = sel.gains(accepted)                     # next backup = most new reach now
            nxt = max(pool, key=lambda b: g[b])
            pool.remove(nxt)
            if rng_dec.random() >= P_DECLINE:
                accepted.append(nxt)
        ran_out += len(accepted) < N_SEEDS
        trained.append(len(accepted))
        with_backup.append(ev.reach_per_world(accepted).mean())
    # Chance of fewer than 25 acceptances among all 35 invitations (binomial, exact).
    k = np.arange(36)
    pmf = np.array([comb(35, int(x)) * (1 - P_DECLINE) ** x * P_DECLINE ** (35 - x) for x in k])
    print(f"Refusals (each invitee declines with chance {P_DECLINE:.0%}; 2,000 simulated rounds of invitations)")
    print(f"  expected declines among first 25 = {N_SEEDS * P_DECLINE:.0f}"
          f"  (sd {np.sqrt(N_SEEDS * P_DECLINE * (1 - P_DECLINE)):.0f})")
    print(f"  all 25 accept: reach={full:.1f}")
    print(f"  no backups:    reach={np.mean(no_backup):.1f}  trained={N_SEEDS * (1 - P_DECLINE):.0f} on average")
    print(f"  10 backups:    reach={np.mean(with_backup):.1f}  trained={np.mean(trained):.1f} on average"
          f"  short of 25 in {ran_out / 20:.1f}% of rounds (binomial: {pmf[:25].sum():.1%})")
    print()

    # --- Measuring spread later.
    s_g = per_world["greedy (influence max.)"].mean() / n
    s_s = per_world["staff picks (most visible)"].mean() / n
    for m_res in (400, 200):
        moe = 1.96 * np.sqrt(s_g * (1 - s_g) / m_res + s_s * (1 - s_s) / m_res)
        print(f"Follow-up survey, {m_res} residents per cycle: predicted share heard greedy={s_g:.1%}"
              f" staff={s_s:.1%}  difference={s_g - s_s:.1%}  margin of error +/-{moe:.1%}")


if __name__ == "__main__":
    main()
