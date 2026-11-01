# Stable Matching Masterclass: Who Goes to Which Employer When Both Sides Choose

*An in-depth walkthrough of two-sided matching markets, stability and deferred acceptance, built on [Case 5: Matching young people to apprenticeships](../cases/05-apprenticeship-matching.md).*

**You need:** proportions, averages, basic probability and the idea of a confidence interval. **You don't need:** any machine learning, game theory or optimization background. Every term is explained when it first appears.

**Approach:** [Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets). **Code:** [`code/case5_deferred_acceptance.py`](code/case5_deferred_acceptance.py). Every number in this tutorial comes from running that file.

---

## Executive Overview

A youth employment NGO places about 200 graduates of its vocational course into 6-month paid apprenticeships each cohort. Sixty local employers offer between 1 and 8 places each, about 220 in total. Until now the placement officer assigned people by judgment. Last cohort, 30 young people turned down their placement or quit in the first month, and several employers refused the candidates they were sent.

The usual fixes fail in instructive ways. A better "fit score" still ignores what the young people and the employers actually want, so some of them walk away. A "first choices first" system asks for preferences but punishes people who list a popular employer first, so they learn to lie about what they want.

This tutorial builds the alternative step by step:

1. **[The Matching Leap](#the-matching-leap--from-assigning-people-to-a-market-where-both-sides-choose)** describes placement as a *two-sided matching market*: two groups, each with preferences about the other, and limited places.
2. **[The Core Bottleneck](#the-core-bottleneck--blocking-pairs-and-the-incentive-to-game)** names the problem: *blocking pairs*, a young person and an employer who would both rather be together than with what they were given, and the gaming that some systems reward.
3. **[From Forms to Estimates](#from-forms-to-estimates--lists-lotteries-and-the-risk-of-going-unmatched)** covers the data: ranked lists, scoring rules, a public lottery for ties, and a simulation (with a confidence interval) of how many people end up unmatched when they may list only 5 employers.
4. **[The Decision Engine](#the-decision-engine--deferred-acceptance)** runs **deferred acceptance** by hand on a six-person market, round by round, checks that the result has no blocking pairs, and shows why honest ranking is safe.
5. **[Scaling Up](#scaling-up--the-full-cohort-and-the-rules-around-it)** scales up to the full cohort: scoring rules, a second round, special constraints, and rules the program must publish and keep.
6. **[Code Implementation & Simulation](#code-implementation--simulation)** implements it from scratch in code and compares it with staff assignment and "first choices first."
7. **[Core Architectural Summary](#core-architectural-summary)** summarizes every piece on one page.

The idea that ties it together: **a placement sticks when no one has a better option that also wants them.**

---

## The Matching Leap – From Assigning People to a Market Where Both Sides Choose

### Why assignment by fit score breaks down

The tempting approach is to give staff, or a computer model, a **fit score** for every young person and every employer (skills, grades, distance) and then assign people to make the scores as high as possible. That treats placement like loading boxes onto trucks: the boxes don't have opinions.

People do. A young person who wanted to be a mechanic and is sent to a bakery may say no, or start and quit. An employer sent someone it didn't choose may refuse them. The program's own records show both. **A placement only works if both sides are willing**, and a fit score sees neither side's wishes.

### What a two-sided matching market is

A **matching market** is a setting where things are paired up and the price can't simply sort it out (no one is bidding for an apprentice). It is **two-sided** when both sides have preferences about the other:

1. **Young people rank employers.** Trade, location and reputation all matter to them.
2. **Employers rank young people.** They want to choose whom they train.
3. **Employers have capacities.** Each offers a fixed number of places, from 1 to 8.
4. **Each young person gets at most one place.** Some may get none.

A **matching** is the list of who goes where, respecting capacities. The question is which matching to pick, and by what procedure.

### Why matching, and not a vote or a waitlist

Two other approaches also let people choose, and it helps to see why neither fits here.

- **A community vote** ([Class 6: Participatory Allocation](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation)) splits *one shared budget* among projects according to residents' ballots; the [participatory budgeting tutorial](07-participatory-budgeting-neighborhood-fund.md) works through one. Here nobody votes on a common pot. Each young person wants particular employers and each employer wants particular young people, as the NGO told the finder: *"Both sides rank each other... There's no vote and no shared budget."* Preferences over specific partners on both sides are what make this a matching problem.
- **Assignment as people arrive** ([Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists)) places each person or item on the spot, before knowing who comes next, and usually only one side chooses (the program decides where a refugee family goes, say). This cohort is known all at once, twice a year, so everyone's lists can be collected first and matched together. If the program switched to rolling intake, with graduates arriving week by week, the problem would move toward Class 10; the [online assignment tutorial](11-online-assignment-refugee-placement.md) covers that setting.

### Mapping it to the program

| Matching term | In this program |
|---|---|
| Proposing side | The ~200 young people in the cohort |
| Receiving side | The 60 employers |
| Capacity | 1–8 places per employer, ~220 in total |
| Young people's preferences | A ranked list of up to 5 employers, on a paper form |
| Employers' preferences | A ranking of the applicants who listed them, or a scoring rule the placement officer applies |
| Tie-break | One lottery number per young person, drawn in public |
| Mechanism | The procedure that turns everyone's lists into a matching: here, deferred acceptance |
| Goal | A **stable** matching (defined in [The Core Bottleneck](#the-core-bottleneck--blocking-pairs-and-the-incentive-to-game)) reached by a procedure in which ranking honestly is safe |

These rows are the same as the [case's "Fit the model to your program" table](../cases/05-apprenticeship-matching.md#follow-up-1-fit-the-model-to-your-program) and the general Class 5 checklist in the [implementation playbook](../../prompt/knowledge/playbook.md#follow-up-1-fit-the-model-to-your-program).

---

## The Core Bottleneck – Blocking Pairs and the Incentive to Game

### A toy market to keep in mind

Throughout the tutorial we use a market small enough to check by hand: six young people and three employers with 5 places between them.

| Young person | 1st choice | 2nd choice | 3rd choice |
|---|---|---|---|
| Ana | Garage | Bakery | Clinic |
| Ben | Garage | Clinic | Bakery |
| Chi | Bakery | Garage | Clinic |
| Dan | Garage | Bakery | *(lists only two)* |
| Eva | Clinic | Garage | Bakery |
| Fin | Bakery | Clinic | Garage |

| Employer (places) | Ranking of applicants, best first |
|---|---|
| Garage (1) | Chi, Ben, Ana, Eva, Dan, Fin |
| Bakery (2) | Ana, Dan, Fin, Chi, Ben, Eva |
| Clinic (2) | Dan, Eva, Ben, Fin, Ana, Chi |

There are 6 people and 5 places, so at least one person goes unplaced whatever we do. (The real program has more places than people; the toy is deliberately tight so the steps are interesting.)

### Blocking pairs: why placements fall apart

Take any matching. A young person $y$ and an employer $e$ form a **blocking pair** if both of these are true:

1. $y$ prefers $e$ to the place $y$ was given (or $y$ was given nothing, or a place $y$ never listed), **and**
2. $e$ either has an empty place, or prefers $y$ to at least one person it was given.

A blocking pair is a deal waiting to happen outside the system. The young person turns down their placement, or quits after a week, and the employer takes them anyway, leaving another young person's placement or an employer's slot in the lurch. The program's 30 refusals and early quits, and employers who "took someone from another program instead," are what blocking pairs look like in the field.

A matching with **no** blocking pairs is called **stable**. Nobody has both the wish and the opportunity to defect, so the placements tend to stick. Stability is the central idea of the whole field, introduced by Gale and Shapley (1962).

### The second problem: systems that reward lying

Many programs ask people for their preferences and then use a rule that sounds fair: **"first choices first."** In round 1, each employer fills its places from people who listed it first, best-ranked first, and those acceptances are final. In round 2, places still open are filled from second choices, and so on. This was the rule used for Boston's school assignment before the city replaced it (Abdulkadiroğlu, Pathak, Roth & Sönmez, 2005), so it is often called the *Boston mechanism*.

Run it on the toy market with everyone honest:

- **Round 1 (first choices).** Garage (1 place) receives Ana, Ben and Dan; it ranks Ben highest of the three and takes him. Bakery (2 places) receives Chi and Fin and takes both. Clinic receives Eva and takes her, with one place left.
- **Round 2 (second choices).** Ana and Dan both list Bakery second, but Bakery is already full.
- **Round 3 (third choices).** Ana lists Clinic third and gets its last place. Dan listed only two employers, so he is **unmatched**.

| | Ana | Ben | Chi | Dan | Eva | Fin |
|---|---|---|---|---|---|---|
| First choices first, honest | Clinic (3rd) | Garage (1st) | Bakery (1st) | **unmatched** | Clinic (1st) | Bakery (1st) |

Notice the cruelty: **Bakery ranks Dan 2nd of everyone**, above Chi and Fin who got its places. Dan lost Bakery not because Bakery didn't want him but because he listed a more popular employer first and Bakery filled up while he was being turned down. That leaves 2 blocking pairs: (Ana, Bakery) and (Dan, Bakery).

Now suppose Dan works out the system and lists **Bakery first** instead of Garage. In round 1 Bakery receives Chi, Fin and Dan and takes its two favorites, Dan and Fin. Result: **Dan gets Bakery** (his true 2nd choice, better than nothing), and **Chi ends up unmatched**: she is turned down by Bakery, finds Garage full in round 2, and loses Clinic's last place to Ana in round 3.

So under "first choices first," lying pays, and it pays at someone else's expense. Young people who are well advised play it safe; those without advice, often the most disadvantaged, rank honestly and lose out. That is the gaming the case describes ("list a less-wanted employer first because they think they have a better chance there"). And because people misreport, the program no longer knows what anyone actually wants.

**The bottleneck in one sentence:** we need a procedure whose result has no blocking pairs, *and* in which no young person can do better by lying.

---

## From Forms to Estimates – Lists, Lotteries and the Risk of Going Unmatched

This section is about the inputs and about one number the program will be asked: *how many people might be left without a place?*

### Step 1: The data the match needs

Matching needs far less data than a prediction model. Three inputs:

| Input | Where it comes from | Format |
|---|---|---|
| Young people's ranked lists | Paper form: "Rank up to 5 employers, best first" | One row per person, 5 columns |
| Employers' rankings | Each employer ranks the applicants who listed it, **or** gives a scoring rule | One ranked list per employer, or a rule like "course grade, plus 1 if you live in our town" |
| Capacities | Each employer's number of places | One number per employer |

Historical data (past placements, completions) is not needed to *run* the match. It is needed to *judge* it afterwards: refusals and first-month quits compared with last cohort's 30 ([Scaling Up](#scaling-up--the-full-cohort-and-the-rules-around-it)).

### Step 2: Breaking ties with a lottery

A scoring rule produces ties. In the code's synthetic cohort the rule is "course grade (1–5), plus 1 if the applicant lives in the employer's town," so scores run from 1 to 6 and many applicants share a score. Someone has to decide which of two equal applicants gets the last place.

The fair and transparent answer is a **lottery**: before the match, each young person draws one random number between 0 and 1, in public. Whenever an employer must choose between two applicants with the same score, the lower number wins. Each number is a draw from the **uniform distribution**, meaning every value between 0 and 1 is equally likely. So among $k$ applicants tied on score, each one has the same chance of coming out on top:

$$
P(\text{a given applicant wins the tie}) = \frac{1}{k}
$$

That is $1/2 = 0.500$ for two tied applicants, $1/3 = 0.333$ for three, $1/4 = 0.250$ for four.

Two details matter in practice:

- **One number per person, used by every employer** (a *single* lottery), rather than a fresh draw at each employer. It is simpler to run and explain, and it is what the case recommends.
- **The lottery really matters.** In the code's sample cohort, 37 employers had to turn someone away, and for **25** of them the last place was decided by the lottery between applicants with the same score. A lottery drawn in private, or redrawn after the fact, would rightly be distrusted.

### Step 3: How many people end up unmatched? Estimate it by simulation

There are about 220 places for about 200 people, so you might expect everyone to be placed. But each person lists only 5 employers. If all 5 are popular and fill up with higher-ranked applicants, that person is **unmatched** even though places remain elsewhere.

We can't work this probability out with a formula, because it depends on everybody's lists at once. Instead we **simulate**: invent many cohorts that look like the program's, run the match on each, and count. Each synthetic cohort (details in [Code Implementation & Simulation](#code-implementation--simulation)) has 200 young people and 60 employers with 1–8 places adding to 220. Tastes are **correlated**: every employer has a popularity level that everyone sees, plus each person's own taste and a bonus for employers in their own town. So some employers are on many lists.

For each cohort we record the share of young people left unmatched. Over $R = 300$ cohorts we get 300 shares $x_1, \dots, x_{300}$. Their average estimates the expected share, and its **95% confidence interval** comes from the familiar formula for a mean:

$$
\bar x \pm 1.96 \times \frac{s}{\sqrt{R}}
$$

where $s$ is the standard deviation of the 300 shares. Repeating this for different list lengths:

| Employers each person may list | Average share unmatched | 95% confidence interval | About how many of 200 |
|---|---|---|---|
| 3 | 20.5% | 20.1% to 21.0% | 41.1 |
| **5** | **12.5%** | **12.2% to 12.9%** | **25.1** |
| 8 | 6.8% | 6.6% to 7.1% | 13.7 |
| 12 | 3.4% | 3.2% to 3.6% | 6.8 |

The intervals are narrow because 300 cohorts is plenty; the uncertainty that really matters is whether the synthetic cohorts resemble the real one. In none of the 300 cohorts with 5-employer lists was everyone placed.

How to read this:

- **These percentages are illustrative.** They depend on how strongly tastes agree. If everyone wants the same three employers, many more people go unmatched; if tastes are spread out, fewer do. The *pattern* is the lesson.
- **Longer lists help a lot.** In this synthetic market, going from 5 to 8 choices roughly halves the number left out. Under deferred acceptance, adding employers to the **end** of your list can never hurt you: you only reach them after everything above has turned you down ([The Decision Engine](#the-decision-engine--deferred-acceptance) explains why).
- **Some unmatched people are likely**, so plan a **second round** from the start ([Scaling Up](#scaling-up--the-full-cohort-and-the-rules-around-it)). With the paper form limited to 5 choices, the second round is not optional.

---

## The Decision Engine – Deferred Acceptance

### The idea

Gale and Shapley's (1962) **deferred acceptance** algorithm fixes the weakness of "first choices first": an employer's yes is not final until the very end. Employers only *hold* their best applicants so far, and can swap a held applicant for a better one who arrives later. With the young people proposing, it runs like this:

1. **Propose.** Every young person who is not currently held applies to the highest employer on their list they haven't tried yet.
2. **Hold or reject.** Each employer looks at everyone it is holding plus its new applicants, **holds** its favorites up to its capacity, and **rejects** the rest. Being held is a "maybe," not a "yes."
3. **Repeat** until no rejected person has an employer left to try.
4. **Finalize.** Everyone held becomes matched to the employer holding them. Anyone who ran out of choices is unmatched.

A person who is rejected only loses a "maybe," and moves down their own list. A person who is held can still be bumped by someone the employer likes more.

### Step-by-step concrete example: the toy market

Here is the code's printout of every round on the toy market from [The Core Bottleneck](#the-core-bottleneck--blocking-pairs-and-the-incentive-to-game). Read "Garage ← Ana, Ben, Dan" as "Ana, Ben and Dan apply to Garage this round."

**Round 1.** Everyone applies to their first choice.
- Garage ← Ana, Ben, Dan. Garage has 1 place and ranks Ben highest of the three: **holds Ben**, rejects Ana and Dan.
- Bakery ← Chi, Fin. Two places, two applicants: **holds Fin and Chi**.
- Clinic ← Eva: **holds Eva**.

**Round 2.** Ana and Dan, just rejected, try their second choice, Bakery.
- Bakery now considers Fin and Chi (held) plus Ana and Dan (new). Its ranking is Ana, Dan, Fin, Chi: it **holds Ana and Dan** and rejects Fin and Chi.

This is the step "first choices first" could not take: Bakery gets to change its mind when better applicants arrive.

**Round 3.** Fin and Chi try their second choices.
- Clinic ← Fin. Clinic has a free place: **holds Eva and Fin**.
- Garage ← Chi. Garage ranks Chi above Ben (Chi is its first choice overall): **holds Chi**, rejects Ben.

**Round 4.** Ben tries his second choice.
- Clinic ← Ben. Clinic considers Eva, Fin and Ben; its ranking puts Eva 2nd, Ben 3rd, Fin 4th: **holds Eva and Ben**, rejects Fin.

**Round 5.** Fin tries his third and last choice.
- Garage ← Fin. Garage prefers Chi, whom it holds: rejects Fin. Fin has no employers left.

Nobody has anyone left to propose to, so the holds become final:

| | Ana | Ben | Chi | Dan | Eva | Fin |
|---|---|---|---|---|---|---|
| Deferred acceptance | Bakery (2nd) | Clinic (2nd) | Garage (2nd) | Bakery (2nd) | Clinic (1st) | unmatched |

### Step-by-step check: is it stable?

Test every young person against every employer they listed **above** what they got. If the employer has a free place or prefers them to someone it holds, that's a blocking pair.

| Person | Got | Employers they'd prefer | Would that employer take them? |
|---|---|---|---|
| Ana | Bakery | Garage | No: Garage holds Chi, its 1st choice; Ana is its 3rd |
| Ben | Clinic | Garage | No: Chi (1st) is ahead of Ben (2nd) |
| Chi | Garage | Bakery | No: Bakery holds Ana (1st) and Dan (2nd); Chi is 4th |
| Dan | Bakery | Garage | No: Chi (1st) is ahead of Dan (5th) |
| Eva | Clinic | none: Clinic is her 1st choice | — |
| Fin | nothing | Bakery, Clinic, Garage | No: Bakery holds its 1st and 2nd (Fin is 3rd); Clinic holds its 2nd and 3rd (Fin is 4th); Garage holds its 1st (Fin is 6th) |

**Zero blocking pairs.** The code confirms it, and also checks every possible way of placing the six people with an employer they listed, or nowhere: this is the **only** stable matching of the toy market. Fin is unmatched in every stable matching, because with 5 places someone must be, and every employer prefers the people it has.

### The same market under staff assignment

Now let staff assign by a fit score instead (the fit scores, 0–10, are in the code; they reflect skills and the officer's judgment, not anyone's ranking). Taking the highest score first and filling places as they come:

| | Ana | Ben | Chi | Dan | Eva | Fin |
|---|---|---|---|---|---|---|
| Staff fit score | Clinic (3rd) | Bakery (3rd) | Garage (2nd) | Clinic (not listed) | Bakery (3rd) | unmatched |

Run the same check and **7 blocking pairs** appear: (Ana, Bakery), (Ben, Clinic), (Chi, Bakery), (Dan, Bakery), (Eva, Clinic), (Fin, Bakery), (Fin, Clinic). For instance, Eva is sent to her last choice, Bakery, while Clinic, her first choice, holds Ana, whom it ranks 5th of 6 and who herself would rather be at Bakery. Every one of those pairs is a likely refusal or early quit, and Dan has been sent somewhere he never asked to go.

### Why honest ranking is safe for the proposing side

Under deferred acceptance with young people proposing, **no young person can get a better result by misreporting their list**. This is a classic result of matching theory, explained for general readers in Roth (2015). The intuition:

- Your list only controls the **order** in which you try employers.
- If an employer turns you down, it is because it is holding enough people it prefers to you. Applying to it earlier or later doesn't change that.
- Trying a popular employer first costs you nothing: unlike "first choices first," the places at your second choice are not given away permanently while you wait. If your second choice wants you, it will still bump someone it likes less.

The code tests this exhaustively on the toy market: for each of the six people, it tries **all 15 possible lists** (every ordering of 1, 2 or 3 of the employers) while everyone else stays honest. Nobody does better than with their honest list. Dan's trick from [The Core Bottleneck](#the-core-bottleneck--blocking-pairs-and-the-incentive-to-game), listing Bakery first, still gets him Bakery, exactly what honesty already gave him. Fin, who is unmatched, stays unmatched whether he lists Garage–Bakery–Clinic, Clinic–Bakery–Garage, only Clinic, or anything else.

So the program can publish, truthfully: *"Rank employers in your true order of preference. Listing a popular employer first never hurts your chances."*

### The trade-off: the proposing side gets its best stable outcome

Some markets have more than one stable matching, and then it matters who proposes. A two-person example from the code: Xia prefers the Print shop to the Salon, Yaw prefers the Salon to the Print shop; but the Print shop prefers Yaw and the Salon prefers Xia. Both of these are stable:

| | Xia | Yaw |
|---|---|---|
| Young people propose | Print shop (1st) | Salon (1st) |
| Employers propose | Salon (2nd) | Print shop (2nd) |

When young people propose, each gets their first choice and each employer gets its second; when employers propose, it's the reverse. In general, deferred acceptance gives the proposing side the **best stable matching for every one of its members**, and the other side the worst stable one. This NGO's mission is the young people, and their honest ranking is the guarantee it wants, so **young people propose**. (The flip side: employers could, in principle, gain by misreporting. A published scoring rule, applied by the placement officer, leaves them little room to.)

In real markets the difference between the two versions is usually small; the toy market above has only one stable matching, so both versions agree there.

---

## Scaling Up – The Full Cohort and the Rules Around It

**1. Full size is not a problem.** The algorithm is the same for 200 young people and 60 employers as for six and three. In the code's sample cohort it finishes in 15 rounds. The placement officer can keep the lists in Excel and run the match with a short script or the free `matching` library ([Code Implementation & Simulation](#code-implementation--simulation)).

**2. Employers that rank vs. employers that use a rule.** Some employers will rank applicants themselves; others will prefer to give a rule ("course grade, plus 1 if local") that the officer applies, with the public lottery for ties. Both produce a ranked list, and that's all the algorithm needs. Employers should rank only applicants they would genuinely take; anyone left off is treated as unacceptable to that employer.

**3. A second round for the unmatched.** [From Forms to Estimates](#from-forms-to-estimates--lists-lotteries-and-the-risk-of-going-unmatched) showed that with 5-choice lists some people will be left out while places remain. After the main match, give the unmatched a short second form listing only employers with places left, and run deferred acceptance again on those places. In the code's sample cohort, 35 people were unmatched after the main round while 18 employers still had 55 places; the second round placed **34 of the 35**. Averaged over 100 synthetic cohorts, the second round left 0.14 people unmatched. The main round's results are not reopened, so nobody placed in round 1 can be bumped.

**4. Special constraints.** The case asks whether any young people need placements in the same town (siblings) or near transport or accessible sites. Constraints on a *single* person ("only employers on a bus route") are easy: they just shorten that person's list. Constraints that **link two people**, such as two siblings who must be placed in the same town, are harder. Couples and linked applications can make a stable matching **fail to exist** at all; the redesigned US medical residency match had to handle couples for this reason (Roth & Peranson, 1999). If there are only a handful of such cases, handle them openly before the match (for example, by agreeing their placements with the employers concerned) and record that you did.

**5. Publish the rules in plain language, before anyone fills in a form.** At minimum: how many employers can be listed; that young people propose; how employers rank; how the lottery is drawn; that there is a second round; and the honesty statement from [The Decision Engine](#the-decision-engine--deferred-acceptance).

**6. No manual overrides.** If staff "fix" individual results after the match, two promises break at once: the result may no longer be stable, and honest ranking is no longer safe, because people will learn that lobbying staff works. Agree in writing, before the match, that results stand. This is one of the readiness checks in the [playbook](../../prompt/knowledge/playbook.md#follow-up-2-readiness-checks).

**Evidence that this scales.** Deferred acceptance runs the US medical residency match (Roth & Peranson, 1999), the closest parallel here: workers and employers ranking each other, with employers taking several people each. When New York City redesigned its high-school admissions around it, the number of students assigned to a school they had not chosen fell from about 30,000 to about 3,000 in the first year (Abdulkadiroğlu, Pathak & Roth, 2005). Boston's switch away from "first choices first" is the clearest documented case of replacing a mechanism that rewarded strategic ranking (Abdulkadiroğlu, Pathak, Roth & Sönmez, 2005).

---

## Code Implementation & Simulation

The full program is [`code/case5_deferred_acceptance.py`](code/case5_deferred_acceptance.py). It needs only `numpy` and the Python standard library, and runs in seconds:

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case5_deferred_acceptance.py
```

Deferred acceptance is written out from scratch so every step is visible. For production use, the [`matching`](https://github.com/daffidwilde/matching) Python library's **hospital–resident** solver does the same job, with employers as "hospitals" and young people as "residents" (see [build options in the playbook](../../prompt/knowledge/playbook.md#follow-up-4-build-options--tools-and-partners)).

### Deferred acceptance, one round at a time

```python
while True:
    proposals = {}
    for p in free:                                    # everyone not being held...
        if next_choice[p] < len(youth_lists[p]):      # ...with someone left to try
            e = youth_lists[p][next_choice[p]]
            next_choice[p] += 1
            proposals.setdefault(e, []).append(p)
    if not proposals:
        break                                         # nobody left to propose: done
    new_free = []                                     # anyone rejected this round
    for e, applicants in proposals.items():
        pool = held[e] + applicants                   # held so far + new applicants
        acceptable = [p for p in pool if p in employer_rank[e]]
        acceptable.sort(key=lambda p: employer_rank[e][p])
        held[e] = acceptable[:capacity[e]]            # keep the best, up to capacity
        new_free += [p for p in pool if p not in held[e]]
    free = new_free
```

(The file's version also keeps a log of each round, which is how the walkthrough in [The Decision Engine](#the-decision-engine--deferred-acceptance) was printed.)

### The stability check

```python
for p, lst in youth_lists.items():
    got = match[p]
    cut = lst.index(got) if got in lst else len(lst)
    for e in lst[:cut]:                               # employers p prefers to what p got
        if p not in employer_rank[e]:
            continue                                  # e would never take p
        given = [q for q, f in match.items() if f == e]
        if len(given) < capacity[e]:                  # e has an empty place
            pairs.append((p, e))
        elif any(employer_rank[e].get(q, 10**9) > employer_rank[e][p] for q in given):
            pairs.append((p, e))                      # e prefers p to someone it has
```

### The synthetic cohort

Each simulated cohort follows the case: 200 young people, 60 employers with 1–8 places adding up to 220, 4 towns. A young person's liking for an employer is the employer's popularity (shared by everyone) plus their own random taste plus a bonus if the employer is in their town; each lists their top 5. Employers rank by the scoring rule "grade (1–5) + 1 if same town," ties broken by the single public lottery. In the sample cohort (seed 2026), the most popular employer was the first choice of 16 people and had 7 places.

Three ways of placing people are compared on the same cohort:

- **Staff fit score:** assign the highest fit score anywhere first, then the next, until places run out. The fit score combines the employer's score, a partial reading of the young person's interests, and the officer's judgment; it does not use the ranked lists.
- **First choices first:** the Boston-style rule from [The Core Bottleneck](#the-core-bottleneck--blocking-pairs-and-the-incentive-to-game), with everyone ranking honestly.
- **Deferred acceptance:** young people propose.

```
Simulation - one synthetic cohort (seed 2026): 200 young people, 60 employers
  places: 220  capacities range 1-8
  most popular employer is the first choice of 16 people and has 7 places
  deferred acceptance took 15 rounds
  employers that turned someone away: 37; of these, last place decided by the lottery among equal scores: 25
  method                     blocking pairs  top choice  any listed  not listed  unmatched
  staff fit score                       414       0.085       0.265         147          0
  first choices first                    76       0.560       0.800           0         40
  deferred acceptance                     0       0.405       0.825           0         35
  second round: 35 unmatched people, 18 employers with 55 places left; placed 34, still unmatched 1

Simulation - the same comparison averaged over 100 cohorts (seeds 0-99)
  method                     blocking pairs  top choice  any listed  not listed  unmatched
  staff fit score                     382.3       0.104       0.338       132.5        0.0
  first choices first                  56.1       0.574       0.852         0.0       29.7
  deferred acceptance                   0.0       0.447       0.874         0.0       25.2
  second round after deferred acceptance: placed 25.0 on average, still unmatched 0.14
```

Column guide: *top choice* and *any listed* are shares of the 200 young people; *not listed* counts people placed with an employer that wasn't on their list; *unmatched* counts people with no place.

### Reading the results

**Staff fit score places everyone, on paper.** But in the sample cohort 147 of the 200 were sent to an employer they never listed, and there were 414 blocking pairs. Each of those placements is a candidate for exactly what happened last cohort: a refusal or an early quit. "Zero unmatched" is an illusion if people won't take the place.

**Deferred acceptance has zero blocking pairs, every time.** In the sample cohort it placed 165 people (82.5%) with an employer on their list, 81 of them (40.5%) at their first choice, and left 35 unmatched before the second round. After the second round, only 1 person was without a place.

**"First choices first" looks better on top choices, and that is the trap.** With everyone honest it gives 56.0% their first choice against 40.5% for deferred acceptance, because it locks in first choices before anything else. But it pays for that with 76 blocking pairs and 5 more people unmatched (40 against 35) in the sample cohort, and its numbers assume people rank honestly, which [The Core Bottleneck](#the-core-bottleneck--blocking-pairs-and-the-incentive-to-game) showed they have every reason not to. Once people game it, its "first choice" figures describe the lists people were coached to write, not what they want. Across 100 cohorts the picture is the same: about 56 blocking pairs on average, and more people unmatched (29.7 against 25.2).

**The second round matters.** Averaged over 100 cohorts, deferred acceptance left 25.2 people unmatched after the main round, and the second round placed 25.0 of them on average.

### The simpler alternative: run deferred acceptance by hand

In this class the best method *is* the simple one. Deferred acceptance needs no prediction, no solver and no data beyond the ranked lists; the [round-by-round example](#the-decision-engine--deferred-acceptance) is exactly what staff would do on paper. With 200 young people and 60 employers it took 15 rounds in the sample cohort: each round, every unplaced young person's form moves to their next employer, and each employer keeps its best applicants up to its places. A wall of envelopes, one per employer, works; so does a spreadsheet with one row per young person, or the free `matching` library for a volunteer who codes.

What to check before running it by hand:

- **Market size.** Up to a few hundred people and a few dozen employers is a day's work for two staff with a checklist; much larger, use the library. The result is the same either way, which is worth saying in the published rules.
- **Employers' rankings must exist before the match.** If employers rank by a scoring rule, apply it first and write each employer's ordered list down; if they insist on interviewing after seeing who applied, that is a different, slower process.
- **The tie-break lottery must be drawn before the match, in public.** By hand it is a numbered draw; that is the simplest step to get wrong.
- **The tempting shortcut is worse.** "First choices first" is also easy by hand, but it gives everyone a reason to rank strategically (Abdulkadiroğlu and Sönmez, American Economic Review, 2003, show this for the old Boston school-choice rule) and left about 56 blocking pairs per cohort here.

Cautions:

- **The cohorts are invented.** The popularity spread, the taste noise and the scoring rule are made up to teach the method. Real shares of first choices and of unmatched people depend on how much young people's tastes agree, which only the program's own forms will show.
- **A blocking pair is a risk, not a certainty.** Not every young person in a blocking pair will actually quit, and employers may not poach. Stability removes one cause of refusals and dropouts, not all of them: a stable match does not guarantee anyone completes the apprenticeship.
- **The comparison is on reported lists.** Stability is checked against what people wrote down. If the form allows only 5 choices, preferences beyond the fifth are invisible to the match.

---

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| **Two-sided market** | young people $Y$, employers $E$, capacities $c_e$ | Treats placement as a choice on both sides, not an assignment |
| **Ranked lists** | each $y$ ranks up to 5 employers; each $e$ ranks applicants or gives a scoring rule | The only data the match needs; collected on a paper form and by email |
| **Lottery tie-break** | one uniform number per person; $P(\text{win a } k\text{-way tie}) = 1/k$ | Breaks equal scores fairly and visibly; drawn in public before the match |
| **Blocking pair** | $y$ prefers $e$ to what $y$ got, and $e$ has room or prefers $y$ to someone it got | Predicts refusals, quits and poaching |
| **Stability** | no blocking pairs | Placements no one has both the wish and the chance to abandon |
| **Deferred acceptance** | propose → hold best up to $c_e$ → reject rest → repeat | Always produces a stable matching; honest ranking is safe for the proposing side |
| **Unmatched-risk simulation** | $\bar x \pm 1.96\, s/\sqrt{R}$ over simulated cohorts | Estimates how many people end up without a place for a given list length |
| **Second round** | deferred acceptance on the places left | Places most of those whose 5 choices all filled up |
| **Published rules, no overrides** | "Rank in your true order. Listing a popular employer first never hurts your chances." | Keeps the honesty guarantee true in practice |

### Where to go next

- **Run the shadow pilot** described in the [case's follow-ups](../cases/05-apprenticeship-matching.md#after-the-recommendation): run the match alongside staff assignment for one cohort, then compare refusals and first-month dropouts with last cohort's 30 (see also [pilot design in the playbook](../../prompt/knowledge/playbook.md#follow-up-3-pilot-design)).
- **Read** Roth, *Who Gets What — and Why* (2015), a book for general readers by one of the designers of these matches; then Roth & Peranson (1999) on the residency match and Abdulkadiroğlu, Pathak & Roth (2005) on New York City, listed in the [playbook's reading list](../../prompt/knowledge/playbook.md#follow-up-5-reading-and-people-to-contact). Gale & Shapley (1962), *College admissions and the stability of marriage*, is the original paper and is short.
- **Code to build on:** the [`matching`](https://github.com/daffidwilde/matching) Python library's hospital–resident solver.
- **Other tutorials:** [restless bandits for home visits](01-restless-bandits-chw-visits.md), [welfare optimization for borehole siting](02-welfare-optimization-borehole-siting.md), [security games for marine patrols](03-security-games-marine-patrols.md), [robust optimization for cyclone pre-positioning](04-robust-optimization-cyclone-prepositioning.md), [when no model is needed: the food pantry](06-no-model-food-pantry.md), [participatory budgeting for a neighborhood fund](07-participatory-budgeting-neighborhood-fund.md) (the other *People choose* class, where the community votes on one budget), and [online assignment for refugee placement](11-online-assignment-refugee-placement.md) (placing people as they arrive).
