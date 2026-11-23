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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pick_n(OUT / "1-pick-n-once.xlsx")
    weekly_visits(OUT / "2-weekly-visit-list.xlsx")
    waitlist(OUT / "3-waitlist.xlsx")
    for p in sorted(OUT.glob("*.xlsx")):
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
