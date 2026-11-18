"""
Build landing pages for the five November 2026 models.

Each page targets one search phrase, describes what is actually in the
workbook (taken from each model's COVER and tab structure, Nov 2026), and
links to its own Lemon Squeezy checkout and its own free sample.

Run:
    cd financial-models-website && python3 build_november_model_pages.py

Output: five .html files in the website root. Prices and checkout URLs are
read from ls-config.js so they cannot drift from what the catalogue sells.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://sfsmodels.org"


def load_ls_config():
    """Parse name, price, buyUrl and freeUrl per product id from ls-config.js."""
    text = (ROOT / "ls-config.js").read_text(encoding="utf-8")
    products = {}
    for m in re.finditer(r'"([a-z0-9-]+)":\s*\{(.*?)\n\s*\}', text, re.S):
        body = m.group(2)
        fields = dict(re.findall(r'(\w+):\s*"([^"]*)"', body))
        products[m.group(1)] = fields
    return products


MODELS = [
    # ── IFRS 9 loan-level ───────────────────────────────────────────────
    {
        "id": "ifrs9-loan-level",
        "slug": "ifrs9-loan-level-ecl-model-excel",
        "title": "Loan-Level IFRS 9 ECL Model in Excel",
        "h1": "IFRS 9 ECL Model: Loan-Level Edition",
        "meta": "Loan-level IFRS 9 ECL model in Excel. Stages up to 1,000 loans on five SICR triggers, four macro scenarios, collateral-aware LGD and IFRS 7 tables.",
        "keywords": "ifrs 9 ecl model excel, loan level ecl model, ifrs 9 staging model, sicr model excel, expected credit loss excel",
        "hero": "Paste a loan tape of up to 1,000 loans. Every loan is staged on five triggers, given a 12-month and a lifetime expected credit loss under four probability-weighted macro scenarios, and rolled up into the movement table and the IFRS 7 disclosures.",
        "problem": [
            "Segment-level ECL models average away the loans that drive the allowance. When the auditor asks why one exposure moved to Stage 2, or why the allowance rose this quarter, a pool model cannot answer at loan level.",
            "Enterprise IFRS 9 engines can answer, but they take months to implement and cost far more than a smaller lender needs to spend. This model sits between the two: loan-by-loan staging and measurement in a workbook your team can open, trace and defend.",
        ],
        "who": "Credit risk and impairment teams at smaller banks, building societies and specialist lenders. Finance teams producing IFRS 9 numbers without an enterprise engine. Auditors, advisors and model validators who need an independent loan-level benchmark.",
        "tabs": [
            ("INPUTS", "Scenario weights (three sets on a selector), staging rules, SICR thresholds and sensitivity settings."),
            ("SEGMENTS", "Five segments: residential mortgages, SME, corporate, consumer loans and credit cards. Credit conversion factor, macro sensitivity, unsecured loss rate, collateral haircut and time to sale, LGD floor and management overlay for each."),
            ("MACRO", "Macroeconomic paths for four scenarios, combined into a credit cycle index per scenario and year."),
            ("TM", "Rating grades and the annual through-the-cycle transition matrix."),
            ("PD_CURVES", "Cumulative PDs from compounding the matrix year after year, converted to hazard rates, then shifted for each scenario by the credit cycle index."),
            ("LOANS", "The loan tape (columns A to O) and the loan-level engine: stage, 12-month and lifetime ECL per loan per scenario, probability-weighted."),
            ("STAGING", "Stage mix, which trigger moved each loan, and past-due analysis."),
            ("ECL", "Allowance by segment, by rating grade and by stage, with coverage ratios."),
            ("SCENARIOS", "ECL under each scenario on its own and under each weighting set."),
            ("MOVEMENT", "Stage transfers and the reconciliation of the opening to the closing allowance."),
            ("DISCLOSURE", "IFRS 7 credit quality and loss allowance tables."),
            ("SENSITIVITY", "Allowance against the SICR threshold, staging bounds and overlays."),
            ("OUTPUTS", "One-page summary and charts."),
            ("CHECKS", "37 integrity checks that turn red if anything stops reconciling."),
        ],
        "diffs": [
            ("Five staging triggers, loan by loan", "Stage 3 on days past due or a default grade. Stage 2 on the past-due backstop, a relative and absolute rise in lifetime PD since origination, a downgrade of a set number of notches, watchlist, or forbearance. Loans at or better than the low-credit-risk grade are exempt from the PD test. STAGING shows which trigger fired."),
            ("PD curves you can trace", "Lifetime PDs come from the transition matrix, not a typed-in table. A neutral economy (credit cycle index of zero) returns the through-the-cycle curve exactly, so the forward-looking adjustment is visible and separable."),
            ("Four scenarios, probability-weighted", "Every loan is measured under each scenario and weighted. Switch between three weight sets to see how much of the allowance is driven by the downside."),
            ("Collateral-aware LGD", "LGD applies a forced-sale haircut and time to sale to the collateral, a loss rate to the uncovered part, and a floor. Set per segment."),
            ("Built for the year-end pack", "The movement table and IFRS 7 tables come straight from the loan-level results, so the disclosure ties to the engine without a manual bridge."),
        ],
        "faqs": [
            ("How many loans can it take?", "Up to 1,000 rows on the LOANS tab. Paste your tape over the demo loans; blank rows return zero. For a larger book, run it by portfolio or group similar loans into representative rows."),
            ("How is this different from the £299 IFRS 9 / CECL model?", "That model works at segment level and switches between IFRS 9 and CECL. This one works loan by loan, with five staging triggers per loan, transition-matrix PD curves and IFRS 7 disclosure tables. Choose this one when you need to explain individual exposures."),
            ("What does it not do?", "It runs in annual steps over a 20-year horizon. Exposure is bullet or straight-line amortising, LGD is constant over a loan's life within a scenario, and there is no cure or prepayment modelling. Prior-period stage and ECL are inputs, used for the movement table."),
            ("Are there macros?", "No. Open formulas, no VBA, no hidden sheets. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live. The only difference is that inputs are locked, so you evaluate it on the demo loan book rather than your own."),
        ],
        "spec": "Excel (.xlsx) &middot; 15 tabs &middot; up to 1,000 loans &middot; 37 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("IFRS 9 / CECL Expected Credit Loss Model (segment level)", "/ifrs9-cecl-model-excel.html"),
            ("Credit Stress Test &amp; Capital Model", "/credit-stress-test-model-excel.html"),
            ("Blog: IFRS 9 staging and SICR in practice", "/blog/ifrs9-staging-sicr.html"),
        ],
    },
    # ── Credit stress test ──────────────────────────────────────────────
    {
        "id": "credit-stress-test",
        "slug": "credit-stress-test-model-excel",
        "title": "Credit Stress Test Model in Excel: Loans to CET1",
        "h1": "Credit Stress Test &amp; Capital Model",
        "meta": "Loan-level credit stress test in Excel. Three scenarios over three years: stressed transition matrices, provisions, RWA, CET1 path, reverse stress test.",
        "keywords": "credit stress test model excel, bank stress test excel, icaap stress test model, cet1 stress test, reverse stress test model",
        "hero": "Takes a loan tape of up to 1,000 loans from macro shock to impairments, risk-weighted assets and the CET1 ratio. Three years, three scenarios: baseline, adverse and severely adverse.",
        "problem": [
            "Many credit stress tests apply a stressed loss rate to each segment and stop there. The supervisor's questions go further: how the loss arises, what the downgrades do to RWA as well as to capital, where the low point falls and how far it sits from the hurdle.",
            "This model answers those from your own loan book. The stress moves every loan through a stressed transition matrix, so Stage 2 balances, provisions and risk weights all respond, and the results flow into an income statement and a capital plan.",
        ],
        "who": "Capital planning and stress testing teams at smaller banks and building societies preparing an ICAAP. CFOs and CROs who need a stress they can defend on their own book. Consultants and reviewers supporting ICAAP and supervisory review.",
        "tabs": [
            ("INPUTS", "Severity dial, staging rules, starting capital, RWA outside the tape, income run-rate, hurdle rates and management actions."),
            ("SEGMENTS", "Five segments with credit conversion factor, macro sensitivity, LGD parameters and standardised risk weights, including loan-to-value bands for mortgages."),
            ("SCENARIOS", "Macro paths, the credit cycle index, collateral value paths and bank-level shocks for each scenario."),
            ("TM", "Rating scale, transition matrix and the SICR matrix."),
            ("LIFETIME", "Through-the-cycle cumulative PD by grade and horizon."),
            ("STRESSED", "Stressed transition matrices by segment, scenario and year."),
            ("DIST", "Grade distributions after one, two and three years."),
            ("FWD", "Forward 12-month PD and lifetime uplift at each year-end."),
            ("LOANS", "The loan tape (columns A to M) and the loan-level engine: probability of performing, Stage 2 and default, stressed LGD, provisions and RWA per loan."),
            ("CREDIT", "Tape results by scenario, year and segment."),
            ("PNL", "Income statement by scenario, without and with management actions."),
            ("CAPITAL", "CET1, RWA, ratios and headroom by scenario."),
            ("BRIDGE", "What moved the CET1 ratio over the three years."),
            ("REVERSE", "Reverse stress test: how much more loss the capital position can absorb before the hurdle."),
            ("OUTPUTS", "One-page summary and charts."),
            ("CHECKS", "43 integrity checks."),
        ],
        "diffs": [
            ("The stress moves the whole matrix", "Macro paths become a credit cycle index that shifts the transition matrix separately for each segment. Downgrades and defaults both rise, so Stage 2 migration and RWA inflation come through, not just losses."),
            ("Collateral drives LGD and risk weights", "Collateral values follow their own path. Falling prices raise loss given default and push mortgages into higher loan-to-value risk-weight bands."),
            ("From loans to the CET1 ratio", "Loan results feed an income statement and a capital plan: the CET1 ratio path, the low point against the hurdle, with and without management actions."),
            ("A bridge and a reverse stress test", "BRIDGE shows what moved the ratio. REVERSE shows how many times larger losses could be before the hurdle is reached, and the cumulative loss rate that would get there."),
            ("A severity dial", "One selector scales the adverse scenarios' credit cycle index and collateral falls, so you can show the board how sensitive capital is to the depth of the stress."),
        ],
        "faqs": [
            ("Which capital approach does it use?", "Standardised risk weights, with loan-to-value bands for mortgage segments. It does not calculate IRB risk weights."),
            ("How does it relate to the Stress Testing Model?", "The Stress Testing Model works at portfolio level across the whole income statement. This model starts from the loan tape and gives a granular credit view with its own capital plan. They can be used together, or this one on its own for a credit-led stress."),
            ("What does it not do?", "Annual steps over three years, expected values rather than simulated paths. No cures from default and no write-offs, so Stage 3 only grows. Tax losses are not carried forward. Under the static balance sheet option, maturing loans are replaced like for like."),
            ("How many loans can it take?", "Up to 1,000 rows. Paste over the demo tape; blank rows return zero."),
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
        ],
        "spec": "Excel (.xlsx) &middot; 17 tabs &middot; up to 1,000 loans &middot; 3 scenarios &times; 3 years &middot; 43 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Bank Stress Test Model (portfolio level)", "/bank-stress-test-model.html"),
            ("IFRS 9 ECL Model: Loan-Level Edition", "/ifrs9-loan-level-ecl-model-excel.html"),
            ("ICAAP Model", "/icaap-model-excel.html"),
            ("Blog: Reverse stress testing for banks", "/blog/reverse-stress-testing-bank.html"),
        ],
    },
    # ── CECL ────────────────────────────────────────────────────────────
    {
        "id": "cecl",
        "slug": "cecl-model-excel",
        "title": "CECL Model in Excel: WARM and PD-LGD (ASC 326)",
        "h1": "CECL Model (ASC 326)",
        "meta": "CECL model in Excel for ASC 326. WARM or PD-LGD by segment, nine interagency Q-factors, forecast and reversion, unfunded commitments, ACL roll-forward.",
        "keywords": "cecl model excel, cecl warm method excel, asc 326 model, allowance for credit losses model, cecl calculator",
        "hero": "The lifetime allowance for credit losses across eight loan segments. Choose WARM or PD-LGD for each segment, apply the nine interagency qualitative factors, and get the ACL, the reserve for unfunded commitments and the period roll-forward.",
        "problem": [
            "Many community banks and credit unions run CECL either on a vendor platform they cannot see inside, or on a spreadsheet that has grown by accretion since adoption. Neither is easy to explain when the examiner asks how the forecast reverts or why a qualitative factor moved.",
            "This model sets the methodology out in the open: the reasonable and supportable period, the reversion, the lookback, the Q-factors and the method choice are each an input you can see and change.",
        ],
        "who": "CFOs, controllers and ACL committees at community banks and credit unions. Finance teams preparing for audit or examination. Consultants and auditors who need a transparent benchmark for a client's allowance.",
        "tabs": [
            ("INPUTS", "Scenario, reasonable and supportable forecast period, reversion period, lookback, forecast scalars and scenario weights."),
            ("POOLS", "Eight segments in Call Report terms: 1-4 family residential, home equity lines, owner-occupied CRE, non-owner-occupied CRE, C&amp;I, construction and land, auto and other consumer. Balance, remaining term, prepayment, PD, LGD and method for each."),
            ("HIST_LOSS", "Ten years of annual net charge-off rates and the lookback average."),
            ("QFACTORS", "The nine interagency qualitative factors, by segment."),
            ("WARM", "Balance run-off and the remaining-life loss estimate."),
            ("PD_LGD", "Probability of default times loss given default on the projected balances."),
            ("ACL", "Allowance by segment, coverage ratios and the reserve for unfunded commitments."),
            ("ROLLFWD", "Allowance roll-forward and provision for the period."),
            ("SENSITIVITY", "All three scenarios, a probability-weighted allowance and a scalar grid."),
            ("OUTPUTS", "One-page summary and charts."),
            ("CHECKS", "19 integrity checks, including that every remaining term is within the model horizon."),
        ],
        "diffs": [
            ("Two methods, chosen per segment", "Run WARM where history is the best guide and PD-LGD where you have default and loss data. Both are calculated for every segment, so you can compare before you choose."),
            ("Forecast and reversion made explicit", "A scalar on loss rates applies in full during the reasonable and supportable period, then reverts to the historical rate on a straight line over the reversion period. Both periods are inputs."),
            ("The nine interagency Q-factors", "Adjustments by factor and by segment, laid out so the committee can see what each one adds to the allowance."),
            ("Unfunded commitments and the roll-forward", "The reserve for unfunded commitments sits beside the ACL, and ROLLFWD reconciles opening to closing allowance and gives the provision for the period."),
            ("Scenario weighting", "Three scenarios, a probability-weighted allowance and a scalar grid on SENSITIVITY."),
        ],
        "faqs": [
            ("WARM or PD-LGD: which should I use?", "WARM suits segments with stable loss history and limited default data. PD-LGD suits segments where you track defaults and recoveries. The model calculates both and lets you pick per segment."),
            ("Is it loan level?", "No. It works on eight pooled segments, which is how most community banks estimate CECL. Balances amortise on a straight line with a constant prepayment rate."),
            ("How is this different from the IFRS 9 / CECL model?", "That model is a PD/LGD/EAD engine with a switch between IFRS 9 and CECL. This one is built for ASC 326 only, with WARM, the interagency Q-factors, the unfunded commitment reserve and the roll-forward."),
            ("What does it not do?", "Annual periods and remaining terms up to 15 years. Losses are applied to projected balances, so exposure is not reduced for earlier defaults, which is slightly conservative. It supports management judgement and audit, it does not replace them."),
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
        ],
        "spec": "Excel (.xlsx) &middot; 12 tabs &middot; 8 loan segments &middot; 19 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("IFRS 9 / CECL Expected Credit Loss Model", "/ifrs9-cecl-model-excel.html"),
            ("Blog: Why most CECL models drift after year 2", "/blog/cecl-methodology-drift.html"),
            ("Credit Stress Test &amp; Capital Model", "/credit-stress-test-model-excel.html"),
        ],
    },
    # ── IRRBB ───────────────────────────────────────────────────────────
    {
        "id": "irrbb",
        "slug": "irrbb-model-excel",
        "title": "IRRBB Model in Excel: Delta EVE, Delta NII, SOT",
        "h1": "IRRBB Model",
        "meta": "IRRBB model in Excel. 19 Basel buckets, six prescribed rate shocks, delta EVE, 12-month delta NII, outlier tests against Tier 1 and NMD slotting.",
        "keywords": "irrbb model excel, delta eve calculation excel, supervisory outlier test, irrbb standardised framework, interest rate risk banking book model",
        "hero": "Slot repricing cash flows into the 19 Basel time buckets, apply the six prescribed interest rate shocks, and see delta EVE, 12-month delta NII and the supervisory outlier tests against Tier 1 on one page.",
        "problem": [
            "Search for IRRBB and you find regulation, reporting templates and enterprise ALM systems. What you rarely find is the calculation itself, built and ready to run.",
            "Smaller banks without an ALM system end up rebuilding the Basel standardised framework in a spreadsheet: the buckets, the shock shapes, the deposit slotting, the outlier tests. This model is that framework, already built, with every assumption on one inputs tab.",
        ],
        "who": "ALM and treasury teams at smaller banks and building societies. Risk teams preparing IRRBB reporting or the ICAAP interest rate risk section. ALCO secretaries who need the numbers on one page. Consultants and auditors checking a client's IRRBB figures.",
        "tabs": [
            ("INPUTS", "Tier 1 capital, shock sizes for your currency, post-shock floor, outlier thresholds, deposit behaviour and the base yield curve."),
            ("BUCKETS", "The 19 Basel time buckets and their midpoints."),
            ("NMD", "Non-maturity deposits: core and non-core split, the Basel caps, and slotting."),
            ("GAP", "Repricing cash flows by bucket and the repricing gap."),
            ("CURVE", "Base curve, the six shocks, shocked curves and discount factors."),
            ("EVE", "Economic value of equity under each shock."),
            ("NII", "12-month change in net interest income under parallel shocks."),
            ("SOT", "Supervisory outlier tests on EVE and NII, against Tier 1."),
            ("SENSITIVITY", "Key-rate PV01 by bucket and the parallel-shift profile."),
            ("OUTPUTS", "One-page summary and charts."),
            ("CHECKS", "18 integrity checks."),
        ],
        "diffs": [
            ("All six prescribed shocks", "Parallel up and down, short up and down, steepener and flattener. Short and long shocks decay exponentially with maturity, steepener and flattener are the Basel combinations, and a post-shock floor stops rates falling through a set lower bound. Defaults are sterling; every shock size is editable for your currency."),
            ("Non-maturity deposits slotted properly", "Deposits are split into core and non-core using the stable share and pass-through rate, subject to the Basel caps. Non-core reprices overnight; core is spread out to twice its average life. The scenario selector flexes these assumptions, because they drive the answer."),
            ("Both outlier tests", "Worst-case delta EVE and delta NII as a share of Tier 1, against thresholds you set (defaults: 15% for EVE, 5% for NII)."),
            ("PV01 by bucket", "Key-rate sensitivity shows where in the curve the risk sits, not just how big it is."),
            ("One page for ALCO", "OUTPUTS puts the six EVE results, the NII result and the outlier status on a single printable page."),
        ],
        "faqs": [
            ("Which rules is it built on?", "The Basel standardised framework for IRRBB: 19 time buckets, six prescribed shocks and the supervisory outlier tests. Bucket boundaries, shock sizes and thresholds are inputs, so you can align them to your regulator's version."),
            ("Does it model option risk?", "Behavioural optionality is captured through deposit slotting. Prepayment and early redemption are not modelled separately: reflect them in the buckets you enter. Automatic options such as caps and floors are not modelled."),
            ("Can it handle more than one currency?", "One currency per copy. Run a copy for each material currency."),
            ("How is it different from the Duration &amp; Rate Sensitivity Model?", "That model measures duration and rate sensitivity for a portfolio. This one implements the regulatory IRRBB framework: Basel buckets, the six shocks, deposit slotting and the outlier tests."),
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
        ],
        "spec": "Excel (.xlsx) &middot; 12 tabs &middot; 19 Basel buckets &middot; 6 rate shocks &middot; 18 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("ILAAP Model", "/ilaap-model-excel.html"),
            ("ICAAP Model", "/icaap-model-excel.html"),
            ("Blog: Calibrating deposit beta", "/blog/deposit-beta-calibration.html"),
        ],
    },
    # ── IFRS 16 ─────────────────────────────────────────────────────────
    {
        "id": "ifrs16-lease",
        "slug": "ifrs16-lease-model-excel",
        "title": "IFRS 16 Lease Model in Excel for a Lease Portfolio",
        "h1": "IFRS 16 Lease Model",
        "meta": "IFRS 16 lessee model in Excel for a lease portfolio. Liability, right-of-use asset, monthly ten-year schedule, maturity analysis, disclosures, journals.",
        "keywords": "ifrs 16 lease model excel, ifrs 16 template excel, lease liability calculation excel, right of use asset excel, ifrs 16 disclosure",
        "hero": "Measure up to ten leases at commencement and run each one month by month for ten years: interest unwind, payments and depreciation. Rolled up into the P&amp;L, balance sheet, cash flow, IFRS 16 disclosures and journals.",
        "problem": [
            "Most IFRS 16 templates calculate one lease. Year-end needs the whole portfolio: a maturity analysis, right-of-use assets by class, the journals, and an answer on the two judgements auditors challenge most, extension options and the incremental borrowing rate.",
            "This model runs the portfolio in one workbook and puts both judgements on a scenario selector, so you can show what each one does to the balance sheet.",
        ],
        "who": "Financial controllers and group reporting teams with a set of property, vehicle and IT leases. Bank finance teams accounting for a branch estate. Accountants preparing year-end files for clients.",
        "tabs": [
            ("INPUTS", "Scenario, model start date, reporting year and the two judgements."),
            ("LEASES", "Lease register: commencement, term, extension option, monthly payment, in advance or arrears, fixed annual uplift, incremental borrowing rate, initial direct costs, incentives and restoration costs. Measurement at commencement."),
            ("SCHEDULE", "The monthly engine: payments, liability, interest, depreciation and right-of-use asset."),
            ("ANNUAL", "Ten-year P&amp;L, balance sheet, cash flow and roll-forwards."),
            ("DISCLOSURE", "Maturity analysis and right-of-use assets by asset class."),
            ("JOURNALS", "Initial recognition and reporting-year journal entries."),
            ("SENSITIVITY", "Lease liability under shifted discount rates."),
            ("OUTPUTS", "One-page summary and charts."),
            ("CHECKS", "20 integrity checks, including that every lease ends within the horizon."),
        ],
        "diffs": [
            ("A portfolio, not one lease", "Ten leases across property, vehicles, IT and equipment, each with its own dates, payments and rate, summed into one set of accounts."),
            ("The details that move the numbers", "Payments in advance or in arrears, fixed annual uplifts, initial direct costs, lease incentives and restoration costs all feed the right-of-use asset at commencement."),
            ("Disclosures and journals included", "The maturity analysis, the right-of-use table by class and the journal entries come from the same schedule, so they tie without rework."),
            ("The two judgements on a switch", "Flex whether extension options are reasonably certain and the incremental borrowing rate, and see the effect on liability, asset and P&amp;L."),
            ("Existing leases handled", "For a lease already running at the model start date, enter the start date and the remaining term: the modified retrospective measurement."),
        ],
        "faqs": [
            ("Lessee or lessor?", "Lessee accounting only."),
            ("How many leases?", "Ten rows, each a separate lease. For a larger estate, run a copy per entity or group leases of the same class and terms."),
            ("Does it handle index-linked payments?", "Payments linked to an index are measured at the commencement rate, as IFRS 16 requires, so only fixed uplifts are projected. Remeasurements and modifications are not modelled."),
            ("Monthly or annual?", "Monthly. A lease that commences mid-month is treated as starting on the first of that month. Every lease must end within the 120-month horizon; CHECKS tests this."),
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo portfolio."),
        ],
        "spec": "Excel (.xlsx) &middot; 10 tabs &middot; up to 10 leases &middot; monthly over 10 years &middot; 20 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Full Model Catalogue: Accounting &amp; Fixed Assets", "/models.html#accounting-fixed-assets"),
            ("Blog: Excel financial model best practices", "/blog/excel-financial-model-best-practices.html"),
        ],
    },
]


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@ | SFS Models</title>
<meta name="description" content="@@META@@">
<meta name="keywords" content="@@KEYWORDS@@">
<link rel="canonical" href="@@URL@@">

<!-- Open Graph / social -->
<meta property="og:type" content="product">
<meta property="og:title" content="@@TITLE@@ | SFS Models">
<meta property="og:description" content="@@META@@">
<meta property="og:url" content="@@URL@@">
<meta property="og:site_name" content="SFS Models">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="@@TITLE@@ | SFS Models">
<meta name="twitter:description" content="@@META@@">

<script type="application/ld+json">
@@PRODUCT_LD@@
</script>
<script type="application/ld+json">
@@FAQ_LD@@
</script>

<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23C9A84C'/><text x='16' y='23' font-family='system-ui' font-size='20' font-weight='700' fill='%230A0C10' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<!-- SFS-ANALYTICS -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "7852444a13cc4cc78cdb4162c284e1de"}'></script>
<!-- /SFS-ANALYTICS -->
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
          <li><a href="/research/">Research</a></li>
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
"""

FOOT = """
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

GOLD_BORDER = "border-left:3px solid #C9A84C; padding-left:1rem;"


def plain(s):
    """Strip entities/tags for JSON-LD text."""
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def buttons(m, big=False):
    size = " btn-lg" if big else ""
    return (
        f'<a href="{m["buy"]}" target="_blank" rel="noopener" class="btn btn-primary{size} ls-buy-btn" '
        f'data-model-id="{m["id"]}">Buy Now - &pound;{m["price"]}</a>\n'
        f'        &nbsp;&nbsp;\n'
        f'        <a href="{m["free"]}" target="_blank" rel="noopener" class="btn btn-secondary{size} ls-free-btn" '
        f'data-model-id="{m["id"]}">Download the Free Sample</a>'
    )


def render(m):
    url = f"{SITE}/{m['slug']}.html"
    product_ld = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": plain(m["h1"]),
        "description": m["meta"],
        "brand": {"@type": "Brand", "name": "SFS Models"},
        "offers": {
            "@type": "Offer",
            "price": m["price"],
            "priceCurrency": "GBP",
            "availability": "https://schema.org/InStock",
            "url": url,
        },
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
            for q, a in m["faqs"]
        ],
    }
    head = (HEAD.replace("@@TITLE@@", m["title"])
                .replace("@@META@@", html.escape(m["meta"], quote=True))
                .replace("@@KEYWORDS@@", m["keywords"])
                .replace("@@URL@@", url)
                .replace("@@PRODUCT_LD@@", json.dumps(product_ld, indent=2, ensure_ascii=False))
                .replace("@@FAQ_LD@@", json.dumps(faq_ld, indent=2, ensure_ascii=False)))

    problem = "\n".join(f'      <p style="line-height:1.7; margin-top:1rem;">{p}</p>' for p in m["problem"])
    tabs = "\n".join(
        f'        <div style="{GOLD_BORDER}"><h4 style="margin:0 0 0.4rem; font-family: \'DM Serif Display\', serif;">{t}</h4>'
        f'<p style="margin:0; color:var(--text-muted);">{d}</p></div>'
        for t, d in m["tabs"])
    diffs = "\n".join(
        f'        <div><h3 style="margin:0 0 0.4rem; color:#C9A84C;">{t}</h3><p style="margin:0; line-height:1.7;">{d}</p></div>'
        for t, d in m["diffs"])
    faqs = "\n".join(
        f'        <div><h4 style="margin:0 0 0.5rem;">{q}</h4><p style="margin:0; color:var(--text-muted); line-height:1.7;">{a}</p></div>'
        for q, a in m["faqs"])
    related = "\n".join(
        f'        <li><a href="{href}" style="color:#C9A84C;">&rarr; {name}</a></li>'
        for name, href in m["related"] + [("Full Model Catalogue", "/models.html")])

    body = f"""
<main id="main-content">

  <!-- HERO -->
  <section class="page-hero">
    <div class="container">
      <h1>{m["h1"]}</h1>
      <p>{m["hero"]}</p>
      <p style="margin-top:1.5rem;">
        {buttons(m)}
      </p>
    </div>
  </section>

  <!-- THE PROBLEM -->
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>The problem it solves</h2>
{problem}
      <h2 style="margin-top:2.5rem;">Who it's for</h2>
      <p style="line-height:1.7; margin-top:1rem;">{m["who"]}</p>
    </div>
  </section>

  <!-- WHAT'S IN THE MODEL -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:900px;">
      <h2>What's in the model</h2>
      <p style="color:var(--text-muted); margin-top:0.75rem;">Every workbook opens on a COVER tab with instructions and a linked tab index. Then:</p>
      <div style="display:grid; gap:1.25rem; margin-top:2rem;">
{tabs}
      </div>
    </div>
  </section>

  <!-- DIFFERENTIATORS -->
  <section class="section">
    <div class="container" style="max-width:900px;">
      <h2>What makes it different</h2>
      <div style="display:grid; gap:1.5rem; margin-top:2rem;">
{diffs}
      </div>
    </div>
  </section>

  <!-- SPEC + CTA -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:760px; text-align:center;">
      <h2>Specifications</h2>
      <p style="font-size:1.05rem; line-height:1.7; margin:1.5rem 0;">{m["spec"]}</p>
      <p style="margin-top:2rem;">
        {buttons(m, big=True)}
      </p>
      <p style="color:var(--text-muted); font-size:0.9rem; margin-top:1rem;">The free sample is the full workbook with inputs locked &middot; one-time purchase, no subscription &middot; secure checkout via Lemon Squeezy</p>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>Frequently asked questions</h2>
      <div style="display:grid; gap:1.5rem; margin-top:2rem;">
{faqs}
      </div>
    </div>
  </section>

  <!-- RELATED -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:760px;">
      <h2>Related</h2>
      <ul style="list-style:none; padding:0; margin-top:1.5rem; display:grid; gap:0.75rem;">
{related}
      </ul>
    </div>
  </section>

  <!-- ABOUT -->
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>About SFS Models</h2>
      <p>SFS Models builds institutional-grade Excel financial models for banking and finance professionals, built by a banking practitioner. Open formulas, no VBA, every number traceable to an input, and a CHECKS tab in every workbook.</p>
      <p style="margin-top:1rem;"><a href="/models.html" class="btn btn-secondary">Browse the full catalogue</a></p>
    </div>
  </section>

</main>
"""
    return head + body + FOOT


def main():
    ls = load_ls_config()
    for m in MODELS:
        p = ls[m["id"]]
        m["price"] = p["price"].replace("£", "").replace(".00", "")
        m["buy"] = p["buyUrl"]
        m["free"] = p["freeUrl"]
        out = ROOT / f"{m['slug']}.html"
        out.write_text(render(m), encoding="utf-8")
        print(f"wrote {out.name}  (£{m['price']})")


if __name__ == "__main__":
    main()
