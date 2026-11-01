"""Case 8 tutorial code: effect-based targeting (policy learning) for 600 business grants.

Every number quoted in docs/tutorials/08-policy-learning-business-grants.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case8_policy_learning.py

It needs only numpy. The pilot of 3,000 applicants, this year's 3,000 applicants
and the grant's true effects are synthetic, generated with fixed random seeds;
they are made up for teaching. Because the data are invented, the code knows each
applicant's true effect, so it can also report how well each rule *really* does,
something a real program can only estimate. The output is identical on every run.
"""

import numpy as np

BUDGET = 600          # grants available this year
N_PILOT = 3000        # last year's randomized pilot
N_NEW = 3000          # this year's applicants (illustrative; the case gives no figure)
P_OFFER = 0.5         # the pilot lottery offered the grant to half the applicants
SHARE = BUDGET / N_NEW  # the budget covers 20% of applicants
MIN_ARM = 40          # a rule's group must hold at least 40 offered and 40 not offered
NEED_FLOOR = 120      # grants reserved for the poorest (20% of 600), by verified assets
Z = 1.96              # 95% confidence intervals


# ------------------------------------------------------------- Synthetic data ---

def true_effect(age, urban):
    """The grant's true effect on monthly income ($): small for shops under two
    years old, large for established shops, largest for established urban shops."""
    return np.where(age < 2, 5.0, np.where(urban == 1, 45.0, 30.0))


def make_applicants(n, rng, share_new=0.40, share_urban=0.45):
    """Applicants as the app records them. Newer shops tend to be poorer."""
    new = rng.random(n) < share_new
    age = np.where(new, rng.uniform(0.1, 2.0, n), 2.0 + rng.exponential(3.0, n))
    age = np.round(age, 1)
    urban = (rng.random(n) < share_urban).astype(int)
    food = (rng.random(n) < 0.5).astype(int)          # sells food (vs. other goods)
    hh = rng.integers(2, 9, n)                        # household size
    income = 150 + 25 * np.minimum(age, 6) + 40 * urban + rng.normal(0, 45, n)
    income = np.maximum(np.round(income), 40)         # monthly income at application, $
    assets = income + rng.normal(0, 20, n)            # asset score checked on a field visit
    return {"age": age, "urban": urban, "food": food, "hh": hh,
            "income": income, "assets": assets, "tau": true_effect(age, urban)}


def run_pilot(d, rng):
    """Lottery: exactly half offered. Outcome = change in monthly income a year later."""
    n = len(d["age"])
    w = np.zeros(n, dtype=int)
    w[rng.permutation(n)[: n // 2]] = 1
    trend = 10 + 3 * np.minimum(d["age"], 6) + 5 * d["urban"]   # what happens anyway
    change = trend + w * d["tau"] + rng.normal(0, 60, n)
    d["w"], d["y"] = w, np.round(change, 1)
    d["y_level"] = d["income"] + d["y"]        # income a year later (the level)
    return d


def diff_in_means(y, w):
    """Effect estimate with its 95% CI: mean(offered) - mean(not offered)."""
    y1, y0 = y[w == 1], y[w == 0]
    est = y1.mean() - y0.mean()
    se = np.sqrt(y1.var(ddof=1) / len(y1) + y0.var(ddof=1) / len(y0))
    return est, est - Z * se, est + Z * se, len(y1), len(y0)


def fmt(t):
    est, lo, hi, n1, n0 = t
    return f"{est:6.1f}  (95% CI {lo:6.1f} to {hi:6.1f})  n={n1}+{n0}"


# ------------------------------------------------- Toy example (by hand) ---------

def toy():
    print("Toy example - 8 pilot applicants, half offered by lottery")
    # (shop age in years, offered?, change in monthly income $)
    rows = [(0.5, 1, 12), (1.0, 0, 8), (3.0, 1, 70), (4.0, 0, 25),
            (0.8, 0, 10), (1.5, 1, 15), (5.0, 1, 60), (2.5, 0, 20)]
    age = np.array([r[0] for r in rows]); w = np.array([r[1] for r in rows])
    y = np.array([r[2] for r in rows], dtype=float)
    print(f"  everyone:          offered mean={y[w==1].mean():.2f}  not offered mean="
          f"{y[w==0].mean():.2f}  effect={y[w==1].mean()-y[w==0].mean():.2f}")
    for name, m in (("shop < 2 years", age < 2), ("shop >= 2 years", age >= 2)):
        e = y[m & (w == 1)].mean() - y[m & (w == 0)].mean()
        print(f"  {name:17s}: offered mean={y[m&(w==1)].mean():.2f}  not offered mean="
              f"{y[m&(w==0)].mean():.2f}  effect={e:.2f}")
    # IPW: each offered person stands for 1/0.5 = 2 people, each non-offered for 2.
    pick = age >= 2
    score = (w / P_OFFER - (1 - w) / P_OFFER) * y
    print(f"  IPW scores (rule 'shop >= 2'): {score[pick].tolist()}  "
          f"sum={score[pick].sum():.0f}  / {pick.sum()} picked = {score[pick].mean():.2f}")
    print()


# ------------------------------------------------------ T-learner ----------------

def features(d):
    return np.column_stack([np.ones(len(d["age"])), d["age"], d["urban"], d["food"],
                            d["hh"], d["income"] / 100])


def t_learner(d, idx):
    """Fit one linear regression for offered and one for not offered; the predicted
    effect is the difference between the two predictions."""
    X, y, w = features(d)[idx], d["y"][idx], d["w"][idx]
    b1 = np.linalg.lstsq(X[w == 1], y[w == 1], rcond=None)[0]
    b0 = np.linalg.lstsq(X[w == 0], y[w == 0], rcond=None)[0]
    return b1, b0


# ------------------------------------------- Learning a short rule ---------------
# A question is (field, threshold): "is field >= threshold?". Only hard-to-fake fields.

QUESTIONS = [("age", t) for t in (0.5, 1, 1.5, 2, 2.5, 3, 4, 5)] + \
            [("urban", 1), ("food", 1)]


def leaves_of(d, idx, rule):
    """Split applicants idx into the rule's groups (leaves). rule = list of questions;
    depth 1 = one question, depth 2 = the second question asked on both branches."""
    groups = [idx]
    for (f, t) in rule:
        groups = [g[m] for g in groups for m in (d[f][g] >= t, d[f][g] < t)]
    return groups


def budget_value(effects, sizes, share):
    """Fill a budget of `share` of all applicants from the best groups first (a lottery
    inside the last group reached). Returns the total estimated gain per applicant."""
    order = np.argsort(effects)[::-1]
    left, total, n = share * sizes.sum(), 0.0, sizes.sum()
    for k in order:
        take = min(left, sizes[k])
        total += take * effects[k]
        left -= take
    return total / n


def fit_rule(d, idx, depth):
    """Try every depth-1 or depth-2 rule; keep the one with the largest estimated gain
    under the 20% budget. Each group's effect is its difference in means."""
    best = None
    cands = [[q] for q in QUESTIONS] if depth == 1 else \
            [[q1, q2] for q1 in QUESTIONS for q2 in QUESTIONS if q2[0] != q1[0]]
    for rule in cands:
        groups = leaves_of(d, idx, rule)
        if any(min(d["w"][g].sum(), (1 - d["w"][g]).sum()) < MIN_ARM for g in groups):
            continue
        eff = np.array([diff_in_means(d["y"][g], d["w"][g])[0] for g in groups])
        val = budget_value(eff, np.array([len(g) for g in groups]), SHARE)
        if best is None or val > best[0]:
            best = (val, rule, eff)
    return best


def rule_priority(d, rule, eff):
    """Priority of each applicant = estimated effect of their group under the rule."""
    idx = np.arange(len(d["age"]))
    pr = np.zeros(len(idx))
    for g, e in zip(leaves_of(d, idx, rule), eff):
        pr[g] = e
    return pr


def describe(rule):
    names = {"age": "shop open >= {} yrs", "urban": "urban", "food": "sells food"}
    return " / ".join(names[f].format(t) for f, t in rule)


# ------------------------------------------------------- Selecting 600 -----------

def select(priority, k, rng):
    """Top-k by priority; ties broken by lottery."""
    jitter = rng.random(len(priority)) * 1e-6
    return np.argsort(-(priority + jitter))[:k]


def policies(d, rule, eff, b1, b0, k, rng, age_field="age"):
    """Each policy returns the indices of the k applicants it funds."""
    dd = dict(d); dd["age"] = d[age_field]
    rp = rule_priority(dd, rule, eff)
    tau_hat = features(dd) @ (b1 - b0)
    out = {
        "random lottery": rng.permutation(len(d["age"]))[:k],
        "poorest first (reported income)": select(-d["income"], k, rng),
        "effect rule (depth 2)": select(rp, k, rng),
        "T-learner ranking (linear)": select(tau_hat, k, rng),
    }
    floor_k = int(round(NEED_FLOOR * k / BUDGET))
    poor = select(-d["assets"], floor_k, rng)
    rest = rp.copy(); rest[poor] = -1e9
    out["effect rule + need floor"] = np.concatenate([poor, select(rest, k - floor_k, rng)])
    return out


def ipw_value(d, sel):
    """Held-out estimate of the average effect among those a rule selects. With a 50/50
    lottery the IPW weights are 1/0.5 = 2 for both groups; normalizing the weights in
    each group gives mean(offered) - mean(not offered) among the selected."""
    return diff_in_means(d["y"][sel], d["w"][sel])


def poorest_share(d, sel):
    """Share of the funded who are among the truly poorest 20% of applicants."""
    inc = d.get("income_true", d["income"])
    return np.mean(inc[sel] <= np.quantile(inc, 0.2))


# ---------------------------------------------------------------- Main -----------

def main():
    toy()
    rng = np.random.default_rng(8)
    pilot = run_pilot(make_applicants(N_PILOT, rng), rng)
    n_new = np.sum(pilot["age"] < 2)
    print("Pilot - 3,000 applicants, lottery offered 1,500")
    print(f"  shops under 2 years: {n_new} ({n_new/N_PILOT:.0%}); urban: "
          f"{pilot['urban'].sum()}; mean income at application ${pilot['income'].mean():.0f}/month")
    print(f"  mean income a year later: offered ${pilot['y_level'][pilot['w']==1].mean():.1f}, "
          f"not offered ${pilot['y_level'][pilot['w']==0].mean():.1f}")
    print(f"  average effect, using income level a year later: {fmt(diff_in_means(pilot['y_level'], pilot['w']))}")
    print(f"  average effect, using change in income:          {fmt(diff_in_means(pilot['y'], pilot['w']))}")
    print()

    print("Subgroup effects (change in monthly income, $), whole pilot")
    poor = pilot["income"] <= np.quantile(pilot["income"], 0.2)
    groups = [("shop < 2 years", pilot["age"] < 2), ("shop >= 2 years", pilot["age"] >= 2),
              ("rural", pilot["urban"] == 0), ("urban", pilot["urban"] == 1),
              ("sells food", pilot["food"] == 1), ("sells other goods", pilot["food"] == 0),
              ("poorest 20% by income", poor), ("other 80%", ~poor),
              (">= 2 yrs and urban", (pilot["age"] >= 2) & (pilot["urban"] == 1)),
              (">= 2 yrs and rural", (pilot["age"] >= 2) & (pilot["urban"] == 0))]
    for name, m in groups:
        print(f"  {name:22s} {fmt(diff_in_means(pilot['y'][m], pilot['w'][m]))}")
    print(f"  share of poorest 20% with shop < 2 years: {np.mean(pilot['age'][poor] < 2):.0%}")
    lvl_new = pilot["y_level"][(pilot["age"] < 2) & (pilot["w"] == 1)].mean()
    lvl_old = pilot["y_level"][(pilot["age"] >= 2) & (pilot["w"] == 1)].mean()
    print(f"  income a year later among offered: shop < 2 yrs ${lvl_new:.0f}, >= 2 yrs ${lvl_old:.0f}")
    print()

    # Split the pilot: learn on one half, check on the other.
    perm = np.random.default_rng(80).permutation(N_PILOT)
    train, test = np.sort(perm[:1500]), np.sort(perm[1500:])

    b1, b0 = t_learner(pilot, train)
    print("T-learner on training half: effect = offered model - not-offered model")
    for nm, c in zip(["constant", "shop age (per yr)", "urban", "sells food",
                      "household size", "income (per $100)"], b1 - b0):
        print(f"  {nm:20s} {c:7.2f}")
    print()

    print("Learning a short rule on the training half (budget = 20% of applicants)")
    v1, r1, e1 = fit_rule(pilot, train, 1)
    v2, r2, e2 = fit_rule(pilot, train, 2)
    print(f"  best depth-1 rule: {describe(r1)}  groups' effects={np.round(e1,1).tolist()}  "
          f"estimated gain per grant={v1/SHARE:.1f}")
    print(f"  best depth-2 rule: {describe(r2)}  groups' effects={np.round(e2,1).tolist()}  "
          f"estimated gain per grant={v2/SHARE:.1f}")
    tg = leaves_of(pilot, train, r2)
    print(f"  depth-2 group sizes in training half: {[len(g) for g in tg]}")
    print()

    # Held-out check: apply each rule to the test half with a budget of 20% (300).
    print("Held-out check - test half (1,500), each rule funds 300 (20%), IPW estimate")
    test_d = {k: v[test] for k, v in pilot.items()}
    trng = np.random.default_rng(81)
    pol = policies(test_d, r2, e2, b1, b0, 300, trng)
    v1_sel = select(rule_priority(test_d, r1, e1), 300, trng)
    pol = dict(list(pol.items())[:3] + [("effect rule (depth 1)", v1_sel)] + list(pol.items())[3:])
    for name, sel in pol.items():
        print(f"  {name:34s} {fmt(ipw_value(test_d, sel))}  true={test_d['tau'][sel].mean():5.1f}")
    print(f"  (estimated gain on the training half was {v2/SHARE:.1f} per grant)")
    print()

    # This year: a shifted applicant pool (more new and rural shops).
    yr = make_applicants(N_NEW, np.random.default_rng(2026), share_new=0.50, share_urban=0.35)
    yr["income_true"] = yr["income"].copy()
    print("This year's applicants - 3,000, 600 grants (true effects known in simulation)")
    print(f"  shops under 2 years: pilot {np.mean(pilot['age']<2):.0%}, this year {np.mean(yr['age']<2):.0%};"
          f" urban: pilot {pilot['urban'].mean():.0%}, this year {yr['urban'].mean():.0%}")
    pg = leaves_of(pilot, np.arange(N_PILOT), r2)
    yg = leaves_of(yr, np.arange(N_NEW), r2)
    print(f"  depth-2 group shares: pilot {[f'{len(g)/N_PILOT:.0%}' for g in pg]}, "
          f"this year {[f'{len(g)/N_NEW:.0%}' for g in yg]}")
    yrng = np.random.default_rng(82)
    res = policies(yr, r2, e2, b1, b0, BUDGET, yrng)
    for name, sel in res.items():
        g = yr["tau"][sel].mean()
        print(f"  {name:34s} gain/grant=${g:5.1f}  total=${g*BUDGET:7,.0f}/month  "
              f"poorest-20% share={poorest_share(yr, sel):4.0%}  new shops={np.mean(yr['age'][sel]<2):4.0%}")
    print()

    # Gaming 1: some applicants under-report income because they think the poorest win.
    print("Gaming 1 - 30% of applicants under-report income by 40%")
    grng = np.random.default_rng(83)
    g1 = dict(yr)
    liars = grng.random(N_NEW) < 0.30
    g1["income"] = np.where(liars, np.round(yr["income"] * 0.6), yr["income"])
    for nm, d in (("honest reports", yr), ("with under-reporting", g1)):
        sel = select(-d["income"], BUDGET, grng)
        print(f"  poorest first, {nm:22s} truly poorest-20% share={poorest_share(yr, sel):4.0%}  "
              f"under-reporters={np.mean(liars[sel]):4.0%}  gain/grant=${yr['tau'][sel].mean():5.1f}")
    print()

    # Gaming 2: once the rule is known, some new-shop owners claim 2+ years.
    print("Gaming 2 - 40% of owners of shops under 2 years claim 2-3 years")
    claim = np.where((yr["age"] < 2) & (grng.random(N_NEW) < 0.40),
                     np.round(grng.uniform(2.0, 3.0, N_NEW), 1), yr["age"])
    g2 = dict(yr); g2["claimed_age"] = claim
    for nm, field in (("shop age verified", "age"), ("shop age self-reported", "claimed_age")):
        sel = policies(g2, r2, e2, b1, b0, BUDGET, np.random.default_rng(84), age_field=field)["effect rule (depth 2)"]
        print(f"  effect rule, {nm:24s} gain/grant=${yr['tau'][sel].mean():5.1f}  "
              f"total=${yr['tau'][sel].mean()*BUDGET:7,.0f}/month  truly new shops={np.mean(yr['age'][sel]<2):4.0%}")


if __name__ == "__main__":
    main()
