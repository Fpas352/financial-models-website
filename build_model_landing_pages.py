"""
Build per-model SEO landing pages for sfsmodels.org.

Each page targets one search phrase, describes what is actually in the
workbook (taken from each model's COVER and tab structure, Nov 2026), and
links to its own Lemon Squeezy checkout and its own free sample.

Run:
    cd financial-models-website && python3 build_model_landing_pages.py

Output: one .html file per entry in MODELS, in the website root. Prices and checkout URLs are
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
            ("CHECKS", "36 integrity checks that turn red if anything stops reconciling."),
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
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo loan book, plus one engine tab with live formulas. To run your own loan book you need the full version."),
        ],
        "spec": "Excel (.xlsx) &middot; 15 tabs &middot; up to 1,000 loans &middot; 36 integrity checks &middot; no macros &middot; instant download",
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
            ("CHECKS", "42 integrity checks."),
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
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 17 tabs &middot; up to 1,000 loans &middot; 3 scenarios &times; 3 years &middot; 42 integrity checks &middot; no macros &middot; instant download",
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
            ("CHECKS", "18 integrity checks, including that every remaining term is within the model horizon."),
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
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 12 tabs &middot; 8 loan segments &middot; 18 integrity checks &middot; no macros &middot; instant download",
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
            ("CHECKS", "17 integrity checks."),
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
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 12 tabs &middot; 19 Basel buckets &middot; 6 rate shocks &middot; 17 integrity checks &middot; no macros &middot; instant download",
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
            ("CHECKS", "19 integrity checks, including that every lease ends within the horizon."),
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
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 10 tabs &middot; up to 10 leases &middot; monthly over 10 years &middot; 19 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Full Model Catalogue: Accounting &amp; Fixed Assets", "/models.html#accounting-fixed-assets"),
            ("Blog: Excel financial model best practices", "/blog/excel-financial-model-best-practices.html"),
        ],
    },
    # ════════════════════════════════════════════════════════════════════
    # Batch 2 (18 Nov 2026): banking and regulatory models with no page.
    # Content from each workbook's COVER, INSTRUCTIONS and NOTES tabs.
    # ════════════════════════════════════════════════════════════════════
    # ── Basel IV RWA ────────────────────────────────────────────────────
    {
        "id": "basel-iv-rwa",
        "slug": "basel-iv-rwa-model-excel",
        "title": "Basel IV RWA Calculator in Excel: SA, IRB, Output Floor",
        "h1": "Basel IV RWA Calculator",
        "meta": "Basel IV RWA model in Excel. Standardised and IRB credit RWA, output floor, FRTB market risk, SMA operational risk and CVA, 20 quarters, four scenarios.",
        "keywords": "basel iv rwa calculator excel, basel 3.1 rwa model, output floor calculation excel, irb rwa formula excel, risk weighted assets model",
        "hero": "Risk-weighted assets under the Basel III final reforms in one workbook: credit RWA under the standardised and IRB approaches, the output floor, market, operational and CVA risk, projected over 20 quarters under four scenarios.",
        "problem": [
            "The Basel III final reforms (Basel IV, or Basel 3.1 in the UK) change almost every RWA calculation at once: a new standardised approach, constraints on IRB, the output floor, the SMA for operational risk and a revised CVA framework. Most banks need to see the combined effect on their ratios before the rules bite, not one component at a time.",
            "This calculator brings all of it into one place, so you can see where the floor binds, what moving a portfolio from SA to IRB is worth, and how the capital ratios respond.",
        ],
        "who": "Capital management and regulatory reporting teams preparing for Basel 3.1 and CRR3. Banks on or moving to IRB that need to understand the output floor. Consultants and analysts sizing the RWA impact of the reforms.",
        "tabs": [
            ("INSTRUCTIONS", "Methodology, scenario definitions and how to run the model."),
            ("INPUTS", "Every assumption, with a scenario selector across Base, Upside, Downside and Stress, and the output floor percentage set by quarter."),
            ("CREDIT_RWA_SA", "Standardised approach across 12 exposure classes, from sovereigns and banks to corporates, retail and real estate: EAD, risk weight, RWA, density and capital requirement."),
            ("CREDIT_RWA_IRB", "IRB capital requirement using the full Vasicek single-factor formula with asset correlation and maturity adjustment."),
            ("OUTPUT_FLOOR", "Floored RWA = MAX(IRB RWA, SA RWA x floor %), in total and by exposure class, with whether the floor binds and its add-on."),
            ("MARKET_RWA", "Sensitivities-based method under FRTB across GIRR, credit spread, equity, commodity and FX risk classes."),
            ("OP_RISK_RWA", "Standardised Measurement Approach: business indicator component with marginal coefficients and the internal loss multiplier."),
            ("CVA_RWA", "Basic CVA approach with systematic and idiosyncratic components."),
            ("RWA_SUMMARY", "Consolidated RWA across all risk types."),
            ("CAPITAL_RATIOS", "Capital adequacy ratios against regulatory minimums."),
            ("MIGRATION", "SA to IRB migration impact analysis."),
            ("DASHBOARD", "Charts and executive summary."),
            ("SENSITIVITY", "Two-way sensitivity tables."),
            ("CHECKS", "65 integrity checks with automated PASS / FAIL."),
        ],
        "diffs": [
            ("The output floor, class by class", "The floor is calculated in total and for each exposure class, so you can see which portfolios drive the add-on rather than just its size."),
            ("A phase-in you control", "The floor percentage is an input for each of the 20 quarters, so you can follow the Basel timetable or your own regulator's transitional path."),
            ("The real IRB formula", "IRB capital uses the Vasicek single-factor model with asset correlation, the 99.9% confidence level and the maturity adjustment, not a lookup of indicative risk weights."),
            ("SA to IRB migration", "MIGRATION shows the RWA effect of moving exposure classes between approaches, once the floor is taken into account."),
            ("All four risk types together", "Credit, market, operational and CVA RWA roll into one summary and one set of ratios, under four scenarios."),
        ],
        "faqs": [
            ("Is this Basel 3.1 / CRR3?", "It implements the Basel III final reforms as published by the Basel Committee in December 2017, which Basel 3.1 in the UK and CRR3 in the EU are based on. Local variations, such as specific risk weights and the transitional floor path, are inputs you can align to your rules."),
            ("What does it not cover?", "Securitisation exposures and counterparty credit risk under SA-CCR are not included. CVA uses the basic approach only, and the market risk standardised approach uses simplified risk weights."),
            ("How is it different from the Capital / Regulatory Model?", "The Capital Model plans the capital base, buffers, Pillar 2 and the five-year capital plan on the current rules. This calculator goes deep on RWA under the final reforms: the new standardised approach, IRB, the output floor, FRTB, SMA and CVA."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 17 tabs &middot; 12 exposure classes &middot; 20 quarters &times; 4 scenarios &middot; 65 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Capital / Regulatory Model", "/bank-capital-model-excel.html"),
            ("ICAAP Model", "/icaap-model-excel.html"),
            ("Credit Stress Test &amp; Capital Model", "/credit-stress-test-model-excel.html"),
        ],
    },
    # ── LCR / NSFR ──────────────────────────────────────────────────────
    {
        "id": "lcr",
        "slug": "lcr-model-excel",
        "title": "LCR and NSFR Model in Excel: Liquidity Stress Testing",
        "h1": "LCR Model: Liquidity Coverage and NSFR",
        "meta": "LCR model in Excel. HQLA levels, haircuts and caps, outflows, inflow cap, NSFR, three liquidity stress scenarios with 90-day survival, 60-month projection.",
        "keywords": "lcr model excel, liquidity coverage ratio calculation excel, nsfr calculation excel, hqla calculation, liquidity stress test model",
        "hero": "The liquidity coverage ratio and the net stable funding ratio, projected monthly for five years. HQLA by level with haircuts and caps, outflows and inflows by category, three stress scenarios with 90-day survival, and a maturity ladder.",
        "problem": [
            "The LCR itself is one division. Getting it right is not: Level 2 and 2B caps applied after haircuts, the 75% inflow cap, the right run-off rate for each deposit class, and a projection that shows where the ratio is heading, not just where it stands today.",
            "This model handles those mechanics and extends them into what liquidity teams need for an ILAAP and for ALCO: the NSFR, idiosyncratic and market-wide stress, a maturity ladder, a funding plan and intraday monitoring.",
        ],
        "who": "Treasury and liquidity risk teams at banks and building societies. Teams preparing an ILAAP or the liquidity section of an ALCO pack. Finance and risk professionals who need to model the LCR effect of balance sheet plans.",
        "tabs": [
            ("INSTRUCTIONS", "Methodology and regulatory references: CRR2, BCBS 238, EBA GL/2017/01 and PRA SS24/15."),
            ("INPUTS", "Every assumption, with a scenario selector across Base, Stress, Severe and Custom."),
            ("HQLA", "High quality liquid assets by Level 1, 2A and 2B, with haircuts and the 40% and 15% caps, over 60 months."),
            ("OUTFLOWS", "Cash outflows by category: stable and less stable retail, operational and non-operational wholesale, secured funding, facilities."),
            ("INFLOWS", "Cash inflows by category, capped at 75% of gross outflows."),
            ("LCR_CALC", "The LCR and compliance against the 100% minimum, month by month."),
            ("NSFR", "Available and required stable funding with ASF and RSF factors."),
            ("STRESS_TEST", "Idiosyncratic, market-wide and combined scenarios with 90-day survival analysis."),
            ("MATURITY_LADDER", "Asset and liability maturity mismatch and cumulative gap."),
            ("FUNDING_PLAN", "12-month funding plan and issuance schedule."),
            ("INTRADAY", "Intraday liquidity monitoring."),
            ("DASHBOARD", "Executive dashboard with six charts."),
            ("SENSITIVITY", "Two-way sensitivity analysis."),
            ("CHECKS", "55 integrity checks."),
        ],
        "diffs": [
            ("Caps applied correctly", "Level 2 assets capped at 40% and Level 2B at 15% of HQLA after haircuts, and inflows capped at 75% of outflows. These are where hand-built LCR spreadsheets most often go wrong."),
            ("Projected, not just measured", "Five years of monthly HQLA, outflows and inflows, so you can see the ratio respond to growth plans, deposit mix changes and maturing funding."),
            ("Three stress scenarios with survival", "Idiosyncratic, market-wide and combined stress, each with a 90-day survival horizon. Parameters are inputs."),
            ("LCR and NSFR together", "Short-term and structural liquidity in one workbook, from the same balance sheet."),
            ("Built for ILAAP and ALCO", "Maturity ladder, funding plan and intraday monitoring alongside the ratios, with a one-page dashboard."),
        ],
        "faqs": [
            ("Which rules does it follow?", "CRR2 and the Basel III LCR (BCBS 238), with HQLA haircuts and caps per the Delegated Regulation, NSFR factors per CRR2, and references to PRA SS24/15. Run-off rates are set at regulatory minimums; calibrate higher where your experience shows it."),
            ("Can I use it for regulatory submissions?", "It is a projection and planning model. Regulatory returns need counterparty-level data and validation against your own systems; this model shows where the numbers are heading and why."),
            ("How is it different from the ILAAP Model?", "The ILAAP Model frames the full internal liquidity adequacy assessment. This model is the calculation engine for the LCR and NSFR, with stress testing and a maturity ladder."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 17 tabs &middot; 60-month projection &middot; 3 stress scenarios &middot; 55 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("ILAAP Model", "/ilaap-model-excel.html"),
            ("Bank Deposits Model", "/bank-deposits-model-excel.html"),
            ("Blog: Building an ILAAP liquidity model", "/blog/ilaap-liquidity-model.html"),
        ],
    },
    # ── Capital / Regulatory ────────────────────────────────────────────
    {
        "id": "capital",
        "slug": "bank-capital-model-excel",
        "title": "Bank Capital Model in Excel: CET1, Buffers, Pillar 2",
        "h1": "Capital &amp; Regulatory Model",
        "meta": "Bank capital model in Excel. CET1, AT1 and Tier 2 with deductions, RWA, buffers and MDA trigger, Pillar 2A and 2B, stress and a five-year capital plan.",
        "keywords": "bank capital model excel, capital adequacy model, cet1 ratio calculation excel, capital planning model bank, mda trigger calculation",
        "hero": "The capital stack, risk-weighted assets, buffers and Pillar 2 in one model, projected monthly for five years. See the CET1 ratio against the MDA trigger under base and stress, and plan the capital that keeps you above it.",
        "problem": [
            "Capital adequacy is a chain: instruments less deductions give CET1, RWA set the denominator, Pillar 1, Pillar 2A and the combined buffer stack up to the MDA trigger. A break anywhere in that chain is how a bank ends up surprised by its own headroom.",
            "This model sets the whole chain out on separate, traceable tabs and projects it forward, so capital planning, stress and the board view all come from the same numbers.",
        ],
        "who": "Capital management, finance and treasury teams at banks and building societies. Teams preparing the ICAAP capital plan or board capital papers. Analysts and consultants assessing a bank's capital position.",
        "tabs": [
            ("INSTRUCTIONS", "How to run the model, step by step."),
            ("INPUTS", "Every assumption, with a scenario selector across Base, Upside, Downside and Severe."),
            ("CAPITAL_BASE", "CET1, AT1 and Tier 2 over 60 months, with deductions: goodwill, intangibles, deferred tax assets, significant investments, pension deficit, own credit and prudent valuation."),
            ("CREDIT_RWA", "Credit RWA under the standardised approach across 10 exposure classes."),
            ("MARKET_RWA", "Market risk capital charge from VaR inputs."),
            ("OP_RISK_RWA", "Operational risk RWA under the Basic Indicator Approach."),
            ("TOTAL_RWA", "Consolidated RWA summary."),
            ("RATIOS", "CET1, Tier 1 and total capital ratios against regulatory minimums."),
            ("BUFFERS", "Capital conservation, countercyclical and systemic buffers, and the MDA trigger."),
            ("PILLAR2", "Pillar 2A and 2B and the ICAAP surplus."),
            ("STRESS", "Three stress scenarios over 60 months: losses after tax and RWA uplift, and the stressed CET1 ratio."),
            ("CAPITAL_PLAN", "Five-year capital plan."),
            ("DASHBOARD", "Executive dashboard with six charts."),
            ("SENSITIVITY", "Two-way sensitivity analysis."),
            ("CHECKS", "64 integrity checks."),
        ],
        "diffs": [
            ("Deductions done properly", "CET1 is built from qualifying instruments less the full list of regulatory deductions, each on its own line, so the capital number can be traced to the balance sheet."),
            ("The MDA trigger, explicit", "Pillar 1 CET1, Pillar 2A CET1 and the combined buffer requirement add up to the MDA trigger, shown against the projected CET1 ratio month by month."),
            ("Pillar 2 and the ICAAP surplus", "Pillar 2A and 2B sit in the stack, so the surplus over total requirement is visible, not just the surplus over Pillar 1."),
            ("Stress on both sides of the ratio", "Each stress scenario applies after-tax losses to capital and an uplift to RWA, so the ratio is hit from both directions."),
            ("Plan and board view from one source", "The five-year capital plan and the dashboard read from the same engine as the ratios."),
        ],
        "faqs": [
            ("Which rules is it based on?", "The Basel III capital framework as applied by the PRA in the UK, with references to the PRA Rulebook and the onshored CRR. Rates such as buffers and Pillar 2A are inputs."),
            ("What does it not do?", "Risk weights are static, with no credit migration. Operational risk uses the Basic Indicator Approach. Counterparty credit risk under SA-CCR and MREL are not included. For the Basel 3.1 RWA changes, see the Basel IV RWA Calculator."),
            ("How does it relate to the ICAAP Model?", "The ICAAP Model frames the whole internal capital adequacy assessment. This model is the capital engine: the stack, RWA, buffers, Pillar 2, stress and the capital plan."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 18 tabs &middot; 60-month projection &middot; 10 exposure classes &middot; 64 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Basel IV RWA Calculator", "/basel-iv-rwa-model-excel.html"),
            ("ICAAP Model", "/icaap-model-excel.html"),
            ("Bank Stress Test Model", "/bank-stress-test-model.html"),
            ("Blog: Reverse stress testing for banks", "/blog/reverse-stress-testing-bank.html"),
        ],
    },
    # ── Lending ─────────────────────────────────────────────────────────
    {
        "id": "lending",
        "slug": "loan-portfolio-model-excel",
        "title": "Bank Lending Model in Excel: Loan Portfolio and NIM",
        "h1": "Lending Model",
        "meta": "Bank lending model in Excel. Eight loan products, rate-locked vintage engine, prepayment and default, P&L, IFRS 9 staging, RWA and NIM analytics.",
        "keywords": "bank lending model excel, loan portfolio model excel, vintage analysis excel, nim model bank, loan book projection",
        "hero": "Project a loan book of eight products month by month: originations, repayments, prepayments, defaults and recoveries, with interest earned on rate-locked vintages. Out come the P&amp;L, IFRS 9 provisions, RWA and a NIM you can explain.",
        "problem": [
            "A lending budget that applies today's rate to the whole book gets NIM wrong in any rate cycle. Existing loans keep the rate they were written at; only new business reprices. The gap between front book and back book is where margin forecasts fail.",
            "This model tracks every origination month as its own vintage with its rate locked, so the NIM path reflects how the book actually reprices, and links it through to provisions and capital.",
        ],
        "who": "FP&amp;A and finance teams at banks, building societies and specialist lenders building the lending budget or plan. Treasury and ALM teams forecasting NIM. Lending heads who need volume, margin, losses and capital in one view.",
        "tabs": [
            ("INSTRUCTIONS", "How to run the model and common uses: budget, stress, board reporting, ICAAP support."),
            ("INPUTS", "Opening balances, origination volumes, contract rates and rate trajectory, prepayment and default rates, LGD, stage allocations, risk weights, funding costs, opex and tax, with a Base, Upside and Downside selector."),
            ("ENGINE", "Monthly roll-forward for eight products: residential, buy-to-let, CRE, SME, corporate, consumer unsecured, cards and government-guaranteed lending."),
            ("VINTAGES", "Cohort matrix: each origination month locks its rate and amortises on its own."),
            ("INCOME", "Monthly P&amp;L from interest through cost of funds, fees, opex and provisions to net profit."),
            ("ECL", "IFRS 9 Stage 1, 2 and 3 provisions, coverage ratios and cost of risk."),
            ("RWA", "Standardised credit RWA by product and operational RWA."),
            ("ANALYTICS", "NIM decomposition, portfolio mix, asset quality and yield waterfall."),
            ("SENSITIVITY", "Two-way tables for NIM and net profit against rates, default and prepayment."),
            ("OUTPUTS", "Executive dashboard with charts."),
            ("CHECKS", "16 integrity checks, including vintage interest tying to the engine and stage allocations summing to 100%."),
        ],
        "diffs": [
            ("Rate-locked vintages", "Interest is calculated on each vintage at the rate it was originated, so a rising or falling rate trajectory flows through to new business while the back book holds its rate."),
            ("A full roll-forward per product", "Opening, originations, scheduled repayment, prepayment, default, recovery, closing. Prepayment and default use annual CPR and CDR converted to monthly rates."),
            ("From volume to capital", "Balances drive the P&amp;L, the IFRS 9 provision and standardised RWA, so a change in origination plans shows up in margin, losses and capital together."),
            ("NIM you can explain", "ANALYTICS breaks NIM down into yield, funding cost and mix, so you can tell the board why it moved."),
            ("Eight UK-style products", "Residential and buy-to-let mortgages, CRE, SME, corporate, unsecured, cards and government-guaranteed schemes, each with its own assumptions."),
        ],
        "faqs": [
            ("How detailed is the IFRS 9 calculation?", "Stage allocations are percentages by product, with ECL as balance times PD times LGD and a lifetime approximation for Stage 2. For loan-by-loan staging, see the IFRS 9 ECL Model: Loan-Level Edition."),
            ("Can I change the products?", "Every volume, rate and risk assumption is set per product on INPUTS, and the eight rows can be relabelled for the lending products you run."),
            ("Does it handle changing interest rates?", "Yes. A rate trajectory sets the rate on new originations year by year, and each vintage keeps its own rate."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 14 tabs &middot; 8 lending products &middot; 60 months, vintage engine &middot; 16 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Bank Deposits Model", "/bank-deposits-model-excel.html"),
            ("IFRS 9 ECL Model: Loan-Level Edition", "/ifrs9-loan-level-ecl-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
        ],
    },
    # ── Deposits ────────────────────────────────────────────────────────
    {
        "id": "deposits",
        "slug": "bank-deposits-model-excel",
        "title": "Bank Deposits Model in Excel: Pricing, Beta, FTP",
        "h1": "Deposits Model",
        "meta": "Bank deposits model in Excel. Seven products, deposit beta with lag, cost of funds, FTP margin, behavioural maturity, LCR and NSFR contribution.",
        "keywords": "bank deposits model excel, deposit beta model, deposit pricing model excel, cost of funds model, ftp model bank",
        "hero": "Model a deposit book of seven products over 60 months: balances, rates with deposit beta and lag, cost of funds, FTP margin, behavioural maturity and the book's contribution to the LCR and NSFR.",
        "problem": [
            "Deposit pricing decides most of a bank's margin, and it rarely moves one for one with the base rate. How much of each rate change you pass on, and how quickly, is the assumption behind every NIM forecast and every ALCO pricing decision.",
            "This model makes that assumption explicit per product, with a beta, a lag and a floor, and follows it through to cost of funds, FTP margin, liquidity value and P&amp;L contribution.",
        ],
        "who": "Treasury, ALM and finance teams at banks and building societies. Savings and deposit product teams setting rates. ALCO members who need the margin and liquidity effect of a pricing decision in one place.",
        "tabs": [
            ("INSTRUCTIONS", "Step-by-step guide and common uses: board reporting, stress, product launch, rate sensitivity, ALCO pack."),
            ("INPUTS", "Base rate path, FTP rate, opening balances and flow rates, floors, betas and lags for each product, with a Base, Upside and Downside selector."),
            ("BOOK", "Monthly balances for current accounts, instant access, 30 and 90-day notice, one and two-year fixed, and ISAs."),
            ("PRICING", "Effective product rates from the floor, beta and lagged base rate, and interest expense on average balances."),
            ("BEHAVIOURAL", "Behavioural maturity using stickiness, core deposits and decay rates."),
            ("LIQUIDITY", "Each product's LCR outflows and NSFR available stable funding."),
            ("FTP", "Funds transfer pricing credit and margin by product."),
            ("PL", "Deposit book P&amp;L contribution."),
            ("SENSITIVITY", "NIM and contribution sensitivities."),
            ("OUTPUTS", "Eight KPIs and six charts, board-ready."),
            ("CHECKS", "27 integrity checks."),
        ],
        "diffs": [
            ("Beta, lag and floor per product", "Effective rate = MAX(floor, floor + beta x (lagged base rate - floor base)). Each product has its own beta and its own lag in months, so instant access and fixed-term deposits respond differently."),
            ("Margin through FTP", "Each product is credited at the FTP rate, so you can see which products earn their keep and which cost more than they are worth."),
            ("Liquidity value alongside margin", "LCR outflow rates and NSFR ASF factors per product show what each pound of deposits is worth for liquidity, not just what it costs."),
            ("Behavioural maturity", "Stickiness and core deposit assumptions shift contractual maturities to behavioural ones."),
            ("No circularity", "Interest uses average balances, so the model calculates cleanly without iterative calculation switched on."),
        ],
        "faqs": [
            ("How is it different from the Deposit Pricing &amp; NII Model?", "The Deposit Pricing &amp; NII Model focuses on pricing and net interest income. This model covers the whole deposit book: balances, pricing, behavioural maturity, liquidity value, FTP and P&amp;L contribution."),
            ("Can I add or rename products?", "Every balance, flow and pricing assumption is set per product on INPUTS, and the seven rows can be relabelled for your own range. Adding a product means extending the formulas on BOOK."),
            ("Which liquidity rules does it use?", "Basel III LCR outflow rates and NSFR available stable funding factors as defaults, editable if your regulator sets different add-ons."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 14 tabs &middot; 7 deposit products &middot; 60-month projection &middot; 27 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Lending Model", "/loan-portfolio-model-excel.html"),
            ("LCR Model", "/lcr-model-excel.html"),
            ("IRRBB Model", "/irrbb-model-excel.html"),
            ("Blog: Calibrating deposit beta", "/blog/deposit-beta-calibration.html"),
        ],
    },
    # ════════════════════════════════════════════════════════════════════
    # Batch 3 (18 Nov 2026): treasury, ALM and credit models with no page.
    # Content from each workbook's COVER, INSTRUCTIONS and NOTES tabs.
    # ════════════════════════════════════════════════════════════════════
    # ── VaR ─────────────────────────────────────────────────────────────
    {
        "id": "var",
        "slug": "var-model-excel",
        "title": "Value at Risk Model in Excel: Three Methods, Backtest",
        "h1": "Value at Risk (VaR) Model",
        "meta": "VaR model in Excel. Parametric, historical and Monte Carlo VaR, expected shortfall, component VaR, stressed VaR and Basel traffic-light backtesting.",
        "keywords": "var model excel, value at risk excel, historical simulation var excel, monte carlo var excel, var backtesting kupiec",
        "hero": "Value at Risk three ways on one portfolio: parametric, historical simulation and Monte Carlo. With expected shortfall, component and marginal VaR, stressed VaR, limits and a 250-day backtest scored on the Basel traffic light.",
        "problem": [
            "A single VaR number hides its own assumptions. Parametric VaR assumes normal returns, historical simulation is only as good as its window, and Monte Carlo inherits whatever you feed it. Risk committees and auditors increasingly ask to see the methods side by side and to know whether the model has been right.",
            "This model calculates all three on the same positions, decomposes the result by asset, stresses it, and backtests it against 250 days of P&amp;L with the Basel traffic light and the Kupiec test.",
        ],
        "who": "Market risk and treasury risk teams. Finance professionals who need to explain VaR to a risk committee. Students and analysts learning how the three methods differ on real calculations.",
        "tabs": [
            ("INPUTS", "Positions, holding period (1 or 10 days), confidence level (95% or 99%), stress factors and limits, with a scenario selector across Base, Stressed, Crisis and Custom."),
            ("MARKET_DATA", "250 trading days of prices across 10 assets."),
            ("RETURNS_ANALYSIS", "Return statistics: volatility, skewness and kurtosis."),
            ("CORRELATION", "Full correlation and covariance matrices."),
            ("PARAMETRIC_VAR", "Variance-covariance VaR from the full covariance matrix."),
            ("HISTORICAL_VAR", "Full revaluation over the historical window, with expected shortfall."),
            ("MONTE_CARLO_VAR", "Simulated P&amp;L distribution and its percentile."),
            ("COMPONENT_VAR", "Component and marginal VaR by asset, and the diversification benefit."),
            ("STRESSED_VAR", "Stressed volatilities and correlations converging towards one."),
            ("BACKTESTING", "250 days of actual P&amp;L against predicted VaR, the Basel traffic light and the Kupiec test."),
            ("LIMITS", "Risk utilisation against approved limits."),
            ("DASHBOARD", "Charts summarising the risk profile."),
            ("SENSITIVITY", "Two-way tables for the main risk drivers."),
            ("CHECKS", "55 integrity checks."),
        ],
        "diffs": [
            ("Three methods, one portfolio", "Parametric, historical and Monte Carlo VaR on the same positions, so the gap between them is visible and explainable."),
            ("Expected shortfall alongside VaR", "The average loss beyond VaR, calculated from the historical distribution: the measure FRTB moved the trading book towards."),
            ("Where the risk comes from", "Component VaR and marginal VaR by asset, with the diversification benefit shown explicitly."),
            ("Stress that removes diversification", "Stressed VaR multiplies volatilities and pushes correlations towards one, which is what happens in a real crisis."),
            ("Backtested the regulatory way", "Exceptions over 250 days scored on the Basel traffic light (green up to 4, amber 5 to 9, red 10 or more) and tested with the Kupiec proportion-of-failures test."),
        ],
        "faqs": [
            ("Can I use my own positions and data?", "Yes. Positions, holding period, confidence level and the market data window are inputs. Replace the 250 days of prices on MARKET_DATA with your own series."),
            ("Does it handle options?", "No. It is a linear VaR model, so it does not capture option gamma or convexity. Multi-day VaR uses the square-root-of-time rule."),
            ("How many simulations does the Monte Carlo use?", "250 scenarios drawn from the estimated distribution, which keeps it fast in Excel. It shows the method clearly; production Monte Carlo engines run many more paths."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 18 tabs &middot; 10 assets &times; 250 days &middot; 3 VaR methods &middot; 55 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Basel IV RWA Calculator", "/basel-iv-rwa-model-excel.html"),
            ("Treasury / Interest Rate Swap Model", "/interest-rate-swap-model-excel.html"),
            ("Bank Stress Test Model", "/bank-stress-test-model.html"),
        ],
    },
    # ── NIM Budget Tracking ─────────────────────────────────────────────
    {
        "id": "nim-budget-tracking",
        "slug": "nim-variance-model-excel",
        "title": "NIM Bridge Model in Excel: NII Budget vs Actual",
        "h1": "NIM Budget Tracking Model",
        "meta": "NIM budget vs actual model in Excel. NII variance split into volume, price, mix, base rate and spread, a full NIM walk and RAG status for ALCO.",
        "keywords": "nim bridge excel, nii variance analysis, nim walk, net interest margin budget vs actual, volume price mix variance bank",
        "hero": "Explain every basis point between budget NIM and actual NIM. Net interest income variance broken into volume, price, mix, base rate and spread across lending, deposits and treasury, with a step-by-step NIM walk for ALCO.",
        "problem": [
            "When NIM misses budget, the first question at ALCO is why: balances, pricing, mix, the base rate or something else. Most finance teams rebuild that bridge by hand every month, and the pieces rarely add back to the total.",
            "This model does the decomposition once, consistently, and reconciles it: volume, price, mix and the cross term add to the total NII variance, and the NIM walk runs from budget to actual in more than 16 steps.",
        ],
        "who": "Bank FP&amp;A and finance business partners producing monthly NII and NIM commentary. ALCO secretaries and treasury teams. Finance directors who need the margin story in one page.",
        "tabs": [
            ("INPUTS", "Scenario (Base, Stress, Outperform, Custom), base rate paths, FTP add-on, pass-through betas and RAG thresholds."),
            ("ACTUALS", "Actual monthly average balances, rates and NII by product."),
            ("BUDGET", "Budget balances, rates and NII in the same structure."),
            ("VPM_ANALYSIS", "Volume, price and mix variance for every product, with subtotals by category and a group total."),
            ("RATE_ANALYSIS", "Book composition, new business and the monthly base rate impact, with a period selector."),
            ("NIM_WALK", "The bridge from budget NIM to actual NIM in more than 16 steps: base rate, customer spread, FTP, hedging and mix."),
            ("RATE_IMPACT", "The base rate effect by segment, using configurable betas."),
            ("DASHBOARD", "Executive KPIs, RAG status and narrative."),
            ("CHECKS", "Reconciliation checks: the variance components must add to the total."),
        ],
        "diffs": [
            ("A decomposition that adds up", "Volume, price, mix and the cross term sum exactly to the total NII variance, and CHECKS proves it each month."),
            ("Base rate separated from pricing", "The base rate effect is isolated with pass-through betas for lending, deposits and treasury, so management pricing decisions show on their own."),
            ("A NIM walk ALCO can read", "More than 16 steps from budget to actual NIM, each one labelled."),
            ("Product, category and group", "VPM by product rolls up to lending, deposits and treasury and to the group, on one tab."),
            ("RAG you can tune", "Variance thresholds for green, amber and red are inputs."),
        ],
        "faqs": [
            ("What data do I need?", "Monthly average balances and rates by product, for actuals and budget. The structure of both tabs is the same, so you paste in two blocks."),
            ("Which base rate does it assume?", "It is set up for the Bank of England base rate with configurable betas, but the rate path is an input, so it works for any policy rate."),
            ("How is it different from the Deposit Pricing &amp; NII Model?", "That model projects deposit pricing and NII forward. This one explains the past: actuals against budget, decomposed."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 13 tabs &middot; lending, deposits and treasury &middot; 16+ step NIM walk &middot; no macros &middot; instant download",
        "related": [
            ("Deposit Pricing &amp; NII Model", "/deposit-pricing-nii-model-excel.html"),
            ("Lending Model", "/loan-portfolio-model-excel.html"),
            ("Bank Deposits Model", "/bank-deposits-model-excel.html"),
        ],
    },
    # ── Deposit Pricing & NII ───────────────────────────────────────────
    {
        "id": "deposit-nii",
        "slug": "deposit-pricing-nii-model-excel",
        "title": "Deposit Pricing and NII Model in Excel",
        "h1": "Deposit Pricing &amp; NII Model",
        "meta": "Deposit pricing model in Excel. Beta and lag by product, front book vs back book, NII and NIM over 60 months, pricing optimisation and repricing gap.",
        "keywords": "deposit pricing model excel, nii model excel, deposit beta lag, front book back book, nii at risk",
        "hero": "Project deposit balances, rates and net interest income over 60 months, then test pricing decisions: what a rate change does to volume, cannibalisation, product margin and NII at risk.",
        "problem": [
            "Every savings rate decision trades margin against balances, and a rate rise on one product pulls money from another. The question at pricing committee is rarely the cost of one product; it is the net effect on NII across the range.",
            "This model puts that trade-off in one place: beta and lag by product, front book against back book, product profitability after FTP, and a pricing optimisation tab that shows cannibalisation.",
        ],
        "who": "Savings and deposit pricing teams. Treasury and ALM teams forecasting NII. Finance business partners supporting pricing committee and ALCO.",
        "tabs": [
            ("INPUTS", "Bank Rate forward curve, opening balances, growth, betas, lags, spreads and floors per product, with Base, Upside, Downside and Stress scenarios."),
            ("BALANCES", "60-month balances: inflows, withdrawals, maturities and rollovers for fixed-term products."),
            ("RATE_ENGINE", "Effective rate by product = MAX(floor, Bank Rate x beta - spread), with lag, and front book against back book."),
            ("NII_CALC", "Interest expense, income on deployed funds, NII and NIM."),
            ("PROFITABILITY", "FTP credit, interest expense and direct costs by product, ranked by margin per million and cost per account."),
            ("PRICING_OPT", "Rate optimisation and cannibalisation analysis."),
            ("REPRICING", "Repricing gap and NII at risk."),
            ("DASHBOARD", "Seven charts."),
            ("SENSITIVITY", "NII impact of rate and beta changes."),
            ("CHECKS", "37 integrity checks."),
        ],
        "diffs": [
            ("Beta, lag and floor by product", "Each product passes on rate changes at its own speed and to its own extent, with a floor so rates never go below what you would pay."),
            ("Front book against back book", "New business and existing balances priced separately, so you can see the cost of the rate differential."),
            ("Cannibalisation in the pricing test", "PRICING_OPT shows the flows between products when one rate moves, so the net NII effect is visible."),
            ("Product economics after FTP", "Net contribution per product after the FTP credit and direct costs, ranked."),
            ("NII at risk", "A repricing gap and the NII effect of parallel rate shifts."),
        ],
        "faqs": [
            ("How is it different from the Deposits Model?", "The Deposits Model covers the whole deposit book including behavioural maturity and liquidity value. This model goes deeper on pricing: front and back book, optimisation, cannibalisation and NII at risk."),
            ("What does it not include?", "Regulatory costs such as the FSCS levy are not in the pricing, market share is static rather than linked to competitor rates, and NII sensitivity assumes parallel curve shifts."),
            ("Which day count does it use?", "Actual/365."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 14 tabs &middot; 60-month projection &middot; 4 scenarios &middot; 37 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Bank Deposits Model", "/bank-deposits-model-excel.html"),
            ("NIM Budget Tracking Model", "/nim-variance-model-excel.html"),
            ("IRRBB Model", "/irrbb-model-excel.html"),
            ("Blog: Calibrating deposit beta", "/blog/deposit-beta-calibration.html"),
        ],
    },
    # ── Treasury / IRS ──────────────────────────────────────────────────
    {
        "id": "treasury",
        "slug": "interest-rate-swap-model-excel",
        "title": "Interest Rate Swap Model in Excel: Pricing, MTM, DV01",
        "h1": "Treasury / Interest Rate Swap Model",
        "meta": "Interest rate swap model in Excel. Bootstrapped zero and forward curves, swap pricing, 20-swap portfolio with MTM and DV01, hedge effectiveness, stress.",
        "keywords": "interest rate swap model excel, swap pricing excel, dv01 calculation excel, yield curve bootstrapping excel, swap mtm",
        "hero": "Build the curve, price the swap, run the book. Zero and forward curves bootstrapped from par rates, a full swap pricing engine, a 20-swap portfolio with mark-to-market and DV01 per position, hedge effectiveness and nine stress scenarios.",
        "problem": [
            "Treasury teams that hedge with swaps need to know three things quickly: what the book is worth, how much it moves for a basis point, and whether the hedges still work. Those answers usually sit in a vendor system that finance cannot open or check.",
            "This model sets out the whole chain in formulas: curve construction, pricing, portfolio valuation, risk and hedge effectiveness, so every number can be traced and challenged.",
        ],
        "who": "Treasury and ALM teams at banks and corporates that hedge interest rate risk. Finance teams checking a counterparty's valuation. Analysts learning curve construction and swap pricing properly.",
        "tabs": [
            ("INPUTS", "Par curve by tenor, swap portfolio terms (notional, fixed rate, pay or receive), and Base, Upside, Downside and Stress scenarios."),
            ("CURVE", "Par, zero and forward curves, with zero rates bootstrapped from par."),
            ("CURVE_DETAIL", "Curve construction detail by tenor."),
            ("IRS_PRICING", "Single swap pricing engine with full cash flow detail."),
            ("SWAP_PORT", "20-swap portfolio with MTM and DV01 per position."),
            ("CASHFLOWS", "60-month aggregate net cash flow projection."),
            ("HEDGING", "Hedge effectiveness and basis risk."),
            ("RISK", "DV01 ladder, parametric VaR and nine stress scenarios."),
            ("GREEKS", "Rate sensitivities."),
            ("MATURITY_PROFILE", "Notional and risk by maturity."),
            ("DASHBOARD", "Seven charts."),
            ("SENSITIVITY", "Two-way tables for portfolio MTM."),
            ("CHECKS", "15 integrity checks."),
        ],
        "diffs": [
            ("A curve you can see being built", "Zero rates bootstrapped from market par rates and forwards derived by no-arbitrage, step by step."),
            ("DV01 by bump and reprice", "Each swap is revalued under a one basis point shift, not approximated from duration."),
            ("A real portfolio, not one swap", "Twenty positions, pay and receive, with MTM, DV01 and cash flows aggregated."),
            ("Hedge effectiveness and basis risk", "Effectiveness as the ratio of hedge to exposure DV01, tested against the 80% to 125% band, with SONIA-swap basis risk."),
            ("Nine stress scenarios", "Shifts to the short and long ends with non-parallel moves interpolated between them."),
        ],
        "faqs": [
            ("Which curve does it use?", "Any curve you enter: par swap rates by tenor on INPUTS. The defaults are sterling with SONIA-based basis."),
            ("What does it not do?", "It assumes a flat volatility surface, the convexity adjustment is approximate, there is no CVA or DVA, and day counts are simplified for semi-annual periods."),
            ("Can I value my own swaps?", "Yes. Each of the 20 portfolio rows takes its own notional, fixed rate, tenor and direction."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 17 tabs &middot; 20-swap portfolio &middot; 9 stress scenarios &middot; 15 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("IRRBB Model", "/irrbb-model-excel.html"),
            ("Value at Risk Model", "/var-model-excel.html"),
            ("Blog: WACC calculation for banking", "/blog/wacc-calculation-banking.html"),
        ],
    },
    # ── Loan Pricing & RAROC ────────────────────────────────────────────
    {
        "id": "loan-pricing",
        "slug": "loan-pricing-raroc-model-excel",
        "title": "Loan Pricing and RAROC Model in Excel",
        "h1": "Loan Pricing &amp; RAROC Model",
        "meta": "Loan pricing model in Excel. FTP, credit spread, cost and margin build-up for 6 products and 7 risk grades, with RAROC, EVA, ROE and capital allocation.",
        "keywords": "loan pricing model excel, raroc model excel, risk based pricing bank, eva loan profitability, ftp loan pricing",
        "hero": "Price a loan from the ground up: funding cost, credit spread, operating cost and margin, for six products across seven risk grades and ten years. Then see which segments clear the hurdle on RAROC and EVA.",
        "problem": [
            "Loans priced off a rate card or a competitor quote can look profitable and still destroy value once expected loss and the capital they consume are counted. Credit committees increasingly ask for the risk-adjusted return, not just the margin.",
            "This model builds the all-in price from its components and measures the return on the capital each loan uses, so you can see which product and grade combinations create value and which do not.",
        ],
        "who": "Lending, pricing and credit teams at banks and specialist lenders. Finance business partners supporting credit committee. Treasury teams setting FTP.",
        "tabs": [
            ("INPUTS", "Base rates, funding spreads, PD and LGD by grade, operating costs, capital requirements, volumes and grade mix, with Base, Upside, Downside and Stress scenarios."),
            ("FUNDING_COST", "FTP build-up: blended wholesale and retail funding, liquidity premium and HQLA buffer cost."),
            ("CREDIT_SPREAD", "Expected loss plus capital cost plus a migration premium, by product, grade and year."),
            ("OPERATING_COST", "Operating cost allocation by product."),
            ("PRICING_ENGINE", "All-in price for 6 products x 7 grades x 10 years."),
            ("CAPITAL_ALLOC", "Regulatory capital from standardised RWA and the full requirement stack, plus economic capital."),
            ("PROFITABILITY", "RAROC, EVA and ROE by product and grade, against the hurdle rate."),
            ("PORTFOLIO", "Portfolio-level aggregation."),
            ("RATE_SENSITIVITY", "NII impact of parallel shifts from -200 to +200 bps."),
            ("DASHBOARD", "Six charts and KPIs."),
            ("SENSITIVITY", "Two-way data tables."),
            ("CHECKS", "76 integrity checks."),
        ],
        "diffs": [
            ("Price built from its parts", "Funding cost, credit spread, operating cost and margin, each on its own tab, so a committee can see what each loan has to cover."),
            ("Credit spread that includes capital", "Expected loss, the cost of the economic capital the loan consumes at the target return, and a migration premium."),
            ("RAROC and EVA against the hurdle", "Every product and grade combination is shown as value-creating or value-destroying."),
            ("Capital from the real requirement stack", "Regulatory capital uses RWA times CET1 minimum, Pillar 2A and the buffers, with an economic capital multiplier on top."),
            ("A wide grid", "Six products, seven risk grades and ten years: 420 price points, all from one set of inputs."),
        ],
        "faqs": [
            ("Which products and grades does it cover?", "Six loan products and seven risk grades, both editable on INPUTS, priced over ten annual periods."),
            ("What does it not do?", "It runs in annual periods, PD and LGD are constant within a scenario with no term structure of default, and portfolio effects are additive with no correlation between products."),
            ("How is it different from the Lending Model?", "The Lending Model projects a loan book's balances, P&amp;L and capital. This model prices individual products and grades and measures their risk-adjusted return."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo bank, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 16 tabs &middot; 6 products &times; 7 grades &times; 10 years &middot; 76 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Lending Model", "/loan-portfolio-model-excel.html"),
            ("Credit Analysis Model", "/credit-analysis-model-excel.html"),
            ("Capital / Regulatory Model", "/bank-capital-model-excel.html"),
        ],
    },
    # ── Credit Analysis ─────────────────────────────────────────────────
    {
        "id": "credit-analysis",
        "slug": "credit-analysis-model-excel",
        "title": "Corporate Credit Analysis Model in Excel",
        "h1": "Credit Analysis Model",
        "meta": "Corporate credit analysis model in Excel. 15 obligors, ratios, Altman Z-score, rating, PD, LGD, expected loss, covenants, stress and a credit decision.",
        "keywords": "credit analysis model excel, corporate credit model, altman z score excel, credit rating model excel, covenant monitoring excel",
        "hero": "Underwrite and monitor up to 15 corporate borrowers in one workbook: five years of history and five of forecast, ratios, Altman Z-score, a composite rating, PD, LGD and expected loss, covenant headroom, stress and a structured credit decision.",
        "problem": [
            "A credit paper needs the same analysis every time: the financials, the ratios, a rating, a probability of default, the loss if it goes wrong, the covenants and what happens under stress. Done by hand per borrower, it is slow and inconsistent across a portfolio.",
            "This model runs that analysis consistently across 15 obligors and ends in a recommendation for each: approve, approve with conditions, or decline, priced by credit spread.",
        ],
        "who": "Corporate and commercial credit analysts at banks and private credit funds. Relationship and portfolio managers monitoring covenants. Students preparing for credit analyst roles.",
        "tabs": [
            ("INPUTS", "Per-borrower financials, seniority, sector, facility size, tenor and collateral, with Base, Upside, Downside and Stress scenarios."),
            ("FINANCIAL_ANALYSIS", "Income statement history and forecast."),
            ("BALANCE_SHEET", "Balance sheet over ten periods."),
            ("CASH_FLOW", "Cash flow over ten periods."),
            ("RATIOS", "Leverage, coverage, liquidity and profitability ratios."),
            ("CREDIT_SCORING", "Altman Z-score with safe, grey and distress zones, and the Z-prime variant for private companies."),
            ("RATING_ANALYSIS", "Composite rating from AAA to CCC, combining Z-score, leverage and coverage."),
            ("PROBABILITY_DEFAULT", "One-year PD by rating, cumulative five-year PD via a migration matrix, and a through-the-cycle to point-in-time adjustment."),
            ("EXPOSURE_LGD", "LGD by seniority with a collateral haircut and floor, and expected loss."),
            ("COVENANT_MONITORING", "Net debt to EBITDA, interest cover and minimum liquidity headroom."),
            ("STRESS_TESTING", "Revenue and margin shocks and a rate rise, re-running every ratio and rating."),
            ("CREDIT_DECISION", "Approve, approve with conditions or decline, priced by credit spread, per obligor."),
            ("DASHBOARD", "Portfolio-level charts."),
            ("SENSITIVITY", "Two-way sensitivity tables."),
            ("CHECKS", "48 integrity checks."),
        ],
        "diffs": [
            ("A portfolio, not one borrower", "Fifteen obligors analysed the same way, so ratings and decisions are consistent and comparable."),
            ("A rating built from evidence", "Z-score, leverage and coverage each imply a rating; the composite averages them rather than relying on a single factor."),
            ("From rating to expected loss", "One-year and cumulative PD, LGD by seniority after collateral, and expected loss on the facility."),
            ("Covenants with headroom", "Leverage, interest cover and liquidity tested every period, so a breach shows before it happens."),
            ("Stress that re-rates", "Shocks flow through the financials, so ratios, ratings and decisions all respond."),
        ],
        "faqs": [
            ("Does it work for private companies?", "Yes. Use the Z-prime variant, which replaces market value of equity with book value."),
            ("What does it not do?", "Collateral values are static, there is no wrong-way risk modelling, and portfolio correlation between obligors is assumed to be zero. The distance-to-default proxy is simplified."),
            ("How often should I update it?", "With each set of audited annual financials. Inputs are annual."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 19 tabs &middot; 15 obligors &times; 10 periods &middot; 48 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Loan Pricing &amp; RAROC Model", "/loan-pricing-raroc-model-excel.html"),
            ("Credit Fund Model", "/credit-fund-model-excel.html"),
            ("IFRS 9 ECL Model: Loan-Level Edition", "/ifrs9-loan-level-ecl-model-excel.html"),
        ],
    },
    # ════════════════════════════════════════════════════════════════════
    # Batch 4 (18 Nov 2026): valuation and corporate finance models.
    # Content from each workbook's COVER, INSTRUCTIONS and NOTES tabs;
    # check counts from each sample COVER (they exclude summary rows).
    # ════════════════════════════════════════════════════════════════════
    # ── Trading comps ───────────────────────────────────────────────────
    {
        "id": "trading-comps",
        "slug": "trading-comps-model-excel",
        "title": "Trading Comps Model in Excel: Comparable Company Analysis",
        "h1": "Trading Comparables Model",
        "meta": "Trading comps model in Excel. 30 peers, 15+ multiples, screening and outlier removal, peer statistics, regression and implied valuation for the target.",
        "keywords": "trading comps model excel, comparable company analysis excel, comps template excel, ev ebitda multiples, implied valuation",
        "hero": "Value a target against a peer group of up to 30 companies across five sectors: more than 15 multiples, screening with outlier removal, peer statistics, regression of multiples on fundamentals, and an implied valuation range.",
        "problem": [
            "A comps table is easy to build and easy to get wrong. The peer set drifts, one outlier drags the mean, and nobody can say why the target deserves the median rather than the top quartile.",
            "This model makes those judgements explicit: screening rules you set, outliers removed by a standard-deviation test you control, statistics on what is left, and a regression that ties multiples to growth and margins so a premium or discount has a reason.",
        ],
        "who": "Investment banking and corporate development analysts. Equity research and private equity associates. Finance teams valuing a business or a stake for a transaction or an impairment test.",
        "tabs": [
            ("INPUTS", "Target company financials, screening criteria, outlier threshold, control premium, liquidity discount, size and country risk premiums, with Base, Upside, Downside and Stress scenarios."),
            ("COMP_DATA", "Up to 30 comparable companies with eight years of data: three historical, the current year and four forecast."),
            ("VALUATION_METRICS", "More than 15 multiples, including EV/EBITDA, EV/Revenue, P/E and PEG, on trailing and forward bases."),
            ("GROWTH_MARGINS", "Growth rates, margins and returns: ROIC, ROE and ROA."),
            ("SCREENING", "Inclusion and exclusion by market cap and margin, and outlier detection by standard deviations from the mean."),
            ("STATISTICS", "Mean, median and percentiles for each multiple across the screened peers."),
            ("IMPLIED_VALUATION", "Peer multiples applied to the target: implied enterprise value, equity value and share price."),
            ("SECTOR_ANALYSIS", "Sector-level averages and premiums across five sectors."),
            ("REGRESSION", "OLS regression of multiples on operating metrics."),
            ("DASHBOARD", "Charts and visual summary."),
            ("SENSITIVITY", "Implied share price across a range of assumptions."),
            ("CHECKS", "58 integrity checks."),
        ],
        "diffs": [
            ("Screening you can defend", "Peers are included or excluded by rules you set on INPUTS, not by hand, and outliers are removed by a standard-deviation threshold."),
            ("Statistics on the clean set", "Mean, median and percentiles are calculated after screening, so one outlier cannot move the answer."),
            ("A reason for the premium", "Regression of multiples on growth and margins shows what the market pays for fundamentals, so the target's position in the range can be argued."),
            ("Adjustments in the open", "Control premium, liquidity discount, size premium and country risk are explicit inputs, not buried in a chosen multiple."),
            ("Trailing and forward", "Multiples on historical and forecast years side by side."),
        ],
        "faqs": [
            ("Can I use my own peer group?", "Yes. COMP_DATA takes up to 30 companies; replace the pre-loaded data with your own peers and their financials."),
            ("Which currency is it in?", "The demo data is in US dollars, millions. All values are inputs, so any currency works if you are consistent."),
            ("How is it different from the Multi-Method Valuations Model?", "This model goes deep on one method: comparable companies. The Multi-Method model runs six methods side by side, with comps as one of them."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo peer set, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 16 tabs &middot; up to 30 peers &times; 8 years &middot; 15+ multiples &middot; 58 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Precedent Transactions Model", "/precedent-transactions-model-excel.html"),
            ("DCF Model", "/dcf-model-excel.html"),
            ("Multi-Method Valuations Model", "/multi-method-valuation-model-excel.html"),
        ],
    },
    # ── Precedent transactions ──────────────────────────────────────────
    {
        "id": "precedent-transactions",
        "slug": "precedent-transactions-model-excel",
        "title": "Precedent Transactions Model in Excel: M&A Multiples",
        "h1": "Precedent Transactions Model",
        "meta": "Precedent transactions model in Excel. 25 deals, LTM and NTM multiples, takeover premiums, synergies, screening, time trends and implied valuation.",
        "keywords": "precedent transactions model excel, m&a comps excel, transaction multiples, takeover premium analysis, football field valuation",
        "hero": "What have buyers actually paid? A database of up to 25 transactions with LTM and forward multiples, takeover premiums against undisturbed prices, announced synergies, screening, trends over time and an implied valuation for your target.",
        "problem": [
            "Precedent multiples carry a control premium and often synergies, and they come from different points in the cycle. Applied without adjustment, they overstate what a target is worth today.",
            "This model separates the pieces: premiums measured against undisturbed prices one day, one week and four weeks before announcement, synergies on their own tab, and time trends so you can see whether the deals you are citing come from a different market.",
        ],
        "who": "M&A and corporate finance advisors. Corporate development teams pricing an acquisition. Private equity associates benchmarking entry multiples.",
        "tabs": [
            ("INPUTS", "Target financials, screening criteria and premium parameters, with Base, Upside and Downside scenarios."),
            ("DEAL_DATA", "Up to 25 transactions across five sectors with full deal financials."),
            ("DEAL_METRICS", "EV/Revenue, EV/EBITDA, EV/EBIT and P/E on LTM, NTM and NTM+1 bases for every deal."),
            ("PREMIUM_ANALYSIS", "Takeover premiums against undisturbed prices one day, one week and four weeks before announcement."),
            ("SYNERGY_ANALYSIS", "Announced synergies and their effect on the price paid."),
            ("SCREENING", "Include or exclude by date range, sector, deal size, and outliers beyond two standard deviations."),
            ("STATISTICS", "Mean, median, quartiles, high and low, by sector and by year."),
            ("TIME_TRENDS", "How multiples and premiums have moved over time."),
            ("IMPLIED_VALUATION", "Selected multiples applied to the target: enterprise value, equity value and share price, with a football field."),
            ("DASHBOARD", "Charts."),
            ("SENSITIVITY", "Implied share price under different multiple and premium assumptions."),
            ("CHECKS", "49 integrity checks."),
        ],
        "diffs": [
            ("Premiums measured properly", "Against undisturbed share prices at three points before announcement, so leaks and run-ups do not distort the premium."),
            ("Synergies separated", "Announced synergies on their own tab, so you can see how much of the multiple was the buyer's synergy rather than the target's value."),
            ("LTM and forward multiples", "Every deal on trailing and two forward bases."),
            ("Time trends", "Deals from different cycles shown as such, so you choose the relevant window rather than averaging across it."),
            ("A full equity bridge", "Enterprise value = equity value + net debt + minorities + preferred, applied consistently to every deal."),
        ],
        "faqs": [
            ("Can I load my own deals?", "Yes. Replace the pre-loaded transactions on DEAL_DATA with your own set; screening, statistics and the implied valuation update automatically."),
            ("How many scenarios does it have?", "Three: Base, Upside and Downside, switched from one cell on INPUTS."),
            ("How should I use the result?", "As one input in a wider valuation alongside comparable companies and a DCF. The football field shows the ranges together."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo deal set, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 16 tabs &middot; up to 25 transactions &middot; LTM, NTM, NTM+1 &middot; 49 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Trading Comparables Model", "/trading-comps-model-excel.html"),
            ("Merger Consequences Model", "/merger-consequences-model-excel.html"),
            ("LBO Model", "/lbo-model-excel.html"),
        ],
    },
    # ── SOTP ────────────────────────────────────────────────────────────
    {
        "id": "sotp",
        "slug": "sotp-valuation-model-excel",
        "title": "Sum-of-the-Parts (SOTP) Valuation Model in Excel",
        "h1": "Sum-of-the-Parts (SOTP) Valuation Model",
        "meta": "SOTP valuation model in Excel. Eight segments each valued by DCF, comps and precedents, a blended value, conglomerate discount and a football field.",
        "keywords": "sotp valuation model excel, sum of the parts valuation, conglomerate discount, segment valuation excel, break-up valuation",
        "hero": "Value a group one division at a time. Eight segments, each with its own ten-year DCF, comparable multiples and precedent transactions, blended into a group value, then compared with the market to measure the conglomerate discount.",
        "problem": [
            "A diversified group rarely trades at the sum of its parts. Analysts, activists and boards all ask the same question: what is each business worth on its own, and how large is the discount the market applies to the whole?",
            "This model answers it segment by segment, with three methods per segment so no single assumption carries the answer, and benchmarks the implied discount against peers.",
        ],
        "who": "Equity research analysts covering diversified groups. Corporate development and strategy teams assessing disposals or spin-offs. Bank and financial services analysts valuing multi-line institutions.",
        "tabs": [
            ("INPUTS", "Segment revenue, margins, growth, WACC and multiples, with Base, Upside, Downside and Stress scenarios."),
            ("SEGMENT_1 to SEGMENT_8", "Eight segments, each with a ten-year P&amp;L, free cash flow build and DCF. The demo is set up as a diversified financial group: consumer, corporate and investment banking, wealth and asset management, insurance, treasury and markets, and digital."),
            ("COMP_MULTIPLES", "Comparable company and precedent transaction valuations per segment."),
            ("SOTP_SUMMARY", "Blended enterprise value per segment and in total, and equity value per share."),
            ("CONGLOMERATE", "Implied conglomerate discount against peer groups."),
            ("FOOTBALL_FIELD", "Valuation ranges across all methods."),
            ("DASHBOARD", "Six charts for board presentations."),
            ("SENSITIVITY", "Two-way tables for the main value drivers, plus extended sensitivities."),
            ("CHECKS", "63 integrity checks."),
        ],
        "diffs": [
            ("Three methods per segment", "DCF, comparable companies and precedent transactions for every segment, blended 50 / 30 / 20 by default, with the weights as inputs."),
            ("A real DCF per segment", "Ten-year explicit forecast, mid-year discounting, segment-specific WACC from CAPM and a Gordon growth terminal value capped below WACC."),
            ("The conglomerate discount, measured", "The gap between the sum of the parts and the group's market value, benchmarked against peer conglomerates."),
            ("A proper equity bridge", "Enterprise value less net debt, minorities and pension deficit, plus associates."),
            ("Board-ready output", "A football field and six charts showing where each segment's value comes from."),
        ],
        "faqs": [
            ("Is it only for banks?", "No. The demo segments are a diversified financial group, but every segment's name and assumptions are inputs, so it works for any multi-division business."),
            ("Can I use fewer than eight segments?", "Yes. Set unused segments to zero and they drop out of the total."),
            ("What does it not capture?", "Optionality and synergy values are not modelled, and terminal value usually makes up a large share of each segment's DCF, as with any DCF."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo group, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 21 tabs &middot; 8 segments &times; 3 methods &middot; 10-year DCF &middot; 63 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("Trading Comparables Model", "/trading-comps-model-excel.html"),
            ("Blog: Mid-year discounting in a DCF", "/blog/mid-year-discounting-dcf.html"),
        ],
    },
    # ── DDM ─────────────────────────────────────────────────────────────
    {
        "id": "ddm",
        "slug": "dividend-discount-model-excel",
        "title": "Dividend Discount Model in Excel: Bank Valuation",
        "h1": "Dividend Discount Model (DDM)",
        "meta": "Dividend discount model in Excel. Gordon growth, two-stage, H-model, FCFE and residual income for a 10-company peer group, with payout and yield analysis.",
        "keywords": "dividend discount model excel, ddm excel template, h model valuation, residual income model excel, bank valuation model",
        "hero": "Value dividend-paying companies five ways at once: Gordon growth, two-stage, H-model, free cash flow to equity and residual income, across a peer group of ten, with payout and yield analysis and a summary against the market price.",
        "problem": [
            "For banks and other financial institutions, enterprise value and EBITDA mean little, so equity is valued from what shareholders receive. But a single-stage DDM is very sensitive to the growth assumption, and one method alone rarely convinces an investment committee.",
            "This model runs four DDM variants and residual income side by side for ten companies, so you can see where the methods agree, where they diverge and why.",
        ],
        "who": "Equity analysts covering banks, insurers and other dividend payers. Investors screening income stocks. Students and candidates preparing for bank equity research and valuation interviews.",
        "tabs": [
            ("INPUTS", "Per-company assumptions and cost of equity from CAPM, with Base, Upside, Downside and Stress scenarios."),
            ("DIVIDEND_PROJ", "Twenty-year dividend projections for all ten companies."),
            ("GORDON_GROWTH", "Single-stage value = DPS1 / (ke - g)."),
            ("TWO_STAGE", "A high-growth period followed by a Gordon terminal value."),
            ("H_MODEL", "Growth declining linearly from the high rate to the stable rate."),
            ("FCFE_MODEL", "Equity valued on cash available to shareholders, not just dividends paid."),
            ("RESIDUAL_INCOME", "Book value plus the present value of returns above the cost of equity."),
            ("PAYOUT_ANALYSIS", "Payout ratios moving towards a steady state."),
            ("YIELD_ANALYSIS", "Dividend yield and dividend quality, including the Chowder number."),
            ("VALUATION_SUMMARY", "All methods compared, with the premium or discount to market price."),
            ("DASHBOARD", "Charts and visual summaries."),
            ("SENSITIVITY", "Two-way tables for the main value drivers."),
            ("CHECKS", "80 integrity checks."),
        ],
        "diffs": [
            ("Five methods, one peer group", "Gordon growth, two-stage, H-model, FCFE and residual income for ten companies, compared on one summary tab."),
            ("Built for financial institutions", "The demo peer group is ten financial institutions, where dividend-based and residual income valuation are standard."),
            ("Guard rails on growth", "Terminal growth must stay below the cost of equity, and the model checks it."),
            ("Dividend quality, not just value", "Payout path, yield and the Chowder number alongside intrinsic value."),
            ("A signal against the market", "Intrinsic value per share against market price for every company and method."),
        ],
        "faqs": [
            ("Can I use it outside banking?", "Yes. Company names and every assumption are inputs. The notes flag where bank-specific features, such as residual income persisting in perpetuity, need adjusting for other sectors."),
            ("How is the cost of equity set?", "CAPM: risk-free rate plus beta times the equity risk premium, per company."),
            ("How long is the projection?", "Twenty years of dividends, with growth transitioning between stages."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo peer group, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 17 tabs &middot; 10 companies &times; 5 methods &middot; 20-year projection &middot; 80 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("Multi-Method Valuations Model", "/multi-method-valuation-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
            ("Blog: WACC calculation for banking", "/blog/wacc-calculation-banking.html"),
        ],
    },
    # ── Multi-method valuations ─────────────────────────────────────────
    {
        "id": "valuations",
        "slug": "multi-method-valuation-model-excel",
        "title": "Multi-Method Valuation Model in Excel: Football Field",
        "h1": "Multi-Method Valuations Model",
        "meta": "Valuation model in Excel with six methods: DCF, trading comps, precedents, DDM, LBO and asset-based, weighted into one value with a football field.",
        "keywords": "valuation model excel, football field valuation excel, multi method valuation, company valuation template, weighted valuation",
        "hero": "Six valuation methods on one company: DCF, trading comparables, precedent transactions, dividend discount, LBO and asset-based. Weighted into one value, shown on a football field, and bridged from enterprise value to equity.",
        "problem": [
            "Every valuation method answers a slightly different question, and a number from one method alone invites the obvious challenge: what do the others say? Building five or six separate models to answer that, and keeping them consistent, takes days.",
            "This model runs all six from one set of inputs, so the ranges are consistent, the weights are explicit and the football field is ready for the committee.",
        ],
        "who": "Corporate finance and transaction advisory teams. Private equity and corporate development. Finance teams preparing fairness, impairment or shareholder valuations. Candidates preparing for valuation case studies.",
        "tabs": [
            ("INPUTS", "Target financials and WACC assumptions, with Base, Upside, Downside and Stress scenarios."),
            ("DCF", "Ten-year unlevered free cash flow, with Gordon growth and exit multiple terminal values blended."),
            ("TRADING_COMPS", "Fifteen comparable companies on EV/Revenue, EV/EBITDA, EV/EBIT, P/E and P/B."),
            ("PRECEDENT_TXNS", "Fifteen transactions with control premium analysis."),
            ("DDM", "Two-stage dividend discount with a ten-year explicit forecast."),
            ("LBO", "Five-year buyout with three debt tranches, a cash sweep and IRR sensitivity to entry and exit multiples."),
            ("ASSET_BASED", "Book value, adjusted net assets, liquidation value and replacement cost."),
            ("WEIGHTED_VALUATION", "Method weights and the blended value."),
            ("FOOTBALL_FIELD", "Valuation ranges across all six methods."),
            ("EQUITY_BRIDGE", "Enterprise value to equity value."),
            ("DASHBOARD", "Charts and summary metrics."),
            ("SENSITIVITY", "Two-way tables, plus extended sensitivities."),
            ("CHECKS", "115 integrity checks."),
        ],
        "diffs": [
            ("Six methods from one set of inputs", "Change the target's numbers once and every method updates, so the ranges stay consistent."),
            ("Weights you set and can defend", "WEIGHTED_VALUATION makes the blend explicit rather than implicit in a chosen point on the football field."),
            ("An LBO as a valuation floor", "What a financial buyer could pay for a target return, from a three-tranche debt structure."),
            ("Asset-based for downside", "Book, adjusted net assets, liquidation and replacement cost show the floor under the going-concern methods."),
            ("115 integrity checks", "Six methods have to stay consistent with each other and with one set of inputs; the checks prove they do."),
        ],
        "faqs": [
            ("How is it different from buying the separate models?", "The separate DCF, Trading Comps, Precedent Transactions, DDM and LBO models each go deeper on their method. This model runs simplified versions of all six together from one set of inputs, for a consistent range."),
            ("What are the limits?", "Point-in-time data, a simplified LBO with a cash sweep, and a DDM that suits regular dividend payers. Each method's tab states its assumptions."),
            ("Which currency is it in?", "The demo is in US dollars, millions. All values are inputs."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo company, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 18 tabs &middot; 6 valuation methods &middot; 4 scenarios &middot; 115 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("LBO Model", "/lbo-model-excel.html"),
            ("Trading Comparables Model", "/trading-comps-model-excel.html"),
            ("Precedent Transactions Model", "/precedent-transactions-model-excel.html"),
        ],
    },
    # ── Three-statement ─────────────────────────────────────────────────
    {
        "id": "three-statement",
        "slug": "three-statement-model-excel",
        "title": "3-Statement Financial Model in Excel: Integrated IS, BS, CF",
        "h1": "3-Statement Integrated Model",
        "meta": "Three-statement model in Excel. Monthly for 3 years then annual to year 10, five-segment revenue build, working capital, debt and PP&E schedules.",
        "keywords": "three statement model excel, 3 statement financial model, integrated financial model excel, financial model template, balance sheet cash flow model",
        "hero": "An integrated income statement, balance sheet and cash flow: 36 months of monthly detail then annual to year ten, with a five-segment revenue build, working capital, debt and fixed asset schedules, and 193 checks that the statements tie.",
        "problem": [
            "The test of a three-statement model is simple: does the balance sheet balance and does cash tie, every period, in every scenario? Many templates pass in the base case and break the moment you change an assumption.",
            "This model is built to stay tied: interest on prior-period balances so there is no circularity, every schedule reconciled, and integrity checks on every period.",
        ],
        "who": "FP&amp;A teams building a budget or long-range plan. Founders and finance leads preparing investor or lender forecasts. Analysts and students learning how the three statements link.",
        "tabs": [
            ("INPUTS", "Segment volume, price and growth, cost structure, working capital days, capex and debt terms, with Base, Upside, Downside and Stress scenarios."),
            ("REVENUE_BUILD", "Bottom-up revenue across five segments with licence, subscription, project and service revenue."),
            ("INCOME_STATEMENT", "Monthly for 36 months, then annual for years 4 to 10."),
            ("BALANCE_SHEET", "Full balance sheet on the same timeline."),
            ("CASHFLOW", "Indirect cash flow tying to balance sheet cash."),
            ("WORKING_CAPITAL", "Receivables, inventory and payables from days assumptions."),
            ("DEBT_SCHEDULE", "Debt roll-forward with interest on prior-period balances."),
            ("PPE_SCHEDULE", "Capex, straight-line depreciation and net book value."),
            ("RATIOS", "Profitability, liquidity, leverage and return ratios."),
            ("DASHBOARD", "Charts."),
            ("SENSITIVITY", "Two-way tables on year-one metrics."),
            ("CHECKS", "193 integrity checks."),
        ],
        "diffs": [
            ("Checks on every period", "193 integrity checks, including the balance sheet balancing and cash tying in every month and year."),
            ("No circularity", "Interest is calculated on prior-period closing balances, so there is no iterative calculation and nothing to break."),
            ("Monthly where it matters", "Three years monthly for budgeting and cash, then annual to year ten for the long-range view."),
            ("Revenue built, not plugged", "Five segments, each with its own volume, price and growth drivers."),
            ("Scenarios that stay tied", "Four scenarios from one selector, with the statements reconciling in each."),
        ],
        "faqs": [
            ("Can I adapt it to my business?", "Yes. Segment names, revenue drivers and every cost and balance sheet assumption are inputs. The demo is a diversified technology company."),
            ("What does it not include?", "Share issuance and buybacks, seasonality, covenant breach mechanics, foreign exchange and acquisitions beyond PP&amp;E. Deferred tax is simplified, and no tax credit is taken on losses."),
            ("Is it suitable for a bank?", "No. Banks need a balance-sheet-driven model with NII, provisions and capital: see the Bank Long-Term Plan Model."),
            ("Are there macros?", "No. Open formulas, no VBA. Every number traces back to an input."),
            ("Can I see it before I buy?", "Yes. The free sample shows every tab, chart and check with real results on the demo company, plus one engine tab with live formulas."),
        ],
        "spec": "Excel (.xlsx) &middot; 16 tabs &middot; 36 months + years 4-10 &middot; 5 revenue segments &middot; 193 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
            ("Blog: Excel financial model best practices", "/blog/excel-financial-model-best-practices.html"),
        ],
    },

    # ════ Batch 5 (18 Nov 2026): treasury, FP&A, accounting, debt, infra. Drafted by agents, fact-checked. ════
    {'id': 'bond-pricing',
     'slug': 'bond-pricing-yield-model-excel',
     'title': 'Bond Pricing and Yield Model in Excel: 30-Bond Portfolio',
     'h1': 'Bond Pricing &amp; Yield Model',
     'meta': 'Bond pricing model in Excel. Clean and dirty price, duration, DV01 and convexity for 30 bonds, '
             'spread breakdown, 9 rate and credit scenarios, total return.',
     'keywords': 'bond pricing model excel, bond yield calculator excel, bond portfolio analysis excel, dv01 '
                 'convexity excel, fixed income model excel',
     'hero': 'Price a reference bond from its cash flows, then run a 30-bond portfolio of gilts, corporates, '
             'covered bonds and ABS through duration, DV01, convexity, a yield breakdown, nine rate and credit '
             'scenarios and a ten-year total return projection.',
     'problem': ['A bond portfolio is easy to list and harder to explain. Which positions carry the rate risk, '
                 'how much of the yield is credit, and what a 100 basis point move or a spread widening does to '
                 'the book are questions that usually get answered one bond at a time.',
                 "This model answers them across the whole portfolio at once. Every bond's duration, DV01 and "
                 'convexity feed a scenario engine that reprices all 30 positions under parallel shifts, a '
                 'steepener, a flattener, a credit spread widening and a default case, and totals the P&amp;L by '
                 'scenario.'],
     'who': 'Fixed income analysts and portfolio managers. Treasury and investment teams at banks, building '
            'societies and insurers holding gilt and credit portfolios. Students and graduates learning bond '
            'maths on a realistic book.',
     'tabs': [('INPUTS',
               "The reference bond's terms, a 13-point benchmark curve and a swap curve, the 30-bond portfolio "
               '(par, coupon, frequency, maturity, sector, rating and market price) and stress parameters.'),
              ('BOND_PRICING',
               'Reference bond engine: cash flow schedule up to 60 semi-annual periods, clean price, accrued '
               'interest, dirty price, current yield, spread to benchmark and a price-yield table.'),
              ('YIELD_ANALYSIS',
               "Each bond's yield split into risk-free rate, credit spread, I-spread, liquidity premium, carry "
               'and roll-down.'),
              ('DURATION',
               'Macaulay and modified duration, DV01 and convexity for every bond, with a period-by-period '
               'workings block for each.'),
              ('PORTFOLIO',
               'Market value, weights and contributions to yield, duration and convexity; sector, rating and '
               'maturity breakdowns; aggregate portfolio cash flows.'),
              ('TOTAL_RETURN',
               'Ten-year projection of income, price and reinvestment return by bond and for the portfolio, '
               'against a benchmark return.'),
              ('SCENARIOS',
               'Nine scenarios across all 30 bonds: parallel +50, +100, +200, -50 and -100 bp, steepener, '
               'flattener, credit spread +100 bp and a default case at the assumed recovery rate.'),
              ('DASHBOARD', 'Key portfolio metrics and seven charts.'),
              ('SENSITIVITY',
               "Portfolio value for yield shifts from -200 to +200 bp, each bond's impact from a +100 bp shift, "
               'and a credit spread by duration grid.'),
              ('CHECKS',
               '15 integrity checks, including clean price plus accrued equal to dirty price, weights summing to '
               '100% and modified duration below Macaulay for every bond.')],
     'diffs': [('Every bond, not just one',
                'Duration, DV01 and convexity are calculated for all 30 positions and rolled up into portfolio '
                'contributions, so you can see which holdings carry the risk.'),
               ('Nine scenarios on the full book',
                'Rate shifts, curve twists, a credit spread widening and a default case, each with P&amp;L by '
                'bond and a portfolio total.'),
               ('Where the yield comes from',
                'Yield split into risk-free rate, credit spread, liquidity premium, carry and roll-down for '
                'every bond.'),
               ('Five sectors, AAA to CCC',
                'Government, corporate, financial, covered and ABS positions, with sector, rating and maturity '
                'bucket breakdowns.'),
               ('Total return over ten years',
                'Income, price and reinvestment return projected by bond and compared with a benchmark.')],
     'faqs': [('What does it not do?',
               'Each bond is discounted at a single flat yield, not off a zero curve, and portfolio yields are '
               'estimated from coupon and market price rather than solved. Scenarios use the duration and '
               'convexity approximation, total return assumes constant yields and reinvestment rates, and the '
               'default case applies one recovery rate to every bond.'),
              ('Can I load my own portfolio?',
               'Yes. The portfolio table on INPUTS holds 30 bonds: replace the names, ISINs, terms, sectors, '
               'ratings and prices with your own holdings.'),
              ('Which currency is it in?',
               'The demo is a sterling portfolio of gilts and UK credit. Prices and terms are all inputs, so any '
               'currency works if you are consistent.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 14 tabs &middot; 30 bonds &middot; 9 scenarios &middot; 15 integrity checks '
             '&middot; no macros &middot; instant download',
     'related': [('Duration &amp; Rate Sensitivity Model', '/duration-rate-sensitivity-model-excel.html'),
                 ('IRRBB Model', '/irrbb-model-excel.html'),
                 ('Treasury / Interest Rate Swap Model', '/interest-rate-swap-model-excel.html'),
                 ('Value at Risk (VaR) Model', '/var-model-excel.html')]},
    {'id': 'duration',
     'slug': 'duration-rate-sensitivity-model-excel',
     'title': 'Duration and Rate Sensitivity Model in Excel: DV01, EVE',
     'h1': 'Duration &amp; Rate Sensitivity Model',
     'meta': 'Duration model in Excel. Macaulay and modified duration, DV01, convexity and key-rate duration for '
             '20 bonds, duration gap, NII and EVE under rate shocks.',
     'keywords': 'duration model excel, modified duration calculator excel, dv01 excel, key rate duration excel, '
                 'duration gap analysis',
     'hero': 'Measure interest rate risk on a 20-bond portfolio and the funding behind it: a bootstrapped zero '
             'curve, Macaulay and modified duration, DV01, convexity and key-rate duration, repricing across 17 '
             'shocks, a duration gap against six liability lines, NII by repricing bucket and EVE under six '
             'shock scenarios.',
     'problem': ['Duration is the first number anyone asks for on a fixed income book and the one most often '
                 'quoted without its context. A portfolio duration means little without the liabilities it '
                 'funds, the convexity that bends it, and the point on the curve where the exposure sits.',
                 'This model puts those together: duration and convexity bond by bond, key-rate durations across '
                 'eight tenors, a duration and BPV gap against the liability profile, and the effect of the same '
                 'rate moves on net interest income and economic value of equity.'],
     'who': 'ALM, treasury and market risk teams at banks and building societies. Investment teams managing bond '
            'portfolios against liabilities. CFA and FRM candidates and finance students who want duration and '
            'convexity worked through on real cash flows.',
     'tabs': [('INPUTS',
               'Scenario selector, a 20-bond portfolio (face value, coupon, maturity, frequency, yield and '
               'spread), a 15-point par yield curve by scenario, shock levels, key-rate tenors, a six-line '
               'liability profile and the NII repricing profile.'),
              ('YIELD_CURVE',
               'Zero rates bootstrapped from par yields, discount factors, forward rates and an interpolated '
               'quarterly curve.'),
              ('BOND_VALUATION',
               'Cash flow discounting for each of the 20 bonds, with clean price and accrued interest.'),
              ('MACAULAY_DURATION',
               'Period-by-period PV weights and Macaulay duration per bond, and the portfolio total.'),
              ('MODIFIED_DURATION',
               'Modified duration, dollar duration and DV01 per bond, and by maturity bucket.'),
              ('CONVEXITY', 'Convexity per bond from the full cash flow schedule, and the portfolio figure.'),
              ('KEY_RATE_DURATION',
               'Duration allocated across eight key rates from 6 months to 30 years, by bond and for the '
               'portfolio.'),
              ('PRICE_SENSITIVITY',
               'Value change for each bond and the portfolio across 17 shocks from -200 to +200 bp, with the '
               'estimate from duration alone beside the estimate including convexity.'),
              ('NII_SENSITIVITY',
               'Repricing gap across nine buckets from overnight to over five years, and the NII impact of eight '
               'parallel shocks plus a steepener and a flattener.'),
              ('IMMUNISATION',
               'Asset and liability duration, BPV and convexity, the duration and BPV gaps, equity at risk at '
               '+100 and +200 bp, and the adjustment needed to close the gap.'),
              ('EVE',
               'Economic value of equity under parallel +200 and -200 bp, steepener, flattener, short up and '
               'short down, with the worst case and the contribution by bond.'),
              ('DASHBOARD', 'Key risk metrics and six charts.'),
              ('SENSITIVITY',
               'Grids of price change by duration and yield move, convexity benefit for a +200 bp shock, and NII '
               'impact by gap size and shock.'),
              ('CHECKS',
               '55 integrity checks, including discount factors decreasing, modified duration below Macaulay for '
               'every bond and key-rate durations summing to total duration.')],
     'diffs': [('Assets and liabilities together',
                'A six-line liability profile sits beside the bond portfolio, so the model measures the duration '
                'gap, BPV gap and equity at risk, not just portfolio duration.'),
               ('Key-rate duration',
                'Exposure split across eight tenors from 6 months to 30 years shows where on the curve the risk '
                'sits.'),
               ('Convexity shown, not assumed away',
                'PRICE_SENSITIVITY sets the estimate from duration alone beside the estimate including convexity '
                'across 17 shocks, so you can see where the straight-line estimate breaks down.'),
               ('Earnings and value',
                'The same rate moves run through NII by repricing bucket and through EVE under six shock shapes, '
                'so the earnings view and the economic value view sit in one workbook.'),
               ('A bootstrapped zero curve',
                'Zero rates are bootstrapped from 15 par yields, with forward rates derived from them.')],
     'faqs': [('What does it not do?',
               'Each bond is discounted at its own yield to maturity rather than off the zero curve. Key-rate '
               'durations are allocated in proportion to maturity proximity rather than by bumping each tenor, '
               'and price and EVE changes use the duration and convexity approximation rather than full '
               'repricing.'),
              ('How is it different from the IRRBB Model?',
               'The IRRBB Model implements the regulatory framework: 19 Basel buckets, the six prescribed '
               'shocks, deposit slotting and the outlier tests. This model measures duration, convexity and rate '
               'sensitivity for a bond portfolio and its funding.'),
              ('Can I use my own portfolio?',
               'Yes. The 20 positions, the par yield curve and the liability profile are all inputs on INPUTS.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 18 tabs &middot; 20 bonds &middot; 17 rate shocks &middot; 55 integrity '
             'checks &middot; no macros &middot; instant download',
     'related': [('IRRBB Model', '/irrbb-model-excel.html'),
                 ('Bond Pricing &amp; Yield Model', '/bond-pricing-yield-model-excel.html'),
                 ('Treasury / Interest Rate Swap Model', '/interest-rate-swap-model-excel.html'),
                 ('Deposit Pricing &amp; NII Model', '/deposit-pricing-nii-model-excel.html')]},
    {'id': 'fx-hedging',
     'slug': 'fx-hedging-model-excel',
     'title': 'FX Hedging Model in Excel: Forwards, Swaps and FX VaR',
     'h1': 'FX Hedging &amp; Currency Risk Model',
     'meta': 'FX hedging model in Excel. Six currency pairs over 60 months, 10 forwards and 5 cross-currency '
             'swaps, MTM, effectiveness tests, OCI reserve and FX VaR.',
     'keywords': 'fx hedging model excel, currency risk model excel, fx forward valuation excel, hedge '
                 'effectiveness test excel, fx var excel',
     'hero': "Manage a sterling company's exposure to six currencies over 60 months: net exposure by currency, "
             'forward curves, ten FX forwards and five cross-currency swaps marked to market, effectiveness '
             'testing, the P&amp;L and OCI impact, a hedge ratio recommendation and FX value at risk.',
     'problem': ['Foreign currency revenue and costs rarely net off neatly, and the hedge book built against '
                 "them drifts as exposures change. Treasury teams end up answering the board's questions (how "
                 'much is hedged, what it is worth today, whether it still qualifies, what risk is left) from '
                 'separate spreadsheets.',
                 'This model holds the exposure, the hedges and the answers in one place. Each forward and swap '
                 "is valued against its currency's forward curve every month, tested against the 80% to 125% "
                 'dollar-offset range, and its mark-to-market is split between P&amp;L and the OCI reserve.'],
     'who': 'Corporate treasury teams and group finance at companies with foreign currency revenue or costs. '
            'Finance directors who report hedge positions to the board or audit committee. Treasury analysts and '
            'students learning how a hedge programme is valued and tested.',
     'tabs': [('INPUTS',
               'Scenario selector, spot rates, monthly forward points and volatilities for six pairs, monthly '
               'revenue and cost exposures, hedge policy limits, interest rate differentials and VaR '
               'parameters.'),
              ('EXPOSURE',
               'Revenue, cost and net exposure by currency for 60 months, with translation exposure and the '
               'cumulative position.'),
              ('FORWARD_CURVES',
               'Outright forward rates built from spot plus cumulative forward points, with discount factors, '
               'for each pair.'),
              ('HEDGE_PORTFOLIO',
               'Ten FX forwards: notional, contracted and current forward rate, mark-to-market, settlement '
               'P&amp;L and hedge ratio contribution.'),
              ('SWAP_PORTFOLIO',
               'Five cross-currency swaps with quarterly leg payments, net settlement, NPV and principal '
               'exchange at maturity.'),
              ('EFFECTIVENESS',
               'Prospective and retrospective dollar-offset tests for all 15 instruments, with a pass rate.'),
              ('MTM_VALUATION',
               'Combined mark-to-market of forwards and swaps by month, split into realised and unrealised.'),
              ('PL_IMPACT',
               'Unhedged FX gains and losses, the effective portion to OCI, the ineffective portion to P&amp;L, '
               'and the OCI reserve roll-forward.'),
              ('HEDGE_STRATEGY',
               'For each currency, expected P&amp;L, volatility and cost of hedging at hedge ratios from 0% to '
               '100%, and the recommended ratio beside the policy minimum and maximum.'),
              ('VaR_FX',
               'Parametric VaR at 95% and 99% over a 10-day holding period by currency, undiversified and '
               "diversified totals, VaR after hedging and each currency's contribution."),
              ('DASHBOARD',
               'Key metrics and chart data for exposure, hedge ratios, MTM, P&amp;L, effectiveness and VaR.'),
              ('SENSITIVITY',
               'Four two-way tables: P&amp;L by spot shock and hedge ratio, VaR by volatility and exposure, '
               'hedging cost by forward points and tenor.'),
              ('CHECKS',
               '70 integrity checks, including forward equal to spot plus points for each pair and the OCI '
               'reserve roll-forward.')],
     'diffs': [('Exposure and hedges side by side',
                'Net exposure by currency and month sits next to the forwards and swaps placed against it, so '
                'the hedge ratio is measured against the real position.'),
               ('Forwards and cross-currency swaps',
                'Ten forwards and five swaps, each valued monthly over the 60-month horizon.'),
               ('Every instrument tested',
                'Prospective and retrospective dollar-offset tests against the 80% to 125% range, instrument by '
                'instrument, with a pass rate.'),
               ('OCI and P&amp;L separated',
                'Hedge MTM is split into the effective portion for the OCI reserve and the ineffective portion '
                'for P&amp;L, and the reserve rolls forward each month.'),
               ('A hedge ratio you can defend',
                'For each currency, volatility reduction against cost of hedging at five hedge ratios, with the '
                'ratio that gives the highest net benefit.')],
     'faqs': [('What does it not do?',
               'It does not model counterparty credit risk, margin requirements or basis risk. VaR is '
               'parametric, forwards are assumed to be physically settled and swaps net settled.'),
              ('Which currencies are covered?',
               'Sterling against USD, EUR, JPY, CHF, AUD and CNY. Spot rates, forward points, volatilities and '
               'exposures are all inputs, so you can replace the demo values with your own.'),
              ('What do the scenarios change?',
               'The market and exposure inputs carry Base, Upside, Downside and Stress values, switched from one '
               'selector on INPUTS.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo company, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 6 currency pairs &times; 60 months &middot; 15 hedge '
             'instruments &middot; 70 integrity checks &middot; no macros &middot; instant download',
     'related': [('Value at Risk (VaR) Model', '/var-model-excel.html'),
                 ('Treasury / Interest Rate Swap Model', '/interest-rate-swap-model-excel.html'),
                 ('Working Capital Optimisation Model', '/working-capital-model-excel.html')]},
    {'id': 'budget-variance',
     'slug': 'budget-vs-actual-variance-model-excel',
     'title': 'Budget vs Actual Variance Model in Excel',
     'h1': 'Budget vs Actual Variance Model',
     'meta': 'Budget vs actual variance model in Excel. 8 departments, 40 lines each, 12 months: variance in GBP '
             'and percent, YTD run-rate, prior year and EBITDA bridge.',
     'keywords': 'budget vs actual model excel, variance analysis excel, budget variance report template, '
                 'monthly variance analysis, ebitda bridge excel',
     'hero': 'Monthly budget against actual for eight departments and 40 revenue and cost lines each: variance '
             'in pounds and percent, a consolidated P&amp;L, year-to-date and run-rate views, prior-year '
             'comparison, trends and an EBITDA bridge from budget to actual.',
     'problem': ['Month-end variance reporting is mostly mechanics: line up budget and actual, work out which '
                 'way is favourable for revenue and for cost, total it by department and explain the bridge. '
                 'Done by hand each month, the sign conventions slip and the totals stop tying.',
                 'This model fixes the mechanics once. Enter actuals on one tab and every variance, in pounds '
                 'and percent, is signed so that positive always means favourable, rolled up by department and '
                 'group, and bridged from budget EBITDA to actual.'],
     'who': 'FP&amp;A teams and management accountants running monthly variance reporting. Department heads and '
            'finance business partners who need a line-by-line view. Finance students learning how a variance '
            'pack is built.',
     'tabs': [('INPUTS',
               'Fiscal year, the monthly budget and the prior-year figures for every line in every department.'),
              ('BUDGET', 'Approved budget by department and line, monthly, with year to date and full year.'),
              ('ACTUALS', 'Where actual results are entered, in the same layout as the budget.'),
              ('VARIANCE_ABS', 'Variance in pounds, signed so positive is favourable for both revenue and cost.'),
              ('VARIANCE_PCT', 'The same variances as a percentage of budget.'),
              ('PRIOR_YEAR', 'Actual against prior year for every line.'),
              ('CONSOLIDATED',
               'Group P&amp;L across all departments: budget, actual, variance and variance percent by month.'),
              ('YTD_ANALYSIS',
               'Year-to-date budget, actual and variance, full-year budget, a run-rate full-year projection and '
               'completion percentage.'),
              ('TREND',
               'Twelve-month trends by department with 3-month rolling averages and a seasonality index.'),
              ('WATERFALL',
               "EBITDA bridge from group budget to actual through each department's revenue and cost variance, "
               'and a department EBITDA comparison.'),
              ('DASHBOARD', 'Six charts.'),
              ('SENSITIVITY',
               'Group EBITDA under revenue and cost changes by department, and a two-way revenue by cost grid.'),
              ('CHECKS',
               '70 integrity checks, including department totals tying to the budget and EBITDA equal to revenue '
               'less costs in both budget and actuals.')],
     'diffs': [('One sign convention',
                'Positive always means favourable: revenue above budget or cost below it. No mental flipping '
                'between revenue and cost lines.'),
               ('Line-level detail, group-level answer',
                'Eight departments with 15 revenue and 25 cost lines each roll up to a consolidated P&amp;L and '
                'a group EBITDA.'),
               ('The bridge, built for you',
                "WATERFALL walks budget EBITDA to actual through each department's revenue and cost variance."),
               ('Year to date and full year',
                'YTD variance, full-year budget and a run-rate projection show where the year is heading, not '
                'just where the month landed.'),
               ('Prior year as well as budget', 'Every line is compared with last year as well as with plan.')],
     'faqs': [('What does it not do?',
               'Actuals are entered by hand on ACTUALS; there is no ledger import. It covers one fiscal year of '
               '12 months, and the run-rate projection annualises year-to-date actuals by the current calendar '
               'month, so it assumes a January to December year.'),
              ('Can I use it outside banking?',
               'Yes. The demo is a bank with departments such as Retail Banking and Treasury, but the structure '
               'is departments and line items. Rename them to match your own chart of accounts.'),
              ('How is it different from the Budget &amp; Forecast Model?',
               'That model builds the annual budget from revenue, cost, headcount and capex assumptions. This '
               'one takes a budget as given and tracks actual results against it every month.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo bank, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 8 departments &times; 40 lines &times; 12 months &middot; '
             '70 integrity checks &middot; no macros &middot; instant download',
     'related': [('Budget &amp; Forecast Model', '/budget-vs-forecast-model-excel.html'),
                 ('Management Accounts &amp; Monthly Reporting Pack', '/management-accounts-pack-excel.html'),
                 ('NIM Budget Tracking Model', '/nim-variance-model-excel.html')]},
    {'id': 'budget-forecast',
     'slug': 'budget-vs-forecast-model-excel',
     'title': 'Budget and Forecast Model in Excel: Annual Department Budget',
     'h1': 'Budget &amp; Forecast Model',
     'meta': 'Budget and forecast model in Excel. 10 departments over 12 months: revenue, costs, headcount, '
             'capex and depreciation, profit and loss and the cash budget.',
     'keywords': 'budget forecast model excel, annual budget template excel, departmental budget model, '
                 'headcount budget excel, cash budget template',
     'hero': 'Build a full-year budget for ten departments month by month: revenue across eight streams, '
             'operating costs across 20 categories, headcount with hires and leavers, capex and depreciation, '
             'then a consolidated P&amp;L, a monthly cash budget and a departmental comparison, under four '
             'scenarios from one selector.',
     'problem': ['Budget season means pulling revenue, cost, headcount and capex plans from every department '
                 'into one P&amp;L, then redoing it when the growth or inflation assumption moves. The '
                 'consolidation is where errors creep in: a department missing from a total, a quarter that does '
                 'not add to the year.',
                 'This model builds the budget from department assumptions and consolidates it automatically. '
                 'Revenue growth, cost and salary inflation, headcount and capex each carry Base, Upside, '
                 'Downside and Stress values, and one selector moves the whole budget between them.'],
     'who': 'FP&amp;A teams and budget owners preparing the annual budget. Finance directors who need the '
            'P&amp;L, cash and headcount plans to agree. Analysts and students learning how a departmental '
            'budget consolidates.',
     'tabs': [('INPUTS',
               'Scenario selector, growth, inflation, tax, bonus, benefits and working capital assumptions, '
               'annual revenue by department and stream, headcount and salary per head by department, and capex '
               'by category with useful lives.'),
              ('REVENUE_BUDGET', 'Monthly revenue by department and stream, with quarters and full year.'),
              ('COST_BUDGET', 'Monthly operating costs by department across 20 categories.'),
              ('HEADCOUNT',
               'Opening headcount, hires, leavers, closing and average headcount, salary, bonus and benefits by '
               'department.'),
              ('CAPEX_PLAN',
               'Monthly capex across six asset categories, straight-line depreciation by useful life, and net '
               'book value.'),
              ('PL_BUDGET',
               'Consolidated P&amp;L from revenue to net income, monthly with quarters and full year.'),
              ('CASH_BUDGET',
               'Operating cash flow with receivable and payable movements from days assumptions, capex, '
               'financing and the closing cash balance.'),
              ('DEPARTMENTAL',
               'P&amp;L by department to EBIT, contribution margin, revenue per FTE, and monthly revenue, cost '
               'and contribution by department.'),
              ('PHASING',
               "Each department's monthly revenue and cost as a share of the year, and cumulative phasing."),
              ('VARIANCE',
               'Budget against prior year by department and month. The prior-year rows are a placeholder set at '
               '95% of budget: replace them with your actuals.'),
              ('DASHBOARD',
               'Chart data for revenue by department, cost structure, cash flow, headcount, margins and capex.'),
              ('SENSITIVITY',
               'EBITDA by revenue growth and cost inflation, and people cost by headcount change and salary '
               'inflation.'),
              ('CHECKS',
               '47 integrity checks, including monthly P&amp;L revenue agreeing to the revenue budget, quarters '
               'summing to the year, and the headcount roll-forward by department.')],
     'diffs': [('Four scenarios, one selector',
                'Growth, inflation, headcount, salary, bonus and capex assumptions each carry Base, Upside, '
                'Downside and Stress values. Change the selector and every department, the P&amp;L and the cash '
                'budget move together.'),
               ('Headcount that rolls forward',
                'Opening headcount plus hires less leavers gives closing headcount every month, and people cost '
                'follows from salary per head, bonus and benefits.'),
               ('Capex with its depreciation',
                'Six asset categories, each depreciated straight-line over its own useful life, feeding D&amp;A '
                'in the P&amp;L and capex in the cash budget.'),
               ('Cash, not just profit',
                'Receivable and payable movements from days assumptions turn the P&amp;L into a monthly cash '
                'budget with a closing balance.'),
               ('Totals that are checked',
                'Every month of P&amp;L revenue is checked against the revenue budget, and quarters against the '
                'year.')],
     'faqs': [('What does it not do?',
               'It is a single-year monthly budget. Cost of goods sold is set at 30% of revenue, revenue and '
               'costs are spread evenly across the months, interest is charged on a fixed debt balance, and the '
               "prior-year comparison is a placeholder until you enter last year's figures."),
              ('Does it compare budget with forecast?',
               'It builds the budget and the forecast cash position behind it. To track actuals against the '
               'budget through the year, see the Budget vs Actual Variance Model; to keep an 18-month forward '
               'view, see the Rolling Forecast Model.'),
              ('Is it built for banks?',
               "The demo departments are a bank's, from Retail Banking to Human Resources, but the structure is "
               'generic: departments, revenue streams, cost categories, headcount and capex.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo bank, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 10 departments &times; 12 months &middot; 4 scenarios '
             '&middot; 47 integrity checks &middot; no macros &middot; instant download',
     'related': [('Budget vs Actual Variance Model', '/budget-vs-actual-variance-model-excel.html'),
                 ('Capital Expenditure Planning Model', '/capex-model-excel.html')]},
    {'id': 'management-accounts',
     'slug': 'management-accounts-pack-excel',
     'title': 'Management Accounts Pack in Excel: Monthly Reporting',
     'h1': 'Management Accounts &amp; Monthly Reporting Pack',
     'meta': 'Management accounts pack in Excel. Month and YTD results vs budget and prior year, six divisions, '
             'balance sheet, cash flow, 20 KPIs and an EBITDA bridge.',
     'keywords': 'management accounts template excel, monthly reporting pack excel, board pack template, kpi '
                 'scorecard excel, month end reporting template',
     'hero': 'A monthly reporting pack for a six-division group: P&amp;L for the month and year to date against '
             'budget and prior year, divisional drill-downs, balance sheet, cash flow, revenue analysis, a '
             '20-KPI scorecard with RAG status, an EBITDA bridge and a full-year forecast.',
     'problem': ['The monthly pack is the same job every month: pull actuals, line them up against budget and '
                 'last year, explain the bridge, refresh the KPIs and get it to the board on time. Rebuilding it '
                 'each month is where the errors and the late nights come from.',
                 'This model gives the pack a fixed structure. Set the reporting month once and every budget and '
                 'prior-year comparison picks up that month, year-to-date totals accumulate to it, and the '
                 'full-year forecast combines the actual months with the budget for the rest.'],
     'who': 'Financial controllers and management accountants producing the monthly pack. FP&amp;A teams '
            'reporting to ExCo and the board. Finance directors who want a consistent structure month after '
            'month.',
     'tabs': [('INPUTS',
               'Reporting year and month, general assumptions, monthly budget and prior year by division and '
               'line, the balance sheet budget, and KPI targets and RAG thresholds.'),
              ('PL_MONTH',
               'Consolidated P&amp;L for the month: actual, budget and prior year, with variances in pounds and '
               'percent.'),
              ('PL_YTD',
               'Year-to-date P&amp;L against budget and prior year, full-year budget and forecast, and a monthly '
               'trend for every revenue line by division.'),
              ('BALANCE_SHEET',
               'Balance sheet against budget and prior year, with a balance check, working capital and net '
               'debt.'),
              ('CASHFLOW',
               'Operating, investing and financing cash flows against budget and prior year, the cash bridge and '
               'monthly detail.'),
              ('DIVISIONAL',
               'P&amp;L for each of six divisions, actual against budget, with contribution by division and cost '
               'by line and division.'),
              ('REVENUE_ANALYSIS',
               'Revenue by product, customer segment and geography, volume and price decomposition, pipeline and '
               'a 12-month trend.'),
              ('KPI_SCORECARD',
               '20 financial, operational and strategic KPIs against target and prior year, with trend and RAG '
               'status.'),
              ('WATERFALL',
               'EBITDA bridge from budget to actual by revenue and cost line, for the month and year to date.'),
              ('FORECAST',
               'Each month flagged actual or forecast from the reporting month, with the full-year forecast '
               'against budget and divisional detail.'),
              ('DASHBOARD',
               'Chart data for the P&amp;L trend, divisional contribution, the EBITDA bridge, cash flow, key '
               'ratios and headcount.'),
              ('SENSITIVITY',
               'Full-year EBITDA by revenue growth and margin, net income by interest and tax rate, named stress '
               'cases, and divisional EBITDA sensitivity.'),
              ('CHECKS',
               '50 integrity checks, including the balance sheet balancing, the cash bridge closing, and the '
               'full-year forecast equal to actual plus remaining budget.')],
     'diffs': [('Set the month once',
                'The reporting month on INPUTS drives every budget and prior-year comparison, the YTD totals and '
                'the actual or forecast flag on each month.'),
               ('Six divisions to one group',
                'Divisional actuals roll up to the consolidated monthly P&amp;L, with contribution by division '
                'alongside.'),
               ('A KPI scorecard with RAG',
                'Twenty KPIs, from cost to income and ROE to CET1, LCR and NPS, each against target and prior '
                'year with green, amber or red status.'),
               ('Board-ready layout',
                'Every tab is set up for A4 landscape printing, so the pack prints as it reads on screen.'),
               ('Forecast from actuals',
                'The full-year forecast takes actual months to date and budget for the remainder, so the '
                'year-end view moves every month.')],
     'faqs': [('What does it not do?',
               'The full-year forecast is year-to-date actuals plus the remaining budget, not a driver-based '
               'reforecast. Balance sheet, cash flow, revenue analysis, KPI actuals and the EBITDA bridge are '
               'entered on their own tabs rather than derived from the P&amp;L, and the pack reports one month '
               'at a time.'),
              ('Is it set up for a bank?',
               'The demo is a financial services group with six divisions, from Retail Banking to Digital '
               'Services, and banking KPIs such as NIM, CET1 and LCR. The P&amp;L structure of revenue, direct '
               'costs and operating expenses works for other businesses if you relabel the lines.'),
              ('How is it different from the Budget vs Actual Variance Model?',
               'That model goes line by line through 40 revenue and cost lines in eight departments for the '
               'whole year. This one is the monthly pack: P&amp;L, balance sheet, cash flow, KPIs and the bridge '
               'for one reporting month.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo bank, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 6 divisions &middot; 20 KPIs &middot; 50 integrity checks '
             '&middot; no macros &middot; instant download',
     'related': [('Budget vs Actual Variance Model', '/budget-vs-actual-variance-model-excel.html'),
                 ('3-Statement Integrated Model', '/three-statement-model-excel.html')]},
    {'id': 'working-capital',
     'slug': 'working-capital-model-excel',
     'title': 'Working Capital Model in Excel: DSO, DIO, DPO and Cash',
     'h1': 'Working Capital Optimisation Model',
     'meta': 'Working capital model in Excel. 5 segments over 60 months: DSO, DIO, DPO, cash conversion cycle, '
             'aging, seasonal swings, financing options, cash release.',
     'keywords': 'working capital model excel, cash conversion cycle excel, dso dio dpo calculator, receivables '
                 'aging excel, working capital optimisation',
     'hero': 'Project and improve working capital for five business segments over 60 months: receivables with '
             'aging and bad debt, inventory by stage, payables, the cash conversion cycle, seasonal financing '
             'need, three financing options and the cash released by shorter collection or longer payment terms.',
     'problem': ['Working capital is where profitable businesses run short of cash. Receivables stretch, '
                 'inventory builds ahead of the season, and finance is asked how much cash a ten-day improvement '
                 'in collections would free up, and whether factoring would cost less than the overdraft.',
                 'This model answers both. It builds receivables, inventory and payables from days assumptions '
                 'for each segment, prices each improvement in cash released and interest saved, and compares '
                 'the overdraft, factoring and supply chain finance on cost.'],
     'who': 'CFOs, treasurers and FP&amp;A teams at companies carrying receivables and inventory. Working '
            "capital and transformation consultants. Lenders and analysts assessing a borrower's cash cycle. "
            'Students learning the cash conversion cycle.',
     'tabs': [('INPUTS',
               'Scenario selector and multipliers, base rate, tax and WACC, and for each of five segments: '
               'revenue, growth, COGS and purchases ratios, target DSO, DIO and DPO, provision rates, an aging '
               'profile and monthly seasonal factors.'),
              ('RECEIVABLES',
               'Gross and net receivables, bad debt provision, five aging buckets, DSO, collection efficiency '
               'and overdue share by segment.'),
              ('INVENTORY',
               'Raw materials, work in progress and finished goods, obsolescence provision, DIO, turnover and '
               'carrying cost by segment.'),
              ('PAYABLES',
               'Trade payables, accruals and other payables, DPO, early payment discount and payables aging by '
               'segment.'),
              ('NWC_SUMMARY',
               'Net working capital, change in NWC, NWC days and financing need by segment and consolidated.'),
              ('CASH_CONVERSION',
               'DSO, DIO, DPO, cash conversion cycle, cash tied up and its financing cost by segment and '
               'blended.'),
              ('SEASONAL',
               'Seasonal revenue and NWC by month, peak and trough flags, and the seasonal financing need or '
               'surplus.'),
              ('FINANCING',
               'Overdraft, receivables factoring and supply chain finance compared on monthly cost.'),
              ('OPTIMISATION',
               'Cash release, new NWC and interest saving for 5, 10 and 15-day improvements in DSO, DIO and DPO, '
               'and a combined case.'),
              ('AGING_DETAIL',
               'Receivables aging and expected loss by customer tier, payables by supplier category, and '
               'concentration measures including a Herfindahl index.'),
              ('DASHBOARD', 'KPIs and six charts.'),
              ('SENSITIVITY',
               'NWC days by DSO and DPO change, cash impact by revenue growth and NWC days, and CCC by DSO and '
               'DIO change.'),
              ('CHECKS',
               '64 integrity checks, including NWC equal to receivables plus inventory less payables, and CCC '
               'equal to DSO plus DIO less DPO, for every segment.')],
     'diffs': [('Days turned into cash',
                'Every improvement is priced: a 5, 10 or 15-day change in DSO, DIO or DPO shows the cash '
                'released, the new NWC and the interest saved.'),
               ('Five segments, one consolidated view',
                'Manufacturing, retail, technology, services and healthcare segments, each with its own drivers, '
                'roll up to blended DSO, DIO, DPO and CCC.'),
               ('Seasonality made visible',
                'Monthly seasonal factors drive revenue, so the model flags the peak and trough working capital '
                'months and the financing the peak needs.'),
               ('Financing options compared',
                'Overdraft, factoring and supply chain finance costed side by side against the same financing '
                'need.'),
               ('Aging and concentration',
                'Five aging buckets with loss rates that rise with age, customer tiers, supplier categories and '
                'a Herfindahl concentration index.')],
     'faqs': [('What does it not do?',
               'Inventory is split 40% raw materials, 25% work in progress and 35% finished goods, accruals and '
               'other payables are set as shares of COGS, and factoring and supply chain finance use fixed '
               'eligibility and advance rates. Days are calculated on a 30-day month, and interest saving is '
               'cash released times the base rate.'),
              ('What do the scenarios change?',
               'Base, Upside, Downside and Stress adjust revenue, costs, DSO and DPO together. In the demo, '
               'Stress takes revenue down 30%, costs up 15%, DSO out 10 days and DPO in 10 days.'),
              ('Which currency is it in?',
               'The demo is in US dollars. All values are inputs, so any currency works if you are consistent.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo company, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 5 segments &times; 60 months &middot; 64 integrity checks '
             '&middot; no macros &middot; instant download',
     'related': [('3-Statement Integrated Model', '/three-statement-model-excel.html'),
                 ('Debt Schedule Model', '/debt-schedule-model-excel.html'),
                 ('FX Hedging &amp; Currency Risk Model', '/fx-hedging-model-excel.html'),
                 ('DCF Model', '/dcf-model-excel.html')]},
    {'id': 'capex',
     'slug': 'capex-model-excel',
     'title': 'Capex Model in Excel: Project Portfolio, NPV and Tracking',
     'h1': 'Capital Expenditure Planning Model',
     'meta': 'Capex model in Excel. 20 projects over 60 months: spend profile, budget vs actual with CPI, '
             'depreciation, NPV and payback, funding gap and approvals.',
     'keywords': 'capex model excel, capital expenditure planning template, capex tracking excel, project npv '
                 'payback excel, capex budget template',
     'hero': 'Plan, approve and track a portfolio of 20 capital projects over 60 months: monthly planned and '
             'actual spend, budget tracking with cost performance, straight-line depreciation, NPV and payback '
             'by project, a funding gap analysis, an approval tracker and a post-completion review.',
     'problem': ['A capital programme is approved project by project and then reported as a portfolio, and the '
                 'two views rarely agree. By the second year nobody can say which projects are over budget, when '
                 'depreciation will hit the P&amp;L, or whether the programme is still funded.',
                 "This model holds both views in one place. Each project's budget, start month, duration, useful "
                 'life and benefit rate drive its spend, its depreciation and its return, and the portfolio, '
                 'funding and dashboard tabs add them up.'],
     'who': 'Finance and capital planning teams. PMO and change teams reporting on a capital programme. CFOs and '
            'investment committees approving projects. FP&amp;A analysts forecasting depreciation.',
     'tabs': [('INPUTS',
               'Scenario selector, start date, tax rate, WACC, inflation, contingency and funding assumptions, '
               'and for each of 20 projects: category, budget, start month, duration, useful life, annual '
               'benefit rate and hurdle rate, each with Base, Upside, Downside and Stress values.'),
              ('PROJECT_REGISTER',
               'All 20 projects with sponsor, category, status, budget, actual to date, completion and RAG.'),
              ('SPEND_PROFILE',
               'Monthly planned and actual spend by project, cumulative and percent complete, and portfolio '
               'totals.'),
              ('BUDGET_TRACKING',
               'Original and revised budget, committed, actual, remaining, estimate at completion and CPI by '
               'project and month.'),
              ('DEPRECIATION',
               'Capitalised amount, monthly straight-line depreciation, accumulated depreciation and net book '
               'value by project, starting after completion.'),
              ('PROJECT_RETURNS',
               'Investment, annual benefit and operating cost, NPV at the WACC, an IRR proxy, payback and '
               'profitability index, with five-year cash flows by project.'),
              ('PORTFOLIO', 'Capex by category, year and status, and the growth against maintenance split.'),
              ('FUNDING',
               'Internal cash, debt, equity and disposals against the capex programme and interest, with the '
               'annual and cumulative funding position.'),
              ('APPROVAL',
               "Approval tracker: each project's IRR proxy against the WACC and payback against five years, "
               'giving approve, review or reject.'),
              ('POST_COMPLETION',
               'Budget against actual cost and expected against actual benefit for each project, with expected '
               'and actual ROI.'),
              ('DASHBOARD',
               'KPIs and chart data for spend by category and year, project returns against hurdle, and '
               'cumulative spend.'),
              ('SENSITIVITY',
               'Portfolio NPV by cost overrun and benefit shortfall, and grids on hurdle rate and budget.'),
              ('CHECKS',
               "72 integrity checks, including portfolio totals equal to the sum of projects and each project's "
               'variance equal to budget less actual.')],
     'diffs': [('Project to portfolio',
                'Twenty projects, each with its own budget, timing, useful life and benefit rate, roll up to '
                'portfolio views by category, year and status.'),
               ('Depreciation that follows delivery',
                'Each project is capitalised when it completes and depreciated straight-line over its useful '
                'life, so the depreciation profile follows the delivery plan.'),
               ('Budget tracking with CPI',
                'Original and revised budget, commitments, actuals, estimate at completion and a cost '
                'performance index for every project.'),
               ('A funding check',
                'Sources of funding against the capex programme and interest each year, with the cumulative '
                'surplus or gap.'),
               ('From approval to review',
                'An approval rule on the IRR proxy and payback, and a post-completion review of cost and benefit '
                'against the business case.')],
     'faqs': [('What does it not do?',
               "Planned spend is spread evenly over each project's duration. Depreciation is straight-line with "
               'no residual value. The IRR column is a proxy (annual net benefit over investment), payback is '
               'simple, internal cash generation is constant each year, and interest is charged on the full debt '
               'facility, which is conservative.'),
              ('Where do I enter actual spend?',
               'On SPEND_PROFILE, one actual row per project per month. Budget tracking, CPI, the register and '
               'the dashboard update from there.'),
              ('What do the scenarios change?',
               'Every project assumption and the global rates carry Base, Upside, Downside and Stress values, '
               'switched from one selector. The SENSITIVITY tables run independently of the selector.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo bank, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 20 projects &times; 60 months &middot; 72 integrity checks '
             '&middot; no macros &middot; instant download',
     'related': [('IAS 16 PP&amp;E Model', '/ias-16-ppe-model-excel.html'),
                 ('IAS 38 Capitalisation Model', '/ias-38-capitalisation-model-excel.html'),
                 ('Budget &amp; Forecast Model', '/budget-vs-forecast-model-excel.html'),
                 ('DCF Model', '/dcf-model-excel.html')]},
    {'id': 'capitalisation',
     'slug': 'ias-38-capitalisation-model-excel',
     'title': 'IAS 38 Capitalisation Model in Excel: Intangible Assets',
     'h1': 'Capitalisation &amp; Intangible Assets Model (IAS 38)',
     'meta': 'IAS 38 capitalisation model in Excel. Six-criteria test for 40 projects, 120-asset register in 8 '
             'categories, monthly amortisation, R&D split, disclosure.',
     'keywords': 'ias 38 model excel, intangible assets model excel, capitalisation model excel, development '
                 'cost capitalisation, intangible asset amortisation schedule',
     'hero': 'Test development spend against the six IAS 38 criteria, carry 120 intangible assets across eight '
             'categories, and roll cost, amortisation, impairment and net book value forward month by month for '
             'five years, ending in the year-by-year reconciliation for the accounts.',
     'problem': ['Whether development spend can be capitalised is a judgement auditors challenge every year, and '
                 'the evidence for it often sits in emails and a spreadsheet that one person understands.',
                 'This model puts the assessment on one tab: each project is scored Yes or No against the six '
                 'criteria, from technical feasibility to reliable measurement, and passes when all six are met. '
                 'Research spend is expensed, development spend is split between capitalised and expensed at a '
                 'rate you set, and the schedules roll cost, amortisation and impairment forward to a closing '
                 'net book value.'],
     'who': 'Technical accounting teams and financial controllers at companies with material software, '
            'development or acquired intangibles. Finance teams preparing the intangible assets note for audit. '
            "Auditors and advisers who want a transparent benchmark for a client's capitalisation policy.",
     'tabs': [('INPUTS',
               'Start date, 60-month horizon, impairment discount rate, tax rate and capitalisation threshold; '
               'then useful life, method, residual value, additions, disposals and impairment trigger for each '
               'of eight categories; plus R&amp;D spend, research share and the development capitalisation rate. '
               'Base, Upside, Downside and Stress scenarios.'),
              ('CAPITALISATION_TEST',
               '40 projects scored against the six IAS 38 criteria: technical feasibility, intention to '
               'complete, ability to use or sell, probable future economic benefits, adequate resources and '
               'reliable measurement. PASS needs all six.'),
              ('ASSET_REGISTER',
               '120 assets, 15 in each category, with cost, useful life, method, accumulated amortisation, net '
               'book value and status: active, near end or fully amortised.'),
              ('COST_ROLL',
               'Monthly gross cost by category: opening, additions, reclassifications, disposals and closing.'),
              ('AMORTISATION',
               'Monthly charge by category on cost less residual value over useful life, with amortisation '
               'released on disposals. Goodwill is not amortised.'),
              ('NBV_SCHEDULE',
               'Gross cost less accumulated amortisation and accumulated impairment, by category and month, with '
               'NBV as a percentage of cost.'),
              ('RD_ANALYSIS',
               'Total R&amp;D spend split into research (expensed), development capitalised and development '
               'expensed, with the capitalisation rate and cumulative totals.'),
              ('IMPAIRMENT',
               'Annual test by category: carrying amount against recoverable amount, the higher of fair value '
               'less costs to sell and value in use.'),
              ('PL_IMPACT',
               'Amortisation, impairment and R&amp;D expense through to EBIT, monthly and as an annual summary.'),
              ('DISCLOSURE',
               'Reconciliation of opening to closing NBV by category for each of the five years, plus a table of '
               'methods, useful lives, residual values and rates.'),
              ('DASHBOARD',
               'KPIs and chart data: NBV by category, amortisation trend, R&amp;D capitalisation, asset age '
               'profile and an NBV waterfall.'),
              ('SENSITIVITY',
               'Useful life moved by up to three years either way, the R&amp;D capitalisation rate flexed, and a '
               'two-way grid of useful life against impairment trigger.'),
              ('CHECKS',
               "53 integrity checks, including that goodwill amortisation is zero and that each category's NBV "
               'equals cost less amortisation and impairment.')],
     'diffs': [('The six criteria, documented',
                'Each project is assessed criterion by criterion, so the file shows why an item was capitalised, '
                'not just that it was.'),
               ('Research and development separated',
                'Research spend goes to the P&amp;L. Development spend is split between capitalised and expensed '
                'at a rate you set, and the split is visible every month.'),
               ('Goodwill treated as goodwill',
                'An indefinite life, no amortisation, an annual impairment test, and a check on CHECKS that its '
                'amortisation stays at zero.'),
               ('The note, already reconciled',
                'DISCLOSURE reconciles opening to closing NBV for each year and category: additions, disposals, '
                'amortisation, impairment and reversals.'),
               ('Sensitivity on the judgement calls',
                'Useful lives and the capitalisation rate are the assumptions auditors challenge. SENSITIVITY '
                'shows what moving each one does to the charge.')],
     'faqs': [('Which categories does it cover?',
               'Eight: software, patents, trademarks, licences, customer relationships, brand, R&amp;D projects '
               'and goodwill. Each has its own useful life, residual value, additions, disposals and impairment '
               'trigger.'),
              ('Is it monthly?',
               'Yes. 60 monthly periods from the start date on INPUTS, with annual totals for the disclosure '
               'note and the dashboard.'),
              ('What does it not do?',
               'The category schedules amortise on a straight line; declining balance is available per asset on '
               'the register. Impairment here is a simplified annual test driven by a trigger percentage per '
               'category, not a cash-flow forecast. For a full CGU test with value in use, see the IAS 36 '
               'Impairment Model.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo company, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 8 categories &middot; 120 assets &times; 60 months '
             '&middot; 53 integrity checks &middot; no macros &middot; instant download',
     'related': [('IAS 36 Impairment Model', '/ias-36-impairment-model-excel.html'),
                 ('IAS 16 PP&amp;E Model', '/ias-16-ppe-model-excel.html'),
                 ('Capex Model', '/capex-model-excel.html')]},
    {'id': 'ppe',
     'slug': 'ias-16-ppe-model-excel',
     'title': 'IAS 16 PPE Model in Excel: Fixed Asset Roll-Forward',
     'h1': 'PP&amp;E / Fixed Assets Model (IAS 16)',
     'meta': 'IAS 16 PP&E model in Excel. 120-asset register in 6 classes, 60-month cost and depreciation '
             'roll-forward, disposals, revaluation, capex plan, disclosure.',
     'keywords': 'ias 16 model excel, fixed asset register excel, ppe roll forward excel, depreciation schedule '
                 'excel, fixed asset model',
     'hero': 'A fixed asset register of 120 assets across six classes, with gross cost, accumulated depreciation '
             'and net book value rolled forward month by month for five years. Disposals with their gain or '
             'loss, a revaluation schedule, a five-year capex plan and the carrying amount reconciliation for '
             'the accounts.',
     'problem': ['The fixed asset note is often built once a year from a register in one place and a '
                 'depreciation run in another. When the auditor asks why closing NBV does not equal opening plus '
                 'movements, the answer takes days.',
                 'This model keeps cost, depreciation, impairment and disposals in one monthly roll-forward per '
                 'class, and DISCLOSURE checks that closing equals opening plus movements for every class, every '
                 'year.'],
     'who': 'Financial controllers and fixed asset accountants. Finance teams preparing the PP&amp;E note or a '
            'capex budget. FP&amp;A teams who need depreciation and capex for a plan.',
     'tabs': [('INPUTS',
               'Start date, 60-month horizon, tax and inflation rates; then for each of six classes: useful '
               'life, method, residual value, annual capex budget, disposal rate, revaluation frequency and '
               'adjustment, and annual impairment rate. Disposal proceeds as a percentage of NBV. Base, Upside, '
               'Downside and Stress scenarios.'),
              ('ASSET_REGISTER',
               '120 assets, 20 in each class, with acquisition date, cost, life, method, residual value, '
               'accumulated depreciation, NBV, location and status.'),
              ('COST_ROLL',
               'Monthly gross cost by class: opening, additions, reclassifications, disposals at cost, '
               'write-offs and closing, plus capital commitments.'),
              ('DEPRECIATION',
               'Monthly charge by class on cost less residual value over useful life, depreciation released on '
               'disposals, and impairment. Land is not depreciated.'),
              ('NBV_SCHEDULE',
               'Gross cost, accumulated depreciation, cumulative impairment and NBV by class, with NBV as a '
               'share of cost, average age and remaining useful life.'),
              ('REVALUATION',
               'Revaluation adjustment by class on year-end NBV, the surplus to reserve, and an annual '
               'revaluation schedule.'),
              ('DISPOSALS',
               'Cost and depreciation disposed, NBV at disposal, proceeds, gain or loss, and tax on the gain or '
               'loss, by class and month.'),
              ('CAPEX_PLAN',
               'Five-year capex by class, split into maintenance and growth, set against depreciation, and '
               'committed against uncommitted.'),
              ('PL_IMPACT',
               'Depreciation, impairment and disposal gains and losses by class, monthly: the EBITDA to EBIT '
               'bridge.'),
              ('DISCLOSURE',
               'Carrying amount reconciliation by class for each year, depreciation methods and useful lives, '
               'and capital commitments contracted and authorised.'),
              ('DASHBOARD',
               'NBV by class, depreciation trend, capex against depreciation, asset age, disposal gains and '
               'losses, and an NBV waterfall.'),
              ('SENSITIVITY',
               'Useful life moved by up to three years either way, residual value flexed, and a two-way grid of '
               'life against residual value.'),
              ('CHECKS',
               '53 integrity checks, including NBV equal to cost less depreciation, and depreciation and '
               'disposal results tying to the P&amp;L, for every class.')],
     'diffs': [('One roll-forward, every class',
                'Cost, accumulated depreciation and NBV move month by month for land, buildings, plant and '
                'machinery, vehicles, fixtures and fittings, and IT equipment.'),
               ('Disposals with the gain or loss',
                'Proceeds are set as a percentage of NBV, so each disposal produces a gain or loss and the tax '
                'on it, and both flow to PL_IMPACT.'),
               ('Capex against depreciation',
                'The capex plan splits spend into maintenance and growth and sets it against the depreciation '
                'charge, so you can see whether the asset base is being replaced.'),
               ('The note reconciles itself',
                'DISCLOSURE builds the carrying amount reconciliation for each year and checks that closing '
                'equals opening plus movements.'),
               ('Scenarios on the judgement calls',
                'Useful lives, residual values, capex budgets and impairment rates all move with the scenario '
                'selector.')],
     'faqs': [('Which asset classes does it cover?',
               'Six: land, buildings, plant and machinery, vehicles, fixtures and fittings, and IT equipment, '
               'with 20 assets in each on the register. Land is not depreciated.'),
              ('Is it monthly?',
               'Yes. 60 monthly periods, with annual totals on CAPEX_PLAN, DISCLOSURE and DASHBOARD.'),
              ('What does it not do?',
               'The monthly class schedules depreciate on a straight line. Revaluation is calculated on '
               'REVALUATION and shown as a memo line in the reconciliation, applied after the period close; it '
               'does not feed back into the depreciation charge. Impairment is an annual rate per class, not a '
               'recoverable amount test: for that, see the IAS 36 Impairment Model.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo company, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 6 asset classes &middot; 120 assets &times; 60 months '
             '&middot; 53 integrity checks &middot; no macros &middot; instant download',
     'related': [('Capex Model', '/capex-model-excel.html'),
                 ('IAS 38 Capitalisation Model', '/ias-38-capitalisation-model-excel.html'),
                 ('IAS 36 Impairment Model', '/ias-36-impairment-model-excel.html')]},
    {'id': 'impairment',
     'slug': 'ias-36-impairment-model-excel',
     'title': 'IAS 36 Impairment Model in Excel: CGU Goodwill Testing',
     'h1': 'Impairment Testing Model (IAS 36)',
     'meta': 'IAS 36 impairment model in Excel. 8 CGUs, 10-year value in use DCF, fair value less costs to sell, '
             'goodwill-first loss allocation, headroom and breakevens.',
     'keywords': 'ias 36 impairment model excel, goodwill impairment test excel, value in use calculation, cgu '
                 'impairment model, impairment headroom analysis',
     'hero': 'Test goodwill and other assets across eight cash-generating units: indicator assessment, a '
             'ten-year value in use DCF with a WACC build-up, fair value less costs to sell, the recoverable '
             'amount, the loss allocated goodwill first, and the headroom and sensitivity the disclosure needs.',
     'problem': ['The annual goodwill test is often a DCF someone built years ago, with a discount rate nobody '
                 'can rebuild and a sensitivity note written by hand. Auditors ask how far the WACC or the '
                 'growth rate has to move before headroom disappears, and the model does not say.',
                 'This model calculates value in use and fair value less costs to sell for each CGU, takes the '
                 'higher as recoverable amount, and shows the headroom with breakeven WACC, terminal growth and '
                 'EBITDA margin beside it.'],
     'who': 'Technical accounting and group reporting teams running the annual goodwill test. Financial '
            'controllers at groups with acquired businesses. Valuation advisers and auditors who need a '
            "transparent benchmark for a client's test.",
     'tabs': [('INPUTS',
               'Reporting date, tax rate, risk-free rate, equity and debt risk premiums, long-term growth and '
               'cost to sell; then for each CGU the carrying amounts of goodwill, intangibles, PP&amp;E and '
               'other assets, revenue, growth, margins, capex, working capital, beta, gearing, size and country '
               'premiums, and trading and transaction multiples. Base, Upside, Downside and Stress scenarios.'),
              ('INDICATOR_ASSESSMENT',
               'Sixteen external and internal indicators per CGU, from a fall in market value to operating '
               'losses, with a summary of whether a test is required.'),
              ('GOODWILL_ALLOCATION',
               'Goodwill by CGU, months since the last test, carrying amounts by asset type and a five-year '
               'goodwill movement schedule.'),
              ('VIU_DCF',
               'Ten-year free cash flow per CGU from revenue and margin, discounted at a WACC built from CAPM '
               'and the cost of debt, with a Gordon growth terminal value.'),
              ('FVLCTS',
               'Fair value from a trading multiple and a transaction multiple, weighted 60/40, less costs to '
               'sell, with sensitivity to the multiple.'),
              ('RECOVERABLE_AMOUNT',
               'The higher of VIU and FVLCTS, which one it was, headroom or impairment, and the loss amount.'),
              ('IMPAIRMENT_CALC',
               'The loss allocated to goodwill first, then pro rata across intangibles, PP&amp;E and other '
               'assets, with post-impairment carrying amounts.'),
              ('REVERSAL_TRACKING',
               'Monthly monitoring of reversal indicators per CGU, capped at the carrying amount there would '
               'have been without the impairment, with goodwill reversal blocked.'),
              ('SENSITIVITY',
               'Headroom against WACC, terminal growth and EBITDA margin for each CGU, and a two-way grid of '
               'WACC against growth.'),
              ('HEADROOM',
               'Headroom, breakeven WACC, growth and margin with the cushion on each, a risk rating, and a '
               'five-year carrying amount projection.'),
              ('DISCLOSURE',
               'Key assumptions and sensitivity items under IAS 36.134, impairment losses under IAS 36.130, and '
               'the IAS 36.135 items, by CGU.'),
              ('DASHBOARD',
               'Carrying against recoverable amount, headroom by CGU, goodwill allocation, VIU composition and '
               'breakeven WACC against actual.'),
              ('MONTHLY_TRACKING', 'Monthly P&amp;L and free cash flow by CGU, with revenue against budget.'),
              ('SCENARIO_COMPARISON',
               'Key assumptions, WACC and an estimated VIU and headroom under all four scenarios side by side.'),
              ('EXTENDED_SENS',
               'A supplementary grid flexing reference values by a row shock and a column factor.'),
              ('CHECKS',
               '54 integrity checks, including recoverable amount equal to the higher of VIU and FVLCTS, and '
               'post-impairment carrying amounts reconciling for every CGU.')],
     'diffs': [('Both measures of recoverable amount',
                'Value in use from a ten-year DCF and fair value less costs to sell from market multiples, '
                'calculated side by side for every CGU, with the basis shown.'),
               ('A WACC you can rebuild',
                'Cost of equity from the risk-free rate, beta, equity risk premium, size premium and country '
                'risk premium; cost of debt from the risk-free rate plus a credit spread; weighted by your '
                'gearing.'),
               ('Allocation in the right order',
                'A loss reduces goodwill first, then the other assets pro rata to their carrying amounts, with a '
                'check that post-impairment amounts reconcile.'),
               ('Headroom with breakevens',
                'For each CGU: how far WACC can rise, or terminal growth and EBITDA margin fall, before headroom '
                'reaches zero, with a LOW, MEDIUM or HIGH risk rating.'),
               ('The disclosure items laid out',
                'Key assumptions, headroom and the change in each assumption that would eliminate it, set out by '
                'CGU under the IAS 36.134 headings.')],
     'faqs': [('How many CGUs can it test?',
               'Eight. The demo uses banking segments, from retail and corporate banking to insurance and an '
               'international unit. Names and every assumption are inputs.'),
              ('Does it handle reversals?',
               'Yes, for assets other than goodwill. REVERSAL_TRACKING tests whether recoverable amount exceeds '
               'carrying amount and caps the reversal at the carrying amount there would have been without the '
               'impairment. Goodwill reversals are blocked.'),
              ('What does it not do?',
               'Value in use is discounted at a post-tax WACC used as a proxy for the pre-tax rate, and the '
               'projection runs ten years where IAS 36 expects five unless a longer period can be justified. '
               'Breakeven WACC, growth and margin on HEADROOM are closed-form approximations, not goal-seek '
               'results. Fair value is based on multiples.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo company, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 20 tabs &middot; 8 CGUs &middot; 10-year DCF &middot; 54 integrity checks '
             '&middot; no macros &middot; instant download',
     'related': [('IAS 38 Capitalisation Model', '/ias-38-capitalisation-model-excel.html'),
                 ('DCF Model', '/dcf-model-excel.html'),
                 ('Blog: WACC calculation in banking', '/blog/wacc-calculation-banking.html')]},
    {'id': 'debt-schedule',
     'slug': 'debt-schedule-model-excel',
     'title': 'Debt Schedule Model in Excel: 8 Facilities and Covenants',
     'h1': 'Debt Schedule &amp; Facility Management Model',
     'meta': 'Debt schedule model in Excel. 8 facilities over 60 months, fixed and floating interest, fees, five '
             'covenants with headroom, maturity ladder, refinancing.',
     'keywords': 'debt schedule model excel, debt schedule template, covenant compliance model excel, revolving '
                 'credit facility model, multi facility debt model',
     'hero': 'Eight facilities, from a term loan and revolver to mezzanine, subordinated notes, leases and a '
             'shareholder loan, each on its own monthly schedule for five years. Consolidated into net debt and '
             'the weighted average cost of debt, with five covenants tested every month.',
     'problem': ["A borrower's debt rarely sits in one instrument. Term loans amortise, the revolver is drawn "
                 'and repaid, the bond is fixed and the mezzanine is not, and the covenant certificate needs all '
                 'of it on one LTM basis every quarter.',
                 "This model gives every facility its own schedule, with interest on the prior month's closing "
                 'balance so there is no circularity, then consolidates them and tests leverage, interest cover, '
                 'DSCR, minimum liquidity and gearing against their limits each month.'],
     'who': 'Treasury and corporate finance teams managing a multi-facility capital structure. Finance directors '
            'preparing covenant compliance. Leveraged finance and private credit analysts monitoring a borrower.',
     'tabs': [('INPUTS',
               'EBITDA and growth, opening cash, tax, a five-year base rate path, capex, working capital and '
               'covenant limits; for each facility: commitment, drawn amount, fixed or floating, spread or fixed '
               'rate, amortising or bullet, maturity, commitment and arrangement fees, prepayments and '
               'drawdowns. Base, Upside, Downside and Stress scenarios.'),
              ('FACILITY_1 to FACILITY_8',
               'One monthly schedule per facility: drawdowns, scheduled repayment, voluntary prepayment, '
               'interest, commitment and arrangement fees, all-in cost, utilisation and effective rate.'),
              ('CONSOLIDATED',
               'All eight facilities combined: balances, interest, fees, debt service, net debt, weighted '
               'average cost of debt, weighted average maturity and utilisation.'),
              ('COVENANTS',
               'Leverage, interest cover, DSCR, minimum liquidity and gearing each month on an LTM basis, with '
               'headroom and a status for each.'),
              ('MATURITY_PROFILE',
               'Maturity ladder by facility, 12 and 24-month refinancing need, refinancing capacity and '
               'coverage, concentration and the maturity wall year.'),
              ('INTEREST_ANALYSIS',
               'Fixed against floating interest, effective rates, and the annual impact of base rate moves from '
               '-100 to +200 bps.'),
              ('REFINANCING',
               'Extend, reprice or replace the term loan and the revolver, with break costs, fees and the NPV '
               'saving of each option.'),
              ('DASHBOARD',
               'Headline KPIs and chart data for balances by facility and quarterly interest and fees.'),
              ('SENSITIVITY',
               'Interest cover by base rate and EBITDA, total interest by prepayment size and timing, and '
               'leverage by EBITDA growth and repayment rate.'),
              ('CHECKS',
               '100 integrity checks, including closing balance within commitment, no negative balances and the '
               'roll-forward on every facility.')],
     'diffs': [('Eight instruments, one structure',
                'Senior term loan, revolver, secured bond, bilateral loan, mezzanine, subordinated notes, lease '
                'obligations and shareholder loan, each with its own rate basis, profile and fees.'),
               ('No circularity',
                "Interest runs on the prior month's closing balance, so the model needs no iterative "
                'calculation.'),
               ('Five covenants, every month',
                'Leverage, interest cover, DSCR, liquidity and gearing are tested on rolling 12-month figures, '
                'with headroom shown against each limit.'),
               ('All-in cost, not just coupon',
                "Commitment and arrangement fees sit beside interest, so each facility's effective rate and the "
                'weighted average cost of debt include them.'),
               ('Refinancing with numbers',
                'Three options for the term loan and the revolver, compared on total cost and NPV, before the '
                'maturity wall arrives.')],
     'faqs': [('Which repayment profiles does it support?',
               'Amortising, with equal quarterly principal repayments over the term, and bullet. Sculpted '
               'repayment is not implemented in this version.'),
              ('Can I change the facility mix?',
               "Yes. Each facility's commitment, rate basis, spread, profile, maturity and fees are inputs, so "
               'the eight slots can carry your own instruments.'),
              ('What does it not do?',
               'Day count is approximated as monthly twelfths for fixed and floating facilities. EBITDA grows at '
               'a constant rate, capex and working capital are held constant, and the cash flow is simplified. '
               'Refinancing options cover the term loan and the revolver.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo company, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 21 tabs &middot; 8 facilities &times; 60 months &middot; 5 covenants '
             '&middot; 100 integrity checks &middot; no macros &middot; instant download',
     'related': [('Debt Amortisation Model', '/debt-amortisation-model-excel.html'),
                 ('LBO Model', '/lbo-model-excel.html'),
                 ('Blog: Debt sizing in an LBO model', '/blog/lbo-model-debt-sizing.html')]},
    {'id': 'debt-amortisation',
     'slug': 'debt-amortisation-model-excel',
     'title': 'Debt Amortisation Model in Excel: Six Repayment Profiles',
     'h1': 'Debt Amortisation &amp; Repayment Model',
     'meta': 'Debt amortisation model in Excel. Six tranches: equal payment, equal principal, bullet, balloon '
             'and sculpted, with prepayment, refinancing and all-in cost.',
     'keywords': 'debt amortisation model excel, loan amortisation schedule excel, balloon payment calculator '
                 'excel, bullet loan schedule, loan refinancing calculator excel',
     'hero': 'Six tranches on six repayment profiles, month by month: two 30-year equal-payment loans, equal '
             'principal, bullet, balloon and a stepped sculpted profile. Compare them side by side, test a '
             'prepayment, price a refinancing and see the all-in cost once fees are counted.',
     'problem': ['The same headline rate can cost very different amounts depending on how the loan repays. '
                 'Borrowers comparing offers, and lenders explaining them, need the full schedule, not just the '
                 'monthly payment.',
                 'This model runs every profile from the same inputs and puts total interest, weighted average '
                 'life and the effective rate including fees next to each other, so the comparison is like for '
                 'like.'],
     'who': 'Corporate treasury and finance teams comparing facility offers. Lenders and brokers explaining '
            'repayment structures. Property investors and finance students learning how amortisation works.',
     'tabs': [('INPUTS',
               'For each tranche: principal, rate, term, frequency, start date, arrangement fee and annual fee; '
               'plus the balloon percentage, prepayment month and amount, and refinancing terms. Base, Upside, '
               'Downside and Stress scenarios.'),
              ('TRANCHE_1 to TRANCHE_6',
               'Monthly schedule per tranche: opening balance, payment, interest, principal, closing balance, '
               'cumulative interest and principal, and percentage repaid.'),
              ('COMPARISON',
               'All six side by side: total interest, total payments, interest to principal, weighted average '
               'life, a simple effective rate, and outstanding balance at annual snapshots.'),
              ('PREPAYMENT',
               'A lump-sum prepayment on the first mortgage tranche, the estimated interest saving, and a grid '
               'of savings by amount and timing.'),
              ('REFINANCING',
               'Existing against new terms at a chosen month: payment saving, break cost and new fee, net saving '
               'and payback period, with 60 months of monthly comparison.'),
              ('EFFECTIVE_RATE',
               'All-in cost of borrowing by tranche, including arrangement and annual fees, with an annual cash '
               'flow summary for the IRR approximation.'),
              ('DASHBOARD', 'Portfolio KPIs and chart data, including balance decline year by year.'),
              ('SENSITIVITY',
               'Total interest by rate and term, and interest saved by prepayment amount and timing.'),
              ('CHECKS', '75 integrity checks.')],
     'diffs': [('Six profiles, one set of inputs',
                'Equal payment, equal principal, bullet, balloon and sculpted, so the difference you see is the '
                'structure, not the assumptions.'),
               ('Sculpting you can read',
                'The sculpted tranche repays 0.5% of the balance a month for the first 40% of the term, 1% up to '
                '70%, then 2%, with the remainder at maturity.'),
               ('Fees in the rate',
                'EFFECTIVE_RATE adds arrangement and annual fees to interest, so the all-in cost of each tranche '
                'can be set against its nominal rate.'),
               ('Prepay or refinance',
                'Interest saved by a lump-sum prepayment, by amount and timing, and the payback period of a '
                'refinancing once break costs and new fees are paid.'),
               ('No circularity', "Interest is calculated on the prior period's closing balance.")],
     'faqs': [('How is it different from the Debt Schedule Model?',
               'This model compares repayment structures for individual loans. The Debt Schedule Model runs a '
               "borrower's whole capital structure of eight facilities, consolidates them and tests covenants."),
              ('What does it not do?',
               'Day count is 30/360 on monthly periods, with payments at month end. Prepayment savings are '
               'approximations, the sculpted tranche uses a stepped formula rather than a link to a cash flow '
               'forecast, and the IRR approximation on EFFECTIVE_RATE uses annual cash flows. Payment holidays, '
               'grace periods and tax effects are not modelled.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 18 tabs &middot; 6 tranches &middot; up to 360 months &middot; 75 integrity '
             'checks &middot; no macros &middot; instant download',
     'related': [('Debt Schedule Model', '/debt-schedule-model-excel.html'),
                 ('LBO Model', '/lbo-model-excel.html')]},
    {'id': 'portfolio-attrib',
     'slug': 'portfolio-return-attribution-model-excel',
     'title': 'Portfolio Return Attribution Model in Excel: Brinson',
     'h1': 'Portfolio Return Attribution Model',
     'meta': 'Portfolio return attribution model in Excel. Brinson allocation, selection and interaction, '
             'Fama-French 5-factor, sector and region views, TE, IR and VaR.',
     'keywords': 'portfolio attribution model excel, brinson attribution excel, performance attribution model, '
                 'fama french five factor excel, tracking error information ratio excel',
     'hero': "Explain where a portfolio's active return came from: Brinson-Hood-Beebower allocation, selection "
             'and interaction for 40 securities over 12 months, a Fama-French five-factor decomposition, sector '
             'and regional attribution, and the risk statistics that go with it.',
     'problem': ['Clients and investment committees do not stop at whether the portfolio beat the benchmark. '
                 'They ask whether it was the sector bets or the stock picks, and whether the excess return was '
                 'paid for with excess risk.',
                 'This model breaks active return into allocation, selection and interaction for every security '
                 'and month, rolls it up by sector and region, and puts tracking error, information ratio, '
                 'Sharpe, Sortino and VaR beside it.'],
     'who': 'Portfolio managers and performance analysts at asset and wealth managers. Investment consultants '
            'and fund selectors reviewing a manager. CFA candidates and students learning performance '
            'attribution.',
     'tabs': [('INPUTS',
               'Scenario, risk-free rate, management fee and a scenario return multiplier; 40 holdings with '
               'sector, region, portfolio and benchmark weights; monthly portfolio, benchmark and factor '
               'returns.'),
              ('PORTFOLIO_HOLDINGS', '40 securities by 12 months: weights, price returns and dividend returns.'),
              ('BENCHMARK', 'Benchmark weights, returns and contributions for the same 40 securities.'),
              ('BRINSON_ATTRIBUTION', 'Allocation, selection and interaction for every security and month.'),
              ('FACTOR_ATTRIBUTION',
               'Market, size, value, profitability and investment factor contributions by month, and '
               'cumulative.'),
              ('RISK_ANALYTICS',
               'Returns, excess returns and the building blocks of volatility for each security and month.'),
              ('SECTOR_ATTRIBUTION',
               'Portfolio and benchmark weights, over and underweights and returns by sector and month.'),
              ('GEOGRAPHIC_ATTRIBUTION', 'The same view across six regions.'),
              ('PERFORMANCE_SUMMARY',
               'Monthly gross and net returns against benchmark, then annualised alpha, tracking error, '
               'information ratio, Sharpe, Sortino, volatility, maximum drawdown and VaR at 95% and 99%.'),
              ('RISK_DECOMPOSITION',
               'Systematic against idiosyncratic risk by security, from beta and volatility.'),
              ('DASHBOARD',
               'Headline returns and ratios, monthly attribution, sector weights and factor exposures.'),
              ('SENSITIVITY',
               'Information ratio by alpha and tracking error, return by beta and market move, and allocation '
               'effect by weight deviation and return spread.'),
              ('CHECKS',
               '75 integrity checks, including portfolio and benchmark weights summing to 100% every month and '
               'the Brinson effects summing to the total.')],
     'diffs': [('Brinson at security level',
                'Allocation = (wp - wb) &times; (rb - Rb), selection = wb &times; (rp - rb), interaction = (wp - '
                'wb) &times; (rp - rb), for each of 40 securities in each of 12 months.'),
               ('Factors as well as bets',
                'The Fama-French five-factor view separates return earned from market, size, value, '
                'profitability and investment exposure.'),
               ('Sector and region roll-ups',
                'The same decomposition aggregated by sector and across six regions, so the committee sees the '
                'bets it recognises.'),
               ('Gross and net of fees',
                'The management fee is applied monthly, so alpha is shown before and after it.'),
               ('Risk next to return',
                'Tracking error, information ratio, Sharpe, Sortino, maximum drawdown and VaR, so excess return '
                'is judged against the risk taken.')],
     'faqs': [('Can I load my own portfolio?',
               'Yes. Replace the 40 holdings, their weights and the monthly portfolio, benchmark and factor '
               'returns on INPUTS. The demo returns are simulated for illustration.'),
              ('Which attribution methods does it use?',
               'Brinson-Hood-Beebower (1986) for allocation, selection and interaction, and the Fama and French '
               '(2015) five-factor model.'),
              ('What does it not do?',
               'Factor loadings are estimated, not regression-based. VaR assumes normally distributed returns, '
               'the risk decomposition is a linear approximation and currency effects are approximated from '
               'input rates. It covers 40 securities over 12 monthly periods.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 40 securities &times; 12 months &middot; 5 factors '
             '&middot; 75 integrity checks &middot; no macros &middot; instant download',
     'related': [('PE Fund Waterfall Model', '/pe-fund-waterfall-model-excel.html'),
                 ('Credit Fund Model', '/credit-fund-model-excel.html'),
                 ('Multi-Method Valuations Model', '/multi-method-valuation-model-excel.html')]},
    {'id': 'infra-dcf',
     'slug': 'infrastructure-dcf-model-excel',
     'title': 'Infrastructure DCF Model in Excel: Toll Road, Wind, Water',
     'h1': 'Infrastructure DCF Model',
     'meta': 'Infrastructure DCF model in Excel. Toll road, wind farm and water utility over 30 years: RAB '
             'roll-forward, DSCR debt sizing, covenants, FCFF and NPV.',
     'keywords': 'infrastructure dcf model excel, infrastructure valuation model, rab model excel, wind farm '
                 'financial model excel, toll road model excel',
     'hero': 'Value three infrastructure assets on their own revenue logic over 30 years: a toll road on traffic '
             'and tariff, a wind farm on capacity, availability and power price, and a water utility on its '
             'regulated asset base. Then size the debt to a target DSCR and test the covenants each year.',
     'problem': ['Infrastructure assets do not earn money the same way. A toll road carries volume risk, a wind '
                 'farm carries resource and price risk, and a regulated utility earns a return on its asset '
                 'base. A generic DCF treats them alike and misses what drives each one.',
                 'This model gives each asset its own revenue build, then runs common schedules for opex, capex '
                 'and RAB, debt, tax and free cash flow, so the three can be compared on one basis.'],
     'who': 'Infrastructure investors and fund analysts. Project finance and infrastructure lending teams sizing '
            'debt. Corporate finance advisers and students learning how regulated and contracted assets are '
            'valued.',
     'tabs': [('INPUTS',
               'WACC, risk-free rate, inflation, tax and concession period; for each asset its capex, operating '
               'assumptions, revenue drivers, senior debt, rate, tenor and target DSCR. Base, Upside, Downside '
               'and Stress scenarios.'),
              ('REVENUE_MODEL',
               '30-year revenue: toll traffic and tariff; wind capacity, capacity factor with degradation, '
               'availability, curtailment and power price; water RAB-based allowed revenue plus connections.'),
              ('OPERATING_COSTS',
               'Fixed and variable opex, insurance, management fees and lifecycle maintenance by asset, with '
               'EBITDA and margin.'),
              ('CAPEX_RAB',
               'Capex and the RAB roll-forward for each asset: opening, additions, depreciation and closing, '
               'with the return on RAB.'),
              ('DEBT_SCHEDULE',
               'Senior debt by asset: interest, amortisation, debt service, DSCR, LLCR, PLCR and DSRA, plus '
               'interest cover, leverage and debt to RAB.'),
              ('TAX',
               'Taxable income after tax depreciation and interest, losses carried forward, tax paid and the tax '
               'shield from debt.'),
              ('FREE_CASH_FLOW',
               'Pre-debt FCFF and post-debt FCFE by asset, with yields and cash-on-cash returns.'),
              ('RETURNS_ANALYSIS',
               'FCFF and FCFE totals, NPV at WACC, equity multiple, payback, average DSCR and gearing, and NPV '
               'at discount rates from 5% to 12%.'),
              ('DEBT_SIZING',
               'Maximum debt from CFADS and the target DSCR, headroom against the debt assumed, and a gearing '
               'table for the toll road from 50% to 80%.'),
              ('COVENANT_DASHBOARD',
               'DSCR, LLCR and PLCR against their minimums each year, the distribution lock-up test and '
               'distributions.'),
              ('SCENARIO_ANALYSIS',
               'All four scenarios for each asset side by side, with variance against the base case.'),
              ('DASHBOARD',
               'Portfolio NPV, equity multiple and average DSCR, with chart data for revenue, DSCR, FCFE, RAB '
               'and capital structure.'),
              ('SENSITIVITY',
               'Seven two-way tables, including portfolio NPV by volume growth and discount rate, and wind farm '
               'NPV by capacity factor and power price.'),
              ('CHECKS',
               '64 integrity checks, including the RAB and debt roll-forwards and cross-sheet consistency of '
               'revenue, EBITDA, debt service and capex for each asset.')],
     'diffs': [('Revenue built the way each asset earns',
                'Traffic times tariff, generation times price after availability and curtailment, and allowed '
                'return on RAB plus depreciation for the utility.'),
               ('Debt sized to cash flow',
                'Maximum debt comes from CFADS and a target DSCR using an annuity formula, with headroom shown '
                'against the debt assumed.'),
               ('Covenants every year',
                'DSCR minimum 1.20x, LLCR 1.10x, PLCR 1.15x and a distribution lock-up below 1.15x DSCR, tested '
                'across the projection.'),
               ('Tax that carries losses',
                'Tax depreciation, interest deductibility and losses carried forward, so early-year tax reflects '
                'the capital structure.'),
               ('Seven sensitivity tables',
                'From discount rate and volume growth to capacity factor and power price, and DSCR target '
                'against interest rate for debt capacity.')],
     'faqs': [('Which currency is it in?',
               'The demo is in US dollars, millions. All values are inputs, so any currency works if you are '
               'consistent.'),
              ('What does it not do?',
               'There is no construction phase: operation is assumed from the start. LLCR and PLCR are '
               'DSCR-based approximations, tax depreciation uses a 150% accelerated proxy, and working capital '
               'is a percentage of the change in revenue. Returns are reported as NPV, equity multiple and '
               'payback rather than IRR.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 18 tabs &middot; 3 assets &times; 30 years &middot; 4 scenarios &middot; 64 '
             'integrity checks &middot; no macros &middot; instant download',
     'related': [('Project Finance Model', '/project-finance-model-excel.html'),
                 ('PPP / Concession Model', '/ppp-concession-model-excel.html'),
                 ('DCF Model', '/dcf-model-excel.html')]},
    {'id': 'ppp-concession',
     'slug': 'ppp-concession-model-excel',
     'title': 'PPP Concession Model in Excel: PFI, VfM and PSC',
     'h1': 'PPP / Concession Model',
     'meta': 'PPP concession model in Excel. Hospital, road and school projects: availability payments, '
             'deductions, PSC, value for money, debt service, DSRA and returns.',
     'keywords': 'ppp model excel, pfi financial model, concession model excel, public sector comparator model, '
                 'value for money analysis ppp',
     'hero': 'Three PPP projects over a 30-year concession: a hospital PFI, a shadow toll road and a schools '
             'project. Model the payment mechanism with deductions, build the public sector comparator, test '
             'value for money, and run the cash flow waterfall, debt service and equity returns.',
     'problem': ['A PPP has two audiences who read the same model differently. The authority wants to know '
                 'whether the deal beats public procurement. Investors and lenders want to know whether the '
                 'unitary charge covers debt service with room for a dividend.',
                 'This model answers both from one set of inputs: a public sector comparator with optimism bias '
                 'and risk adjustments against the PPP cost to the authority, and a project cash flow waterfall '
                 'with DSCR, a debt service reserve and a dividend lock-up test.'],
     'who': 'Project finance and infrastructure teams at sponsors, lenders and advisers. Public sector finance '
            'teams assessing value for money. Infrastructure investors reviewing a PPP portfolio, and students '
            'of project finance.',
     'tabs': [('INPUTS',
               'PSC discount rate, inflation, tax, base rate, CAPM inputs, deduction rate, demand growth and '
               'cost overrun factor; for each project its construction cost, concession, availability payment, '
               'opex, lifecycle, debt and equity, demand base, third-party income, DSRA and lock-up DSCR; and '
               'the PSC risk and optimism bias percentages. Base, Upside, Downside and Stress scenarios.'),
              ('PSC_BENCHMARK',
               'Public sector comparator per project: raw cost, optimism bias, retained, transferred and '
               'transferable risk, competitive neutrality, and its NPV.'),
              ('CONCESSION_STRUCT',
               'The payment mechanism: availability payment by component, performance deductions, shadow toll or '
               'demand payment, third-party income and inflation uplift.'),
              ('REVENUE_FORECAST', '60-period revenue per project, in real and nominal terms.'),
              ('LIFECYCLE_CAPEX',
               'Annual lifecycle budget, five-year major maintenance and a reserve fund with contributions, '
               'drawdowns and interest.'),
              ('FINANCING_STRUCT',
               'Senior and mezzanine debt, equity, gearing, blended cost of debt, CAPM cost of equity, WACC, '
               'tenor, DSRA months and the interest rate hedge.'),
              ('CASH_FLOWS',
               'The waterfall per project: revenue, opex, lifecycle, debt service, tax, DSRA, the lock-up test, '
               'dividends and cash balance.'),
              ('DEBT_SERVICE', 'Drawdown, interest, repayment, DSCR, approximate LLCR and the DSRA per project.'),
              ('VFM_ANALYSIS',
               'PSC NPV against PPP NPV, the value for money saving, a breakeven discount rate and sensitivity '
               'to the discount rate.'),
              ('RISK_MATRIX',
               '15 risk types allocated between the public and private sectors, with the mitigant for each and '
               'quantified values per project.'),
              ('RETURNS',
               'Equity multiple, nominal and real equity IRR, NPV at cost of equity, payback, dividend yield, '
               'average and minimum DSCR, and LLCR.'),
              ('DASHBOARD',
               'Value for money, equity IRR, MOIC, minimum DSCR, gearing and dividend yield, with chart data for '
               'VfM and the DSCR profile.'),
              ('SENSITIVITY',
               'VfM by discount rate and deduction rate, equity IRR by availability payment and inflation, and '
               'NPV by cost overrun and demand growth.'),
              ('CHECKS',
               '59 integrity checks, including equity plus debt equal to total sources, debt repaid by maturity '
               'and non-negative cash and lifecycle reserves for every project.')],
     'diffs': [('Quarterly where it matters',
                'Forty quarterly periods for the first ten years, through construction and early operations, '
                'then twenty annual periods to year 30.'),
               ('Value for money from both sides',
                'PSC with optimism bias, risk adjustments and competitive neutrality against the PPP cost to the '
                'authority, with the saving and its sensitivity to the discount rate.'),
               ('A real payment mechanism',
                'Availability payment less performance deductions, plus demand or shadow toll payments and '
                'third-party income, indexed to inflation.'),
               ('Lender protections modelled',
                'A six-month debt service reserve, a lifecycle reserve fund and a dividend lock-up when DSCR '
                'falls below the covenant.'),
               ('Risk allocation on one page',
                'Fifteen risks, from construction overrun to refinancing, allocated public, private or shared, '
                'with the contractual mitigant for each.')],
     'faqs': [('Which projects are in the demo?',
               'A hospital PFI, a road on shadow tolls and a schools project, in sterling. Every assumption is '
               'an input, so each slot can carry your own project.'),
              ('What does it not do?',
               "Interest is not calculated on exact dates. Equity IRR uses Excel's IRR on annual cash flows "
               'rather than date-based XIRR, LLCR is approximated from DSCR, construction cost is spread evenly, '
               'and one inflation rate applies throughout; sector-specific indices are not modelled.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 18 tabs &middot; 3 projects &middot; 40 quarters + 20 years &middot; 59 '
             'integrity checks &middot; no macros &middot; instant download',
     'related': [('Project Finance Model', '/project-finance-model-excel.html'),
                 ('Infrastructure DCF Model', '/infrastructure-dcf-model-excel.html'),
                 ('Debt Schedule Model', '/debt-schedule-model-excel.html')]},
    {'id': 'buy-to-let',
     'slug': 'buy-to-let-model-excel',
     'title': 'Buy-to-Let Model in Excel: Portfolio Returns and Tax',
     'h1': 'Buy-to-Let Property Investment Model',
     'meta': 'Buy-to-let model in Excel. 10 UK properties: SDLT, monthly mortgages, cash flow, Section 24, '
             'personal vs company tax, equity build-up and yields.',
     'keywords': 'buy to let model excel, buy to let calculator excel, property investment model excel, section '
                 '24 calculator, rental yield calculator excel',
     'hero': 'Ten rental properties in one workbook: acquisition costs and stamp duty, a monthly mortgage '
             'schedule for each, annual P&amp;L and cash flow, value and equity growth, yields and equity '
             'multiples, and a side-by-side of owning personally or through a limited company.',
     'problem': ['Since Section 24, the same rent can leave a higher-rate landlord with much less than a company '
                 'owner keeps, and a portfolio spread across cities is hard to judge property by property on the '
                 'back of an envelope.',
                 'This model runs each property from purchase price and rent to net cash flow and equity, then '
                 'compares personal ownership, with mortgage interest relieved by a 20% tax credit, against a '
                 'company paying corporation tax and dividend tax on extraction.'],
     'who': 'Landlords and property investors, with one property or a portfolio. Mortgage brokers and property '
            'advisers modelling options for clients. Accountants comparing personal and company ownership.',
     'tabs': [('INPUTS',
               'Income tax, CGT, corporation tax, allowances and dividend rates; acquisition fees and the '
               'additional property surcharge; and for each of ten properties: price, deposit, mortgage rate and '
               'term, rent, voids, agent fee, service charge, ground rent, insurance, maintenance, house price '
               'growth and rental growth. Base, Upside, Downside and Stress scenarios.'),
              ('ACQUISITION_COSTS',
               'Deposit, mortgage, stamp duty, legal, survey, broker and valuation fees, total equity required '
               'and LTV per property.'),
              ('SDLT_CALCULATOR',
               'Stamp duty band by band for each property, plus the additional property surcharge and the '
               'effective rate.'),
              ('MORTGAGE_SCHEDULE',
               'Monthly repayment schedule for all ten mortgages: payment, interest, principal and balance.'),
              ('ANNUAL_PL',
               'Rent less voids and agent fees, mortgage interest and running costs, with the Section 24 credit '
               'and tax, per property.'),
              ('CASH_FLOW',
               'Annual cash in and out per property, cumulative cash flow and cash yield on equity.'),
              ('VALUATION',
               'Value with house price growth, mortgage outstanding, equity, LTV, gross yield and cumulative '
               'capital gain.'),
              ('RETURNS',
               'Gross and net yield, cash-on-cash, total return and equity multiple at 5, 10 and 25 years, per '
               'property.'),
              ('TAX_OPTIMISATION',
               'Personal ownership against a limited company for the portfolio: Section 24, personal allowance '
               'and bands, corporation tax and dividend tax on extraction.'),
              ('PORTFOLIO_SUMMARY',
               'All ten properties in one view, with weighted LTV, regions, flats against houses, and total '
               'value, equity and rent.'),
              ('DASHBOARD',
               'Chart data for equity build-up, cash flow, value against debt, yields, mortgage balances and the '
               'tax comparison.'),
              ('SENSITIVITY',
               'Five-year return by house price growth and yield, mortgage payment by rate and LTV, and net cash '
               'flow by void rate and mortgage rate.'),
              ('CHECKS',
               '62 integrity checks, including each mortgage repaid to zero at term and total principal repaid '
               'equal to the original loan.')],
     'diffs': [('Section 24 built in',
                'For personal ownership, mortgage interest is not deducted from rental profit; relief comes as a '
                '20% tax credit, property by property and for the portfolio.'),
               ('Personal or company, side by side',
                'The same portfolio taxed both ways: income tax with Section 24 against corporation tax and '
                'dividend tax on extracting the profit, with the annual difference.'),
               ('Stamp duty by band',
                'Each band calculated separately, with the additional property surcharge as an input.'),
               ('A mortgage schedule for every property',
                "Monthly repayment schedules on the annuity method, with interest on the prior month's balance."),
               ('Returns over three horizons',
                'Yield, cash-on-cash, total return and equity multiple at 5, 10 and 25 years, so near-term cash '
                'flow and long-term equity are both visible.')],
     'faqs': [('Which mortgage type does it model?',
               'Repayment mortgages on the annuity method. Refinancing and remortgaging are not modelled in this '
               'version.'),
              ('What does it not do?',
               'Stamp duty uses the SDLT bands on SDLT_CALCULATOR for every property, so Scottish LBTT and Welsh '
               'LTT are not calculated. Service charges and insurance rise at a fixed 3% a year, ground rent is '
               'held flat, and the company route assumes all profit is extracted as dividends.'),
              ('Are there macros?', 'No. Open formulas, no VBA. Every number traces back to an input.'),
              ('Can I see it before I buy?',
               'Yes. The free sample shows every tab, chart and check with real results on the demo portfolio, '
               'plus one engine tab with live formulas.')],
     'spec': 'Excel (.xlsx) &middot; 17 tabs &middot; 10 properties &middot; 30-year horizon &middot; 62 '
             'integrity checks &middot; no macros &middot; instant download',
     'related': [('Real Estate Fund Model', '/real-estate-fund-model-excel.html'),
                 ('Debt Amortisation Model', '/debt-amortisation-model-excel.html')]},
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
          <li><a href="/research/">Method Notes</a></li>
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
          <!-- SFS-LINKEDIN --><p class="footer-follow" style="margin-top:0.75rem;"><a href="https://www.linkedin.com/company/sfs-models/" target="_blank" rel="noopener" style="color:#C9A84C;">Follow SFS Models on LinkedIn &rarr;</a></p>
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
      <p style="color:var(--text-muted); font-size:0.9rem; margin-top:1rem;">The free sample shows every tab with real results &middot; one-time purchase, no subscription &middot; secure checkout via Lemon Squeezy</p>
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
        assert len(m["meta"]) <= 155, (m["id"], len(m["meta"]))
        p = ls[m["id"]]
        m["price"] = p["price"].replace("£", "").replace(".00", "")
        m["buy"] = p["buyUrl"]
        m["free"] = p["freeUrl"]
        out = ROOT / f"{m['slug']}.html"
        out.write_text(render(m), encoding="utf-8")
        print(f"wrote {out.name}  (£{m['price']})")


if __name__ == "__main__":
    main()
