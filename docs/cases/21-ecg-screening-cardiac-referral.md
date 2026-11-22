# Case 21: Choosing whom to refer for a cardiac workup from routine ECGs

| | |
|---|---|
| **Domain** | Cardiovascular health |
| **Intervention type** | Limited specialist workups to find hidden risk |
| **Expected class** | [12 — Risk-Based Inspection (predictive inspection)](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection), with a prediction model the program **uses** rather than builds |
| **Most likely confusion** | Training a new deep-learning model on the program's own few hundred deaths, or treating "highest risk" as "most helped by a defibrillator" |
| **In-depth tutorial** | [Class 12 tutorial](../tutorials/13-risk-based-inspection-lead-pipes.md) (the ranking-and-random-share design is the same) |
| **Real-world pattern** | Obermeyer and colleagues' ECG deep-learning model for sudden cardiac death (Nature, 2026) (see [Evidence](#what-a-good-recommendation-contains)) |

## Scenario

A (fictional) NGO runs a heart-health program with a public hospital network in a middle-income country. The network's clinics record about 90,000 routine 12-lead ECGs a year. Sudden cardiac death kills people who never saw a cardiologist. An implantable defibrillator (ICD) can prevent it, but the network has only two cardiologists for this program, and they can do about 1,200 full workups a year (an echocardiogram, a Holter monitor and a consultation). Today a patient is referred if a clinic doctor reads the ECG as abnormal or notices heart failure.

*This is an illustrative scenario, not a real program.*

## Interview answers

**Filter 1 — The resource and its intent.**
> We're allocating cardiology workups: about 1,200 a year, against about 90,000 ECGs. The workup itself doesn't treat anyone. It tells the cardiologist who might need a defibrillator or medication.
>
> *Next turn (which fits best):* (d), used to look for something hidden: patients whose heart could stop without warning.

**Filter 2 — Choice and preferences.**
> We decide whom to call in. Patients can decline, but they don't compete for slots.

**Filter 3 — Environment dynamics.**
> No one avoids us. A patient's risk changes slowly over years.

**Filter 4 — Tolerance for being wrong.**
> A wasted workup costs a cardiologist's hour and an echo. A missed patient can die suddenly. So misses are the costly error.
>
> *Next turn (records):* We have about five years of ECGs linked to the national death registry, so we know who died and of what, but sudden cardiac deaths number only a few hundred.

**Filter 5 — Field data and workflow friction.**
> ECGs are stored digitally as waveform files, with the reading. A hospital IT officer can run software on a server once a week.

**Narrowing question — Space, movement and risk.**
> Finding hidden problems. We don't know which patients with a normal-looking ECG are at risk.

**Second decision.**
> After the workup, the cardiologist decides who gets a defibrillator, following clinical guidelines. That isn't ours to change.

## Why Class 12: Risk-Based Inspection

- **A resource used to look for something hidden** (Filter 1, option (d)) and **central decisions** (Filter 2) put this in *Space, movement and risk*; **finding hidden problems** picks Class 12.
- The three conditions hold: risk is hidden until a workup, workups are scarce (about 1 in 75 ECGs), and past outcomes exist, including negatives (Filter 4).
- **The prediction model is an input the program uses, not one it builds.** A few hundred deaths are far too few to train a deep network; published models were trained on hundreds of thousands of ECGs. The program's job is to check that an existing model works on its own patients (external validation), set the referral threshold, and keep a random share.
- Not [Class 7 (Effect-Based Targeting)](../../prompt/knowledge/taxonomy.md#class-7-effect-based-targeting) for this decision: the workup is a test, not a treatment, so ranking by the chance of finding risk is right. But the *second* decision, who gets a defibrillator, is about benefit: a patient at high risk of dying of something else gains less. That decision stays with cardiologists and guidelines, so it is not a layer here; the model should still report competing risk to them.
- Not [Class 3](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search): nothing adapts to avoid the program.

## What a good recommendation contains

**1. Class.** Risk-based inspection. Each week, an ECG risk model scores the new ECGs; the cardiologists' slots go to the highest absolute risk, plus a fixed random share (say 10%) of patients just below the threshold. The model is licensed or obtained from its developers, not trained locally, and validated on the network's five years of ECGs linked to the death registry before use.

**2. Counterfactual warning.** Training a new model on a few hundred local deaths will overfit and look accurate only on the data it learned from. Using a published model without local validation risks a different failure: ECG machines, filters and populations differ, so a model can rank well and still mis-state absolute risk, sending slots to the wrong number of people. And a score that predicts *death* is not a score for *benefit from a defibrillator*: patients likely to die of other causes in the year may top the list. Check accuracy and calibration separately for women and men, age groups and regions; models trained in one country can be less accurate elsewhere.

**3. Field pathway.** Weekly, the IT officer runs the scoring software on the server over new ECG files and exports a list in Excel: patients above the risk threshold, plus the random share, each marked. Clinic nurses call patients in. Cardiologists see the risk score, the model's predicted ejection fraction and competing-risk estimate, and decide as now.

**4. Evidence.**
- *Same problem, published model:* Obermeyer and colleagues trained a deep residual network on about 440,000 Swedish ECGs linked to death certificates to predict sudden cardiac death within a year, and validated it without retraining on hospital data from San Diego and Taipei. Its high-risk group had about a 7% annual rate of sudden cardiac death, against 4.6% for patients flagged by the standard ejection-fraction test, and most of the patients it flagged were missed by that test ([Berkeley News, June 2026](https://news.berkeley.edu/2026/06/24/with-ai-researchers-discover-new-way-to-detect-sudden-cardiac-death-risk/); Nature, [doi:10.1038/s41586-026-10674-6](https://doi.org/10.1038/s41586-026-10674-6)). The model also predicts ejection fraction and death from other causes, which is the competing-risk check above.
- *Same design, different domain:* the Flint lead-pipe search (Abernethy et al., 2018) and Eva border testing (Bastani et al., 2021): limited tests, ranking by risk, and a random share.
- *Caution:* Obermeyer et al. (Science 2019): a score that predicts the wrong outcome harms the groups it under-scores.

**5. Report card.**
- *Successes:* the published model kept its accuracy on two health systems it was never trained on.
- *Challenges:* access to the model and its licence; ECG file formats; cardiologists trusting a score they can't read from the trace.
- *Unknowns:* accuracy on this network's machines and population; whether the national registry codes sudden cardiac death reliably; whether there is a defibrillator budget for the extra patients found.

**6. Simpler alternative.** Refer by the clinic doctor's reading plus a published rule from the ECG and record (for example a wide QRS complex, or known heart failure with low ejection fraction), keeping the random share. It is close if the network's past deaths cluster in patients those rules already catch. The published model's main finding is that most of its high-risk patients were *not* flagged by the ejection-fraction rule, so the check before settling for the simple rule is: on the five years of linked records, what share of sudden deaths would the rule have referred?

**Next steps.** Link five years of ECG files to the death registry; ask the model's developers for access and run a validation; agree a threshold that fills about 1,200 slots; confirm the defibrillator budget before finding more patients who need one.

## What the assistant should not do

- Recommend training a deep-learning model from scratch on a few hundred local events.
- Use a published model without validating it, and its calibration, on local data.
- Treat the highest-risk patients as those who benefit most from a defibrillator.
- Recommend a defibrillator-allocation model; that decision belongs to clinicians and guidelines.
- Quote the 7% figure as what this network would achieve.

## After the recommendation

This case shows **Follow-up 2** in full; the others are summarized.

### Follow-up 2: Readiness checks

| Check | Status | What to fix before the pilot |
|---|---|---|
| Outcome records include negatives | Yes: five years of ECGs linked to the registry | Confirm how the registry codes sudden cardiac death |
| Enough events to *train* a model | **No**: a few hundred deaths | Use a published model; validate, don't train |
| Model validated on local data | Not yet | Discrimination and calibration by sex, age and region on the linked records |
| Someone can run it weekly | Yes: IT officer, hospital server | Agree the file export and who fixes failures |
| Action on findings | Partly | Confirm the defibrillator budget and waiting time |
| Random share | Not yet | Agree 10% below the threshold, so the model's misses can be measured |
| Privacy | ECGs are health records | Run on the hospital server; no data leaves the network |

### The other follow-ups, in brief

- **1. Fit the model:** units are new ECGs each week; the budget is about 25 workups a week; the threshold is set on absolute risk, not rank.
- **3. Pilot design:** for six months, alternate clinics between model referral and current practice; compare high-risk findings per workup; harm measure: sudden deaths among patients not referred.
- **4. Build options:** the model's developers and an academic cardiology partner; validation needs a statistician, not a deep-learning team.
- **5. Reading:** the Nature paper above; Abernethy et al. (2018) for the ranking-and-exploration design.
- **6. Brief:** one page asking a cardiology research group to validate the model on the linked records.
