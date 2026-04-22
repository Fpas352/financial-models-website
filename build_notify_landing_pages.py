"""
Build SEO landing pages for unbuilt models with a 'Notify when available' CTA.

These 4 models (ICAAP, Project Finance, PE Fund, IFRS 17) are built as Excel
files but not yet hooked up to Lemon Squeezy checkout. Each page captures
demand via a Netlify form so we can email when the product launches.

Run:
    cd financial-models-website && python3 build_notify_landing_pages.py

Output: 4 .html files in the website root.
"""

from pathlib import Path

MODELS = [
    {
        "slug": "icaap-model-excel",
        "title": "ICAAP Model Excel Template",
        "h1": "ICAAP Model Excel Template",
        "keyword": "icaap model excel",
        "meta_desc": "ICAAP model in Excel for UK and EU banks. Pillar 2 capital adequacy assessment, stress testing, capital buffers, SREP-aligned output. Notify when available.",
        "subtitle": "ICAAP capital adequacy model for UK and EU banks. Pillar 2 capital, stress testing, MDA buffer, SREP-aligned output. Built by practitioners.",
        "form_name": "icaap-notify",
        "audience": "Bank Capital Planning teams, CFOs and Finance Directors at UK and EU banks subject to PRA SREP or ECB SSM. Consultancies supporting bank ICAAP submissions.",
        "tabs": [
            ("COVER", "Model documentation, scenario active, version control."),
            ("INPUTS", "Capital base, credit RWA assumptions, market RWA, op risk RWA, stress test parameters, P2A loadings."),
            ("CAPITAL_BASE", "CET1, AT1, T2 build with deductions: goodwill, intangibles, DTA, significant investments."),
            ("CREDIT_RWA", "Credit RWA by exposure class. Standardised approach with optional IRB add-on."),
            ("MARKET_RWA", "Market risk capital charge: VaR-based or sensitivities-based."),
            ("OP_RWA", "Op risk RWA under SMA (Standardised Measurement Approach), Basel IV-aligned."),
            ("STRESS", "Three-year capital plan under base, adverse, severely adverse scenarios with PRA buffer logic."),
            ("PILLAR2", "P2A from SREP letter. P2B (PRA buffer) under stress. Combined buffer requirement."),
            ("CAPITAL_RATIOS", "CET1, T1, Total ratios projected. MDA distribution restriction trigger."),
            ("OUTPUTS", "Executive summary, capital adequacy table, board-pack format. PRA SREP submission-ready."),
            ("CHECKS", "Capital reconciliation, RWA tie-out, scenario hand-off correct."),
        ],
        "differentiators": [
            ("PRA SREP submission alignment", "Output tab maps to PRA SREP table format. Saves weeks at submission time vs reformatting."),
            ("Combined buffer logic", "P1 + P2A + P2B (PRA) + Conservation + Countercyclical + Systemic combined into one MDA threshold."),
            ("Three-year capital plan", "Projects capital ratios across the planning horizon under base + stress."),
            ("Stress test integrated", "Same engine handles capital adequacy and stress testing &mdash; not two separate models."),
            ("UK + EU coverage", "Works for both PRA-supervised UK banks and ECB SSM-supervised EU banks. Buffer logic is jurisdiction-aware."),
        ],
        "faqs": [
            ("When will this be available?", "We're targeting Q3 2026 release. Sign up for notification and we'll email you the moment it ships."),
            ("Will it cover ILAAP too?", "ILAAP (Internal Liquidity Adequacy Assessment Process) is a separate model on a parallel track. Sign up here to get notified for both when ready."),
            ("Is there a US equivalent?", "Yes &mdash; our <a href=\"/bank-stress-test-model.html\">Bank Stress Test Model</a> covers CCAR / DFAST for US BHCs (live now)."),
            ("Can I commission an early build?", "Yes &mdash; we do custom builds for institutions that need it sooner. Pricing varies by scope. Use the form below or contact us directly."),
        ],
        "spec": "Excel (.xlsx) &middot; ~14 tabs &middot; PRA + ECB SSM aligned &middot; expected pricing &pound;1,295 &middot; Q3 2026 launch target",
        "related": [
            ("Bank Stress Test Model (live)", "/bank-stress-test-model.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
            ("IFRS 9 / CECL Model", "/ifrs9-cecl-model-excel.html"),
        ],
    },
    {
        "slug": "project-finance-model-excel",
        "title": "Project Finance Model Excel Template",
        "h1": "Project Finance Model (SPV) Excel Template",
        "keyword": "project finance model excel",
        "meta_desc": "Project finance / SPV model in Excel. DSCR-driven debt sizing, LLCR/PLCR, multi-tranche debt sculpting, equity returns. Long-dated infrastructure deals. Notify when available.",
        "subtitle": "Project finance / SPV model with DSCR-driven debt sizing, LLCR/PLCR cover ratios, multi-tranche debt sculpting, and equity IRR. For infrastructure, energy, and PPP deals.",
        "form_name": "project-finance-notify",
        "audience": "Project finance teams at investment banks, infrastructure funds, energy developers, project sponsors, and PPP/concession advisors. Lenders modelling deals on the credit side.",
        "tabs": [
            ("COVER", "Model documentation, hyperlinked tab index."),
            ("INPUTS", "Construction cost, capex schedule, opex, revenue model, debt terms (rate, tenor, target DSCR), equity contribution."),
            ("CONSTRUCTION", "Capex monthly drawdown, interest during construction (IDC), equity vs debt funding split."),
            ("OPERATING", "Operating phase cash flow: revenue, opex, taxes, working capital, FCFF."),
            ("DEBT_SCHEDULE", "Multi-tranche senior debt with sculpting (DSCR-driven amortisation). Optional mezzanine layer. DSRA modelling."),
            ("DSCR_LLCR", "Debt service cover ratio (period and minimum). Loan life cover ratio. Project life cover ratio."),
            ("EQUITY_RETURNS", "Equity IRR with dividend timing. Sensitivity to revenue / opex / capex overrun."),
            ("DEBT_SIZING", "Solve maximum debt quantum from target DSCR. Iterate against target equity IRR."),
            ("OUTPUTS", "Executive summary, key metrics, financing summary, sensitivity tables."),
            ("CHECKS", "Sources = uses, debt schedule ties, cash sweep priority, IRR reconciles."),
        ],
        "differentiators": [
            ("Debt sculpting", "Senior debt amortisation calibrated to maintain target DSCR throughout the operating phase. Most templates use straight-line amortisation."),
            ("DSRA modelling", "Debt Service Reserve Account funded at financial close, drawn down on cash flow shortfalls, replenished from project cash."),
            ("LLCR + PLCR + DSCR", "All three cover ratios calculated &mdash; not just DSCR. Lenders will want all three."),
            ("Long-dated horizon", "Up to 30-year forecast. Works for infrastructure concessions and PPP deals."),
            ("Debt sizing tool", "Solves debt quantum from target DSCR, not the other way around. Standard at infrastructure desks."),
        ],
        "faqs": [
            ("When will this be available?", "Built as an .xlsx file already. Currently being prepared for launch &mdash; targeting May 2026. Sign up to get notified the moment it ships."),
            ("Will it support PPP / concession deals?", "Yes &mdash; the same engine handles infrastructure, energy, PPP, concession deals. Toggle on INPUTS."),
            ("What about renewable energy specifics?", "Solar, wind, battery storage all work. Revenue can be PPA-based, merchant-based, or blended."),
            ("Can I commission an early build?", "Yes &mdash; for time-sensitive deals, we do custom builds with same-day delivery. Use the form below or contact us."),
        ],
        "spec": "Excel (.xlsx) &middot; ~12 tabs &middot; up to 30-year horizon &middot; expected pricing &pound;495 &middot; May 2026 launch target",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("LBO Model", "/lbo-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
        ],
    },
    {
        "slug": "pe-fund-waterfall-model-excel",
        "title": "PE Fund Waterfall Model Excel Template",
        "h1": "Private Equity Fund Waterfall Model",
        "keyword": "private equity waterfall excel",
        "meta_desc": "PE fund waterfall model in Excel. European and American carry, hurdle rate, catch-up, GP/LP split. IRR, MOIC, DPI, TVPI. Open formulas. Notify when available.",
        "subtitle": "PE fund-level returns waterfall. European and American carry, hurdle rate, catch-up, GP/LP split. Calculates IRR, MOIC, DPI, RVPI, TVPI by deal and at fund level.",
        "form_name": "pe-fund-notify",
        "audience": "PE fund operations, fund accounting teams, LP analysts evaluating fund terms, GP teams modelling carry economics. Fund administrators and audit/advisory firms supporting GP/LP work.",
        "tabs": [
            ("COVER", "Model documentation, fund parameters."),
            ("FUND_INPUTS", "Commitment size, fund term, investment period, fee schedule, carry structure, hurdle rate, catch-up."),
            ("CAPITAL_CALLS", "Cash flow projection: commitments, calls by deal, returns by deal."),
            ("DEAL_RETURNS", "IRR, MOIC, gross/net of fees, by deal."),
            ("FUND_RETURNS", "Gross IRR, Net IRR, DPI, RVPI, TVPI at fund level."),
            ("WATERFALL", "European or American carry waterfall (switchable). Hurdle rate (preferred return) with full catch-up logic."),
            ("FEES", "Management fee schedule (commitment-based or NAV-based). Carry crystallisation tracking."),
            ("REALISATION", "Exit timing and multiple sensitivity. Cash distribution profile."),
            ("OUTPUTS", "LP report format. Investment summary. Returns dashboard."),
            ("CHECKS", "Fund cash flows reconcile, returns calculations tie, waterfall splits sum correctly."),
        ],
        "differentiators": [
            ("European + American carry", "Most templates support one. Ours has both with a single switch &mdash; useful when modelling different fund structures or comparing waterfall economics."),
            ("Full catch-up mechanics", "GP catch-up after LP preferred return is calculated explicitly with the right precedence. Most templates skip this."),
            ("Realistic fee modelling", "Management fee on commitment vs NAV with the standard taper post-investment period."),
            ("LP-side perspective", "Output tab includes LP-side cash flow profile, not just GP economics."),
            ("Fund vs deal split", "Both fund-level and deal-level returns calculated and reconciled."),
        ],
        "faqs": [
            ("When will this be available?", "Built as an .xlsx file already. Currently being prepared for launch &mdash; targeting May 2026. Sign up to get notified the moment it ships."),
            ("Does it support continuation funds?", "Not in v1. Available as a custom build &mdash; contact us."),
            ("What about real estate / credit funds?", "Separate models on the same release track: <a href=\"/contact.html\">contact us</a> if you want all three."),
            ("Can I commission an early build?", "Yes &mdash; we do custom builds for fund teams that need it sooner. Use the form below."),
        ],
        "spec": "Excel (.xlsx) &middot; ~10 tabs &middot; expected pricing &pound;295 &middot; May 2026 launch target",
        "related": [
            ("LBO Model", "/lbo-model-excel.html"),
            ("DCF Model", "/dcf-model-excel.html"),
            ("Project Finance Model", "/project-finance-model-excel.html"),
        ],
    },
    {
        "slug": "ifrs17-insurance-model-excel",
        "title": "IFRS 17 Insurance Model Excel Template",
        "h1": "IFRS 17 Insurance Model Excel Template",
        "keyword": "ifrs 17 model excel",
        "meta_desc": "IFRS 17 insurance contract model in Excel. CSM build, GMM and PAA approaches, BBA, transition methods, P&L disclosure. Audit-ready. Notify when available.",
        "subtitle": "IFRS 17 insurance contract model. CSM build, General Measurement Model and Premium Allocation Approach, transition methods, P&amp;L disclosure format. Built for actuarial and finance teams.",
        "form_name": "ifrs17-notify",
        "audience": "Insurance company finance and actuarial teams, IFRS 17 implementation leads, audit firms supporting insurance clients. Insurance regulators and rating agencies modelling capital requirements.",
        "tabs": [
            ("COVER", "Model documentation, methodology selection."),
            ("INPUTS", "Contract groups, coverage units, expected cash flows, risk adjustment, discount rates."),
            ("CSM", "Contractual Service Margin build. Initial recognition, release pattern over coverage period."),
            ("GMM", "General Measurement Model: BEL + risk adjustment + CSM. For long-duration contracts."),
            ("PAA", "Premium Allocation Approach. For short-duration contracts (typically &lt;1 year coverage). Simplified measurement."),
            ("FULFILMENT_CF", "Best estimate liability (BEL) projection: future cash flows discounted at locked-in rate."),
            ("RISK_ADJUSTMENT", "Risk adjustment build. Confidence level disclosure."),
            ("TRANSITION", "Three transition methods: full retrospective, modified retrospective, fair value approach."),
            ("PL_DISCLOSURE", "P&amp;L statement in IFRS 17 format: insurance revenue, insurance service expenses, insurance finance income/expense."),
            ("OUTPUTS", "Roll-forward summary, key disclosure tables, sensitivity analysis."),
            ("CHECKS", "BEL + RA + CSM ties to total liability, P&amp;L reconciles, transition adjustments balance."),
        ],
        "differentiators": [
            ("Both GMM and PAA", "Same workbook handles long-duration (life, health) and short-duration (P&amp;C) contracts. Switch by contract group."),
            ("Three transition methods", "Full retrospective, modified retrospective, fair value &mdash; all built in for institutions still finalising the transition story."),
            ("CSM amortisation", "Coverage units approach. Time-based and other allocation patterns supported."),
            ("Disclosure format", "P&amp;L output matches IFRS 17 financial statement disclosure format. Audit-ready."),
            ("Sensitivity testing", "Discount rate, risk adjustment, lapse rate sensitivities with one-click recalc."),
        ],
        "faqs": [
            ("When will this be available?", "Built as an .xlsx file already. Currently being prepared for launch &mdash; targeting Q3 2026. Sign up to get notified."),
            ("Does it cover SST (Swiss Solvency Test) too?", "Not in v1. SST and Solvency II capital modelling is a separate release track."),
            ("Will it work with my actuarial system data?", "Yes &mdash; the model is data-input agnostic. Paste cash flows from any system into the input tab."),
            ("Can I commission an early build?", "Yes &mdash; for institutions in implementation, we do custom builds. Use the form below or contact us."),
        ],
        "spec": "Excel (.xlsx) &middot; ~12 tabs &middot; GMM + PAA + Transition &middot; expected pricing &pound;1,295 &middot; Q3 2026 launch target",
        "related": [
            ("IFRS 9 / CECL Model", "/ifrs9-cecl-model-excel.html"),
            ("Bank Long-Term Plan", "/bank-financial-model.html"),
            ("Full Catalogue", "/models.html"),
        ],
    },
]


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | SFS Models</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keyword}, financial model, excel template, sfs models">
<link rel="canonical" href="https://sfsmodels.org/{slug}.html">

<meta property="og:type" content="product">
<meta property="og:title" content="{title} | SFS Models">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://sfsmodels.org/{slug}.html">
<meta property="og:site_name" content="SFS Models">

<script type="application/ld+json">
{{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{title}",
  "description": "{meta_desc}",
  "brand": {{ "@type": "Brand", "name": "SFS Models" }},
  "offers": {{
    "@type": "Offer",
    "availability": "https://schema.org/PreOrder",
    "url": "https://sfsmodels.org/{slug}.html"
  }}
}}
</script>

<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23C9A84C'/><text x='16' y='23' font-family='system-ui' font-size='20' font-weight='700' fill='%230A0C10' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<a href="#main-content" class="skip-link">Skip to main content</a>

<header class="site-header">
  <div class="container">
    <nav class="nav-inner">
      <a href="index.html" class="logo">SFS Models</a>
      <ul class="nav-links">
        <li><a href="models.html">Models</a></li>
        <li><a href="previews.html">Preview Models</a></li>
        <li><a href="free-samples.html">Free Samples</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
      <div class="nav-cta">
        <a href="contact.html" class="btn btn-primary btn-sm">Get a Custom Model</a>
      </div>
      <button class="hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>

<main id="main-content">

  <section class="page-hero">
    <div class="container">
      <p style="background:#C9A84C; color:#0A0C10; display:inline-block; padding:0.25rem 0.7rem; border-radius:4px; font-weight:600; font-size:0.85rem; margin-bottom:0.75rem;">Coming soon</p>
      <h1>{h1}</h1>
      <p>{subtitle}</p>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>Who it's for</h2>
      <p>{audience}</p>
    </div>
  </section>

  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:900px;">
      <h2>What's in the model</h2>
      <div style="display:grid; gap:1.25rem; margin-top:2rem;">
        {tabs_html}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:900px;">
      <h2>What makes this different</h2>
      <div style="display:grid; gap:1.5rem; margin-top:2rem;">
        {diff_html}
      </div>
    </div>
  </section>

  <!-- NOTIFY FORM -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:540px; text-align:center;">
      <h2>Get notified when this launches</h2>
      <p style="margin-bottom:1.5rem;">{spec}</p>
      <form name="{form_name}" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" action="/thankyou.html">
        <input type="hidden" name="form-name" value="{form_name}">
        <input type="hidden" name="model" value="{slug}">
        <p style="display:none;"><label>Don't fill this out: <input name="bot-field"></label></p>
        <div style="display:grid; gap:0.75rem; margin-bottom:1rem;">
          <input type="text" name="name" placeholder="Your name" required style="padding:0.7rem; border:1px solid #ccc; border-radius:4px;">
          <input type="email" name="email" placeholder="Your work email" required style="padding:0.7rem; border:1px solid #ccc; border-radius:4px;">
          <input type="text" name="company" placeholder="Company (optional)" style="padding:0.7rem; border:1px solid #ccc; border-radius:4px;">
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center;">Notify me when available</button>
      </form>
      <p style="color:var(--text-muted); font-size:0.85rem; margin-top:1rem;">No spam. One email when it ships. Or contact us at sfsmodels362@gmail.com for a custom early build.</p>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>Frequently asked questions</h2>
      <div style="display:grid; gap:1.5rem; margin-top:2rem;">
        {faq_html}
      </div>
    </div>
  </section>

  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:760px;">
      <h2>Related models (live now)</h2>
      <ul style="list-style:none; padding:0; margin-top:1.5rem; display:grid; gap:0.75rem;">
        {related_html}
      </ul>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>About SFS Models</h2>
      <p>SFS Models builds institutional-grade Excel financial models for banking and finance professionals. Used by FP&amp;A, Treasury, ALM and Capital teams at US and UK regional banks, by PE firms, and by corporate finance consultancies. Open formulas, no VBA, fully auditable.</p>
      <p style="margin-top:1rem;"><a href="/models.html" class="btn btn-secondary">Browse the live catalogue</a></p>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="logo">SFS Models</a>
        <p>Institutional-grade financial models for banks, fintechs, and advisory firms. Pre-built or custom.</p>
      </div>
      <div class="footer-col">
        <h4>Models</h4>
        <ul>
          <li><a href="models.html#banking-lending">Banking &amp; Lending</a></li>
          <li><a href="models.html#treasury-capital-markets">Treasury</a></li>
          <li><a href="models.html#risk-regulatory">Risk &amp; Regulatory</a></li>
          <li><a href="models.html#valuation-corporate-finance">Valuation</a></li>
          <li><a href="models.html#fpa-management-reporting">FP&amp;A</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="about.html#methodology">Methodology</a></li>
          <li><a href="pricing.html#faq">FAQ</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 SFS Models. All rights reserved.</span>
      <span><a href="terms.html">Terms &amp; Conditions</a> &middot; <a href="privacy.html">Privacy Policy</a> &middot; London, UK &middot; sfsmodels362@gmail.com</span>
    </div>
  </div>
</footer>

<script src="js/scripts.js"></script>
</body>
</html>
"""


def render_tabs(tabs):
    rows = []
    for name, desc in tabs:
        rows.append(
            f'<div style="border-left:3px solid #C9A84C; padding-left:1rem;">'
            f'<h4 style="margin:0 0 0.4rem; font-family: \'DM Serif Display\', serif;">{name}</h4>'
            f'<p style="margin:0; color:var(--text-muted);">{desc}</p>'
            f"</div>"
        )
    return "\n        ".join(rows)


def render_diff(diffs):
    rows = []
    for name, desc in diffs:
        rows.append(
            f'<div>'
            f'<h3 style="margin:0 0 0.4rem; color:#C9A84C;">{name}</h3>'
            f'<p style="margin:0; line-height:1.7;">{desc}</p>'
            f"</div>"
        )
    return "\n        ".join(rows)


def render_faq(faqs):
    rows = []
    for q, a in faqs:
        rows.append(
            f'<div>'
            f'<h4 style="margin:0 0 0.5rem;">{q}</h4>'
            f'<p style="margin:0; color:var(--text-muted); line-height:1.7;">{a}</p>'
            f"</div>"
        )
    return "\n        ".join(rows)


def render_related(related):
    rows = []
    for name, href in related:
        rows.append(f'<li><a href="{href}" style="color:#C9A84C;">&rarr; {name}</a></li>')
    return "\n        ".join(rows)


def main():
    out_dir = Path(__file__).parent
    for m in MODELS:
        html = PAGE_TEMPLATE.format(
            title=m["title"],
            h1=m["h1"],
            keyword=m["keyword"],
            meta_desc=m["meta_desc"],
            slug=m["slug"],
            subtitle=m["subtitle"],
            form_name=m["form_name"],
            audience=m["audience"],
            tabs_html=render_tabs(m["tabs"]),
            diff_html=render_diff(m["differentiators"]),
            spec=m["spec"],
            faq_html=render_faq(m["faqs"]),
            related_html=render_related(m["related"]),
        )
        out_path = out_dir / f"{m['slug']}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"Wrote {out_path.name} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
