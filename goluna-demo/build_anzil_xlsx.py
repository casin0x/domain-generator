#!/usr/bin/env python3
"""Build Anzil_Brazil_Pilot_Forecast.xlsx — Sheet 1: Path C cost forecast, Sheet 2: revenue targets."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

ARIAL = "Arial"
BLUE = Font(name=ARIAL, size=10, color="0000FF")          # hardcoded inputs
BLACK = Font(name=ARIAL, size=10)                          # formulas
GREEN = Font(name=ARIAL, size=10, color="008000")          # cross-sheet links
BOLD = Font(name=ARIAL, size=10, bold=True)
H1 = Font(name=ARIAL, size=14, bold=True)
SUB = Font(name=ARIAL, size=9, italic=True, color="666666")
HDR_FILL = PatternFill("solid", start_color="1F1F3A")
HDR_FONT = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
ANZIL_FILL = PatternFill("solid", start_color="EDE9FE")
YELLOW = PatternFill("solid", start_color="FFFF00")
TOT_FILL = PatternFill("solid", start_color="EFEFEF")
CUR = '$#,##0;[Red]($#,##0);"-"'
PROFIT = '+$#,##0;($#,##0);"-"'
PCT = "0.0%"
NUM = '#,##0;[Red](#,##0);"-"'
GOOD_RULE = lambda: CellIsRule(operator="greaterThan", formula=["0"],
    fill=PatternFill("solid", start_color="C6EFCE"), font=Font(name=ARIAL, size=10, bold=True, color="006100"))
BAD_RULE = lambda: CellIsRule(operator="lessThan", formula=["0"],
    fill=PatternFill("solid", start_color="FFC7CE"), font=Font(name=ARIAL, size=10, bold=True, color="9C0006"))
def profit_color(ws, rng):
    ws.conditional_formatting.add(rng, GOOD_RULE())
    ws.conditional_formatting.add(rng, BAD_RULE())
thin = Side(style="thin", color="CCCCCC")
BORDER = Border(top=thin, bottom=thin, left=thin, right=thin)

wb = Workbook()

# ---------------- Sheet 1: Cost Forecast ----------------
ws = wb.active
ws.title = "Cost Forecast"

ws["A1"] = "GoLuna — Path C (Anzil) Month-by-Month Cost Forecast (USD)"
ws["A1"].font = H1
ws.merge_cells("A1:N1")
ws["A2"] = ("Anzil engagement hard-capped at $100K over the 3-month pilot (M2–M4) · 1M SEK dedicated to Brazil/Anzil · "
            "clipping + influencer activation removed · M2 kill checkpoint (decision 2026-06-11). "
            "Benchmarks, not GoLuna-measured data — verify at M4.")
ws["A2"].font = SUB
ws.merge_cells("A2:N2")

# assumptions
ws["A4"] = "Assumptions"; ws["A4"].font = BOLD
rows_a = [
    ("FX (SEK per USD)", 10.5, BLUE, "0.0", True),
    ("Working budget (2.5M SEK, USD)", "=2500000/B5", BLACK, CUR, False),
    ("Brazil/Anzil envelope (1M SEK, USD)", "=1000000/B5", BLACK, CUR, False),
    ("Anzil management fee (% of media)", 0.15, BLUE, PCT, True),
    ("Anzil contract hard cap (USD)", 100000, BLUE, CUR, True),
]
for i, (label, val, font, fmt, yellow) in enumerate(rows_a, start=5):
    ws.cell(row=i, column=1, value=label).font = BLACK
    c = ws.cell(row=i, column=2, value=val); c.font = font; c.number_format = fmt
    if yellow: c.fill = YELLOW

HDR = 11
ws.cell(row=HDR, column=1, value="Line")
for m in range(1, 13):
    ws.cell(row=HDR, column=1 + m, value=f"M{m}")
ws.cell(row=HDR, column=14, value="Total")
for col in range(1, 15):
    c = ws.cell(row=HDR, column=col); c.fill = HDR_FILL; c.font = HDR_FONT
    c.alignment = Alignment(horizontal="right" if col > 1 else "left")

# (label, [12 monthly values], is_anzil)
lines = [
    ("Salaries (T+O+G)", [5000]*12, False),
    ("X VIP Transfer Method", [0]+[1143]*11, False),
    ("Cubeia AWS hosting", [1836]*12, False),
    ("Customer.io (Cubeia App. B)", [324]*12, False),
    ("Freshchat (Cubeia App. B)", [0]+[54]*11, False),
    ("Cubeia platform min (from M7)", [0]*6+[5400]*6, False),
    ("Security stack subs", [281]*12, False),
    ("Claude Max", [200]*12, False),
    ("Security stack — hardware (one-time)", [1652]+[0]*11, False),
    ("Costa Rica corp (2026)", [6858]+[0]*11, False),
    ("Designer (casino design)", [4800]+[0]*11, False),
    ("Betby setup (sportsbook)", [3000]+[0]*11, False),
    ("Other subscriptions", [476]*12, False),
    ("Anzil setup (€3K, one-time, M1)", [3240]+[0]*11, True),
    ("Anzil retainer (€1.5K/mo, M2–M4)", [0]+[1620]*3+[0]*8, True),
    ("Anzil media — Meta+WhatsApp (M2–M4)", [0, 15000, 25000, 29000]+[0]*8, True),
    ("Anzil management (15% of media)", None, True),  # formula row
]
FIRST = HDR + 1
MEDIA_ROW = FIRST + 15
for i, (label, vals, is_anzil) in enumerate(lines):
    r = FIRST + i
    lc = ws.cell(row=r, column=1, value=label); lc.font = BOLD if is_anzil else BLACK
    for m in range(12):
        col = 2 + m
        if vals is None:  # management = 15% x media
            c = ws.cell(row=r, column=col, value=f"={get_column_letter(col)}{MEDIA_ROW}*$B$8")
            c.font = BLACK
        else:
            c = ws.cell(row=r, column=col, value=vals[m]); c.font = BLUE
        c.number_format = CUR
        if is_anzil: c.fill = ANZIL_FILL
    t = ws.cell(row=r, column=14, value=f"=SUM(B{r}:M{r})"); t.font = BLACK; t.number_format = CUR
    if is_anzil: t.fill = ANZIL_FILL
LAST = FIRST + len(lines) - 1
ANZIL_FIRST, ANZIL_LAST = FIRST + 13, FIRST + 16  # setup..management
FIX_LAST = FIRST + 12                              # GoLuna fixed block

# subtotal rows: marketing (Anzil) and GoLuna fixed, per month
MKT = LAST + 1
ws.cell(row=MKT, column=1, value="MARKETING / ANZIL — monthly total (setup + retainer + media + mgmt)").font = BOLD
for m in range(13):
    col = get_column_letter(2 + m)
    rng = f"{col}{ANZIL_FIRST}:{col}{ANZIL_LAST}"
    c = ws.cell(row=MKT, column=2 + m, value=f"=SUM({rng})")
    c.font = BOLD; c.number_format = CUR; c.fill = ANZIL_FILL
FIX = MKT + 1
ws.cell(row=FIX, column=1, value="GoLuna fixed — monthly total (salaries, platform, security, one-times)").font = BOLD
for m in range(13):
    col = get_column_letter(2 + m)
    c = ws.cell(row=FIX, column=2 + m, value=f"=SUM({col}{FIRST}:{col}{FIX_LAST})")
    c.font = BOLD; c.number_format = CUR; c.fill = TOT_FILL

TOT = FIX + 1
ws.cell(row=TOT, column=1, value="Monthly total (fixed + marketing)").font = BOLD
for m in range(13):
    col = get_column_letter(2 + m)
    c = ws.cell(row=TOT, column=2 + m, value=f"={col}{MKT}+{col}{FIX}")
    c.font = BOLD; c.number_format = CUR; c.fill = TOT_FILL

CUM = TOT + 1
ws.cell(row=CUM, column=1, value="Cumulative").font = BOLD
ws.cell(row=CUM, column=2, value=f"=B{TOT}").number_format = CUR
for m in range(1, 12):
    col, prev = get_column_letter(2 + m), get_column_letter(1 + m)
    c = ws.cell(row=CUM, column=2 + m, value=f"={prev}{CUM}+{col}{TOT}")
    c.font = BLACK; c.number_format = CUR
ws.cell(row=CUM, column=2).font = BLACK

REM = CUM + 1
ws.cell(row=REM, column=1, value="Operating budget remaining (vs 2.5M SEK)").font = BOLD
for m in range(12):
    col = get_column_letter(2 + m)
    c = ws.cell(row=REM, column=2 + m, value=f"=$B$6-{col}{CUM}")
    c.font = BLACK; c.number_format = CUR

# Anzil summary block
S = REM + 3
ws.cell(row=S, column=1, value="Anzil engagement summary").font = BOLD
items = [
    ("Anzil committed total (setup + retainer + media + mgmt)", f"=N{FIRST+13}+N{FIRST+14}+N{FIRST+15}+N{FIRST+16}", CUR, BLACK),
    ("Brazil/Anzil envelope (1M SEK)", "=B7", CUR, BLACK),
    ("Headroom vs envelope (WhatsApp/PIX fees, TBD)", f"=B7-B{S+1}", CUR, BLACK),
    ("Contract hard cap", "=B9", CUR, BLACK),
    ("Headroom vs hard cap", f"=B9-B{S+1}", CUR, BLACK),
    ("Sunk if cut at M2 checkpoint (setup + M2 retainer/media/mgmt)", f"=B{FIRST+13}+C{FIRST+14}+C{FIRST+15}+C{FIRST+16}", CUR, BLACK),
    ("Never deployed if cut at M2", f"=B{S+1}-B{S+6}", CUR, BLACK),
    ("Paid if cut after 2 live months (end of M3)", f"=B{S+6}+D{FIRST+14}+D{FIRST+15}+D{FIRST+16}", CUR, BLACK),
]
for i, (label, formula, fmt, font) in enumerate(items, start=S + 1):
    ws.cell(row=i, column=1, value=label).font = BLACK
    c = ws.cell(row=i, column=2, value=formula); c.font = font; c.number_format = fmt

ws.column_dimensions["A"].width = 44
for col in range(2, 15):
    ws.column_dimensions[get_column_letter(col)].width = 11
ws.freeze_panes = "B12"

# ---------------- Sheet 2: Revenue Targets ----------------
w2 = wb.create_sheet("Revenue Targets")
w2["A1"] = "GoLuna — Path C Revenue Targets by Month (what to optimize for)"
w2["A1"].font = H1
w2.merge_cells("A1:H1")
w2["A2"] = ("NEED = ~28% retention (the break-even line: M4-exit run-rate covers the M7+ fixed burn). "
            "OPTIMIZE = ~39% retention (the flywheel compounds). Basis: ARPU $30/mo (Brazil regulated avg), "
            "CAC $20 (Anzil quote), net contribution 51.5% of GGR (incl. ~5% high-estimate PIX fee). "
            "Market benchmarks, not GoLuna data — recalibrate with real cohorts at M2–M3.")
w2["A2"].font = SUB
w2.merge_cells("A2:H2")

w2["A4"] = "Assumptions"; w2["A4"].font = BOLD
rows_b = [
    ("ARPU (GGR / active / month)", 30, BLUE, CUR, True),
    ("CAC per FTD (Anzil quote $12–25)", 20, BLUE, CUR, True),
    ("NGR (GGR − bonuses 25%)", 0.75, BLUE, PCT, False),
    ("Net contribution (after all variable, incl. PIX high-est.)", 0.515, BLUE, PCT, True),
    ("Retention — NEED (break-even line)", 0.28, BLUE, PCT, True),
    ("Retention — OPTIMIZE (compounding)", 0.39, BLUE, PCT, True),
    ("M7+ fixed run-rate (from Cost Forecast)", f"='Cost Forecast'!H{TOT}", GREEN, CUR, False),
]
for i, (label, val, font, fmt, yellow) in enumerate(rows_b, start=5):
    w2.cell(row=i, column=1, value=label).font = BLACK
    c = w2.cell(row=i, column=2, value=val); c.font = font; c.number_format = fmt
    if yellow: c.fill = YELLOW

T = 20  # monthly-detail header row; rows 13-18 hold the PROFIT AT A GLANCE block (filled in after the detail blocks exist)
heads = ["Metric", "M1 (onboard)", "M2 (pilot 1)", "M3 (pilot 2)", "M4 (pilot 3 · gate)", "M5", "M6", "M7+ /mo"]
for j, h in enumerate(heads):
    c = w2.cell(row=T, column=1 + j, value=h); c.fill = HDR_FILL; c.font = HDR_FONT
    c.alignment = Alignment(horizontal="right" if j else "left")

mr = MEDIA_ROW
r_media, r_ftd, r_cum = T + 1, T + 2, T + 3
w2.cell(row=r_media, column=1, value="Anzil media spend").font = BLACK
for j, src in enumerate(["B", "C", "D", "E", "F", "G", "H"]):
    c = w2.cell(row=r_media, column=2 + j, value=f"='Cost Forecast'!{src}{mr}")
    c.font = GREEN; c.number_format = CUR
w2.cell(row=r_ftd, column=1, value="New FTDs (media ÷ CAC)").font = BLACK
for j in range(7):
    col = get_column_letter(2 + j)
    c = w2.cell(row=r_ftd, column=2 + j, value=f"={col}{r_media}/$B$6")
    c.font = BLACK; c.number_format = NUM
w2.cell(row=r_cum, column=1, value="Cumulative FTDs (end of month)").font = BLACK
w2.cell(row=r_cum, column=2, value=f"=B{r_ftd}").number_format = NUM
for j in range(1, 7):
    col, prev = get_column_letter(2 + j), get_column_letter(1 + j)
    c = w2.cell(row=r_cum, column=2 + j, value=f"={prev}{r_cum}+{col}{r_ftd}")
    c.font = BLACK; c.number_format = NUM
w2.cell(row=r_cum, column=2).font = BLACK

def block(start, ret_cell, tag):
    r_act, r_ggr, r_ngr, r_net, r_cost, r_res, r_cum2 = range(start, start + 7)
    w2.cell(row=start - 1, column=1, value=tag).font = BOLD
    w2.cell(row=start - 1, column=1).fill = TOT_FILL
    for j in range(7):
        w2.cell(row=start - 1, column=2 + j).fill = TOT_FILL
    w2.cell(row=r_act, column=1, value="Active depositors").font = BLACK
    for j in range(7):
        col = get_column_letter(2 + j)
        if j == 0:
            f = "=0"
        elif j <= 3:  # M2-M4: new + ret x cum prior
            prev = get_column_letter(1 + j)
            f = f"={col}{r_ftd}+{ret_cell}*{prev}{r_cum}"
        else:  # M5+: ret x total pilot FTDs (cum at M4 = col E)
            f = f"={ret_cell}*$E${r_cum}"
        c = w2.cell(row=r_act, column=2 + j, value=f); c.font = BLACK; c.number_format = NUM
    for r, label, mult in [
        (r_ggr, "Target GGR (actives × ARPU)", f"{r_act}*$B$5"),
        (r_ngr, "≈ NGR (GGR − 25% bonuses)", f"{r_ggr}*$B$7"),
        (r_net, "Net contribution (51.5% of GGR)", f"{r_ggr}*$B$8"),
    ]:
        w2.cell(row=r, column=1, value=label).font = BLACK
        for j in range(7):
            col = get_column_letter(2 + j)
            c = w2.cell(row=r, column=2 + j, value=f"={col}{mult}")
            c.font = BLACK; c.number_format = CUR
    w2.cell(row=r_cost, column=1, value="Monthly cost (from Cost Forecast)").font = BLACK
    for j, src in enumerate(["B", "C", "D", "E", "F", "G", "H"]):
        c = w2.cell(row=r_cost, column=2 + j, value=f"='Cost Forecast'!{src}{TOT}")
        c.font = GREEN; c.number_format = CUR
    w2.cell(row=r_res, column=1, value="MONTHLY PROFIT / LOSS  (net contribution − cost)").font = BOLD
    for j in range(7):
        col = get_column_letter(2 + j)
        c = w2.cell(row=r_res, column=2 + j, value=f"={col}{r_net}-{col}{r_cost}")
        c.font = BOLD; c.number_format = PROFIT
    w2.cell(row=r_cum2, column=1, value="CUMULATIVE PROFIT / LOSS  (M1–M6)").font = BOLD
    w2.cell(row=r_cum2, column=2, value=f"=B{r_res}").number_format = PROFIT
    for j in range(1, 6):
        col, prev = get_column_letter(2 + j), get_column_letter(1 + j)
        c = w2.cell(row=r_cum2, column=2 + j, value=f"={prev}{r_cum2}+{col}{r_res}")
        c.font = BOLD; c.number_format = PROFIT
    w2.cell(row=r_cum2, column=8, value="n/a").font = SUB
    profit_color(w2, f"B{r_res}:H{r_res}")
    profit_color(w2, f"B{r_cum2}:G{r_cum2}")
    return r_res, r_cum2

need_res, need_cum = block(T + 6, "$B$9", "NEED — break-even line (~28% retention)")
opt_res, opt_cum = block(need_cum + 3, "$B$10", "OPTIMIZE — compounding (~39% retention)")
end_opt = opt_cum

# ---- PROFIT AT A GLANCE (rows 13-18, references the detail blocks below) ----
G = 13
w2.cell(row=G, column=1, value="PROFIT — AT A GLANCE").font = BOLD
w2.cell(row=G, column=1).fill = TOT_FILL
for j in range(1, 5): w2.cell(row=G, column=1 + j).fill = TOT_FILL
gheads = ["Scenario", "Pilot M1–M4 (the investment)", "M5–M6 / mo", "M7+ / mo", "Cumulative at M6"]
for j, h in enumerate(gheads):
    c = w2.cell(row=G + 1, column=1 + j, value=h); c.fill = HDR_FILL; c.font = HDR_FONT
    c.alignment = Alignment(horizontal="right" if j else "left")
for i, (nm, r_res_x, r_cum_x) in enumerate([("NEED — break-even (~28% ret.)", need_res, need_cum),
                                            ("OPTIMIZE — compounding (~39% ret.)", opt_res, opt_cum)]):
    r = G + 2 + i
    w2.cell(row=r, column=1, value=nm).font = BOLD
    for col_i, f in [(2, f"=SUM(B{r_res_x}:E{r_res_x})"), (3, f"=F{r_res_x}"), (4, f"=H{r_res_x}"), (5, f"=G{r_cum_x}")]:
        c = w2.cell(row=r, column=col_i, value=f); c.font = BOLD; c.number_format = PROFIT
profit_color(w2, f"B{G+2}:E{G+3}")
w2.cell(row=G + 5, column=1, value=("Read: the pilot is an investment (red) in both scenarios. At the NEED line the machine reaches break-even from M7 "
    "(profit ≈ $0/mo — that is the definition of the line). At the OPTIMIZE line the same spend returns ~+$6K/mo from M7 to reinvest. Green = profit, red = loss.")).font = SUB
w2.merge_cells(start_row=G + 5, start_column=1, end_row=G + 5, end_column=8)

# after-M4 states
A = end_opt + 3
w2.cell(row=A, column=1, value="After-M4 states (exit run-rate vs the floor)").font = BOLD
hdrs = ["Retention of ~3,450 pilot FTDs", "Active deps", "GGR / mo", "Net / mo (51.5%)", "vs M7+ run-rate", "Verdict"]
for j, h in enumerate(hdrs):
    c = w2.cell(row=A + 1, column=1 + j, value=h); c.fill = HDR_FILL; c.font = HDR_FONT
states = [(0.15, "KILL — bleeds"), (0.25, "Marginal — kill unless trending up"), (0.28, "Break-even — the GO line"), (0.39, "Compounding — scale it")]
for i, (ret, verdict) in enumerate(states):
    r = A + 2 + i
    c = w2.cell(row=r, column=1, value=ret); c.font = BLUE; c.number_format = PCT
    w2.cell(row=r, column=2, value=f"=A{r}*$E${r_cum}").number_format = NUM
    w2.cell(row=r, column=3, value=f"=B{r}*$B$5").number_format = CUR
    w2.cell(row=r, column=4, value=f"=C{r}*$B$8").number_format = CUR
    w2.cell(row=r, column=5, value=f"=D{r}-$B$11").number_format = PROFIT
    w2.cell(row=r, column=6, value=verdict).font = BLACK
    for col in range(2, 6): w2.cell(row=r, column=col).font = BLACK
profit_color(w2, f"E{A+2}:E{A+5}")

F = A + 8
w2.cell(row=F, column=1, value="M4 gate floor (GGR/mo) = M7+ run-rate ÷ net contribution").font = BOLD
c = w2.cell(row=F, column=2, value="=B11/B8"); c.font = BLACK; c.number_format = CUR

w2.column_dimensions["A"].width = 44
for col in range(2, 9):
    w2.column_dimensions[get_column_letter(col)].width = 15
w2.freeze_panes = "B21"

wb.save("Anzil_Brazil_Pilot_Forecast.xlsx")
print("saved", TOT, CUM, REM)
