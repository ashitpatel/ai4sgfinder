# Case harness

Runs the [worked cases](../../docs/cases/README.md) against the assistant and records, for every turn, what it said and what it cost in tokens. It is the test set for prompt changes and the baseline for [tools mode](../../docs/plans/tools-mode.md).

It uses Claude Code's headless mode (`claude -p`), so it needs [Claude Code](https://claude.com/claude-code) installed and signed in. Runs use your Claude plan or API credit: the full set of 25 cases reads several million input tokens, most of them from the prompt cache. Run it by hand before a release, not in CI.

```bash
python3 tests/cases/run_case.py --all --jobs 4
```

```bash
python3 tests/cases/report.py tests/cases/runs/<run folder>
```

- **One case:** `python3 tests/cases/run_case.py 01-chw-hypertension-visits.md`
- **Then a follow-up:** add the turns to send after the recommendation, e.g. `... 01-chw-hypertension-visits.md "4"` for Follow-up 4.
- **The one-click kickoff instead of the full setup:** `--mode kickoff`.
- **Another model:** `--model <name>`.

## What it does

For an interview case it sends the scenario, then each scripted answer from *Interview answers*, one per turn, then asks for the recommendation; it stops sending scripted answers once a recommendation arrives. For a funder case it sends what the funder pastes, and if the assistant asks for the funder's own context, a standard answer. Each case is written as JSON to the run folder (by default `tests/cases/runs/<date>-<mode>/`, which git ignores), with each turn's input tokens (fresh, cache writes and cache reads), output tokens, the list-price cost `claude -p` reports, and the time taken.

`report.py` grades each case against [`expected.json`](expected.json): the primary class for an interview, including a layer where the case has one, or the verdict for a funder review. The grading is a first pass by pattern; read anything it marks *check* or *fail*, and use the [cases index's checklist](../../docs/cases/README.md#using-the-cases) for the rest.

## Baseline

[baseline.md](baseline.md) holds the chat-mode results that tools mode is measured against.
