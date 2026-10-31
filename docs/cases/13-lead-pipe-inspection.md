# Case 13: Finding lead service lines with a limited number of digs

| | |
|---|---|
| **Domain** | Environmental health and drinking water |
| **Intervention type** | Inspections to find a hidden hazard |
| **Expected class** | [12 — Risk-Based Inspection (predictive inspection)](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection) |
| **Most likely confusion** | Re-digging the streets where lead was found before |

## Scenario

A children's environmental-health NGO in the (fictional) city of Millbrook works with the municipal water utility to find lead service lines, the pipes that connect each home to the water main. About 20,000 older homes might have one, and nobody knows which: the utility's records are incomplete, and the only sure way to check is to dig. The utility's crews can dig and check 300 service lines this year. Every lead pipe that goes unfound is a home where children keep drinking contaminated water.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We're allocating digs: the utility can excavate and check 300 service lines this year, out of about 20,000 older homes. The aim is to find as many lead pipes as possible so they can be replaced.
>
> *Next turn (which fits best):* (d), used to look for something hidden. A dig doesn't help the household by itself; it tells us whether there's a lead pipe under the ground.

**Filter 2 — Choice and preferences.**
> We decide, with the utility, where crews dig. Homeowners are notified and agree to access, but they don't choose or compete for a dig.

**Filter 3 — Environment dynamics.**
> Nobody avoids us. Pipes don't move, and no one is hiding them. The only thing that changes is what we know.

**Filter 4 — Tolerance for being wrong.**
> A wasted dig costs money and a crew-day, which we can absorb. A *missed* pipe is worse: children in that home keep drinking lead-contaminated water, and lead harm to children doesn't reverse. So mistakes matter for lives, but one wrong dig isn't a catastrophe on its own.
>
> *Next turn (records):* We have results from about 1,500 past digs, both the ones that found lead and the ones that didn't. Most were chosen because a resident complained or a street was being repaved anyway, not at random.

**Filter 5 — Field data and workflow friction.**
> Crews log each dig's result in an Excel sheet: address, date, pipe material on each side of the meter. The utility also has property records with the year each house was built.
>
> *Next turn (who would run it):* One analyst at the utility. She could rerun a model once a month, but not every day.

**Narrowing question — Space, movement and risk.**
*"What is the hardest part: outwitting people who avoid you, preparing for a rare disaster, moving goods to many places, or finding hidden problems?"*
> Finding hidden problems. We know roughly where lead pipes could be; we don't know which homes actually have them.

## Why Class 12: Risk-Based Inspection

The assistant should select **[Class 12 (Risk-Based Inspection)](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection)**, solved with a predictive risk model that ranks homes for digging, updated as results come in.

- **A resource used to look for something hidden** (Filter 1 — The resource and its intent, option (d)) places the problem in the *Space, movement and risk* family, and **central decisions** (Filter 2 — Choice and preferences) keep it there.
- The narrowing answer, **finding hidden problems**, picks Class 12 (Risk-Based Inspection) within the family. The class's three conditions all hold: the problem is hidden until someone digs, digs are limited (300 of 20,000), and 1,500 past results exist, including negatives (Filter 4 — Tolerance for being wrong; Filter 5 — Field data and workflow friction).
- Not [Class 3 (Spatiotemporal Security & Adaptive Search)](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search): nothing evades the crews (Filter 3 — Environment dynamics), so a randomized game against an adversary would add complexity with no benefit.
- Not [Class 2 (Static Demographic Targeting)](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting): a dig is not a benefit handed to a household; the pipes are *findings*, and the value of each dig depends on how likely it is to find lead.
- Not [Class 8 (Learn-While-Allocating)](../../prompt/knowledge/taxonomy.md#class-8-learn-while-allocating) as the primary class: there are no competing program options to compare. But a learning element sits *inside* Class 12: each month's digs update the model, and a random share keeps it learning about places it would otherwise skip.

## What a good recommendation contains

**1. Class.** Risk-based inspection: a supervised model (for example a gradient-boosted classifier or logistic regression) trained on the 1,500 past digs predicts each home's chance of a lead line from house age, utility and permit records, and neighbourhood. Crews dig the highest-risk homes, each month's results retrain the model, and a fixed random share of digs (say 10–20%) goes to homes the model would not pick. This is the design behind the Flint lead-pipe search (Abernethy et al.).

**2. Counterfactual warning.** A model trained naively on the 1,500 past digs learns where the utility *chose* to dig (complaints, repaving), not where lead is. It will send crews back to the same streets, "confirm" them, and never learn about neighbourhoods that were never checked, which are often the ones with the fewest complaints, not the least lead. Re-digging the streets where lead was found before has the same flaw. Without an equity check, the model can quietly concentrate digs in already over-inspected areas. Also check what the score actually predicts (Obermeyer et al.): a score trained on "was dug" or "complained" is not a score for "has lead."

**3. Field pathway.** Once a month, the analyst appends the crews' Excel results, reruns the model, and exports a ranked dig list: about 25 addresses for the month, marked "risk-ranked" or "random check." Crews see only the address list and keep logging results in the same Excel sheet. Every home where lead is found goes onto a replacement list with a date; high-risk homes not yet dug, and homes with confirmed lead awaiting replacement, are offered interim protection (certified filters and flushing guidance) right away.

**4. Evidence.**
- *Deployment, same problem:* Abernethy et al. (KDD 2018), *ActiveRemediation*, is the documented search for lead pipes in Flint, Michigan, using predictive modelling to guide where to dig. Cite the paper for its reported results; do not quote figures from memory.
- *Deployment, closely related:* Potash et al. (KDD 2015) worked with the Chicago Department of Public Health on predictive modelling to prevent childhood lead poisoning by targeting lead-hazard inspections.
- *Parallel, different domain:* Eva (Bastani et al., Nature 2021) chose which travelers to test at Greek borders in 2020, mixing risk targeting with exploration, and found about 1.85 times as many asymptomatic infections as random testing. The parallel is the design (limited tests, learning as results arrive), not the size of the gain for lead pipes.
- *Parallel, risk ranking with a public agency:* Carton et al. (KDD 2016) built an early-warning model with the Charlotte-Mecklenburg Police Department.
- *Caution:* Obermeyer et al. (Science 2019) showed a risk score that predicted health costs rather than illness under-referred Black patients.

**5. Report card.**
- *Successes:* the Flint and Chicago projects were built with public agencies on their own records (see the papers for reported results); Eva shows the explore-and-target design outperforming random choice at scale.
- *Challenges:* incomplete, inconsistent records; crews and residents asking why one street is dug and the next isn't; finding pipes faster than the utility can replace them.
- *Unknowns:* how badly the selective past digs bias the starting model; whether records are worse in poorer neighbourhoods, so the model under-scores them; whether the replacement budget keeps pace with findings.

**Next steps.** Clean the 1,500 past dig records and flag how each was chosen; join them to house age and neighbourhood; agree with the utility the random share, the equity check, and the replacement and filter plan *before* the first ranked list goes out.

## What the assistant should *not* do

- Recommend a security game (Class 3); no one is evading the crews.
- Treat the digs as a benefit to distribute fairly (Class 2), or as an experiment between program options (Class 8).
- Train only on past digs without a random share or a correction for how those digs were chosen.
- Quote Flint or Chicago results not given in the verified references, or present Eva's 1.85x as what a lead-pipe model would achieve.
- Recommend finding pipes without a plan to replace them and protect children in the meantime.

## After the recommendation

The assistant then offers the six follow-ups from the [implementation playbook](../../prompt/knowledge/playbook.md), tailored to these answers. This case shows **Follow-up 1** and **Follow-up 6** in full; the others are summarized at the end.

### Follow-up 1: Fit the model to your program

A good answer maps every element of risk-based inspection to this program, citing the interview answer it came from:

| Element | For this program | From |
|---|---|---|
| Units | The ~20,000 older homes that could have a lead service line | Filter 1 — The resource and its intent |
| Hidden problem | A lead service line (either side of the meter) | Filter 3 — Environment dynamics |
| Inspection budget | 300 digs this year, about 25 a month | Filter 1 — The resource and its intent |
| Risk features | Year built, utility and permit records, neighbourhood | Filter 5 — Field data and workflow friction |
| Past inspections | ~1,500 past digs with results, lead and not lead; most chosen by complaints or repaving | Filter 4 — Tolerance for being wrong |
| Exploration share | 10–20% of each month's digs drawn at random from homes the model would not pick | Filter 4 — Tolerance for being wrong |
| Action on findings | Replacement list with dates; filters for confirmed and high-risk homes in the meantime; who pays agreed with the utility | Filter 1 — The resource and its intent |

It should also flag the gap that matters most: **how each past dig was chosen.** If the Excel sheet doesn't record whether a dig came from a complaint, repaving or anything else, add that column now and backfill what you can; the analyst needs it to correct for the bias in the starting data.

### Follow-up 6: One-page brief for a technical partner

If the user picks **6**, a good answer fills the playbook template from the interview:

```
PROJECT BRIEF — Millbrook lead service line search (illustrative)

The decision we need help with
  Each month, choose which ~25 of about 20,000 older homes the water
  utility's crews dig up to check for a lead service line (300 this year).

Why it matters
  Every lead pipe left unfound is a home where children keep drinking
  lead-contaminated water. Lead harm to children does not reverse.

Current approach
  Digs follow resident complaints and street repaving, so they cluster
  in some neighbourhoods and leave others never checked.

Recommended approach
  Class 12 (Risk-Based Inspection): a risk model ranks homes by the
  chance of a lead line, with a random share of digs to correct for
  past selective digging, retrained monthly, because the pipes are
  hidden, digs are limited and past results exist.

Data we have
  ~1,500 past dig results (lead and not) in Excel; property records with
  year built. Gap: how each past dig was chosen is not recorded.

Constraints
  300 digs this year; one analyst, monthly reruns; an equity check so
  digs don't concentrate in already over-inspected neighbourhoods.

What success looks like
  Lead lines found per dig, compared with current practice. Harm
  measure: neighbourhoods with high predicted risk but no digs.

How results must reach staff
  A monthly ranked address list in Excel, marked risk-ranked or random.
  Crews log results in the same sheet.

What we are asking for
  Help building the first model and a 3-month pilot, plus a handover
  so our analyst can rerun it monthly.

Contact
  [Name, role, email]
```

### The other follow-ups, in brief

- **2. Readiness checks:** the 1,500 records include negatives, which this class needs, but were selectively chosen; agree the replacement plan and filter distribution before the pilot; check the score doesn't send crews back to over-inspected neighbourhoods; homeowners' addresses are personal data, so store them securely.
- **3. Pilot design:** split the next 3 months of digs between the model's list and current practice; compare lead lines found per dig; track high-risk neighbourhoods with no digs as the harm measure.
- **4. Build options:** [scikit-learn](https://scikit-learn.org) for the risk model and a spreadsheet for the ranked list, both mature and free; a data scientist builds it, the analyst reruns it. DataKind, Statistics Without Borders or the Data Science for Social Good Fellowship are realistic partners. Confirm any tool or partner is still active before relying on it.
- **5. Reading and contacts:** start with Abernethy et al. (2018), free at [arXiv 1806.10692](https://arxiv.org/abs/1806.10692); then Potash et al. (2015) and Bastani et al. (2021). Jacob Abernethy (Georgia Tech) worked on the Flint search; Rayid Ghani (Carnegie Mellon) on public-health early-warning models.
