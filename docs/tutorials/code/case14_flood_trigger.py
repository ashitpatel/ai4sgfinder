"""Case 14 tutorial code: a forecast trigger for cash before a river flood, plus the list.

Every number quoted in docs/tutorials/14-anticipatory-cash-flood-trigger.md comes from
running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case14_flood_trigger.py

It needs numpy and PuLP 3 (which ships with the free CBC solver). The program is
illustrative: the river, the twelve "recorded" seasons, the forecast errors, the value
of a transfer and the 40,000 surveyed households are all made up for teaching.

Layer 1, the trigger (Class 4, the primary decision): at what forecast level to release
$500,000 to 10,000 households before the peak. Six rules:
  A. pay after       - last year's practice: pay once the severe flood has passed
  B. danger level    - release on the first forecast above the danger level
  C. calculator      - a threshold read off a table of the twelve recorded seasons
  D. expected value  - best average under a forecast model fitted to the record
  E. robust          - best worst case over every forecast model the record can't rule out
  F. robust + 20% reserve
Layer 2, the list (Class 2): which 10,000 of 40,000 households receive the transfer.
"""

import time

import numpy as np
import pulp

rng = np.random.default_rng(14)

# ============================================================ The river ===
# Levels are in cm above the gauge's danger level. A wave peaking at +100 cm or more is
# a severe flood. Each monsoon has three flood waves; the forecast service issues a
# 5-day-ahead forecast of each wave's peak.
SEVERE = 100
WAVES = 3
HOUSEHOLDS_PAID = 10_000

# What a $50 transfer is worth, in units of "a transfer that arrives before a severe peak".
# Illustrative values chosen for teaching, not estimates from any study.
V_EARLY = 1.00   # paid on the forecast of the severe wave, before its peak
V_TOO_SOON = 0.30  # paid on an earlier, smaller wave; spent before the severe one came
V_FALSE = 0.10   # paid, and no severe flood came this season (a false alarm)
V_LATE = 0.35    # paid after the severe peak (last year's practice)
V_HELD = 0.35    # not paid this season; returned to the donor for another use


def seasons(n, shift=0.0, bias=-5.0, sd=30.0, underpredict=0.0, blind=0.0, gen=rng):
    """Simulate n monsoons: actual wave peaks h and 5-day forecasts f, both (n, WAVES).

    shift        - a wetter (+) or drier (-) climate, in cm added to every peak
    bias, sd     - forecast error = forecast - actual ~ Normal(bias, sd)
    underpredict - forecasts of big waves fall short by this share of the peak above +50
    blind        - chance that a severe wave's 5-day forecast misses the rise entirely
    """
    wet = gen.normal(0, 45, size=(n, 1))
    h = wet + gen.normal(30, 35, size=(n, WAVES)) + shift
    f = h + gen.normal(bias, sd, size=h.shape)
    f -= underpredict * np.maximum(h - 50, 0)
    if blind:
        miss = (h >= SEVERE) & (gen.random(h.shape) < blind)
        f[miss] = gen.normal(-20, 20, size=miss.sum())
    return h, f


def outcomes(h, f, T, reserve=0.0):
    """Score a trigger at forecast level T on seasons (h, f).

    Returns per-season value (average over the 10,000 transfers) and the counts that the
    calculator table uses: hit, too soon, missed, false alarm."""
    sev = h >= SEVERE
    any_sev = sev.any(axis=1)
    first_sev = np.where(any_sev, sev.argmax(axis=1), WAVES)
    fired = f >= T
    any_fire = fired.any(axis=1)
    first_fire = np.where(any_fire, fired.argmax(axis=1), WAVES)

    hit = any_sev & (first_fire == first_sev)
    too_soon = any_sev & (first_fire < first_sev)
    missed = any_sev & (first_fire > first_sev)
    false_alarm = any_fire & ~any_sev

    early = np.select([hit, too_soon, false_alarm], [V_EARLY, V_TOO_SOON, V_FALSE], V_LATE)
    early = np.where(~any_fire & ~any_sev, V_HELD, early)
    value = (1 - reserve) * early + reserve * V_LATE   # reserve: paid late, or held (same value)
    return value, hit, too_soon, missed, false_alarm


def summary(h, f, T, reserve=0.0):
    value, hit, soon, miss, fa = outcomes(h, f, T, reserve)
    sev = (h >= SEVERE).any(axis=1)
    return {"value": value.mean(),
            "hit": hit.sum() / max(sev.sum(), 1),
            "fa": fa.sum() / max((~sev).sum(), 1),
            "soon": soon.sum() / max(sev.sum(), 1)}


def wilson(k, n, z=1.96):
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


THRESHOLDS = list(range(0, 181, 20))

# ======================================================= The record ===
# Twelve seasons drawn from the "true" river; the seed is chosen so that 3 were severe.
for seed in range(1000):
    H, F = seasons(12, gen=np.random.default_rng(seed))
    if (H >= SEVERE).any(axis=1).sum() == 3:
        break
REC_SEV = (H >= SEVERE).any(axis=1)

print("The record - twelve monsoons at the main gauge (cm above danger level)")
print("  season   5-day forecasts (wave 1, 2, 3)   actual peaks (wave 1, 2, 3)   severe?")
for s in range(12):
    fs = " ".join(f"{v:5.0f}" for v in F[s])
    hs = " ".join(f"{v:5.0f}" for v in H[s])
    print(f"  {2013 + s}     {fs}                {hs}                {'yes' if REC_SEV[s] else ''}")
errors = (F - H).ravel()
b_hat, s_hat = errors.mean(), errors.std(ddof=1)
print(f"  forecast error (forecast - actual), 36 waves: mean={b_hat:+.1f} cm, sd={s_hat:.1f} cm")

# ===================================================== Estimates ===
print()
print("Estimates - how much twelve seasons can say")
lo, hi = wilson(3, 12)
print(f"  severe seasons: 3 of 12 = {3/12:.0%}, 95% Wilson interval {lo:.0%} to {hi:.0%}")
se_b = s_hat / np.sqrt(36)
print(f"  forecast bias: {b_hat:+.1f} cm, 95% interval {b_hat - 1.96*se_b:+.1f} to {b_hat + 1.96*se_b:+.1f}")
# chi-square interval for the sd with 35 degrees of freedom (values from tables)
CHI_LO, CHI_HI = 20.57, 53.20
s_lo, s_hi = s_hat * np.sqrt(35 / CHI_HI), s_hat * np.sqrt(35 / CHI_LO)
print(f"  forecast error sd: {s_hat:.1f} cm, 95% interval {s_lo:.1f} to {s_hi:.1f}")
sev_err = (F - H)[H >= SEVERE]
print(f"  errors on the {len(sev_err)} severe waves alone: {', '.join(f'{e:+.0f}' for e in sev_err)}")

# cost-loss rule: act on a wave when P(severe) > cost of a false alarm / (cost + gain of a hit)
p_star = (V_HELD - V_FALSE) / ((V_HELD - V_FALSE) + (V_EARLY - V_LATE))
print(f"  break-even chance of a severe flood (cost-loss ratio): {p_star:.3f}")

# ================================================ Decision engine ===
print()
print("Decision engine - the calculator table over the twelve seasons")
print("     T   fired  hits  too soon  missed  false alarms  value/season")
calc_rows = []
for T in THRESHOLDS:
    v, hit, soon, miss, fa = outcomes(H, F, T)
    fired = (F >= T).any(axis=1).sum()
    calc_rows.append((T, hit.sum(), soon.sum(), miss.sum(), fa.sum(), v.mean()))
    print(f"  {T:4d}   {fired:5d}  {hit.sum():4d}  {soon.sum():8d}  {miss.sum():6d}  {fa.sum():12d}  {v.mean():12.3f}")
FA_LIMIT = 3   # the donor accepts about one false alarm in four seasons
ok = [r for r in calc_rows if r[4] <= FA_LIMIT]
# fewest misses and too-soon releases; then fewest false alarms; then, between thresholds the
# record can't tell apart, the lower one (it gives more warning of a flood the record lacks)
T_CALC = min(ok, key=lambda r: (r[2] + r[3], r[4], r[0]))[0]
best_key = min((r[2] + r[3], r[4]) for r in ok)
tied = [r[0] for r in ok if (r[2] + r[3], r[4]) == best_key]
T_CALC_HIGH = max(tied)
print(f"  calculator choice (fewest misses + too-soon with <= {FA_LIMIT} false alarms): T = {T_CALC}"
      f"  (the record can't tell apart: {tied})")

# Expected value: resample the twelve seasons' actual peaks and add fitted forecast errors.
def record_model(n, shift=0.0, bias=b_hat, sd=s_hat, underpredict=0.0, gen=None):
    gen = gen or np.random.default_rng(1)
    idx = gen.integers(0, 12, size=n)
    h = H[idx] + shift
    f = h + gen.normal(bias, sd, size=h.shape) - underpredict * np.maximum(h - 50, 0)
    return h, f

N_PLAN = 20_000
ev = {T: outcomes(*record_model(N_PLAN), T)[0].mean() for T in THRESHOLDS}
T_EV = max(ev, key=ev.get)
print("  expected value under the fitted model: " +
      "  ".join(f"T={T}:{v:.3f}" for T, v in ev.items()))
print(f"  expected-value choice: T = {T_EV}")

# Robust: every combination the record can't rule out, plus two expert scenarios.
# A climate shift that moves the share of severe seasons to the Wilson bounds:
def severe_share(shift):
    h, _ = record_model(N_PLAN, shift=shift)
    return (h >= SEVERE).any(axis=1).mean()

def shift_for(target):
    lo_s, hi_s = -150.0, 150.0
    for _ in range(40):
        mid = (lo_s + hi_s) / 2
        lo_s, hi_s = (mid, hi_s) if severe_share(mid) < target else (lo_s, mid)
    return (lo_s + hi_s) / 2

SH_LO, SH_HI = shift_for(lo), shift_for(hi)
print(f"  climate shifts matching the interval for severe seasons: {SH_LO:+.0f} cm and {SH_HI:+.0f} cm")
PLAUSIBLE = [dict(shift=sh, bias=b, sd=sd)
             for sh in (SH_LO, 0.0, SH_HI)
             for b in (b_hat - 1.96 * se_b, b_hat, b_hat + 1.96 * se_b)
             for sd in (s_lo, s_hat, s_hi)]
EXPERT = [dict(underpredict=0.4), dict(shift=SH_HI, underpredict=0.4)]
PLAN_SET = PLAUSIBLE + EXPERT


def plan_values(reserve=0.0):
    """Value of every threshold under every forecast model in the planning set."""
    return np.array([[outcomes(*record_model(N_PLAN, gen=np.random.default_rng(7), **sc), T, reserve)[0].mean()
                      for T in THRESHOLDS] for sc in PLAN_SET])


PV = plan_values()
BEST = PV.max(axis=1, keepdims=True)          # the best threshold's value, model by model
REGRET = BEST - PV                            # how far each threshold falls short of it
rob = dict(zip(THRESHOLDS, REGRET.max(axis=0)))
T_ROB = min(rob, key=rob.get)
print(f"  planning set: {len(PLAUSIBLE)} plausible forecast models + {len(EXPERT)} expert scenarios")
print(f"  best threshold, model by model: ranges from T={min(THRESHOLDS[i] for i in PV.argmax(axis=1))}"
      f" to T={max(THRESHOLDS[i] for i in PV.argmax(axis=1))}")
print("  largest shortfall from each model's best threshold (max regret): " +
      "  ".join(f"T={T}:{v:.3f}" for T, v in rob.items()))
print(f"  robust choice (smallest max regret): T = {T_ROB}")
print("  worst-case value over the set: " +
      "  ".join(f"T={T}:{v:.3f}" for T, v in zip(THRESHOLDS, PV.min(axis=0))))
j = THRESHOLDS.index(T_ROB)
for r in (0.1, 0.2, 0.3):
    pr = plan_values(r)[:, j]
    print(f"  robust T={T_ROB} with {r:.0%} reserve: max regret {(BEST[:, 0] - pr).max():.3f}")


# ===================================================== Simulation ===
RULES = [("A pay after", None, 0.0), ("B danger level", 0, 0.0), ("C calculator", T_CALC, 0.0),
         ("C' calculator, other tie", T_CALC_HIGH, 0.0),
         ("D expected value", T_EV, 0.0), ("E robust", T_ROB, 0.0),
         ("F robust + 20% reserve", T_ROB, 0.2)]
SCENARIOS = [("typical (the true river)", {}),
             ("wetter decade (+40 cm)", dict(shift=40)),
             ("drier decade (-40 cm)", dict(shift=-40)),
             ("forecasts under-predict big floods", dict(underpredict=0.4)),
             ("noisier forecasts (sd 55 cm)", dict(sd=55)),
             ("forecasts run high (+35 cm)", dict(bias=35)),
             ("fast floods: 30% of severe waves unforecast", dict(blind=0.3))]
N_SIM = 50_000

print()
print(f"Simulation - seven trigger rules over {N_SIM:,} simulated monsoons per scenario")
print("  value = average worth of the 10,000 transfers (1 = all paid before a severe peak)")
table, best_in = {}, {}
for name, kw in SCENARIOS:
    h, f = seasons(N_SIM, gen=np.random.default_rng(99), **kw)
    best_in[name] = max([V_LATE] + [summary(h, f, T)["value"] for T in THRESHOLDS])
    sev_rate = (h >= SEVERE).any(axis=1).mean()
    print(f"  {name}  (severe seasons {sev_rate:.0%})")
    for rname, T, r in RULES:
        if T is None:
            res = {"value": V_LATE, "hit": 0.0, "fa": 0.0, "soon": 0.0}
        else:
            res = summary(h, f, T, r)
        table[(name, rname)] = res
        tlabel = "  -" if T is None else f"{T:3d}"
        print(f"    {rname:24s} T={tlabel}  value={res['value']:.3f}  paid before the peak={res['hit']:5.1%}"
              f"  too soon={res['soon']:5.1%}  false alarms={res['fa']:5.1%}")

print("  best value any threshold reaches, scenario by scenario: " +
      "  ".join(f"{v:.3f}" for v in best_in.values()))
print("  across the seven scenarios: average value, worst value, largest shortfall from the best")
for rname, T, r in RULES:
    vals = [table[(n, rname)]["value"] for n, _ in SCENARIOS]
    short = max(best_in[n] - table[(n, rname)]["value"] for n, _ in SCENARIOS)
    print(f"    {rname:24s} avg={np.mean(vals):.3f}  worst={min(vals):.3f}  largest shortfall={short:.3f}")

# ===================================================== The list ===
print()
print("Layer 2 - the list: 10,000 of 40,000 surveyed households")
AREA_SIZE = np.array([9000, 8000, 7000, 6500, 5500, 4000])
AREA_ELEV = np.array([1.6, 1.3, 1.1, 0.9, 1.2, 0.6])   # mean village height above river, m
AREAS = len(AREA_SIZE)
lg = np.random.default_rng(2024)
area = np.repeat(np.arange(AREAS), AREA_SIZE)
n_hh = len(area)
village = np.concatenate([a * 100 + lg.integers(0, 30, s) for a, s in enumerate(AREA_SIZE)])
v_ids = np.unique(village)
v_elev = dict(zip(v_ids, np.clip(AREA_ELEV[v_ids // 100] + lg.normal(0, 0.45, len(v_ids)), 0.1, None)))
elev = np.array([v_elev[v] for v in village])
dist = np.clip(lg.gamma(2.0, 0.4, n_hh), 0.05, None)    # km from the river bank
plinth = lg.random(n_hh) < 0.30                         # house on a raised plinth
kids = lg.random(n_hh) < 0.35                           # child under 5
no_income = lg.random(n_hh) < 0.40                      # no regular income
need = 1 + kids + no_income


def flood_logit(plinth_effect=-1.0):
    return 2.2 - 1.6 * elev - 0.9 * dist + plinth_effect * plinth


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def floor_counts(score_area_total, floor_share):
    """Minimum households per area: floor_share of the area's share of total expected flooding."""
    return np.floor(floor_share * HOUSEHOLDS_PAID * score_area_total / score_area_total.sum()).astype(int)


def greedy_with_floor(order, floors):
    """Walk down a ranked list. First fill each area's floor from its own top-ranked
    households, then fill the rest of the 10,000 in overall rank order."""
    chosen = np.zeros(n_hh, bool)
    for a in range(AREAS):
        in_area = order[area[order] == a]
        chosen[in_area[:floors[a]]] = True
    for i in order:
        if chosen.sum() >= HOUSEHOLDS_PAID:
            break
        chosen[i] = True
    return chosen


def ilp_list(score, floors):
    """The integer program: maximize total score with every area at or above its floor."""
    prob = pulp.LpProblem("list", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(n_hh)]
    prob += pulp.lpSum(float(score[i]) * x[i] for i in range(n_hh))
    prob += pulp.lpSum(x) == HOUSEHOLDS_PAID
    for a in range(AREAS):
        prob += pulp.lpSum(x[i] for i in np.flatnonzero(area == a)) >= int(floors[a])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    assert pulp.LpStatus[prob.status] == "Optimal"
    return np.array([v.value() > 0.5 for v in x])


def evaluate_list(chosen, plinth_effect=-1.0, floods=1000):
    """Replay severe floods: which households actually flood, and how many were on the list."""
    gen = np.random.default_rng(5)
    base = flood_logit(plinth_effect) + gen.normal(0, 0.5, n_hh)      # household detail no survey sees
    v_index = np.searchsorted(v_ids, village)
    reached, need_reached, area_ratio = [], [], []
    for _ in range(floods):
        shock = gen.normal(0, 0.7, len(v_ids))[v_index]
        flooded = gen.random(n_hh) < sigmoid(base + shock)
        reached.append((flooded & chosen).sum() / flooded.sum())
        need_reached.append((need * (flooded & chosen)).sum() / (need * flooded).sum())
        per_area = [(flooded & chosen & (area == a)).sum() / max((flooded & (area == a)).sum(), 1)
                    for a in range(AREAS)]
        area_ratio.append(min(per_area))
    return np.mean(reached), np.mean(need_reached), np.mean(area_ratio), (flooded & chosen).sum()


p_hat = sigmoid(flood_logit())                     # the survey-based exposure model
score = p_hat * need
exp_area = np.array([p_hat[area == a].sum() for a in range(AREAS)])
print(f"  households per area: {AREA_SIZE.tolist()}  mean village height (m): {AREA_ELEV.tolist()}")
print(f"  expected flooded households in a severe flood, by area: {np.round(exp_area).astype(int).tolist()}"
      f"  total={exp_area.sum():,.0f}")
FLOOR = 0.6
floors = floor_counts(exp_area, FLOOR)
print(f"  floor: each area gets at least {FLOOR:.0%} of its share of expected flooding: {floors.tolist()}")

t0 = time.time()
x_ilp = ilp_list(score, floors)
t_ilp = time.time() - t0
order_model = np.argsort(-score, kind="stable")
x_greedy = greedy_with_floor(order_model, floors)
print(f"  integer program: {n_hh:,} yes/no variables, solved in {t_ilp:.1f}s, score={score[x_ilp].sum():,.1f}")
print(f"  greedy with floor on the same score: score={score[x_greedy].sum():,.1f}  "
      f"households that differ: {(x_ilp != x_greedy).sum()}")

order_geo = np.lexsort((-need, np.round(elev, 1)))   # lowest villages first, neediest first within
x_geo = np.zeros(n_hh, bool)
x_geo[order_geo[:HOUSEHOLDS_PAID]] = True
x_geo_floor = greedy_with_floor(order_geo, floors)
rand = np.zeros(n_hh, bool)
rand[np.random.default_rng(3).choice(n_hh, HOUSEHOLDS_PAID, replace=False)] = True

LISTS = [("random 10,000 of the survey", rand), ("geographic rule", x_geo),
         ("geographic rule + floor", x_geo_floor), ("exposure model + floor (ILP)", x_ilp)]
for label, effect in (("survey fields explain most exposure (plinth effect -1.0)", -1.0),
                      ("household detail matters more (plinth effect -2.5)", -2.5)):
    print(f"  replay of 1,000 severe floods - {label}")
    if effect != -1.0:
        p2 = sigmoid(flood_logit(effect))
        e2 = np.array([p2[area == a].sum() for a in range(AREAS)])
        x2 = ilp_list(p2 * need, floor_counts(e2, FLOOR))
        lists = LISTS[:3] + [("exposure model + floor (ILP)", x2)]
    else:
        lists = LISTS
    for name, chosen in lists:
        r, nr, ar, _ = evaluate_list(chosen, effect)
        shares = [chosen[area == a].sum() for a in range(AREAS)]
        print(f"    {name:30s} flooded households on the list={r:5.1%}  need-weighted={nr:5.1%}"
              f"  worst area={ar:5.1%}  per area={[int(s) for s in shares]}")

# ===================================================== Trigger card ===
print()
print("Field pathway - the trigger card")
print(f"  If the morning bulletin forecasts the main gauge at +{T_ROB} cm or more above danger level")
print(f"  within 5 days, release the transfer to List A today ({HOUSEHOLDS_PAID:,} households, $50 each).")
print("  One release per season. If no release has happened when a severe flood passes, pay List A then.")
