"""Case 6 tutorial code: deciding, with basic statistics, that no optimization model is needed.

Every number quoted in docs/tutorials/06-no-model-food-pantry.md comes from running
this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case6_no_model_check.py

Only numpy and the standard library are needed. The pantry's record (150 households,
3 short weeks out of 52, short by about 10-20 boxes) comes from the case file. Everything
else (turnout rates, the size of supply disruptions, the share of priority households)
is made up for teaching and is labeled illustrative in the tutorial.
"""

import math

import numpy as np

# ------------------------------------------------------ the pantry's record ---
HOUSEHOLDS = 150          # registered households (case file)
WEEKS = 52                # weeks of records
SHORT_WEEKS = 3           # weeks the pantry ran short (case file)
SHORT_LOW, SHORT_HIGH = 10, 20   # "short by about 10-20 boxes" (case file)
END_OF_MONTH_WEEKS = 12   # one end-of-month week per calendar month

# ------------------------------------------------- illustrative assumptions ---
PRIORITY_SHARE = 0.30     # households with children under 5 or no other support
RECOGNIZED = 0.90         # share of priority households the sign-in volunteer recognizes
TURNOUT_ORDINARY = 0.78   # chance a registered household comes in an ordinary week
TURNOUT_END_OF_MONTH = 0.95
BOXES_ORDERED = 150       # boxes the pantry expects each week
DISRUPTION_CHANCE = 0.25  # chance a week's delivery comes up short ...
DISRUPTION_MIN, DISRUPTION_MAX = 18, 26   # ... by this many boxes
MONTH_LENGTHS = [4, 4, 5] * 4             # a 4-4-5 calendar: 12 months, 52 weeks
Z = 1.96                  # 95% two-sided normal multiplier


# ---------------------------------------------------------------- Estimates ---

def wald_interval(k, n, z=Z):
    """Textbook normal-approximation interval: p_hat +/- z * sqrt(p_hat(1-p_hat)/n)."""
    p = k / n
    half = z * math.sqrt(p * (1 - p) / n)
    return p - half, p + half


def wilson_interval(k, n, z=Z):
    """Wilson score interval: the set of p for which k/n is not surprising."""
    p = k / n
    centre = (p + z**2 / (2 * n)) / (1 + z**2 / n)
    half = (z / (1 + z**2 / n)) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return centre - half, centre + half


def binom_cdf(k, n, p):
    """P(X <= k) for X ~ Binomial(n, p)."""
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))


def bisect(f, lo, hi, iters=100):
    """Find x in [lo, hi] where the increasing function f crosses zero."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def exact_interval(k, n, alpha=0.05):
    """Clopper-Pearson 'exact' interval, found by searching the binomial distribution.

    Lower end: the p at which seeing k or more is just 2.5% likely.
    Upper end: the p at which seeing k or fewer is just 2.5% likely.
    """
    lower = 0.0 if k == 0 else bisect(lambda p: (1 - binom_cdf(k - 1, n, p)) - alpha / 2, 0, 1)
    upper = 1.0 if k == n else bisect(lambda p: alpha / 2 - binom_cdf(k, n, p), 0, 1)
    return lower, upper


def poisson_cdf(c, lam):
    return sum(math.exp(-lam) * lam**i / math.factorial(i) for i in range(c + 1))


def poisson_interval(count, weeks, alpha=0.05):
    """Exact 95% interval for a weekly rate, from `count` events in `weeks` weeks."""
    if count == 0:  # one-sided upper bound: P(0 events) = 5%
        return 0.0, -math.log(alpha) / weeks
    lower = bisect(lambda lam: (1 - poisson_cdf(count - 1, lam)) - alpha / 2, 0, 10 * count + 10)
    upper = bisect(lambda lam: alpha / 2 - poisson_cdf(count, lam), 0, 10 * count + 10)
    return lower / weeks, upper / weeks


# --------------------------------------------------------------- Scaling up ---

def p_month_flag(p, weeks=4):
    """Chance a month has MORE THAN ONE short week, if each week is short with chance p."""
    return 1 - (1 - p)**weeks - weeks * p * (1 - p)**(weeks - 1)


def p_fires_in_year(p, month_lengths=MONTH_LENGTHS, run=3):
    """Chance the trigger (a flagged month `run` months running) fires within a year.

    Tracks the probability of each current run length (0, 1, 2 flagged months in a row).
    """
    state = np.zeros(run)
    state[0] = 1.0
    fired = 0.0
    for w in month_lengths:
        f = p_month_flag(p, w)
        new = np.zeros(run)
        new[0] = state.sum() * (1 - f)          # an unflagged month resets the run
        new[1:] = state[:-1] * f                # a flagged month extends it
        fired += state[-1] * f                  # a run of `run` months: the trigger fires
        state = new
    return fired


def p_quarter_count(p, weeks=13, at_least=3):
    """Alternative check: chance of `at_least` short weeks in a 13-week quarter."""
    return 1 - binom_cdf(at_least - 1, weeks, p)


# --------------------------------------------------------------- Simulation ---

def simulate(years, households=HOUSEHOLDS, seed=6):
    """Simulate `years` years of weekly turnout and supply. Returns per-week arrays."""
    rng = np.random.default_rng(seed)
    end_of_month = np.zeros(WEEKS, dtype=bool)
    end_of_month[np.cumsum(MONTH_LENGTHS) - 1] = True
    turnout = np.where(end_of_month, TURNOUT_END_OF_MONTH, TURNOUT_ORDINARY)
    n_priority = round(PRIORITY_SHARE * households)
    priority_come = rng.binomial(n_priority, turnout, size=(years, WEEKS))
    others_come = rng.binomial(households - n_priority, turnout, size=(years, WEEKS))
    demand = priority_come + others_come
    disrupted = rng.random((years, WEEKS)) < DISRUPTION_CHANCE
    cut = rng.integers(DISRUPTION_MIN, DISRUPTION_MAX + 1, size=(years, WEEKS))
    supply = BOXES_ORDERED - disrupted * cut
    return demand, priority_come, supply, end_of_month, rng


def trigger_fires(short):
    """Case trigger on a (years, 52) array of short-week flags: >1 short week in a month,
    three months running, at any point in the year."""
    starts = np.concatenate([[0], np.cumsum(MONTH_LENGTHS)[:-1]])
    flagged = np.stack([short[:, s:s + w].sum(axis=1) > 1
                        for s, w in zip(starts, MONTH_LENGTHS)], axis=1)
    runs = flagged[:, :-2] & flagged[:, 1:-1] & flagged[:, 2:]
    return runs.any(axis=1)


def quarter_check_fires(short):
    """Alternative check: 3 or more short weeks in any 13-week quarter of the year."""
    return (short.reshape(short.shape[0], 4, 13).sum(axis=2) >= 3).any(axis=1)


def allocation_outcomes(demand, priority_come, supply, rng):
    """Per year: boxes that priority households went without, under three ways of
    handling a short week. A household sent home empty misses 1 box; a household given
    a smaller box misses the part of a box it didn't get."""
    short = supply < demand
    d, dp, s = demand[short], priority_come[short], supply[short]
    turned_away = d - s
    # No rule: first come, first served; the last arrivals go home with nothing.
    # The number of priority households among them follows a hypergeometric draw.
    no_rule_priority = rng.hypergeometric(dp, d - dp, turned_away)
    # Written rule, as applied: recognized priority households get full boxes first;
    # everyone else (including unrecognized priority households) shares what is left.
    recognized = rng.binomial(dp, RECOGNIZED)
    full = np.minimum(recognized, s)
    smaller_box = (s - full) / (d - full)
    rule_missed = (dp - full) * (1 - smaller_box)
    # Perfect allocator: knows every household's status, but can't create boxes.
    perfect_missed = np.maximum(0, dp - s)
    years = demand.shape[0]
    return {
        "short weeks": short.sum() / years,
        "boxes short": turned_away.sum() / years,
        "no rule": no_rule_priority.sum() / years,
        "rule": rule_missed.sum() / years,
        "perfect": perfect_missed.sum() / years,
        "unrecognized": (dp - full).sum() / years,
        "smaller box": smaller_box.mean(),
    }


def main():
    p_hat = SHORT_WEEKS / WEEKS
    print("Estimates - how often is the pantry short? (3 short weeks out of 52)")
    print(f"  estimate p_hat = {SHORT_WEEKS}/{WEEKS} = {p_hat:.4f} "
          f"(standard error {math.sqrt(p_hat * (1 - p_hat) / WEEKS):.4f})")
    for name, fn in (("normal approx (Wald)", wald_interval),
                     ("Wilson", wilson_interval),
                     ("exact (Clopper-Pearson)", exact_interval)):
        lo, hi = fn(SHORT_WEEKS, WEEKS)
        print(f"  {name:24s} 95% CI = ({lo:+.4f}, {hi:.4f})  -> {lo * 52:+.1f} to {hi * 52:.1f} short weeks/year")

    print("\nEstimates - how big is the shortfall?")
    total = HOUSEHOLDS * WEEKS
    mid = (SHORT_LOW + SHORT_HIGH) / 2
    for size in (SHORT_LOW, mid, SHORT_HIGH):
        print(f"  {SHORT_WEEKS} weeks x {size:4.1f} boxes = {SHORT_WEEKS * size:5.1f} boxes/year "
              f"= {100 * SHORT_WEEKS * size / total:.2f}% of {total:,} boxes")
    wilson_hi = wilson_interval(SHORT_WEEKS, WEEKS)[1]
    worst = wilson_hi * WEEKS * SHORT_HIGH
    print(f"  pessimistic: Wilson upper rate {wilson_hi:.4f} x 52 x {SHORT_HIGH} boxes "
          f"= {worst:.0f} boxes/year = {100 * worst / total:.2f}%")

    print("\nEstimates - is it an end-of-month problem?")
    chance = math.comb(END_OF_MONTH_WEEKS, 3) / math.comb(WEEKS, 3)
    print(f"  P(all 3 short weeks fall in the 12 end-of-month weeks by chance) = "
          f"C(12,3)/C(52,3) = {math.comb(12, 3)}/{math.comb(52, 3)} = {chance:.4f}")
    for label, k, n in (("end-of-month weeks", 3, 12), ("other weeks", 0, 40)):
        lo, hi = wilson_interval(k, n)
        lo = max(0.0, lo)  # exactly 0 when k = 0; avoid printing -0.000
        print(f"  {label:18s} {k}/{n} = {k / n:.3f}, Wilson 95% CI ({lo:.3f}, {hi:.3f})")

    print("\nEstimates - hidden demand: recording turn-aways for 3 months (13 weeks)")
    for count in (0, 13):
        lo, hi = poisson_interval(count, 13)
        print(f"  {count:2d} turn-aways recorded: rate {count / 13:.2f}/week, 95% CI ({lo:.2f}, {hi:.2f}) "
              f"-> up to {hi * 52:.0f} households/year")

    print("\nDecision engine - step-by-step example of one short week (illustrative)")
    demand, supply = 140, 125
    priority = round(PRIORITY_SHARE * demand)
    others = demand - priority
    print(f"  demand {demand}, supply {supply}, short by {demand - supply}; priority households {priority}")
    print(f"  no rule: {demand - supply} households leave with nothing; expected priority among them "
          f"= {demand - supply} x {PRIORITY_SHARE} = {(demand - supply) * PRIORITY_SHARE:.1f}")
    print(f"  rule: {priority} full boxes; {others} others share {supply - priority} boxes "
          f"= {(supply - priority) / others:.3f} of a box each")
    print(f"  per year at 3 short weeks: priority households protected = "
          f"{SHORT_WEEKS * (demand - supply) * PRIORITY_SHARE:.1f}")
    print(f"  expected households short per week = {p_hat:.4f} x {mid:.0f} = {p_hat * mid:.2f}")
    print(f"  illustrative tool upkeep: {HOUSEHOLDS} households x 1 minute x 52 weeks "
          f"= {HOUSEHOLDS * 52 / 60:.0f} volunteer-hours/year")
    print(f"  illustrative buffer: {SHORT_HIGH} extra boxes x {END_OF_MONTH_WEEKS} end-of-month weeks "
          f"= {SHORT_HIGH * END_OF_MONTH_WEEKS} boxes/year")

    print("\nScaling up - how unusual is the revisit trigger at today's rate?")
    p = p_hat
    q4 = (1 - p)**4
    one = 4 * p * (1 - p)**3
    f = p_month_flag(p)
    print(f"  P(0 short of 4) = {q4:.4f}, P(1 short of 4) = {one:.4f}, "
          f"P(more than 1) = {f:.4f}")
    print(f"  three months running = {f:.4f}^3 = {f**3:.2e}")
    print("  weekly short rate | P(month flagged) | P(3 months running) | P(fires in a year) | "
          "P(>=3 short in a quarter) | P(quarter check fires in a year)")
    for rate in (p_hat, 0.10, 0.15, 0.25, 0.35, 0.50):
        fq = p_quarter_count(rate)
        print(f"  {rate:17.4f} | {p_month_flag(rate):16.4f} | {p_month_flag(rate)**3:19.4f} | "
              f"{p_fires_in_year(rate):18.4f} | {fq:25.4f} | {1 - (1 - fq)**4:.4f}")

    print("\nSimulation - simulated pantry (illustrative), 10,000 years each")
    for label, households in (("today (150 households)", 150),
                              ("demand +10% (165 households)", 165),
                              ("demand +20% (180 households)", 180)):
        demand_w, prio_w, supply_w, eom, rng = simulate(10_000, households)
        short = supply_w < demand_w
        eom_share = short[:, eom].sum() / short.sum()
        print(f"  {label:29s} short weeks/yr {short.sum(axis=1).mean():5.2f}  "
              f"(end-of-month share {eom_share:.2f})  "
              f"mean shortfall {(demand_w - supply_w)[short].mean():5.1f} boxes  "
              f"case trigger fires {trigger_fires(short).mean():.4f}  "
              f"quarter check fires {quarter_check_fires(short).mean():.4f}")

    print("\nSimulation - who bears a short week? (today, per year, illustrative)")
    demand_w, prio_w, supply_w, _, rng = simulate(10_000, 150)
    out = allocation_outcomes(demand_w, prio_w, supply_w, rng)
    print(f"  short weeks {out['short weeks']:.2f}, boxes short {out['boxes short']:.1f}")
    print(f"  households sent home with nothing: no rule {out['boxes short']:.1f} "
          f"(of them priority {out['no rule']:.2f}), written rule 0")
    print(f"  average smaller box under the rule, in short weeks: {out['smaller box']:.3f} of a full box")
    print(f"  unrecognized priority households given a smaller box: {out['unrecognized']:.2f}")
    print(f"  boxes priority households went without: no rule {out['no rule']:.2f}, "
          f"written rule {out['rule']:.2f}, perfect allocator {out['perfect']:.2f}")
    print(f"  most a perfect allocator could add: over the written rule "
          f"{out['rule'] - out['perfect']:.2f} boxes/year, over no rule {out['no rule'] - out['perfect']:.2f}")


if __name__ == "__main__":
    main()
