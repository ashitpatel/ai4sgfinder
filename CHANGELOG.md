# Changelog

Each release on GitHub attaches the ready-to-use files from `dist/`. The version lives in [`VERSION`](VERSION).

## Unreleased

- **Simpler alternatives.** Every recommendation now has a sixth heading, *The simpler alternative*: the best paper, spreadsheet or calculator option for the class, in what ways it comes close (total outcome, fairness, worst case, evidence) and what it gives up, the assumptions to check before settling for it, and how to compare it with the model on past records. The taxonomy's new [Section 4](prompt/knowledge/taxonomy.md#4-simpler-alternatives-for-each-class) lists the option for each class with verified evidence where it exists; the playbook adds a readiness check, a pilot comparison against the simple option, and a "Simpler option to beat" line in the partner brief.
- **Tutorials measure the simple option.** Each tutorial for Cases 1–13 ends with a section comparing the best simple rule with the method on the same illustrative data. New rules in the programs: a six-cell one-step table (Case 1), greedy with a district floor (2), a weighted patrol lottery and a Goal Seek equilibrium (3), an equal split of stock (4), greedy within area envelopes (7), greedy placement with quarterly allotments (11), most-named residents spread across friend groups (12) and oldest-first with a random share (13). Earlier figures in the tutorials are unchanged.
- **Two classes together.** The interview ends with a question about a second decision in the same program (when to act, where to look first, how it reaches people, or which version works for whom); a yes adds a second class as a layer. The taxonomy's new [Section 5](prompt/knowledge/taxonomy.md#5-when-two-classes-combine) lists combinations seen in practice, with real examples.
- Three new worked cases that combine classes: cash released before a flood (Class 4 trigger with a Class 2 targeting layer), snare search with randomized patrols (Class 12 with a Class 3 layer) and job-search support that learns which option works for whom (Class 8 with a Class 7 layer). Cases 1–13 gain an answer to the second-decision question and a simpler-alternative section; Cases 4, 7, 9 and 13 show second decisions that are not a separate layer, or only a later one.
- New tutorial 14, for the cash-before-a-flood case: choosing a forecast trigger with the cost-loss rule, a calculator table of past seasons, and a threshold that holds up across every forecast model a thin record can't rule out, with the targeting list as a second layer. Its program tests the rules on simulated monsoons and stress scenarios; the calculator table chose the same threshold as both models.
- New verified references: Hanna & Olken (2018), Kim et al. (2015), Abdulkadiroğlu & Sönmez (2003), Clarke & Wright (1964), Hadad et al. (2021), Gholami et al. (2017), Pople et al. (2021), Bansak et al. (2018), plus comparisons with simple rules reported in Mate et al. (2022), Aiken et al. (2022) and Kempe et al. (2003).

## 1.2.0 — 2026-10-31

- Seven new allocation classes, found by reviewing the research of Lily Xu, Roshni Sahoo and Ashish Goel's group, then their wider networks of collaborators and the AI-for-social-good literature, against the original five:
  - **Class 6: Participatory Allocation** — a community votes on how a shared budget is split (participatory budgeting, knapsack voting, the method of equal shares).
  - **Class 7: Effect-Based Targeting** — give a program to the people it helps most, learned from pilot or trial data, rather than to the neediest by default (policy learning, causal forests).
  - **Class 8: Learn-While-Allocating** — learn which of several stable options works while still serving people (bandits, adaptive experiments).
  - **Class 9: Routing & Logistics** — move goods or people through depots and routes at least cost (vehicle routing, supply-chain network design).
  - **Class 10: Online Assignment & Waitlists** — place people or items that arrive one at a time (online allocation, dynamic rationing, lotteries).
  - **Class 11: Network Seeding** — choose the few people whose social ties spread information furthest (influence maximization).
  - **Class 12: Risk-Based Inspection** — decide where to inspect or test to find hidden hazards (predictive risk ranking, active search).
- The twelve classes are grouped into five families in the system prompt and kickoff, which now list one line per class to stay within the 8,000- and 4,000-character limits. Class numbers 1–5 are unchanged.
- The taxonomy, decision tree, system prompt, kickoff prompt, playbook, README and social preview image cover all twelve classes. The interview now runs in two stages: five filters, each one plain question per turn (with an optional follow-up), place the problem in a family; then one or two narrowing questions pick the class. Each family's narrowing questions are in the taxonomy's decision tree, along with a table of the data each class needs.
- Feeding America's "Choice System" moves from Class 5 to Class 10: it is an auction with credits for donations as they arrive, not a two-sided stable match.
- Class 4 now covers forecast-triggered anticipatory action; Class 2 notes predict-then-assign variants and eligibility rules that applicants can game.
- The unverified "Roshni Sahu" attribution is corrected to Roshni Sahoo, with her verified papers.
- Seven new worked cases (Cases 7–13), one for each of Classes 6–12, each with interview answers, what a good recommendation contains, and Follow-ups 1 and 6 in full. The six existing cases are updated for the two-stage interview and name their new neighboring classes. The case index is grouped by family.
- Seven new tutorials (7–13), one per new case, each with a runnable program that produces every number in the text. Tutorials 1–6 reviewed and updated to name their new neighboring classes and link the new tutorials.

## 1.1.2 — 2026-10-31

- New in-depth tutorials, one per worked case, explaining how each method works for readers with basic statistics and no optimization background. Each comes with a runnable Python program that produces every number in the text.
- New `CITATION.cff`, so the repository can be cited (GitHub's "Cite this repository" button). Releases are archived on Zenodo with a DOI.
- The README now opens with a short sample session.
- The files in `dist/` are unchanged apart from the version number in the Claude Code plugin manifest.

## 1.1.1 — 2026-10-30

- Each class now has a plain-language definition in the taxonomy: what it is, the question it answers, and when to use or avoid it.
- Class names in the worked cases, cases index, playbook and README link to these definitions.
- The playbook uses the full Class 3 name (Spatiotemporal Security & Adaptive Search) throughout.

## 1.1.0 — 2026-10-30

- New implementation playbook (`playbook.md`), shipped as a second knowledge file in every package, covering what to do after an approach is chosen.
- After its recommendation, the assistant now offers six follow-ups tailored to the user's answers: fit the model to your program, readiness checks, pilot design, build options (tools and partners), reading and people to contact, and a one-page brief for a technical partner.
- The kickoff prompt offers the same follow-ups.
- Worked case 1 now includes a filled-in partner brief.

## 1.0.0 — 2026-10-30

First release.

- System prompt that diagnoses an allocation problem through five filters and recommends one of five AI4SG approaches, or no model at all.
- Reference taxonomy with a decision tree and verified citations; unverified claims from the original draft are flagged.
- Ready-made files for Claude Projects, Custom GPTs, Gemini Gems, Google AI Studio, and browser assistants (including a paste-in kickoff prompt under 4,000 characters).
- Claude Skill and Claude Code plugin.
- API chat examples for Claude, OpenAI, and Gemini.
- Six worked cases, one per class plus a "no model" case.
