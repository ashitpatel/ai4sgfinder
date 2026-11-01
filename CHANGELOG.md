# Changelog

Each release on GitHub attaches the ready-to-use files from `dist/`. The version lives in [`VERSION`](VERSION).

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
