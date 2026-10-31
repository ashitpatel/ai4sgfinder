# Changelog

Each release on GitHub attaches the ready-to-use files from `dist/`. The version lives in [`VERSION`](VERSION).

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
