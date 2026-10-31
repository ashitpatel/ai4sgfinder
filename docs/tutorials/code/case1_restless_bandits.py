"""Case 1 tutorial code: restless bandits with a Whittle index for CHW home visits.

Every number quoted in docs/tutorials/01-restless-bandits-chw-visits.md comes from
running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case1_restless_bandits.py

Only numpy is needed. The program is illustrative; the patient groups and their
probabilities are made up for teaching.
"""

import numpy as np

LAPSING, ADHERING = 0, 1
BETA = 0.9  # discount: a week from now counts 90% as much as this week

# Chance of being ADHERING next week, given this week's state, without (passive)
# and with (active) a visit. Index [state] -> probability of adhering next week.
GROUPS = {
    "steady":      {"passive": [0.30, 0.95], "active": [0.40, 0.97]},
    "responsive":  {"passive": [0.10, 0.70], "active": [0.60, 0.95]},
    "hard-to-move": {"passive": [0.05, 0.50], "active": [0.08, 0.55]},
}


# ---------------------------------------------------------- Decision engine ---

def values_with_subsidy(p_passive, p_active, subsidy, beta=BETA, iters=2000):
    """Long-run value of each state when the passive choice earns an extra `subsidy`.

    Reward each week = 1 if adhering, plus `subsidy` if we choose not to visit.
    Returns (V, Q_passive, Q_active), each indexed by state.
    """
    V = np.zeros(2)
    for _ in range(iters):
        q_pas = np.array([s + subsidy + beta * (p_passive[s] * V[1] + (1 - p_passive[s]) * V[0])
                          for s in (0, 1)])
        q_act = np.array([s + beta * (p_active[s] * V[1] + (1 - p_active[s]) * V[0])
                          for s in (0, 1)])
        V = np.maximum(q_pas, q_act)
    return V, q_pas, q_act


def whittle_index(p_passive, p_active, state, beta=BETA):
    """Smallest subsidy that makes 'don't visit' as good as 'visit' in this state.

    Found by bisection: if the active choice still wins, the subsidy is too low.
    """
    lo, hi = -1.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        _, q_pas, q_act = values_with_subsidy(p_passive, p_active, mid, beta)
        if q_act[state] > q_pas[state]:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def passive_values(p_passive, beta=BETA):
    """Long-run value of each state if the patient is never visited.

    Two equations, two unknowns:
        V0 = 0 + beta * (p0 * V1 + (1 - p0) * V0)
        V1 = 1 + beta * (p1 * V1 + (1 - p1) * V0)
    """
    p0, p1 = p_passive
    A = np.array([[1 - beta * (1 - p0), -beta * p0],
                  [-beta * (1 - p1), 1 - beta * p1]])
    return np.linalg.solve(A, np.array([0.0, 1.0]))


def one_step_benefit(p_passive, p_active, state, beta=BETA):
    """Hand-calculable approximation: visit once now, then leave the patient alone.

    = beta * (extra chance of adhering next week) * (value gap between the states)
    """
    V = passive_values(p_passive, beta)
    return beta * (p_active[state] - p_passive[state]) * (V[ADHERING] - V[LAPSING]), V


# ---------------------------------------------------------------- Estimates ---

def estimate(successes, trials, prior=0.5):
    """Point estimate with half a success and half a failure added (avoids 0/0)."""
    return (successes + prior) / (trials + 2 * prior)


def optimistic(successes, trials, week, prior=0.5):
    """Upper end of a confidence band: estimate + sqrt(2 ln t / n), capped at 1."""
    p_hat = estimate(successes, trials, prior)
    radius = np.sqrt(2 * np.log(week) / (trials + 2 * prior))
    return min(1.0, p_hat + radius), p_hat, radius


# --------------------------------------------------------------- Simulation ---

def simulate(policy, weeks=12, n_per_group=400, budget=80, seed=7):
    """Run 1,200 patients (400 per group) for `weeks` weeks under a visit policy.

    Returns the average share of patients adhering per week.
    """
    rng = np.random.default_rng(seed)
    names = list(GROUPS)
    group = np.repeat(np.arange(len(names)), n_per_group)
    state = rng.random(group.size) < 0.6          # 60% adhering at the start
    index_table = {(g, s): whittle_index(GROUPS[n]["passive"], GROUPS[n]["active"], s)
                   for g, n in enumerate(names) for s in (0, 1)}
    adhering_share = []
    for week in range(weeks):
        if policy == "rotation":
            chosen = np.arange(week * budget, (week + 1) * budget) % group.size
        elif policy == "risk score":   # visit lapsing patients first, worst groups first
            risk = (1 - state) * 10 + np.array([GROUPS[names[g]]["passive"][0] for g in group]) * -1
            chosen = np.argsort(-risk, kind="stable")[:budget]
        elif policy == "whittle":
            idx = np.array([index_table[(g, int(s))] for g, s in zip(group, state)])
            chosen = np.argsort(-idx, kind="stable")[:budget]
        visit = np.zeros(group.size, dtype=bool)
        visit[chosen] = True
        p_next = np.array([GROUPS[names[g]]["active" if v else "passive"][int(s)]
                           for g, s, v in zip(group, state, visit)])
        state = rng.random(group.size) < p_next
        adhering_share.append(state.mean())
    return float(np.mean(adhering_share))


def main():
    np.set_printoptions(precision=3, suppress=True)
    print("Decision engine - Whittle index and one-step benefit, by group and state")
    for name, g in GROUPS.items():
        for s, label in ((LAPSING, "lapsing"), (ADHERING, "adhering")):
            w = whittle_index(g["passive"], g["active"], s)
            b, V = one_step_benefit(g["passive"], g["active"], s)
            print(f"  {name:13s} {label:9s} index={w:6.3f}  one-step={b:6.3f}  "
                  f"left-alone V(lapsing)={V[0]:.2f} V(adhering)={V[1]:.2f}")

    print("\nDecision engine - worked example (responsive, lapsing), step by step")
    g = GROUPS["responsive"]
    V = passive_values(g["passive"])
    no_visit = 0 + BETA * (0.10 * V[1] + 0.90 * V[0])
    visit = 0 + BETA * (0.60 * V[1] + 0.40 * V[0])
    print(f"  left alone: V(lapsing)={V[0]:.3f}  V(adhering)={V[1]:.3f}  gap={V[1]-V[0]:.3f}")
    print(f"  no visit now={no_visit:.3f}  visit now={visit:.3f}  difference={visit-no_visit:.3f}")
    print(f"  Whittle index (accounts for future visits too) = "
          f"{whittle_index(g['passive'], g['active'], LAPSING):.3f}")

    print("\nEstimates - estimates from the ledger (responsive group, lapsing state)")
    # Passive: 1,500 lapsing patient-weeks without a visit, 150 recovered.
    # Active: only 20 lapsing patient-weeks with a visit, 12 recovered.
    for label, k, n in (("no visit", 150, 1500), ("visit", 12, 20)):
        up, p_hat, r = optimistic(k, n, week=39)
        lo_wald = p_hat - 1.96 * np.sqrt(p_hat * (1 - p_hat) / n)
        hi_wald = p_hat + 1.96 * np.sqrt(p_hat * (1 - p_hat) / n)
        print(f"  {label:8s} k={k:4d} n={n:5d} p_hat={p_hat:.3f}  95% CI=({lo_wald:.3f}, {hi_wald:.3f})"
              f"  radius={r:.3f}  optimistic={up:.3f}")

    print("\nEstimates - forgetting old data (alpha = 0.9 per week)")
    weights = 0.9 ** np.arange(39)[::-1]
    print(f"  weight of a 1-week-old record={weights[-2]:.2f}, 10 weeks={0.9**10:.2f}, "
          f"26 weeks={0.9**26:.3f}; effective sample size of 39 weeks={weights.sum():.1f}")

    print("\nSimulation - 12-week simulation, average share adhering (1,200 patients, 80 visits/week)")
    for policy in ("rotation", "risk score", "whittle"):
        print(f"  {policy:10s} {simulate(policy):.3f}")


if __name__ == "__main__":
    main()
