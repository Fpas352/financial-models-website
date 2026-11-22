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


def line_svg(series, xlabels, ymax, yfmt=lambda v: f"{v:.0f}%", width=640, height=260, yticks=4,
             hlines=(), markers=False):
    """series = [(name, [values], colour, dashed_bool)]. hlines = [(value, label)] reference lines."""
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
    for hl in hlines:
        v, lab = hl[0], hl[1]
        left = len(hl) > 2 and hl[2] == "left"
        out.append(f'<line x1="{L}" x2="{width - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#333" '
                   f'stroke-width="1" stroke-dasharray="4 3"/>')
        tx, anc = (L + 6, "start") if left else (width - R - 2, "end")
        out.append(f'<text x="{tx}" y="{y(v) - 4:.1f}" text-anchor="{anc}" fill="#333">{lab}</text>')
    if markers:
        for name, vals, col, dashed in series:
            for i, v in enumerate(vals):
                out.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3" fill="{col}"/>')
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


def divbar_svg(rows, vmin, vmax, width=640, bar_h=13, gap=5, label_w=92, step=20, fmt=lambda v: f"{v:+.1f}"):
    """Diverging horizontal bars around zero. rows = [(label, value)]."""
    L, R = label_w, 46
    pw = width - L - R
    x = lambda v: L + pw * (v - vmin) / (vmax - vmin)
    h = len(rows) * (bar_h + gap) + 30
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="{FONT}" font-size="11">']
    for k in range(int(vmin), int(vmax) + 1, step):
        out.append(f'<line x1="{x(k):.1f}" x2="{x(k):.1f}" y1="0" y2="{h - 22}" stroke="{LIGHT}"/>')
        out.append(f'<text x="{x(k):.1f}" y="{h - 8}" text-anchor="middle" fill="{GREY}">{k}</text>')
    out.append(f'<line x1="{x(0):.1f}" x2="{x(0):.1f}" y1="0" y2="{h - 22}" stroke="#555"/>')
    for i, (lab, v) in enumerate(rows):
        yy = 2 + i * (bar_h + gap)
        x0, x1 = sorted((x(0), x(v)))
        col = NEG if v < 0 else MID
        out.append(f'<text x="{L - 8}" y="{yy + bar_h * 0.8}" text-anchor="end" fill="#222">{lab}</text>')
        out.append(f'<rect x="{x0:.1f}" y="{yy}" width="{max(0.8, x1 - x0):.1f}" height="{bar_h}" fill="{col}"/>')
        if abs(v) >= 0.05:
            tx, anc = (x1 + 4, "start") if v >= 0 else (x0 - 4, "end")
            out.append(f'<text x="{tx:.1f}" y="{yy + bar_h * 0.8}" text-anchor="{anc}" fill="#222">'
                       f'{fmt(v).replace("-", chr(8722))}</text>')
    out.append("</svg>")
    return "".join(out)


def tornado_svg(rows, vmin, vmax, width=640, bar_h=20, gap=12, label_w=210, step=5):
    """Tornado chart. rows = [(label, low_pct, high_pct, low_note, high_note)] in % change."""
    L, R = label_w, 70
    pw = width - L - R
    x = lambda v: L + pw * (v - vmin) / (vmax - vmin)
    h = len(rows) * (bar_h + gap) + 30
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" '
           f'font-family="{FONT}" font-size="11.5">']
    k = vmin
    while k <= vmax:
        out.append(f'<line x1="{x(k):.1f}" x2="{x(k):.1f}" y1="0" y2="{h - 22}" stroke="{LIGHT}"/>')
        out.append(f'<text x="{x(k):.1f}" y="{h - 8}" text-anchor="middle" fill="{GREY}">'
                   f'{("+" if k > 0 else "") + str(k).replace("-", chr(8722))}%</text>')
        k += step
    out.append(f'<line x1="{x(0):.1f}" x2="{x(0):.1f}" y1="0" y2="{h - 22}" stroke="#555"/>')
    for i, (lab, lo, hi, lon, hin) in enumerate(rows):
        yy = 3 + i * (bar_h + gap)
        out.append(f'<text x="{L - 8}" y="{yy + bar_h * 0.7}" text-anchor="end" fill="#222">{lab}</text>')
        out.append(f'<rect x="{x(lo):.1f}" y="{yy}" width="{x(0) - x(lo):.1f}" height="{bar_h}" fill="{MID}"/>')
        out.append(f'<rect x="{x(0):.1f}" y="{yy}" width="{x(hi) - x(0):.1f}" height="{bar_h}" fill="{NAVY}"/>')
        lo_txt = f"{lo:.1f}%".replace("-", chr(8722))
        out.append(f'<text x="{x(lo) - 4:.1f}" y="{yy + bar_h * 0.7}" text-anchor="end" fill="#222">{lo_txt}</text>')
        out.append(f'<text x="{x(hi) + 4:.1f}" y="{yy + bar_h * 0.7}" fill="#222">+{hi:.1f}%</text>')
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
table.pair th:nth-child(3), table.pair td:nth-child(3) { text-align: left; padding-left: 28px; }
table.text th, table.text td { text-align: left; padding-right: 10px; vertical-align: top; }
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
    body = re.sub(r'(<div class="cap">[^<]*<span>[^<]*</span></div>\s*<table[^>]*>.*?</table>\s*<p class="src">.*?</p>)',
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
<p class="meta">{note.get('meta', 'Related model: ' + note['model_name'] + '<br>Figures: demo data supplied with the model')}</p>
<div class="abstract"><div class="label">Summary</div><p>{note['abstract']}</p></div>
{body}
<h2>{note.get('close_heading', 'The model')}</h2>
<p style="text-align:left">{note['model_para']} {note.get('sample_line', 'The free sample shows the model&#39;s results on the same demo data used in this note, so the figures here can be compared with it:')}
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

# ── NOTE 4: NMD slotting and delta EVE ───────────────────────────────────────
# Figures: irrbb-model-v5.xlsx demo (Base) plus four copies re-run in desktop
# Excel on 20 Nov 2026 (Upside and Downside selectors; all stable shares set
# to zero; stable share 100%, pass-through 0, lives at the Basel caps). Every
# copy passed all 17 checks.
n4_line = line_svg([
    ("Worst ΔEVE, % of Tier 1", [33.07, 19.34, 8.85, 5.15, 8.32], NAVY, False),
    ("Worst ΔNII, % of Tier 1", [0.78, 1.05, 3.83, 4.86, 5.01], MID, True)],
    ["0", "723", "1,017", "1,155", "1,390"], ymax=35, yticks=7, markers=True,
    hlines=[(15, "EVE threshold 15%"), (5, "NII threshold 5%", "left")])

NOTE4 = dict(
    slug="nmd-slotting-delta-eve", no=4, topic="IRRBB", date_label="November 2026",
    title="Non-maturity deposits in IRRBB: core balances, slotting and their effect on ΔEVE",
    dek="How the core deposit assumption is built under the Basel standardised framework, and how far it moves the "
        "economic value and earnings measures",
    model_name="IRRBB Model", model_url="irrbb-model-excel.html",
    summary="How the core deposit split is built under the Basel standardised framework, and how the same balance "
            "sheet moves from an EVE outlier to an NII outlier as the core assumption changes.",
    abstract="Non-maturity deposits have no contractual maturity, so the interest rate risk they carry depends on a "
             "behavioural assumption. This note sets out how core and non-core balances are derived and slotted under "
             "the Basel standardised framework, then re-runs the demo bank with five sets of deposit assumptions. With "
             "no core balance, the worst ΔEVE is 33.1% of Tier 1, well beyond the 15% outlier threshold. At the "
             "base assumptions it is 8.9%. With core balances at the Basel caps the EVE result is within limits, but the "
             "12-month NII measure reaches 5.01% of Tier 1 and breaches its own 5% threshold. The assumption moves risk "
             "between the two measures as well as changing its size.",
    model_para="The IRRBB Model derives the core split from the stable share and pass-through rate for each deposit "
               "category, applies the Basel caps, slots the balances and runs all six shocks. Its scenario selector "
               "switches between three sets of deposit assumptions, which produced the Base, Upside and Downside rows "
               "of Table 3.",
    refs=["Basel Committee on Banking Supervision, <i>Interest rate risk in the banking book</i>, April 2016 (d368).",
          "European Banking Authority, Regulatory Technical Standards specifying supervisory outlier tests, 2022."],
    body=f"""
<h2><span class="n">1</span>Introduction</h2>
<p>Instant access accounts and current account balances can be withdrawn on demand and repriced at the bank's discretion.
Contractually they reprice overnight. In practice a large part of these balances stays for years, and the rate paid on it
moves much less than the policy rate. How a bank represents that behaviour in its IRRBB measures is often the most
important single assumption in the economic value result, and smaller banks often have the least data with which to support
it. This note describes the approach used in the IRRBB Model and measures the effect of the assumption on the model's demo
bank.</p>

<h2><span class="n">2</span>The standardised framework</h2>
<p>Under the Basel standardised framework [1], non-maturity deposits are first divided into stable and non-stable balances.
The stable part is then divided into a core element, which is unlikely to reprice even under a significant change in rates,
and a non-core element. Non-stable and non-core balances are treated as repricing overnight. Core balances may be spread
across the time buckets, subject to two limits for each category of deposit: a cap on the share of balances treated as core,
and a cap on their average maturity.</p>
<div class="cap">Table 1 <span>Basel caps on core deposits</span></div>
<table>
<tr><th>Deposit category</th><th>Cap on core share</th><th>Cap on average maturity of core (years)</th></tr>
<tr><td>Retail transactional</td><td>90%</td><td>5.0</td></tr>
<tr><td>Retail non-transactional</td><td>70%</td><td>4.5</td></tr>
<tr><td>Wholesale</td><td>50%</td><td>4.0</td></tr>
</table>
<p class="src">Source: BCBS (2016) [1].</p>
<p>The model sets the core share for each category as the stable share multiplied by one minus the pass-through rate, the
proportion of a change in market rates that the bank would pass on to depositors, and then applies the cap. Core balances are
spread evenly from the overnight bucket out to twice their average life, which gives the average life entered. Table 2 shows
the result for the demo bank.</p>
<div class="cap">Table 2 <span>Core and non-core split, demo bank, base assumptions</span></div>
<table>
<tr><th>Category</th><th>Balance (£m)</th><th>Stable share</th><th>Pass-through</th><th>Core share</th><th>Core (£m)</th><th>Average life (years)</th></tr>
<tr><td>Retail transactional</td><td>900</td><td>85%</td><td>15%</td><td>72.3%</td><td>650.3</td><td>4.0</td></tr>
<tr><td>Retail non-transactional</td><td>650</td><td>75%</td><td>35%</td><td>48.8%</td><td>316.9</td><td>3.5</td></tr>
<tr><td>Wholesale</td><td>250</td><td>50%</td><td>60%</td><td>20.0%</td><td>50.0</td><td>2.5</td></tr>
<tr class="tot"><td>Total</td><td>1,800</td><td></td><td></td><td>56.5%</td><td>1,017.1</td><td></td></tr>
</table>
<p class="src">None of the three categories is constrained by its cap at these inputs. Source: NMD tab.</p>

<h2><span class="n">3</span>Why the assumption matters</h2>
<p>The demo bank has total rate-sensitive assets of £3,390m, including £1,070m of fixed-rate mortgages and £395m of fixed-rate
corporate and SME loans. It funds them largely with £1,800m of non-maturity deposits. Tier 1 capital is £310m.</p>
<p>If every deposit is treated as repricing overnight, the liabilities carry almost no duration. A rise in rates reduces the
value of the fixed-rate assets with little offsetting fall in the value of the funding, and ΔEVE is large. Spreading the
core balance over several years gives the liabilities duration of their own, so the same shock reduces their value as well
and much of the asset loss is offset. The balance sheet and the shock are unchanged; the result depends on how the deposits
are slotted.</p>
<p>To measure the effect, the model was run with five sets of deposit assumptions. Three are the model's own scenario
settings. The other two are the extremes: no core balance at all, and every category at its Basel cap with a stable share of
100% and no pass-through.</p>
<div class="cap">Table 3 <span>Worst-case results under five sets of deposit assumptions</span></div>
<table>
<tr><th>Deposit assumptions</th><th>Core (£m)</th><th>Worst ΔEVE (£m)</th><th>Shock</th><th>% of Tier 1</th><th>Worst ΔNII, % of Tier 1</th><th>Outlier test</th></tr>
<tr><td>No core balance</td><td>0</td><td>(102.5)</td><td>Parallel up</td><td>33.07%</td><td>0.78%</td><td>EVE breached</td></tr>
<tr><td>Downside settings</td><td>723.1</td><td>(60.0)</td><td>Parallel up</td><td>19.34%</td><td>1.05% (a)</td><td>EVE breached</td></tr>
<tr><td>Base settings</td><td>1,017.1</td><td>(27.4)</td><td>Parallel up</td><td>8.85%</td><td>3.83%</td><td>Within</td></tr>
<tr><td>Upside settings</td><td>1,154.9</td><td>(16.0)</td><td>Flattener</td><td>5.15%</td><td>4.86% (a)</td><td>Within</td></tr>
<tr><td>At the Basel caps</td><td>1,390.0</td><td>(25.8)</td><td>Parallel down</td><td>8.32%</td><td>5.01%</td><td>NII breached</td></tr>
</table>
<p class="src">Thresholds: 15% of Tier 1 for ΔEVE [1] and 5% for 12-month ΔNII [2]. (a) The Downside and Upside settings
also change the deposit beta used in the NII measure (60% and 30%, against 40% elsewhere). Every run passed all 17 of the
model's integrity checks when recalculated in Excel. Source: SOT tab.</p>
<div class="fig"><div class="cap">Figure 1 <span>Worst-case ΔEVE and ΔNII against the core deposit balance (£m)</span></div>{n4_line}
<p class="src">Source: Table 3.</p></div>

<h2><span class="n">4</span>Reading the results</h2>
<p>With no core balance the worst ΔEVE is a loss of £102.5m, a third of Tier 1, and both the parallel up and the short rates
up shocks breach the 15% threshold. At the base assumptions the same shock costs £27.4m, or 8.9% of Tier 1. The outlier status
of the bank therefore depends on the deposit assumption rather than on the assets.</p>
<p>The relationship is not simply that more core balance means less risk. At the Basel caps the deposits carry more duration
than the assets they fund, and the worst case moves from the parallel up shock to the parallel down shock. The worst ΔEVE
rises again, to 8.3% of Tier 1, and the lowest worst-case result in the table is at the Upside settings, between the two.</p>
<p>The NII measure moves in the opposite direction. Deposits treated as core do not reprice within the 12-month horizon, so the
more balances are slotted as core, the more the bank's earnings depend on rates. At the caps the worst ΔNII reaches 5.01% of
Tier 1, just beyond its threshold. A bank that justifies a high core share to reduce its EVE result should expect its NII result
to rise, and should be ready to explain both.</p>

<h2><span class="n">5</span>Supporting the assumption</h2>
<p>The caps in Table 1 are upper limits, not a default. The stable share is normally estimated from the history of each deposit
category, for example the proportion of the balance that has remained through past periods of outflow. The pass-through rate is
estimated by comparing past changes in the rate paid with changes in the policy rate. The average life should be consistent with
observed account attrition. Where the data are short, as they often are for smaller banks and for products launched since rates
rose, the assumption should be presented as a judgement with a stated range rather than as an estimate.</p>
<p>We would put ΔEVE in front of ALCO at the base assumption and at a more conservative one, together with the NII result
for each. The difference between them shows how much of the reported risk rests on the deposit assumption.</p>

<h2><span class="n">6</span>Documentation</h2>
<p>For each reporting date we would expect the IRRBB file to show:</p>
<ol>
<li>the stable share, pass-through rate and average life for each deposit category, with the evidence for each;</li>
<li>the resulting core share and whether any cap is binding;</li>
<li>the slotting of core and non-core balances by time bucket;</li>
<li>ΔEVE and ΔNII at the base assumptions and at least one more conservative set;</li>
<li>a back-test of the stable share against actual balance movements since the previous review.</li>
</ol>
""")


# ── NOTE 5: IRRBB measurement ────────────────────────────────────────────────
n5_pv01 = divbar_svg([
    ("Overnight", 0.1), ("O/N to 1M", -1.6), ("1M to 3M", -0.3), ("3M to 6M", -2.4), ("6M to 9M", 7.3),
    ("9M to 1Y", 1.2), ("1Y to 1.5Y", -1.4), ("1.5Y to 2Y", -9.3), ("2Y to 3Y", -55.9), ("3Y to 4Y", -53.7),
    ("4Y to 5Y", -47.3), ("5Y to 6Y", 32.2), ("6Y to 7Y", 23.7), ("7Y to 8Y", 40.1), ("8Y to 9Y", 0.0),
    ("9Y to 10Y", -32.5), ("10Y to 15Y", -14.9), ("15Y to 20Y", 0.0), ("Over 20Y", 0.0)],
    vmin=-70, vmax=50, step=10, fmt=lambda v: f"{v:.1f}", bar_h=10, gap=4)

NOTE5 = dict(
    slug="irrbb-standardised-measurement", no=5, topic="IRRBB", date_label="November 2026",
    title="Measuring IRRBB under the standardised framework: shocks, outlier tests and where the risk sits",
    dek="Slotting repricing cash flows, constructing the six supervisory shocks, and reading ΔEVE, ΔNII and "
        "key-rate sensitivities together",
    model_name="IRRBB Model", model_url="irrbb-model-excel.html",
    summary="Building the six supervisory shocks, the EVE and NII outlier tests, and key-rate PV01s on the demo bank, "
            "and why its economic value and earnings move in opposite directions.",
    abstract="Smaller banks without an ALM system often rebuild the Basel standardised IRRBB framework in a spreadsheet. "
             "This note follows the calculation on the IRRBB Model's demo bank: slotting repricing cash flows into the "
             "19 time buckets, constructing the six supervisory shocks, and applying the EVE and NII outlier tests. The "
             "worst ΔEVE is a loss of £27.4m under the parallel up shock, 8.9% of Tier 1 against a 15% threshold, "
             "while the same shock increases 12-month NII by £11.9m. Key-rate PV01s show that the economic value "
             "exposure is concentrated between two and five years and partly offset between five and eight years, "
             "where the core deposits sit.",
    model_para="The IRRBB Model slots repricing cash flows into the 19 Basel time buckets, applies the six prescribed "
               "shocks with an optional post-shock floor, and reports both outlier tests, key-rate PV01s and the "
               "parallel-shift profile on one page for ALCO.",
    refs=["Basel Committee on Banking Supervision, <i>Interest rate risk in the banking book</i>, April 2016 (d368).",
          "European Banking Authority, Regulatory Technical Standards specifying supervisory outlier tests, 2022."],
    body=f"""
<h2><span class="n">1</span>Introduction</h2>
<p>The Basel standardised framework for interest rate risk in the banking book [1] is published in full, but turning it into a
working calculation takes a number of decisions that the text leaves to the bank: how cash flows are slotted, how the shocks are
applied to a particular curve, and how the results are presented. This note works through those steps using the demo bank in
the IRRBB Model. It is a companion to Method Note 4, which covers the treatment of non-maturity deposits.</p>

<h2><span class="n">2</span>The repricing gap</h2>
<p>Every rate-sensitive position is slotted into one of 19 time buckets, from overnight to over 20 years, according to its next
repricing date: the contractual maturity for fixed-rate items and the next reset for floating-rate items. Each bucket is
represented by its midpoint for discounting. Table 1 summarises the demo bank.</p>
<p>The difference between slotted assets and liabilities in Table 1, £410m, must equal equity and other non-rate-sensitive items. The model
checks this control total at every reporting date. It is the simplest way of confirming that nothing has been left out of the
gap or counted twice.</p>
<div class="cap">Table 1 <span>Demo bank, rate-sensitive positions</span></div>
<table class="pair">
<tr><th>Assets</th><th>£m</th><th>Liabilities</th><th>£m</th></tr>
<tr><td>Cash and central bank reserves</td><td>380</td><td>Non-maturity deposits</td><td>1,800</td></tr>
<tr><td>Floating-rate loans</td><td>1,110</td><td>Term deposits</td><td>840</td></tr>
<tr><td>Fixed-rate mortgages</td><td>1,070</td><td>Wholesale funding and debt issued</td><td>300</td></tr>
<tr><td>Fixed-rate corporate and SME loans</td><td>395</td><td>Subordinated debt</td><td>40</td></tr>
<tr><td>Securities</td><td>410</td><td></td><td></td></tr>
<tr><td>Other</td><td>25</td><td></td><td></td></tr>
<tr class="tot"><td>Total</td><td>3,390</td><td>Total</td><td>2,980</td></tr>
</table>
<p class="src">Interest rate swaps of £300m notional are slotted as a receive leg and a pay leg. Tier 1 capital £310m.
Source: GAP and INPUTS tabs.</p>

<h2><span class="n">3</span>The six supervisory shocks</h2>
<p>The framework prescribes six interest rate shock scenarios: parallel up and down, short rates up and down, a steepener and a
flattener. For sterling the parallel shock is 250 basis points, the short-rate shock 300 and the long-rate shock 150 [1]. The
short and long shocks vary with maturity t, in years:</p>
<div class="eq">Short shock(t) = 300 × exp(−t / 4)<br>
Long shock(t) = 150 × (1 − exp(−t / 4))<br>
Steepener(t) = −0.65 × short shock(t) + 0.9 × long shock(t)<br>
Flattener(t) = +0.8 × short shock(t) − 0.6 × long shock(t)</div>
<div class="cap">Table 2 <span>Shock sizes at selected maturities, basis points</span></div>
<table>
<tr><th>Maturity (years)</th><th>0.25</th><th>1</th><th>3</th><th>5</th><th>10</th><th>20</th></tr>
<tr><td>Short rates up</td><td>282</td><td>234</td><td>142</td><td>86</td><td>25</td><td>2</td></tr>
<tr><td>Long shock</td><td>9</td><td>33</td><td>79</td><td>107</td><td>138</td><td>149</td></tr>
<tr><td>Steepener</td><td>(175)</td><td>(122)</td><td>(21)</td><td>41</td><td>108</td><td>133</td></tr>
<tr><td>Flattener</td><td>220</td><td>167</td><td>66</td><td>5</td><td>(63)</td><td>(88)</td></tr>
</table>
<p class="src">Source: CURVE tab formulas.</p>
<p>The shocks are applied to zero rates, and the model can apply a post-shock floor. The default follows the EBA approach [2]:
minus 150 basis points at the overnight point, rising by three basis points a year to zero. On the demo curve, which runs from
3.4% to 4.5%, the lowest shocked rate is 0.75%, so the floor does not bind. It becomes relevant when starting rates are low.</p>

<h2><span class="n">4</span>Economic value of equity</h2>
<p>EVE is the present value of the slotted asset cash flows less that of the liabilities. ΔEVE under each shock is the change
in that value when the cash flows are discounted at the shocked curve. On the base curve the demo bank's EVE is £366.4m.</p>
<div class="cap">Table 3 <span>ΔEVE under the six supervisory shocks</span></div>
<table>
<tr><th>Shock</th><th>ΔEVE (£m)</th><th>% of Tier 1</th></tr>
<tr><td>Parallel up</td><td>(27.4)</td><td>(8.85%)</td></tr>
<tr><td>Parallel down</td><td>30.1</td><td>9.70%</td></tr>
<tr><td>Steepener</td><td>3.2</td><td>1.03%</td></tr>
<tr><td>Flattener</td><td>(8.0)</td><td>(2.60%)</td></tr>
<tr><td>Short rates up</td><td>(16.5)</td><td>(5.32%)</td></tr>
<tr><td>Short rates down</td><td>17.2</td><td>5.55%</td></tr>
</table>
<p class="src">Outlier threshold: a loss of 15% of Tier 1 [1]. Source: SOT tab.</p>
<p>The worst case is the parallel up shock, a loss of 8.85% of Tier 1, comfortably inside the threshold. The response is not
symmetric: a 300 basis point fall in all rates would add £36.4m to EVE, while a 300 basis point rise would remove £32.7m. The
model shows this across a range of parallel shifts in 50 basis point steps.</p>

<h2><span class="n">5</span>Net interest income</h2>
<p>The 12-month NII measure holds the balance sheet constant. A position that reprices within the year earns the shocked rate for
the rest of the year; positions repricing after 12 months do not contribute. Non-maturity deposits reprice with a deposit beta of
40%, the share of a rate change passed to depositors within the year.</p>
<p>Under the parallel up shock the demo bank's NII rises by £11.9m, and under the parallel down shock it falls by the same amount,
3.83% of Tier 1 against a 5% threshold [2]. The bank therefore loses economic value when rates rise but gains earnings. That is
common for a bank with floating-rate assets and slow-repricing deposits funding a fixed-rate mortgage book, and it is why the two
measures should be presented together: a hedge that reduces one will usually increase the other.</p>

<h2><span class="n">6</span>Where the risk sits</h2>
<p>A single ΔEVE figure shows the size of the exposure but not its location on the curve. Key-rate PV01s, the change in EVE
for a one basis point rise in the rate for one bucket alone, show where it comes from. Figure 1 shows them for the demo bank.</p>
<p>The exposure is concentrated between two and five years: £156.9k per basis point across the three buckets. £590m of the
£1,070m of fixed-rate mortgages reprice in that range. It is partly offset between five and eight years, which contributes +£96.1k per basis point. That is
where the core retail deposits sit, spread out to twice their average life. A further £47.4k of sensitivity lies between nine
and 15 years. The duration of equity is 3.1 years.</p>
<div class="fig"><div class="cap">Figure 1 <span>Key-rate PV01 by time bucket, £ thousand per basis point</span></div>{n5_pv01}
<p class="src">Total PV01 −£114.7k per basis point. Source: SENSITIVITY tab.</p></div>
<p>The key-rate PV01s sum to −£114,673, against −£114,653 when every rate is moved by one basis point at once. The model checks
that the two agree within a tolerance, which confirms that the bucket-level figures account for the whole exposure.</p>

<h2><span class="n">7</span>Reporting to ALCO</h2>
<p>For each reporting date we would expect the IRRBB pack to include:</p>
<ol>
<li>the repricing gap by bucket, with the control total against equity and non-rate-sensitive items;</li>
<li>ΔEVE under all six shocks and ΔNII under the parallel shocks, each against its outlier threshold;</li>
<li>key-rate PV01s, so that a proposed hedge can be placed at the right maturity;</li>
<li>the deposit assumptions behind the result and their effect, as set out in Method Note 4;</li>
<li>the movement in each measure since the previous report, with the main causes.</li>
</ol>
""")


# ── NOTE 6: build standards ──────────────────────────────────────────────────
NOTE6 = dict(
    slug="bank-model-build-standards", no=6, topic="Model build", date_label="November 2026",
    title="Building a bank model that will stand up to review",
    dek="The structure, formula conventions and integrity checks that internal validation, auditors and supervisors "
        "look for, with examples from three models",
    model_name="the SFS Models catalogue", model_url="models.html",
    meta="Applies to: model build and review<br>Examples: IFRS 9 ECL Model: Loan-Level Edition, "
         "Credit Stress Test &amp; Capital Model, IRRBB Model",
    close_heading="The models",
    sample_line="Each model has a free sample showing its results on demo data:",
    summary="The structure, formula conventions and integrity checks that make a spreadsheet model reviewable, with "
            "examples from the IFRS 9, stress testing and IRRBB models.",
    abstract="A model used for an allowance, a capital plan or an ALCO report will be reviewed by people who did not build "
             "it. Their questions are predictable: where the assumptions are, whether the logic can be followed, and how "
             "anyone knows the result is arithmetically right. This note sets out the standard we build to, "
             "covering the layout of the workbook, the scenario switch, the treatment of balances and interest, the formula "
             "conventions, and the integrity checks. The three models used as examples carry 36, 42 and 17 checks "
             "respectively.",
    model_para="The three models used as examples are built to the standard described here. Every model in the SFS Models "
               "catalogue has its own integrity checks tab.",
    body="""
<h2><span class="n">1</span>Introduction</h2>
<p>Most errors in spreadsheet models are not errors of method. They are a hard-coded number inside a formula, a range that stops
one row short, a scenario switch that reaches some tabs but not others, or a balance that no longer reconciles after a change.
Each is easy to make and hard to find in a large workbook. A reviewer's job is to find them, and a model built with review in mind
makes that job quick. This note sets out the conventions we use, with examples from three models in the catalogue.</p>

<h2><span class="n">2</span>Layout</h2>
<p>The three example models share the same structure. A COVER tab explains what the model does, what to enter and what the outputs
show. Assumptions are entered on INPUTS, or, where a model needs a large table of inputs such as a transition matrix or a set of
repricing cash flows, on a tab that holds that table. Calculation tabs follow in the order the calculation runs. An OUTPUTS tab
gives a one-page summary that can be printed for a committee, and a CHECKS tab holds the integrity checks.</p>
<p>Cells are coloured by type throughout: blue text on a pale yellow fill for inputs, black for formulas, and green for links to
another tab. Units sit in their own column next to each label. Negative numbers are shown in brackets and zeros as a dash. None of
this is decorative. A reviewer who can see at a glance
which cells are inputs can confirm quickly that no formula contains a typed assumption.</p>

<h2><span class="n">3</span>One scenario switch</h2>
<p>Each of the three example models has a single scenario selector on INPUTS. Every assumption that differs by scenario is held in adjacent columns and
picked by the same index, for example INDEX(C12:E12, 1, ScenIdx). There is no second switch on a calculation tab and no
scenario-specific copy of a calculation. The test is simple: change the selector once and every output in the workbook should
move. A model that passes this test cannot report one scenario's losses alongside another's capital.</p>

<h2><span class="n">4</span>Balances and interest</h2>
<p>Every balance is built as an explicit roll-forward, with a row for each movement and a closing row that adds them to the
opening balance. The closing balance is never calculated another way and then reconciled afterwards.</p>
<p>Interest is calculated on the opening balance of the period, which is the previous period's closing balance, or on the average
of the opening and closing balances where the closing balance does not itself include the period's interest. It is never
calculated on a closing balance that includes it. Calculating interest on a closing balance that itself includes the interest creates a
circular reference. Excel can resolve it only with iterative calculation switched on, the result can depend on the iteration
settings and on the values left in the cells from the previous calculation, and a genuine circular error elsewhere in the workbook
is then hidden. Where a model genuinely links two blocks in both directions, for example a capital constraint that limits lending
which in turn uses capital, the link is broken by taking the constraint from the prior period.</p>

<h2><span class="n">5</span>Formula conventions</h2>
<p>The conventions below are chosen for the reader of the formula rather than its author.</p>
<ol>
<li>No INDIRECT. It breaks when a tab is renamed, recalculates on every change and cannot be traced with Excel's precedent tools.</li>
<li>No array formulas entered with Ctrl+Shift+Enter. SUMPRODUCT does the same work and survives editing by someone who does not
know the formula was an array.</li>
<li>No more than three nested IF functions. Beyond that, a lookup table or a helper row is easier to read and to test.</li>
<li>Formulas over about 200 characters are split into labelled helper rows.</li>
<li>Key inputs have named ranges, so that a formula reads BaseRate rather than INPUTS!$C$12.</li>
<li>Divisions are guarded so that an empty segment shows zero rather than an error. Because a guarded zero can hide a real problem,
the totals built from those divisions are reconciled on CHECKS, so a zero that should not be there tends to show up as a
failure.</li>
</ol>

<h2><span class="n">6</span>Integrity checks</h2>
<p>A check is most useful when it reaches the same number by an independent route. Restating a total does not test anything; adding
up the parts a different way does. Each check on CHECKS has an expected value, an actual value, a tolerance and a status, and an
OVERALL row counts the failures. Table 1 gives examples from three models.</p>
<div class="cap">Table 1 <span>Examples of integrity checks</span></div>
<table class="text">
<tr><th>Model</th><th>Check</th><th>What it catches</th></tr>
<tr><td>IRRBB</td><td>Net repricing gap equals equity and non-rate-sensitive items</td><td>Positions omitted from, or counted twice in, the gap</td></tr>
<tr><td>IRRBB</td><td>Key-rate PV01s sum to the full-repricing PV01</td><td>Buckets missed by the sensitivity analysis</td></tr>
<tr><td>IFRS 9 Loan-Level</td><td>Probability-weighted total equals the allowance before overlay</td><td>Scenario weights not applied consistently</td></tr>
<tr><td>IFRS 9 Loan-Level</td><td>Each Stage 2 loan has exactly one first reason</td><td>Gaps or overlaps in the staging precedence</td></tr>
<tr><td>Credit Stress Test</td><td>Impairment charges equal the change in provisions</td><td>A break between the income statement and the balance sheet</td></tr>
<tr><td>Credit Stress Test</td><td>CET1 bridge closes for every scenario</td><td>A movement in capital that the bridge does not explain</td></tr>
</table>
<p class="src">The three models carry 36 (IFRS 9 Loan-Level), 42 (Credit Stress Test) and 17 (IRRBB) checks. Source: CHECKS tab of each model.</p>
<p>Tolerances are set deliberately. Reconciliations of currency amounts allow £1 for rounding. Checks that compare two
approximations need a wider tolerance: in the IRRBB Model the sum of the key-rate PV01s (−£114,673) and the full-repricing PV01
(−£114,653) are first-order estimates of the same quantity and are allowed to differ by 2%. Some checks test the shape of a result
rather than a total, for example that cumulative default probabilities never fall as the horizon lengthens, or that losses rise
from the baseline to the adverse to the severe scenario.</p>

<h2><span class="n">7</span>Testing</h2>
<p>A model should be tested in the application its users will open. We recalculate every workbook in desktop Excel before release
and read the checks from the values Excel itself has calculated. Third-party calculation engines are useful during the build, but
they do not always treat functions, text results and errors exactly as Excel does, and a check that passes in one can fail in the
other.</p>
<p>Beyond the checks, three tests are worth running on any model before it is relied on: change the scenario selector and confirm
that every output moves; set an adjustment to zero and confirm that the unadjusted result comes back exactly (Method Note 2 gives an
example); and enter an extreme but valid input, such as a balance of zero, and confirm that nothing breaks.</p>

<h2><span class="n">8</span>A reviewer's checklist</h2>
<ol>
<li>Every assumption is in a marked input cell, and no formula contains a typed assumption.</li>
<li>One selector drives every scenario-dependent input.</li>
<li>Every balance has an explicit roll-forward, and no interest calculation refers to a balance that includes that interest.</li>
<li>There are no circular references and iterative calculation is switched off.</li>
<li>There is no INDIRECT and no array formula.</li>
<li>The checks reach their figures by independent routes, and the OVERALL row shows no failures in Excel.</li>
<li>The OUTPUTS page names the active scenario and the reporting date.</li>
</ol>
""")

# ── NOTE 7: reviewing a model you did not build ─────────────────────────────
# Figures: four copies of irrbb-model-v5.xlsx with one error planted in each,
# recalculated in desktop Excel on 22 Nov 2026 (scratchpad irrbb-review/).
# Correct Downside figures from the 20 Nov runs used in Method Note 4.
NOTE7 = dict(
    slug="reviewing-a-model-you-did-not-build", no=7, topic="Model review", date_label="November 2026",
    title="Reviewing a model you did not build: what integrity checks catch and what they miss",
    dek="Four common errors planted in a copy of a working IRRBB model, the checks that found two of them, and the "
        "tests that find the other two",
    model_name="IRRBB Model", model_url="irrbb-model-excel.html",
    meta="Applies to: any model built by someone else, or by an AI tool<br>Example: IRRBB Model, demo data",
    summary="Four errors planted in a copy of a working model: the integrity checks caught two, and the other two "
            "needed a scenario test to find. A review procedure for inherited and AI-built models.",
    abstract="More finance teams now receive models they did not build, either inherited from a colleague or produced "
             "with an AI tool. To see what a reviewer can rely on, we planted four common errors, one at a time, in "
             "copies of the IRRBB Model and recalculated each in Excel. The model's integrity checks caught two: a sum "
             "range that stopped one row short and a typed-over output. They missed two: a typed number left in place "
             "of a formula, and an assumption that no longer followed the scenario selector. Both of those left the base "
             "case unchanged and showed up only when an input was changed. The note sets out a review procedure that "
             "covers both kinds of error.",
    close_heading="The model",
    model_para="The IRRBB Model used for the test has 17 integrity checks, a live-value column on INPUTS showing which "
               "value each scenario-dependent assumption is using, and a scenario selector that switches all of them.",
    body="""
<h2><span class="n">1</span>Introduction</h2>
<p>A model that arrives from someone else carries none of the reasoning that went into it. That has always been true of
inherited spreadsheets, and it is now true of models built with AI tools, which can produce a working structure quickly but
cannot be asked afterwards why a range stops where it does. In either case the reviewer has to establish four things: where the
inputs are, whether the logic can be followed, whether the arithmetic is right, and whether the model responds correctly when
its inputs change. Integrity checks help with the third. This note tests how far they go.</p>

<h2><span class="n">2</span>The test</h2>
<p>We took the IRRBB Model, which recalculates with all 17 of its integrity checks passing, and made four copies. In each copy we
planted one error of a kind that is common in practice. Each copy was then recalculated in desktop Excel, first in the base
scenario and, where relevant, in the Downside scenario, and the results were compared with the unaltered model.</p>
<div class="cap">Table 1 <span>Four planted errors and what found them</span></div>
<table class="text">
<tr><th>Planted error</th><th>Integrity checks</th><th>Effect on the reported results</th></tr>
<tr><td>A sum range stops one row short: £25m of other assets dropped from the one-month bucket</td><td>Two failed</td><td>Barely visible: worst ΔEVE −£27.41m against −£27.44m</td></tr>
<tr><td>A typed-over output: one shock's ΔEVE on the outlier tab replaced with a number</td><td>One failed</td><td>Worst ΔEVE shown as −£20.0m beside a ratio still at 8.85%</td></tr>
<tr><td>A typed number left in place of the core deposit formula for one category</td><td>All passed</td><td>None in the base case. In Downside, core deposits £867.1m instead of £723.1m and worst ΔEVE 16.46% of Tier 1 instead of 19.34%</td></tr>
<tr><td>The deposit beta used for NII no longer follows the scenario selector</td><td>All passed</td><td>None in the base case. In Downside, worst ΔNII 2.89% of Tier 1 instead of 1.05%</td></tr>
</table>
<p class="src">Each error was planted in a separate copy of the model and recalculated in Excel. Source: CHECKS, SOT and NMD tabs.</p>

<h2><span class="n">3</span>What the checks caught</h2>
<p>The short range removed £25m from the asset total of one time bucket. The results moved so little that no reviewer reading the
outputs would have noticed: the worst ΔEVE changed by about £26,000. Two checks failed because they reach the same figure by a
second route. One compares the net cash flows used in the EVE calculation with the total of the repricing gap; the other
compares the cumulative gap in the last bucket with the total. In each, one side is built from the bucket columns and the other
from row totals, so they disagreed by exactly £25m.</p>
<p>The typed-over output failed the check that adds the six ΔEVE results on the outlier tab and compares them with the same
six figures on the EVE tab. The error was also visible on the page, because the worst-case value and the worst-case ratio no longer
agreed, but only to a reader who compared them.</p>
<p>Both errors were caught because the checks compare two independent routes to the same number. A check that restated the damaged
total would have passed.</p>

<h2><span class="n">4</span>What the checks missed</h2>
<p>The typed number was entered over the formula for core retail transactional deposits, at the value the formula was producing at
the time. In the base case nothing changed and every check passed, since each check that uses the core balance reads it from the
same cell. The error appeared only when the scenario was switched to Downside: the core balance stayed at its base value, core
deposits were overstated by £144.0m, and the worst ΔEVE fell from 19.34% to 16.46% of Tier 1. Both figures breach the 15%
threshold, but a reviewer would have been looking at the wrong number.</p>
<p>The broken scenario link behaved the same way. The deposit beta used in the NII measure was fixed at its base value of 40%
rather than following the selector. Every check passed, because no check tests whether an input responds to the
selector. Under Downside the worst ΔNII was reported as 2.89% of Tier 1 instead of 1.05%.</p>
<p>Neither error breaks an identity in the model. Each one replaces a relationship between an input and a result with a fixed value
that happens to be right at the moment it is entered. Arithmetic checks cannot see that. Changing the inputs can.</p>

<h2><span class="n">5</span>A review procedure</h2>
<p>For a model we did not build, we would work through the following steps in order.</p>
<ol>
<li>Map the inputs. List every tab that holds assumptions, and confirm that the cells styled as inputs are the only cells that
contain typed numbers. In Excel, Go To Special with Constants selected, applied to each calculation tab, selects every typed value at
once.</li>
<li>Recalculate in desktop Excel and read the integrity checks. Note which checks reach their figure by an independent route; a
check that restates a total adds nothing.</li>
<li>Switch every scenario and confirm that each scenario-dependent input changes. Where the model shows the value in use next to
each input, as the IRRBB Model does, this takes a few minutes and would have found the broken link in Table 1.</li>
<li>Change the main inputs one at a time and confirm that the results move in the expected direction and by a plausible amount. A
result that does not move when its driver changes points to a typed value, as with the core deposit error.</li>
<li>Trace one figure from the output page back to the inputs, cell by cell.</li>
<li>Enter extreme but valid values, such as a zero balance or a 100% weight on one scenario, and confirm that nothing breaks.</li>
</ol>
<p>Steps 3 and 4 would have found both of the errors that the checks missed, and they take less time than step 5.</p>

<h2><span class="n">6</span>Models built with AI tools</h2>
<p>The same procedure applies. Two points deserve emphasis. First, a model reviewed by the tool that produced it is not
independently reviewed: the review needs a person, or at least a different route to the numbers. Second, an AI-built model can be
correct for the inputs it was built with and fragile when those inputs change, which is exactly the class of error in section 4.
Changing the inputs and watching the results is the most useful single test.</p>
""")


# ── NOTE 8: which assumptions move the answer ───────────────────────────────
# Figures: ifrs9-loan-level-model-v5.xlsx demo. Weights and threshold from the
# model's SENSITIVITY tab; the other four from copies with SEGMENTS flexed,
# recalculated in desktop Excel on 22 Nov 2026 (scratchpad ifrs9-sens/), all
# 36 checks passing.
n8_tornado = tornado_svg([
    ("Scenario weights (alternative sets)", -10.1, 15.5, "", ""),
    ("Unsecured loss rate ±10%", -8.7, 8.6, "", ""),
    ("SICR threshold 3× / 1.5×", -1.4, 9.7, "", ""),
    ("Macro sensitivity ±20%", -3.9, 4.4, "", ""),
    ("LGD floor ±5pp", -3.2, 4.0, "", ""),
    ("Collateral haircut ±5pp", -1.6, 1.7, "", "")], vmin=-15, vmax=20, step=5)

NOTE8 = dict(
    slug="which-assumptions-move-the-answer", no=8, topic="IFRS 9", date_label="November 2026",
    title="Which assumptions move the answer: ranking sensitivities in an IFRS 9 model",
    dek="A loan-level model has hundreds of inputs. Flexing them one at a time shows that a few judgements carry most of "
        "the result.",
    model_name="IFRS 9 ECL Model: Loan-Level Edition", model_url="ifrs9-loan-level-ecl-model-excel.html",
    summary="Flexing six assumptions in a 1,000-loan IFRS 9 model one at a time: two judgements, the scenario weights and "
            "the unsecured loss rate, move the allowance more than the other four combined.",
    abstract="Detailed models invite the question of whether the detail improves the answer. This note flexes six "
             "assumptions in the IFRS 9 ECL Model: Loan-Level Edition, one at a time, and ranks them by their effect on "
             "the demo portfolio's £4.33m allowance. The alternative scenario weightings move it by between −10.1% and "
             "+15.5%, and a 10% change in unsecured loss rates by about ±8.7%. Collateral haircuts, which can attract the "
             "most modelling effort, move it by less than 2% for a five-point change. A sensitivity ranking of this kind shows a "
             "committee where its attention is best spent and where additional model detail is unlikely to change the "
             "result.",
    model_para="The IFRS 9 ECL Model: Loan-Level Edition re-runs the portfolio at alternative SICR thresholds, staging "
               "bounds and scenario weightings on its SENSITIVITY tab. The four LGD and macro sensitivities in Table 1 "
               "were produced by changing the segment parameters on its SEGMENTS tab.",
    body=f"""
<h2><span class="n">1</span>Introduction</h2>
<p>Institutional models tend to be large. A loan-level IFRS 9 model carries a transition matrix, macroeconomic paths, segment
parameters, staging rules and, for every loan, a dozen or more fields. Size is sometimes taken as evidence of rigour, and some of
it is necessary. But the number of inputs says little about which of them matter, and a committee that reviews every assumption
with equal care will spend most of its time on the ones that do not move the result. A sensitivity ranking shows which ones do.</p>

<h2><span class="n">2</span>Method</h2>
<p>Each assumption was changed on its own, with everything else held at its demo value, and the allowance was recalculated. The
size of each change was chosen to represent a plausible range of judgement rather than a stress: plus and minus 20% on the
sensitivity of default rates to the credit cycle index, plus and minus 10% on unsecured loss rates, five percentage points either
way on collateral haircuts and on the LGD floor, the tighter and looser SICR thresholds from Method Note 1, and the two alternative
scenario weightings held in the model. Every run was recalculated in Excel with all 36 integrity checks passing.</p>
<div class="cap">Table 1 <span>Change in the allowance for each assumption, demo portfolio</span></div>
<table>
<tr><th>Assumption</th><th>Low setting</th><th>High setting</th><th>Low</th><th>High</th><th>Range</th></tr>
<tr><td>Scenario weights</td><td>45/30/20/5</td><td>30/10/40/20</td><td>(10.1%)</td><td>+15.5%</td><td>25.6pp</td></tr>
<tr><td>Unsecured loss rate</td><td>×0.9</td><td>×1.1</td><td>(8.7%)</td><td>+8.6%</td><td>17.3pp</td></tr>
<tr><td>SICR relative threshold</td><td>3.0×</td><td>1.5×</td><td>(1.4%)</td><td>+9.7%</td><td>11.1pp</td></tr>
<tr><td>Macro sensitivity (beta)</td><td>×0.8</td><td>×1.2</td><td>(3.9%)</td><td>+4.4%</td><td>8.3pp</td></tr>
<tr><td>LGD floor</td><td>−5pp</td><td>+5pp</td><td>(3.2%)</td><td>+4.0%</td><td>7.2pp</td></tr>
<tr><td>Collateral haircut</td><td>−5pp</td><td>+5pp</td><td>(1.6%)</td><td>+1.7%</td><td>3.3pp</td></tr>
</table>
<p class="src">Base allowance £4.33m, of which management overlay £0.11m. Weights are baseline/upside/downside/severe downside; the
base weighting is 40/20/30/10. LGD floors and haircuts apply only to the secured segments. Source: SENSITIVITY tab and recalculated
copies of the model.</p>
<div class="fig"><div class="cap">Figure 1 <span>Change in the allowance by assumption</span></div>{n8_tornado}
<p class="src">Source: Table 1.</p></div>

<h2><span class="n">3</span>Reading the ranking</h2>
<p>Two judgements dominate. The choice between the model's three scenario weightings moves the allowance across a range of 25.6
percentage points, and a modest change in unsecured loss rates across 17.3 points. Together they account for more of the range than
the other four assumptions combined. Neither is estimated by the model. The weights are set by a committee, and the unsecured loss
rates are segment-level inputs that often rest on limited recovery data.</p>
<p>The SICR threshold sits third, and its effect is one-sided: tightening it adds far more than loosening it removes, for the reason
set out in Method Note 1. The macro sensitivity and the LGD floor follow at around four percentage points either way.</p>
<p>Collateral haircuts come last. In the demo portfolio a five-point change in the forced-sale discount moves the allowance by less than
2%. Haircuts can nonetheless be among the most carefully documented assumptions in an ECL model.</p>
<p>The LGD and macro sensitivity runs all kept 157 loans in Stage 2. Their effect comes through the size of the expected loss on each loan, not through staging.</p>

<h2><span class="n">4</span>The same pattern elsewhere</h2>
<p>The IRRBB results in Method Note 4 show the same concentration. In that model one assumption, the core deposit split, moves the
worst ΔEVE from 8.85% of Tier 1 to 19.34% between the base and downside settings, more than doubling it. Most of the other inputs,
including the positions themselves, are taken from the balance sheet and leave little room for judgement.</p>

<h2><span class="n">5</span>Using the ranking</h2>
<p>A ranking of this kind is cheap to produce once the model can be re-run, and it changes how the model is governed.</p>
<ol>
<li>Put the top two or three assumptions in front of the committee with their ranges, and record the decision on each.</li>
<li>Spend validation and documentation effort in proportion to the ranking, not in proportion to the number of cells.</li>
<li>Before adding detail to a model, ask whether it would change one of the top-ranked inputs. If it would not, it is unlikely to change
the result.</li>
<li>Repeat the ranking at each review. The order changes with the portfolio and with the economic outlook.</li>
</ol>
""")

NOTES = [NOTE1, NOTE2, NOTE3, NOTE4, NOTE5, NOTE6, NOTE7, NOTE8]


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
