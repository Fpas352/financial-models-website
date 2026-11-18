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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live. The only difference is that inputs are locked, so you evaluate it on the demo loan book rather than your own."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo portfolio."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo portfolio."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo portfolio."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo bank."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo portfolio."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo peer set."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo deal set."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo group."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo peer group."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo company."),
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
            ("Can I see it before I buy?", "Yes. The free sample is the complete workbook with every formula and check live, inputs locked, so you evaluate it on the demo company."),
        ],
        "spec": "Excel (.xlsx) &middot; 16 tabs &middot; 36 months + years 4-10 &middot; 5 revenue segments &middot; 193 integrity checks &middot; no macros &middot; instant download",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
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
