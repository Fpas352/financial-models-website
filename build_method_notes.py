#!/usr/bin/env python3
"""Build the SFS Models method notes as PDFs.

Each note is written below as HTML, rendered to research/notes/<slug>.pdf with
headless Chrome, and listed in research/notes.json for build_research_index.py.

Worked figures come from the demo books inside the named models
(models/final/*.xlsx, cached values as last calculated in Excel). If a model's
demo book changes, re-read the figures and update the note.

Run:  python3 build_method_notes.py   (then python3 build_research_index.py)
"""
import json, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "research" / "notes"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "https://sfsmodels.org"

NAVY, GOLD, GREY, LIGHT = "#1F3864", "#B8962E", "#6B6F76", "#E7E9EE"


# ── small SVG chart helpers ──────────────────────────────────────────────────
def hbar_svg(rows, unit="", width=640, bar_h=26, gap=12, label_w=190, note=""):
    """Horizontal bars. rows = [(label, value, highlight_bool)]."""
    vmax = max(v for _, v, _ in rows) or 1
    plot_w = width - label_w - 70
    h = len(rows) * (bar_h + gap) + 10
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="DM Sans, Arial, sans-serif" font-size="13">']
    for i, (lab, v, hi) in enumerate(rows):
        y = 5 + i * (bar_h + gap)
        w = max(2, plot_w * v / vmax)
        col = NAVY if hi else "#9AA3B5"
        u = unit[:-1] if v == 1 and unit.endswith("s") else unit
        out.append(f'<text x="{label_w - 10}" y="{y + bar_h * 0.68}" text-anchor="end" fill="#222">{lab}</text>')
        out.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{col}" rx="2"/>')
        out.append(f'<text x="{label_w + w + 8:.1f}" y="{y + bar_h * 0.68}" fill="#222" font-weight="600">{v:g}{u}</text>')
    out.append("</svg>")
    return "".join(out)


def line_svg(series, xlabels, ymax, yfmt=lambda v: f"{v:.0f}%", width=640, height=280, yticks=5):
    """series = [(name, [values], colour, dashed_bool)]."""
    L, R, T, B = 52, 20, 14, 46
    pw, ph = width - L - R, height - T - B
    n = len(xlabels)
    x = lambda i: L + pw * i / (n - 1)
    y = lambda v: T + ph * (1 - v / ymax)
    out = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="DM Sans, Arial, sans-serif" font-size="12">']
    for k in range(yticks + 1):
        v = ymax * k / yticks
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{LIGHT}"/>')
        out.append(f'<text x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end" fill="{GREY}">{yfmt(v)}</text>')
    for i, lab in enumerate(xlabels):
        out.append(f'<text x="{x(i):.1f}" y="{height - B + 18}" text-anchor="middle" fill="{GREY}">{lab}</text>')
    lx = L
    for name, vals, col, dashed in series:
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"{dash}/>')
        for i, v in enumerate(vals):
            out.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.5" fill="{col}"/>')
        out.append(f'<line x1="{lx}" x2="{lx + 26}" y1="{height - 9}" y2="{height - 9}" stroke="{col}" stroke-width="2.5"{dash}/>')
        out.append(f'<text x="{lx + 32}" y="{height - 5}" fill="#222">{name}</text>')
        lx += 32 + 7.2 * len(name) + 28
    out.append("</svg>")
    return "".join(out)


def waterfall_svg(steps, ymin, ymax, hurdle=None, width=640, height=300):
    """steps = [(label, value, kind)] kind in start|delta|end. Values in % points."""
    L, R, T, B = 46, 14, 14, 58
    pw, ph = width - L - R, height - T - B
    n = len(steps)
    slot = pw / n
    bw = slot * 0.62
    y = lambda v: T + ph * (ymax - v) / (ymax - ymin)
    out = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="DM Sans, Arial, sans-serif" font-size="11.5">']
    for k in range(int(ymin), int(ymax) + 1, 2):
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(k):.1f}" y2="{y(k):.1f}" stroke="{LIGHT}"/>')
        out.append(f'<text x="{L - 7}" y="{y(k) + 4:.1f}" text-anchor="end" fill="{GREY}">{k}%</text>')
    if hurdle is not None:
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(hurdle):.1f}" y2="{y(hurdle):.1f}" '
                   f'stroke="#B42318" stroke-width="1.5" stroke-dasharray="5 4"/>')
        out.append(f'<text x="{L + 6}" y="{y(hurdle) + 14:.1f}" text-anchor="start" fill="#B42318">'
                   f'Hurdle {hurdle:.1f}%</text>')
    run = 0.0
    for i, (lab, v, kind) in enumerate(steps):
        cx = L + slot * i + (slot - bw) / 2
        if kind in ("start", "end"):
            top, bot, col, run = v, 0 if ymin <= 0 else ymin, NAVY, v
            txt = f"{v:.2f}%"
        else:
            top, bot = (run + v, run) if v >= 0 else (run, run + v)
            col = "#3C8D5A" if v >= 0 else "#B42318"
            run += v
            txt = f"{v:+.2f}"
        out.append(f'<rect x="{cx:.1f}" y="{y(top):.1f}" width="{bw:.1f}" height="{max(1, y(bot) - y(top)):.1f}" fill="{col}"/>')
        out.append(f'<text x="{cx + bw / 2:.1f}" y="{y(top) - 5:.1f}" text-anchor="middle" fill="#222" font-weight="600">{txt}</text>')
        for j, part in enumerate(lab.split("|")):
            out.append(f'<text x="{cx + bw / 2:.1f}" y="{height - B + 17 + j * 14}" text-anchor="middle" fill="{GREY}">{part}</text>')
    out.append("</svg>")
    return "".join(out)


# ── page template ────────────────────────────────────────────────────────────
CSS = """
@page { size: A4; margin: 20mm 19mm 20mm 19mm;
  @bottom-left { content: "SFS Models  ·  Method Note"; font: 8pt 'DM Sans', Arial; color: #8A8F98; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 8pt 'DM Sans', Arial; color: #8A8F98; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'DM Sans', Arial, sans-serif; font-size: 10.2pt; line-height: 1.55; color: #1B1D21; margin: 0; }
.mast { border-top: 5px solid #1F3864; padding-top: 10px; display: flex; justify-content: space-between;
  font-size: 8.5pt; letter-spacing: .06em; text-transform: uppercase; color: #6B6F76; }
.mast b { color: #1F3864; }
h1 { font-family: 'DM Serif Display', Georgia, serif; font-weight: 400; font-size: 26pt; line-height: 1.12;
  color: #1F3864; margin: 18px 0 10px; }
.dek { font-size: 12pt; line-height: 1.5; color: #3A3F47; margin: 0 0 14px; }
.byline { font-size: 8.5pt; color: #6B6F76; border-bottom: 1px solid #D9DCE2; padding-bottom: 12px; margin-bottom: 4px; }
.summary { background: #F4F1E6; border-left: 4px solid #B8962E; padding: 10px 14px; margin: 16px 0 6px; }
.summary h3 { margin: 0 0 4px; font-size: 9pt; letter-spacing: .06em; text-transform: uppercase; color: #8A6D1C; }
.summary ul { margin: 0; padding-left: 18px; } .summary li { margin: 2px 0; }
h2 { font-family: 'DM Serif Display', Georgia, serif; font-weight: 400; font-size: 15.5pt; color: #1F3864;
  margin: 22px 0 6px; break-after: avoid; }
h2 .n { color: #B8962E; margin-right: 6px; }
p { margin: 0 0 8px; } ul, ol { margin: 0 0 8px; padding-left: 20px; } li { margin: 2px 0; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 4px; font-size: 9.2pt; break-inside: avoid; }
th { background: #1F3864; color: #fff; font-weight: 600; text-align: right; padding: 5px 8px; }
th:first-child, td:first-child { text-align: left; }
td { padding: 4px 8px; border-bottom: 1px solid #E3E5EA; text-align: right; font-variant-numeric: tabular-nums; }
tr.hl td { background: #FBF7EA; font-weight: 600; }
tr.tot td { border-top: 1.5px solid #1F3864; font-weight: 700; }
.cap { font-size: 8.3pt; color: #6B6F76; margin: 2px 0 10px; }
.fig { break-inside: avoid; margin: 10px 0 4px; }
.figt { font-size: 9pt; font-weight: 700; color: #1F3864; margin-bottom: 4px; }
.formula { font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 8.8pt; background: #F3F4F7;
  border: 1px solid #E3E5EA; padding: 7px 10px; margin: 6px 0 10px; white-space: pre-wrap; break-inside: avoid; }
.callout { border: 1px solid #D9DCE2; border-left: 4px solid #1F3864; padding: 9px 13px; margin: 10px 0; break-inside: avoid; }
.callout b:first-child { color: #1F3864; }
.check { list-style: none; padding-left: 0; } .check li { padding-left: 22px; position: relative; margin: 4px 0; }
.check li:before { content: ""; position: absolute; left: 2px; top: 4px; width: 10px; height: 10px; border: 1.5px solid #1F3864; }
.model { background: #1F3864; color: #fff; padding: 14px 18px; margin: 18px 0 8px; break-inside: avoid; }
.model h3 { font-family: 'DM Serif Display', Georgia, serif; font-weight: 400; font-size: 14pt; margin: 0 0 6px; color: #fff; }
.model p { color: #E3E6EE; margin: 0 0 6px; } .model a { color: #E8C964; font-weight: 600; text-decoration: none; }
.legal { font-size: 7.8pt; color: #8A8F98; border-top: 1px solid #E3E5EA; padding-top: 8px; margin-top: 14px; }
a { color: #1F3864; }
"""


def page(note):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>{note['title']} | SFS Models Method Note</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="mast"><span><b>SFS Models</b> · Method Note No. {note['no']}</span><span>{note['topic']} · {note['date_label']}</span></div>
<h1>{note['title']}</h1>
<p class="dek">{note['dek']}</p>
<div class="byline">Written by SFS Models, a practitioner with a senior banking FP&amp;A background. Worked figures come from
the demo loan book inside the {note['model_name']}, so every number here can be traced to a cell.</div>
{note['body']}
<div class="model"><h3>Run this on your own book</h3>{note['model_box']}
<p><a href="{SITE}/{note['model_url']}">{note['model_name']}: details and free sample →</a></p></div>
<p class="legal">Illustrative only. The figures describe a demo loan book, not any real institution. This note is general
methodology, not accounting, regulatory or investment advice; apply your own policy and seek your auditor's view.
© 2026 SFS Models · sfsmodels.org</p>
</body></html>"""


# ── NOTE 1: SICR ─────────────────────────────────────────────────────────────
n1_bar = hbar_svg([
    ("PD increase", 80, True), ("30+ days past due", 45, False), ("Watchlist", 22, False),
    ("Forbearance", 9, False), ("Rating downgrade", 1, False)], unit=" loans")

NOTE1 = dict(
    slug="sicr-staging-triggers", no=1, topic="IFRS 9", date_label="November 2026",
    title="What actually triggers SICR: building a Stage 2 test you can defend",
    dek="Thirty days past due is the backstop, not the test. How to design a significant increase in credit risk "
        "assessment that moves loans early, behaves sensibly across the rating scale, and leaves an audit trail "
        "for every exposure.",
    model_name="IFRS 9 ECL Model: Loan-Level Edition", model_url="ifrs9-loan-level-ecl-model-excel.html",
    summary="Why a fixed PD multiple behaves differently at each end of the rating scale, what the demo book's "
            "trigger mix looks like, and how far the allowance moves when the threshold changes.",
    model_box="<p>The loan-level model applies all five Stage 2 triggers and the low credit risk exemption to every "
              "loan in a tape of up to 1,000, records which trigger fired first, and re-runs the book at a tighter "
              "and a looser PD threshold so the sensitivity in section 6 is produced for you.</p>",
    body=f"""
<div class="summary"><h3>In brief</h3><ul>
<li>IFRS 9 compares the risk of default over the remaining life now against the same measure at initial recognition. Days past due only matter when that comparison has failed to move a loan in time.</li>
<li>A fixed relative threshold on lifetime PD is easy to hit for strong grades and hard to hit for weak ones. Pair it with an absolute threshold and a notch-based downgrade trigger, or it will stage the wrong loans.</li>
<li>In the demo book, the PD test is the first reason for 51% of Stage 2 loans and days past due for 29%. A higher DPD share is the clearest sign the forward-looking test is arriving late.</li>
<li>Record which trigger fired for every loan. It is the only answer to "why did this one move?"</li>
</ul></div>

<h2><span class="n">1</span>The question staging has to answer</h2>
<p>IFRS 9 (paragraphs 5.5.3 and 5.5.9) asks whether credit risk on a financial instrument has increased significantly
since initial recognition. The comparison is between the risk of a default occurring over the expected life as at the
reporting date and the same risk as it was assessed at initial recognition. Three things follow from that wording, and
most weak staging policies break at least one of them.</p>
<ul>
<li><b>It is relative to origination, not to today's average.</b> A grade 6 loan that was originated at grade 6 has not
deteriorated. A grade 4 loan that was originated at grade 1 has.</li>
<li><b>It is about default risk over the life, not the next twelve months.</b> Twelve-month PD is an accepted proxy only
where it gives a reasonable approximation, which it often does not for long-dated or back-loaded exposures.</li>
<li><b>The 30 days past due presumption (5.5.11) is rebuttable and is a backstop.</b> Its purpose is to catch what the
forward-looking assessment missed. A policy that leans on it is reporting deterioration after the borrower has already
stopped paying.</li>
</ul>

<h2><span class="n">2</span>Compare like with like: lifetime PD over the remaining term</h2>
<p>The cleanest quantitative test compares lifetime PD for the remaining term at the current grade with lifetime PD for
the same term at the origination grade. Using the same remaining term on both sides strips out the fact that cumulative
PD rises with horizon on its own. In the model both curves are compounded from one transition matrix, so they are
consistent by construction (Method Note No. 2 shows how).</p>
<p>The table below uses the demo matrix with four years remaining. One-year PDs double with each grade, from 0.03% at
grade 1 to 28% at grade 10.</p>
<table>
<tr><th>Origination grade</th><th>4-year PD at origination grade</th><th>After 1-notch downgrade</th><th>Ratio</th><th>Absolute rise</th><th>2× and +0.5pp both met?</th></tr>
<tr><td>1 Exceptional</td><td>0.16%</td><td>0.40%</td><td>2.54×</td><td>+0.24pp</td><td>No (absolute)</td></tr>
<tr><td>2 Very strong</td><td>0.40%</td><td>0.96%</td><td>2.40×</td><td>+0.56pp</td><td>Yes, but exempt*</td></tr>
<tr class="hl"><td>3 Strong</td><td>0.96%</td><td>2.10%</td><td>2.19×</td><td>+1.14pp</td><td>Yes</td></tr>
<tr class="hl"><td>4 Good</td><td>2.10%</td><td>4.21%</td><td>2.01×</td><td>+2.11pp</td><td>Yes, just</td></tr>
<tr><td>5 Satisfactory</td><td>4.21%</td><td>8.20%</td><td>1.95×</td><td>+3.99pp</td><td>No (relative)</td></tr>
<tr><td>6 Acceptable</td><td>8.20%</td><td>15.24%</td><td>1.86×</td><td>+7.04pp</td><td>No (relative)</td></tr>
<tr><td>7 Watch</td><td>15.24%</td><td>27.28%</td><td>1.79×</td><td>+12.04pp</td><td>No (relative)</td></tr>
</table>
<p class="cap">* A loan now at grade 3 or better is inside the low credit risk exemption and is not tested on PD. Source: PD_CURVES tab, demo matrix.</p>
<p>The pattern matters more than the numbers. Lifetime PDs compress towards 100% as grades weaken, so the same one-notch
move produces a smaller ratio lower down the scale. A single 2× multiple therefore treats a one-notch move as significant
for a grade 3 or 4 borrower and not for a grade 5 to 7 borrower, even though the absolute increase for the weaker
borrower is several times larger. For a two-notch move the ratio stays above 2× for every origination grade up to 8 (5.26× at
grade 2, 3.62× at grade 5, 2.59× at grade 8).</p>
<p>There are two defensible responses. Either accept that SICR for weaker grades means two notches, and say so in the
policy, or vary the relative threshold by origination grade. What does not survive challenge is a single multiple whose
effect across the scale nobody has worked out.</p>

<h2><span class="n">3</span>Why you need the absolute threshold as well</h2>
<p>The absolute test exists for the top of the scale. A loan moving from 0.16% to 0.40% lifetime PD has more than doubled,
and is still a very low risk. Without an absolute floor it would move to Stage 2, carry a lifetime allowance, and add noise
to the Stage 2 population that the board and the auditor then have to explain. The demo model requires both: lifetime PD at
least 2× the origination level <i>and</i> at least 0.5 percentage points higher.</p>
<p>The low credit risk exemption (5.5.10) does similar work for investment-grade-equivalent exposures. In the demo it covers
grades 1 to 3 (one-year PD up to 0.20%). Twelve loans in the demo book met the PD test but were held in Stage 1 by the
exemption. Report that number: it shows the exemption is doing something, and shows how much it is doing.</p>

<h2><span class="n">4</span>The qualitative triggers the PD will not see in time</h2>
<p>Rating models update on a cycle. Credit officers see problems between cycles. Three non-PD triggers close that gap.</p>
<ul>
<li><b>Downgrade of a set number of notches</b> (three in the demo). This is a backstop for the PD test, not a duplicate of
it. It catches the weak-grade cases from section 2 where a multi-notch fall fails the relative test.</li>
<li><b>Watchlist.</b> If a loan is on the watchlist, someone has a concern the model has not priced. Many lenders treat it as
an automatic Stage 2 trigger, and the demo does.</li>
<li><b>Forbearance.</b> A concession granted because the borrower is in difficulty is evidence of increased credit risk
almost by definition.</li>
</ul>

<h2><span class="n">5</span>What the demo book's trigger mix shows</h2>
<p>The demo tape has 1,000 loans across five segments: 824 in Stage 1, 157 in Stage 2 and 19 in Stage 3. A loan can hit more
than one trigger, so the model also records the first reason in a fixed order of precedence.</p>
<div class="fig"><div class="figt">Stage 2 loans by first trigger (demo book, 157 loans)</div>{n1_bar}</div>
<p class="cap">Source: STAGING tab, section C. 96 loans met the PD test in total, 49 the downgrade test, 39 watchlist, 21 forbearance.</p>
<p>Two readings are worth making in any book. First, the share that reached Stage 2 on days past due alone: 45 loans, 29%
here. That is the population the forward-looking test failed to catch before arrears. If it is most of your Stage 2 book,
the primary test is arriving late. Second, the downgrade trigger is the first reason for only one loan but is hit by 49:
it is overlapping with the PD test, as a backstop should, rather than doing the staging on its own.</p>

<h2><span class="n">6</span>Calibrate the threshold by showing what it does</h2>
<p>The relative threshold is a judgement, and the most useful thing you can give a committee is its effect on the book. The
demo model re-stages every loan at a tighter and a looser setting.</p>
<table>
<tr><th>Relative PD threshold</th><th>1.5× (tighter)</th><th>2.0× (in use)</th><th>3.0× (looser)</th></tr>
<tr><td>Stage 2 loans</td><td>214</td><td>157</td><td>137</td></tr>
<tr><td>Stage 2 share of exposure</td><td>21.9%</td><td>14.9%</td><td>13.1%</td></tr>
<tr><td>Loss allowance</td><td>£4.76m</td><td>£4.33m</td><td>£4.27m</td></tr>
<tr class="hl"><td>Change in allowance</td><td>+9.7%</td><td>–</td><td>(1.4%)</td></tr>
</table>
<p class="cap">Source: SENSITIVITY tab. Exposure at default £227.7m.</p>
<p>The response is asymmetric. Tightening to 1.5× adds 57 loans and nearly 10% to the allowance; loosening to 3× removes 20
loans and 1.4%. The book has a cluster of 57 loans between 1.5× and 2×, which is exactly the population a reviewer will ask
about. The outer bounds are also worth one line in the pack: with every performing loan in Stage 1 the allowance before
overlay would be £3.12m, as staged it is £4.23m, and with every performing loan in Stage 2 it would be £6.18m. Staging
judgements are worth up to £3m on this book.</p>

<h2><span class="n">7</span>The audit file: what to be able to show</h2>
<ul class="check">
<li>For each Stage 2 loan, the trigger or triggers that fired and the first reason, as at the reporting date.</li>
<li>The share of Stage 2 reached on days past due alone, with a view on whether it is falling over time.</li>
<li>The effect of the relative threshold across the rating scale (the section 2 table for your own matrix).</li>
<li>How many loans the absolute threshold and the low credit risk exemption held back.</li>
<li>Allowance at a tighter and a looser threshold, and the all-Stage-1 and all-Stage-2 bounds.</li>
<li>Movements between stages in the period, tied to the IFRS 7 reconciliation without a manual bridge.</li>
</ul>
<div class="callout"><b>The test of a staging policy</b> is whether you can answer this for any single loan: "It was downgraded
three notches and the relative PD test fired on the same date." "It breached one of five tests" is not an answer.</div>
""")


# ── NOTE 2: lifetime PD and forward-looking adjustment ───────────────────────
n2_line = line_svg([
    ("Through-the-cycle", [0.900, 1.901, 3.005, 4.212, 5.516], "#9AA3B5", True),
    ("SME, downside scenario", [1.585, 3.208, 4.609, 5.888, 7.163], NAVY, False)],
    ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], ymax=8, yfmt=lambda v: f"{v:.0f}%", yticks=4)

NOTE2 = dict(
    slug="lifetime-pd-forward-looking", no=2, topic="IFRS 9", date_label="November 2026",
    title="From transition matrix to forward-looking lifetime PD",
    dek="How to build IFRS 9 lifetime PD curves that are traceable from end to end: compounding a rating matrix, "
        "turning macro scenarios into one credit cycle index, shifting hazard rates, and why the probability-weighted "
        "allowance is higher than the baseline.",
    model_name="IFRS 9 ECL Model: Loan-Level Edition", model_url="ifrs9-loan-level-ecl-model-excel.html",
    summary="Compounding a transition matrix into PD curves, building a credit cycle index from four macro variables, "
            "and why the weighted allowance sits 24% above the baseline in the demo book.",
    model_box="<p>The PD_CURVES tab compounds your transition matrix, MACRO turns four variables into the credit cycle "
              "index, and every loan is measured under four scenarios and probability-weighted. Set the index to zero "
              "and the through-the-cycle curve comes back exactly.</p>",
    body=f"""
<div class="summary"><h3>In brief</h3><ul>
<li>Derive lifetime PDs from one transition matrix rather than typing a curve per grade. Every horizon is then consistent, and the curve can be traced back to a single input.</li>
<li>Express each macro scenario as one credit cycle index: a weighted sum of standardised variables. Shift each segment's hazard rates in log-odds by a sensitivity times that index.</li>
<li>Design for one check above all: an index of zero must return the through-the-cycle curve exactly. That puts the forward-looking adjustment in plain view.</li>
<li>Losses are convex in the macro path, so the probability-weighted allowance sits above the baseline. In the demo book it is 24% higher. That gap is the point of IFRS 9 5.5.17, not an error.</li>
</ul></div>

<h2><span class="n">1</span>Why derive PDs from a matrix at all</h2>
<p>Many smaller lenders hold a table of lifetime PDs by grade and year, typed in from a vendor or an old calibration. It
works until someone asks where year 4 for grade 6 came from, or why the curve for grade 7 crosses the curve for grade 8 in
year 9. A one-year transition matrix gives one source for every horizon: the probability of being in default by year
<i>t</i> is the default column of the matrix raised to the power <i>t</i>. Change the matrix and every curve, every stage and
every allowance moves together.</p>
<div class="formula">Cumulative PD, years 1..t, starting grade g  =  [ M^t ](g, Default)
In Excel:  C(t, g) = SUMPRODUCT( row g of M, C(t-1, every grade) )
with C(0, ·) = 0 for performing grades and 1 for default (default is absorbing).</div>
<p>The demo matrix has ten performing grades and an absorbing default state. Each row sums to 100%, which the model
checks. For a grade 5 (Satisfactory) borrower the compounding gives:</p>
<table>
<tr><th>Year</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><td>Cumulative PD</td><td>0.90%</td><td>1.90%</td><td>3.00%</td><td>4.21%</td><td>5.52%</td></tr>
<tr><td>Marginal hazard rate</td><td>0.90%</td><td>1.01%</td><td>1.13%</td><td>1.24%</td><td>1.36%</td></tr>
</table>
<p class="cap">Hazard rate = (C<sub>t</sub> − C<sub>t−1</sub>) / (1 − C<sub>t−1</sub>): the chance of defaulting in year t given survival to the start of it. Source: PD_CURVES, sections A and B.</p>
<p>The hazard rises with time for a mid-grade borrower because some survivors migrate down the scale. That shape comes out
of the matrix without anyone choosing it, which is the point.</p>

<h2><span class="n">2</span>One index per scenario</h2>
<p>The matrix is through-the-cycle: it describes an average year. IFRS 9 wants point-in-time estimates that reflect current
conditions and forecasts. The simplest transparent bridge is a credit cycle index: for each year of each scenario, a weighted
sum of how far each macro variable sits from its long-run mean, in standard deviations, signed so that positive means worse.</p>
<table>
<tr><th>Variable</th><th>Long-run mean</th><th>Std dev</th><th>Direction</th><th>Weight</th><th>Downside, year 1</th><th>Contribution</th></tr>
<tr><td>GDP growth</td><td>1.6%</td><td>1.8%</td><td>−1</td><td>30%</td><td>(0.8%)</td><td>+0.400</td></tr>
<tr><td>Unemployment rate</td><td>5.0%</td><td>1.4%</td><td>+1</td><td>35%</td><td>5.8%</td><td>+0.200</td></tr>
<tr><td>House price growth</td><td>3.5%</td><td>6.0%</td><td>−1</td><td>20%</td><td>(6.0%)</td><td>+0.317</td></tr>
<tr><td>Policy rate</td><td>3.0%</td><td>1.8%</td><td>+1</td><td>15%</td><td>4.5%</td><td>+0.125</td></tr>
<tr class="tot"><td>Credit cycle index</td><td></td><td></td><td></td><td>100%</td><td></td><td>+1.042</td></tr>
</table>
<p class="cap">GDP: (−0.8% − 1.6%) / 1.8% = −1.33 standard deviations, × direction −1 × weight 30% = +0.400. Source: MACRO tab.</p>
<p>Across the five projection years the demo indices run from +0.08 to −0.14 in the baseline, +1.04 falling to zero in the
downside, and +2.19 falling to +0.15 in the severe downside. After year 5 each index fades in a straight line to zero over a
set number of years (three in the demo), so long-dated loans revert to through-the-cycle risk rather than carrying a
recession for their whole life.</p>
<p>The weights are a judgement and should be documented as one. A regression of historical default rates on the same variables
is a good way to set them; even without one, a committee can reason about whether unemployment should carry more weight than
the policy rate for a mortgage book.</p>

<h2><span class="n">3</span>Shift hazards, not cumulative PDs</h2>
<p>Each segment gets a sensitivity, beta, to the index. The point-in-time hazard for a grade, year and scenario is the
through-the-cycle hazard moved in log-odds:</p>
<div class="formula">PIT hazard = 1 / ( 1 + EXP( −( LN(h / (1 − h)) + beta × index ) ) )</div>
<p>Working in log-odds keeps every result between 0 and 1, and moves low hazards proportionally more than high ones, which
is how default rates behave across a cycle. Shifting the hazard rather than the cumulative curve keeps the curve
monotonic. For an SME loan at grade 5 (beta 0.55) in the downside scenario:</p>
<div class="fig"><div class="figt">Cumulative PD, grade 5: through-the-cycle against the SME downside path</div>{n2_line}</div>
<p class="cap">Year 1 hazard moves from 0.90% to 1.59%; by year 5 the index has faded and the yearly hazard is back to 1.36%, but the cumulative PD stays 1.6 points higher: the recession years are not undone.</p>
<div class="callout"><b>The zero-index check.</b> Set every index to zero and the point-in-time curves must equal the
through-the-cycle curves to the last decimal. If they do not, something other than the macro overlay is changing the PDs. It
is the first test to run on any PD model you inherit. In the demo model it holds by construction, because the shift term becomes beta × 0.</div>

<h2><span class="n">4</span>From curves to an allowance</h2>
<p>For each loan and scenario, expected loss in each future year is the marginal PD × LGD × exposure at default, discounted at
the effective interest rate. Stage 1 sums the first twelve months; Stage 2 sums the remaining life; Stage 3 uses a PD of one.
The demo book's coverage shows the step between stages that staging decisions control:</p>
<table>
<tr><th>Stage</th><th>Loans</th><th>Exposure</th><th>Allowance</th><th>Coverage</th></tr>
<tr><td>Stage 1</td><td>824</td><td>£190.5m</td><td>£1.19m</td><td>0.62%</td></tr>
<tr><td>Stage 2</td><td>157</td><td>£34.0m</td><td>£2.08m</td><td>6.12%</td></tr>
<tr><td>Stage 3</td><td>19</td><td>£3.2m</td><td>£1.06m</td><td>33.4%</td></tr>
<tr class="tot"><td>Total</td><td>1,000</td><td>£227.7m</td><td>£4.33m</td><td>1.90%</td></tr>
</table>
<p class="cap">Source: STAGING, section A. Includes a management overlay of £0.11m (2.5% of modelled ECL).</p>

<h2><span class="n">5</span>Why the weighted allowance is above the baseline</h2>
<p>IFRS 9 (5.5.17) requires an unbiased, probability-weighted amount determined by evaluating a range of possible outcomes.
Running only the central case and calling it the weighted answer understates the allowance whenever losses respond more to bad
outcomes than to good ones, which they nearly always do.</p>
<table>
<tr><th>Scenario</th><th>Weight</th><th>Allowance before overlay</th><th>Weighted contribution</th></tr>
<tr><td>Baseline</td><td>40%</td><td>£3.42m</td><td>£1.37m</td></tr>
<tr><td>Upside</td><td>20%</td><td>£2.93m</td><td>£0.59m</td></tr>
<tr><td>Downside</td><td>30%</td><td>£4.94m</td><td>£1.48m</td></tr>
<tr><td>Severe downside</td><td>10%</td><td>£7.94m</td><td>£0.79m</td></tr>
<tr class="tot"><td>Probability-weighted</td><td>100%</td><td></td><td>£4.23m</td></tr>
</table>
<p class="cap">Source: SCENARIOS and OUTPUTS. Contributions are rounded.</p>
<p>The upside saves £0.49m against the baseline; the severe downside adds £4.53m. The weighted allowance is £0.81m, or 23.8%,
above the baseline. Two things drive the asymmetry: hazards are shifted in log-odds, so bad years raise them faster than good
years lower them, and adverse scenarios push more loans past the staging thresholds into lifetime measurement.</p>
<p>Report that gap explicitly. It answers the question a committee will ask about the weights ("what if we put 5% more on the
downside?") and it shows the forward-looking adjustment is material and deliberate. The demo model also carries three weight
sets on INPUTS, giving £3.80m, £4.23m and £4.88m, so the sensitivity to the weighting is one switch away.</p>

<h2><span class="n">6</span>Validation checklist</h2>
<ul class="check">
<li>Every row of the transition matrix sums to 100%; default is absorbing.</li>
<li>Cumulative PDs rise with horizon and worsen with grade, for every grade and year.</li>
<li>An index of zero returns the through-the-cycle curves exactly.</li>
<li>Index weights sum to 100% and each variable's direction is signed so that positive means worse.</li>
<li>Scenario weights sum to 100%, and the weighted allowance is reported alongside the baseline and each scenario.</li>
<li>The movement table and IFRS 7 tables are built from the same loan-level results as the allowance.</li>
</ul>
""")


# ── NOTE 3: credit stress test and capital ───────────────────────────────────
n3_wf = waterfall_svg([
    ("CET1 ratio|at start", 15.71, "start"), ("Pre-provision|profit", 2.39, "delta"),
    ("Impairment|charge", -9.19, "delta"), ("Other|losses", -0.40, "delta"),
    ("Tax and|dividends", 0.0, "delta"), ("RWA|change", -0.77, "delta"),
    ("CET1 ratio|end year 3", 7.73, "end")], ymin=0, ymax=20, hurdle=7.0)

NOTE3 = dict(
    slug="credit-stress-test-capital", no=3, topic="Stress testing", date_label="November 2026",
    title="Stress testing capital from the loan book",
    dek="A stressed loss rate answers one supervisory question. This note covers the follow-ups: migration as well as "
        "default, the RWA inflation that downgrades cause, the CET1 bridge a board can read, and a reverse stress test "
        "expressed in numbers rather than prose.",
    model_name="Credit Stress Test & Capital Model", model_url="credit-stress-test-model-excel.html",
    summary="Migration, RWA inflation, the CET1 bridge and a reverse stress test in numbers, worked through on the demo "
            "bank, where the severe scenario leaves 0.73 points of headroom.",
    model_box="<p>The model takes a tape of up to 1,000 loans through three scenarios over three years, shifts the "
              "transition matrix by segment, follows collateral values into LGD and risk weights, and produces the "
              "capital plan, the BRIDGE and the REVERSE tabs used here, with and without management actions.</p>",
    body=f"""
<div class="summary"><h3>In brief</h3><ul>
<li>Stress the whole transition matrix, not just the default column. Downgrades drive Stage 2 migration and higher risk weights, and both hit the CET1 ratio.</li>
<li>Let collateral values follow their own path. Falling prices raise LGD and move mortgages into higher loan-to-value risk-weight bands.</li>
<li>Show the result as a bridge from the starting CET1 ratio to the end. In the demo bank's severe scenario the ratio falls from 15.7% to 7.7% against a 7.0% hurdle; impairment accounts for 9.2 points of the fall.</li>
<li>Express the reverse stress test as a number: losses could be 1.08 times larger in the severe scenario before the hurdle is reached, which is a cumulative loss rate of 9.1%.</li>
</ul></div>

<h2><span class="n">1</span>Three channels, not one</h2>
<p>A credit stress hits capital through three routes, and a model that only produces a loss rate captures one of them.</p>
<ul>
<li><b>Impairment.</b> Defaults, and the move from 12-month to lifetime allowances as loans migrate into Stage 2. In the early years of a stress the second part
can be as large as the first.</li>
<li><b>Risk-weighted assets.</b> Under the standardised approach, defaulted exposures and higher loan-to-value mortgages carry
higher weights. The denominator of the ratio rises while the numerator falls.</li>
<li><b>Earnings.</b> Lower income on non-performing loans and reduced pre-provision profit reduce the buffer that absorbs
losses before they reach capital.</li>
</ul>

<h2><span class="n">2</span>Shift the whole matrix</h2>
<p>The demo model converts each scenario's macro path into a credit cycle index (the construction is in Method Note No. 2)
and applies it to the transition matrix segment by segment. It does this on the cumulative "at or worse than" probabilities
in each row, in log-odds:</p>
<div class="formula">P(k or worse | stressed) = logistic( logit P(k or worse | TTC) + beta(segment) × index )
P(end in grade k) = P(k or worse) − P(k+1 or worse)</div>
<p>Shifting the cumulative row moves probability mass towards worse grades all the way along it. Downgrades and defaults
both rise, each row still sums to 100%, and the ordering of grades is preserved. A loan that is downgraded but does not
default still costs capital: it may cross the Stage 2 threshold and take a lifetime allowance, and it carries a higher
expected loss in later years.</p>

<h2><span class="n">3</span>Collateral has its own path</h2>
<p>Each scenario carries a collateral value path alongside the macro variables, and the severity dial scales both. Falling
values do two things. LGD rises, because less of the exposure is covered after the forced-sale haircut. And for residential
mortgages the indexed loan-to-value ratio rises, which can move a loan into a higher standardised risk-weight band. That is the
part most simple stress tests leave out, and it is why RWA can rise in a stress even when the book is not growing.</p>

<h2><span class="n">4</span>The CET1 path and the bridge</h2>
<p>The demo bank starts with £30.0m CET1 against £191.0m RWA, a CET1 ratio of 15.7%. The stress hurdle is 7.0% (Pillar 1
plus Pillar 2A, with buffers treated as usable in stress); the baseline requirement including buffers is 10.5%.</p>
<table>
<tr><th>Scenario</th><th>Lowest CET1 ratio</th><th>Year of low point</th><th>Hurdle</th><th>Headroom</th><th>Headroom (£)</th></tr>
<tr><td>Baseline</td><td>16.30%</td><td>1</td><td>10.5%</td><td>5.80pp</td><td>£11.08m</td></tr>
<tr><td>Adverse</td><td>14.07%</td><td>2</td><td>7.0%</td><td>7.07pp</td><td>£13.89m</td></tr>
<tr class="hl"><td>Severely adverse</td><td>7.73%</td><td>3</td><td>7.0%</td><td>0.73pp</td><td>£1.47m</td></tr>
</table>
<p class="cap">Before management actions. Source: CAPITAL and REVERSE tabs, demo bank.</p>
<p>A board pack should then show <i>why</i> the ratio moved. The bridge expresses each three-year income and loss line as a
share of year-3 RWA, plus a separate line for the dilution of starting capital by the change in RWA, so the steps add up to
the reported ratio exactly.</p>
<div class="fig"><div class="figt">CET1 ratio bridge, severely adverse scenario, start to end of year 3 (percentage points)</div>{n3_wf}</div>
<p class="cap">Source: BRIDGE tab. Tax and dividends are nil: no tax relief is recognised on losses, and no dividend is paid without a profit.</p>
<p>Three readings from it. Impairment is the story, at 9.19 points. Pre-provision profit offsets about a quarter of it. And the
RWA line, 0.77 points, is small next to impairment but is the difference between passing and failing here: without it the
headroom would be 1.50 points rather than 0.73. A stress test that held RWA flat would have shown roughly twice the real margin.</p>
<p>In the adverse scenario the same bridge runs 15.71% + 4.16 − 5.07 − 0.15 − 0.04 (tax) − 0.04 (dividends) − 0.41 (RWA) =
14.15% at the end of year 3, recovering slightly from a low point of 14.07% in year 2.</p>

<h2><span class="n">5</span>Reverse stress: a number, not a narrative</h2>
<p>Reverse stress testing asks what it would take to break the bank. It is often answered with a story. A first-order numeric
answer is easy to produce from the same model and gives the narrative something to be checked against.</p>
<div class="formula">Headroom at low point        = CET1 at low point − hurdle × RWA at low point
Further pre-tax losses       = headroom / (1 − tax rate × tax relief flag)
Losses could be ... × larger = 1 + further losses / losses already taken to the low point
Breaking loss rate           = (further losses + losses taken) / exposure</div>
<table>
<tr><th></th><th>Adverse</th><th>Severely adverse</th></tr>
<tr><td>CET1 headroom at the low point</td><td>£13.89m</td><td>£1.47m</td></tr>
<tr><td>Losses already taken to the low point</td><td>£8.37m</td><td>£19.27m</td></tr>
<tr class="hl"><td>Losses could be this many times larger</td><td>2.66×</td><td>1.08×</td></tr>
<tr><td>Cumulative loss rate at which the hurdle is reached</td><td>9.78%</td><td>9.11%</td></tr>
</table>
<p class="cap">Source: REVERSE tab. Exposure £227.7m. First-order estimate: holds RWA, income and dividends at their stressed levels.</p>
<p>The two breaking loss rates differ because the scenarios reach their low points in different years with different RWA and
income. Either way, the board can be told in one sentence that a cumulative credit loss of around 9% to 10% of the book
over the horizon would take the bank to its hurdle. That is a statement it can compare with history and with its risk appetite.</p>

<h2><span class="n">6</span>Show sensitivity to depth, not just one path</h2>
<p>A single adverse path invites the question "and if it were worse?" A severity dial that scales the adverse scenarios' index and
collateral falls together (1.0×, 0.75× and 1.25× across the model's three input cases) answers it with three runs of the same model, and
lets the board see whether capital degrades smoothly or falls off a cliff. Management actions sit on top: in the demo, a nil
dividend, a 5% saving on operating costs and a 10% reduction in RWA outside the tape, applied to the adverse scenarios only, with
results available before and after so the actions are never buried in the base result.</p>

<h2><span class="n">7</span>ICAAP checklist</h2>
<ul class="check">
<li>The full matrix is stressed, so Stage 2 migration and RWA inflation come through, not only defaults.</li>
<li>Collateral values follow their own path into LGD and loan-to-value risk-weight bands.</li>
<li>CET1 path and low point for each scenario against the right hurdle (buffers usable in stress, or not, stated).</li>
<li>A bridge from starting to ending ratio that reconciles to the capital plan exactly.</li>
<li>A numeric reverse stress result: the loss multiple and the breaking cumulative loss rate.</li>
<li>Results before and after management actions, with each action stated.</li>
<li>Sensitivity to the depth of the stress, not only one adverse path.</li>
</ul>
""")

NOTES = [NOTE1, NOTE2, NOTE3]


def render(note):
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / f"{note['slug']}.pdf"
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / f"{note['slug']}.html"
        src.write_text(page(note), encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", src.as_uri()],
                       check=True, capture_output=True)
    return pdf


if __name__ == "__main__":
    index = []
    for n in NOTES:
        pdf = render(n)
        print(f"Wrote {pdf.relative_to(HERE)} ({pdf.stat().st_size // 1024} KB)")
        index.append({k: n[k] for k in ("slug", "no", "topic", "date_label", "title", "dek", "summary",
                                         "model_name", "model_url")} | {"pdf": f"/research/notes/{n['slug']}.pdf"})
    (HERE / "research" / "notes.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print("Wrote research/notes.json")
