"""Grade and summarise a run folder written by run_case.py.

    python3 tests/cases/report.py tests/cases/runs/<run> [--markdown out.md]

For each case: whether the primary class (interviews) or verdict (funder reviews) matches
tests/cases/expected.json, turns, input tokens (fresh + cache writes + cache reads), output
tokens, the list-price cost claude -p reports, and the length of the recommendation or memo.
The grading is a first pass by pattern: read any case marked "check" or "fail" by hand.
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = json.loads((HERE / "expected.json").read_text())
REC = re.compile(r"(?is)what kind of problem.*simpler option")
MEMO = re.compile(r"(?is)verdict.*(funding stages|evidence check)|(funding stages|evidence check).*verdict")   # a memo, not a request for context
VERDICTS = ["heavier than needed", "no model needed", "mismatch", "fits"]


def primary_class(text):
    head = text[:900]
    m = re.search(r"(?i)\*\*class:?\*\*\s*(?:class\s*)?(\d{1,2})\b", head)
    if m:
        return int(m.group(1))
    if re.search(r"(?i)\*\*class:?\*\*[^\n]{0,80}(don.t need|no (optimization )?model|not need)", head):
        return "none"
    m = re.search(r"(?i)\bclass\s+(\d{1,2})\b", head)
    if m:
        return int(m.group(1))
    if re.search(r"(?i)(don.t need an optimization model|no model (is )?needed)", head):
        return "none"
    return None


def verdicts(text):
    found = []
    for m in re.finditer(r"(?i)verdict", text):
        window = text[m.end():m.end() + 80].lower()
        hits = [(window.find(v), v) for v in VERDICTS if v in window]
        if hits:
            found.append(min(hits)[1])
    return found


def grade(rec):
    exp = EXPECTED.get(rec["case"], {})
    turns = rec["turns"]
    inp = sum(t["input_tokens"] + t["cache_creation_input_tokens"] + t["cache_read_input_tokens"] for t in turns)
    out = sum(t["output_tokens"] for t in turns)
    cost = sum(t["cost_usd"] or 0 for t in turns)
    row = {"case": rec["case"][:2], "kind": rec["kind"], "turns": len(turns), "input": inp, "output": out,
           "cost": cost, "words": "", "got": "", "result": "no answer"}
    if rec["kind"] == "interview":
        idx = next((i for i, t in enumerate(turns) if REC.search(t["assistant"])), None)
        if idx is None:
            return row
        text = turns[idx]["assistant"]
        got = primary_class(text)
        row.update(words=len(text.split()), got=got, turns_to_answer=idx + 1)
        ok = got in exp.get("classes", [])
        layer = exp.get("layer")
        if ok and layer and not re.search(rf"(?i)class\s*{layer}\b|\b{layer}\s*[—-]", text[:2500]):
            row["result"] = "check (layer?)"
        else:
            row["result"] = "pass" if ok else ("check" if got is None else "fail")
    else:
        idx = next((i for i, t in enumerate(turns) if MEMO.search(t["assistant"])), None)
        if idx is None:
            return row
        text = turns[idx]["assistant"]
        got = verdicts(text)
        row.update(words=len(text.split()), got=", ".join(dict.fromkeys(got)), turns_to_answer=idx + 1)
        want = exp.get("verdicts", [])
        row["result"] = "pass" if any(v in want for v in got) else ("check" if not got else "fail")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", type=Path)
    ap.add_argument("--markdown", type=Path)
    a = ap.parse_args()
    rows = [grade(json.loads(p.read_text())) for p in sorted(a.run.glob("*.json"))]
    lines = ["| Case | Kind | Result | Got | Turns | Input tokens | Output tokens | Words in answer | Cost (list, US$) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['case']} | {r['kind']} | {r['result']} | {r['got']} | {r['turns']} | {r['input']:,} | "
                     f"{r['output']:,} | {r['words']} | {r['cost']:.2f} |")
    n = len(rows) or 1
    tot_in, tot_out, tot_cost = (sum(r[k] for r in rows) for k in ("input", "output", "cost"))
    passes = sum(r["result"] == "pass" for r in rows)
    lines += ["", f"Cases: {len(rows)}; pass: {passes}; others to read by hand: {len(rows) - passes}.",
              f"Input tokens: {tot_in:,} in all, {tot_in // n:,} a case on average. "
              f"Output tokens: {tot_out:,} in all, {tot_out // n:,} a case. "
              f"List-price cost reported: US${tot_cost:.2f} in all, US${tot_cost / n:.2f} a case."]
    text = "\n".join(lines)
    print(text)
    if a.markdown:
        a.markdown.write_text(text + "\n")


if __name__ == "__main__":
    main()
