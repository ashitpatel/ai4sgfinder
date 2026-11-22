# Expanded scan: AI/ML interventions the earlier scans missed

Status: scan done 2026-11-22. Proposals 1–3 done the same day (taxonomy Section 6, playbook, Cases 24 and 25); proposals 4–7 not started.

## 1. Why the earlier scans missed four sources

Four sources (Adalat AI, and three 2026 Berkeley News stories on an ECG model for sudden cardiac death, Emma Pierson's work on bias, and a database of local laws) surfaced patterns the project hadn't covered: input layers and fairness audits ([plan](input-layers-and-fairness-audit.md)). The earlier scans had five blind spots.

1. **Seeded from one research community.** The twelve classes came from the work of a few AI-for-social-good optimization researchers (Milind Tambe's Teamcore group, Lily Xu, Roshni Sahoo, Ashish Goel's group) and then their co-authors. That follows one citation network, centred on AAAI, AAMAS, EC and KDD. The four sources sit in others: medicine (Nature, a school of public health), algorithmic fairness (PNAS, Science Advances), computational law and NLP (NeurIPS datasets, a public-policy school) and speech technology (Interspeech).
2. **Framed by the answer.** The scans looked for *allocation* methods, so anything that doesn't allocate was out of frame by construction. The landscape page explicitly set aside model providers such as AI4Bharat.
3. **Counted, not mined.** The landscape scan classified about 190 projects from fourteen funders and builders by *kind* of AI (generative, predictive, vision), to show that none offers method-choice guidance. It didn't ask what decision each project feeds. Adalat AI's funders include Fast Forward and The/Nudge, two of the fourteen, so the project was within reach of a scan that only counted.
4. **One kind of source.** Organizations' own project pages and papers. University news offices, which translate papers from every department into plain language, weren't used; three of the four sources came from one.
5. **Geography and sector.** The Indian legal-tech sector, and justice and law generally, weren't sampled. Recency wasn't the cause: the ECG and local-laws stories appeared in June and October 2026, before the class scan at the end of October.

## 2. The expanded scan

Seven parallel sweeps, each with the same brief (what is already covered, what to look for, a fixed table format) and a different source cluster:

| Sweep | Sources |
|---|---|
| A. US universities beyond CS/OR | Berkeley in depth (CEGA, Global Policy Lab, Public Health, Goldman, Computational Precision Health), Stanford (RegLab, King Center, Sustainability & AI Lab), MIT, Harvard, CMU, Chicago (Crime Lab), Columbia, Princeton, UW, Michigan, Cornell, Penn, Duke, Johns Hopkins, Georgia Tech |
| B. Universities and institutes outside the US | UK and Europe (Oxford, Cambridge, LSE, UCL, Imperial, Turing, ETH, EPFL), Canada (Mila, Vector), India (IIT Madras, IISc, IIIT Hyderabad, Wadhwani AI), Africa (Makerere, Cape Town, AIMS, Masakhane, Lacuna Fund grantees), Latin America, South and Southeast Asia |
| C. Research funders, mined for grantees' methods | Gates, Wellcome, Rockefeller, Schmidt Sciences, McGovern, Google.org, OpenAI and Anthropic programmes, Microsoft, Mulago, Skoll, Echoing Green, MIT Solve, IDRC AI4D, Lacuna Fund, Grand Challenges Canada, NSF AI Institutes, Fast Forward and Pragati cohorts |
| D. Frontier labs and companies | Google Research and DeepMind, Microsoft AI for Good Lab, Meta Data for Good, OpenAI, Anthropic, Amazon, IBM, NVIDIA; impact companies such as Karya, Jacaranda Health, Noora Health, Rocket Learning, Precision Development, Dimagi |
| E. Venues and catalogues, as a systematic sample | AAAI AI for Social Impact, IJCAI AI for Social Good, KDD Applied Data Science, NeurIPS Datasets & Benchmarks and workshops, ML4H, CHIL, COMPASS, EAAMO, FAccT, Interspeech/ACL, Nature/PNAS/Science papers; ITU AI for Good, OECD.AI, Climate Change AI |
| F. Operating NGOs, UN agencies and governments | WFP, UNHCR, UNICEF, OCHA, IFRC/510, IRC, BRAC, GiveDirectly, IDinsight, IPA; government systems including failures (SyRI, Robodebt, Allegheny, UK exam grading) |
| G. University news, Jan 2025–Nov 2026 | About 25 university and institute news sites, followed to the paper, with a yield count to judge whether a news-led sweep is worth repeating |

Each item is classed by what the AI does for the program: (a) allocates or decides, (b) an input layer feeding a decision, (c) the intervention itself, (d) measurement or evaluation of impact, (e) science or discovery, (f) governance or audit.

## 3. Findings

The seven sweeps returned about 170 items. Most rows rest on search summaries of the linked primary page, not on full papers, so **nothing below is a verified reference yet**: each item must be checked against its source before it enters the taxonomy. Figures marked *(self-reported)* come from the organization itself.

### What the AI does, across the sample

The venues sweep classified 97 papers by role (IJCAI 2025 AI & Social Good, AAAI-26 AI for Social Impact, and targeted journal searches):

| Role | Count | Share |
|---|---|---|
| (a) Allocates or decides | 14 | 14% |
| (b) Input layer feeding a decision | 42 | 43% |
| (c) The intervention itself | 12 | 12% |
| (d) Measurement or evaluation of impact | 5 | 5% |
| (e) Science or discovery | 10 | 10% |
| (f) Governance or audit | 14 | 14% |

Only about one paper in seven allocates anything, the part ai4sgfinder covers best. Input layers are the largest group, and governance work is as common as allocation. The other sweeps show the same shape. The news sweep screened about 280 stories and found about 38 relevant, about 20 of them not already covered: mostly input layers and audits, not new allocation classes.

### Ten patterns

Each pattern was raised by at least two sweeps. "Sweeps" uses the letters in Section 2.

**1. Screening classifiers that decide who gets referred** (A, B, C, D, E, G). Cheap perception at the point of care or in the field, whose output is a referral for a confirmatory test.
- Wadhwani AI's Cough Against TB, offline on a phone, with India's Central TB Division *(self-reported scale; the page gives two different figures)*.
- EPFL and CHUV's ULTR-AI lung-ultrasound TB triage, in a 3,000-patient study in Benin, Mali and South Africa.
- AI cervical screening in Kenya and Tanzania (Uppsala, Karolinska, Helsinki FIMM): the field study found reagent supply, power cuts and loss to follow-up hurt results as much as the model did.
- Google, Jacaranda Health and Northwestern's blind-sweep ultrasound for gestational age, non-inferior to sonographers in a prospective study (JAMA Network Open, 2026).
- Computer-aided detection thresholds for chest X-ray TB screening in Uganda (Lancet Digital Health, 2025): the threshold, not the model, sets how many people are sent for a test.
- Crop versions: Wadhwani AI's CottonAce pest-trap photos; Makerere's cassava-disease app.

*What's missing:* Section 6 lists speech, documents and published risk models, but not perception classifiers. The method choices are the referral threshold against testing capacity, validation against a reference test in the population served, and what happens after the flag.

**2. Forecasts and early warning as inputs** (A, C, D, E, F, G).
- Disease: Wellcome-funded E-DENGUE (a district forecast two months ahead, to be tested in a cluster randomized trial), IDExtremes and CholOut; InfoDengue in Brazil; the US CDC's FluSight ensemble, scored publicly every season.
- Weather and floods: Google's Flood Hub (Nature 2024, forecasts in ungauged basins); a blend of Google's NeuralGCM and ECMWF's AI model sending monsoon-onset forecasts by SMS to about 38 million farmers in India (UChicago, Berkeley, Precision Development); Michigan's ML correction of the US National Water Model.
- Displacement and food: UNHCR's Project Jetson; WFP's HungerMap LIVE nowcasts.

*What's missing:* Class 4 assumes a forecast exists. There is no guidance on choosing a forecast source, checking its skill where the program works, or on forecasts sent directly to people as an information intervention, whose evaluation (uptake, decisions changed, value per dollar) is the real method question.

**3. Ready-made geospatial layers** (B, D, F, G).
- Google Open Buildings; Meta's Relative Wealth Index (PNAS 2022) and population maps (no longer updated after 2024); UNICEF and ITU's Giga school mapping; Microsoft and 510's damage assessment; Ai2's Skylight vessel detection, used by about 150 organizations; EPFL's PopAI population mapping; ETH's cocoa map, which found official figures undercount planted area by up to 40% in Ghana.

*What's missing:* these feed targeting (Class 2), inspection (Class 12) and patrols (Class 3), each with known failure modes: uncalibrated scores, stale layers, relative rather than absolute measures.

**4. ML as the measurement in an evaluation** (A, B, C, D, G). The model replaces the survey that measures whether a program worked.
- Satellite building footprints to estimate a GiveDirectly cash program's impact (Berkeley, CEGA).
- A negative case: phone-metadata welfare estimates didn't detect a Haiti cash program's effect that surveys did (Journal of Development Economics, 2025).
- Carbon and biomass measurement for agroforestry (Farmers for Forests, Pragati); worksheet grading (Saarthi); camera traps and bioacoustics (SpeciesNet, Perch); calibrated low-cost air sensors (Makerere's AirQo).
- Correcting for classifier error: Cornell's Bayesian correction of zero-shot flood labels from dashcams; the Urban Institute's race imputation to audit home-valuation models without race data.

*What's missing:* the pilot-design follow-up assumes outcomes are measured directly. Measurement error in an ML proxy flows straight into the impact estimate.

**5. LLMs as the intervention, with real evaluations** (A, C, D, E, G). This is now the best-evaluated field category, and the results point both ways.
- Positive: GPT-4 tutoring in Edo State, Nigeria (World Bank randomized trial, about 0.31 standard deviations in six weeks); Stanford's Tutor CoPilot coaching human tutors (randomized, 900 tutors); UW's HAILEY empathy feedback for peer supporters (randomized, Nature Machine Intelligence).
- Null or mixed: an independent randomized trial of Khanmigo found about 0.06–0.08 standard deviations, no better than practice without AI (NBER w35620); Penda Health's AI Consult cut diagnostic errors in an observational study, but a later cluster randomized trial reportedly found no gain in patient outcomes *(paper not located)*.
- Triage with human escalation: Jacaranda Health's PROMPTS answers about 70% of mothers' messages and routes about 30% to nurses *(self-reported)*.

*What's missing:* the assistant treats chatbots as out of scope. But for an NGO the method question is real: copilot for a worker or a replacement, human escalation, and how to test it (A/B test, adaptive experiment, randomized trial, silent trial, grading against expert answers).

**6. Fraud scoring of beneficiaries: the most common government model and the most common failure** (B, F).
- Struck down or suspended: the Netherlands' SyRI (court ruling, 2020); the Dutch childcare-benefit model, which used nationality; Rotterdam's welfare score (bias against women, parents and weaker Dutch speakers); Amsterdam's Smart Check, built to be fair and still biased, scrapped after a pilot; Sweden's parental-benefit flags.
- Unlawful or wrong at scale: Australia's Robodebt (a Royal Commission found it unlawful); Michigan's MiDAS (a state review found 93% of automated fraud findings wrong).
- Contested or deployed: France's CNAF score before the Conseil d'État; the UK DWP's Universal Credit Advances model, with published fairness reports.
- Exclusion by data matching: Telangana's Samagra Vedika record linkage and wrongful ration cancellations; Aadhaar authentication for rations in Jharkhand (a J-PAL trial found leakage fell but exclusion rose).
- The objective, not the model: the IRS audited Black taxpayers 2.9–4.7 times as often, driven by what the selection model was asked to predict (Stanford RegLab and Treasury).

*What's missing:* this is Class 12 pointed at the people the program serves, where a flag is an accusation. The taxonomy has no warning for it.

**7. Allocation patterns outside the twelve classes** (B, E, G).
- *Policy simulation, to choose a rule before rollout:* UNDP's Policy Priority Inference, an agent-based model linking budgets to SDG indicators, used in two countries; agent-based models for homelessness policy (IJCAI 2025); the Gates Institute for Disease Modeling, now with Anthropic, making transmission models usable for deployment decisions.
- *Sequential facility planning:* which health posts to upgrade as budget arrives year by year, with Ethiopia's Ministry of Health (HARP, AAAI-26). Single-shot siting is already Class 2.
- *Designing data collection:* where to send survey enumerators under a travel budget (Mapping on a Budget, AAAI-26).
- *Timing of contact:* learning when to call mothers in India's Kilkari program (a field trial with about 6,500 mothers).
- *Subsidy design:* optimizing food subsidies from shop scanner data (MIT Sloan, J-WAFS, India).
- *Reserve selection and repair sequencing:* conservation connectivity planning and equitable power restoration (IJCAI 2025).

**8. Triage of scarce professional attention** (A, C, D). Early warnings that decide whom a clinician sees next: Johns Hopkins' TREWS sepsis alerts (five hospitals); Duke's Sepsis Watch (no outcome study found); Penn's mortality-prediction nudges for serious-illness conversations (a stepped-wedge randomized trial). The design choices (alert threshold, alert fatigue, capacity to respond) sit between Classes 12 and 10.

**9. Governance as a deployment choice** (A, F, G).
- Advisory or binding: UW found people mirror an AI's hiring bias; Nevada's hard cutoff in a school-funding score cut the at-risk count from 288,000 to 63,000.
- Review before use: OCHA's peer-review framework for predictive models that drive humanitarian funding; the UK DWP's published fairness assessments; public algorithm registers (Amsterdam, Chile's GobLab).
- Privacy: Microsoft and IOM's differentially private trafficking data; Oxford's OpenSAFELY, where analysis runs inside the record holders' systems; Harvard's differential-privacy deployment registry.
- A simple baseline that came close: Chicago's Officer Support System, where ranking officers by past complaints captured much of the model's benefit.

**10. Low-resource language tech as building blocks** (B, C, D). Meta's NLLB-200; India's Bhashini and AI4Bharat's IndicTrans2; Microsoft's Paza speech models for Kenyan languages; Karya's paid speech-data collection; Lacuna Fund datasets; AfriVox benchmarks. The method question is whether an evaluation set exists for the program's language, and whether data is collected ethically.

## 4. Coverage map

| Pattern | ai4sgfinder today | Gap |
|---|---|---|
| 1. Screening classifiers | Class 12 covers ranking under a test budget; Section 6 has no perception-for-screening kind | Threshold vs capacity, reference-test validation, follow-up after the flag |
| 2. Forecasts | Class 4 trigger and cost-loss threshold (Tutorial 14) | Choosing and checking a forecast source; forecasts sent to people |
| 3. Geospatial layers | Aiken et al. phone-and-satellite targeting under Class 2 | A Section 6 kind with known failure modes |
| 4. ML as measurement | None | Pilot design with a proxy outcome; correcting for proxy error |
| 5. LLM interventions | Out of scope; funder review says "doesn't apply" | How to test it; copilot or replacement; escalation |
| 6. Beneficiary fraud scoring | Class 12 has no warning; the fairness audit covers bias only | An explicit avoid-or-safeguard rule; the objective as a source of harm; exclusion by data matching |
| 7. New allocation types | Single-shot siting under Class 2 | Policy simulation; data-collection design; timing; subsidy design |
| 8. Professional triage | Class 12, partly | Alert threshold and fatigue, capacity to respond |
| 9. Governance | Human override and maintenance in readiness checks | Advisory vs binding, peer review, registers, privacy-preserving release |
| 10. Language tech | Speech recognition only (Case 20) | Translation, benchmarks per language, ethical data collection |

## 5. Proposals, in order of value

1. **Extend taxonomy Section 6** with three more kinds of input layer, each with its own checks: *screening classifiers* (pattern 1), *forecasts* (2) and *geospatial layers* (3). Add language technology (10) under perception. This is the largest gap the sweeps agree on, and it fits the structure added in step 1 of the previous plan.
2. **Add a warning for beneficiary risk scoring** (pattern 6): in Class 12's "Avoid when", the readiness checks and the funder review. When the target is the people served, require a legal basis, human review of every flag, an appeal route, and a published accuracy and fairness report. Add that the choice of what a model predicts can cause the disparity (IRS), and that record linkage can exclude people (Telangana, Jharkhand). Candidate funder-review case: a welfare-fraud score, with SyRI, Rotterdam and Amsterdam as evidence.
3. **Cover LLM interventions as an evaluation question** (pattern 5): in the funder review and the scope line, when the AI *is* the intervention, review how it will be tested and escalated, not the model. Evidence: the Edo trial, the Khanmigo trial, Tutor CoPilot, Penda. Candidate case: a funder review of an LLM-tutor proposal.
4. **Add measurement to pilot design** (pattern 4): Follow-up 3 gains a check for ML-proxy outcomes, with the Haiti negative case and error-correction methods (misclassification models, prediction-powered inference).
5. **Assess a thirteenth class for policy simulation** (pattern 7), choosing a rule rather than units, with a warning that validation evidence is weak. Data-collection design, contact timing and subsidy design first need a check of whether they are variants of Classes 2, 8 and 7.
6. **Add governance items to the readiness checks** (patterns 8 and 9): advisory or binding, alert thresholds and capacity, peer review before use, privacy-preserving release.
7. **Repeat the scan quarterly** with the recipe below, and finish what this pass didn't reach.

Every proposal needs its references verified first: most rows above come from search summaries.

## 6. Limits of this scan, and the recipe for the next one

**What wasn't reached.** Four of the seven sweeps ran out of web-search budget: one turn allows about 200 searches across all agents.
- *Venues:* KDD Applied Data Science, NeurIPS Datasets & Benchmarks and workshops (ML4H, CHIL, AfricaNLP, Practical ML for Low Resource Settings, Climate Change AI), COMPASS, EAAMO, FAccT, CHI and CSCW, Interspeech, and every catalogue (OECD.AI, ITU AI for Good, GPAI, UNESCO, the AI Index, AI-for-SDGs databases).
- *Outside the US:* Japan, Korea, Israel, Australia, KNUST, Data Science Africa, AIMS, IIIT Hyderabad, IIT Bombay, Ashoka University, welfare-fraud models in India.
- *Funders:* Microsoft, Amazon, Skoll, Echoing Green, MIT Solve, the Global Innovation Fund, Wellcome Leap, NSF AI Institutes' deployments, IDRC's AI4D and AI4PEP projects, the OpenAI People-First Fund grantee list.
- *Operators:* MSF, Mercy Corps, Save the Children, BRAC, Pratham, Last Mile Health, IPA, UNDP Accelerator Labs.
- *News:* Princeton, Yale, Columbia, UCSF, Broad, Santa Fe Institute, RAND, Toronto, Imperial, ETH, IISc; Stanford Report and Michigan research news blocked automated fetches.

**Recipe for the next scan**
- Run the sweeps over several turns, two or three at a time, so the search budget isn't shared seven ways.
- For news, fetch listing pages directly (MIT News topic pages, washington.edu/news by month, Berkeley CDSS, cam.ac.uk/stories, actu.epfl.ch, allenai.org/blog, urban.org, J-PAL Project AI Evidence, Stanford RegLab and HAI); they gave about three times the yield per call of search. Use EurekAlert or RSS where a site blocks fetches.
- Mine funders' grantee lists for the decision each project feeds, not only the kind of AI.
- Classify every item by role (a)–(f), and keep the counts, so the next scan can see whether the mix is shifting.
- Cadence: quarterly. The news sweep's yield (about 20 new items in 280 stories) is worth repeating, mostly for input layers and governance.

## 7. Proposals 1–3: what was done and tested

Done 2026-11-22.
- **Taxonomy Section 6:** three more kinds of input layer (screening classifier, forecast, geospatial layer), with what to check for each; language technology under perception; two new parts, *When a score targets the people you serve* and *When the AI is the intervention*. Class 12's "avoid when" points to the first.
- **Playbook:** a readiness check for scoring beneficiaries; pilot-design checks for AI as the intervention and for outcomes measured by a model; funder-review rules for both.
- **References:** 15 checked against primary sources before use; 8 verified as given and 6 corrected (the Edo trial's English effect is 0.23 SD, 0.31 being the combined test; Khanmigo's gains were *similar to* non-AI practice; Elzayn et al. has eight authors and appeared in the QJE in 2025; the Jharkhand biometric checks didn't reduce leakage at all; Amsterdam's pilot ended in 2023; the MiDAS 93% figure covers a subset of cases and is listed as unverified). The CAD-threshold paper's main finding is a modest sensitivity gain from stratified thresholds.
- **Cases run** against the rebuilt assistant (Claude Opus 5.5 via `claude -p`):
  - *Case 24, benefit-fraud score:* opened by saying the score flags the people the program serves, ruled out automatic pauses, required every safeguard, cited SyRI, Robodebt, Amsterdam, the tax audits and Jharkhand correctly, and marked the MiDAS figure unverified. Its verdict for the referral step was *Heavier than needed* (36 confirmed cases), which the case now accepts alongside *Mismatch*.
  - *Case 25, AI tutor:* reviewed the test plan, not the model; *Mismatch* on usage measures; a randomized pilot against clubs without the tutor; "double learning gains" marked overstated. One paraphrase said Khanmigo was "no better than" non-AI practice where the reference says "similar to".
  - *Case 20, court transcription:* still *No model needed* for the rollout, and now also flags the usage measure as a test-plan *Mismatch*, because the summaries reach litigants directly. The case now lists that as acceptable.
  - *Case 6, food pantry:* still no model.
