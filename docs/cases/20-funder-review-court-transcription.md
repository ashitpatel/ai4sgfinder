# Case 20: Funder review of a courtroom transcription proposal

| | |
|---|---|
| **Domain** | Access to justice |
| **Who is using the assistant** | A foundation program officer reviewing a proposal |
| **Expected verdict** | **The review doesn't apply to the transcription itself**; the one allocation decision inside it, the rollout order, needs **no model** |
| **Also acceptable** | Flagging the test plan as a *Mismatch*: the litigant summaries reach people directly, so "pages transcribed per day" measures use, not benefit ([taxonomy, Section 6](../../prompt/knowledge/taxonomy.md#when-the-ai-is-the-intervention)) |
| **Most likely confusion** | Forcing an allocation class onto a speech-recognition tool, or scoring the speech model as if it were an allocation method |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal) |
| **Real-world pattern** | [Adalat AI](https://adalat.ai)'s courtroom transcription in India (see [Evidence](#the-real-world-pattern)) |

## Scenario

A legal-access foundation has a proposal from a (fictional) legal-tech NGO. In the district courts of one state, judges dictate depositions and orders to a typist, slowly, and hearings run short for lack of time. The NGO wants to put a speech-recognition system into 300 courtrooms. It would transcribe testimony in two regional languages and English, and a language model would draft a plain-language summary of each order for litigants. It has the budget for 60 courtroom kits in year one.

*This is an illustrative scenario, not a real program or proposal. The technical approach follows published work by Adalat AI.*

## What the funder pastes

**The proposal, summarized.**
> We will fine-tune an open speech model (Whisper) on legal speech in our two languages and deploy it on an on-premises GPU server in each court complex, so audio never leaves the court. A language model will summarize and translate orders for litigants over WhatsApp. Year one: 60 courtrooms, chosen by an AI model that predicts where the system will save the most time. Similar systems have cut hearing time in half. Budget: US$400,000 over two years. Success measure: pages transcribed per day.

**The funder's answers.**
> We fund access to justice in South Asia. Grants are US$100,000–500,000 over two years. We'll fund pilots, but we need a credible measure of benefit to litigants.

## Why the verdict is "doesn't apply", plus "no model needed" for the rollout

Most of this proposal is a **perception and generation tool**: speech to text, then text to a summary. Nothing is allocated by it. The allocation filters don't fit a typist's replacement, so the assistant says the review doesn't apply to that part ([playbook rule](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal): "If nothing is allocated…").

One decision inside the proposal *is* an allocation: **which 60 of 300 courtrooms get kits first.** Read against the filters:

- **Filter 1:** equipment handed over once, but a rollout: every courtroom gets one within about three years.
- **Filter 4:** a courtroom that waits a year is not harmed; it keeps today's process.
- **Supply and demand:** everyone gets served; only the order changes.

That is the pattern for *No model needed*. A published rule (for example, the courtrooms with the longest backlog first, one per court complex so every district's staff learn the system, and the rest in later waves) is easy to explain to judges and captures nearly all the value. A model that "predicts time saved" needs transcription data that only exists after deployment.

What the funder *does* need is a check on the tool's quality, which is outside the allocation taxonomy but can still be asked about plainly. See questions 2–4 below.

## What a good memo contains

1. **The decision:** which 60 of 300 courtrooms receive transcription kits in year one. The transcription and summaries themselves allocate nothing.
2. **Method fit:** *Review doesn't apply* to the speech model and summaries. For the rollout order, *No model needed*: every courtroom is served within the grant period, so a published order is enough.
3. **The simpler option:** for the rollout, a written order (backlog first, at least one courtroom per court complex). For the tool, the simpler comparison is today's typist on the same hearings.
4. **Questions for the NGO:**
   - What is the word error rate on *your* courts' audio, in each language, measured on recordings the model was not trained on? Is it reported separately for legal terms, names and numbers, which matter most in a deposition?
   - Who corrects the transcript before it becomes part of the record, and how long does correction take compared with typing?
   - How will you check that litigant summaries are accurate, and who answers for a wrong one?
   - What would show benefit to litigants, not pages per day: hearings completed per day, time from hearing to certified copy?
   - What rule will decide the rollout order, and will it be published to judges?
5. **Risks to people:** transcription errors in testimony, worse for speakers of dialects or with strong accents, enter a legal record; a summary that misstates an order can mislead a litigant who can't read the original; recordings of testimony are sensitive and must stay on court premises.
6. **Evidence check:** "cut hearing time in half" has no source and is not among the verified references: *unverified, ask for the citation*. Published work on this approach reports speed and word error rates on benchmarks, not hearing-time effects.
7. **Funding stages:**
   1. A small grant to measure word error rates on 50 hours of the state's own court audio, by language, and the correction time per page.
   2. A pilot in the first wave of courtrooms against matched courtrooms still on typists, measuring hearings completed and time to a certified copy.
   3. Scale by the published rollout order, with a named owner for the servers and a fallback to typists.

## The real-world pattern

[Adalat AI](https://adalat.ai), an Indian legal-tech nonprofit, describes the same system:

- **Speech recognition.** Whisper models fine-tuned for Indian languages, with voice-activity detection cutting audio into short segments and parallel inference on a single GPU ([Interspeech 2025, arXiv 2507.01021](https://arxiv.org/abs/2507.01021)). Its own Conformer models, built in NVIDIA NeMo and released for offline use, are on [Hugging Face](https://huggingface.co/adalat-ai).
- **Evaluation.** A benchmark split by acoustic difficulty ([Vividh-ASR](https://huggingface.co/blog/adalat-ai/vividh-benchmark)), and a metric that separates errors in words, punctuation, numbers and legal entities ([SCRIBE, arXiv 2605.20712](https://arxiv.org/abs/2605.20712)). That is the measurement question 2 asks for.
- **Language models.** Summaries and translations of court orders through a WhatsApp helpline ([customer story](https://claude.com/fr/customers/adalat-ai)).

Reported scale varies by source and date (thousands of courtrooms across several states). The productivity trials Adalat mentions are not published, so a memo should not cite them. The Interspeech paper (Nethil et al., 2025) is among the taxonomy's verified references, for the method only; the productivity claims and courtroom counts are listed as unverified.

## What the assistant should not do

- Pick an allocation class for the speech model itself, or call speech recognition "Class 12" because it uses a trained model.
- Recommend a prediction model to order a rollout that reaches every courtroom anyway.
- Accept "pages transcribed per day" as a benefit to litigants.
- Judge the NGO, or say whether to fund it.
- Quote word error rates or courtroom counts as the proposal's own results.
