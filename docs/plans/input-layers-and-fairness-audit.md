# Plan: cover input layers and fairness audits

Status: steps 1–4 done 2026-11-22. The version bump is left for a release commit.

This plan comes from a review of four real projects against ai4sgfinder: [Adalat AI](https://adalat.ai), and three UC Berkeley projects reported by Berkeley News in 2026 ([sudden cardiac death from ECGs](https://news.berkeley.edu/2026/06/24/with-ai-researchers-discover-new-way-to-detect-sudden-cardiac-death-risk/), [Emma Pierson's work on bias](https://news.berkeley.edu/2026/01/20/ai-has-a-bias-problem-can-we-build-something-smarter/), [a database of local laws](https://news.berkeley.edu/2026/10/02/to-decipher-local-laws-researchers-used-ai-to-build-a-database-of-millions-of-them/)). Cases [20](../cases/20-funder-review-court-transcription.md)–[23](../cases/23-local-ordinance-advocacy-targeting.md) are built on their problem patterns.

## 1. What each project uses

**Confirmed** means a primary source states it (paper, model card, dataset card, the organization's own write-up). **Guessed** means inferred from similar public work. Nature, PNAS and Science Advances pages were not readable directly; the ECG details come from the paper's published peer-review file and press releases.

| Project | Techniques | Confirmed | Guessed |
|---|---|---|---|
| **Adalat AI** (courtroom transcription, India) | Speech recognition: Whisper Small/Medium fully fine-tuned on Indian-language speech (IndicVoices, Kathbath, Shrutilipi, FLEURS and others) with a hard-to-easy curriculum; its own Conformer encoder + TDT decoder with a CTC head (~120M parameters, NVIDIA NeMo), the Hindi one starting from AI4Bharat's checkpoint, released for offline use with ONNX exports; Silero voice-activity detection into 3–30 s segments and parallel faster-whisper on one T4 GPU. Evaluation: Vividh-ASR benchmark by acoustic difficulty; SCRIBE metric splitting errors into words, punctuation, numerals and legal entities. LLMs: Claude models summarise and translate court orders on a WhatsApp helpline. Legal speech data with Karya. | [arXiv 2507.01021](https://arxiv.org/abs/2507.01021), [Vividh blog](https://huggingface.co/blog/adalat-ai/vividh-benchmark), [model card](https://huggingface.co/adalat-ai/koyal-hi-120m-1.0), [arXiv 2605.20712](https://arxiv.org/abs/2605.20712), [customer story](https://claude.com/fr/customers/adalat-ai) | Legal vocabulary handled by biased decoding or glossaries; on-premises GPU servers per court complex. Productivity trials are claimed in pitch material but unpublished. Courtroom counts vary by source (2,500 in 8 states; 4,000+ in 9). |
| **ECG and sudden cardiac death** (Obermeyer et al., Nature 2026) | Supervised deep learning on waveforms: a 64-layer ResNet trained on 441,614 Swedish ECGs; label = sudden cardiac death within one year, from death certificates (binary, scored by AUC, not a survival model). Ensemble with predicted ejection fraction and competing-risk mortality (multi-task). External validation without retraining: US (AUC 0.79) and Taiwan (0.77). Fixed absolute-risk threshold carried over from Sweden. Explanation with a generative model showing which waveform features drive risk (a new feature in lead aVL). High-risk group: 7.0% annual sudden-death rate against 4.6% for low ejection fraction; most flagged patients were not flagged by ejection fraction. | [Peer-review file](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10674-6/MediaObjects/41586_2026_10674_MOESM3_ESM.pdf), [EurekAlert](https://www.eurekalert.org/news-releases/1133419), [doi:10.1038/s41586-026-10674-6](https://doi.org/10.1038/s41586-026-10674-6) | Input is raw 12-lead, 10 s at 500 Hz, as in other ECG ResNets (Ribeiro et al. 2020; Mayo AI-ECG). The generative explainer is probably a conditional VAE or GAN. |
| **Emma Pierson's fairness work** | (a) Within-person comparison: linear probability model with driver fixed effects on stops where the same driver was perceived as Hispanic vs white (Stanford Open Policing data, AZ/CO/TX; 54,170 drivers), clustered errors, conditional-logit robustness checks. (b) Race in risk models: logistic regression with and without race and a race × family-history interaction; calibration, AUC with DeLong's test, share of each group in top-risk slots, bootstrap intervals; dropping race under-predicts risk for Black participants because family history is recorded less reliably for them. (c) Under-reporting: PURPLE, a positive-unlabeled estimator of relative prevalence. (d) Threshold tests for discrimination (hierarchical Bayesian; Pierson's fast version). | [arXiv 2409.11269](https://arxiv.org/abs/2409.11269), [PNAS 2024 (PMC11348319)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11348319/), [arXiv 2110.04133](https://arxiv.org/abs/2110.04133), [arXiv 1702.08536](https://arxiv.org/abs/1702.08536) | That Science Advances doi:10.1126/sciadv.adx5829 is the published version of arXiv 2409.11269 (likely, not confirmed). |
| **Local Law Observatory / LOCUS-v1** (Davenport et al., NeurIPS 2026) | Crawling with browser automation and per-publisher download logic (9,239 code PDFs, ~7M pages). Vision-language OCR (LightOnOCR-2-1B, Qwen3-based) at about $0.30 per 1,000 pages, with header/footer removal and cross-page merging. Segmentation by section headers. LLM labelling (GPT-5.4-nano on 100k sections, GPT-5.4 re-checking the hardest 5.5%) for substantivity, function and topic. Distillation into ModernBERT classifiers. Normative scores (opacity, enforcement discretion, paternalism) from 200k pairwise LLM comparisons aggregated with TrueSkill, then regressed with ModernBERT. Released with a 250-row human-audit subset; the dataset card shows majority votes across several model annotators. | [arXiv 2606.19334](https://arxiv.org/abs/2606.19334), [LOCUS-v1](https://huggingface.co/datasets/LocalLaws/LOCUS-v1) | Near-duplicate removal (e.g. MinHash), since many towns adopt the same model codes. No agreement figures against the human audit were found. |

## 2. What ai4sgfinder covers today

ai4sgfinder is scoped to **allocation**: who gets a limited resource, where to look, when to act. Its prompt says to stay in scope and redirect other requests. Against that scope:

| Technique family | Covered? | Where |
|---|---|---|
| Supervised risk prediction for a limited test or inspection | **Yes**, as the core of Class 12 | [Taxonomy, Class 12](../../prompt/knowledge/taxonomy.md#class-12-risk-based-inspection); Case 13 |
| Prediction model feeding an allocation | **Partly**: "10 + prediction" and "12 + 3" combinations | [Taxonomy, Section 5](../../prompt/knowledge/taxonomy.md#5-when-two-classes-combine) |
| Using a model someone else built: external validation, recalibration, absolute-risk thresholds, too few local events to train | **No** | — |
| Risk ≠ benefit, competing risks | **Partly**: Class 7 and Case 17 cover risk vs effect; competing risk is not mentioned | Taxonomy Class 7 |
| Fairness checks on a risk score | **Thin**: one bullet ("check what it predicts and whether it is equally accurate across groups") and Obermeyer et al. 2019 | [Playbook, ethics](../../prompt/knowledge/playbook.md) |
| Race-aware vs race-blind models; calibration by group; label bias from who gets tested; positive-unlabeled correction; within-person and threshold tests | **No** | — |
| Speech recognition, OCR, LLM labelling and summarising, distillation | **No, by design**: outside allocation. The funder review says "if nothing is allocated, the review doesn't apply"; the landscape lists AI4Bharat as a model provider not compared | [Playbook, funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal); [landscape](../landscape.md) |
| Checking an extraction or perception layer before an allocation uses it (measured error on own data, by group or language, hand-checked sample) | **No** | — |

So the gap is not a missing allocation class. Three of the four projects build **inputs** to decisions (a transcript, a risk score, a table of laws), and the fourth is about **auditing** a risk score. The assistant already meets these when it reviews a proposal, but has no guidance for them.

## 3. Recommendation

Don't add new classes, and don't widen the assistant into choosing speech or vision models: that is a different tool, and AI4Bharat, Hugging Face model cards and the providers already serve it. Instead, add two things that keep the allocation focus:

1. **Input layers**: how to recognise a perception, extraction or prediction component inside a program, what to check before an allocation relies on it, and when to use a published model instead of building one.
2. **A fairness audit for risk scores**: a short, concrete checklist that the readiness checks and funder review point to.

## 4. Steps

Each step names its files and what done looks like. Steps 1–3 are independent; step 4 depends on all three.

### Step 1. Taxonomy: a section on input layers (done)

- **File:** `prompt/knowledge/taxonomy.md`, new **Section 6: Input layers** after Section 5.
- **Content:**
  - Three kinds, each with one line on what it produces and the real example: *perception* (speech to text, images to labels: Adalat AI), *extraction* (documents to a table: LOCUS-v1), *prediction* (records to a risk score: the ECG model).
  - The rule: an input layer allocates nothing; name the decision it feeds, classify that, and pilot the input layer first (as Section 5 already says for combinations).
  - **Build, adapt or use:** train only with enough local outcomes; otherwise use a published model and validate it locally (discrimination, calibration, by group), or fine-tune an open one (Adalat's Whisper fine-tunes).
  - **What to measure:** error rate on the program's own data, never the benchmark (word error rate by language for speech; label accuracy on a hand-checked random sample for extraction; calibration by group for prediction); cost per unit; who corrects errors.
- **Verified references:** add, after checking each resolves: Obermeyer et al. 2026 (Nature); Zink, Obermeyer, Pierson 2024 (PNAS); Davenport et al. 2026 (arXiv 2606.19334, NeurIPS); Adalat AI, arXiv 2507.01021; Shanmugam and Pierson (arXiv 2110.04133). Put Gera and Pierson (Science Advances 2025) under unverified until the DOI is confirmed. Put Adalat's productivity claims and courtroom counts under unverified.
- **Done:** Section 6 exists; the system prompt's list of taxonomy sections names it ("tools that feed a decision"); five references are verified, and three claims (Adalat's productivity results and scale, the Science Advances version of Gera and Pierson, LOCUS at NeurIPS) are listed as unverified.

### Step 2. Playbook: a fairness audit for risk scores (done)

- **File:** `prompt/knowledge/playbook.md`. Expand the "Bias in risk scores" bullet into a short subsection, linked from Follow-up 2 (readiness checks) and the funder review's "Risks to people" heading.
- **Checklist:**
  1. *What does the label measure?* Cost vs illness (Obermeyer 2019); "diagnosed" vs "has the condition", when some groups are tested less (positive-unlabeled correction).
  2. *Calibration by group:* predicted against observed rates for each group, not only overall accuracy.
  3. *With and without group variables:* removing race or sex doesn't make a model fair; compare both, and interactions where a predictor is recorded unevenly (Zink et al. 2024).
  4. *Share of slots by group* under the score and under the simpler rule.
  5. *A random share* so the model's misses can be measured.
  6. *For discrimination claims* in enforcement data: outcome or threshold tests, and within-person comparisons where the same person is seen differently (Gera and Pierson).
- **Tools:** [scikit-learn calibration curves](https://scikit-learn.org/stable/modules/calibration.html) and [Fairlearn](https://fairlearn.org) for metrics by group. Confirm both are maintained before listing.
- **Done:** the subsection "Fairness audit for a risk score" sits at the end of Follow-up 2, linked from the "Bias in risk scores" check and the funder memo's "Risks to people" heading; Fairlearn is listed for Class 12; Gera & Pierson (2024, arXiv) moved to the verified references. Case 22's memo matches it and links to it; Case 13 is unchanged.

### Step 3. Playbook and prompt: input layers in the readiness checks and funder review (done)

- **Files:** `prompt/knowledge/playbook.md`. The system prompt already names taxonomy Section 6 (step 1); the kickoff has no scope or funder-review text and is at 3,989 of 4,000 characters, so it is unchanged.
- **Changes made:**
  - Funder review: a rule for proposals that are input layers: don't classify, judge or swap the model; review any decision it feeds; and always ask three questions (error on the program's own data by language or group; who corrects errors and how long that takes; what decision its output feeds and who makes it).
  - Memo template, evidence check: "accuracy measured on a published benchmark presented as accuracy on the program's own data" is now an example of an overstated claim.
  - Follow-up 2: an "Input layers" check under "For every class" (done in step 2).
  - Follow-up 4: an "Input layers" paragraph after the software table. It names no models, points to Hugging Face model cards, providers' evaluation reports and AI4Bharat, and makes a hand-checked test on 50–100 of the program's own items the deciding check, plus the licence.
- **Done:** Cases 19 (chatbot, still "doesn't apply"), 20 (its memo already asks the three questions) and 23 (interview; the extraction layer is checked by hand) read consistently with the new text. They have not been rerun against the assistant; that is step 4.

### Step 4. Rebuild, test and document (done)

- `dist/` rebuilt after each step; `python3 scripts/build.py --check` passes. Instructions are at 7,997 of 8,000 characters, the kickoff at 3,989 of 4,000.
- **Cases run, 2026-11-22**, against `dist/all-in-one.md` with Claude Opus 5.5 through `claude -p` (no tools), one interview answer per turn:

| Case | Expected | Result |
|---|---|---|
| 6. Food pantry | No model needed | **Pass.** No model; written packing and short-week rules; no eagerness for technology. |
| 19. Screening chatbot | No model needed, allocation hidden in a chatbot | **Pass** after a second turn. The case's paste didn't give supply against demand, so the assistant asked (as the funder-review rules require). With "about 40 a month, can pay about 35", it gave No model needed for the scoring and kept the chatbot as an intake question. The case now includes that figure in the funder's answers. |
| 20. Court transcription | Review doesn't apply to the tool; rollout needs no model | **Pass.** Called the speech and summary tools an input layer and didn't judge them; No model needed for the rollout (and suggested a lottery of waves, which gives a comparison group); asked all three input-layer questions; marked the hearing-time claim unverified and noted Nethil et al. report speed only. |
| 21. ECG referral | Class 12 with a published model | **Pass.** Class 12 with the published model as an input layer; said a few hundred deaths are too few to train on; calibration by group; competing risk; Zink et al. on removing group variables; the ICD decision left to cardiologists. Follow-up 2 table followed. It argued the death registry measures misses, so it kept the random share only for the simple rule; acceptable. |
| 22. Race-blind risk score | Fits, with fairness conditions | **Pass** after a case fix. The first run asked for the funder's risk appetite, which the case's paste lacked; the paste now includes it and the pool size. Then: Fits with conditions; the full fairness audit (label, calibration by group, with and without race, share of slots); Zink et al. cited correctly. |
| 23. Local-law campaigns | Class 2 with an extraction layer | **Pass.** A yearly scored selection with regional floors; code reading treated as the input layer and tested first against the 30 hand-read codes; LOCUS suggested as a check before building; the NeurIPS acceptance marked unverified. |

- No prompt changes were needed. Cases 1–5 and 7–18 were not rerun; the changes add text for tools, fairness audits and funder reviews, which those cases don't exercise, but a full rerun before the next release is still worthwhile.
- CHANGELOG entries added under **Unreleased**. `VERSION` is unchanged at 1.3.0: in this repo a version bump is its own "Release" commit, together with the funder review already under Unreleased.

## 5. Open questions

- Should the assistant ever say *which* speech or OCR model to use? This plan says no; it would need its own evidence base and would date quickly.
- Should Case 21 become a combined case (Class 12 referral + a Class 7 layer for defibrillator benefit) if a program, not clinicians, decided who gets a device? This plan keeps one class, because guidelines own that decision.
