#!/usr/bin/env python3
"""Build the SFS Models method notes as PDFs.

Each note is written below as HTML, rendered to research/notes/<slug>.pdf with
headless Chrome, and listed in research/notes.json for build_research_index.py.

Worked figures come from the demo books inside the named models
(models/final/*.xlsx, cached values as last calculated in Excel). If a model's
demo book changes, re-read the figures and update the note.

House style: a methodology paper, not a marketing piece. Numbered sections,
running prose, ruled tables with numbered captions, references at the end.
No summary boxes, tick-box checklists, call-out panels or "X, not Y" headings.

Run:  python3 build_method_notes.py   (then python3 build_research_index.py
      and python3 add_analytics.py)
"""
import json, re, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "research" / "notes"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "https://sfsmodels.org"

NAVY, GREY, LIGHT = "#1F3864", "#5F6368", "#E4E6EA"
MID, NEG = "#8C9BB5", "#9E3B32"
FONT = "'Source Sans 3', Arial, sans-serif"


# ── chart helpers (inline SVG) ───────────────────────────────────────────────
def hbar_svg(rows, unit="", width=640, bar_h=22, gap=12, label_w=170):
    """Horizontal bars. rows = [(label, value)]."""
    vmax = max(v for _, v in rows) or 1
    plot_w = width - label_w - 80
    h = len(rows) * (bar_h + gap) + 6
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="{FONT}" font-size="12.5">']
    for i, (lab, v) in enumerate(rows):
        y = 3 + i * (bar_h + gap)
        w = max(2, plot_w * v / vmax)
        u = unit[:-1] if v == 1 and unit.endswith("s") else unit
        out.append(f'<text x="{label_w - 10}" y="{y + bar_h * 0.7}" text-anchor="end" fill="#222">{lab}</text>')
        out.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{NAVY}"/>')
        out.append(f'<text x="{label_w + w + 7:.1f}" y="{y + bar_h * 0.7}" fill="#222">{v:g}{u}</text>')
    out.append("</svg>")
    return "".join(out)


def line_svg(series, xlabels, ymax, yfmt=lambda v: f"{v:.0f}%", width=640, height=260, yticks=4):
    """series = [(name, [values], colour, dashed_bool)]."""
    L, R, T, B = 48, 16, 12, 44
    pw, ph = width - L - R, height - T - B
    n = len(xlabels)
    x = lambda i: L + pw * i / (n - 1)
    y = lambda v: T + ph * (1 - v / ymax)
    out = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="{FONT}" font-size="12">']
    for k in range(yticks + 1):
        v = ymax * k / yticks
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{LIGHT}"/>')
        out.append(f'<text x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end" fill="{GREY}">{yfmt(v)}</text>')
    out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(0):.1f}" y2="{y(0):.1f}" stroke="#555"/>')
    for i, lab in enumerate(xlabels):
        out.append(f'<text x="{x(i):.1f}" y="{height - B + 18}" text-anchor="middle" fill="{GREY}">{lab}</text>')
    lx = L
    for name, vals, col, dashed in series:
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')
        out.append(f'<line x1="{lx}" x2="{lx + 24}" y1="{height - 8}" y2="{height - 8}" stroke="{col}" stroke-width="2"{dash}/>')
        out.append(f'<text x="{lx + 30}" y="{height - 4}" fill="#222">{name}</text>')
        lx += 30 + 6.6 * len(name) + 26
    out.append("</svg>")
    return "".join(out)


def waterfall_svg(steps, ymin, ymax, hurdle=None, width=640, height=290):
    """steps = [(label, value, kind)] kind in start|delta|end. Values in % points."""
    L, R, T, B = 44, 12, 14, 52
    pw, ph = width - L - R, height - T - B
    n = len(steps)
    slot = pw / n
    bw = slot * 0.58
    y = lambda v: T + ph * (ymax - v) / (ymax - ymin)
    out = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="{FONT}" font-size="11.5">']
    for k in range(int(ymin), int(ymax) + 1, 4):
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(k):.1f}" y2="{y(k):.1f}" stroke="{LIGHT}"/>')
        out.append(f'<text x="{L - 7}" y="{y(k) + 4:.1f}" text-anchor="end" fill="{GREY}">{k}%</text>')
    out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(ymin):.1f}" y2="{y(ymin):.1f}" stroke="#555"/>')
    if hurdle is not None:
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(hurdle):.1f}" y2="{y(hurdle):.1f}" '
                   f'stroke="#333" stroke-width="1" stroke-dasharray="4 3"/>')
        out.append(f'<text x="{L + slot * 4.5:.1f}" y="{y(hurdle) + 14:.1f}" text-anchor="middle" fill="#333">'
                   f'Stress hurdle {hurdle:.1f}%</text>')
    run = 0.0
    for i, (lab, v, kind) in enumerate(steps):
        cx = L + slot * i + (slot - bw) / 2
        if kind in ("start", "end"):
            top, bot, col, run = v, ymin, NAVY, v
            txt = f"{v:.2f}"
        else:
            top, bot = (run + v, run) if v >= 0 else (run, run + v)
            col = MID if v >= 0 else NEG
            run += v
            txt = "0.00" if v == 0 else f"{v:+.2f}".replace("-", "\u2212")
        out.append(f'<rect x="{cx:.1f}" y="{y(top):.1f}" width="{bw:.1f}" height="{max(1, y(bot) - y(top)):.1f}" fill="{col}"/>')
        out.append(f'<text x="{cx + bw / 2:.1f}" y="{y(top) - 5:.1f}" text-anchor="middle" fill="#222">{txt}</text>')
        for j, part in enumerate(lab.split("|")):
            out.append(f'<text x="{cx + bw / 2:.1f}" y="{height - B + 17 + j * 14}" text-anchor="middle" fill="{GREY}">{part}</text>')
    out.append("</svg>")
    return "".join(out)


# ── page template ────────────────────────────────────────────────────────────
CSS = """
@page { size: A4; margin: 22mm 22mm 20mm 22mm;
  @bottom-left { content: "SFS Models  |  Method Note " var(--no); font: 7.5pt 'Source Sans 3', Arial; color: #777; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 7.5pt 'Source Sans 3', Arial; color: #777; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Source Serif 4', Georgia, serif; font-size: 10.3pt; line-height: 1.5; color: #1A1A1A; margin: 0;
  hyphens: auto; }
.sans, .runhead, h2, h3, table, .cap, .src, .meta, .label { font-family: 'Source Sans 3', Arial, sans-serif; }
.runhead { display: flex; justify-content: space-between; font-size: 8pt; color: #555;
  border-bottom: 0.75pt solid #1A1A1A; padding-bottom: 5px; }
.runhead b { color: #1F3864; font-weight: 700; }
h1 { font-weight: 600; font-size: 20pt; line-height: 1.2; color: #1A1A1A; margin: 26px 0 8px; }
.sub { font-size: 11.5pt; line-height: 1.45; color: #444; margin: 0 0 12px; }
.meta { font-size: 8.5pt; color: #555; margin: 0 0 18px; line-height: 1.6; }
.label { font-size: 8.5pt; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: #1F3864; margin: 0 0 3px; }
.abstract { border-top: 0.5pt solid #999; border-bottom: 0.5pt solid #999; padding: 9px 0 10px; margin: 0 0 6px; }
.abstract p { margin: 0; font-size: 10pt; }
h2 { font-size: 12pt; font-weight: 700; color: #1F3864; margin: 20px 0 6px; break-after: avoid; }
h2 .n { display: inline-block; min-width: 22px; }
p { margin: 0 0 8px; text-align: justify; }
ol { margin: 4px 0 10px; padding-left: 22px; } ol li { margin: 3px 0; }
.cap { font-size: 8.8pt; font-weight: 700; margin: 12px 0 4px; break-after: avoid; }
.cap span { font-weight: 400; }
table { width: 100%; border-collapse: collapse; font-size: 8.9pt; border-top: 1pt solid #1A1A1A;
  border-bottom: 1pt solid #1A1A1A; margin: 0 0 3px; break-inside: avoid; }
th { font-weight: 600; text-align: right; padding: 5px 6px 4px; border-bottom: 0.6pt solid #1A1A1A; vertical-align: bottom; }
td { padding: 3px 6px; text-align: right; font-variant-numeric: tabular-nums; }
th:first-child, td:first-child { text-align: left; padding-left: 0; }
th:last-child, td:last-child { padding-right: 0; }
tr.tot td { border-top: 0.6pt solid #1A1A1A; font-weight: 600; }
.src { font-size: 7.8pt; color: #555; margin: 0 0 12px; }
.fig { break-inside: avoid; }
.eq { font-family: 'Source Sans 3', Arial, sans-serif; font-size: 9.2pt; margin: 6px 0 10px 18px; line-height: 1.7;
  break-inside: avoid; }
.refs { font-size: 8.5pt; color: #333; } .refs p { margin: 0 0 2px; text-align: left; }
.legal { font-family: 'Source Sans 3', Arial, sans-serif; font-size: 7.6pt; color: #666; border-top: 0.5pt solid #999;
  padding-top: 7px; margin-top: 16px; text-align: left; }
a { color: #1F3864; text-decoration: none; hyphens: manual; white-space: nowrap; }
"""


def page(note):
    body = re.sub(r'(<div class="cap">[^<]*<span>[^<]*</span></div>\s*<table>.*?</table>\s*<p class="src">.*?</p>)',
                  r'<div class="fig">\1</div>', note['body'], flags=re.S)
    refs = "".join(f"<p>[{i}] {r}</p>" for i, r in enumerate(note.get("refs", []), 1))
    refs_block = f'<h2>References</h2><div class="refs">{refs}</div>' if refs else ""
    return f"""<!DOCTYPE html><html lang="en" style="--no: '{note['no']}'"><head><meta charset="utf-8">
<title>{note['title']} | SFS Models Method Note {note['no']}</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<style>{CSS.replace('var(--no)', '"' + str(note['no']) + '"')}</style></head><body>
<div class="runhead"><span><b>SFS Models</b>&nbsp;&nbsp;Method Note {note['no']}</span><span>{note['topic']}&nbsp;&nbsp;|&nbsp;&nbsp;{note['date_label']}</span></div>
<h1>{note['title']}</h1>
<p class="sub">{note['dek']}</p>
<p class="meta">Related model: {note['model_name']}<br>Figures: demo data supplied with the model</p>
<div class="abstract"><div class="label">Summary</div><p>{note['abstract']}</p></div>
{body}
<h2>The model</h2>
<p style="text-align:left">{note['model_para']} The free sample, with inputs locked, runs on the same demo data used in this note:
<a href="{SITE}/{note['model_url']}">sfsmodels.org/{note['model_url']}</a>.</p>
{refs_block}
<p class="legal">This note describes general modelling methodology. The figures relate to illustrative demo data and not to any
institution. It is not accounting, regulatory or investment advice. © 2026 SFS Models, sfsmodels.org.</p>
</body></html>"""


# ── NOTE 1: SICR ─────────────────────────────────────────────────────────────
n1_bar = hbar_svg([("PD test", 80), ("30+ days past due", 45), ("Watchlist", 22),
                   ("Forbearance", 9), ("Rating downgrade", 1)], unit=" loans")

NOTE1 = dict(
    slug="sicr-staging-triggers", no=1, topic="IFRS 9", date_label="November 2026",
    title="Designing the SICR assessment under IFRS 9",
    dek="Relative and absolute PD thresholds, qualitative triggers and the evidence needed to support a Stage 2 population",
    model_name="IFRS 9 ECL Model: Loan-Level Edition", model_url="ifrs9-loan-level-ecl-model-excel.html",
    summary="How a relative PD threshold behaves across a rating scale, which triggers stage the demo portfolio, "
            "and how much the allowance moves when the threshold changes.",
    abstract="A relative threshold applied to lifetime PD does not treat all grades alike. On the demo rating scale, a "
             "2× threshold classifies a one-notch downgrade as significant for grades 3 and 4 but not for grades 5 to 7, "
             "although the absolute increase in default risk is much larger for the weaker grades. This note sets out "
             "the components of the assessment used in the model, shows which of them place loans in Stage 2 in the demo "
             "portfolio, and quantifies the effect of the threshold on the allowance. Moving the threshold from 2× to 1.5× "
             "increases the allowance by 9.7%; moving it to 3× reduces it by 1.4%.",
    model_para="The IFRS 9 ECL Model: Loan-Level Edition applies the assessment described here to a loan tape of up to "
               "1,000 loans. It records the triggers met and the first reason for every Stage 2 loan, and re-stages the "
               "portfolio at alternative thresholds to produce the analysis in Table 2.",
    refs=["IFRS 9 <i>Financial Instruments</i>, paragraph 5.5.3.",
          "IFRS 9, paragraph 5.5.9.",
          "IFRS 9, paragraph 5.5.11.",
          "IFRS 9, paragraph 5.5.10."],
    body=f"""
<h2><span class="n">1</span>Introduction</h2>
<p>Most staging policies at smaller lenders combine a PD-based test, a days-past-due backstop and a small number of
qualitative flags. None of these components is unusual in itself. The difficulty lies in how they interact across a rating
scale, and in being able to explain afterwards why a particular loan moved. This note describes the approach taken in the
IFRS 9 ECL Model: Loan-Level Edition and illustrates each step with the model's demo portfolio of 1,000 loans.</p>

<h2><span class="n">2</span>The requirement</h2>
<p>At each reporting date an entity assesses whether credit risk on a financial instrument has increased significantly
since initial recognition [1]. The comparison is between the risk of a default occurring over the expected life of the
instrument at the reporting date and the same risk at initial recognition [2]. A 12-month PD may be used where it gives a
reasonable approximation of that comparison, although for longer-dated or back-loaded exposures it often does not.</p>
<p>The standard also contains a rebuttable presumption that credit risk has increased significantly once contractual
payments are more than 30 days past due [3]. That presumption is intended as a backstop. A loan that first reaches Stage 2
through arrears was not identified by the forward-looking assessment, and a large share of such loans in the Stage 2
population usually means that the PD test is reacting late.</p>

<h2><span class="n">3</span>The relative PD threshold</h2>
<p>The primary quantitative test in the model compares lifetime PD over the remaining term at the current grade with
lifetime PD over the same term at the origination grade. Holding the term constant removes the increase in cumulative PD
that comes from horizon alone. Both curves are compounded from the same transition matrix, which is the subject of
Method Note 2.</p>
<p>A threshold of 2× is a common starting point. Table 1 shows its effect across the demo rating scale for a one-notch
downgrade with four years remaining. One-year PDs on this scale double from each grade to the next, from 0.03% at grade 1 to
28% at grade 10.</p>
<div class="cap">Table 1 <span>Four-year lifetime PD before and after a one-notch downgrade</span></div>
<table>
<tr><th>Origination grade</th><th>At origination grade</th><th>One notch lower</th><th>Ratio</th><th>Increase (pp)</th><th>Test met at 2× and 0.5pp</th></tr>
<tr><td>1 Exceptional</td><td>0.16%</td><td>0.40%</td><td>2.54</td><td>0.24</td><td>No: absolute</td></tr>
<tr><td>2 Very strong</td><td>0.40%</td><td>0.96%</td><td>2.40</td><td>0.56</td><td>Yes, but exempt (a)</td></tr>
<tr><td>3 Strong</td><td>0.96%</td><td>2.10%</td><td>2.19</td><td>1.14</td><td>Yes</td></tr>
<tr><td>4 Good</td><td>2.10%</td><td>4.21%</td><td>2.01</td><td>2.11</td><td>Yes</td></tr>
<tr><td>5 Satisfactory</td><td>4.21%</td><td>8.20%</td><td>1.95</td><td>3.99</td><td>No: relative</td></tr>
<tr><td>6 Acceptable</td><td>8.20%</td><td>15.24%</td><td>1.86</td><td>7.04</td><td>No: relative</td></tr>
<tr><td>7 Watch</td><td>15.24%</td><td>27.28%</td><td>1.79</td><td>12.04</td><td>No: relative</td></tr>
</table>
<p class="src">(a) A loan now rated grade 3 or better falls within the low credit risk exemption and is not tested on PD.
Source: demo transition matrix, PD_CURVES tab.</p>
<p>As lifetime PDs approach 100% they flatten, so the ratio produced by a one-notch move falls as credit quality weakens.
At 2×, a one-notch downgrade counts as significant for grades 3 and 4 but not for grades 5 to 7, even though the absolute
increase at grade 7 is 12.0 percentage points against 1.1 at grade 3. For a two-notch move the ratio is above 2× for every
origination grade up to grade 8 (5.26 at grade 2, 3.62 at grade 5 and 2.59 at grade 8).</p>
<p>This outcome may be acceptable, but it should be chosen rather than inherited. A lender that wants a one-notch
downgrade to count across the scale can set the multiple by origination grade. A lender that accepts a two-notch standard
for weaker grades should say so in the policy, so that the auditor is not the first to notice it.</p>

<h2><span class="n">4</span>The absolute threshold and the low credit risk exemption</h2>
<p>A relative threshold used alone produces the opposite problem at the top of the scale. A move from 0.16% to 0.40%
lifetime PD is an increase of 2.5 times, yet the exposure remains very low risk. The model therefore also requires an
absolute increase of at least 0.5 percentage points before the PD test is met.</p>
<p>The low credit risk exemption [4] is applied to grades 1 to 3 in the demo set-up, equivalent to a one-year PD of 0.20% or
less. Twelve loans in the demo portfolio met the PD test but stayed in Stage 1 under the exemption. We would report that
number alongside the stage split, because it shows directly how much the exemption is affecting the result.</p>

<h2><span class="n">5</span>Qualitative triggers</h2>
<p>Ratings are usually refreshed on a cycle, so the PD test can lag information that the credit team already holds. The
model includes three further triggers: a downgrade of three or more notches since origination, inclusion on the watchlist,
and forbearance. The downgrade trigger also catches the weaker-grade cases in Table 1, where a substantial move does not meet
the relative threshold. Watchlist and forbearance are treated as automatic Stage 2 triggers. That is a common choice,
though the standard does not require it.</p>

<h2><span class="n">6</span>Results on the demo portfolio</h2>
<p>The demo portfolio has 824 loans in Stage 1, 157 in Stage 2 and 19 in Stage 3. Because a loan can meet more than one
trigger, the model also assigns each Stage 2 loan a single first reason, using a fixed order of precedence. Figure 1 shows
the result.</p>
<div class="fig"><div class="cap">Figure 1 <span>Stage 2 loans by first reason, demo portfolio (157 loans)</span></div>{n1_bar}
<p class="src">Loans meeting each trigger in total: PD test 96, downgrade 49, watchlist 39, forbearance 21, 30+ days past due 45.
Source: STAGING tab, section C.</p></div>
<p>The PD test is the first reason for 80 loans (51%) and the days-past-due backstop for 45 (29%). The downgrade trigger is
met by 49 loans but is the first reason for only one. That is the expected pattern if it is acting as a backstop to the PD
test rather than driving staging on its own. In a live portfolio, the share of Stage 2 reached through arrears alone is the
figure we would follow most closely from one reporting date to the next.</p>

<h2><span class="n">7</span>Sensitivity to the threshold</h2>
<p>The relative threshold is a judgement, and a committee can approve it more readily when it sees the effect of the
alternatives. The model re-stages the whole portfolio at 1.5× and at 3×.</p>
<div class="cap">Table 2 <span>Effect of the relative PD threshold on staging and the allowance</span></div>
<table>
<tr><th>Relative threshold</th><th>1.5×</th><th>2.0× (in use)</th><th>3.0×</th></tr>
<tr><td>Stage 2 loans</td><td>214</td><td>157</td><td>137</td></tr>
<tr><td>Stage 2 share of exposure</td><td>21.9%</td><td>14.9%</td><td>13.1%</td></tr>
<tr><td>Loss allowance (£m)</td><td>4.76</td><td>4.33</td><td>4.27</td></tr>
<tr><td>Change in allowance</td><td>+9.7%</td><td></td><td>(1.4%)</td></tr>
</table>
<p class="src">Exposure at default £227.7m. Source: SENSITIVITY tab.</p>
<p>The effect is uneven. At 1.5× a further 57 loans move to Stage 2 and the allowance rises by 9.7%; at 3× twenty loans
return to Stage 1 and the allowance falls by 1.4%. A sizeable group of loans therefore sits between 1.5× and 2×. As outer
bounds, the allowance before overlay would be £3.12m with every performing loan in Stage 1 and £6.18m with every performing
loan in Stage 2, against £4.23m as staged.</p>

<h2><span class="n">8</span>Documentation</h2>
<p>For each reporting date we would expect the staging file to show:</p>
<ol>
<li>the triggers met by each Stage 2 loan and its first reason;</li>
<li>the share of Stage 2 reached through days past due alone, and how it has moved;</li>
<li>the effect of the relative threshold across the rating scale, in the form of Table 1;</li>
<li>the number of loans held in Stage 1 by the absolute threshold and by the low credit risk exemption;</li>
<li>the allowance at alternative thresholds, with the all-Stage 1 and all-Stage 2 bounds;</li>
<li>transfers between stages in the period, reconciled to the IFRS 7 disclosure.</li>
</ol>
<p>With this in place, a question about a single exposure can be answered from the file: for example, that the loan was
downgraded three notches and met the relative PD test at the same reporting date.</p>
""")


# ── NOTE 2: lifetime PD and forward-looking adjustment ───────────────────────
n2_line = line_svg([
    ("Through-the-cycle", [0.900, 1.901, 3.005, 4.212, 5.516], MID, True),
    ("SME, downside scenario", [1.585, 3.208, 4.609, 5.888, 7.163], NAVY, False)],
    ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], ymax=8, yfmt=lambda v: f"{v:.0f}%", yticks=4)

NOTE2 = dict(
    slug="lifetime-pd-forward-looking", no=2, topic="IFRS 9", date_label="November 2026",
    title="Lifetime PD under IFRS 9: from transition matrix to forward-looking curves",
    dek="Compounding a rating transition matrix, summarising macroeconomic scenarios in a credit cycle index, and "
        "probability-weighting the result",
    model_name="IFRS 9 ECL Model: Loan-Level Edition", model_url="ifrs9-loan-level-ecl-model-excel.html",
    summary="Deriving lifetime PD curves from one transition matrix, adjusting them for macroeconomic scenarios, and why "
            "the weighted allowance in the demo portfolio is 23.8% above the baseline.",
    abstract="Lifetime PD curves are often held as a fixed table by grade and year, which makes them hard to explain and "
             "harder to update. This note derives every curve from a single one-year transition matrix, adjusts the "
             "resulting hazard rates for each macroeconomic scenario using a credit cycle index, and measures the allowance "
             "under four weighted scenarios. In the demo portfolio the probability-weighted allowance is £4.23m, 23.8% "
             "above the baseline result of £3.42m, because losses rise faster in adverse scenarios than they fall in "
             "favourable ones.",
    model_para="The IFRS 9 ECL Model: Loan-Level Edition builds its PD curves in this way on the PD_CURVES and MACRO tabs "
               "and measures every loan under four scenarios with three alternative sets of weights.",
    refs=["IFRS 9 <i>Financial Instruments</i>, paragraph 5.5.17(a)."],
    body=f"""
<h2><span class="n">1</span>Introduction</h2>
<p>Lifetime PD curves sit underneath both the staging assessment and the Stage 2 allowance. At many smaller lenders they
are held as a static table by grade and year, often inherited from a vendor or an earlier calibration. A table of that kind
is difficult to explain when a reviewer asks where a particular value came from, and it has to be re-entered by hand
whenever the view of risk changes. This note describes the approach used in the IFRS 9 ECL Model: Loan-Level Edition, in
which every curve is derived from a single transition matrix and a set of macroeconomic scenarios.</p>

<h2><span class="n">2</span>Cumulative PD from a transition matrix</h2>
<p>Let M be a one-year through-the-cycle transition matrix in which default is an absorbing state. The probability that a
borrower starting in grade g has defaulted within t years is the default entry in row g of M raised to the power t. In a
spreadsheet this can be built without matrix functions by rolling forward one year at a time:</p>
<div class="eq">C(t, g) = SUMPRODUCT( row g of M, C(t − 1, all grades) )<br>
with C(0, g) = 0 for each performing grade and C(0, default) = 1.</div>
<p>The marginal, or hazard, rate for year t is h(t) = (C(t) − C(t − 1)) / (1 − C(t − 1)): the probability of default in year
t for a borrower that has survived to the start of it. Table 1 shows both measures for grade 5 of the demo matrix.</p>
<div class="cap">Table 1 <span>Through-the-cycle PD, grade 5 (Satisfactory)</span></div>
<table>
<tr><th>Year</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><td>Cumulative PD</td><td>0.90%</td><td>1.90%</td><td>3.00%</td><td>4.21%</td><td>5.52%</td></tr>
<tr><td>Hazard rate</td><td>0.90%</td><td>1.01%</td><td>1.13%</td><td>1.24%</td><td>1.36%</td></tr>
</table>
<p class="src">Source: PD_CURVES tab, sections A and B.</p>
<p>The hazard rate for this grade rises over time because some surviving borrowers migrate to weaker grades. That shape
follows from the matrix and does not have to be imposed. Because all curves come from the same matrix, a change in the
matrix flows consistently through every grade and horizon. The model checks that each row of the matrix sums to 100%, that
cumulative PD never falls as the horizon lengthens, and that one-year PD rises with each grade.</p>

<h2><span class="n">3</span>The credit cycle index</h2>
<p>The matrix describes an average year. To produce point-in-time estimates, each scenario's macroeconomic path is summarised
in a credit cycle index. For each year, every variable is expressed as its deviation from a long-run mean in standard
deviations, signed so that a positive value indicates weaker credit conditions, and the results are combined using fixed
weights. Table 2 shows the calculation for the first year of the downside scenario.</p>
<div class="cap">Table 2 <span>Credit cycle index, downside scenario, year 1</span></div>
<table>
<tr><th>Variable</th><th>Long-run mean</th><th>Std. dev.</th><th>Sign</th><th>Weight</th><th>Year 1 value</th><th>Contribution</th></tr>
<tr><td>GDP growth</td><td>1.6%</td><td>1.8%</td><td>−1</td><td>30%</td><td>(0.8%)</td><td>0.400</td></tr>
<tr><td>Unemployment rate</td><td>5.0%</td><td>1.4%</td><td>+1</td><td>35%</td><td>5.8%</td><td>0.200</td></tr>
<tr><td>House price growth</td><td>3.5%</td><td>6.0%</td><td>−1</td><td>20%</td><td>(6.0%)</td><td>0.317</td></tr>
<tr><td>Policy rate</td><td>3.0%</td><td>1.8%</td><td>+1</td><td>15%</td><td>4.5%</td><td>0.125</td></tr>
<tr class="tot"><td>Index</td><td></td><td></td><td></td><td>100%</td><td></td><td>1.042</td></tr>
</table>
<p class="src">For GDP: (−0.8% − 1.6%) / 1.8% = −1.33 standard deviations; × −1 × 30% = 0.400. Source: MACRO tab.</p>
<p>Over the five projection years the demo index moves between +0.08 and −0.14 in the baseline, falls from +1.04 to about zero
in the downside, and from +2.19 to +0.15 in the severe downside. After year 5 it reverts in a straight line to zero over three
years, so long-dated exposures return to through-the-cycle risk.</p>
<p>The variable weights are a judgement. Where there is enough default history they can be estimated by regression. Where
there is not, they should be documented as an expert assumption and reviewed with the scenarios themselves.</p>

<h2><span class="n">4</span>Point-in-time hazard rates</h2>
<p>Each portfolio segment has a sensitivity, beta, to the index. The point-in-time hazard rate is the through-the-cycle
hazard adjusted in log-odds:</p>
<div class="eq">PIT hazard = 1 / ( 1 + EXP( −( LN( h / (1 − h) ) + beta × index ) ) )</div>
<p>Working in log-odds keeps every result between zero and one and gives proportionally larger moves to low hazard rates.
Applying the adjustment to the hazard rates rather than to the cumulative curve keeps the cumulative curve increasing.
Figure 1 shows the effect for an SME loan at grade 5, where beta is 0.55, in the downside scenario.</p>
<div class="fig"><div class="cap">Figure 1 <span>Cumulative PD, grade 5: through-the-cycle and SME downside</span></div>{n2_line}
<p class="src">Source: PD_CURVES tab.</p></div>
<p>The year 1 hazard rises from 0.90% to 1.59%. By year 5 the index has largely reverted and the hazard is close to its
through-the-cycle level, but cumulative PD remains 1.6 percentage points higher because of the earlier years.</p>
<p>One property of this construction is useful in review. With the index set to zero, the adjustment term is zero and the
point-in-time curves are identical to the through-the-cycle curves. Any difference between the two in a model under review
must therefore come from something other than the macroeconomic adjustment.</p>

<h2><span class="n">5</span>From PD to the allowance</h2>
<p>For each loan, scenario and year, expected loss is the marginal PD multiplied by LGD and exposure at default, discounted at
the effective interest rate. Stage 1 loans are measured over the next twelve months and Stage 2 loans over their remaining
life. Table 3 shows the resulting coverage in the demo portfolio.</p>
<div class="cap">Table 3 <span>Allowance and coverage by stage</span></div>
<table>
<tr><th>Stage</th><th>Loans</th><th>Exposure (£m)</th><th>Allowance (£m)</th><th>Coverage</th></tr>
<tr><td>Stage 1</td><td>824</td><td>190.5</td><td>1.19</td><td>0.62%</td></tr>
<tr><td>Stage 2</td><td>157</td><td>34.0</td><td>2.08</td><td>6.12%</td></tr>
<tr><td>Stage 3</td><td>19</td><td>3.2</td><td>1.06</td><td>33.4%</td></tr>
<tr class="tot"><td>Total</td><td>1,000</td><td>227.7</td><td>4.33</td><td>1.90%</td></tr>
</table>
<p class="src">Includes a management overlay of £0.11m, 2.5% of modelled ECL. Source: STAGING tab, section A.</p>
<p>Coverage rises from 0.62% in Stage 1 to 6.12% in Stage 2, which is why the staging assessment in Method Note 1 carries so
much weight in the total.</p>

<h2><span class="n">6</span>Probability weighting</h2>
<p>The allowance must reflect an unbiased and probability-weighted amount, determined by evaluating a range of possible
outcomes [1]. Table 4 sets out the scenario results and weights for the demo portfolio.</p>
<div class="cap">Table 4 <span>Allowance by scenario, before overlay</span></div>
<table>
<tr><th>Scenario</th><th>Weight</th><th>Allowance (£m)</th><th>Weighted (£m)</th></tr>
<tr><td>Baseline</td><td>40%</td><td>3.42</td><td>1.37</td></tr>
<tr><td>Upside</td><td>20%</td><td>2.93</td><td>0.59</td></tr>
<tr><td>Downside</td><td>30%</td><td>4.94</td><td>1.48</td></tr>
<tr><td>Severe downside</td><td>10%</td><td>7.94</td><td>0.79</td></tr>
<tr class="tot"><td>Probability-weighted</td><td>100%</td><td></td><td>4.23</td></tr>
</table>
<p class="src">Weighted amounts are rounded. Source: SCENARIOS and OUTPUTS tabs.</p>
<p>The weighted allowance of £4.23m is £0.81m, or 23.8%, above the baseline. Against the baseline, the upside scenario reduces
the allowance by £0.49m and the severe downside increases it by £4.53m. Two features of the model produce this asymmetry.
Under the log-odds adjustment, a rise in the index increases hazard rates by more than an equal fall reduces them; and in the
adverse scenarios more loans pass the staging thresholds and are measured on a lifetime basis.</p>
<p>We would present the baseline and weighted results together, along with the effect of alternative weights. The model
holds three weight sets, which give allowances of £3.80m, £4.23m and £4.88m.</p>

<h2><span class="n">7</span>Validation</h2>
<p>The model's integrity checks cover the points a reviewer would normally test:</p>
<ol>
<li>each row of the transition matrix sums to 100%, and default is absorbing;</li>
<li>cumulative PD does not fall as the horizon lengthens, and one-year PD rises with each grade;</li>
<li>index weights and scenario weights each sum to 100%;</li>
<li>the probability-weighted total agrees with the allowance before overlay;</li>
<li>the movement table and IFRS 7 disclosures reconcile to the loan-level results.</li>
</ol>
""")


# ── NOTE 3: credit stress test and capital ───────────────────────────────────
n3_wf = waterfall_svg([
    ("Start", 15.71, "start"), ("Pre-provision|profit", 2.39, "delta"),
    ("Impairment", -9.19, "delta"), ("Other|losses", -0.40, "delta"),
    ("Tax and|dividends", 0.0, "delta"), ("RWA|effect", -0.77, "delta"),
    ("End of|year 3", 7.73, "end")], ymin=0, ymax=20, hurdle=7.0)

NOTE3 = dict(
    slug="credit-stress-test-capital", no=3, topic="Stress testing", date_label="November 2026",
    title="Credit stress testing and capital: migration, risk-weighted assets and reverse stress",
    dek="Taking a loan-level credit stress through to the CET1 ratio, explaining the movement, and quantifying the "
        "distance to the hurdle",
    model_name="Credit Stress Test & Capital Model", model_url="credit-stress-test-model-excel.html",
    summary="Taking a credit stress through rating migration, risk-weighted assets and earnings to the CET1 ratio, with a "
            "quantified reverse stress test on the demo bank.",
    abstract="A stressed loss rate by portfolio captures only one of the routes by which a credit stress reaches capital. "
             "This note stresses the full transition matrix, so that rating migration affects both the allowance and "
             "risk-weighted assets, and follows the result through to the CET1 ratio. In the severely adverse scenario "
             "the demo bank's ratio falls from 15.7% to 7.7% against a hurdle of 7.0%. The increase in risk-weighted "
             "assets accounts for 0.77 percentage points of the fall, close to the 0.73 points of headroom that remain. "
             "A first-order reverse stress test puts the cumulative loss rate at which the hurdle is reached at 9.1% to "
             "9.8% of exposure.",
    model_para="The Credit Stress Test & Capital Model takes a loan tape of up to 1,000 loans through three scenarios over "
               "three years and produces the capital plan, the bridge (BRIDGE tab) and the reverse stress test (REVERSE tab) "
               "used in this note, before and after management actions.",
    body=f"""
<h2><span class="n">1</span>Introduction</h2>
<p>Stress tests and ICAAPs at smaller banks are often built around a stressed loss rate for each portfolio. That answers the
first question a supervisor asks, but not the ones that usually follow: how the losses arise, what rating migration does to
risk-weighted assets, when the capital low point occurs and how close it comes to the hurdle. This note describes how the
Credit Stress Test &amp; Capital Model addresses those questions, using the model's demo bank throughout.</p>

<h2><span class="n">2</span>How a credit stress reaches capital</h2>
<p>There are three main channels. The first is impairment, from defaults and from the transfer of loans into Stage 2, where
the allowance moves to a lifetime basis. The second is risk-weighted assets. Under the standardised approach, defaulted
exposures and mortgages at higher loan-to-value ratios attract higher risk weights, so RWA can increase at the same time as
capital falls. The third is earnings: lower pre-provision profit absorbs less of the loss before it reaches capital. A
loss-rate approach captures the first of these and little of the other two.</p>

<h2><span class="n">3</span>Stressing the transition matrix</h2>
<p>The model summarises each scenario in a credit cycle index, built in the same way as in Method Note 2, and applies it to
the transition matrix separately for each segment. The adjustment is made in log-odds to the cumulative probability of
ending the year in a given grade or worse:</p>
<div class="eq">P(grade k or worse, stressed) = logistic( logit P(grade k or worse, TTC) + beta × index )<br>
P(grade k, stressed) = P(grade k or worse) − P(grade k + 1 or worse)</div>
<p>Adjusting the cumulative probabilities shifts the whole row towards weaker grades while keeping it summing to 100% and
preserving the order of the grades. Downgrades and defaults therefore both increase. A downgraded loan that does not default
still affects capital, through a higher allowance (on a lifetime basis if it crosses the staging threshold) and, where it
moves into a higher risk-weight band, through RWA.</p>

<h2><span class="n">4</span>Collateral values</h2>
<p>Each scenario also carries a path for collateral values. Lower values increase LGD, and for residential mortgages they
raise the indexed loan-to-value ratio, which can move a loan into a higher standardised risk-weight band. A severity
multiplier scales both the index and the collateral falls in the adverse scenarios.</p>

<h2><span class="n">5</span>The capital path</h2>
<p>The demo bank starts with CET1 capital of £30.0m and RWA of £191.0m, a CET1 ratio of 15.7%. The stress hurdle is 7.0%,
covering Pillar 1 and Pillar 2A with buffers treated as usable in stress. The baseline requirement including buffers is
10.5%. Table 1 shows the low point in each scenario before management actions.</p>
<div class="cap">Table 1 <span>CET1 ratio low point by scenario, before management actions</span></div>
<table>
<tr><th>Scenario</th><th>Lowest CET1 ratio</th><th>Year</th><th>Hurdle</th><th>Headroom (pp)</th><th>Headroom (£m)</th></tr>
<tr><td>Baseline</td><td>16.30%</td><td>1</td><td>10.5%</td><td>5.80</td><td>11.08</td></tr>
<tr><td>Adverse</td><td>14.07%</td><td>2</td><td>7.0%</td><td>7.07</td><td>13.89</td></tr>
<tr><td>Severely adverse</td><td>7.73%</td><td>3</td><td>7.0%</td><td>0.73</td><td>1.47</td></tr>
</table>
<p class="src">Source: CAPITAL and REVERSE tabs.</p>
<p>The movement in the ratio can be analysed with a bridge from the opening to the closing position. Each three-year income
and loss item is expressed as a proportion of year 3 RWA, and a separate item shows the effect of the change in RWA on the
opening capital, so that the components add up exactly to the reported ratio. Figure 1 shows the severely adverse scenario.</p>
<div class="fig"><div class="cap">Figure 1 <span>CET1 ratio bridge, severely adverse scenario, percentage points</span></div>{n3_wf}
<p class="src">No tax relief is recognised on losses and no dividend is paid without a profit, so the tax and dividend item is
nil. Source: BRIDGE tab.</p></div>
<p>Impairment reduces the ratio by 9.19 percentage points, of which pre-provision profit offsets 2.39. The RWA effect is
0.77 percentage points. That is small next to impairment, but it is close to the remaining headroom of 0.73 points. Had RWA
been held constant, the headroom would have been reported at about 1.50 points.</p>
<p>In the adverse scenario the components are +4.16 for pre-provision profit, −5.07 for impairment, −0.15 for other losses,
−0.04 each for tax and dividends and −0.41 for RWA, giving 14.15% at the end of year 3 after a low of 14.07% in year 2.</p>

<h2><span class="n">6</span>Reverse stress testing</h2>
<p>Reverse stress tests are often presented in qualitative terms. The model also produces a first-order quantitative
estimate, holding RWA, income and dividends at their stressed levels:</p>
<div class="eq">Headroom = CET1 at low point − hurdle × RWA at low point<br>
Further pre-tax loss capacity = headroom / (1 − tax rate × tax relief flag)<br>
Loss multiple = 1 + further loss capacity / losses taken to the low point<br>
Breaking loss rate = (further loss capacity + losses taken to the low point) / exposure</div>
<div class="cap">Table 2 <span>Reverse stress test</span></div>
<table>
<tr><th></th><th>Adverse</th><th>Severely adverse</th></tr>
<tr><td>Headroom at the low point (£m)</td><td>13.89</td><td>1.47</td></tr>
<tr><td>Losses taken to the low point (£m)</td><td>8.37</td><td>19.27</td></tr>
<tr><td>Loss multiple</td><td>2.66</td><td>1.08</td></tr>
<tr><td>Cumulative loss rate at which the hurdle is reached</td><td>9.78%</td><td>9.11%</td></tr>
</table>
<p class="src">Exposure £227.7m. Source: REVERSE tab.</p>
<p>In the severely adverse scenario, losses would need to be 1.08 times those already projected for the bank to reach its
hurdle, a cumulative loss rate of 9.1% of exposure. The adverse scenario gives 2.66 times and 9.8%. The two rates differ
because the scenarios reach their low points in different years, with different RWA and income. Expressed in this form, the
result can be compared directly with historical loss experience and with the bank's stated risk appetite.</p>

<h2><span class="n">7</span>Severity and management actions</h2>
<p>A single adverse path tends to prompt questions about a deeper stress. The severity multiplier, set at 1.0, 0.75 and 1.25
across the model's three input cases, runs the same scenario at different depths, which shows whether capital declines
gradually or falls sharply beyond a certain point. Management actions are applied to the adverse scenarios only. In the demo
they are a nil dividend, a 5% reduction in operating costs and a 10% reduction in RWA outside the loan tape, and results are
reported both before and after them.</p>

<h2><span class="n">8</span>Documentation</h2>
<p>For an ICAAP submission we would expect the stress testing section to include:</p>
<ol>
<li>a description of how the transition matrix is stressed, covering migration as well as default;</li>
<li>the collateral paths and their effect on LGD and on loan-to-value risk-weight bands;</li>
<li>the CET1 path and low point for each scenario, against a stated hurdle;</li>
<li>a bridge from the opening to the closing ratio that reconciles exactly to the capital plan;</li>
<li>a quantified reverse stress result;</li>
<li>results before and after management actions, with each action described;</li>
<li>results at more than one level of severity.</li>
</ol>
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
