# Tutorials

In-depth walkthroughs of the method behind each [worked case](../cases/). Each one assumes basic statistics (proportions, expected values, confidence intervals) and no knowledge of machine learning or optimization. Every term is explained when it first appears.

| Tutorial | Approach | Case it builds on |
|---|---|---|
| [1. Restless bandits: who gets this week's home visit](01-restless-bandits-chw-visits.md) | [Class 1: Dynamic State Evolution](../../prompt/knowledge/taxonomy.md#class-1-dynamic-state-evolution) | [Health worker visits](../cases/01-chw-hypertension-visits.md) |
| [2. Welfare optimization: siting boreholes fairly](02-welfare-optimization-borehole-siting.md) | [Class 2: Static Demographic Targeting](../../prompt/knowledge/taxonomy.md#class-2-static-demographic-targeting) | [Borehole siting](../cases/02-borehole-siting.md) |
| [3. Security games: patrolling against adaptive fishers](03-security-games-marine-patrols.md) | [Class 3: Spatiotemporal Security & Adaptive Search](../../prompt/knowledge/taxonomy.md#class-3-spatiotemporal-security--adaptive-search) | [Marine patrols](../cases/03-marine-patrols.md) |
| [4. Robust optimization: preparing for cyclones you can't forecast](04-robust-optimization-cyclone-prepositioning.md) | [Class 4: Robust Contingency Planning](../../prompt/knowledge/taxonomy.md#class-4-robust-contingency-planning) | [Cyclone supplies](../cases/04-cyclone-prepositioning.md) |
| [5. Stable matching: placing apprentices when both sides choose](05-stable-matching-apprenticeships.md) | [Class 5: Strategic Matching Markets](../../prompt/knowledge/taxonomy.md#class-5-strategic-matching-markets) | [Apprenticeships](../cases/05-apprenticeship-matching.md) |
| [6. No model needed: deciding with basic statistics](06-no-model-food-pantry.md) | No optimization model | [Food pantry](../cases/06-food-pantry-no-model.md) |

## How each tutorial is organized

Every tutorial follows the same arc, so once you've read one the others are easy to navigate:

1. **Executive Overview:** the decision, why the usual approach fails, and a chapter roadmap.
2. **Chapter 1 – The leap:** from the simple approach to the model, with a table mapping the model's terms to the program.
3. **Chapter 2 – The core bottleneck:** what is unknown or hard.
4. **Chapter 3 – From data to estimates:** the statistics: estimates, margins of error, and what to do when data are thin.
5. **Chapter 4 – The decision engine:** the method itself, with a small example you can check by hand.
6. **Chapter 4.5 – Scaling up:** the full-size problem and its real-world limits.
7. **Chapter 5 – Code and simulation:** a runnable program and what its results mean.
8. **Chapter 6 – Summary:** each part of the method, its core formula and what it does in practice.

## Running the code

Each tutorial has a short Python program in [`code/`](code/). Every number in a tutorial comes from running its program.

```bash
pip install -r docs/tutorials/code/requirements.txt
python3 docs/tutorials/code/case1_restless_bandits.py
```

The programs need only `numpy` and, for cases 2–4, PuLP 3 with its built-in free solver. PuLP is pinned below version 4, which changed the way models are written.

All organizations and numbers in the tutorials are illustrative, chosen to teach the method. The research they cite is real and is drawn from the verified references in the [taxonomy](../../prompt/knowledge/taxonomy.md).
