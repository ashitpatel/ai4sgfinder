# Case 25: Funder review of an AI tutor proposal

| | |
|---|---|
| **Domain** | Secondary education |
| **Who is using the assistant** | A foundation program officer reviewing a proposal |
| **Expected verdict** | **Mismatch in the test plan**: the AI is the intervention, and success is measured by usage, not learning |
| **Most likely confusion** | Saying the review doesn't apply because nothing is allocated, or judging the language model instead of the test |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal) |
| **Real-world pattern** | Randomized trials of AI tutors in Nigeria and the US, with opposite results ([taxonomy, Section 6](../../prompt/knowledge/taxonomy.md#when-the-ai-is-the-intervention)) |

## Scenario

A (fictional) education NGO runs after-school English and maths clubs in 40 public secondary schools. It wants to add an AI tutor on WhatsApp for about 5,000 students, available at home and in the clubs.

*This is an illustrative scenario, not a real program or proposal.*

## What the funder pastes

**The proposal, summarized.**
> We will build an AI tutor on a large language model that explains English and maths step by step in English and the local language, available on WhatsApp. Club facilitators will introduce it, and students can use it at home. AI tutors have been shown to double learning gains. Budget: US$220,000 over two years. Success measures: monthly active users and messages per student.

**The funder's answers.**
> We fund secondary education in two countries in West Africa. Grants are US$100,000–300,000 over two years. We fund pilots but need evidence of learning before scaling.

## Why the verdict is a Mismatch in the test plan

Nothing is allocated here: the tutor is the program. So the question isn't which class of method, but whether the proposal will show that the tutor improves learning. It won't, as written:

- **The success measures count use, not learning.** A tutor can be popular and teach little, or be used briefly and teach a lot.
- **There's no comparison.** Without one, gains can't be separated from what the clubs already achieve.
- **The evidence points both ways.** A six-week randomized trial of GPT-4 tutoring in after-school sessions in Edo State, Nigeria, raised English scores by 0.23 standard deviations (De Simone et al., 2025). A two-year trial of Khanmigo in 18 US middle schools found gains similar to practice without AI (Oreopoulos & Low, 2026). Both are randomized trials, and neither shows "double".
- **Design matters as much as the model.** In Edo, students worked in pairs with a teacher present; tools that support a human tutor have also shown gains (Wang et al., 2024). At-home use with no facilitator is a different program.

## What a good memo contains

1. **The decision:** whether to add an AI tutor to after-school clubs in 40 schools for about 5,000 students. Nothing is allocated; the tutor is the intervention.
2. **Method fit:** *Mismatch in the test plan.* The review doesn't judge the model. It judges the test: usage measures can't show learning, and there is no comparison group.
3. **The simpler option to beat:** the clubs as they are, or the clubs with the same extra time spent on practice without AI. That is the comparison arm.
4. **Questions for the NGO:**
   - Which learning outcome will you measure (a curriculum-aligned English and maths test), and when?
   - Will you randomize, by school or by club, between the clubs with the tutor and the clubs without?
   - Will students use it in clubs with a facilitator, at home alone, or both? Those are different programs; test the one you'll scale.
   - How will you check its answers, in both languages, against a teacher's on a sample of questions?
   - What does it do when a student asks something off-topic or unsafe, and who is told?
5. **Risks to people:** wrong explanations, worse in the local language; students without phones left out; children's messages and data held by a third party.
6. **Evidence check:** "double learning gains" has no source: *unverified*. The verified trials found gains of about a quarter of a standard deviation in one setting and close to non-AI practice in another.
7. **Funding stages:**
   1. A small grant to build the tutor and grade 200 of its answers against teachers', by language.
   2. A one-year pilot randomized across the 40 schools, measuring learning against the clubs without the tutor, with use tracked only as a secondary measure.
   3. Scale only if learning gains are clear, with a named owner for the content and safety checks.

## What the assistant should not do

- Say the review doesn't apply because nothing is allocated.
- Judge or recommend a particular language model.
- Accept monthly active users as evidence of learning.
- Quote the Nigerian trial's effect as what this program will achieve.
