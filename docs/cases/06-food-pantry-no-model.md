# Case 6: A neighborhood food pantry that doesn't need a model

| | |
|---|---|
| **Domain** | Food security |
| **Intervention type** | Recurring in-kind distribution |
| **Expected class** | None — "You don't need an optimization model" |
| **Most likely confusion** | Class 1 (Dynamic State Evolution) or Class 2 (Static Demographic Targeting), because the setting sounds like an allocation problem |

## Scenario

A volunteer-run food pantry serves about 150 registered households. It hands out weekly grocery boxes. A local foundation has offered to fund "an AI tool to allocate food more fairly."

*This is an illustrative scenario, not a real program. It tests whether the assistant will recommend less technology when that is the right answer.*

## Interview answers

**Filter 1 — Resource and intent.**
> Weekly grocery boxes. We want every registered household to have enough food. A box is used up, and we have a fresh supply every week. Giving the box meets the need directly.

**Filter 2 — Choice and preferences.**
> Households pick up when they can. We'd like them to be able to choose some items, like halal or vegetarian.

**Filter 3 — Environment dynamics.**
> Cooperative. Demand rises a bit at the end of the month.

**Filter 4 — Tolerance for being wrong.**
> Nobody goes hungry on our watch: in 49 of the last 52 weeks, we had enough boxes for everyone who came. The other 3 weeks we ran short by about 10–20 boxes.

**Filter 5 — Field data and workflow.**
> Volunteers tick names on a paper sign-in sheet. There's one laptop. Volunteers change every few months.

## Why no model

The assistant should select **none of the five classes** and recommend simple rules instead.

- Supply **meets demand in 94% of weeks** (Filter 4). An optimizer has almost nothing to optimize; the rare shortfall is a supply problem, not an allocation problem.
- **Low data and high volunteer turnover** (Filter 5) mean any tool must survive with no one who understands it.
- The preference question (Filter 2) is about *item choice inside a box*, which a pantry "choice" shelf handles without an algorithm.

## What a good recommendation contains

A good answer still uses the five headings, but each is short and honest:

**1. Class.** No optimization model. Use two simple rules: (a) a predictable end-of-month top-up order from the supplier, and (b) a written shortfall rule (for example, households with children under 5 or with no other support are served first; everyone else gets a smaller box).

**2. Counterfactual warning.** The risk here runs the other way: an "AI allocation" tool adds cost, a dependency on one technical volunteer, and a scoring system that households may experience as surveillance or means-testing, all to solve a problem that occurs 3 weeks a year.

**3. Field pathway.** A laminated card at the sign-in table with the shortfall rule, and a monthly tally of boxes given vs. households served on the paper sheet.

**4. Evidence.** At the network level, food *allocation* does merit mechanism design: Feeding America's Choice System, which lets food banks bid for donated loads with an internal currency, improved allocation across food banks (Prendergast, JPE 2022). That is a different scale; if the pantry later joins a regional network, that is where such tools belong.

**5. Report card.** Successes: simple rules are transparent and survive volunteer turnover. Challenges: the end-of-month spike needs a standing supplier arrangement. Unknowns: whether unregistered households are being turned away, which the sign-in sheet doesn't capture.

**Next steps.** Spend the foundation's offer on storage capacity or a supplier buffer for end-of-month weeks, and record turn-aways for 3 months to check whether hidden demand exists.

## What the assistant should *not* do

- Recommend a restless bandit or ILP because the foundation asked for "AI."
- Refuse to engage: it should still explain where optimization *would* help (the regional network).
