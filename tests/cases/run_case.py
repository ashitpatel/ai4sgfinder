"""Run the worked cases against the assistant through Claude Code's headless mode
(`claude -p`), one turn per scripted answer, and log every turn's tokens.

    python3 tests/cases/run_case.py 01-chw-hypertension-visits.md          # one case
    python3 tests/cases/run_case.py --all --jobs 4                          # all 25
    python3 tests/cases/run_case.py --mode kickoff 19-funder-review-screening-chatbot.md
    python3 tests/cases/run_case.py 01-chw-hypertension-visits.md "4"       # then ask for Follow-up 4
    python3 tests/cases/report.py tests/cases/runs/<run>                    # grade and summarise

Modes:
  chat     the all-in-one file (dist/all-in-one.md) as the system prompt
  kickoff  the one-click kickoff pasted into the first message, with a neutral system prompt

Each case's transcript, with tokens, cost and time per turn, is written as JSON to the
run folder (default tests/cases/runs/<date>-<mode>/, which git ignores). Runs cost tokens:
run them by hand before a release, not in CI.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CASES = REPO / "docs" / "cases"
ALL_IN_ONE = REPO / "dist" / "all-in-one.md"
KICKOFF = REPO / "dist" / "kickoff.md"

REC = re.compile(r"(?is)what kind of problem.*simpler option")
MEMO = re.compile(r"(?is)verdict.*(funding stages|evidence check)|(funding stages|evidence check).*verdict")   # a memo, not a request for context
FUNDER_CONTEXT = ("Our foundation funds programs in this sector in the region the proposal covers; "
                  "grants of US$50,000-200,000 over two years; we fund early pilots if there is a clear test.")
DONE = "That's everything I can tell you. Please give your recommendation."


def section(text, head):
    m = re.search(rf"^## {re.escape(head)}.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def quotes(block):
    """Blockquote runs -> turns, splitting at '*Next turn' lines."""
    turns, cur = [], []
    for line in block.splitlines():
        if line.startswith(">"):
            body = line[1:].strip()
            if body.startswith("*Next turn"):
                if cur:
                    turns.append(" ".join(cur).strip())
                    cur = []
                body = re.sub(r"^\*Next turn[^*]*\*\s*", "", body)
            if body:
                cur.append(body)
        elif cur and line.strip():
            turns.append(" ".join(cur).strip())
            cur = []
    if cur:
        turns.append(" ".join(cur).strip())
    return turns


def script(case_file):
    """The scripted turns for a case, and whether it is an interview or a funder review."""
    text = (CASES / case_file).read_text()
    if "## What the funder pastes" in text:
        paste = section(text, "What the funder pastes")
        paste = re.sub(r"^\*\*|\*\*$", "", paste, flags=re.M).replace("> ", "").replace(">", "")
        return ["I'm a program officer at a foundation reviewing an NGO's proposal.\n\n" + paste], "funder"
    scen = section(text, "Scenario").split("*This is an illustrative")[0].strip()
    return ["Hi. Here's our situation: " + scen] + quotes(section(text, "Interview answers")) + [DONE], "interview"


def ask(msg, sid, mode, model, cwd):
    cmd = ["claude", "-p", msg, "--tools", "", "--output-format", "json", "--setting-sources", ""]
    if mode == "kickoff":
        cmd += ["--system-prompt", "You are a helpful assistant."]
    else:
        cmd += ["--system-prompt-file", str(ALL_IN_ONE)]
    if model:
        cmd += ["--model", model]
    if sid:
        cmd += ["--resume", sid]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200, cwd=cwd)
    if r.returncode:
        raise RuntimeError(f"claude failed: {r.stderr[:500]} {r.stdout[:500]}")
    d = json.loads(r.stdout)
    u = d.get("usage", {})
    return d["result"], d["session_id"], {
        "input_tokens": u.get("input_tokens", 0),
        "cache_creation_input_tokens": u.get("cache_creation_input_tokens", 0),
        "cache_read_input_tokens": u.get("cache_read_input_tokens", 0),
        "output_tokens": u.get("output_tokens", 0),
        "cost_usd": d.get("total_cost_usd"),
        "duration_ms": d.get("duration_ms"),
        "model": next(iter(d.get("modelUsage", {}) or {}), None),
    }


def run(case_file, extra, mode, out, model):
    turns, kind = script(case_file)
    if mode == "kickoff":
        turns[0] = KICKOFF.read_text() + "\n\n" + turns[0]
    out.mkdir(parents=True, exist_ok=True)
    path = out / case_file.replace(".md", ".json")
    record = {"case": case_file, "kind": kind, "mode": mode, "started": dt.datetime.now().isoformat(timespec="seconds"),
              "turns": []}
    sid, done, context_sent = None, False, False
    queue, extra = list(turns), list(extra)
    while queue or extra:
        if queue and not done:
            t = queue.pop(0)
        elif extra:
            t = extra.pop(0)
        else:
            break
        reply, sid, usage = ask(t, sid, mode, model, out)
        record["turns"].append({"user": t, "assistant": reply, **usage})
        if kind == "interview" and REC.search(reply):
            done = True                       # recommendation given: skip the rest of the script
        if kind == "funder" and not done:
            if MEMO.search(reply):
                done = True
            elif not context_sent:            # the assistant asked for the funder's context
                queue.append(FUNDER_CONTEXT)
                context_sent = True
        path.write_text(json.dumps(record, indent=1))
    record["finished"] = dt.datetime.now().isoformat(timespec="seconds")
    path.write_text(json.dumps(record, indent=1))
    return f"done {case_file}: {len(record['turns'])} turns"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case", nargs="?", help="case file name in docs/cases")
    ap.add_argument("extra", nargs="*", help="turns to send after the recommendation or memo")
    ap.add_argument("--all", action="store_true", help="run every case")
    ap.add_argument("--mode", choices=["chat", "kickoff"], default="chat")
    ap.add_argument("--out", type=Path, help="run folder")
    ap.add_argument("--model", help="model to pass to claude -p")
    ap.add_argument("--jobs", type=int, default=1, help="cases to run at once")
    a = ap.parse_args()
    if not a.all and not a.case:
        ap.error("give a case file or --all")
    out = a.out or REPO / "tests" / "cases" / "runs" / f"{dt.date.today()}-{a.mode}"
    cases = sorted(p.name for p in CASES.glob("[0-9][0-9]-*.md")) if a.all else [a.case]
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        futures = [pool.submit(run, c, a.extra, a.mode, out, a.model) for c in cases]
        for f in futures:
            try:
                print(f.result(), flush=True)
            except Exception as e:  # keep going; the report shows what is missing
                print(f"FAILED: {e}", file=sys.stderr, flush=True)
    print(f"run folder: {out}")


if __name__ == "__main__":
    main()
