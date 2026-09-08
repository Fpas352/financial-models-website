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
        "cta_name": "ICAAP Model",
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
            ("Stress test integrated", "Same engine handles capital adequacy and stress testing - not two separate models."),
            ("UK + EU coverage", "Works for both PRA-supervised UK banks and ECB SSM-supervised EU banks. Buffer logic is jurisdiction-aware."),
        ],
        "faqs": [
            ("When will this be available?", "We're targeting Q3 2026 release. Sign up for notification and we'll email you the moment it ships."),
            ("Will it cover ILAAP too?", "ILAAP (Internal Liquidity Adequacy Assessment Process) is a separate model on a parallel track. Sign up here to get notified for both when ready."),
            ("Is there a US equivalent?", "Yes - our <a href=\"/bank-stress-test-model.html\">Bank Stress Test Model</a> covers CCAR / DFAST for US BHCs (live now)."),
            ("Can I commission an early build?", "Yes - we do custom builds for institutions that need it sooner. Pricing varies by scope. Use the form below or contact us directly."),
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
        "cta_name": "Project Finance SPV Model",
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
            ("LLCR + PLCR + DSCR", "All three cover ratios calculated - not just DSCR. Lenders will want all three."),
            ("Long-dated horizon", "Up to 30-year forecast. Works for infrastructure concessions and PPP deals."),
            ("Debt sizing tool", "Solves debt quantum from target DSCR, not the other way around. Standard at infrastructure desks."),
        ],
        "faqs": [
            ("When will this be available?", "Built as an .xlsx file already. Currently being prepared for launch - targeting May 2026. Sign up to get notified the moment it ships."),
            ("Will it support PPP / concession deals?", "Yes - the same engine handles infrastructure, energy, PPP, concession deals. Toggle on INPUTS."),
            ("What about renewable energy specifics?", "Solar, wind, battery storage all work. Revenue can be PPA-based, merchant-based, or blended."),
            ("Can I commission an early build?", "Yes - for time-sensitive deals, we do custom builds with same-day delivery. Use the form below or contact us."),
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
        "cta_name": "PE Fund Waterfall Model",
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
            ("European + American carry", "Most templates support one. Ours has both with a single switch - useful when modelling different fund structures or comparing waterfall economics."),
            ("Full catch-up mechanics", "GP catch-up after LP preferred return is calculated explicitly with the right precedence. Most templates skip this."),
            ("Realistic fee modelling", "Management fee on commitment vs NAV with the standard taper post-investment period."),
            ("LP-side perspective", "Output tab includes LP-side cash flow profile, not just GP economics."),
            ("Fund vs deal split", "Both fund-level and deal-level returns calculated and reconciled."),
        ],
        "faqs": [
            ("When will this be available?", "Built as an .xlsx file already. Currently being prepared for launch - targeting May 2026. Sign up to get notified the moment it ships."),
            ("Does it support continuation funds?", "Not in v1. Available as a custom build - contact us."),
            ("What about real estate / credit funds?", "Separate models on the same release track: <a href=\"/contact.html\">contact us</a> if you want all three."),
            ("Can I commission an early build?", "Yes - we do custom builds for fund teams that need it sooner. Use the form below."),
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
        "cta_name": "IFRS 17 Insurance Model",
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
            ("Three transition methods", "Full retrospective, modified retrospective, fair value - all built in for institutions still finalising the transition story."),
            ("CSM amortisation", "Coverage units approach. Time-based and other allocation patterns supported."),
            ("Disclosure format", "P&amp;L output matches IFRS 17 financial statement disclosure format. Audit-ready."),
            ("Sensitivity testing", "Discount rate, risk adjustment, lapse rate sensitivities with one-click recalc."),
        ],
        "faqs": [
            ("When will this be available?", "Built as an .xlsx file already. Currently being prepared for launch - targeting Q3 2026. Sign up to get notified."),
            ("Does it cover SST (Swiss Solvency Test) too?", "Not in v1. SST and Solvency II capital modelling is a separate release track."),
            ("Will it work with my actuarial system data?", "Yes - the model is data-input agnostic. Paste cash flows from any system into the input tab."),
            ("Can I commission an early build?", "Yes - for institutions in implementation, we do custom builds. Use the form below or contact us."),
        ],
        "spec": "Excel (.xlsx) &middot; ~12 tabs &middot; GMM + PAA + Transition &middot; expected pricing &pound;1,295 &middot; Q3 2026 launch target",
        "related": [
            ("IFRS 9 / CECL Model", "/ifrs9-cecl-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
            ("Full Catalogue", "/models.html"),
        ],
    },
    {
        "slug": "ilaap-model-excel",
        "cta_name": "ILAAP Model",
        "title": "ILAAP Model Excel Template",
        "h1": "ILAAP Model Excel Template",
        "keyword": "ilaap model excel",
        "meta_desc": "ILAAP model in Excel for UK and EU banks. Internal Liquidity Adequacy Assessment Process, LCR, NSFR, stress liquidity outflows, survival horizon. Notify when available.",
        "subtitle": "Internal Liquidity Adequacy Assessment Process (ILAAP) model for UK and EU banks. LCR, NSFR, stress liquidity outflows, survival horizon, FTP framework. Practitioner-built.",
        "form_name": "ilaap-notify",
        "audience": "Bank Treasury and Liquidity teams, CFOs and Finance Directors at PRA-supervised and ECB SSM-supervised banks. ALCO secretariats, liquidity risk managers, and consultancies supporting ILAAP submissions.",
        "tabs": [
            ("COVER", "Model documentation, methodology selection, ILAAP submission context."),
            ("INPUTS", "Liquidity buffer calibration, stress scenario parameters, LCR/NSFR weights, FTP rate assumptions, survival horizon target."),
            ("HQLA_BUFFER", "High Quality Liquid Assets (HQLA) stock: Level 1, Level 2A, Level 2B. Haircutting and concentration limits."),
            ("LCR", "Liquidity Coverage Ratio: net 30-day stressed outflows vs HQLA. Regulatory threshold tracking (100% minimum)."),
            ("NSFR", "Net Stable Funding Ratio: available stable funding vs required stable funding. Basel III/CRR2 methodology."),
            ("STRESS_OUTFLOWS", "Idiosyncratic, market-wide, and combined stress scenarios. Contractual vs behavioural outflow assumptions."),
            ("SURVIVAL_HORIZON", "Days of survival under each stress scenario. Cash flow waterfall by day/week."),
            ("FTP_FRAMEWORK", "Funds Transfer Pricing: liquidity cost allocation to business lines. Internal pricing of liquidity risk."),
            ("CONTINGENCY_PLAN", "Contingency Funding Plan triggers and early warning indicators. Escalation thresholds."),
            ("OUTPUTS", "Executive summary, regulator-ready liquidity position table, ALCO dashboard format."),
            ("CHECKS", "LCR numerator/denominator ties, NSFR reconciles, survival horizon calculations balance."),
        ],
        "differentiators": [
            ("PRA ILAAP submission alignment", "Output format mirrors PRA ILAAP table structure. Reduces reformatting work at submission time."),
            ("LCR + NSFR + Survival Horizon", "All three regulatory liquidity metrics in one model. Most templates cover only LCR."),
            ("Idiosyncratic + systemic stress", "Three stress scenarios built in: bank-specific crisis, market-wide stress, combined. Regulator expectation."),
            ("FTP framework integrated", "Internal liquidity cost allocation framework included. Not just regulatory metrics - operational ALM tool."),
            ("Companion to ICAAP model", "Designed to pair with the ICAAP model for banks needing both Pillar 2 submissions."),
        ],
        "faqs": [
            ("When will this be available?", "Targeting Q3 2026. Sign up and we'll email you the moment it ships."),
            ("Is there an ICAAP model too?", "Yes - the <a href=\"/icaap-model-excel.html\">ICAAP Model</a> is on the same release track. Sign up for both."),
            ("Does it cover US LCR (FR 2052a)?", "v1 covers CRR2/PRA methodology. US LCR (FR 2052a reporting) is a separate model on the pipeline."),
            ("Can I commission an early build?", "Yes. For time-sensitive ILAAP submissions, we do custom builds. Use the form below or email sfsmodels362@gmail.com."),
        ],
        "spec": "Excel (.xlsx) &middot; ~12 tabs &middot; CRR2 / PRA ILAAP aligned &middot; expected pricing &pound;995 &middot; Q3 2026 launch target",
        "related": [
            ("ICAAP Model (coming soon)", "/icaap-model-excel.html"),
            ("Bank Long-Term Plan Model", "/bank-financial-model.html"),
            ("Bank Stress Test Model", "/bank-stress-test-model.html"),
        ],
    },
    {
        "slug": "real-estate-fund-model-excel",
        "cta_name": "Real Estate Fund Model",
        "title": "Real Estate Fund Model Excel Template",
        "h1": "Real Estate Fund Financial Model Excel Template",
        "keyword": "real estate fund model excel",
        "meta_desc": "Real estate fund model in Excel. Property valuation, NOI, leveraged returns, IRR, equity multiple, GP/LP waterfall for property funds and REITs. Notify when available.",
        "subtitle": "Real estate fund model with property-level NOI, leveraged returns, IRR, equity multiple, and GP/LP waterfall. Handles residential, commercial, and mixed-use portfolios.",
        "form_name": "real-estate-fund-notify",
        "audience": "Real estate fund managers, property investment analysts, REITs and private real estate funds, infrastructure and alternative asset managers adding real estate exposure, family offices with direct property portfolios.",
        "tabs": [
            ("COVER", "Model documentation, asset type toggle, jurisdiction selector."),
            ("FUND_INPUTS", "Commitment size, fund term, investment period, target return, fee structure, carry terms."),
            ("PROPERTY_INPUTS", "Asset type (residential/commercial/mixed), purchase price, rental income, exit cap rate, vacancy assumptions, capex schedule."),
            ("NOI", "Net Operating Income build: gross rental income, vacancy, operating expenses, property taxes, management fees."),
            ("DEBT_SCHEDULE", "LTV-based acquisition debt, amortisation, refinancing. Interest cover ratio (ICR) tracking."),
            ("PROPERTY_RETURNS", "Levered and unlevered IRR per asset. Gross and net equity multiple. Cash-on-cash yield."),
            ("FUND_RETURNS", "Aggregated fund-level returns. Vintage year blending. DPI, RVPI, TVPI."),
            ("WATERFALL", "GP/LP waterfall: preferred return, catch-up, carried interest. European structure."),
            ("SENSITIVITY", "Returns sensitivity to entry yield, exit cap rate, vacancy, LTV, and hold period."),
            ("OUTPUTS", "Investment committee format summary. Property-level and fund-level return table."),
            ("CHECKS", "Cash flows reconcile, debt service tiesout, waterfall splits correct."),
        ],
        "differentiators": [
            ("Property-level and fund-level returns", "Calculates IRR both at individual asset level and rolled up to fund level. Handles portfolio blending."),
            ("ICR covenant tracking", "Interest cover ratio calculated and flagged against covenant threshold throughout hold period."),
            ("Leveraged and unlevered IRR", "Both always calculated and displayed. Separates asset quality from capital structure effect."),
            ("Exit cap rate sensitivity", "One of the most important real estate valuation inputs - dedicated sensitivity table with 5 scenarios."),
            ("GP/LP waterfall included", "Full European waterfall mechanics. Not just property-level returns - fund economics too."),
        ],
        "faqs": [
            ("When will this be available?", "Targeting Q3 2026. Sign up and we'll email when it ships."),
            ("Does it handle REITs?", "v1 targets private real estate funds. REIT-specific modelling (NAV, FFO, AFFO) is a separate release track."),
            ("What about UK Stamp Duty and SDLT?", "Yes - transaction cost assumptions include configurable SDLT for UK assets. Other jurisdictions configurable via INPUTS."),
            ("Can I commission an early build for a live deal?", "Yes. For active transactions, we do custom builds with fast turnaround. Use the form below."),
        ],
        "spec": "Excel (.xlsx) &middot; ~12 tabs &middot; commercial and residential &middot; expected pricing &pound;395 &middot; Q3 2026 launch target",
        "related": [
            ("PE Fund Waterfall Model", "/pe-fund-waterfall-model-excel.html"),
            ("Project Finance Model", "/project-finance-model-excel.html"),
            ("DCF Model", "/dcf-model-excel.html"),
        ],
    },
    {
        "slug": "credit-fund-model-excel",
        "cta_name": "Credit Fund Model",
        "title": "Credit Fund Model Excel Template",
        "h1": "Credit Fund Financial Model Excel Template",
        "keyword": "credit fund model excel",
        "meta_desc": "Credit fund model in Excel. Fixed income portfolio, yield-to-maturity, duration, credit spread, default risk, NAV, IRR, fund-level economics. Notify when available.",
        "subtitle": "Credit fund model for direct lending, CLO, and fixed income portfolio managers. Yield-to-maturity, duration, credit spread, default assumptions, NAV build, fund-level IRR and management economics.",
        "form_name": "credit-fund-notify",
        "audience": "Direct lending fund managers, CLO managers, credit analysts at asset managers, credit hedge funds, insurance company investment teams managing fixed income portfolios, LP investors evaluating credit fund terms.",
        "tabs": [
            ("COVER", "Model documentation, credit strategy selector (direct lending / CLO / fixed income)."),
            ("FUND_INPUTS", "Fund size, vintage, fee structure, hurdle, carry terms, investment period."),
            ("PORTFOLIO_INPUTS", "Loan/bond details: face value, coupon/spread, maturity, credit rating, expected recovery."),
            ("YIELD_CALC", "Yield-to-maturity, yield-to-call, current yield. Accrued interest. Clean vs dirty price."),
            ("DURATION", "Macaulay duration, modified duration, convexity. DV01 per position and aggregate."),
            ("DEFAULT_MODEL", "Default rate assumptions by rating cohort. Recovery rate, LGD, expected credit loss."),
            ("NAV", "Net Asset Value build: portfolio fair value + accrued income - management fees - carried interest. Monthly NAV roll."),
            ("FUND_RETURNS", "Gross and net IRR, MOIC, DPI, TVPI. Cash yield vs total return split."),
            ("WATERFALL", "Management fee and carry calculation. Hurdle rate mechanics for credit fund structure."),
            ("SENSITIVITY", "Returns sensitivity to default rate, recovery, spread, and reinvestment rate assumptions."),
            ("OUTPUTS", "LP report format. Portfolio analytics. Performance attribution."),
            ("CHECKS", "NAV reconciles, yield calculations tie to cash flows, waterfall splits correct."),
        ],
        "differentiators": [
            ("Direct lending and fixed income", "Single model handles both direct lending (floating rate, OID) and fixed income bond portfolios. Toggle on INPUTS."),
            ("Duration and DV01", "Full duration analytics: Macaulay, modified, convexity, DV01. Not just yield metrics."),
            ("Default scenario analysis", "Stress default rates by rating category with recovery assumptions. Calculates fund-level impact on IRR."),
            ("NAV roll-forward", "Monthly NAV build with fee netting. Essential for credit fund reporting."),
            ("Reinvestment rate sensitivity", "Critical for credit funds with revolving portfolios - built into the returns engine."),
        ],
        "faqs": [
            ("When will this be available?", "Targeting Q3 2026. Sign up and we'll email when it ships."),
            ("Does it cover CLO tranche structuring?", "v1 focuses on the equity/GP perspective. CLO tranching model is a separate release on the pipeline."),
            ("What about private credit / direct lending?", "Yes - the floating rate, OID, PIK mechanics for direct lending are all supported."),
            ("Can I commission an early build?", "Yes. Use the form below or email sfsmodels362@gmail.com for custom builds."),
        ],
        "spec": "Excel (.xlsx) &middot; ~13 tabs &middot; direct lending + fixed income &middot; expected pricing &pound;395 &middot; Q3 2026 launch target",
        "related": [
            ("PE Fund Waterfall Model", "/pe-fund-waterfall-model-excel.html"),
            ("LBO Model", "/lbo-model-excel.html"),
            ("IFRS 9 / CECL Model", "/ifrs9-cecl-model-excel.html"),
        ],
    },
    {
        "slug": "merger-consequences-model-excel",
        "cta_name": "Merger Consequences Model",
        "title": "Merger Consequences Model Excel Template",
        "h1": "Merger Consequences (Accretion / Dilution) Model",
        "keyword": "merger consequences model excel",
        "meta_desc": "Merger consequences model in Excel. Accretion/dilution analysis, pro forma EPS, purchase price allocation, goodwill, synergies, financing mix. Investment banking ready. Notify when available.",
        "subtitle": "Merger consequences model with accretion/dilution analysis, pro forma EPS, purchase price allocation, goodwill calculation, synergy modelling, and deal financing mix. Built for investment banking deal teams.",
        "form_name": "merger-consequences-notify",
        "audience": "Investment banking M&A analysts and associates, corporate development teams at acquirers, financial advisors on buy-side M&A mandates. CFOs evaluating acquisition economics and board-level deal presentations.",
        "tabs": [
            ("COVER", "Model documentation, deal parameters, accretion/dilution headline."),
            ("INPUTS", "Acquirer standalone financials, target financials, deal price and structure, financing mix (cash/stock/debt), synergy assumptions."),
            ("TRANSACTION", "Transaction summary: enterprise value, equity value, offer premium, deal multiples (EV/EBITDA, EV/Revenue, P/E)."),
            ("PPA", "Purchase price allocation: book value step-up, fair value adjustments, identified intangibles, residual goodwill calculation."),
            ("SYNERGIES", "Revenue and cost synergy modelling with phasing (Year 1-3). Pre-tax synergies, tax impact, cost to achieve."),
            ("PRO_FORMA_IS", "Pro forma income statement: combined P&L, D&A step-up from PPA, interest on deal debt, synergies, one-off costs."),
            ("ACCRETION_DILUTION", "EPS accretion/dilution: standalone acquirer EPS vs pro forma EPS. Breakeven synergies. IRR of the deal."),
            ("FINANCING", "Financing mix analysis: all-cash, all-stock, mixed. Impact on leverage, interest coverage, credit profile."),
            ("SENSITIVITY", "Accretion/dilution sensitivity to offer price, synergies, financing mix, and tax rate."),
            ("OUTPUTS", "Investment committee / board summary: headline metrics, deal rationale, accretion/dilution summary."),
            ("CHECKS", "PPA sources and uses balance, EPS calculations tie, pro forma financials reconcile."),
        ],
        "differentiators": [
            ("Purchase price allocation built in", "Goodwill, D&A step-up, identified intangibles all modelled explicitly - not just headline EPS math."),
            ("Synergy breakeven analysis", "Calculates the minimum synergies required for accretion. Standard ask from investment committee."),
            ("Financing mix toggle", "Switch between all-cash, all-stock, and mixed financing in one click. Each updates accretion/dilution automatically."),
            ("Cost to achieve synergies", "Transaction and integration costs modelled with phasing - not just gross synergies."),
            ("IRR of the acquisition", "Calculates implied IRR of the deal at current price and synergy assumptions. Bridges M&A and PE frameworks."),
        ],
        "faqs": [
            ("When will this be available?", "Targeting Q2 2026. Sign up and we'll email when it ships."),
            ("Does it work for bank M&A (bank-on-bank deals)?", "v1 is sector-agnostic. Bank-specific M&A model (tangible book value dilution, CET1 impact) is a separate release."),
            ("Will it handle stock-for-stock deals with exchange ratios?", "Yes - fixed exchange ratio, fixed value, and collar structures are all supported."),
            ("Can I commission an early build for a live deal?", "Yes. For live mandates, we build custom models with same-day or next-day turnaround. Use the form below."),
        ],
        "spec": "Excel (.xlsx) &middot; ~11 tabs &middot; sector-agnostic &middot; expected pricing &pound;295 &middot; Q2 2026 launch target",
        "related": [
            ("DCF Model", "/dcf-model-excel.html"),
            ("LBO Model", "/lbo-model-excel.html"),
            ("PE Fund Waterfall Model", "/pe-fund-waterfall-model-excel.html"),
        ],
    },
    {
        "slug": "restructuring-model-excel",
        "cta_name": "Restructuring and Recovery Model",
        "title": "Restructuring & Recovery Financial Model Excel",
        "h1": "Restructuring & Recovery Financial Model",
        "keyword": "restructuring financial model excel",
        "meta_desc": "Restructuring and recovery financial model in Excel. Distressed scenario modelling, liquidity runway, debt-for-equity swap, recovery analysis, creditor waterfall. Notify when available.",
        "subtitle": "Restructuring and recovery model for distressed situations. Liquidity runway, going concern analysis, debt-for-equity swap mechanics, creditor recovery waterfall, and plan of reorganisation financials.",
        "form_name": "restructuring-notify",
        "audience": "Restructuring advisors at investment banks and advisory firms, distressed debt investors, insolvency practitioners and administrators, turnaround management teams, creditor committees and their legal advisors.",
        "tabs": [
            ("COVER", "Model documentation, scenario active, restructuring timeline."),
            ("INPUTS", "Current debt structure, creditor hierarchy, liquidity position, trading assumptions, restructuring levers."),
            ("LIQUIDITY", "13-week cash flow: receipts, disbursements, net cash burn. Liquidity runway calculation. DIP financing sizing."),
            ("GOING_CONCERN", "Going concern vs liquidation analysis. Minimum liquidity covenant threshold. Covenant breach date."),
            ("DEBT_STRUCTURE", "Current debt waterfall by tranche: secured, unsecured, subordinated. Interest burden and coverage."),
            ("RECOVERY_ANALYSIS", "Creditor recovery rates by tranche under multiple scenarios. Enterprise value range (DCF + comparables). Recovery vs par."),
            ("DX_SWAP", "Debt-for-equity swap mechanics. New equity value post-restructuring. Existing equity dilution/wipeout."),
            ("POR_FINANCIALS", "Plan of reorganisation: pro forma financials post-restructuring. Emergence capital structure. Day-1 leverage."),
            ("SENSITIVITY", "Recovery sensitivity to enterprise value assumption. Trading case vs liquidation case comparison."),
            ("CREDITOR_WATERFALL", "Detailed waterfall of recoveries by creditor class under each scenario."),
            ("OUTPUTS", "Management summary, creditor recovery table, emergence capitalisation table."),
            ("CHECKS", "Cash flows reconcile, creditor waterfall sums correctly, debt service on exit structure is serviceable."),
        ],
        "differentiators": [
            ("13-week cash flow", "Week-by-week liquidity model with receipts and disbursements - essential for any distressed situation."),
            ("Going concern vs liquidation", "Side-by-side comparison with break-even enterprise value. Fundamental to any restructuring engagement."),
            ("Debt-for-equity mechanics", "Proper treatment of the debt-for-equity conversion including new money, backstop fees, and equity allocation."),
            ("Creditor recovery waterfall", "Full priority waterfall by tranche with recovery rates. Essential tool for any creditor-side or advisor engagement."),
            ("Plan of reorganisation financials", "Pro forma emergence financials with exit capital structure. Bridges the restructuring and M&A frameworks."),
        ],
        "faqs": [
            ("When will this be available?", "Targeting Q3 2026. Sign up and we'll email when it ships."),
            ("Does it cover UK administration and CVA processes?", "Yes - UK administration, CVA, and US Chapter 11 scenarios are all handled. Jurisdiction is configurable."),
            ("Will it work for financial institutions (bank restructurings)?", "v1 is sector-agnostic. Bank-specific restructuring (regulatory capital implications, resolution mechanics) is a custom build."),
            ("Can I commission an early build for a live situation?", "Yes - for live mandates this is the most common request. Same-day builds available. Use the form below."),
        ],
        "spec": "Excel (.xlsx) &middot; ~12 tabs &middot; UK administration + US Chapter 11 &middot; expected pricing &pound;495 &middot; Q3 2026 launch target",
        "related": [
            ("LBO Model", "/lbo-model-excel.html"),
            ("DCF Model", "/dcf-model-excel.html"),
            ("Merger Consequences Model", "/merger-consequences-model-excel.html"),
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
<!-- SFS-ANALYTICS -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "7852444a13cc4cc78cdb4162c284e1de"}}'></script>
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
      <p style="margin-top:1rem;"><a href="/contact.html?model={slug}" class="btn btn-primary" data-enquiry-cta="{slug}">Request the {cta_name}</a> <a href="/models.html" class="btn btn-secondary">Browse the live catalogue</a></p>
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
            cta_name=m["cta_name"],
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
