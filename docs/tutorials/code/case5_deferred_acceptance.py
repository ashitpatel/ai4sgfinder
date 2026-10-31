"""Case 5 tutorial code: stable matching by deferred acceptance for apprenticeships.

Every number quoted in docs/tutorials/05-stable-matching-apprenticeships.md comes
from running this file:

    pip install -r docs/tutorials/code/requirements.txt
    python3 docs/tutorials/code/case5_deferred_acceptance.py

Only numpy and the standard library are needed. Deferred acceptance is written out
from scratch so every step is visible; in production, the `matching` library's
hospital-resident solver does the same job. The program is illustrative: the toy
market and the synthetic cohort are made up for teaching.
"""

from itertools import permutations, product

import numpy as np

UNMATCHED = None


# ---------------------------------------------------------- the algorithm ---

def deferred_acceptance(youth_lists, employer_rank, capacity):
    """Young-people-proposing deferred acceptance with employer capacities.

    youth_lists:   {person: [employer, employer, ...]}  best first
    employer_rank: {employer: {person: rank}}  lower rank = preferred;
                   a person missing from the dict is not acceptable to that employer
    capacity:      {employer: number of places}

    Each round, every young person who is not being held proposes to the next
    employer on their list. Each employer looks at everyone it is holding plus the
    new proposals, keeps its best `capacity` and rejects the rest. Nothing is final
    until nobody has anyone left to propose to.
    Returns (match, rounds) where match is {person: employer or None}.
    """
    next_choice = {p: 0 for p in youth_lists}        # position on each person's list
    held = {e: [] for e in capacity}                  # tentatively held, per employer
    free = [p for p in youth_lists]                   # people not currently held
    rounds = []
    while True:
        proposals = {}
        for p in free:
            if next_choice[p] < len(youth_lists[p]):
                e = youth_lists[p][next_choice[p]]
                next_choice[p] += 1
                proposals.setdefault(e, []).append(p)
        if not proposals:
            break
        log = {"proposals": proposals, "rejected": []}
        new_free = []                                 # anyone rejected this round
        for e, applicants in proposals.items():
            pool = held[e] + applicants
            acceptable = [p for p in pool if p in employer_rank[e]]
            acceptable.sort(key=lambda p: employer_rank[e][p])
            held[e] = acceptable[:capacity[e]]
            rejected = [p for p in pool if p not in held[e]]
            log["rejected"] += [(p, e) for p in rejected]
            new_free += rejected
        log["held"] = {e: list(v) for e, v in held.items()}
        rounds.append(log)
        free = new_free
    match = {p: UNMATCHED for p in youth_lists}
    for e, people in held.items():
        for p in people:
            match[p] = e
    return match, rounds


def first_choices_first(youth_lists, employer_rank, capacity):
    """The 'Boston' mechanism: round k fills places from k-th choices, permanently.

    Each round, every unplaced person applies to the k-th employer on their list.
    An employer with places left accepts its best applicants up to the places
    remaining, and those acceptances are final.
    """
    left = dict(capacity)
    match = {p: UNMATCHED for p in youth_lists}
    for k in range(max(len(v) for v in youth_lists.values())):
        applicants = {}
        for p, lst in youth_lists.items():
            if match[p] is UNMATCHED and k < len(lst):
                applicants.setdefault(lst[k], []).append(p)
        for e, people in applicants.items():
            people = sorted([p for p in people if p in employer_rank[e]],
                            key=lambda p: employer_rank[e][p])
            for p in people[:left[e]]:
                match[p] = e
            left[e] -= min(left[e], len(people))
    return match


def blocking_pairs(match, youth_lists, employer_rank, capacity):
    """Every (person, employer) pair who would both rather be together.

    A person prefers employer e if e is on their list above what they got (getting
    nothing, or an employer they never listed, is worse than anything listed).
    The employer wants the person if it has an empty place and finds them
    acceptable, or if it ranks them above someone it was given.
    """
    pairs = []
    for p, lst in youth_lists.items():
        got = match[p]
        cut = lst.index(got) if got in lst else len(lst)
        for e in lst[:cut]:
            if p not in employer_rank[e]:
                continue
            given = [q for q, f in match.items() if f == e]
            if len(given) < capacity[e]:
                pairs.append((p, e))
            elif any(employer_rank[e].get(q, 10**9) > employer_rank[e][p] for q in given):
                pairs.append((p, e))
    return pairs


def greedy_fit_assignment(fit, capacity):
    """Staff assignment: take the highest fit score anywhere, assign it, repeat.

    fit: {(person, employer): score}. The young people's ranked lists are not used.
    """
    left = dict(capacity)
    match = {}
    for (p, e), _ in sorted(fit.items(), key=lambda kv: -kv[1]):
        if p not in match and left[e] > 0:
            match[p] = e
            left[e] -= 1
    return match


# ---------------------------------------------------------- toy market -------

TOY_YOUTH = {                      # each young person's ranked list, best first
    "Ana": ["Garage", "Bakery", "Clinic"],
    "Ben": ["Garage", "Clinic", "Bakery"],
    "Chi": ["Bakery", "Garage", "Clinic"],
    "Dan": ["Garage", "Bakery"],
    "Eva": ["Clinic", "Garage", "Bakery"],
    "Fin": ["Bakery", "Clinic", "Garage"],
}
TOY_EMPLOYER_ORDER = {             # each employer's ranking of applicants, best first
    "Garage": ["Chi", "Ben", "Ana", "Eva", "Dan", "Fin"],
    "Bakery": ["Ana", "Dan", "Fin", "Chi", "Ben", "Eva"],
    "Clinic": ["Dan", "Eva", "Ben", "Fin", "Ana", "Chi"],
}
TOY_CAPACITY = {"Garage": 1, "Bakery": 2, "Clinic": 2}
TOY_RANK = {e: {p: i for i, p in enumerate(order)} for e, order in TOY_EMPLOYER_ORDER.items()}
# Staff "fit scores" (0-10), based on skills and the officer's judgment, not on wishes.
TOY_FIT = {
    ("Ana", "Clinic"): 9, ("Ben", "Bakery"): 8, ("Chi", "Garage"): 8,
    ("Dan", "Clinic"): 7, ("Eva", "Bakery"): 7, ("Fin", "Clinic"): 6,
    ("Ana", "Garage"): 5, ("Ben", "Garage"): 5, ("Chi", "Bakery"): 5,
    ("Dan", "Garage"): 4, ("Eva", "Garage"): 4, ("Fin", "Bakery"): 4,
    ("Ana", "Bakery"): 3, ("Ben", "Clinic"): 3, ("Chi", "Clinic"): 3,
    ("Dan", "Bakery"): 2, ("Eva", "Clinic"): 2, ("Fin", "Garage"): 2,
}


def place_label(match, p, lst):
    e = match[p]
    if e is UNMATCHED:
        return "unmatched"
    return f"{e} (choice {lst.index(e) + 1})" if e in lst else f"{e} (not listed)"


def all_lists(employers, max_len):
    """Every ordered list of distinct employers of length 1..max_len."""
    out = []
    for k in range(1, max_len + 1):
        out += [list(x) for x in permutations(employers, k)]
    return out


def all_stable_matchings(youth_lists, employer_rank, capacity):
    """Brute force over the toy: every assignment that respects lists and capacities."""
    people = list(youth_lists)
    found = []
    for combo in product(*[[UNMATCHED] + youth_lists[p] for p in people]):
        m = dict(zip(people, combo))
        counts = {e: sum(1 for x in combo if x == e) for e in capacity}
        if any(counts[e] > capacity[e] for e in capacity):
            continue
        if not blocking_pairs(m, youth_lists, employer_rank, capacity):
            found.append(m)
    return found


def employer_proposing(youth_lists, employer_rank, capacity):
    """Deferred acceptance with the employers proposing (for comparison only)."""
    order = {e: sorted(r, key=r.get) for e, r in employer_rank.items()}
    pos = {e: 0 for e in capacity}
    held = {p: UNMATCHED for p in youth_lists}
    pref = {p: {e: i for i, e in enumerate(l)} for p, l in youth_lists.items()}
    while True:
        moved = False
        for e in capacity:
            n_held = sum(1 for x in held.values() if x == e)
            while n_held < capacity[e] and pos[e] < len(order[e]):
                p = order[e][pos[e]]
                pos[e] += 1
                if e not in pref[p]:
                    continue
                cur = held[p]
                if cur is UNMATCHED or pref[p][e] < pref[p][cur]:
                    held[p] = e
                    n_held += 1
                    moved = True
        if not moved:
            break
    return held


# ---------------------------------------------------------- synthetic cohort --

N_YOUTH, N_EMPLOYERS, N_TOWNS = 200, 60, 4


def make_market(seed, list_len=5):
    """A synthetic cohort like the case: 200 young people, 60 employers, ~220 places.

    Young people's tastes are correlated: every employer has a popularity level that
    everyone sees, plus each person's own taste and a bonus for their own town.
    Employers use a scoring rule: course grade (1-5) + 1 if the applicant lives in
    the employer's town. Ties are broken by one public lottery number per person.
    """
    rng = np.random.default_rng(seed)
    capacity = rng.integers(1, 9, N_EMPLOYERS)                 # 1-8 places
    while capacity.sum() != 220:                               # nudge to ~220 total
        j = rng.integers(N_EMPLOYERS)
        if capacity.sum() > 220 and capacity[j] > 1:
            capacity[j] -= 1
        elif capacity.sum() < 220 and capacity[j] < 8:
            capacity[j] += 1
    popularity = rng.normal(0, 0.4, N_EMPLOYERS)     # some employers are popular
    emp_town = rng.integers(0, N_TOWNS, N_EMPLOYERS)
    youth_town = rng.integers(0, N_TOWNS, N_YOUTH)
    grade = rng.integers(1, 6, N_YOUTH)
    lottery = rng.random(N_YOUTH)                              # uniform on (0, 1)
    utility = (popularity[None, :] + rng.normal(0, 1.0, (N_YOUTH, N_EMPLOYERS))
               + 0.5 * (youth_town[:, None] == emp_town[None, :]))
    full_order = np.argsort(-utility, axis=1)                  # each person's true order
    score = grade[:, None] + (youth_town[:, None] == emp_town[None, :])
    return dict(capacity=capacity, utility=utility, full_order=full_order, score=score,
                lottery=lottery, list_len=list_len, grade=grade)


def market_inputs(mk, list_len=None, only_employers=None):
    """Turn a synthetic market into the dicts deferred_acceptance expects."""
    k = mk["list_len"] if list_len is None else list_len
    youth_lists = {}
    for i in range(N_YOUTH):
        order = [int(j) for j in mk["full_order"][i]]
        if only_employers is not None:
            order = [j for j in order if j in only_employers]
        youth_lists[i] = order[:k]
    # Employer ranking = scoring rule, ties broken by lottery (lower number first).
    employer_rank = {}
    for j in range(N_EMPLOYERS):
        order = sorted(range(N_YOUTH), key=lambda i: (-mk["score"][i, j], mk["lottery"][i]))
        employer_rank[j] = {i: r for r, i in enumerate(order)}
    capacity = {j: int(mk["capacity"][j]) for j in range(N_EMPLOYERS)}
    return youth_lists, employer_rank, capacity


def summarize(match, youth_lists):
    n = len(youth_lists)
    first = sum(1 for p, e in match.items() if e is not UNMATCHED and youth_lists[p][:1] == [e])
    listed = sum(1 for p, e in match.items() if e is not UNMATCHED and e in youth_lists[p])
    unmatched = sum(1 for e in match.values() if e is UNMATCHED)
    return first / n, listed / n, unmatched


def second_round(mk, match, capacity):
    """Unmatched young people rank (up to 5) employers that still have places."""
    used = {}
    for e in match.values():
        if e is not UNMATCHED:
            used[e] = used.get(e, 0) + 1
    open_places = {j: capacity[j] - used.get(j, 0) for j in capacity if capacity[j] - used.get(j, 0) > 0}
    left_out = [p for p, e in match.items() if e is UNMATCHED]
    lists2, rank2, _ = market_inputs(mk, only_employers=set(open_places))
    lists2 = {p: lists2[p] for p in left_out}
    m2, _ = deferred_acceptance(lists2, rank2, open_places)
    return m2, len(open_places), sum(open_places.values())


def staff_fit_assignment(mk, seed):
    """Staff assign by a 'fit score': the employer's score, a partial reading of the
    young person's interests (half weight), and the officer's own judgment."""
    rng = np.random.default_rng(seed + 1000)
    judgment = rng.normal(0, 1.0, (N_YOUTH, N_EMPLOYERS))
    fit = {(i, j): mk["score"][i, j] + 0.5 * mk["utility"][i, j] + judgment[i, j]
           for i in range(N_YOUTH) for j in range(N_EMPLOYERS)}
    return greedy_fit_assignment(fit, {j: int(c) for j, c in enumerate(mk["capacity"])})


# ---------------------------------------------------------- printing ---------

def main():
    youth, rank, cap = TOY_YOUTH, TOY_RANK, TOY_CAPACITY

    print("Chapter 4 - toy market: deferred acceptance, round by round")
    match, rounds = deferred_acceptance(youth, rank, cap)
    for r, log in enumerate(rounds, 1):
        props = "; ".join(f"{e} <- {', '.join(ps)}" for e, ps in log["proposals"].items())
        rej = ", ".join(f"{p} by {e}" for p, e in log["rejected"]) or "nobody"
        held = "; ".join(f"{e}: {', '.join(v) or '-'}" for e, v in log["held"].items())
        print(f"  round {r}: proposals {props}")
        print(f"           rejected {rej}")
        print(f"           holding  {held}")
    print("  final match:")
    for p in youth:
        print(f"    {p}: {place_label(match, p, youth[p])}")
    bp = blocking_pairs(match, youth, rank, cap)
    print(f"  blocking pairs: {len(bp)} {bp}")

    print("\nChapter 4 - same toy market, staff assignment by fit score")
    fit_match = greedy_fit_assignment(TOY_FIT, cap)
    fit_match = {p: fit_match.get(p, UNMATCHED) for p in youth}
    for p in youth:
        print(f"    {p}: {place_label(fit_match, p, youth[p])}")
    bp = blocking_pairs(fit_match, youth, rank, cap)
    print(f"  blocking pairs: {len(bp)} {bp}")

    print("\nChapter 2 - same toy market, 'first choices first' (Boston-style)")
    honest = first_choices_first(youth, rank, cap)
    for p in youth:
        print(f"    {p}: {place_label(honest, p, youth[p])}")
    bp = blocking_pairs(honest, youth, rank, cap)
    print(f"  blocking pairs: {len(bp)} {bp}")
    gamed = dict(youth)
    gamed["Dan"] = ["Bakery", "Garage"]
    g = first_choices_first(gamed, rank, cap)
    print(f"  Dan lists Bakery first instead: result for Dan = {g['Dan'] or 'unmatched'}, "
          f"result for Chi = {g['Chi'] or 'unmatched'}")
    print(f"  (Dan's true list is {youth['Dan']}; honest result = {honest['Dan'] or 'unmatched'})")

    print("\nChapter 4 - can anyone gain by misreporting under deferred acceptance?")
    employers = list(cap)
    gains = 0
    for p in youth:
        true_pos = {e: i for i, e in enumerate(youth[p])}
        honest_pos = true_pos.get(match[p], len(youth[p]))
        best_pos = honest_pos
        for lst in all_lists(employers, 3):
            trial = dict(youth)
            trial[p] = lst
            m, _ = deferred_acceptance(trial, rank, cap)
            best_pos = min(best_pos, true_pos.get(m[p], len(youth[p])))
        gains += best_pos < honest_pos
        print(f"  {p}: honest result {match[p] or 'unmatched'}; best result over {len(all_lists(employers, 3))} "
              f"possible lists = {youth[p][best_pos] if best_pos < len(youth[p]) else 'unmatched'}")
    print(f"  people who could do better by lying: {gains}")
    for lst in (["Bakery", "Garage"], ["Bakery"]):
        trial = dict(youth)
        trial["Dan"] = lst
        m, _ = deferred_acceptance(trial, rank, cap)
        print(f"  Dan reports {lst}: Dan gets {m['Dan'] or 'unmatched'}")
    for lst in (["Garage", "Bakery", "Clinic"], ["Clinic", "Bakery", "Garage"], ["Clinic"]):
        trial = dict(youth)
        trial["Fin"] = lst
        m, _ = deferred_acceptance(trial, rank, cap)
        print(f"  Fin reports {lst}: Fin gets {m['Fin'] or 'unmatched'}")

    print("\nChapter 4 - every stable matching of the toy market")
    stable = all_stable_matchings(youth, rank, cap)
    for m in stable:
        print("   ", {p: m[p] for p in youth})
    emp = employer_proposing(youth, rank, cap)
    print(f"  employer-proposing result: { {p: emp[p] for p in youth} }")

    print("\nChapter 4 - who benefits: a 2-person market with two stable matchings")
    mini_youth = {"Xia": ["Print shop", "Salon"], "Yaw": ["Salon", "Print shop"]}
    mini_rank = {"Print shop": {"Yaw": 0, "Xia": 1}, "Salon": {"Xia": 0, "Yaw": 1}}
    mini_cap = {"Print shop": 1, "Salon": 1}
    for m in all_stable_matchings(mini_youth, mini_rank, mini_cap):
        print("    stable:", m)
    print("  young-people-proposing:", deferred_acceptance(mini_youth, mini_rank, mini_cap)[0])
    print("  employer-proposing:    ", employer_proposing(mini_youth, mini_rank, mini_cap))

    print("\nChapter 3 - lottery tie-break: chance of winning a tie among k equal scores")
    for k in (2, 3, 4):
        print(f"  k={k}: each wins first place with probability 1/{k} = {1/k:.3f}")

    print("\nChapter 3 - risk of ending unmatched vs list length (300 synthetic cohorts each)")
    reps = 300
    for k in (3, 5, 8, 12):
        shares = []
        for s in range(reps):
            mk = make_market(seed=s, list_len=k)
            yl, er, cp = market_inputs(mk)
            m, _ = deferred_acceptance(yl, er, cp)
            shares.append(sum(1 for e in m.values() if e is UNMATCHED) / N_YOUTH)
        shares = np.array(shares)
        mean, se = shares.mean(), shares.std(ddof=1) / np.sqrt(reps)
        print(f"  list of {k:2d}: mean share unmatched = {mean:.4f}  "
              f"95% CI ({mean - 1.96 * se:.4f}, {mean + 1.96 * se:.4f})  "
              f"= about {mean * N_YOUTH:.1f} of 200 people;  cohorts with nobody unmatched: "
              f"{(shares == 0).mean():.2f}")

    print("\nChapter 5 - one synthetic cohort (seed 2026): 200 young people, 60 employers")
    mk = make_market(seed=2026, list_len=5)
    yl, er, cp = market_inputs(mk)
    print(f"  places: {int(mk['capacity'].sum())}  capacities range {mk['capacity'].min()}-"
          f"{mk['capacity'].max()}")
    top_counts = np.bincount(mk["full_order"][:, 0], minlength=N_EMPLOYERS)
    j_pop = int(np.argmax(top_counts))
    print(f"  most popular employer is the first choice of {top_counts[j_pop]} people "
          f"and has {mk['capacity'][j_pop]} places")
    staff = staff_fit_assignment(mk, 2026)
    staff = {p: staff.get(p, UNMATCHED) for p in yl}
    boston = first_choices_first(yl, er, cp)
    da, rounds = deferred_acceptance(yl, er, cp)
    print(f"  deferred acceptance took {len(rounds)} rounds")
    # Where did the lottery decide who got the last place? An employer whose lowest
    # kept applicant has the same score as its best rejected applicant.
    proposed = {}
    for log in rounds:
        for e, ps in log["proposals"].items():
            proposed.setdefault(e, set()).update(ps)
    full, by_lottery = 0, 0
    for j, ps in proposed.items():
        kept = [p for p in ps if da[p] == j]
        lost = [p for p in ps if da[p] != j]
        if lost:
            full += 1
            if min(mk["score"][p, j] for p in kept) == max(mk["score"][p, j] for p in lost):
                by_lottery += 1
    print(f"  employers that turned someone away: {full}; of these, last place decided "
          f"by the lottery among equal scores: {by_lottery}")
    print("  method                     blocking pairs  top choice  any listed  not listed  unmatched")
    for name, m in (("staff fit score", staff), ("first choices first", boston),
                    ("deferred acceptance", da)):
        first, listed, un = summarize(m, yl)
        not_listed = sum(1 for p, e in m.items() if e is not UNMATCHED and e not in yl[p])
        print(f"  {name:26s} {len(blocking_pairs(m, yl, er, cp)):14d}  {first:10.3f}  "
              f"{listed:10.3f}  {not_listed:10d}  {un:9d}")
    m2, n_open, places_open = second_round(mk, da, cp)
    placed2 = sum(1 for e in m2.values() if e is not UNMATCHED)
    print(f"  second round: {len(m2)} unmatched people, {n_open} employers with "
          f"{places_open} places left; placed {placed2}, still unmatched {len(m2) - placed2}")

    print("\nChapter 5 - the same comparison averaged over 100 cohorts (seeds 0-99)")
    tot = {n: np.zeros(5) for n in ("staff fit score", "first choices first", "deferred acceptance")}
    r2_placed, r2_left = [], []
    for s in range(100):
        mk = make_market(seed=s, list_len=5)
        yl, er, cp = market_inputs(mk)
        staff = staff_fit_assignment(mk, s)
        staff = {p: staff.get(p, UNMATCHED) for p in yl}
        da, _ = deferred_acceptance(yl, er, cp)
        for name, m in (("staff fit score", staff),
                        ("first choices first", first_choices_first(yl, er, cp)),
                        ("deferred acceptance", da)):
            first, listed, un = summarize(m, yl)
            not_listed = sum(1 for p, e in m.items() if e is not UNMATCHED and e not in yl[p])
            tot[name] += [len(blocking_pairs(m, yl, er, cp)), first, listed, not_listed, un]
        m2, _, _ = second_round(mk, da, cp)
        placed2 = sum(1 for e in m2.values() if e is not UNMATCHED)
        r2_placed.append(placed2)
        r2_left.append(len(m2) - placed2)
    print("  method                     blocking pairs  top choice  any listed  not listed  unmatched")
    for name, t in tot.items():
        t = t / 100
        print(f"  {name:26s} {t[0]:14.1f}  {t[1]:10.3f}  {t[2]:10.3f}  {t[3]:10.1f}  {t[4]:9.1f}")
    print(f"  second round after deferred acceptance: placed {np.mean(r2_placed):.1f} on average, "
          f"still unmatched {np.mean(r2_left):.2f}")


if __name__ == "__main__":
    main()
