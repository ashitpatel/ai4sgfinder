"""Case 13 tutorial code: risk-based inspection for lead service lines.

Every number quoted in docs/tutorials/13-risk-based-inspection-lead-pipes.md
comes from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case13_risk_inspection.py

It needs only numpy. The city of Millbrook, its 20,000 older homes, their hidden
lead status and the 1,500 past digs are synthetic, generated with fixed random
seeds; they are made up for teaching. The output is the same on every run.

The program:
  1. builds a synthetic city where each home secretly does or doesn't have lead;
  2. simulates 1,500 past digs chosen the way the utility chose them
     (resident complaints and street repaving), not at random;
  3. fits a logistic regression risk model to those digs, written in numpy;
  4. checks the model's calibration;
  5. simulates one year (12 months x 25 digs = 300) under four dig rules and
     compares lead found, estimates of the city's total, and neighborhood coverage.
"""

import numpy as np

N_HOMES = 20_000          # older homes that might have a lead service line
N_PAST = 1_500            # past digs with results (lead and not lead)
MONTHS = 12               # the analyst reruns the model once a month
DIGS_PER_MONTH = 25       # 12 x 25 = 300 digs this year
RANDOM_PER_MONTH = 4      # random checks per month: 4 of 25 = 16% (case: 10-20%)
RIDGE = 2.0               # shrinkage strength for the neighborhood estimates
N_CITIES = 30             # synthetic cities for the averaged comparison

# name, share of homes, mean year built, hidden lead effect (log-odds),
# complaint rate, repaving rate, share of homes with no utility record
NEIGHBOURHOODS = [
    ("Old Town",  0.12, 1915,  0.3, 1.0, 0.30, 0.30),
    ("Northgate", 0.15, 1935, -0.3, 1.6, 0.25, 0.15),
    ("Westbury",  0.14, 1940, -0.6, 1.4, 0.20, 0.15),
    ("Riverside", 0.13, 1925,  0.0, 0.8, 0.15, 0.30),
    ("Eastfield", 0.13, 1945, -0.4, 0.8, 0.05, 0.20),
    ("Mill Hill", 0.12, 1930,  0.2, 0.5, 0.05, 0.40),
    ("Southbank", 0.11, 1928,  0.5, 0.2, 0.00, 0.50),
    ("Lowmoor",   0.10, 1920,  1.2, 0.1, 0.00, 0.60),
]
NAMES = [n[0] for n in NEIGHBOURHOODS]
K = len(NEIGHBOURHOODS)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def wilson(k, n, z=1.96):
    """95% confidence interval for a proportion k/n (Wilson's version)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return center - half, center + half


# ------------------------------------------------------------- The city ---

def make_city(seed):
    """20,000 homes with build year, utility record, neighborhood and hidden lead."""
    rng = np.random.default_rng(seed)
    shares = np.array([n[1] for n in NEIGHBOURHOODS])
    hood = rng.choice(K, size=N_HOMES, p=shares / shares.sum())
    year = np.array([NEIGHBOURHOODS[h][2] for h in hood]) + rng.normal(0, 12, N_HOMES)
    year = np.clip(np.round(year), 1880, 1985).astype(int)
    effect = np.array([NEIGHBOURHOODS[h][3] for h in hood])
    # Hidden truth: older homes and some neighborhoods are more likely to have lead.
    p_true = sigmoid(-1.6 + 0.6 * (1940 - year) / 10 + effect)
    lead = rng.random(N_HOMES) < p_true
    # Utility records: missing for some homes; where present they are right
    # most of the time but not always.
    missing = rng.random(N_HOMES) < np.array([NEIGHBOURHOODS[h][6] for h in hood])
    says_lead = np.where(lead, rng.random(N_HOMES) < 0.65, rng.random(N_HOMES) < 0.08)
    record = np.where(missing, 0, np.where(says_lead, 1, 2))   # 0 none, 1 lead, 2 not lead
    complain = np.array([NEIGHBOURHOODS[h][4] for h in hood])
    repave = np.array([NEIGHBOURHOODS[h][5] for h in hood])
    return dict(hood=hood, year=year, record=record, lead=lead, p_true=p_true,
                complain=complain, repave=repave)


def current_practice(city, n, available, rng):
    """Pick n homes the way the utility did: 60% from complaints, 40% from repaving.
    Complaints are more likely where there is lead (water-quality worries), and far
    more likely in some neighborhoods than others."""
    chosen = np.zeros(N_HOMES, bool)
    for count, w in ((round(0.6 * n), city["complain"] * (1 + 2 * city["lead"])),
                     (n - round(0.6 * n), city["repave"])):
        w = np.where(available & ~chosen, w, 0.0)
        idx = rng.choice(N_HOMES, size=count, replace=False, p=w / w.sum())
        chosen[idx] = True
    return np.flatnonzero(chosen)


# --------------------------------------------------- The risk model ---

def features(city):
    """One row per home: intercept, decades before 1940, record says lead,
    record says not lead, then one column per neighborhood."""
    X = np.zeros((N_HOMES, 4 + K))
    X[:, 0] = 1.0
    X[:, 1] = (1940 - city["year"]) / 10
    X[:, 2] = city["record"] == 1
    X[:, 3] = city["record"] == 2
    X[np.arange(N_HOMES), 4 + city["hood"]] = 1.0
    return X


def fit_logistic(X, y, ridge=RIDGE):
    """Logistic regression by Newton's method. Neighborhood columns are shrunk
    toward zero (the city average) so a neighborhood with few digs isn't given
    a wild estimate; that is what 'ridge' does."""
    penalty = np.zeros(X.shape[1])
    penalty[4:] = ridge
    beta = np.zeros(X.shape[1])
    for _ in range(50):
        p = sigmoid(X @ beta)
        grad = X.T @ (y - p) - penalty * beta
        hess = X.T @ (X * (p * (1 - p))[:, None]) + np.diag(penalty + 1e-9)
        step = np.linalg.solve(hess, grad)
        beta += step
        if np.max(np.abs(step)) < 1e-8:
            break
    return beta


# --------------------------------------------------------- Dig rules ---

def run_year(city, X, past, rule, seed):
    """Simulate 12 months of 25 digs under one rule. Returns the homes dug this
    year, which of them were random checks, and the model fitted at the end."""
    rng = np.random.default_rng(seed)
    dug = np.zeros(N_HOMES, bool)
    dug[past] = True
    year_digs, random_digs = [], []
    for _ in range(MONTHS):
        avail = ~dug
        if rule == "current practice":
            pick = current_practice(city, DIGS_PER_MONTH, avail, rng)
        elif rule in ("oldest first", "oldest + random"):
            cand = np.flatnonzero(avail)
            order = np.lexsort((rng.random(cand.size), city["year"][cand]))
            n_rank = DIGS_PER_MONTH - (RANDOM_PER_MONTH if rule == "oldest + random" else 0)
            pick = cand[order[:n_rank]]
            if rule == "oldest + random":
                rest = avail.copy()
                rest[pick] = False
                rand = rng.choice(np.flatnonzero(rest), RANDOM_PER_MONTH, replace=False)
                random_digs.extend(rand)
                pick = np.concatenate([pick, rand])
        else:
            beta = fit_logistic(X[dug], city["lead"][dug].astype(float))   # monthly refit
            risk = np.where(avail, sigmoid(X @ beta), -1.0)
            n_rank = DIGS_PER_MONTH - (RANDOM_PER_MONTH if rule == "model + random" else 0)
            pick = np.argsort(-risk, kind="stable")[:n_rank]
            if rule == "model + random":
                rest = avail.copy()
                rest[pick] = False
                rand = rng.choice(np.flatnonzero(rest), RANDOM_PER_MONTH, replace=False)
                random_digs.extend(rand)
                pick = np.concatenate([pick, rand])
        dug[pick] = True
        year_digs.extend(pick)
    beta = fit_logistic(X[dug], city["lead"][dug].astype(float))
    return np.array(year_digs), np.array(random_digs, int), beta, dug


def estimate_total(city, X, past, year, rand, beta, dug, rule):
    """The estimate of the city's lead lines each rule would naturally produce."""
    lead = city["lead"]
    if rule in ("current practice", "oldest first"):
        all_dug = np.concatenate([past, year])          # hit rate of every dig so far
        return lead[all_dug].mean() * N_HOMES, None
    if rule == "model, no random":                       # known finds + model's sum for the rest
        return lead[dug].sum() + sigmoid(X[~dug] @ beta).sum(), None
    # Random share: known finds + random-check hit rate x homes nobody chose.
    k, n = int(lead[rand].sum()), len(rand)
    chosen = np.setdiff1d(np.flatnonzero(dug), rand)
    pool = N_HOMES - chosen.size
    lo, hi = wilson(k, n)
    base = lead[chosen].sum()
    return base + k / n * pool, (base + lo * pool, base + hi * pool)


RULES = ["current practice", "oldest first", "oldest + random", "model, no random", "model + random"]
WITH_RANDOM = ("oldest + random", "model + random")


# ------------------------------------------------------------- Main ---

def main():
    city = make_city(13)
    X = features(city)
    rng = np.random.default_rng(1013)
    past = current_practice(city, N_PAST, np.ones(N_HOMES, bool), rng)
    lead, hood = city["lead"], city["hood"]

    print("City - Millbrook (synthetic), 20,000 older homes")
    print("  neighborhood  homes  built(median)  no record  TRUE lead rate (hidden)  past digs  past hit rate")
    for h in range(K):
        m = hood == h
        pd = past[hood[past] == h]
        rate = f"{lead[pd].mean():.2f}" if pd.size else "  - "
        print(f"  {NAMES[h]:<13}{m.sum():>6}  {int(np.median(city['year'][m])):>8}       "
              f"{(city['record'][m] == 0).mean():>5.0%}           {lead[m].mean():.2f}"
              f"            {pd.size:>5}      {rate}")
    print(f"  whole city: {lead.sum():,} lead lines of {N_HOMES:,} ({lead.mean():.3f})  (hidden)")

    # ---- the hit rate as a proportion with a confidence interval
    k = int(lead[past].sum())
    lo, hi = wilson(k, N_PAST)
    se = np.sqrt(k / N_PAST * (1 - k / N_PAST) / N_PAST)
    print("\nPast digs - hit rate as a proportion")
    print(f"  lead found in {k} of {N_PAST:,} past digs: {k / N_PAST:.3f}  "
          f"(standard error {se:.4f}; 95% CI {lo:.3f} to {hi:.3f})")
    print(f"  naive city estimate = {k / N_PAST:.3f} x 20,000 = {k / N_PAST * N_HOMES:,.0f}; "
          f"true = {lead.sum():,}")

    # ---- the starting risk model
    beta = fit_logistic(X[past], lead[past].astype(float))
    print("\nStarting model - logistic regression on the 1,500 past digs")
    labels = ["intercept", "per decade before 1940", "record says lead",
              "record says not lead"] + [f"neighborhood {n}" for n in NAMES]
    for lab, b in zip(labels, beta):
        print(f"  {lab:<28} coef {b:+.2f}   odds x{np.exp(b):.2f}")

    # ---- toy example to check by hand
    print("\nToy example - three homes, by hand")
    toy = [("1915, no record, Old Town", 2.5, 0, 0, "Old Town"),
           ("1945, record says not lead, Westbury", -0.5, 0, 1, "Westbury"),
           ("1920, no record, Lowmoor", 2.0, 0, 0, "Lowmoor")]
    for desc, dec, rl, rn, nm in toy:
        z = beta[0] + beta[1] * dec + beta[2] * rl + beta[3] * rn + beta[4 + NAMES.index(nm)]
        print(f"  {desc:<38} score z = {z:+.2f}  ->  risk = 1/(1+e^-z) = {sigmoid(z):.3f}")

    # ---- calibration of the starting model
    p0 = sigmoid(X @ beta)
    print("\nCalibration - starting model, by predicted-risk band")
    print("  band         homes  mean predicted  past digs: n, observed   ALL homes: observed (hidden)")
    edges = [0, 0.1, 0.2, 0.4, 0.6, 1.01]
    for a, b in zip(edges[:-1], edges[1:]):
        m = (p0 >= a) & (p0 < b)
        mp = m[past]
        obs_past = f"{lead[past][mp].mean():.2f}" if mp.sum() else " - "
        print(f"  {a:.1f}-{min(b, 1):.1f}   {m.sum():>7}      {p0[m].mean():.2f}"
              f"            {mp.sum():>4}, {obs_past}            {lead[m].mean():.2f}")
    print("  by neighborhood: mean predicted vs true rate (hidden)")
    for h in range(K):
        m = hood == h
        print(f"    {NAMES[h]:<11} predicted {p0[m].mean():.2f}   true {lead[m].mean():.2f}")
    print(f"  model's sum of risks over all homes: {p0.sum():,.0f}  (true {lead.sum():,})")
    undug = np.setdiff1d(np.arange(N_HOMES), past)
    top = undug[np.argsort(-p0[undug], kind="stable")[:300]]
    print(f"  top 300 undug homes by starting risk: expected lead = sum of risks = "
          f"{p0[top].sum():.0f}; actually lead (hidden) = {lead[top].sum()}")

    # ---- one simulated year, five rules
    print("\nOne year in Millbrook - 300 digs (12 months x 25), five rules")
    results = {}
    for r in RULES:
        year, rand, b_end, dug = run_year(city, X, past, r, seed=7)
        est, ci = estimate_total(city, X, past, year, rand, b_end, dug, r)
        results[r] = (year, rand, b_end, dug)
        found = int(lead[year].sum())
        n_zero = sum(1 for h in range(K) if (hood[year] == h).sum() == 0)
        ci_txt = f" (95% CI {ci[0]:,.0f} to {ci[1]:,.0f})" if ci else ""
        print(f"  {r:<17} lead found {found:>3}/300 ({found / 300:.0%})  "
              f"neighborhoods with no digs: {n_zero}  estimated total {est:,.0f}{ci_txt}")
    print(f"  true total: {lead.sum():,}")
    print("  digs per neighborhood this year:")
    print("    " + " " * 17 + "".join(f"{n[:9]:>10}" for n in NAMES))
    for r in RULES:
        counts = [(hood[results[r][0]] == h).sum() for h in range(K)]
        print(f"    {r:<17}" + "".join(f"{c:>10}" for c in counts))

    # ---- what the random checks reveal
    year, rand, b_end, _ = results["model + random"]
    k, n = int(lead[rand].sum()), len(rand)
    lo, hi = wilson(k, n)
    print("\nRandom checks - model + random rule")
    print(f"  {n} random digs found lead in {k}: {k / n:.2f} (95% CI {lo:.2f} to {hi:.2f})")
    print(f"  starting model's mean predicted risk for those same homes: {p0[rand].mean():.2f}")
    print(f"  random digs in Lowmoor: {(hood[rand] == NAMES.index('Lowmoor')).sum()}, "
          f"lead found: {lead[rand][hood[rand] == NAMES.index('Lowmoor')].sum()}")
    _, _, b_norand, _ = results["model, no random"]
    low = NAMES.index("Lowmoor")
    print(f"  Lowmoor coefficient: start {beta[4 + low]:+.2f}, end of year with random "
          f"share {b_end[4 + low]:+.2f}, end of year without {b_norand[4 + low]:+.2f}")

    # ---- equity check
    print("\nEquity check - model + random rule, end of year")
    print("  neighborhood  mean predicted risk (end)  past digs  digs this year  lead found")
    p_end = sigmoid(X @ b_end)
    for h in range(K):
        m = hood == h
        yh = year[hood[year] == h]
        print(f"  {NAMES[h]:<13}          {p_end[m].mean():.2f}               "
              f"{(hood[past] == h).sum():>4}         {yh.size:>4}          {lead[yh].sum():>4}")

    # ---- averaged over many synthetic cities
    print(f"\nAverage over {N_CITIES} synthetic cities (each with its own past digs)")
    tally = {r: dict(found=[], zero=[], err=[], low=[]) for r in RULES}
    covered = {r: 0 for r in WITH_RANDOM}
    for s in range(N_CITIES):
        c = make_city(100 + s)
        Xc = features(c)
        pst = current_practice(c, N_PAST, np.ones(N_HOMES, bool), np.random.default_rng(200 + s))
        for r in RULES:
            yr, rd, be, dg = run_year(c, Xc, pst, r, seed=300 + s)
            est, ci = estimate_total(c, Xc, pst, yr, rd, be, dg, r)
            t = tally[r]
            t["found"].append(c["lead"][yr].sum())
            t["zero"].append(sum(1 for h in range(K) if (c["hood"][yr] == h).sum() == 0))
            t["err"].append(est - c["lead"].sum())
            t["low"].append((c["hood"][yr] == low).sum())
            if ci and ci[0] <= c["lead"].sum() <= ci[1]:
                covered[r] += 1
    print("  rule               lead found per 300 (min-max)  hit rate  hoods w/o digs  "
          "Lowmoor digs  total estimate error (mean, typical size)")
    for r in RULES:
        t = tally[r]
        f = np.array(t["found"])
        e = np.array(t["err"])
        print(f"  {r:<17}  {f.mean():6.1f} ({f.min()}-{f.max()})            {f.mean() / 300:.0%}"
              f"        {np.mean(t['zero']):.1f}          {np.mean(t['low']):5.1f}"
              f"        {e.mean():+7,.0f}, {np.sqrt(np.mean(e ** 2)):6,.0f}")
    for r in WITH_RANDOM:
        print(f"  {r}: 95% CI for the total contained the truth in {covered[r]} of {N_CITIES} cities")


if __name__ == "__main__":
    main()
