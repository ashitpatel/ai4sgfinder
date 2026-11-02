# Building an AI4SG Finder from Scratch


## Prompts

These prompts follow the requests that built AI4SG Finder. Each has been rewritten so an agent is less likely to drift: it states the goal and the audience, what to check, and what to avoid. Later corrections are folded into the first prompt that needs them, so nothing has to be redone.

- **Prompts 1–3** design prompts
- **Prompts 4–8** implementation prompts

Read each result before sending the next prompt.

### Design the prompt (chat assistant)

**Prompt 1: Is it worth building?**

```text
I work with NGOs. Is it worth building a decision support system that helps an NGO choose a suitable method for a resource-allocation problem in any impact domain? The method might be an advanced AI/ML method, a simpler optimization method, or no model at all. The system would then help adapt the method to the NGO's key constraints.

1. Does such a tool already exist? Name specific tools, toolkits or papers, with links, and say what each covers and what it doesn't. If you aren't sure something exists, say so; don't invent it.
2. Is it worth building as a set of agent instructions an NGO can run itself? Give the case for and against.

The users are program staff, not computer scientists. Stay on this topic, and don't offer to write other documents.
```

**Prompt 2: Map the methods and the questions that separate them**

```text
Search the academic literature on AI for social good and operations research. Start with the published work of Prof. Lily Xu and Prof. Roshni Sahoo (Columbia) and Prof. Ashish Goel (Stanford), then widen to their students and co-authors and to the rest of the field.

1. Group the allocation approaches into classes. For each class give:
   - a plain-language name;
   - the decision it answers;
   - the underlying methods;
   - the problem traits that point to it;
   - documented field deployments, with full citations (authors, year, venue).
2. For each class, find the simplest approach that comes close: paper and pencil, a spreadsheet or a calculator. Say in what ways it comes close, and what a user must check to decide whether it is close enough.
3. Find real programs that combined two classes, and what signals that need.
4. Turn the characteristics that tell the classes apart into interview questions:
   - Each question is open-ended and asks one thing. Examples are illustrations, not the only choices.
   - Where two classes would get the same answers, add a narrowing question.
   - End with a question that uncovers a second decision calling for a second class.
5. List the well-studied approaches you left out, and why. Don't call the list exhaustive unless you can show it is.
6. Check every researcher's name and every deployment. Mark anything you couldn't confirm as unverified.

Return this as one reference document.
```

**Prompt 3: Write the system prompt**

```text
Using that reference, write a system prompt for the assistant.

It interviews the user one plain-language question per turn, skipping what they have already answered. Then it gives one recommendation with these sections:
1. The recommended class, and why the user's answers point there.
2. What goes wrong with a naive ML model or a spreadsheet instead.
3. How field staff use the result on paper or in Excel.
4. Real deployments of the same or a similar method, preferably by NGOs in the same or a similar domain, with the parallels explained.
5. A report card covering successes, field challenges and unknowns.
6. The simpler alternative: how close it comes, and what to check before settling for it.

If the program needs two classes, it names a primary class and adds the second as a layer.

Rules for the prompt:
- Never invent a citation, deployment or statistic.
- Mark anything uncertain as unverified.
- Never present a simulation as a deployment.

Return the full prompt.
```

### Build the project (coding agent)

**Prompt 4: Package it**

```text
Below are a system prompt and a reference document from a design conversation. Set up a GitHub project in this folder that makes them easy to use in Claude, ChatGPT and Gemini. Also cover browser-based assistants such as Google AI Mode, which have no system-prompt field and no file upload.

- Work out the best format for each platform. Keep one source of truth so the versions can't drift apart.
- Check each platform's current limits, such as instruction length, and stay within them.
- Define each class once, and link every mention of a class name to its definition.
- Write a README that explains how to use each version.
- Use the Apache 2.0 licence.
- Initialize git and commit. Ask me before creating the GitHub repository or pushing anything.

[paste the system prompt and reference document]
```

**Prompt 5: What happens after the recommendation**

```text
Add follow-ups the assistant offers after its recommendation, tailored to the user's answers:
- how to adapt the method to their program;
- what to check before starting: data, consent, fairness, staff capacity;
- how to design a small pilot that is compared with the simpler alternative;
- where to find tools, services or partners;
- what to read and whom to contact;
- a short brief they can hand to a technical partner.

Check that every tool and organization you list exists and is active, and include links. Tell users to recheck them before relying on them.
```

**Prompt 6: Worked examples**

```text
Create worked examples across different impact domains and intervention types. Together they should cover every class and the common combinations of classes. Document them in the repository.

Each example has:
- an illustrative scenario with a fictional organization;
- the answers that organization would give to each interview question;
- the class the assistant should recommend, and why;
- the classes it rules out, and why;
- what a good recommendation contains, including the simpler alternative;
- what a wrong recommendation would look like;
- how the follow-ups help that organization.

Wherever you mention a class or an interview question, give its number and name together. Cite only research you have verified.

Check that the interview questions lead each example to its expected class. Where they don't, fix the prompt.
```

**Prompt 7: Tutorials**

The template inside this prompt is distilled from the project's 14 tutorials, so you don't need a tutorial of your own to attach.

```text
Write an in-depth tutorial for each worked example, for a reader who knows basic statistics (proportions, expected values, confidence intervals) but has no knowledge of ML or advanced optimization. Where an example only combines methods that other tutorials already teach, link to those tutorials instead of writing a new one.

Instructions:
- Files: docs/tutorials/NN-method-program.md, with its program at docs/tutorials/code/caseN_method.py. Add a docs/tutorials/README.md that lists each tutorial with its class and case, and a requirements.txt.
- Use the example's organization and numbers. The data are invented to teach the method; say so.
- Explain every term the first time it appears. Write every formula in math notation, and say in words what each symbol means.
- Work one small example by hand in "The Decision Engine", so a reader can check every step with a calculator.
- In the simulation, compare the method with current practice and with the simpler alternative, on the same data, over many runs.
- Programs use fixed random seeds and numpy. Add a free solver (for example PuLP, with its version pinned) only where it's needed. Each program prints labelled sections that match the tutorial's sections, and runs in about a minute or less.
- Copy every number in the text from the program's output. After any change to the code, rerun it and update the text.
- Use plain headings: no "Chapter" labels and no decimal section numbers.
- Cite only verified references from the taxonomy. Never present a simulation as a deployment.
- When you're done, run every program, check that every number in the text matches its output, and check that every link and anchor resolves.

Template (replace everything in square brackets; keep the headings and their order):

# [Method] Masterclass: [the decision, as a question in the program's words]

*An in-depth walkthrough of [method names], built on [Case N: title](link to the case).*

**You need:** proportions, probabilities, expected values and the idea of a confidence interval. **You don't need:** any machine learning or optimization background. Every term is explained when it first appears.

**Approach:** [Class N: Name](link to its definition). **Code:** [code/caseN_method.py](link). Every number in this tutorial comes from running that file.

---

## Executive Overview

[Two or three short paragraphs: the organization, its numbers (people, budget, how often it decides), and the decision someone must make each round.]
[Why the usual answers (a rotation, a risk score, first come first served, a fixed list) fail, in concrete terms.]

This tutorial builds the alternative step by step:
1. [The Leap]: [one line, linked to the section]
2. The Core Bottleneck: [one line]
3. From [Data] to Estimates: [one line]
4. The Decision Engine: [one line]
5. Scaling Up: [one line]
6. Code Implementation & Simulation: [one line, naming the rules compared]
7. Core Architectural Summary: every piece on one page.

The idea that ties it together: **[one sentence]**

## The [Name] Leap – From [the simple approach] to [the model]

### What [the core concept] is
[The concept in plain words, with an everyday example.]

### Mapping it to the program
| Model term | In this program |
|---|---|
| [term] | [what it is here, with the program's own numbers] |
[Six to nine rows.]

### Why this and not a neighboring class
[The one or two classes it is most easily confused with, by number and name, and the answer that rules each out.]

## The Core Bottleneck – [what is unknown or hard]
[The quantity nobody knows and why it matters, a small table of illustrative groups, and the complications saved for later sections.]

## From [Data] to Estimates – [subtitle]

### Step 1: [Count or tabulate the records]
### Step 2: Put a margin of error on each estimate
### Step 3: [What to do when data are thin]
[For each step: a formula, a worked number from the program, and a table with the estimate, its 95% interval and how many records it rests on.]

## The Decision Engine – [method name]

### The question it answers
### Step-by-step concrete example
[One small case, worked by hand, with every arithmetic step shown.]
### [The result for every group or option]

## Scaling Up – [the real-world limits]
[Capacity, fairness guarantees, staff limits, legal rules: how each changes the plan, and what becomes hard at full size.]

## Code Implementation & Simulation

### [A key piece of the code]
[A short excerpt and what it does.]

### Simulation: [the rules compared, and the number of rounds and runs]
[A table comparing the method, current practice and the simpler alternative on outcome, fairness and cost, followed by what the results mean.]

### The simpler alternative: [the paper, spreadsheet or calculator rule]
[How it performed against the method on the same data.]

In what ways it is close, and what to check before settling for it:
- **Close on [dimension] when [assumption].** [Evidence from the simulation.]
- **Differs when [condition].** [By how much.]
- **Check [assumption] before relying on it.** [How to check it on the program's own records.]

## Core Architectural Summary

| Module | Core formula | What it does in practice |
|---|---|---|
| [each piece of the method, in order] | [its formula] | [its job in the program] |

### Where to go next
- Run the pilot described in the case's follow-ups.
- Read [verified references from the taxonomy].
- Code to build on: [verified open-source tools].
- Other tutorials: [neighboring classes, and when to read each].
```

**Prompt 8: Release**

```text
Before releasing, check three things: every link resolves, every number in a tutorial matches its program's output, and every prompt version is within its platform's limit.

Then bump the version, update the changelog, and show me what will be committed and tagged. After I confirm, commit, push, and publish a release with the files people need attached.
```
