# Case 6: A neighborhood food pantry that doesn't need a model

| | |
|---|---|
| **Domain** | Food security |
| **Intervention type** | Recurring in-kind distribution |
| **Expected class** | None — "You don't need an optimization model" |
| **Most likely confusion** | [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) or [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting), because the setting sounds like an allocation problem |
| **In-depth tutorial** | [How the method works, step by step](../tutorials/06-no-model-food-pantry.md) |

## Scenario

A volunteer-run food pantry serves about 150 registered households. It hands out weekly grocery boxes. A local foundation has offered to fund "an AI tool to allocate food more fairly."

*This is an illustrative scenario, not a real program. It tests whether the assistant will recommend less technology when that is the right answer.*

## Interview answers

**Filter 1 — The resource and its intent.**
> Weekly grocery boxes. We want every registered household to have enough food. A box is used up, and we have a fresh supply every week. Giving the box meets the need directly. So (b): given again and again, every week.

**Filter 2 — Choice and preferences.**
> We hand out the boxes; nobody ranks or votes. Households pick up when they can. We'd like them to be able to choose some items, like halal or vegetarian.

**Filter 3 — Environment dynamics.**
> No. Nobody avoids us or games anything. Demand rises a bit at the end of the month.

**Filter 4 — Tolerance for being wrong.**
> Nobody goes hungry on our watch: in 49 of the last 52 weeks, we had enough boxes for everyone who came. The other 3 weeks we ran short by about 10–20 boxes. Our only records are the paper sign-in sheets; we've never run a pilot or trial.

**Filter 5 — Field data and workflow friction.**
> Volunteers tick names on a paper sign-in sheet. There's one laptop. Volunteers change every few months. Whoever is shift lead that day would have to run anything we use.

**Narrowing question — Repeated decisions that learn.** *"Which describes your uncertainty better: how each person's situation changes from week to week, or which of several program options works best?"*
> Neither, really. Every registered household that comes gets a box, so we aren't choosing who gets one, and there's only one kind of box.

**Second decision.** *"Is there a second decision in this program: when to act, where to look first, how it reaches people, or which version works for whom?"*
> No. There's nothing else to decide; the boxes go out on the same days to whoever comes.

## Why no model

The assistant should select **none of the twelve classes** and recommend simple rules instead.

- **Given again and again** (Filter 1 — The resource and its intent) with **central hand-out** (Filter 2 — Choice and preferences) places the problem in the *Repeated decisions that learn* family. But the narrowing answer leaves nothing to decide: everyone who comes is served, so there is no weekly choice of who gets help for [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution), and no set of options to compare for [Class 8: Learn-While-Allocating](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating).
- Supply **meets demand in 94% of weeks** (Filter 4 — Tolerance for being wrong). An optimizer has almost nothing to optimize; the rare shortfall is a supply problem, not an allocation problem.
- **Low data and high volunteer turnover** (Filter 5 — Field data and workflow friction) mean any tool must survive with no one who understands it.
- The preference question (Filter 2 — Choice and preferences) is about *item choice inside a box*, which a pantry "choice" shelf handles without an algorithm. It is not two sides ranking each other, so it doesn't make this a *People choose* problem.
- Not [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists) either. Households do arrive one at a time, but with enough boxes for everyone in almost every week, there is no capacity to ration across the season.

## What a good recommendation contains

A good answer still uses the six headings, but each is short and honest:

**1. Class.** No optimization model. Use two simple rules: (a) a predictable end-of-month top-up order from the supplier, and (b) a written shortfall rule (for example, households with children under 5 or with no other support are served first; everyone else gets a smaller box).

**2. Counterfactual warning.** The risk here runs the other way: an "AI allocation" tool adds cost, a dependency on one technical volunteer, and a scoring system that households may experience as surveillance or means-testing, all to solve a problem that occurs 3 weeks a year.

**3. Field pathway.** A laminated card at the sign-in table with the shortfall rule, and a monthly tally of boxes given vs. households served on the paper sheet.

**4. Evidence.** At the network level, food *allocation* does merit mechanism design: Feeding America's Choice System, which lets food banks bid for donated loads with an internal currency, improved allocation across food banks (Prendergast, JPE 2022). It is an example of [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists): loads are placed as they arrive. That is a different scale; if the pantry later joins a regional network, that is where such tools belong.

**5. Report card.** Successes: simple rules are transparent and survive volunteer turnover. Challenges: the end-of-month spike needs a standing supplier arrangement. Unknowns: whether unregistered households are being turned away, which the sign-in sheet doesn't capture.

**6. Simpler alternative.** Here the simple rule *is* the recommendation, so this heading says what would make it stop being close enough: shortfalls in more than a few weeks a year, recorded turn-aways, or the pantry starting to share supply with other sites. Until one of those appears, the written rule and the supplier buffer capture almost all the value a model could add.

**Next steps.** Spend the foundation's offer on storage capacity or a supplier buffer for end-of-month weeks, and record turn-aways for 3 months to check whether hidden demand exists.

## What the assistant should *not* do

- Recommend a restless bandit or ILP because the foundation asked for "AI."
- Refuse to engage: it should still explain where optimization *would* help (the regional network).

## After the recommendation

When the answer is "no model," the follow-ups still apply, scaled down. The assistant should offer them, and a good answer keeps each one short.

- **1. Fit the model → write down the rule.** The shortfall rule on one card: in a short week, households with children under 5 or no other support get a full box first, and everyone else gets a smaller box. The shift lead applies it.
- **2. Readiness checks:** the sign-in sheet holds names, so keep it stored securely and don't add scoring or ranking of households; volunteers change every few months (Filter 5 — Field data and workflow friction), so the rule must fit on the card.
- **3. Pilot design:** use the rule for 3 months, then ask volunteers and a few households whether it felt fair.
- **4. Build options:** nothing to build. A tally sheet on the existing laptop is enough.
- **5. Reading and contacts:** if the pantry joins a regional network, read Prendergast (2022) on Feeding America's Choice System; the regional food bank is the contact.

### What would change the answer

A good answer also says when to revisit, so the "no" isn't permanent. Track two numbers monthly: weeks the pantry ran short, and households turned away (start recording these now). Reconsider if:
- the pantry runs short in more than one week a month for three months running, or
- recorded turn-aways show hidden demand, or
- the pantry starts sharing supply with other pantries, where allocation across sites becomes a real problem (see [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) if a coordinator divides supply by need, or [Class 10: Online Assignment & Waitlists](../../prompt/knowledge/taxonomy.md#class-10-online-assignment--waitlists) if donated loads arrive over time and pantries bid for them, as in the Choice System).

### Instead of a technical brief: a note to the foundation

```
Thank you for offering to fund an AI allocation tool. We looked at this
carefully: in 49 of the last 52 weeks we had enough food for everyone who
came, so an allocation model would have little to improve. The 3 short
weeks were a supply problem at the end of the month.

We'd like to propose using the funds for extra storage and a standing
end-of-month supplier order instead, and to start recording households we
turn away so we can check for unmet demand. We'll report both numbers to
you quarterly.
```
