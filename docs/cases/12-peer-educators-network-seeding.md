# Case 12: Choosing peer educators for HIV prevention at a youth shelter

| | |
|---|---|
| **Domain** | Sexual health and youth homelessness |
| **Intervention type** | Peer education (a message passed person to person) |
| **Expected class** | [11 — Network Seeding (influence maximization)](../../prompt/knowledge/taxonomy.md#class-11-network-seeding) |
| **Most likely confusion** | Training the most at-risk youth, or letting staff pick "natural leaders" with no model |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/12-network-seeding-peer-educators.md) |

## Scenario

A city youth-services NGO runs a shelter and drop-in center used by about 400 young people aged 16–24. It has funding to train 25 of them as peer educators on HIV prevention (testing, PrEP, condom use) over a two-day course. The goal is for the message to reach as many residents as possible through conversations among the youth themselves. Until now, case workers have picked the trainees.

*This is an illustrative scenario, not a real program.*

## Interview answers

Paste these one at a time, in order, when testing the assistant.

**Filter 1 — The resource and its intent.**
> We're allocating 25 places on a peer-educator training. We want HIV-prevention information to reach as many of the roughly 400 young people at the shelter as possible.
>
> *(Next turn, which option fits best?)* (e), definitely. The training is a message we want them to pass on to their friends. Nobody benefits much from the course alone.

**Filter 2 — Choice and preferences.**
> We choose whom to invite. They can say no, and some will, but there's no ranking on their side; they just accept or decline.

**Filter 3 — Environment dynamics.**
> No one avoids us. The youth come and go, and some are wary of staff, but nobody is working against the program.

**Filter 4 — Tolerance for being wrong.**
> A poor choice means the message spreads less, not that anyone is harmed. We can run another training next season.
>
> *(Next turn, what records?)* Nothing useful. We have intake records, but no data on who trained before or how far the message went.

**Filter 5 — Field data and workflow friction.**
> Staff could run a short survey on the shelter's tablets during check-in; most residents pass the front desk every day. We use Excel.
>
> *(Next turn, who would run the tool?)* Our program manager would own it. We don't have a data person, but a graduate student volunteers with us.

**Narrowing question (Spread).** *"Do you know, even roughly, who talks to whom, or could people name the trusted messengers in their community?"*
> Not today, but we could ask residents who their closest friends at the shelter are, on the tablets.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> No. The training is the same for everyone we choose.

## Why Class 11: Network Seeding

The assistant should select **[Class 11 (Network Seeding)](../../prompt/knowledge/taxonomy.md#class-11-network-seeding)**, solved with influence maximization and greedy seed selection.

- **A message people should pass on** (Filter 1 — The resource and its intent, option e) places the problem in the *Spread through people* family. The value lies in the conversations the 25 trainees start, not in the training itself. That rules out [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) and [Class 7 (Effect-Based Targeting)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting), which are for benefits that stay with the person who receives them.
- **Central invitation with a yes/no reply** (Filter 2 — Choice and preferences) is not two-sided ranking, so [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) does not apply. Refusals matter, but as a planning input (backup seeds), not as preferences.
- **No adversary** (Filter 3 — Environment dynamics) rules out [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search). **Cheap, fixable errors** (Filter 4 — Tolerance for being wrong) mean no [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) layer.
- **A tablet survey at check-in** (Filter 5 — Field data and workflow friction) can supply the "rough map of who knows whom" Class 11 needs, and the narrowing answer confirms it: residents can name their closest friends → Class 11. Had they said no, the assistant should fall back to a simpler rule, such as asking staff to nominate trusted messengers.

## What a good recommendation contains

**1. Class.** Influence maximization (Kempe, Kleinberg & Tardos, 2003). Map who knows whom with a short friendship survey, model how likely a friend is to pass the message on, then pick the 25 residents whose *combined* reach is largest, using the greedy method: add one seed at a time, each time choosing the person who adds the most new reach. This naturally avoids putting several seeds in the same friendship cluster. The research group behind the closest work is Bryan Wilder (Carnegie Mellon) and Eric Rice (USC).

**2. Counterfactual warning.** Training the 25 most at-risk youth (a risk ranking, as in Class 2) treats training as a benefit that stays with the person; at-risk youth may be peripheral in the network, so the message stops with them. Letting staff choose the most visible "leaders" tends to pick friends of one another, so several seeds reach the same people and whole groups hear nothing. Picking the 25 with the most friends has the same flaw. None of these plans for refusals.

**3. Field pathway.** At check-in, staff ask each consenting resident to name up to three closest friends at the shelter on the tablet (or answer "who here is good at spreading news?" as a cheaper fallback). The graduate student runs a short script once per training cycle on pseudonymized IDs and returns a ranked list of 25 seeds plus 10 ranked backups to the program manager. Case workers see only names to invite; when someone declines, they invite the next backup. If the survey falls short, staff picks remain the fallback.

**4. Evidence.** The closest parallels are direct: Yadav et al. (IJCAI 2018) ran pilots with 173 youth in Los Angeles shelters, using algorithm-chosen peer leaders to raise HIV awareness, and Wilder et al. (AAAI 2021) reported a trial with 713 youth experiencing homelessness in which risk behavior fell in the arm whose peer leaders the algorithm chose. These are research pilots and a trial, not routine deployments. Banerjee et al. (Review of Economic Studies, 2019) is a parallel from another domain: in Haryana, India, seeding immunization reminders with villagers nominated as good spreaders of news raised vaccinations (about 22% in the paper's abstract; J-PAL's summary reports 27%). It shows the cheaper "nominate a spreader" proxy works.

**5. Report card.**
- *Successes:* in the 2021 trial, risk behavior fell in the algorithm-chosen arm, with the shelter population matching this case closely.
- *Challenges:* shelter populations change week to week, so the network goes stale; invited youth decline or leave before training; residents may hesitate to name friends to staff.
- *Unknowns:* how likely a friend is to pass the message on (it must be guessed roughly); whether a friendship map collected by staff could be misused (it reveals who associates with whom in a vulnerable population); how much better than staff picks it will be *at this shelter*.

**6. Simpler alternative.** Count friends from the tablet survey and pick the most-named residents, spread across friend groups in proportion to each group's size; where a survey isn't possible, ask residents "who here is good at spreading news?" or train the friends that residents name. In the [tutorial](../tutorials/12-network-seeding-peer-educators.md#the-simpler-alternative-count-friends-spread-across-groups) the spread-out count reached about 94% as many residents as greedy seeding and far more than staff picks (illustrative data). It is close on reach when friend groups are clear and the message travels only a step or two; the gap grows when people pass a message on readily. Check before settling for it: staff can tell where the friend groups are; the count includes residents who didn't answer but were named. The asking rules have field evidence elsewhere (Banerjee et al., 2019; Kim et al., 2015), in other settings and for other messages.

**Next steps.** Draft a one-screen consent and friendship question with the shelter's safeguarding lead; collect two weeks of answers on the tablets; have the volunteer produce a seed list and a staff-picked list for comparison before the next training.

## What the assistant should *not* do

- Recommend training the highest-risk youth (Class 2 logic) or treat this as a prediction problem.
- Say "no model needed, staff can choose" without noting that staff picks cluster; a staff list is the right *comparison*, not the default.
- Quote a percentage reduction in risk behavior from Wilder et al. (2021); the taxonomy records only that it fell.
- Ignore consent, privacy and safe storage of friendship data for minors and homeless youth.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

A good answer maps each element of network seeding to this program, citing the interview answer it came from:

| Element | For this program | From |
|---|---|---|
| Population | The roughly 400 young people using the shelter | Filter 1 — The resource and its intent |
| Network data | Tablet survey at check-in: "Name up to three closest friends here." Fallback: "Who here is good at spreading news?" | Filter 5 — Field data and workflow friction; narrowing answer |
| Seeds | 25 training places | Filter 1 — The resource and its intent |
| Spread model | A rough, assumed chance that a friend passes the message on; test a low and a high value and check the seed list barely changes | Filter 4 — Tolerance for being wrong (no past data) |
| Participation | Some invitees will decline or leave; rank 10 backups and refill each place with the next backup who adds the most new reach | Filter 2 — Choice and preferences |
| Outcome | Residents who have heard the message, measured by a follow-up tablet question ("Has another resident talked to you about HIV testing or PrEP?") | Filter 1 — The resource and its intent |
| Privacy | Opt-in consent; pseudonymized IDs; the friendship file stored encrypted, accessible only to the program manager and the volunteer, deleted after the cycle | Ethics |

It should flag the gap that matters most: **the friendship map ages fast.** Residents arrive and leave weekly, so collect it in the two weeks before each training, not once a year.

### Follow-up 6: One-page brief for a technical partner

```
PROJECT BRIEF — Youth shelter peer-educator program (illustrative)

The decision we need help with
  Which 25 of about 400 shelter residents to invite to a peer-educator
  training on HIV prevention, once per training cycle.

Why it matters
  The message only reaches residents if trainees pass it on. Staff picks
  tend to cluster in one friendship group, so many residents hear nothing.

Current approach
  Case workers choose trainees by judgment. No record of how far the
  message spread.

Recommended approach
  Class 11 (Network Seeding): influence maximization with greedy seed
  selection, because the benefit spreads through friendships and residents
  can tell us who their closest friends are.

Simpler option to beat
  The most-named residents, spread across friend groups. Close on reach when
  groups are clear; falls behind when the message spreads easily.

Data we have
  None yet. Planned: a consented tablet survey at check-in naming up to
  three closest friends; pseudonymized IDs; Excel export.

Constraints
  25 places per training. Invitees may decline: we need 10 ranked backups.
  Sensitive population: data encrypted, access limited, deleted after use.

What success looks like
  Share of residents who report hearing the message, compared with a
  staff-picked cohort. Harm measure: any complaint or breach involving
  the friendship data.

How results must reach staff
  A list of 25 names plus 10 backups for the program manager, once per cycle.

What we are asking for
  A short script (NetworkX) and help designing a two-cycle comparison
  with staff picks.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** consent covering network data, reviewed by the safeguarding lead (residents under 18 may need extra steps); enough trainers for 25; a follow-up question that measures spread; a named owner for the encrypted file.
- **3. Pilot design:** alternate training cycles (or, if the NGO has two sites, sites) between model-chosen and staff-picked seeds for 2–6 months; compare the share of residents who report hearing the message.
- **4. Build options:** [NetworkX](https://networkx.org) stores the network and the greedy method is a short script, so the volunteer graduate student can build it; DataKind, Statistics Without Borders or a local university are backups. Confirm each is still active before relying on it.
- **5. Reading and contacts:** start with Banerjee et al. (2019), *Using Gossips to Spread Information*; then Wilder et al. (2021) on the HIV-prevention trial and Kempe, Kleinberg & Tardos (2003). Bryan Wilder (Carnegie Mellon) and Eric Rice (USC) work on peer-leader selection for this population.
