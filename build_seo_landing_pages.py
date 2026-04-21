"""
Build 5 SEO-optimised landing pages for sfsmodels.org.
Each targets one buyer-intent keyword and links to the existing Lemon Squeezy checkout.

Run:
    cd financial-models-website && python3 build_seo_landing_pages.py

Output: 5 .html files in the website root.
"""

from pathlib import Path

# ── Model data ──────────────────────────────────────────────────────────
MODELS = [
    {
        "slug": "dcf-model-excel",
        "title": "DCF Model Excel Template",
        "h1": "DCF Model Excel Template",
        "keyword": "dcf model excel template",
        "meta_desc": "Bank-grade DCF valuation model in Excel. Three-statement integration, mid-year discounting, terminal value cross-check, sensitivity tables. Built by practitioners. £249.",
        "subtitle": "Three-statement integration. Mid-year discounting. Terminal value cross-check. Built by practitioners, not template shops.",
        "price_gbp": "249",
        "price_usd": "320",
        "checkout": "https://sfsmodels.lemonsqueezy.com/checkout/buy/e1b91846-dd4c-43ae-b5c8-69c0388862d4",
        "data_model_id": "dcf",
        "audience": "Investment banking associates, private equity associates, corporate development, valuation analysts, finance directors. Used on real deals — not just for case studies.",
        "tabs": [
            ("COVER", "Model name, version, instructions, hyperlinked tab index."),
            ("INPUTS", "All assumptions on one tab: WACC components, growth rates, margins, working capital, capex. Three scenarios — Base, Upside, Downside — controlled by one dropdown."),
            ("OPERATING", "Five-year P&amp;L forecast. Revenue build, gross margin, EBITDA, taxes."),
            ("FCF", "Unlevered free cash flow with full reconciliation: EBIT &times; (1&minus;t) + D&amp;A &minus; Capex &minus; &Delta;WC. Mid-year discounting toggle."),
            ("WACC", "Cost of equity (CAPM), cost of debt (post-tax), capital structure, weighted average. Bottom-up beta calculation."),
            ("DCF", "Present value of explicit forecast plus terminal value. Two terminal value methods (Gordon growth and exit multiple) calculated in parallel as a cross-check."),
            ("OUTPUTS", "Enterprise value, equity value, implied share price, sensitivity table (WACC &times; terminal growth), summary chart."),
            ("CHECKS", "Eight integrity checks: BS balances, CF closing ties to BS cash, FCF reconciliation, terminal value sanity check. Same standard used at top-tier banks."),
        ],
        "differentiators": [
            ("Mid-year discounting", "Most templates only do end-of-year, which under-discounts cash flows by half a year of WACC. Material on growth businesses."),
            ("Terminal value cross-check", "Gordon growth and exit multiple calculated independently and compared. If they diverge by more than 15%, your assumptions are inconsistent."),
            ("Three-statement integration that ties", "The DCF doesn't sit in isolation. It's built on a forecast P&amp;L, BS, and CF that cross-check."),
            ("CHECKS tab", "Eight integrity checks that go red if anything breaks. Industry standard at investment banks; rarely included in template-shop models."),
            ("Open formulas", "No macros, no VBA, no hidden sheets. You can audit every number to its source."),
        ],
        "faqs": [
            ("Does it include industry-specific variants?", "No — this is the generalist model. Industry-specific variants (banks, insurance, REITs, project finance) are available as separate models in the catalogue."),
            ("Can I customise it?", "Yes — fully open formulas. You own the file outright once purchased."),
            ("Will it work in Google Sheets?", "Yes, with minor adjustments. Array formulas behave differently and conditional formatting may need to be re-applied. Around 80% works out of the box."),
            ("Refund policy?", "14-day money-back guarantee, no questions asked, if it doesn't fit your need."),
        ],
        "spec": "Excel (.xlsx) &middot; 7 tabs &middot; ~600 formula cells &middot; print-ready (A4 landscape, fit-to-page) &middot; file size &lt;500 KB &middot; same-day delivery",
        "related": [
            ("LBO Model", "/lbo-model-excel.html"),
            ("Bank Long-Term Plan", "/bank-financial-model.html"),
            ("Free Sample", "/free-sample.html"),
        ],
    },
    {
        "slug": "lbo-model-excel",
        "title": "LBO Model Excel Template",
        "h1": "LBO Model Excel Template",
        "keyword": "lbo model excel",
        "meta_desc": "Bank-grade LBO model in Excel. Multi-tranche debt, real cash sweep priority, covenant tracking, GP/LP returns waterfall (European or American carry). £299.",
        "subtitle": "Multi-tranche debt. Real cash sweep priority logic. Covenant tracking. Returns waterfall with European or American carry.",
        "price_gbp": "299",
        "price_usd": "385",
        "checkout": "https://sfsmodels.lemonsqueezy.com/checkout/buy/d70dace0-06f4-4d12-b10a-bf2f119ebd10",
        "data_model_id": "lbo",
        "audience": "PE associates and VPs, debt advisory professionals, investment banking M&amp;A teams, LBO interview prep. Built for real deals, not just case studies.",
        "tabs": [
            ("COVER", "Model documentation, version, hyperlinked tab index."),
            ("INPUTS", "Purchase price, transaction costs, capital structure, debt terms (rate, tenor, amortisation, covenants), exit assumptions, scenarios."),
            ("SOURCES &amp; USES", "Full transaction structuring with equity check calculation."),
            ("OPERATING", "Five-year P&amp;L forecast: revenue, EBITDA, capex, working capital."),
            ("DEBT_SCHEDULE", "Multi-tranche debt with mandatory amortisation, cash sweep priority, covenant tracking. Up to six tranches: RCF, TLA, TLB, second lien, mezzanine, PIK."),
            ("CASHFLOW", "Unlevered FCF &rarr; debt service &rarr; cash sweep &rarr; ending cash."),
            ("RETURNS", "IRR, MOIC, equity bridge by year. Sensitivity table on entry/exit multiple and leverage."),
            ("WATERFALL", "GP/LP returns waterfall with European or American carry. Hurdle rate, catch-up, carried interest split."),
            ("CHECKS", "Twelve integrity checks: sources = uses, debt schedule ties to BS, cash sweep priority correct, returns reconcile."),
        ],
        "differentiators": [
            ("Real cash sweep priority logic", "Most templates apply cash to whichever tranche the modeller hardcoded first. Ours follows actual credit agreement priority: mandatory amortisation, then first lien sweep, then second lien sweep, then optional repayment."),
            ("Covenant tracking", "Maintenance covenants (leverage, interest cover, FCCR) calculated each period with breach flags. Most templates ignore covenants entirely."),
            ("Dividend recap toggle", "Built-in dividend recap event in year three of the hold flexes capital structure mid-deal. Off by default."),
            ("Returns waterfall &mdash; both conventions", "European and American carry waterfall. Switch via dropdown."),
            ("Realistic debt terms", "Floating rate (SOFR + spread) with rate curves, OID, prepayment penalty &mdash; all built in."),
        ],
        "faqs": [
            ("Does it support add-on acquisitions?", "Yes &mdash; a separate add-on transaction tab adds new sources/uses and consolidates into the operating model."),
            ("Can it model a take-private?", "Yes &mdash; built for both private and take-private LBOs. Toggle on the INPUTS tab."),
            ("Does it cover continuation funds or GP-led secondaries?", "Not in v1. Available as a custom build &mdash; contact us."),
            ("Refund policy?", "14-day money-back guarantee, no questions asked."),
        ],
        "spec": "Excel (.xlsx) &middot; 9 tabs &middot; ~1,500 formula cells &middot; print-ready &middot; file size ~800 KB &middot; same-day delivery",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("Free Sample", "/free-sample.html"),
            ("Full Model Catalogue", "/models.html"),
        ],
    },
    {
        "slug": "bank-stress-test-model",
        "title": "Bank Stress Test Model — ICAAP / CCAR / DFAST in Excel",
        "h1": "Bank Stress Test Model",
        "keyword": "bank stress test model",
        "meta_desc": "Bank-grade stress testing model in Excel for ICAAP, CCAR and DFAST. Scenario engine, P&L impact, capital projection, board-ready output. £299.",
        "subtitle": "Scenario engine for ICAAP, CCAR and DFAST. P&amp;L impact, capital projection, board-ready output. Re-point to a new supervisory scenario in hours, not weeks.",
        "price_gbp": "299",
        "price_usd": "385",
        "checkout": "https://sfsmodels.lemonsqueezy.com/checkout/buy/a56cffcd-a0a3-4387-b50e-b13238942a07",
        "data_model_id": "stress-testing",
        "audience": "Bank capital planning teams, risk and finance functions running ICAAP, CCAR, DFAST or supervisory parallel runs. Practitioners at Category III/IV US BHCs and UK/EU banks doing PRA SREP submissions.",
        "tabs": [
            ("COVER", "Model documentation, scenario active, run timestamp."),
            ("SCENARIOS", "Base, adverse, severely adverse macro paths (GDP, unemployment, rates, equity, credit spreads, real estate, FX). Drop in Fed CCAR scenarios or PRA ACS scenarios via paste."),
            ("PPNR", "Pre-provision net revenue under each scenario. NII rate sensitivity, non-interest income, non-interest expense."),
            ("CREDIT_LOSSES", "Loss forecast by portfolio segment with PD/LGD/EAD methodology and macro overlays."),
            ("RWA_PROJECTION", "RWA paths under stress with credit migration and downgrade modelling."),
            ("CAPITAL_RATIOS", "CET1, Tier 1, leverage and SLR projected through the stress horizon. MDA buffer monitoring."),
            ("OUTPUTS", "Executive summary, capital ratio path charts, one-page board view, ICAAP/CCAR-ready tables."),
            ("CHECKS", "Integrity checks: BS balances, capital reconciliation, RWA ties, scenario hand-off correct."),
        ],
        "differentiators": [
            ("Scenario re-pointing in hours", "Macro variables on one tab. All downstream calculations key off named ranges. Drop in the new Fed or PRA scenario, recalc, done."),
            ("Multi-jurisdiction", "Same engine handles US (CCAR/DFAST), UK (PRA SREP / ICAAP) and EU (EBA stress test) supervisory frameworks. Buffer logic is jurisdiction-aware."),
            ("Real PPNR overlay structure", "NII rate sensitivity, non-interest income trajectory, non-interest expense &mdash; with explicit overlay capacity for management actions."),
            ("Credit loss methodology", "PD/LGD/EAD by segment with macro overlays. The same structure used by enterprise stress testing platforms, just in Excel."),
            ("Capital action logic", "Distributions auto-restricted when capital ratios fall below the MDA threshold."),
        ],
        "faqs": [
            ("Does it cover CECL or IFRS 9?", "ECL methodology lives in our separate IFRS 9 / CECL model. The stress test takes ECL output as an input."),
            ("Will it work for Category I/II US BHCs?", "It's calibrated for Category III/IV. For Category I/II requiring tailored portfolio segmentation or non-standard PPNR builds, contact us for a custom build."),
            ("Does it support both CCAR and DFAST?", "Yes &mdash; both use the same supervisory scenarios. The model serves both."),
            ("Refund policy?", "14-day money-back guarantee."),
        ],
        "spec": "Excel (.xlsx) &middot; ~14 tabs &middot; ~4,000 formula cells &middot; file size ~3 MB &middot; same-day delivery &middot; includes 1 hour of email support",
        "related": [
            ("IFRS 9 / CECL ECL Model", "/ifrs9-cecl-model-excel.html"),
            ("Bank Long-Term Plan", "/bank-financial-model.html"),
            ("Full Model Catalogue", "/models.html"),
        ],
    },
    {
        "slug": "ifrs9-cecl-model-excel",
        "title": "IFRS 9 / CECL ECL Model Excel Template",
        "h1": "IFRS 9 / CECL Expected Credit Loss Model",
        "keyword": "ifrs 9 cecl model excel",
        "meta_desc": "Expected credit loss model in Excel supporting IFRS 9 and CECL. Stage migration, lifetime ECL, PD/LGD/EAD, macro overlays. Audit-ready. £299.",
        "subtitle": "Both IFRS 9 (international) and CECL (US ASC 326) methodologies in one workbook. Stage migration, lifetime ECL, audit-ready documentation.",
        "price_gbp": "299",
        "price_usd": "385",
        "checkout": "https://sfsmodels.lemonsqueezy.com/checkout/buy/c2e532cd-876b-4b73-b0b9-8f48a2b5c5b5",
        "data_model_id": "ifrs9-ecl",
        "audience": "Bank credit risk teams, allowance managers, IFRS 9 and CECL implementation leads, audit and advisory professionals supporting bank clients.",
        "tabs": [
            ("COVER", "Model documentation, methodology selection."),
            ("PORTFOLIO_INPUTS", "Exposure data by segment (C&amp;I, CRE, residential, consumer, credit card), vintage, current balance, weighted average life."),
            ("PD_TERM_STRUCTURES", "Point-in-time PDs by segment and rating, with macro overlay."),
            ("LGD_INPUTS", "LGD by segment, collateral coverage, recovery lag."),
            ("EAD_PROFILES", "Exposure at default by product, including undrawn commitment haircut."),
            ("PDLGDEAD_METHOD", "Full PD &times; LGD &times; EAD calculation, life-of-loan loss, with macro forecast overlay."),
            ("STAGE_MIGRATION", "Stage 1 / 2 / 3 migration matrices for IFRS 9. Lifetime ECL throughout for CECL."),
            ("OUTPUTS", "Allowance by segment, total allowance, provision movement, FFIEC Schedule RI-C format (US) and IFRS 9 disclosures."),
            ("CHECKS", "Methodology consistency, allowance ties to GL, provision movement reconciles."),
        ],
        "differentiators": [
            ("Both standards in one model", "IFRS 9 and CECL share most of the underlying mechanics but diverge on staging and lifetime treatment. Most templates support one. Ours supports both with a switch."),
            ("Macro overlay built in", "Reasonable and supportable forecast (R&amp;S) period and reversion to historical loss rates &mdash; both modelled explicitly with adjustable parameters."),
            ("Stage migration", "Useful for IFRS 9 reporting and for institutions dual-reporting (e.g., US subsidiaries of European banks)."),
            ("Regulatory output alignment", "Output tab aligns to FFIEC Call Report Schedule RI-C (US) and IFRS 9 financial statement disclosures (international)."),
            ("Audit-ready documentation", "Every assumption has a comment cell explaining the source and the methodology decision."),
        ],
        "faqs": [
            ("Does it support DCF methodology in addition to PD/LGD?", "PD/LGD/EAD is the default. DCF methodology variant available as a custom build &mdash; contact us."),
            ("Will the output map to my call report schedule?", "Yes &mdash; for US institutions, output aligns to FFIEC Schedule RI-C. For European institutions, output aligns to IFRS 9 financial statement disclosures."),
            ("Does it handle dual-reporting (IFRS 9 + CECL)?", "Yes &mdash; common for US subsidiaries of European banks. Run both methodologies side-by-side and compare."),
            ("Refund policy?", "14-day money-back guarantee."),
        ],
        "spec": "Excel (.xlsx) &middot; 11 tabs &middot; fully labelled &middot; same-day delivery &middot; includes 1 hour of email support",
        "related": [
            ("Bank Stress Test Model", "/bank-stress-test-model.html"),
            ("Bank Long-Term Plan", "/bank-financial-model.html"),
            ("Full Model Catalogue", "/models.html"),
        ],
    },
    {
        "slug": "bank-financial-model",
        "title": "Bank Financial Model — Long-Term Plan in Excel",
        "h1": "Bank Long-Term Plan Model",
        "keyword": "bank financial model",
        "meta_desc": "Integrated bank LTP in Excel. Lending engine, deposits, treasury (IRRBB), capital and regulatory, KPI dashboards. Used by mid-market bank FP&A teams. £999.",
        "subtitle": "Five-year integrated bank planning model. Lending engine, deposits, treasury, capital and regulatory, executive KPI dashboards. Single timeline. Single scenario switch.",
        "price_gbp": "999",
        "price_usd": "1,295",
        "checkout": "https://sfsmodels.lemonsqueezy.com/checkout/buy/82b900e2-1410-44b6-a317-c77276d70af1",
        "data_model_id": "complete-ltp",
        "audience": "Bank FP&amp;A leads, Finance Directors, ALM and Treasury teams at community and regional banks. Bank consultancies supporting mid-market clients. Built for the gap between Excel templates and £500k enterprise planning systems.",
        "tabs": [
            ("Time / Control", "Shared timeline, period flags, day count conventions."),
            ("Lending", "Cohort &times; calendar month engine by product. Origination, prepayment, default, recovery, provision. NII, fees, cost of funds, NIM. Vintage curves and portfolio composition."),
            ("Deposits", "Book by product (instant access, notice, fixed term). Pricing tab with deposit beta logic. Maturity profile and repricing gap."),
            ("Treasury / IRRBB", "Yield curve, forward rates, MTM. DV01, hedge effectiveness, ALM gap report."),
            ("Capital &amp; Regulatory", "Capital base build (CET1, T1, Total). Credit, market, op risk RWA. Capital ratios with MDA trigger. Five-year capital plan."),
            ("Integrated", "Consolidated P&amp;L, BS, CF. Ten independent scenario switches. KPI dashboard. Data export for board pack."),
            ("INPUTS &amp; CHECKS", "Single INPUTS tab for all assumptions. Forty integrity checks on the CHECKS tab."),
        ],
        "differentiators": [
            ("Single source of truth", "All modules reference one timeline and one scenario selector. Change scenario once and every output across every module updates."),
            ("No circular references", "Capital constraint references prior period, not current. Interest on opening balance, not closing. Built to recalculate cleanly with iteration off."),
            ("Forty integrity checks", "All must pass before the model is presented externally. Same standard used at top-tier banks."),
            ("Real bank P&amp;L structure", "NII, fees, cost of funds, opex, provisions, tax &mdash; the standard FP&amp;A layout, not a generic three-statement."),
            ("ALM-grade treasury", "Real DV01 calculation, real hedge effectiveness ratio, real EVE/NII shock scenarios."),
        ],
        "faqs": [
            ("How long to set up the first run?", "Around two to four hours to populate INPUTS with your bank's data. Two hours of email support included to help with the first run."),
            ("Does it cover stress testing?", "High-level scenario flexing yes (the ten toggles on the Integrated module). For full ICAAP/CCAR-grade stress testing, see our separate Bank Stress Test Model."),
            ("Does it cover ECL / provisions?", "Provision rate is a flexible input. For full PD/LGD/EAD or stage migration, see our separate IFRS 9 / CECL model."),
            ("Refund policy?", "14-day money-back guarantee."),
        ],
        "spec": "Excel (.xlsx) &middot; 18+ tabs &middot; ~6,000 formula cells &middot; same-day delivery &middot; includes 2 hours of email support",
        "related": [
            ("Bank Stress Test Model", "/bank-stress-test-model.html"),
            ("IFRS 9 / CECL ECL Model", "/ifrs9-cecl-model-excel.html"),
            ("Full Model Catalogue", "/models.html"),
        ],
    },
]

# ── Page template ──────────────────────────────────────────────────────────
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | SFS Models</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="{keyword}, financial model, excel template, banking model, sfs models">
<link rel="canonical" href="https://sfsmodels.org/{slug}.html">

<!-- Open Graph / social -->
<meta property="og:type" content="product">
<meta property="og:title" content="{title} | SFS Models">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://sfsmodels.org/{slug}.html">
<meta property="og:site_name" content="SFS Models">

<!-- Schema.org Product markup -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "{title}",
  "description": "{meta_desc}",
  "brand": {{ "@type": "Brand", "name": "SFS Models" }},
  "offers": {{
    "@type": "Offer",
    "price": "{price_gbp}",
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock",
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

  <!-- HERO -->
  <section class="page-hero">
    <div class="container">
      <h1>{h1}</h1>
      <p>{subtitle}</p>
      <p style="margin-top:1.5rem;">
        <a href="{checkout}" target="_blank" rel="noopener" class="btn btn-primary" data-model-id="{data_model_id}">Buy Now &mdash; &pound;{price_gbp}</a>
        &nbsp;&nbsp;
        <a href="/free-sample.html" class="btn btn-secondary">Try Free Sample First</a>
      </p>
    </div>
  </section>

  <!-- WHO IT'S FOR -->
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>Who it's for</h2>
      <p>{audience}</p>
    </div>
  </section>

  <!-- WHAT'S IN THE MODEL -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:900px;">
      <h2>What's in the model</h2>
      <div style="display:grid; gap:1.25rem; margin-top:2rem;">
        {tabs_html}
      </div>
    </div>
  </section>

  <!-- DIFFERENTIATORS -->
  <section class="section">
    <div class="container" style="max-width:900px;">
      <h2>What makes this different</h2>
      <div style="display:grid; gap:1.5rem; margin-top:2rem;">
        {diff_html}
      </div>
    </div>
  </section>

  <!-- SPEC + CTA -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:760px; text-align:center;">
      <h2>Specifications</h2>
      <p style="font-size:1.05rem; line-height:1.7; margin:1.5rem 0;">{spec}</p>
      <p style="margin-top:2rem;">
        <a href="{checkout}" target="_blank" rel="noopener" class="btn btn-primary btn-lg" data-model-id="{data_model_id}">Buy Now &mdash; &pound;{price_gbp}</a>
      </p>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-top:1rem;">14-day money-back guarantee &middot; same-day delivery &middot; secure checkout via Lemon Squeezy</p>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>Frequently asked questions</h2>
      <div style="display:grid; gap:1.5rem; margin-top:2rem;">
        {faq_html}
      </div>
    </div>
  </section>

  <!-- RELATED -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:760px;">
      <h2>Related models</h2>
      <ul style="list-style:none; padding:0; margin-top:1.5rem; display:grid; gap:0.75rem;">
        {related_html}
      </ul>
    </div>
  </section>

  <!-- ABOUT -->
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>About SFS Models</h2>
      <p>SFS Models builds institutional-grade Excel financial models for banking and finance professionals. Our models are used by FP&amp;A, Treasury, ALM and Capital teams at US and UK regional banks, by PE firms, and by corporate finance consultancies. Open formulas, no VBA, fully auditable. Built by practitioners.</p>
      <p style="margin-top:1rem;"><a href="/models.html" class="btn btn-secondary">Browse the full catalogue</a></p>
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
            price_gbp=m["price_gbp"],
            checkout=m["checkout"],
            data_model_id=m["data_model_id"],
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
