# Case 19: Funder review of a screening-chatbot proposal

| | |
|---|---|
| **Domain** | Emergency assistance |
| **Who is using the assistant** | A community foundation program officer reviewing a proposal |
| **Expected verdict** | **No model needed**, with an allocation decision hidden inside a chatbot proposal |
| **Most likely confusion** | Saying the review doesn't apply because the proposal is "just a chatbot" |
| **Playbook section** | [Funder review](../../prompt/knowledge/playbook.md#funder-review-checking-a-proposal) |

## Scenario

A community foundation has a proposal from a local NGO that runs a small emergency fund for rent and utility bills. It receives about 40 applications a month and can pay about 35. The NGO wants to build an AI chatbot that talks applicants through the form and recommends which applications to approve.

*This is an illustrative scenario, not a real program or proposal.*

## What the funder pastes

**The proposal, summarized.**
> We will build a chatbot on a large language model that guides applicants through our application, answers questions in English and Spanish, and scores each application so staff can approve the most urgent first. This will make decisions faster and fairer. Budget: US$60,000 for a developer and a year of hosting. Success measure: time from application to decision.

**The funder's answers.**
> We fund basic needs in one county. Grants are US$5,000–50,000 a year. We're cautious about technology projects; we'd want to know this is the right tool.

## Why the verdict is No model needed

Most of the proposal is a chatbot that answers questions, which on its own would be outside this review. But it also **scores applications to decide who gets paid**. That is an allocation decision, and it's the part that affects people most.

Read against the filters:

- **Filter 1:** cash handed over once (*who gets it*).
- **Filter 4:** a wrong refusal can mean an eviction or a shut-off: harm, not a fixable loss.
- **Supply and demand:** about 35 of 40 monthly applicants can be paid. With supply close to demand, there is little to optimize; the decision is mostly whether each application meets the rules.

A written eligibility rule and a checklist, applied by staff, capture nearly all of the value. A model that scores urgency adds risk: it can be wrong in ways staff can't explain to an applicant who was refused. The speed problem may be real, but it isn't an allocation problem.

## What a good memo contains

1. **The decision:** which of about 40 monthly applicants receive emergency rent or utility help, when about 35 can be paid.
2. **Method fit:** *No model needed.* With supply near demand, a published eligibility rule and checklist decide almost every case. The urgency score is the part to question; the bilingual help with the form is a separate, reasonable use of a chatbot.
3. **The simpler option:** a written rule (eligibility, then order of receipt or a published priority such as a shut-off notice), applied with a checklist. It is easy to explain to every applicant.
4. **Questions for the NGO:**
   - How many eligible applicants were turned away last year for lack of funds? If almost none, what would the score decide?
   - What would the score be based on, and how would staff explain a refusal to an applicant?
   - Where does time go today: the form, missing documents, or the approval itself?
   - Would a simpler form and a bilingual help line meet the speed goal for less?
5. **Risks to people:** an automated urgency score can disadvantage applicants who describe their situation less fluently, or in their second language; a refusal the NGO can't explain undermines trust.
6. **Evidence check:** "faster and fairer" is a claim, not evidence; the proposal cites none.
7. **Funding stages:**
   1. Before any build: a short review of last year's applications, showing how many eligible applicants weren't paid and where delays occurred.
   2. If delays are in the form, fund the help with the form (bilingual guidance) without the scoring.
   3. Revisit scoring only if demand grows well beyond what the fund can pay.

## What the assistant should not do

- Say the review doesn't apply because it's a chatbot, missing the scoring decision inside it.
- Recommend a targeting model (Class 2 or 7) when supply nearly meets demand.
- Judge the NGO or say whether to fund it.
