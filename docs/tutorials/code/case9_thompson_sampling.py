"""Case 9 tutorial code: an adaptive experiment across four SMS reminder wordings.

Every number quoted in docs/tutorials/09-adaptive-experiments-sms-reminders.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case9_thompson_sampling.py

It needs only numpy. Each wording's on-time rate gets a Beta posterior; the
probability that each wording is best is computed by numerical integration on a
grid (no random draws), so it is exact to about three decimal places. The "true"
on-time rates and the parents' outcomes are synthetic, generated with fixed random
seeds; they are made up for teaching. The output is the same on every run.
"""

import numpy as np

WORDINGS = ["A", "B", "C", "D"]        # A = current plain reminder (the control)
PARENTS_PER_WEEK = 400                 # new parents entering the list each week
FLOOR = np.array([0.20, 0.10, 0.10, 0.10])  # A: fixed 20% control; B-D: 10% floor each
ADAPTIVE = 1.0 - FLOOR.sum()           # the 50% that moves with the data
STOP_PROB = 0.95                       # stop when one wording is >= 95% likely best
MAX_WEEKS = 10                         # ... or after 10 weeks
LAG = 2                                # week t's shares use outcomes from weeks <= t-2
SEASON_WEEKS = 26                      # half a year: the experiment, then the winner
PRIOR = (1.0, 1.0)                     # Beta(1, 1): every on-time rate equally plausible

# Illustrative "true" on-time rates (share vaccinated within 7 days of the due date).
# Nobody knows these in practice; the simulation uses them to score each design.
TRUE_RATES = np.array([0.60, 0.67, 0.62, 0.64])

GRID = (np.arange(2000) + 0.5) / 2000  # rate values 0.00025, 0.00075, ..., 0.99975
LOG_X, LOG_1MX = np.log(GRID), np.log1p(-GRID)


# ------------------------------------------------------------- Beta posterior ---

def posterior_grid(succ, fail):
    """Posterior density and CDF of each wording's rate on the grid.

    succ, fail: arrays (..., 4) of on-time / not-on-time counts. Returns
    (weights, cdf), each shaped (..., 4, G), with weights summing to 1."""
    a = np.asarray(succ, float)[..., None] + PRIOR[0]
    b = np.asarray(fail, float)[..., None] + PRIOR[1]
    logw = (a - 1) * LOG_X + (b - 1) * LOG_1MX
    w = np.exp(logw - logw.max(axis=-1, keepdims=True))
    w /= w.sum(axis=-1, keepdims=True)
    cdf = np.cumsum(w, axis=-1) - w / 2          # mid-point rule
    return w, cdf


def prob_best(succ, fail):
    """P(wording k has the highest true rate), for each k.

    P(k best) = sum over x of density_k(x) * product over j != k of P(rate_j < x)."""
    w, cdf = posterior_grid(succ, fail)
    out = []
    for k in range(4):
        others = np.prod(np.delete(cdf, k, axis=-2), axis=-2)
        out.append((w[..., k, :] * others).sum(axis=-1))
    p = np.stack(out, axis=-1)
    return p / p.sum(axis=-1, keepdims=True)


def prob_beats_a(succ, fail):
    """P(wording k's true rate is above wording A's), for each k (A gets 0)."""
    w, cdf = posterior_grid(succ, fail)
    p = (w * cdf[..., 0:1, :]).sum(axis=-1)
    p[..., 0] = 0.0
    return p


def credible_interval(s, f, level=0.95):
    """Central 95% credible interval of one Beta posterior, read off the grid CDF."""
    _, cdf = posterior_grid(np.array([s, 0, 0, 0]), np.array([f, 0, 0, 0]))
    lo = GRID[np.searchsorted(cdf[0], (1 - level) / 2)]
    hi = GRID[np.searchsorted(cdf[0], 1 - (1 - level) / 2)]
    return lo, hi


# ------------------------------------------------------------ Assignment rules ---

def thompson_weights(p_best):
    """Thompson sampling: share proportional to the probability of being best."""
    return p_best


def exploration_weights(p_best):
    """Exploration sampling (Kasy & Sautmann 2021): share proportional to p(1 - p).

    A wording that is surely best (p near 1) or surely not (p near 0) gets little;
    close contenders get the most, so the final pick is more reliable."""
    q = p_best * (1 - p_best)
    total = q.sum(axis=-1, keepdims=True)
    return np.where(total > 0, q / np.where(total > 0, total, 1), 0.25)


def shares_with_guards(weights):
    """Apply the guards: 20% fixed on A, 10% floor on B-D, the other 50% adaptive."""
    return FLOOR + ADAPTIVE * weights


def counts_from_shares(shares, n=PARENTS_PER_WEEK):
    """Whole numbers of parents per wording that add to n (largest remainder)."""
    raw = shares * n
    base = np.floor(raw).astype(int)
    short = n - base.sum(axis=-1)
    order = np.argsort(-(raw - base), axis=-1, kind="stable")
    for r in range(base.shape[0]):
        base[r, order[r, :short[r]]] += 1
    return base


def final_choice(succ, fail):
    """Decision at the 10-week cap, from the data in hand.

    Pick the wording that is >= 95% likely best; failing that, switch to the top
    wording only if it is >= 95% likely to beat A; otherwise keep A."""
    pb = prob_best(succ, fail)
    top = pb.argmax(axis=-1)
    beats = prob_beats_a(succ, fail)[np.arange(len(top)), top]
    clear = pb.max(axis=-1) >= STOP_PROB
    return np.where(clear | (beats >= STOP_PROB), top, 0)


# ------------------------------------------------------------------ Hand example ---

def hand_example():
    print("Hand example - two weeks of results, prior Beta(1, 1)")
    start = counts_from_shares(shares_with_guards(np.full((1, 4), 0.25)))[0]
    print(f"  starting shares (no data yet): "
          + "  ".join(f"{w}={s:.1%}" for w, s in
                      zip(WORDINGS, shares_with_guards(np.full(4, 0.25))))
          + f"  -> parents per week {dict(zip(WORDINGS, start.tolist()))}")
    # Illustrative results: on-time out of sent, for weeks 1 and 2 (same counts sent,
    # because week 2 goes out before any week-1 outcome is known).
    week_succ = [np.array([78, 61, 55, 58]), np.array([80, 62, 54, 56])]
    succ, fail = np.zeros(4), np.zeros(4)
    for wk, ws in enumerate(week_succ, start=1):
        succ = succ + ws
        fail = fail + (start - ws)
        n = succ + fail
        print(f"\n  After week {wk} results (used for week {wk + LAG} shares):")
        print("    wording  on-time/sent  rate   posterior      mean    95% credible   "
              "usual 95% CI (p +/- 1.96 se)")
        for k, w in enumerate(WORDINGS):
            a, b = succ[k] + PRIOR[0], fail[k] + PRIOR[1]
            p = succ[k] / n[k]
            se = np.sqrt(p * (1 - p) / n[k])
            lo, hi = credible_interval(succ[k], fail[k])
            print(f"    {w}        {int(succ[k]):>3}/{int(n[k]):<3}       {p:.3f}  "
                  f"Beta({int(a)},{int(b)})  {a / (a + b):.3f}   {lo:.3f} to {hi:.3f}   "
                  f"{p - 1.96 * se:.3f} to {p + 1.96 * se:.3f}")
        pb = prob_best(succ, fail)
        th = shares_with_guards(thompson_weights(pb))
        ex = shares_with_guards(exploration_weights(pb))
        print("    P(best):           " + "  ".join(f"{w}={p:.3f}" for w, p in zip(WORDINGS, pb)))
        print("    p(1-p) weights:    " + "  ".join(f"{w}={p:.3f}" for w, p in
                                                   zip(WORDINGS, exploration_weights(pb))))
        print("    Thompson shares:    " + "  ".join(f"{w}={s:.1%}" for w, s in zip(WORDINGS, th))
              + f"   parents {counts_from_shares(th[None])[0].tolist()}")
        print("    Exploration shares: " + "  ".join(f"{w}={s:.1%}" for w, s in zip(WORDINGS, ex))
              + f"   parents {counts_from_shares(ex[None])[0].tolist()}")
        print(f"    P(beats A):        " + "  ".join(
            f"{w}={p:.3f}" for w, p in zip(WORDINGS[1:], prob_beats_a(succ, fail)[1:])))
        if wk == 1:
            # Thompson sampling the "one draw per parent" way gives the same split.
            rng = np.random.default_rng(9)
            a = succ + PRIOR[0]
            b = fail + PRIOR[1]
            draws = rng.beta(a, b, size=(PARENTS_PER_WEEK, 4))
            wins = np.bincount(draws.argmax(axis=1), minlength=4)
            print(f"    one draw per parent, 400 parents -> wins {dict(zip(WORDINGS, wins.tolist()))}"
                  f"  vs 400 x P(best) = {dict(zip(WORDINGS, np.round(400 * pb).astype(int).tolist()))}")


# ------------------------------------------------------------------ Simulation ---

def simulate(design, rates, reps, seed):
    """Run one design `reps` times. Returns per-rep results as a dict of arrays.

    design: "equal" (fixed 25% each for 10 weeks), "thompson" or "exploration"
    (shares from the data, with the guards and the stopping rule)."""
    rng = np.random.default_rng(seed)
    sent = np.zeros((reps, MAX_WEEKS, 4), int)       # parents per wording per week
    ontime = np.zeros((reps, MAX_WEEKS, 4), int)     # on-time vaccinations observed
    stopped_at = np.full(reps, MAX_WEEKS)           # weeks run with experimental shares
    winner = np.full(reps, -1)
    for t in range(MAX_WEEKS):                       # t = 0 is week 1
        seen = max(0, t - LAG + 1)                   # weeks whose outcomes are in
        succ = ontime[:, :seen].sum(axis=1)
        fail = sent[:, :seen].sum(axis=1) - succ
        active = winner < 0
        if design == "equal":
            shares = np.full((reps, 4), 0.25)
        else:
            pb = prob_best(succ, fail)
            if seen > 0:                             # the stopping rule
                newly = active & (pb.max(axis=1) >= STOP_PROB)
                winner[newly] = pb[newly].argmax(axis=1)
                stopped_at[newly] = t
                active = winner < 0
            w = thompson_weights(pb) if design == "thompson" else exploration_weights(pb)
            shares = shares_with_guards(w)
        n = counts_from_shares(shares)
        done = ~active                               # after stopping: winner to everyone
        n[done] = 0
        n[done, winner[done]] = PARENTS_PER_WEEK
        sent[:, t] = n
        ontime[:, t] = rng.binomial(n, rates)
    # At the cap: decide from the outcomes in hand (weeks 1..MAX_WEEKS-LAG+1).
    seen = MAX_WEEKS - LAG + 1
    succ = ontime[:, :seen].sum(axis=1)
    fail = sent[:, :seen].sum(axis=1) - succ
    undecided = winner < 0
    winner[undecided] = final_choice(succ[undecided], fail[undecided])
    total_sent = sent.sum(axis=1)
    return {
        "sent": total_sent,
        # Expected on-time vaccinations (true rate x parents sent): less noisy than
        # counting simulated outcomes, and the same on average.
        "exp_10wk": (total_sent * rates).sum(axis=1),
        "exp_season": (total_sent * rates).sum(axis=1)
        + (SEASON_WEEKS - MAX_WEEKS) * PARENTS_PER_WEEK * rates[winner],
        "winner": winner,
        "stopped_at": stopped_at,
        "stopped_early": ~undecided,
        "succ": succ, "fail": fail,
    }


def report(rates, reps, seed, title):
    best = int(np.argmax(rates))
    tie = np.all(rates == rates[0])          # no true best: "pick best" is meaningless
    print(f"\n{title}")
    print(f"  true on-time rates: " + "  ".join(f"{w}={r:.2f}" for w, r in zip(WORDINGS, rates))
          + f"   ({reps:,} replications of a {MAX_WEEKS}-week run, {PARENTS_PER_WEEK} parents/week)")
    print(f"  benchmarks over 10 weeks (4,000 parents): all-A = {4000 * rates[0]:,.0f} on time,"
          f"  all-best = {4000 * rates.max():,.0f},  equal split = {4000 * rates.mean():,.0f}")
    res = {d: simulate(d, rates, reps, seed) for d in ("equal", "thompson", "exploration")}
    base10 = res["equal"]["exp_10wk"].mean()
    base26 = res["equal"]["exp_season"].mean()
    names = {"equal": "equal split 25% each", "thompson": "Thompson + guards",
             "exploration": "exploration sampling + guards"}
    print("  design                          on-time,10wk  extra vs equal  on-time,26wk  "
          "extra vs equal  pick best  keep A  stop<10wk  mean weeks")
    for d, r in res.items():
        picks = np.bincount(r["winner"], minlength=4) / reps
        print(f"  {names[d]:<31} {r['exp_10wk'].mean():>10,.0f}  {r['exp_10wk'].mean() - base10:>+12,.0f}"
              f"  {r['exp_season'].mean():>12,.0f}  {r['exp_season'].mean() - base26:>+12,.0f}"
              f"  {'n/a' if tie else f'{picks[best]:.1%}':>9}  {picks[0]:>6.1%}  {r['stopped_early'].mean():>8.1%}"
              f"  {r['stopped_at'].mean():>9.1f}")
    print("  final pick, share of replications:")
    for d, r in res.items():
        picks = np.bincount(r["winner"], minlength=4) / reps
        print(f"    {names[d]:<31} " + "  ".join(f"{w}={p:.1%}" for w, p in zip(WORDINGS, picks)))
    print("  parents sent each wording over 10 weeks (average), and 95% CI half-width"
          " for wording C at the decision:")
    for d, r in res.items():
        n = r["succ"] + r["fail"]
        p = np.clip(r["succ"][:, 2] / np.maximum(n[:, 2], 1), 0, 1)
        half = 1.96 * np.sqrt(p * (1 - p) / np.maximum(n[:, 2], 1))
        print(f"    {names[d]:<31} " + "  ".join(f"{w}={v:,.0f}" for w, v in
                                                 zip(WORDINGS, r["sent"].mean(axis=0)))
              + f"   C: +/-{half.mean():.3f}")
    return res


def main():
    hand_example()
    print("\nWhy an equal split is costly - one week, 400 parents, true rates "
          + "  ".join(f"{w}={r:.2f}" for w, r in zip(WORDINGS, TRUE_RATES)))
    eq = PARENTS_PER_WEEK * TRUE_RATES.mean()
    print(f"  equal split: {eq:.0f} on time;  all on best wording: "
          f"{PARENTS_PER_WEEK * TRUE_RATES.max():.0f};  shortfall {PARENTS_PER_WEEK * TRUE_RATES.max() - eq:.0f}"
          f" per week, {MAX_WEEKS * (PARENTS_PER_WEEK * TRUE_RATES.max() - eq):.0f} over 10 weeks")
    report(TRUE_RATES, reps=2000, seed=2021,
           title="Simulation 1 - wordings differ (B is best)")
    report(np.array([0.60, 0.60, 0.60, 0.60]), reps=2000, seed=2024,
           title="Simulation 2 - no real difference (all four equal)")
    report(np.array([0.60, 0.62, 0.61, 0.61]), reps=2000, seed=1,
           title="Simulation 3 - small differences (B best by 1-2 points)")


if __name__ == "__main__":
    main()
