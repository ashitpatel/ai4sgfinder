"""Build the replay kit: three Excel workbooks that replay a program's past records
under its current practice, a simple rule and (optionally) a model's scores.

    pip install openpyxl
    python3 scripts/build_replay_kit.py

Writes tools/replay-kit/*.xlsx. Every result is a formula, so the sheets
recalculate when a program pastes in its own records. The sample data is made
up (fixed seed) and only shows the format.
"""
import math
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter as col

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "replay-kit"

FONT = "Arial"
F = Font(name=FONT, size=10)
BOLD = Font(name=FONT, size=10, bold=True)
TITLE = Font(name=FONT, size=14, bold=True)
H2 = Font(name=FONT, size=11, bold=True)
INPUT = Font(name=FONT, size=10, color="0000FF")
WRAP = Alignment(wrap_text=True, vertical="top")
FILL_INPUT = PatternFill("solid", fgColor="FFF2CC")   # pale yellow: cells to edit
FILL_HEAD = PatternFill("solid", fgColor="D9E1F2")    # header rows
FILL_CALC = PatternFill("solid", fgColor="F2F2F2")    # calculated, don't edit
THIN = Border(bottom=Side(style="thin", color="999999"))
PCT = "0.0%"
NUM1 = "0.0"
NUM2 = "0.00"


def font_all(ws):
    for row in ws.iter_rows():
        for c in row:
            if c.font is None or c.font.name != FONT:
                c.font = Font(name=FONT, size=c.font.size if c.font and c.font.size else 10,
                              bold=c.font.bold if c.font else False,
                              color=c.font.color if c.font else None)


def head(ws, row, labels, start=1):
    for i, text in enumerate(labels):
        c = ws.cell(row=row, column=start + i, value=text)
        c.font, c.fill, c.alignment = BOLD, FILL_HEAD, WRAP


def readme(wb, title, paragraphs):
    ws = wb.active
    ws.title = "Read me"
    ws.column_dimensions["A"].width = 110
    ws["A1"] = title
    ws["A1"].font = TITLE
    r = 3
    for p in paragraphs:
        if p.startswith("## "):
            ws.cell(row=r, column=1, value=p[3:]).font = H2
        else:
            c = ws.cell(row=r, column=1, value=p)
            c.font, c.alignment = F, WRAP
        r += 1
    legend = r + 1
    ws.cell(row=legend, column=1, value="Colours").font = H2
    c = ws.cell(row=legend + 1, column=1, value="Yellow cells with blue text: your settings and records. Edit these.")
    c.fill, c.font = FILL_INPUT, INPUT
    c = ws.cell(row=legend + 2, column=1, value="Grey cells: calculated. Don't type over them.")
    c.fill, c.font = FILL_CALC, F
    c = ws.cell(row=legend + 3, column=1, value="Blue header rows: column names.")
    c.fill, c.font = FILL_HEAD, BOLD
    return ws


def setting(ws, row, label, value, note, fmt=None):
    ws.cell(row=row, column=1, value=label).font = F
    c = ws.cell(row=row, column=2, value=value)
    if isinstance(value, str) and value.startswith("="):
        c.font, c.fill = F, FILL_CALC
    else:
        c.font, c.fill = INPUT, FILL_INPUT
    if fmt:
        c.number_format = fmt
    n = ws.cell(row=row, column=3, value=note)
    n.font, n.alignment = F, WRAP


COMMON_END = [
    "## What a replay can and can't tell you",
    "It shows what each rule would have chosen from the same records, and how those choices compare on the measures below. It doesn't show what would have happened to people under a rule nobody used: their outcomes were never recorded. Read the results as a check of whether a model is worth building, not as a forecast.",
    "Keep the records on your own computer. Don't paste names or phone numbers: an ID that only your staff can link to a person is enough.",
    "If a rule you are testing comes within a few percent of the model, the simple rule is usually the better choice: it costs less, staff can explain it, and it doesn't break when a volunteer leaves.",
    "Made by AI4SG Finder (github.com/ashitpatel/ai4sgfinder). The sample records are made up and only show the format.",
]


# ---------------------------------------------------------------------------
# 1. Pick N once, checked against an outcome known later
# ---------------------------------------------------------------------------

def pick_n(path):
    rng = random.Random(11)
    MAXROWS = 2000
    last = MAXROWS + 1
    groups = ["North", "South", "East", "West"]
    wb = Workbook()
    readme(wb, "Replay kit 1: Pick N once (who gets it)", [
        "For a one-off choice of who or what gets a limited resource: cash transfers, filters, places in a program, sites to inspect. It ranks your past list under three rules and checks each against an outcome you learned later, such as which households a survey found to be poor, or which homes turned out to have lead pipes.",
        "## What you need",
        "One row per person, household or site considered, up to 2,000 rows. For each: a group (district, area), up to three facts you could have used to rank them, whether your current practice chose them, a model's score if a partner built one, and the outcome learned later.",
        "The later outcome must be known for everyone on the list, or for a random sample of it. If it is known only for the ones you chose (you only find lead in the homes you inspect), this replay will mislead: add a random share to next year's choice first.",
        "## Steps",
        "1. On Settings, enter how many could be chosen (N), any minimum per group, and the points for each fact in the simple rule.",
        "2. On Data, replace the sample rows with your own records in the yellow columns A to H. Leave the grey columns alone. Delete unused sample rows from columns A to H.",
        "3. On Settings, list your groups (up to eight).",
        "4. Read Results: how many of each rule's choices turned out to be in need, and what share of everyone in need each rule reached, overall and by group.",
        "## The three rules",
        "Current practice: whoever you actually chose (column F). Simple rule: a points score from up to three facts, highest first, after giving each group its minimum. Model: a partner's score (column G), highest first, with the same minimum. A random choice of N is shown as a floor any rule should beat.",
    ] + COMMON_END)

    st = wb.create_sheet("Settings")
    st.column_dimensions["A"].width = 34
    st.column_dimensions["B"].width = 14
    st.column_dimensions["C"].width = 70
    st["A1"] = "Settings"
    st["A1"].font = TITLE
    setting(st, 3, "How many can be chosen (N)", 200, "The number of slots: transfers, filters, places, inspections.")
    setting(st, 4, "Minimum chosen per group", 30, "Applied to the simple rule and the model. 0 for none. Groups with fewer people get all of them.")
    st.cell(row=6, column=1, value="Simple rule: points per unit of each fact").font = H2
    setting(st, 7, "=Data!C1", 1, "Points for each unit of this fact (the name comes from the Data header). A negative number lowers priority.")
    setting(st, 8, "=Data!D1", 3, "")
    setting(st, 9, "=Data!E1", 2, "")
    for r in (7, 8, 9):
        st.cell(row=r, column=1).fill = FILL_CALC
    st.cell(row=11, column=1, value="Groups (up to eight)").font = H2
    for i in range(8):
        c = st.cell(row=12 + i, column=1, value=groups[i] if i < len(groups) else None)
        c.font, c.fill = INPUT, FILL_INPUT
    st.cell(row=12, column=3, value="Type each group name exactly as it appears in Data column B.").font = F
    st.cell(row=21, column=1, value="Worked out from the data").font = H2
    setting(st, 22, "Rows of data", f"=COUNTA(Data!A2:A{last})", "")
    setting(st, 23, "Slots reserved for minimums: simple rule", f"=SUM(Data!K2:K{last})", "")
    setting(st, 24, "Slots reserved for minimums: model", f"=SUM(Data!P2:P{last})", "")
    setting(st, 25, "Model scores given", f"=COUNT(Data!G2:G{last})", "0 means no model to compare; its rows in Results stay blank.")

    d = wb.create_sheet("Data")
    head(d, 1, ["ID", "Group", "Household size", "No land (1/0)", "Woman-headed (1/0)",
                "Chosen now (1/0)", "Model score", "In need, found later (1/0)",
                "Simple score", "Simple: rank in group", "Simple: reserved", "Simple: rank, rest", "Simple: chosen",
                "Model: rank in group", "Model: reserved", "Model: rank, rest", "Model: chosen"])
    widths = [10, 10, 11, 10, 12, 11, 10, 12, 10, 11, 10, 10, 10, 11, 10, 10, 10]
    for i, w in enumerate(widths):
        d.column_dimensions[col(i + 1)].width = w
    d.freeze_panes = "A2"
    d["A1"].comment = Comment("One row per person, household or site considered. Use an ID, not a name.", "AI4SG Finder")
    d["H1"].comment = Comment("1 if the outcome learned later shows they were in need (or a hazard was found), else 0. Must be known for everyone, or a random sample.", "AI4SG Finder")
    d["G1"].comment = Comment("Optional: a partner model's score, higher = higher priority. Leave blank if there is none.", "AI4SG Finder")
    d["F1"].comment = Comment("1 if your current practice chose them, else 0.", "AI4SG Finder")

    # sample: 1,000 households
    n = 1000
    for i in range(n):
        r = i + 2
        g = groups[i % 4]
        size = max(1, min(10, int(rng.gauss(5, 2))))
        noland = 1 if rng.random() < 0.35 else 0
        woman = 1 if rng.random() < 0.25 else 0
        area = {"North": 0.3, "South": -0.2, "East": 0.1, "West": -0.4}[g]
        base = 0.35 * size + 1.1 * noland + 0.6 * woman + area - 3.2
        poor = 1 if base + rng.gauss(0, 1.3) > 0 else 0          # what a later survey finds
        model = round(1 / (1 + math.exp(-(base + rng.gauss(0, 0.4)))), 3)  # knows the fields and areas, not the rest
        current = 0.15 * size + 0.5 * noland + rng.gauss(0, 1.2) + (0.4 if g == "South" else 0)
        vals = [f"H{i + 1:04d}", g, size, noland, woman, current, model, poor]
        for j, v in enumerate(vals):
            c = d.cell(row=r, column=j + 1, value=v)
            c.font, c.fill = INPUT, FILL_INPUT
    # current practice: top 200 by its own noisy view, plus 50 per South (a local quota)
    cur = sorted(range(n), key=lambda i: -d.cell(row=i + 2, column=6).value)[:200]
    for i in range(n):
        d.cell(row=i + 2, column=6).value = 1 if i in set(cur) else 0

    for r in range(2, last + 1):
        A = f"$A{r}"
        f = {
            "I": f'=IF({A}="","",C{r}*Settings!$B$7+D{r}*Settings!$B$8+E{r}*Settings!$B$9)',
            "J": f'=IF({A}="","",COUNTIFS($B$2:$B${last},B{r},$I$2:$I${last},">"&I{r})+COUNTIFS($B$2:B{r},B{r},$I$2:I{r},I{r}))',
            "K": f'=IF({A}="","",IF(J{r}<=Settings!$B$4,1,0))',
            "L": f'=IF({A}="","",IF(K{r}=1,"",COUNTIFS($K$2:$K${last},0,$I$2:$I${last},">"&I{r})+COUNTIFS($K$2:K{r},0,$I$2:I{r},I{r})))',
            "M": f'=IF({A}="","",IF(K{r}=1,1,IF(L{r}<=Settings!$B$3-Settings!$B$23,1,0)))',
            "N": f'=IF(OR({A}="",G{r}=""),"",COUNTIFS($B$2:$B${last},B{r},$G$2:$G${last},">"&G{r})+COUNTIFS($B$2:B{r},B{r},$G$2:G{r},G{r}))',
            "O": f'=IF(OR({A}="",G{r}=""),"",IF(N{r}<=Settings!$B$4,1,0))',
            "P": f'=IF(OR({A}="",G{r}=""),"",IF(O{r}=1,"",COUNTIFS($O$2:$O${last},0,$G$2:$G${last},">"&G{r})+COUNTIFS($O$2:O{r},0,$G$2:G{r},G{r})))',
            "Q": f'=IF(OR({A}="",G{r}=""),"",IF(O{r}=1,1,IF(P{r}<=Settings!$B$3-Settings!$B$24,1,0)))',
        }
        for k, v in f.items():
            c = d[f"{k}{r}"]
            c.value, c.fill, c.font = v, FILL_CALC, F
    # the model's reserved column is O, so fix the Settings reference
    st["B24"] = f"=SUM(Data!O2:O{last})"

    res = wb.create_sheet("Results")
    res.column_dimensions["A"].width = 30
    for c_ in "BCDEFGHIJ":
        res.column_dimensions[c_].width = 14
    res["A1"] = "Results"
    res["A1"].font = TITLE
    res["A2"] = "All figures are formulas over the Data sheet. Read them with the notes on the Read me sheet."
    res["A2"].font = F
    head(res, 4, ["Rule", "Chosen", "Of whom in need", "Share of chosen in need", "Share of all in need reached"])
    R = f"Data!$H$2:$H${last}"
    rows = [
        ("Current practice", f"Data!$F$2:$F${last}"),
        ("Simple rule", f"Data!$M$2:$M${last}"),
        ("Model", f"Data!$Q$2:$Q${last}"),
    ]
    for i, (name, rng_) in enumerate(rows):
        r = 5 + i
        res.cell(row=r, column=1, value=name).font = BOLD
        guard = 'IF(Settings!$B$25=0,"",' if name == "Model" else "("
        res.cell(row=r, column=2, value=f"={guard}COUNTIF({rng_},1))")
        res.cell(row=r, column=3, value=f"={guard}COUNTIFS({rng_},1,{R},1))")
        res.cell(row=r, column=4, value=f'=IF(OR(B{r}="",B{r}=0),"",C{r}/B{r})').number_format = PCT
        res.cell(row=r, column=5, value=f'=IF(OR(B{r}="",COUNTIF({R},1)=0),"",C{r}/COUNTIF({R},1))').number_format = PCT
    r = 8
    res.cell(row=r, column=1, value="Random choice of N (expected)").font = BOLD
    res.cell(row=r, column=2, value="=Settings!$B$3")
    res.cell(row=r, column=3, value=f"=Settings!$B$3*COUNTIF({R},1)/Settings!$B$22").number_format = NUM1
    res.cell(row=r, column=4, value=f'=IF(B{r}=0,"",C{r}/B{r})').number_format = PCT
    res.cell(row=r, column=5, value=f'=IF(COUNTIF({R},1)=0,"",C{r}/COUNTIF({R},1))').number_format = PCT
    res.cell(row=10, column=1, value="People in need on the list").font = F
    res.cell(row=10, column=2, value=f"=COUNTIF({R},1)")
    res.cell(row=11, column=1, value="Chosen by both the simple rule and the model").font = F
    res.cell(row=11, column=2, value=f'=IF(Settings!$B$25=0,"",COUNTIFS(Data!$M$2:$M${last},1,Data!$Q$2:$Q${last},1))')
    res.cell(row=12, column=1, value="Simple rule's gap to the model, in people in need reached").font = F
    res.cell(row=12, column=2, value='=IF(Settings!$B$25=0,"",C7-C6)')
    res.cell(row=12, column=3, value="Positive: the model reaches more. Weigh it against the model's full cost.").font = F

    head(res, 14, ["By group", "On the list", "In need", "Chosen now", "In need reached now",
                   "Chosen: simple", "In need reached: simple", "Chosen: model", "In need reached: model"])
    G = f"Data!$B$2:$B${last}"
    for i in range(8):
        r = 15 + i
        res.cell(row=r, column=1, value=f'=IF(Settings!$A${12 + i}="","",Settings!$A${12 + i})')
        a = f"$A{r}"
        res.cell(row=r, column=2, value=f'=IF({a}="","",COUNTIF({G},{a}))')
        res.cell(row=r, column=3, value=f'=IF({a}="","",COUNTIFS({G},{a},{R},1))')
        res.cell(row=r, column=4, value=f'=IF({a}="","",COUNTIFS({G},{a},Data!$F$2:$F${last},1))')
        res.cell(row=r, column=5, value=f'=IF({a}="","",COUNTIFS({G},{a},Data!$F$2:$F${last},1,{R},1))')
        res.cell(row=r, column=6, value=f'=IF({a}="","",COUNTIFS({G},{a},Data!$M$2:$M${last},1))')
        res.cell(row=r, column=7, value=f'=IF({a}="","",COUNTIFS({G},{a},Data!$M$2:$M${last},1,{R},1))')
        res.cell(row=r, column=8, value=f'=IF(OR({a}="",Settings!$B$25=0),"",COUNTIFS({G},{a},Data!$Q$2:$Q${last},1))')
        res.cell(row=r, column=9, value=f'=IF(OR({a}="",Settings!$B$25=0),"",COUNTIFS({G},{a},Data!$Q$2:$Q${last},1,{R},1))')
    res.cell(row=24, column=1, value="Compare each group's share of the chosen with its share of the people in need. A rule that reaches more people in total can still leave one group behind.").font = F
    for ws in wb.worksheets:
        font_all(ws)
    wb.calculation.fullCalcOnLoad = True   # no cached values: compute on open
    wb.save(path)


# ---------------------------------------------------------------------------
# 2. Weekly visit list
# ---------------------------------------------------------------------------

def weekly_visits(path):
    rng = random.Random(7)
    MAXROWS = 6000
    last = MAXROWS + 1
    groups = ["A", "B", "C"]
    # chance of being "on track" next week: (group) -> (state now) -> (no visit, visit)
    P = {"A": {1: (0.80, 0.95), 0: (0.15, 0.55)},
         "B": {1: (0.85, 0.90), 0: (0.10, 0.20)},
         "C": {1: (0.60, 0.85), 0: (0.30, 0.45)}}
    wb = Workbook()
    readme(wb, "Replay kit 2: Weekly visit list", [
        "For a decision made again each week about the same people: which patients get a home visit, which mothers get a call, which students get a tutor session. It learns from your past weeks how much a visit helped people in each group and situation, then asks how much each rule's choice would have gained each week.",
        "## What you need",
        "One row per person per week, up to 6,000 rows: the week number, an ID, a group (for example, how they responded in the past, or an area), whether they were on track that week (1) or not (0), whether they got a visit, whether they were on track the next week, and a risk score if you use one.",
        "\"On track\" is whatever your program aims for, recorded the same way each week: took their medication, attended, picked up the call.",
        "## Steps",
        "1. On Settings, enter how many visits staff can make each week, and list your groups.",
        "2. On Data, replace the sample rows with your records in the yellow columns A to G. Leave the grey columns alone.",
        "3. Check the Table sheet: each cell shows how often people in a group and situation were on track the next week with and without a visit. Cells with few records are flagged; merge groups if many are.",
        "4. Read Results: the expected extra people on track from each rule's visits, per 100 visits, and how visits split across groups.",
        "## The rules",
        "Current practice: the visits staff actually made. Table rule: each week, visit the people whose group and situation gained most from a visit in the past (the \"six-cell table\" from the AI4SG Finder tutorials). Risk score: each week, visit the highest risk scores. Random visits are shown as a floor.",
        "## A caution about the table",
        "The table compares people who were visited with people who weren't. If staff chose whom to visit, those groups differ in ways the records may not show, and the table can overstate or understate what a visit does. A small random share of visits each week (one in ten, say) makes next year's table trustworthy. The gain counts only the next week; a visit's effect that lasts longer isn't counted.",
    ] + COMMON_END)

    st = wb.create_sheet("Settings")
    st.column_dimensions["A"].width = 34
    st.column_dimensions["B"].width = 14
    st.column_dimensions["C"].width = 70
    st["A1"] = "Settings"
    st["A1"].font = TITLE
    setting(st, 3, "Visits staff can make each week", 20, "The same number is used for the table rule and the risk score.")
    setting(st, 4, "Records needed per table cell", 20, "Cells with fewer records than this are flagged on the Table sheet.")
    st.cell(row=6, column=1, value="Groups (up to six)").font = H2
    for i in range(6):
        c = st.cell(row=7 + i, column=1, value=groups[i] if i < len(groups) else None)
        c.font, c.fill = INPUT, FILL_INPUT
    st.cell(row=7, column=3, value="Type each group name exactly as it appears in Data column C.").font = F
    st.cell(row=14, column=1, value="Worked out from the data").font = H2
    setting(st, 15, "Rows of data", f"=COUNTA(Data!B2:B{last})", "")
    setting(st, 16, "Weeks in the data", f"=IF(COUNT(Data!A2:A{last})=0,0,MAX(Data!A2:A{last})-MIN(Data!A2:A{last})+1)", "Week numbers should run without gaps.")
    setting(st, 17, "Risk scores given", f"=COUNT(Data!G2:G{last})", "0 means no risk score to compare.")

    d = wb.create_sheet("Data")
    head(d, 1, ["Week", "ID", "Group", "On track this week (1/0)", "Visited (1/0)", "On track next week (1/0)",
                "Risk score", "Visit gain (from table)", "Table rule: rank in week", "Table rule: visit",
                "Risk: rank in week", "Risk: visit"])
    for i, w in enumerate([7, 9, 8, 12, 9, 12, 9, 11, 11, 9, 10, 9]):
        d.column_dimensions[col(i + 1)].width = w
    d.freeze_panes = "A2"
    d["A1"].comment = Comment("Week number, 1, 2, 3 ... with no gaps. One row per person per week.", "AI4SG Finder")
    d["G1"].comment = Comment("Optional: higher = more at risk. Leave blank if you don't use one.", "AI4SG Finder")

    npat, weeks, K = 150, 12, 20
    gmap = {f"P{p + 1:03d}": groups[0 if p < 50 else 1 if p < 100 else 2] for p in range(npat)}
    state = {pid: (1 if rng.random() < 0.6 else 0) for pid in gmap}
    r = 2
    for w in range(1, weeks + 1):
        risk = {pid: round(1 - P[gmap[pid]][state[pid]][0] + rng.gauss(0, 0.08), 3) for pid in gmap}
        # current practice: highest risk first, but 1 in 4 visits go to whoever is easiest to reach
        ranked = sorted(gmap, key=lambda pid: -risk[pid])
        visited = set(ranked[:15]) | set(rng.sample(ranked[15:], 5))
        nxt = {}
        for pid in gmap:
            p = P[gmap[pid]][state[pid]][1 if pid in visited else 0]
            nxt[pid] = 1 if rng.random() < p else 0
        for pid in gmap:
            vals = [w, pid, gmap[pid], state[pid], 1 if pid in visited else 0, nxt[pid], risk[pid]]
            for j, v in enumerate(vals):
                c = d.cell(row=r, column=j + 1, value=v)
                c.font, c.fill = INPUT, FILL_INPUT
            r += 1
        state = nxt

    for r in range(2, last + 1):
        B = f"$B{r}"
        f = {
            "H": f'=IF({B}="","",SUMIFS(Table!$I$3:$I$14,Table!$A$3:$A$14,C{r},Table!$B$3:$B$14,D{r}))',
            "I": f'=IF({B}="","",COUNTIFS($A$2:$A${last},A{r},$H$2:$H${last},">"&H{r})+COUNTIFS($A$2:A{r},A{r},$H$2:H{r},H{r}))',
            "J": f'=IF({B}="","",IF(I{r}<=Settings!$B$3,1,0))',
            "K": f'=IF(OR({B}="",G{r}=""),"",COUNTIFS($A$2:$A${last},A{r},$G$2:$G${last},">"&G{r})+COUNTIFS($A$2:A{r},A{r},$G$2:G{r},G{r}))',
            "L": f'=IF(OR({B}="",G{r}=""),"",IF(K{r}<=Settings!$B$3,1,0))',
        }
        for k, v in f.items():
            c = d[f"{k}{r}"]
            c.value, c.fill, c.font = v, FILL_CALC, F
            if k == "H":
                c.number_format = "0.000"

    t = wb.create_sheet("Table")
    t["A1"] = "How often people were on track the next week, with and without a visit"
    t["A1"].font = TITLE
    head(t, 2, ["Group", "On track this week", "Records: visited", "On track next: visited",
                "Records: not visited", "On track next: not visited", "Chance on track: visited",
                "Chance on track: not visited", "Gain from a visit", "Check"])
    for i, w in enumerate([10, 10, 10, 11, 11, 11, 12, 12, 11, 30]):
        t.column_dimensions[col(i + 1)].width = w
    D = lambda c_: f"Data!${c_}$2:${c_}${last}"
    for i in range(12):
        r = 3 + i
        gi, s = i // 2, 1 - (i % 2)
        t.cell(row=r, column=1, value=f'=IF(Settings!$A${7 + gi}="","",Settings!$A${7 + gi})')
        t.cell(row=r, column=2, value=f'=IF(A{r}="","",{s})')
        a = f"$A{r}"
        t.cell(row=r, column=3, value=f'=IF({a}="","",COUNTIFS({D("C")},{a},{D("D")},B{r},{D("E")},1))')
        t.cell(row=r, column=4, value=f'=IF({a}="","",COUNTIFS({D("C")},{a},{D("D")},B{r},{D("E")},1,{D("F")},1))')
        t.cell(row=r, column=5, value=f'=IF({a}="","",COUNTIFS({D("C")},{a},{D("D")},B{r},{D("E")},0))')
        t.cell(row=r, column=6, value=f'=IF({a}="","",COUNTIFS({D("C")},{a},{D("D")},B{r},{D("E")},0,{D("F")},1))')
        t.cell(row=r, column=7, value=f'=IF(OR({a}="",C{r}=0),"",D{r}/C{r})').number_format = PCT
        t.cell(row=r, column=8, value=f'=IF(OR({a}="",E{r}=0),"",F{r}/E{r})').number_format = PCT
        t.cell(row=r, column=9, value=f'=IF({a}="","",IF(OR(C{r}=0,E{r}=0),0,G{r}-H{r}))').number_format = "0.000"
        t.cell(row=r, column=10, value=f'=IF({a}="","",IF(OR(C{r}<Settings!$B$4,E{r}<Settings!$B$4),"Few records: treat with care",""))')
    t.cell(row=16, column=1, value="Gain from a visit = chance on track next week if visited, minus the chance if not. A cell with no records in either column counts as no gain.").font = F

    res = wb.create_sheet("Results")
    res.column_dimensions["A"].width = 36
    for c_ in "BCDEFGH":
        res.column_dimensions[c_].width = 14
    res["A1"] = "Results"
    res["A1"].font = TITLE
    res["A2"] = "Expected extra people on track the next week, using the Table sheet's gains. All figures are formulas."
    res["A2"].font = F
    head(res, 4, ["Rule", "Visits", "Expected extra on track", "Per 100 visits"])
    Hh = D("H")
    rules = [("Current practice", D("E"), "("), ("Table rule", D("J"), "("),
             ("Risk score", D("L"), 'IF(Settings!$B$17=0,"",')]
    for i, (name, rr, guard) in enumerate(rules):
        r = 5 + i
        res.cell(row=r, column=1, value=name).font = BOLD
        res.cell(row=r, column=2, value=f"={guard}COUNTIF({rr},1))")
        res.cell(row=r, column=3, value=f"={guard}SUMIFS({Hh},{rr},1))").number_format = NUM1
        res.cell(row=r, column=4, value=f'=IF(OR(B{r}="",B{r}=0),"",100*C{r}/B{r})').number_format = NUM1
    r = 8
    res.cell(row=r, column=1, value="Random visits (expected)").font = BOLD
    res.cell(row=r, column=2, value="=Settings!$B$3*Settings!$B$16")
    res.cell(row=r, column=3, value=f'=IF(Settings!$B$15=0,"",B{r}*SUM({Hh})/Settings!$B$15)').number_format = NUM1
    res.cell(row=r, column=4, value=f'=IF(OR(C{r}="",B{r}=0),"",100*C{r}/B{r})').number_format = NUM1
    res.cell(row=10, column=1, value="The table rule's gain over current practice, per 100 visits").font = F
    res.cell(row=10, column=2, value='=IF(OR(D5="",D6=""),"",D6-D5)').number_format = NUM1

    head(res, 12, ["Share of visits by group", "Records", "Current practice", "Table rule", "Risk score"])
    for i in range(6):
        r = 13 + i
        res.cell(row=r, column=1, value=f'=IF(Settings!$A${7 + i}="","",Settings!$A${7 + i})')
        a = f"$A{r}"
        res.cell(row=r, column=2, value=f'=IF({a}="","",COUNTIF({D("C")},{a}))')
        res.cell(row=r, column=3, value=f'=IF(OR({a}="",$B$5=0),"",COUNTIFS({D("C")},{a},{D("E")},1)/$B$5)').number_format = PCT
        res.cell(row=r, column=4, value=f'=IF(OR({a}="",$B$6=0),"",COUNTIFS({D("C")},{a},{D("J")},1)/$B$6)').number_format = PCT
        res.cell(row=r, column=5, value=f'=IF(OR({a}="",$B$7="",$B$7=0),"",COUNTIFS({D("C")},{a},{D("L")},1)/$B$7)').number_format = PCT
    res.cell(row=20, column=1, value="A rule that gains most can still send almost no visits to one group. If a group must keep a minimum, set it as a rule for staff and check that the gain holds.").font = F
    for ws in wb.worksheets:
        font_all(ws)
    wb.calculation.fullCalcOnLoad = True   # no cached values: compute on open
    wb.save(path)


# ---------------------------------------------------------------------------
# 3. Waitlist
# ---------------------------------------------------------------------------

def waitlist(path):
    rng = random.Random(5)
    MAXROWS, WEEKS = 500, 52
    last = MAXROWS + 1
    wb = Workbook()
    readme(wb, "Replay kit 3: Waitlist", [
        "For people who arrive over time and wait for a limited number of places each week: counselling, housing repairs, clinic slots, legal aid. It replays your past arrivals week by week under two ordering rules you set, and compares how long people waited, overall, for the most urgent, and by group.",
        "## What you need",
        "One row per applicant, up to 500 rows, sorted by arrival week: an ID, a group (area, language), the week they joined the list (1 to 52), their priority points under your published criteria, and the week they were actually served (blank if still waiting).",
        "## Steps",
        "1. On Settings, enter the places available each week, the number of weeks to replay, and the points that count as urgent.",
        "2. Set the two rules. Each orders the waiting list by (points weight x priority points) + (waiting weight x weeks waited). Rule A's default, points 0 and waiting 1, is first come, first served. Rule B's default, points 1 and waiting 0.25, puts urgent cases first but lets four weeks of waiting count as much as one point, so nobody waits for ever.",
        "3. On Data, replace the sample rows with your records in the yellow columns A to E.",
        "4. Read Results. The Rule A and Rule B sheets show, week by week, who would have been served.",
        "When every place is filled every week, the average wait is the same under any ordering: the same number of people are served each week. What a rule changes is who waits: the urgent, the longest-waiting, one area or another.",
        "## What this replay assumes",
        "The same people arrive in the same weeks whatever the rule, the places each week are fixed, and nobody leaves the list. If many people give up waiting, the longest waits here are too long, and the rule that serves them sooner matters more than the averages show. Ties go to whoever is higher on the list, so sort it by arrival week.",
    ] + COMMON_END)

    st = wb.create_sheet("Settings")
    st.column_dimensions["A"].width = 34
    st.column_dimensions["B"].width = 14
    st.column_dimensions["C"].width = 70
    st["A1"] = "Settings"
    st["A1"].font = TITLE
    setting(st, 3, "Places available each week", 10, "The same every week.")
    setting(st, 4, "Weeks to replay", 26, "Up to 52. Arrivals after this week are left out.")
    setting(st, 5, "Priority points that count as urgent", 4, "Results show waits for applicants with at least this many points.")
    st.cell(row=7, column=1, value="Rule A").font = H2
    setting(st, 8, "Points weight", 0, "Default: first come, first served.")
    setting(st, 9, "Waiting weight (per week)", 1, "")
    st.cell(row=11, column=1, value="Rule B").font = H2
    setting(st, 12, "Points weight", 1, "Default: urgent first, with waiting time counting too.")
    setting(st, 13, "Waiting weight (per week)", 0.25, "")
    st.cell(row=15, column=1, value="Groups (up to six)").font = H2
    for i, g in enumerate(["Town", "Villages", None, None, None, None]):
        c = st.cell(row=16 + i, column=1, value=g)
        c.font, c.fill = INPUT, FILL_INPUT
    st.cell(row=16, column=3, value="Type each group name exactly as it appears in Data column B.").font = F

    d = wb.create_sheet("Data")
    head(d, 1, ["ID", "Group", "Arrival week", "Priority points", "Served week, actual",
                "Weeks waited: now", "Weeks waited: rule A", "Weeks waited: rule B", "In replay (1/0)"])
    for i, w in enumerate([9, 10, 9, 9, 11, 11, 11, 11, 9]):
        d.column_dimensions[col(i + 1)].width = w
    d.freeze_panes = "A2"
    d["E1"].comment = Comment("The week your current practice served them. Leave blank if they were still waiting.", "AI4SG Finder")
    d["D1"].comment = Comment("Points under your published criteria, e.g. 0 to 5. Higher = more urgent.", "AI4SG Finder")

    # sample: ~11.5 arrivals a week for 26 weeks; current practice is first come, first served,
    # except that town applicants who call in are often moved up
    apps = []
    for w in range(1, 27):
        for _ in range(rng.choice([9, 10, 11, 12, 13, 14])):
            g = "Town" if rng.random() < 0.5 else "Villages"
            pts = min(5, max(0, int(rng.gauss(2, 1.4))))
            apps.append([w, g, pts])
    apps = apps[:MAXROWS]
    waiting, served = [], {}
    for w in range(1, 27):
        waiting += [i for i, a in enumerate(apps) if a[0] == w]
        order = sorted(waiting, key=lambda i: (apps[i][0] - (3 if apps[i][1] == "Town" and rng.random() < 0.5 else 0), i))
        for i in order[:10]:
            served[i] = w
        waiting = [i for i in waiting if i not in served]
    for i, (w, g, pts) in enumerate(apps):
        r = i + 2
        for j, v in enumerate([f"A{i + 1:03d}", g, w, pts, served.get(i)]):
            c = d.cell(row=r, column=j + 1, value=v)
            c.font, c.fill = INPUT, FILL_INPUT

    W = "Settings!$B$4"
    for rule, wp, ww in (("Rule A", "Settings!$B$8", "Settings!$B$9"), ("Rule B", "Settings!$B$12", "Settings!$B$13")):
        g = wb.create_sheet(rule)
        g["A1"] = f"{rule}: who is served each week (1 = served that week)"
        g["A1"].font = H2
        head(g, 2, ["ID", "Served week"])
        g.column_dimensions["A"].width = 9
        g.column_dimensions["B"].width = 9
        s0, v0 = 4, 4 + WEEKS + 1          # score grid starts at D; served grid after a gap
        g.cell(row=1, column=s0, value="Score each week (blank = not waiting)").font = BOLD
        g.cell(row=1, column=v0, value="Served (1/0)").font = BOLD
        for k in range(WEEKS):
            for base in (s0, v0):
                c = g.cell(row=2, column=base + k, value=k + 1)
                c.font, c.fill = BOLD, FILL_HEAD
                g.column_dimensions[col(base + k)].width = 5
        g.freeze_panes = "C3"
        for i in range(MAXROWS):
            r, dr = 3 + i, 2 + i
            g.cell(row=r, column=1, value=f'=IF(Data!$A{dr}="","",Data!$A{dr})')
            vfirst, vlast = col(v0), col(v0 + WEEKS - 1)
            g.cell(row=r, column=2,
                   value=f'=IF($A{r}="","",IFERROR(INDEX(${vfirst}$2:${vlast}$2,MATCH(1,{vfirst}{r}:{vlast}{r},0)),""))')
            for k in range(WEEKS):
                wk = f"{col(s0 + k)}$2"
                prior = "0" if k == 0 else f"SUM(${vfirst}{r}:{col(v0 + k - 1)}{r})"
                sc = g.cell(row=r, column=s0 + k)
                sc.value = (f'=IF(OR($A{r}="",Data!$C{dr}>{wk},{wk}>{W},{prior}>0),"",'
                            f'{wp}*Data!$D{dr}+{ww}*({wk}-Data!$C{dr})-ROW()/1000000)')
                scol = col(s0 + k)
                vc = g.cell(row=r, column=v0 + k)
                vc.value = (f'=IF({scol}{r}="",0,IF(COUNTIF({scol}$3:{scol}${MAXROWS + 2},">"&{scol}{r})'
                            f'<Settings!$B$3,1,0))')
            for cc in range(1, v0 + WEEKS):
                g.cell(row=r, column=cc).font = F

    for r in range(2, last + 1):
        A, C = f"$A{r}", f"$C{r}"
        f = {
            "I": f'=IF({A}="","",IF({C}<={W},1,0))',
            "F": f'=IF(OR({A}="",I{r}<>1),"",IF(OR(E{r}="",E{r}>{W}),{W}+1-{C},E{r}-{C}))',
            "G": f"=IF(OR({A}=\"\",I{r}<>1),\"\",IF('Rule A'!$B{r + 1}=\"\",{W}+1-{C},'Rule A'!$B{r + 1}-{C}))",
            "H": f"=IF(OR({A}=\"\",I{r}<>1),\"\",IF('Rule B'!$B{r + 1}=\"\",{W}+1-{C},'Rule B'!$B{r + 1}-{C}))",
        }
        for k, v in f.items():
            c = d[f"{k}{r}"]
            c.value, c.fill, c.font = v, FILL_CALC, F

    res = wb.create_sheet("Results")
    res.column_dimensions["A"].width = 44
    for c_ in "BCD":
        res.column_dimensions[c_].width = 16
    res["A1"] = "Results"
    res["A1"].font = TITLE
    res["A2"] = ("Weeks waited = week served minus week joined. For anyone still waiting at the end, it counts the weeks "
                 "waited so far, so a rule can't look good by leaving people on the list.")
    res["A2"].font, res["A2"].alignment = F, WRAP
    res.row_dimensions[2].height = 28
    head(res, 4, ["", "Current practice", "Rule A", "Rule B"])
    rng_ = {"B": f"Data!$F$2:$F${last}", "C": f"Data!$G$2:$G${last}", "D": f"Data!$H$2:$H${last}"}
    inrep = f"Data!$I$2:$I${last}"
    pts = f"Data!$D$2:$D${last}"
    grp = f"Data!$B$2:$B${last}"
    servedcol = {"B": f"Data!$E$2:$E${last}", "C": f"'Rule A'!$B$3:$B${MAXROWS + 2}", "D": f"'Rule B'!$B$3:$B${MAXROWS + 2}"}
    lines = [
        ("Applicants in the replay", lambda c_: f"=COUNTIF({inrep},1)", "0"),
        ("Served by the end", None, "0"),
        ("Still waiting at the end", lambda c_: f"={c_}5-{c_}6", "0"),
        ("Average weeks waited", lambda c_: f'=IFERROR(AVERAGEIFS({rng_[c_]},{inrep},1),"")', NUM1),
        ("Average weeks waited: urgent", lambda c_: f'=IFERROR(AVERAGEIFS({rng_[c_]},{inrep},1,{pts},">="&Settings!$B$5),"")', NUM1),
        ("Average weeks waited: everyone else", lambda c_: f'=IFERROR(AVERAGEIFS({rng_[c_]},{inrep},1,{pts},"<"&Settings!$B$5),"")', NUM1),
        ("Longest wait (weeks)", lambda c_: f"=MAX({rng_[c_]})", "0"),
        ("Waited more than 8 weeks", lambda c_: f'=COUNTIFS({inrep},1,{rng_[c_]},">8")', "0"),
    ]
    for i, (label, fn, fmt) in enumerate(lines):
        r = 5 + i
        res.cell(row=r, column=1, value=label).font = BOLD if i in (3, 4) else F
        for c_ in "BCD":
            if label == "Served by the end":
                if c_ == "B":
                    v = f'=COUNTIFS({inrep},1,{servedcol["B"]},"<="&{W})'
                else:
                    v = f'=COUNTIF({servedcol[c_]},"<="&{W})'
            else:
                v = fn(c_)
            cell = res[f"{c_}{r}"]
            cell.value, cell.number_format = v, fmt
    head(res, 14, ["Average weeks waited, by group", "Current practice", "Rule A", "Rule B"])
    for i in range(6):
        r = 15 + i
        res.cell(row=r, column=1, value=f'=IF(Settings!$A${16 + i}="","",Settings!$A${16 + i})')
        for c_ in "BCD":
            res[f"{c_}{r}"] = f'=IF($A{r}="","",IFERROR(AVERAGEIFS({rng_[c_]},{inrep},1,{grp},$A{r}),""))'
            res[f"{c_}{r}"].number_format = NUM1
    res.cell(row=22, column=1, value="When every place is filled each week, every ordering gives the same average wait: the rules differ in who waits. Compare the urgent, the longest waits and the groups, not the average.").font = F
    for ws in wb.worksheets:
        font_all(ws)
    wb.calculation.fullCalcOnLoad = True   # no cached values: compute on open
    wb.save(path)


# ---------------------------------------------------------------------------
# 4. Monthly health check, after launch
# ---------------------------------------------------------------------------

def health_check(path, report_month=11):
    import datetime as dt
    from openpyxl.formatting.rule import CellIsRule
    rng = random.Random(3)
    MAXROWS = 20000
    last = MAXROWS + 1
    NM = 12
    months = [dt.date(2026, m, 1) for m in range(1, 13)]
    groups = ["North", "Central", "South"]
    wb = Workbook()
    readme(wb, "Health check: is the tool still working? (monthly)", [
        "For a program already using a model, a score or a ranked list to choose whom to serve: inspections, outreach, visits, referrals. Each month, paste in the month's records and read one page: whether staff follow the list, whether its picks still do better than a random share, whether its scores still match what happens, and how each group fares. It pairs the playbook's fairness audit with a check that the tool is still worth using.",
        "## What you need",
        "One row per person, home or site considered each month, up to 20,000 rows in all: the month, an ID, a group, whether the tool picked them, whether they were served, whether they were served as part of a random share, the tool's score if it gives one, the outcome once known, and whether a simple rule would have picked them.",
        "The random share is the key column. Each month, serve a small number (one in ten, say) chosen at random from those the tool did not pick, and mark them 1. Without it, nobody can tell whether the tool's picks do better than chance, or what it misses.",
        "Use \"outcome\" for what the program looks for: a hazard found, a need confirmed, a missed appointment prevented. Leave it blank until it is known.",
        "## Steps",
        "1. On Settings, check the thresholds, list the months (the first day of each month) and the groups.",
        "2. Each month, add that month's rows to Data, columns A to I.",
        "3. On Settings, set the month to report: the latest month whose outcomes are mostly in.",
        "4. Read Report. Anything marked Check needs a conversation, not an automatic change. Monthly shows each measure month by month.",
        "## Reading the checks",
        "Hit rates and calibration pool the last three months (fewer at the start), because a month's random share is small, and they are left blank until there are enough outcomes to judge. A score is calibrated when, among people given a 30% chance, about 30% turn out to have the outcome; the check compares the average score of those served with the share who had the outcome. A group gap compares a group's share of those served with its share of those considered: a gap can be right when need differs, but it should be a decision, not a drift.",
        "A report like this one can go to a funder or a board as it is. It describes the tool, not the staff: overrides are information about where the tool is wrong or unworkable.",
    ] + COMMON_END[2:])

    st = wb.create_sheet("Settings")
    st.column_dimensions["A"].width = 50
    st.column_dimensions["B"].width = 14
    st.column_dimensions["C"].width = 70
    st["A1"] = "Settings"
    st["A1"].font = TITLE
    setting(st, 3, "Month to report", months[report_month - 1], "The latest month whose outcomes are mostly in. Must be one of the months listed below.", "mmm yyyy")
    st.cell(row=5, column=1, value="Thresholds: a value past these is marked Check").font = H2
    TH = {}
    for i, (key, label, val, fmt, note) in enumerate([
        ("follow", "Share of the tool's picks served, at least", 0.80, PCT, "Lower means staff often skip the list. Ask why."),
        ("over", "Share of those served who were overrides, at most", 0.20, PCT, "Served though the tool didn't pick them and not in the random share."),
        ("rand", "Random share of those served, at least", 0.05, PCT, "Too small a random share means the hit-rate check can't be read."),
        ("lead", "Tool's hit rate above the random share's, at least (points)", 0.05, PCT, "Over the last three months."),
        ("cal", "Gap between average score and outcome rate, at most (points)", 0.05, PCT, "Over the last three months, overall and for each group."),
        ("gap", "Gap between a group's share served and share considered, at most (points)", 0.10, PCT, ""),
        ("rec", "Share of those served with an outcome recorded, at least", 0.80, PCT, "If this month's outcomes are still coming in, report an earlier month."),
        ("chg", "Change in records from the month before, at most", 0.25, PCT, "A sudden change often means a recording problem."),
        ("ovl", "Overlap with the simple rule that suggests checking the tool's cost", 0.90, PCT, "If a simple rule picks almost the same people, is the tool worth its cost?"),
        ("minn", "Outcomes needed before a hit rate or calibration is judged", 30, "0", "Over the last three months: for the random share, and for each group's calibration."),
    ]):
        r = 6 + i
        setting(st, r, label, val, note, fmt)
        TH[key] = f"Settings!$B${r}"
    st.cell(row=17, column=1, value="Months (first day of each month)").font = H2
    for i in range(NM):
        c = st.cell(row=18 + i, column=1, value=months[i])
        c.font, c.fill, c.number_format = INPUT, FILL_INPUT, "mmm yyyy"
    st.cell(row=31, column=1, value="Groups (up to six)").font = H2
    for i in range(6):
        c = st.cell(row=32 + i, column=1, value=groups[i] if i < len(groups) else None)
        c.font, c.fill = INPUT, FILL_INPUT
    st.cell(row=32, column=3, value="Type each group name exactly as it appears in Data column C.").font = F

    d = wb.create_sheet("Data")
    head(d, 1, ["Month", "ID", "Group", "Picked by the tool (1/0)", "Served (1/0)", "Random share (1/0)",
                "Score (0-1)", "Outcome (1/0)", "Simple rule would pick (1/0)"])
    for i, w in enumerate([11, 10, 10, 11, 9, 10, 9, 10, 12]):
        d.column_dimensions[col(i + 1)].width = w
    d.freeze_panes = "A2"
    d["A1"].comment = Comment("The first day of the month, e.g. 1 March 2026. One row per person, home or site considered that month.", "AI4SG Finder")
    d["F1"].comment = Comment("1 if served as part of a random share chosen from those the tool did NOT pick; else 0 or blank.", "AI4SG Finder")
    d["G1"].comment = Comment("Optional: the tool's predicted chance of the outcome, between 0 and 1.", "AI4SG Finder")
    d["H1"].comment = Comment("1 if the outcome happened (hazard found, need confirmed), 0 if not. Blank until known; usually known only for those served.", "AI4SG Finder")
    d["I1"].comment = Comment("Optional: 1 if a simple rule (e.g. oldest homes first) would have picked them.", "AI4SG Finder")

    # sample: a home-inspection program, 400 homes considered a month, 50 picked, 12 random checks.
    # From August a new hazard source, mostly in the South, appears that the model never saw.
    # From October staff who know about it set aside about a third of the list for South homes.
    homes = []
    for h in range(1200):
        g = groups[0] if h < 480 else groups[1] if h < 900 else groups[2]
        age = rng.random()
        newsrc = 1 if (g == "South" and rng.random() < 0.5) or rng.random() < 0.1 else 0
        homes.append((f"H{h + 1:04d}", g, age, newsrc))
    r = 2
    for mi, m in enumerate(months):
        pool = rng.sample(homes, 400)
        rows_ = []
        for hid, g, age, newsrc in pool:
            base = 0.04 + 0.5 * age ** 2 + (0.06 if g == "North" else 0)
            p = base + (0.30 * newsrc if mi >= 7 else 0)
            score = min(0.95, max(0.01, base + rng.gauss(0, 0.04)))
            rows_.append([m, hid, g, score, p, age, newsrc])
        order = sorted(range(400), key=lambda i: -rows_[i][3])
        picked = set(order[:50])
        simple = set(sorted(range(400), key=lambda i: -rows_[i][5])[:50])
        served = set()
        for i in picked:
            skip = 0.33 if mi >= 9 else 0.04
            if rng.random() >= skip:
                served.add(i)
        others = [i for i in range(400) if i not in picked]
        rand = set(rng.sample(others, 12))
        rest = [i for i in others if i not in rand]
        if mi >= 9:   # staff pick South homes they know have the new hazard source
            local = [i for i in rest if rows_[i][2] == "South" and rows_[i][6] == 1]
            rng.shuffle(local)
            rest = local + [i for i in rest if i not in set(local)]
            over = set(rest[:50 - len(served)])
        else:
            over = set(rng.sample(rest, 50 - len(served)))
        served |= rand | over
        for i, (m_, hid, g, score, p, age, _src) in enumerate(rows_):
            known = 0.95 if mi < 11 else 0.55
            out = (1 if rng.random() < p else 0) if (i in served and rng.random() < known) else None
            vals = [m_, hid, g, 1 if i in picked else 0, 1 if i in served else 0, 1 if i in rand else 0,
                    round(score, 3), out, 1 if i in simple else 0]
            for j, v in enumerate(vals):
                c = d.cell(row=r, column=j + 1, value=v)
                c.font, c.fill = INPUT, FILL_INPUT
                if j == 0:
                    c.number_format = "mmm yyyy"
            r += 1

    R = lambda c_: f"Data!${c_}$2:${c_}${last}"
    A, C_, D_, E, F_, G_, H, I_ = (R(x) for x in "ACDEFGHI")

    mo = wb.create_sheet("Monthly")
    mo.column_dimensions["A"].width = 52
    mo["A1"] = "Month by month"
    mo["A1"].font = TITLE
    mo.cell(row=3, column=1, value="Month").font = BOLD
    for k in range(NM):
        c = mo.cell(row=3, column=2 + k, value=f'=IF(Settings!$A${18 + k}="","",Settings!$A${18 + k})')
        c.font, c.fill, c.number_format = BOLD, FILL_HEAD, "mmm yyyy"
        mo.column_dimensions[col(2 + k)].width = 10
    mo.cell(row=3, column=1).fill = FILL_HEAD
    ROW = {}
    spec = [
        ("h", "Records"),
        ("cons", "Considered", lambda m: f"COUNTIFS({A},{m})", "0"),
        ("picked", "Picked by the tool", lambda m: f"COUNTIFS({A},{m},{D_},1)", "0"),
        ("served", "Served", lambda m: f"COUNTIFS({A},{m},{E},1)", "0"),
        ("chg", "Change in records from the month before", None, PCT),
        ("scoremiss", "Considered with no score", lambda m: f'IF(COUNTIFS({A},{m},{G_},"<>")=0,"",1-COUNTIFS({A},{m},{G_},"<>")/MAX(1,COUNTIFS({A},{m})))', PCT),
        ("h", "Following the list"),
        ("pserved", "Tool's picks served", lambda m: f"COUNTIFS({A},{m},{D_},1,{E},1)", "0"),
        ("follow", "Share of the tool's picks served", "rate:pserved/picked", PCT),
        ("over_n", "Overrides (served, not picked, not random)", lambda m: f'COUNTIFS({A},{m},{E},1,{D_},0,{F_},"<>1")', "0"),
        ("over", "Overrides as a share of those served", "rate:over_n/served", PCT),
        ("rand_n", "Served in the random share", lambda m: f"COUNTIFS({A},{m},{E},1,{F_},1)", "0"),
        ("rand", "Random share of those served", "rate:rand_n/served", PCT),
        ("h", "Results"),
        ("known", "Served with an outcome recorded", lambda m: f'COUNTIFS({A},{m},{E},1,{H},"<>")', "0"),
        ("rec", "Share of those served with an outcome recorded", "rate:known/served", PCT),
        ("tk", "Tool's picks with an outcome", lambda m: f'COUNTIFS({A},{m},{D_},1,{E},1,{H},"<>")', "0"),
        ("th", "Tool's picks with the outcome (hits)", lambda m: f"COUNTIFS({A},{m},{D_},1,{E},1,{H},1)", "0"),
        ("thit", "Hit rate: tool's picks", "rate:th/tk", PCT),
        ("rk", "Random share with an outcome", lambda m: f'COUNTIFS({A},{m},{F_},1,{E},1,{H},"<>")', "0"),
        ("rh", "Random share with the outcome (hits)", lambda m: f"COUNTIFS({A},{m},{F_},1,{E},1,{H},1)", "0"),
        ("rhit", "Hit rate: random share", "rate:rh/rk", PCT),
        ("h", "Calibration (served, with a score and an outcome)"),
        ("cn", "Records", lambda m: f'COUNTIFS({A},{m},{E},1,{H},"<>",{G_},"<>")', "0"),
        ("cs", "Sum of scores", lambda m: f'SUMIFS({G_},{A},{m},{E},1,{H},"<>",{G_},"<>")', NUM2),
        ("ch", "Outcomes", lambda m: f'COUNTIFS({A},{m},{E},1,{H},1,{G_},"<>")', "0"),
        ("cscore", "Average score", "rate:cs/cn", PCT),
        ("cobs", "Outcome rate", "rate:ch/cn", PCT),
        ("h", "Simple rule"),
        ("both", "Tool's picks the simple rule would also pick", lambda m: f'IF(COUNT({I_})=0,"",COUNTIFS({A},{m},{D_},1,{I_},1))', "0"),
        ("ovl", "Overlap with the simple rule", "rate:both/picked", PCT),
    ]
    r = 4
    for item in spec:
        if item[0] == "h":
            r += 1
            mo.cell(row=r, column=1, value=item[1]).font = H2
            r += 1
            continue
        key, label, fn, fmt = item
        ROW[key] = r
        mo.cell(row=r, column=1, value=label).font = F
        r += 1
    for item in spec:
        if item[0] == "h":
            continue
        key, label, fn, fmt = item
        rr = ROW[key]
        for k in range(NM):
            m = f"{col(2 + k)}$3"
            cc = col(2 + k)
            if key == "chg":
                v = '=""' if k == 0 else f'=IF(OR({m}="",{col(1 + k)}{ROW["cons"]}="",{col(1 + k)}{ROW["cons"]}=0),"",{cc}{ROW["cons"]}/{col(1 + k)}{ROW["cons"]}-1)'
            elif isinstance(fn, str):
                a, b = fn[5:].split("/")
                v = f'=IF(OR({m}="",{cc}{ROW[b]}="",{cc}{ROW[b]}=0),"",{cc}{ROW[a]}/{cc}{ROW[b]})'
            else:
                v = f'=IF({m}="","",{fn(m)})'
            c = mo.cell(row=rr, column=2 + k, value=v if v else None)
            c.number_format, c.fill = fmt, FILL_CALC
    # groups
    r += 1
    mo.cell(row=r, column=1, value="By group").font = H2
    r += 1
    GROW = []
    for gi in range(6):
        g = f"Settings!$A${32 + gi}"
        base = r
        labels = ["share of those considered", "share of those served", "gap (served minus considered)",
                  "calibration records", "sum of scores", "outcomes"]
        for j, lab in enumerate(labels):
            mo.cell(row=base + j, column=1, value=f'=IF({g}="","",{g}&": {lab}")').font = F
        for k in range(NM):
            m = f"{col(2 + k)}$3"
            cc = col(2 + k)
            fs = [
                f'=IF(OR({m}="",{g}="",{cc}${ROW["cons"]}=0),"",COUNTIFS({A},{m},{C_},{g})/{cc}${ROW["cons"]})',
                f'=IF(OR({m}="",{g}="",{cc}${ROW["served"]}=0),"",COUNTIFS({A},{m},{C_},{g},{E},1)/{cc}${ROW["served"]})',
                f'=IF(OR({cc}{base}="",{cc}{base + 1}=""),"",{cc}{base + 1}-{cc}{base})',
                f'=IF(OR({m}="",{g}=""),"",COUNTIFS({A},{m},{C_},{g},{E},1,{H},"<>",{G_},"<>"))',
                f'=IF(OR({m}="",{g}=""),"",SUMIFS({G_},{A},{m},{C_},{g},{E},1,{H},"<>",{G_},"<>"))',
                f'=IF(OR({m}="",{g}=""),"",COUNTIFS({A},{m},{C_},{g},{E},1,{H},1,{G_},"<>"))',
            ]
            for j, v in enumerate(fs):
                c = mo.cell(row=base + j, column=2 + k, value=v)
                c.fill = FILL_CALC
                c.number_format = PCT if j < 3 else (NUM2 if j == 4 else "0")
        GROW.append(base)
        r = base + 7
    mo.freeze_panes = "B4"

    # ---- Report
    rp = wb.create_sheet("Report")
    rp.column_dimensions["A"].width = 44
    rp.column_dimensions["B"].width = 14
    rp.column_dimensions["C"].width = 12
    rp.column_dimensions["D"].width = 15
    rp.column_dimensions["E"].width = 70
    rp["A1"] = "Health check"
    rp["A1"].font = TITLE
    rp["A2"] = "Month reported"
    rp["A2"].font = BOLD
    rp["B2"] = "=Settings!$B$3"
    rp["B2"].number_format = "mmm yyyy"
    rp["C2"] = '=IFERROR(MATCH(Settings!$B$3,Monthly!$B$3:$M$3,0),"")'
    rp["C2"].number_format = "0"
    rp["D2"] = '=IF(C2="","The month to report isn\'t in the months list on Settings.","")'
    K = "$C$2"

    def cur(key):
        return f"INDEX(Monthly!$B${ROW[key]}:$M${ROW[key]},{K})"

    def pool(key):
        rr = ROW[key]
        return f"SUM(INDEX(Monthly!$B${rr}:$M${rr},MAX(1,{K}-2)):INDEX(Monthly!$B${rr}:$M${rr},{K}))"

    head(rp, 4, ["Check", "Value", "Threshold", "Status", "What to do if it says Check"])
    checks = [
        ("Records considered this month", f'={cur("cons")}', None, '=""', "", "0"),
        ("Change from the month before", f'={cur("chg")}', TH["chg"], f'=IF(B6="","",IF(ABS(B6)>C6,"Check","OK"))',
         "Find out whether the program changed or the recording did before reading anything else.", PCT),
        ("Share of the tool's picks served", f'={cur("follow")}', TH["follow"], f'=IF(B7="","",IF(B7<C7,"Check","OK"))',
         "Ask staff which picks they skip and why: unreachable, unsafe, already served, or a list that looks wrong.", PCT),
        ("Overrides as a share of those served", f'={cur("over")}', TH["over"], f'=IF(B8="","",IF(B8>C8,"Check","OK"))',
         "Review a sample of overrides. Many overrides in one area or for one reason point to a gap in the tool.", PCT),
        ("Random share of those served", f'={cur("rand")}', TH["rand"], f'=IF(B9="","",IF(B9<C9,"Check","OK"))',
         "Restore the random share: without it the hit-rate check below can't be trusted.", PCT),
        ("Outcomes recorded for those served", f'={cur("rec")}', TH["rec"], f'=IF(B10="","",IF(B10<C10,"Check","OK"))',
         "If results are still coming in, report an earlier month. Otherwise fix the recording first.", PCT),
        ("Hit rate, tool's picks (up to 3 months)", f'=IF({pool("tk")}=0,"",{pool("th")}/{pool("tk")})', None, '=""', "", PCT),
        ("Hit rate, random share (up to 3 months)", f'=IF({pool("rk")}=0,"",{pool("rh")}/{pool("rk")})', None, '=""', "", PCT),
        ("Tool's lead over the random share", '=IF(OR(B11="",B12=""),"",B11-B12)', TH["lead"],
         f'=IF({K}="","",IFERROR(IF({pool("rk")}<{TH["minn"]},"Too few to tell",IF(B13="","",IF(B13<C13,"Check","OK"))),""))',
         "The tool's picks no longer find much more than chance. Ask a partner to recheck the model on recent records; meanwhile compare with the simple rule.", PCT),
        ("Average score minus outcome rate (up to 3 months)", f'=IF({pool("cn")}<{TH["minn"]},"",({pool("cs")}-{pool("ch")})/{pool("cn")})', TH["cal"],
         f'=IF(B14="","",IF(ABS(B14)>C14,"Check","OK"))',
         "Positive: the score expects more than happens; negative: less. Either way the model needs recalibrating on recent records.", PCT),
        ("Largest group gap this month (points)", "=IF(COUNT(D23:D28)=0,\"\",MAX(MAX(D23:D28),-MIN(D23:D28)))", TH["gap"],
         f'=IF(B15="","",IF(B15>C15,"Check","OK"))',
         "See the table below. Decide whether the difference is justified by need; if not, set a minimum per group.", PCT),
        ("Largest group calibration gap (up to 3 months)", "=IF(COUNT(E23:E28)=0,\"\",MAX(MAX(E23:E28),-MIN(E23:E28)))", TH["cal"],
         f'=IF(B16="","",IF(B16>C16,"Check","OK"))',
         "A score that under-predicts for one group sends it fewer slots: step 2 of the playbook's fairness audit.", PCT),
        ("Overlap with the simple rule", f'={cur("ovl")}', TH["ovl"], f'=IF(B17="","",IF(B17>=C17,"Note","OK"))',
         "The simple rule picks almost the same. Weigh what the tool costs each month against what it adds.", PCT),
        ("Considered with no score", f'={cur("scoremiss")}', None, '=""', "", PCT),
    ]
    for i, (label, val, th, status, todo, fmt) in enumerate(checks):
        r = 5 + i
        rp.cell(row=r, column=1, value=label).font = F
        rp.cell(row=r, column=2, value=f'=IF({K}="","",IFERROR({val[1:]},""))').number_format = fmt
        if th:
            c = rp.cell(row=r, column=3, value=f"={th}")
            c.number_format = "0" if th == TH["minn"] else PCT
        rp.cell(row=r, column=4, value=status).font = BOLD
        c = rp.cell(row=r, column=5, value=todo)
        c.font, c.alignment = F, WRAP
    rp.conditional_formatting.add("D5:D18", CellIsRule(operator="equal", formula=['"Check"'],
                                  fill=PatternFill("solid", fgColor="F8CBAD")))
    rp.conditional_formatting.add("D5:D18", CellIsRule(operator="equal", formula=['"OK"'],
                                  fill=PatternFill("solid", fgColor="C6EFCE")))
    rp.cell(row=19, column=1, value="Random-share outcomes, last 3 months").font = F
    rp.cell(row=19, column=2, value=f'=IF({K}="","",{pool("rk")})').number_format = "0"

    head(rp, 22, ["Group", "Share considered", "Share served", "Gap (points)", "Score minus outcome rate (3 months; blank if too few)"])
    for gi in range(6):
        r = 23 + gi
        b = GROW[gi]
        rp.cell(row=r, column=1, value=f'=IF(Settings!$A${32 + gi}="","",Settings!$A${32 + gi})')
        for j, cc in enumerate("BCD"):
            rp[f"{cc}{r}"] = f'=IF(OR($A{r}="",{K}=""),"",IFERROR(INDEX(Monthly!$B${b + j}:$M${b + j},{K}),""))'
            rp[f"{cc}{r}"].number_format = PCT
        pn = lambda rr: f"SUM(INDEX(Monthly!$B${rr}:$M${rr},MAX(1,{K}-2)):INDEX(Monthly!$B${rr}:$M${rr},{K}))"
        rp[f"E{r}"] = f'=IF(OR($A{r}="",{K}=""),"",IF({pn(b + 3)}<{TH["minn"]},"",({pn(b + 4)}-{pn(b + 5)})/{pn(b + 3)}))'
        rp[f"E{r}"].number_format = PCT
    rp.cell(row=30, column=1, value="Check means look and talk, not change the tool automatically. Keep each month's report: the trend is the point.").font = F
    rp.freeze_panes = "A5"
    wb.move_sheet("Report", offset=-(len(wb.sheetnames) - 2))
    for ws in wb.worksheets:
        font_all(ws)
    wb.calculation.fullCalcOnLoad = True
    wb.save(path)


# ---------------------------------------------------------------------------
# 5. Cost of ownership: the model against the simple rule
# ---------------------------------------------------------------------------

def cost_of_ownership(path):
    wb = Workbook()
    readme(wb, "Cost of ownership: what the model costs against the simple rule", [
        "The replay workbooks show how many more people a model reaches than a simple rule. This one adds up what each costs to set up and run, so you can see the cost of each extra person reached, and what you still need to find out.",
        "It is a checklist as much as a calculator. Every line is something that costs money or staff time; a blank line is something you haven't found out yet, and the Summary counts them. Type 0 when a line truly costs nothing.",
        "## Steps",
        "1. On Settings, enter your currency, the cost of an hour of staff time, the number of years to compare, how many rounds (weeks, months) a year the decision is made, and a contingency.",
        "2. On Costs, for each line, enter money and staff hours for the simple rule and for the model. The \"How to find it\" column says whom to ask. Partners' quotes go in money; your own staff's time goes in hours. Volunteer time is worth recording as hours too: it ends.",
        "3. On Settings, enter how many more people a year the model reaches than the simple rule, from the replay kit or a partner's test, and your current cost per person served.",
        "4. Read Summary: total cost of each over the period, the model's extra cost, the cost of each extra person it reaches, and how many lines are still blank.",
        "## Reading it",
        "If each extra person the model reaches costs many times what the program spends per person today, the simple rule is likely the better use of the money, unless those extra people are the ones who matter most. If the model's lines are mostly blank, the honest answer is that its cost isn't known yet: find out before deciding.",
        "No figure here comes from AI4SG Finder. Ask the partners and programs listed in the playbook's Follow-up 4 and 5 what their setups took.",
    ] + COMMON_END[2:])

    st = wb.create_sheet("Settings")
    st.column_dimensions["A"].width = 52
    st.column_dimensions["B"].width = 14
    st.column_dimensions["C"].width = 70
    st["A1"] = "Settings"
    st["A1"].font = TITLE
    setting(st, 3, "Currency", "USD", "Shown in the Summary headings.")
    setting(st, 4, "Cost of one hour of staff time", 15, "Salary and overheads divided by working hours. Use one average figure.", "#,##0.00")
    setting(st, 5, "Years to compare", 3, "Three is usual: long enough for running costs to show.")
    setting(st, 6, "Rounds a year", 52, "How often the decision is made: 52 for weekly, 12 for monthly, 1 for once a year.")
    setting(st, 7, "Contingency", 0.15, "Added to both totals for what goes wrong.", PCT)
    st.cell(row=9, column=1, value="What the model adds").font = H2
    setting(st, 10, "Extra people reached a year: model over simple rule", 15, "From the replay kit (Results) or a partner's test on past records. Leave blank if unknown.", "#,##0")
    setting(st, 11, "Extra people reached a year: simple rule over current practice", 60, "Optional, for comparison.", "#,##0")
    setting(st, 12, "Current cost per person served a year", 120, "What the program spends now for each person it serves. Optional.", "#,##0")

    c = wb.create_sheet("Costs")
    head(c, 1, ["Group", "Line", "When", "How to find it", "Simple rule: money", "Simple rule: staff hours",
                "Model: money", "Model: staff hours", "Simple rule: total", "Model: total",
                "Simple rule: costed?", "Model: costed?"])
    for i, w in enumerate([13, 40, 10, 52, 12, 12, 12, 12, 13, 13, 13, 13]):
        c.column_dimensions[col(i + 1)].width = w
    c.freeze_panes = "C2"
    c["E1"].comment = Comment("Money for each time the line occurs: once, each round or each year (see When).", "AI4SG Finder")
    c["F1"].comment = Comment("Staff hours for each time the line occurs. Blank = not found out yet; 0 = costs nothing.", "AI4SG Finder")
    lines = [
        ("One-off", "Gather, clean and link the data", "One-off", "Ask the builder how many days the data will take; count your own staff's hours pulling records", "", 40, 5000, 120),
        ("One-off", "Build the rule or model", "One-off", "A partner's written quote; for a volunteer, their estimate of hours", "", 16, 25000, 80),
        ("One-off", "Test on past records", "One-off", "The replay kit takes staff a day or two; a partner's replay is part of their quote", "", 16, 2000, 16),
        ("One-off", "Connect it to the forms or systems staff use", "One-off", "Whoever maintains your forms, app or database", 0, 0, 3000, 24),
        ("One-off", "Train staff", "One-off", "Number of staff x hours of training, plus the trainer", "", 8, "", 16),
        ("One-off", "Consent and legal review", "One-off", "Your data-protection lead or legal adviser", "", 8, 1000, 16),
        ("One-off", "Explain it to the community", "One-off", "Meetings or materials planned with community representatives", "", 8, "", ""),
        ("One-off", "Fairness audit, if it ranks people", "One-off", "Playbook Follow-up 2: a partner or an analyst with group-level data", 0, 0, 1500, 16),
        ("One-off", "Run the old process alongside during the pilot", "One-off", "Staff time to keep the old list going for the pilot's length", 0, 0, "", 80),
        ("Each round", "Enter the data", "Per round", "Time a round's data entry now; ask whether the model needs more fields", "", 2, "", 2),
        ("Each round", "Run it and check the output", "Per round", "Time a dry run; ask the builder", "", 0.5, "", 0.25),
        ("Each round", "Act on the list (extra time compared with today)", "Per round", "Field supervisors: does the new list mean more travel or longer visits?", 0, 0, 0, 0),
        ("Each year", "Hosting or software", "Per year", "The builder; free tools often need paid hosting", 0, 0, 1200, 0),
        ("Each year", "Maintenance and fixes", "Per year", "A partner's support quote, or a named person's hours", "", 8, 8000, 8),
        ("Each year", "Recalibrate on new records", "Per year", "The builder: how often, and how long each time", "", 8, "", 40),
        ("Each year", "Monthly health check and yearly fairness recheck", "Per year", "The replay kit's health check takes an hour or two a month", "", 24, "", 24),
        ("Often missed", "Cover when a volunteer or partner leaves", "Per year", "What it would cost to hire someone to take it over", 0, 0, "", ""),
        ("Often missed", "Managers' time to approve and explain it", "Per year", "Hours a year for reviews, complaints, board and funder questions", "", 12, "", 24),
    ]
    first = 2
    for i, (grp, line, when, how, sm, sh, mm, mh) in enumerate(lines):
        r = first + i
        for j, v in enumerate([grp, line, when, how]):
            cc = c.cell(row=r, column=j + 1, value=v)
            cc.font, cc.alignment = F, WRAP
        for j, v in enumerate([sm, sh, mm, mh]):
            cc = c.cell(row=r, column=5 + j, value=None if v == "" else v)
            cc.font, cc.fill = INPUT, FILL_INPUT
            cc.number_format = "#,##0.##"
        mult = f'IF(C{r}="One-off",1,IF(C{r}="Per year",Settings!$B$5,Settings!$B$5*Settings!$B$6))'
        for j, (m_, h_) in enumerate((("E", "F"), ("G", "H"))):
            cc = c.cell(row=r, column=9 + j, value=f"=(N({m_}{r})+N({h_}{r})*Settings!$B$4)*{mult}")
            cc.fill, cc.font, cc.number_format = FILL_CALC, F, "#,##0"
            cc = c.cell(row=r, column=11 + j, value=f'=IF(AND({m_}{r}="",{h_}{r}=""),"Find out","Yes")')
            cc.fill, cc.font = FILL_CALC, F
    lastr = first + len(lines) - 1
    n = len(lines)
    c.cell(row=lastr + 2, column=2, value="Add lines above this row if you need them, copying the grey formulas.").font = F
    c.conditional_formatting.add(f"K{first}:L{lastr}", CellIsRule(operator="equal", formula=['"Find out"'],
                                 fill=PatternFill("solid", fgColor="F8CBAD")))

    sm = wb.create_sheet("Summary")
    sm.column_dimensions["A"].width = 56
    sm.column_dimensions["B"].width = 16
    sm.column_dimensions["C"].width = 16
    sm["A1"] = "Summary"
    sm["A1"].font = TITLE
    sm["A2"] = '="Over "&Settings!$B$5&" years, in "&Settings!$B$3&". The sample figures are made up."'
    sm["A2"].font = F
    head(sm, 4, ["", "Simple rule", "Model"])
    I_, J_ = f"Costs!$I${first}:$I${lastr}", f"Costs!$J${first}:$J${lastr}"
    oneoff = lambda rng_: f'SUMIFS({rng_},Costs!$C${first}:$C${lastr},"One-off")'
    rows = [
        ("Set-up (one-off)", oneoff(I_), oneoff(J_), "#,##0"),
        ("Running, over the whole period", f"SUM({I_})-B5", f"SUM({J_})-C5", "#,##0"),
        ("Contingency", "(B5+B6)*Settings!$B$7", "(C5+C6)*Settings!$B$7", "#,##0"),
        ("Total cost", "B5+B6+B7", "C5+C6+C7", "#,##0"),
        ("Running cost a year", "B6/Settings!$B$5", "C6/Settings!$B$5", "#,##0"),
        ("Of the total, staff time (hours)", None, None, "#,##0"),
        ("Lines still to find out", f'COUNTIF(Costs!$K${first}:$K${lastr},"Find out")', f'COUNTIF(Costs!$L${first}:$L${lastr},"Find out")', "0"),
    ]
    for i, (label, fb, fc, fmt) in enumerate(rows):
        r = 5 + i
        sm.cell(row=r, column=1, value=label).font = BOLD if label == "Total cost" else F
        if label.startswith("Of the total"):
            mult = lambda rr: f'IF(Costs!$C{rr}="One-off",1,IF(Costs!$C{rr}="Per year",Settings!$B$5,Settings!$B$5*Settings!$B$6))'
            fb = "+".join(f"N(Costs!$F{rr})*{mult(rr)}" for rr in range(first, lastr + 1))
            fc = "+".join(f"N(Costs!$H{rr})*{mult(rr)}" for rr in range(first, lastr + 1))
        for cc_, fx in (("B", fb), ("C", fc)):
            cell = sm[f"{cc_}{r}"]
            cell.value, cell.number_format, cell.fill = f"={fx}", fmt, FILL_CALC
    head(sm, 13, ["What the model's extra cost buys", "", ""])
    out = [
        ("Model's extra cost over the simple rule", "=C8-B8", "#,##0"),
        ("Extra people reached over the period", '=IF(Settings!$B$10="","",Settings!$B$10*Settings!$B$5)', "#,##0"),
        ("Cost of each extra person the model reaches", '=IF(OR(B15="",B15<=0),"",B14/B15)', "#,##0"),
        ("Current cost per person served a year", '=IF(Settings!$B$12="","",Settings!$B$12)', "#,##0"),
        ("Each extra person costs this many times the current cost per person", '=IF(OR(B16="",B17="",B17=0),"",B16/B17)', "0.0"),
        ("For comparison: cost of each extra person the simple rule reaches over current practice", '=IF(OR(Settings!$B$11="",Settings!$B$11<=0),"",B8/(Settings!$B$11*Settings!$B$5))', "#,##0"),
    ]
    for i, (label, fx, fmt) in enumerate(out):
        r = 14 + i
        cc = sm.cell(row=r, column=1, value=label)
        cc.font, cc.alignment = F, WRAP
        cell = sm.cell(row=r, column=2, value=fx)
        cell.number_format, cell.fill = fmt, FILL_CALC
    sm["A21"] = ('=IF(C11>0,"The model still has "&C11&" line(s) to find out: its total is a floor, not an estimate.",'
                 '"Every line has a figure. Recheck them with the partner before deciding.")')
    sm["A21"].font, sm["A21"].alignment = BOLD, WRAP
    sm["A22"] = "The last comparison counts the simple rule's whole cost against what it gains over today; leave it blank if you don't know that gain."
    sm["A22"].font, sm["A22"].alignment = F, WRAP
    sm.row_dimensions[21].height = 30
    sm.row_dimensions[22].height = 30
    wb.move_sheet("Summary", offset=-(len(wb.sheetnames) - 2))
    for ws in wb.worksheets:
        font_all(ws)
    wb.calculation.fullCalcOnLoad = True
    wb.save(path)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pick_n(OUT / "1-pick-n-once.xlsx")
    weekly_visits(OUT / "2-weekly-visit-list.xlsx")
    waitlist(OUT / "3-waitlist.xlsx")
    health_check(OUT / "4-monthly-health-check.xlsx")
    cost_of_ownership(OUT / "5-cost-of-ownership.xlsx")
    for p in sorted(q for q in OUT.glob("*.xlsx") if not q.name.startswith("~$")):
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
