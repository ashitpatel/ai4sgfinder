# Case 8: Business grants for women shopkeepers

| | |
|---|---|
| **Domain** | Livelihoods and women's economic empowerment |
| **Intervention type** | One-off grant with business training |
| **Expected class** | [7 — Effect-Based Targeting (policy learning)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) |
| **Most likely confusion** | Ranking applicants by poverty and funding the poorest ([Class 2](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting)) |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/08-policy-learning-business-grants.md) |

## Scenario

A women's enterprise NGO has funding for 600 one-off grants, each paired with a short business-training course, for women who run small shops. The goal is higher household income a year later. Last year it ran a randomized pilot: of 3,000 applicants, some were offered the grant by lottery and the rest were not, and income was measured for both groups a year later. This year's call is open now, and applications come in through a phone app. The question is which 600 applicants to fund.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We give 600 grants, each with business training, to women who run small shops. The goal is that their income is higher a year later. It's handed over once and they keep it; we don't take it back or give a second one.

**Filter 2 — Choice and preferences.**
> We choose who receives it. Women apply, but they don't pick between options and we don't negotiate.

**Filter 3 — Environment dynamics.**
> Nobody avoids us. But applicants might exaggerate how poor they are, because they assume the poorest get chosen.

**Filter 4 — Tolerance for being wrong.**
> A wrong choice wastes a grant, which hurts, but it isn't dangerous. Nobody's safety depends on it.

*Next turn (records):*
> Last year we ran a randomized pilot with 3,000 applicants and measured income a year later, for those offered the grant and those who weren't.

**Filter 5 — Field data and workflow friction.**
> Applications come through an app: name, location, how long the shop has been open, what it sells, household size, and a few questions about income and assets. Pilot data is in the same format.

*Next turn (who runs it):*
> Our analyst uses R. Selection is done once a year, after the call closes.

**Narrowing 1 — "Do you know everyone who could receive it before you decide, or do people or items arrive one at a time and need a decision on the spot?"**
> We know all applicants before deciding. The call closes on a fixed date and we select after that.

**Narrowing 2 — "Do you have pilot or trial results showing the program helps some kinds of people much more than others?"**
> Yes. The pilot showed big income gains for women who had run a shop for two years or more, and little for very new businesses.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> No. The grant and training come as one package this year.

## Why Class 7: Effect-Based Targeting

The assistant should select **[Class 7 (Effect-Based Targeting)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting)**, solved with causal forests and a short learned targeting rule.

- **Handed over once and kept** (Filter 1 — The resource and its intent, option a) places the problem in the *who gets a limited resource* family. A one-off grant rules out [Class 1 (Dynamic State Evolution)](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution), which needs a resource reused round after round.
- **Central choice** (Filter 2 — Choice and preferences) keeps that family and rules out [Class 5 (Strategic Matching Markets)](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) and [Class 6 (Participatory Allocation)](../../prompt/knowledge/taxonomy.md#class-6-participatory-allocation).
- **No adversary over territory, but applicants may exaggerate** (Filter 3 — Environment dynamics). That is not [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search); the decision tree says to keep the class and build the rule from characteristics that are hard to game.
- **A wasted grant, not a catastrophe, plus randomized trial results** (Filter 4 — Tolerance for being wrong): [Class 4 (Robust Contingency Planning)](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) isn't needed, and trial results are exactly what opens Class 7. With outcomes a year away and one program rather than several options, [Class 8 (Learn-While-Allocating)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) doesn't fit either.
- **App data and an R analyst** (Filter 5 — Field data and workflow friction) meet Class 7's data need: a randomized pilot with outcomes and characteristics for each participant.
- **Everyone is known before the decision** (Narrowing 1) rules out [Class 10 (Online Assignment & Waitlists)](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists). **The effect differs sharply by shop age** (Narrowing 2) points to Class 7 rather than [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting).

## What a good recommendation contains

**1. Class.** Effect-based targeting (policy learning). Use the pilot to estimate, for each kind of applicant, how much the grant *raises* income a year later (a causal forest), then learn a short rule, such as a two- or three-question decision tree, that selects the 600 applicants with the largest expected gain. Check the rule on part of the pilot held back from fitting before using it. Frameworks: causal forests (Wager & Athey, 2018), empirical welfare maximization (Kitagawa & Tetenov, 2018) and policy learning (Athey & Wager, 2021), from Susan Athey and Stefan Wager's work at Stanford.

**2. Counterfactual warning.** Ranking applicants by poverty and funding the poorest 600 sends many grants to very new businesses, where the pilot found little gain, so the same money buys much less income. A standard prediction model of "who will earn most next year" is no better: it picks women who would have done well anyway. Both approaches target the outcome, not the *change* the grant causes. And a need ranking built on self-reported income rewards exactly the exaggeration Filter 3 describes.

**3. Field pathway.** The analyst runs the model in R once, after the call closes, on the app export. Staff never see a forest: they get the final rule written as a short checklist (for example, "shop open two years or more, and …"), the list of 600 selected applicants, and a one-line reason per applicant for appeals. Selection inputs are limited to characteristics that are hard to exaggerate and can be checked, such as shop age confirmed by a licence or a market committee, not self-reported income or assets.

**4. Evidence.** The closest parallel is Athey, Keleher & Spiess (Journal of Econometrics, 2025): in a field experiment with more than 53,000 CUNY students, targeting a financial-aid renewal nudge by estimated effect beat targeting by predicted need. It is a parallel, not a deployment of business grants; the structural match is a limited offer, randomized data, and need-based versus effect-based targeting. Björkegren, Blumenstock & Knight (arXiv 2020; a revised version is reported as accepted at the American Economic Review (unverified — please confirm before citing the journal)) show in Nairobi how people change behavior once a scoring rule is used. No documented NGO deployment of a learned rule for business grants is known to the assistant.

**5. Report card.**
- *Successes:* in the CUNY study, effect-based targeting outperformed need-based targeting on the outcome the program cared about; the rule is short and auditable.
- *Challenges:* with 3,000 pilot applicants, only large, simple differences (such as shop age) can be estimated reliably; staff and funders may resist not funding the poorest; verifying shop age takes field time.
- *Unknowns:* whether this year's applicants resemble the pilot's (Sahoo, Lei & Wager, 2023, treat this problem), and whether reported shop age shifts once the rule is known. Ethically, the rule will turn away some very needy women with new shops. Recommend a need floor: reserve a share of grants for the poorest applicants by verifiable indicators, and offer training alone or a later round to new businesses.

**6. Simpler alternative.** A pivot table of the randomized pilot: split it by shop age band (and then urban or rural), compare average income of offered and not-offered applicants within each group, fund the group with the largest difference, and confirm the choice on a held-back half of the pilot. In the [tutorial](../tutorials/08-policy-learning-business-grants.md#the-simpler-alternative-a-pivot-table-of-the-pilot) a one-question rule from the table captured about 60% of the best rule's gain over a lottery, and a two-question rule matched it (illustrative data). It is close when the effect depends on one or two characteristics. It saves the modeling, not the experiment: without the pilot's lottery, the table compares who applied, not what the grant did. Check before settling for it: groups of a few hundred or more; the characteristics are verifiable; the held-out half confirms the pattern. One causal-forest run with a partner shows whether the pattern really is that simple.

**Next steps.** Split the pilot data and hold back a part for validation; list which app fields can be verified and drop the rest from the rule; agree the need floor with the board and funder before seeing results.

## What the assistant should *not* do

- Recommend a poverty ranking or an integer program over need scores (Class 2) as the main method, or a waitlist model (Class 10) when everyone is known by the closing date.
- Use self-reported income or assets as rule inputs, or present a black-box score staff cannot explain.
- Quote a specific gain from the CUNY study, or present it or any other paper as a deployment of business grants.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

A good answer maps every element of effect-based targeting to this program, citing the interview answer it came from:

| Element | For this program | From |
|---|---|---|
| Program | 600 one-off grants with business training | Filter 1 — The resource and its intent |
| Trial data | Last year's randomized pilot: 3,000 applicants, grant offered by lottery, income measured a year later | Filter 4 — Tolerance for being wrong |
| Outcome | Household income a year after the grant | Filter 1 — The resource and its intent |
| Characteristics | App fields known at application: location, shop age, what it sells, household size | Filter 5 — Field data and workflow friction |
| Rule form | A decision tree of depth two or three, written as a checklist | Filter 5 — Field data and workflow friction |
| Need floor | A reserved share of grants for the poorest applicants, judged by verifiable indicators | Filters 2 and 4 |
| Gaming check | Self-reported income and assets excluded; shop age verified before payment | Filter 3 — Environment dynamics |

It should also flag the gap that matters most: **the rule may only use characteristics recorded before the lottery.** Anything the pilot measured afterwards may itself have been changed by the grant. And it should ask how many of the 3,000 were offered the grant; if few were, the estimates for small groups will be noisy.

### Follow-up 6: One-page brief for a technical partner

If the user picks **6**, a good answer fills the playbook template from the interview:

```
PROJECT BRIEF — Women's shop grants program (illustrative)

The decision we need help with
  Once a year, after the call closes, choose which 600 applicants receive
  a one-off grant with business training.

Why it matters
  The pilot showed big income gains for shops open 2+ years and little
  for very new ones, so funding the poorest by default wastes grants.

Current approach
  Selection by need from self-reported income, which may be exaggerated.

Recommended approach
  Class 7 (Effect-Based Targeting): a causal forest on our pilot, then a
  short rule, because the grant is one-off, all applicants are known
  before deciding, and our randomized pilot shows the effect varies.

Simpler option to beat
  A pivot table of the pilot by shop age and urban/rural, checked on the
  held-back half. Close if one or two characteristics drive the effect.

Data we have
  A randomized pilot of 3,000 applicants: app data plus income a year
  later. This year's applications use the same app.

Constraints
  600 grants. A need floor for the poorest applicants. Rule inputs must be
  hard to exaggerate and checkable. Staff must be able to explain it.

What success looks like
  Higher income a year later per grant, compared with need ranking.
  Harm measure: the share of the poorest applicants still served.

How results must reach staff
  A written checklist rule and a list of 600 names with a one-line reason
  each. Our analyst reruns it in R each year.

What we are asking for
  Help fitting and validating the model on held-out pilot data, and
  designing a comparison in this year's round.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** 3,000 pilot applicants meets the playbook's "few thousand" minimum; confirm the rule's fields exist in this year's app; confirm applicants consented to their pilot data guiding selection; get the board and funder to accept, in writing, not funding some needy applicants unlikely to benefit.
- **3. Pilot design:** within this year's round, randomly assign applicants to selection by the learned rule or by the current need ranking, and compare income a year later per grant; watch the share of the poorest served as the harm measure.
- **4. Build options:** the analyst already uses R, so [grf](https://cran.r-project.org/package=grf) (causal forests) and [policytree](https://cran.r-project.org/package=policytree) (short rules) are the natural fit; EconML is the Python alternative. If help is needed, Statistics Without Borders or a university economics department suits a trial-data problem. Confirm each is still active.
- **5. Reading and contacts:** start with Athey, Keleher & Spiess (free at arXiv 2310.08672), then Athey & Wager (2021) on policy learning. Stefan Wager and Susan Athey (Stanford) and Roshni Sahoo (Columbia Business School) work on these methods.
