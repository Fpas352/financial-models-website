# Lemon Squeezy Product Setup Reference Sheet

> Generated from the SFS Models website codebase. Use this to create each product in Lemon Squeezy with consistent names, descriptions, and prices.

---

## Product Summary Table

| # | Product Name | Short Description | Price (GBP) | Tier |
|---|---|---|---|---|
| 1 | Lending Model | Model retail and commercial loan books with full amortisation and covenant tracking. Cohort-based vintage engine with PD/LGD and NIM bridge output. | £299 | Banking & Lending |
| 2 | Deposits Model | Analyse deposit product mix, funding costs, and maturity profiles. Product-level stock and flow engine with deposit beta pricing. | £249 | Banking & Lending |
| 3 | Credit Analysis Model | Assess borrower creditworthiness with ratio analysis and scoring. Includes qualitative overlays, risk rating, and summary credit memo output. | £249 | Banking & Lending |
| 4 | Loan Pricing Model | Price loans to target return on equity with full cost-of-funds build. Includes capital allocation, target ROE back-solve, and breakeven analysis. | £249 | Banking & Lending |
| 5 | IFRS 9 ECL Model | Calculate expected credit losses across stages with PD/LGD/EAD inputs. Stage 1/2/3 allocation with lifetime and 12-month ECL calculation. | £299 | Banking & Lending |
| 6 | Deposit Pricing & NII Model | Model deposit pricing decisions and net interest income impact. Product-level rate setting with beta pass-through and competitive positioning. | £249 | Banking & Lending |
| 7 | Treasury / IRS Model | Value and risk-manage interest rate swaps with full cash flow schedules. Yield curve build, discount factors, DV01, and hedge effectiveness. | £299 | Treasury & Capital Markets |
| 8 | Bond Pricing & Yield Model | Price fixed income instruments and calculate yield metrics. Dirty/clean price, YTM, Z-spread, duration, and convexity output. | £249 | Treasury & Capital Markets |
| 9 | Duration & Rate Sensitivity Model | Measure portfolio duration, convexity, and rate sensitivity. Parallel and non-parallel shift scenarios with P&L impact in basis points. | £249 | Treasury & Capital Markets |
| 10 | FX Hedging Model | Model FX exposure and evaluate hedging strategies. Multi-currency exposure mapping with forward and option hedge cost tracking. | £249 | Treasury & Capital Markets |
| 11 | LCR Model | Calculate Liquidity Coverage Ratio to Basel III standards. HQLA classification, net cash outflow calculation, and 30-day stress buffer. | £249 | Treasury & Capital Markets |
| 12 | Capital / Regulatory Model | Calculate risk-weighted assets and capital ratios under Basel frameworks. Credit, market, and operational risk RWA with Pillar 2A and stress testing. | £299 | Risk & Regulatory |
| 13 | VaR Model | Estimate Value at Risk using historical and parametric methods. Confidence intervals at 95% and 99% with backtesting and stress VaR. | £299 | Risk & Regulatory |
| 14 | Stress Testing Model | Run scenario and sensitivity analysis for ICAAP and board reporting. Base, adverse, and severe scenarios with P&L, capital, and liquidity impact. | £299 | Risk & Regulatory |
| 15 | DCF Valuation Model | Intrinsic value via discounted cash flow with WACC and terminal value. FCFF/FCFE projections with sensitivity tables and football field output. | £249 | Valuation & Corporate Finance |
| 16 | Trading Comps Model | Peer group valuation using market multiples. EV/EBITDA, P/E, and P/B multiples with peer screening and implied valuation range. | £199 | Valuation & Corporate Finance |
| 17 | Precedent Transactions Model | M&A deal comps with transaction multiple analysis. Deal database with premium analysis and implied valuation output. | £199 | Valuation & Corporate Finance |
| 18 | LBO Model | Leveraged buyout returns model with debt waterfall and IRR analysis. Sources and uses, multi-tranche debt, and sensitivity on entry/exit multiples. | £299 | Valuation & Corporate Finance |
| 19 | SOTP Valuation Model | Sum-of-the-parts valuation for diversified businesses. Segment-level DCF and comps with holding company discount analysis. | £199 | Valuation & Corporate Finance |
| 20 | DDM (Dividend Discount) Model | Equity valuation based on projected dividend streams. Multi-stage growth DDM with cost of equity and CAPM build. | £199 | Valuation & Corporate Finance |
| 21 | Valuations Model (Multi-Method) | Combined valuation across DCF, comps, and precedents in a single workbook. Football field chart and weighted blended valuation output. | £299 | Valuation & Corporate Finance |
| 22 | 3-Statement Integrated Model | Fully linked P&L, balance sheet, and cash flow model. Revenue and cost driver assumptions with 3 scenarios and ratio analysis. | £249 | FP&A & Management Reporting |
| 23 | Budget vs Actual Variance Model | Monthly variance analysis with commentary framework. Volume, price, and mix variance decomposition with YTD tracking. | £149 | FP&A & Management Reporting |
| 24 | Rolling Forecast Model | Dynamic 12-month rolling forecast with reforecast logic. Auto-roll mechanism with actuals lock and forecast accuracy tracking. | £149 | FP&A & Management Reporting |
| 25 | Budget vs Forecast Model | Track forecast accuracy against original budget. Side-by-side budget, latest forecast, and actuals with variance waterfall. | £149 | FP&A & Management Reporting |
| 26 | Cost Control Model | Departmental cost tracking and variance analysis. Cost centre breakdown with headcount, non-staff costs, and savings analysis. | £149 | FP&A & Management Reporting |
| 27 | Management Accounts Pack | Board-ready management accounts with KPI dashboard. P&L, balance sheet, and cash flow summaries with RAG indicators. | £199 | FP&A & Management Reporting |
| 28 | Working Capital Model | Cash conversion cycle and working capital requirement analysis. Receivables, payables, and inventory drivers with facility sizing. | £149 | FP&A & Management Reporting |
| 29 | Capitalisation Model (IAS 38) | Intangible asset capitalisation with phase tracking and amortisation. Research vs development phase tracking with IAS 38 compliance checks. | £99 | Accounting & Fixed Assets |
| 30 | PPE Model (IAS 16) | Property, plant, and equipment register with depreciation schedules. Asset register with straight-line and reducing balance depreciation. | £99 | Accounting & Fixed Assets |
| 31 | Impairment Model (IAS 36) | Impairment testing with value-in-use and recoverable amount. CGU-level allocation with reversal tracking and disclosure output. | £99 | Accounting & Fixed Assets |
| 32 | Capex Model | Capital expenditure planning, approval tracking, and variance analysis. Project-level tracking with phasing, budget vs actual, and forecast to complete. | £149 | Accounting & Fixed Assets |
| 33 | Debt Schedule Model | Full debt waterfall with covenant testing and refinancing scenarios. Multi-tranche debt with leverage, DSCR, and ICR covenant testing. | £199 | Debt & Leverage |
| 34 | Debt Amortisation Model | Loan amortisation schedules across multiple tranches. Bullet, annuity, and sculpted repayment with fixed and floating rate support. | £149 | Debt & Leverage |
| 35 | Complete LTP Model | Comprehensive Long-Term Plan model fully integrated across capital, funding, income, costs, and balance sheet projections. 3 scenarios with board-ready outputs. | £999 | Integrated Planning |

---

## Lemon Squeezy Product Descriptions

Paste the description below into the Lemon Squeezy product page for each model.

---

### 1. Lending Model — £299

An institutional-grade Excel model for retail and commercial lending portfolios. Built around a cohort-based vintage engine with PD/LGD inputs, amortisation schedules, and covenant tracking. Outputs include a full P&L with net interest income, provisions, NIM bridge, and three scenario overlays (Base, Upside, Downside). Includes a built-in CHECKS tab for model integrity and is formatted for A4 landscape printing. Fully unlocked — modify any assumption, formula, or layout.

---

### 2. Deposits Model — £249

A product-level deposit book model covering current accounts, savings, notice accounts, and fixed-term deposits. Uses a stock-and-flow balance engine with deposit beta pricing, NIM contribution analysis, and maturity/repricing gap reporting. Includes three scenario overlays and full cost-of-funds decomposition. Designed for FP&A, ALM, and treasury teams at banks and building societies. Fully unlocked Excel workbook with documentation and integrity checks.

---

### 3. Credit Analysis Model — £249

A structured credit assessment model with financial ratio analysis, qualitative scoring overlays, and risk rating output. Suitable for analysing corporate, SME, and institutional borrowers. Produces a summary credit memo with key metrics, risk flags, and recommendation framework. Three scenario overlays allow stress-testing under different economic assumptions. Fully unlocked Excel workbook with built-in checks and print-ready output.

---

### 4. Loan Pricing Model — £249

Price individual loans to a target return on equity with a full cost-of-funds and capital allocation build. Includes funding cost decomposition, expected loss provisions, operating cost allocation, and fee income modelling. Back-solves for the minimum rate required to hit target ROE and provides breakeven analysis. Three scenario overlays with sensitivity tables. Fully unlocked Excel workbook designed for credit and pricing teams.

---

### 5. IFRS 9 ECL Model — £299

Calculate expected credit losses under IFRS 9 with stage 1, 2, and 3 allocation logic. Inputs include PD term structures, LGD assumptions, and EAD profiles with automated stage transfer triggers. Computes both 12-month and lifetime ECL with macro-economic overlay and sensitivity analysis. Suitable for regulatory reporting, audit support, and board presentations. Fully unlocked Excel workbook with documentation and integrity checks.

---

### 6. Deposit Pricing & NII Model — £249

Model the net interest income impact of deposit pricing decisions across your product range. Includes product-level rate setting, deposit beta pass-through mechanics, and competitive positioning analysis. Calculates NII sensitivity to base rate changes and quantifies the cost of rate adjustments. Three scenario overlays for strategic pricing decisions. Fully unlocked Excel workbook built for treasury and ALM teams.

---

### 7. Treasury / IRS Model — £299

Value and risk-manage interest rate swaps with full fixed and floating leg cash flow schedules. Includes yield curve construction, discount factor calculation, net MTM valuation, and DV01 sensitivity. Hedge effectiveness testing complies with IFRS 9 / IAS 39 requirements. Outputs include a full P&L impact analysis with three scenario overlays. Fully unlocked Excel workbook designed for treasury desks and ALM teams.

---

### 8. Bond Pricing & Yield Model — £249

Price fixed income securities and calculate a full suite of yield and risk metrics. Covers dirty and clean price, accrued interest, yield to maturity, current yield, Z-spread, duration, and convexity. Supports government bonds, corporate bonds, and floating rate notes. Three scenario overlays with sensitivity to rate movements. Fully unlocked Excel workbook with documentation and print-ready output.

---

### 9. Duration & Rate Sensitivity Model — £249

Measure the interest rate sensitivity of a fixed income portfolio using modified and effective duration, convexity, and key rate durations. Model parallel and non-parallel yield curve shifts and calculate the P&L impact in basis points. Suitable for ALM, treasury, and investment management teams. Three scenario overlays with print-ready sensitivity tables. Fully unlocked Excel workbook with built-in integrity checks.

---

### 10. FX Hedging Model — £249

Map multi-currency exposures across your business and evaluate hedging strategies using forwards, options, and cross-currency swaps. Track hedge costs, effectiveness, and mark-to-market P&L impact over time. Supports transaction, translation, and economic exposure analysis. Three scenario overlays for different rate environments. Fully unlocked Excel workbook designed for corporate treasury and risk teams.

---

### 11. LCR Model — £249

Calculate the Liquidity Coverage Ratio to Basel III / CRD IV standards. Classifies high-quality liquid assets (HQLA) by level with regulatory haircuts, calculates net cash outflows over a 30-day stress period, and produces the LCR ratio with buffer analysis. Suitable for regulatory reporting and ALCO presentations. Three scenario overlays with fully unlocked formulas and built-in integrity checks.

---

### 12. Capital / Regulatory Model — £299

A comprehensive Basel III capital adequacy model covering credit, market, and operational risk RWA. Calculates CET1, Tier 1, and Total Capital ratios with conservation, countercyclical, and systemic buffers. Includes Pillar 2A add-ons, MDA trigger analysis, stress testing under adverse scenarios, and RAROC output. Designed for regulatory reporting and board presentations. Fully unlocked Excel workbook with documentation and integrity checks.

---

### 13. VaR Model — £299

Estimate portfolio Value at Risk using both historical simulation and parametric (variance-covariance) methods. Calculates VaR at 95% and 99% confidence intervals with backtesting validation and stressed VaR under adverse market conditions. Suitable for market risk reporting, ICAAP, and regulatory submissions. Three scenario overlays with fully unlocked formulas. Built for risk teams at banks and investment firms.

---

### 14. Stress Testing Model — £299

Run structured scenario analysis for ICAAP submissions and board-level risk reporting. Covers base, adverse, and severe downside scenarios with impacts quantified across P&L, capital ratios, and liquidity metrics. Includes sensitivity analysis for key risk drivers and produces board-ready summary tables and charts. Three scenario overlays with built-in integrity checks. Designed for CRO offices and regulatory reporting teams.

---

### 15. DCF Valuation Model — £249

A discounted cash flow model with FCFF and FCFE projections, WACC build, and terminal value using both Gordon growth and exit multiple methods. Includes detailed sensitivity tables, scenario analysis, and football field valuation output. Suitable for equity research, M&A advisory, and investment committee presentations. Three scenario overlays with fully unlocked formulas. Print-ready output formatted for professional use.

---

### 16. Trading Comps Model — £199

A comparable company analysis model using EV/EBITDA, P/E, P/B, and EV/Revenue multiples. Includes peer group screening, outlier detection, and implied valuation range output. Designed for equity research analysts, M&A teams, and investment banking associates. Three scenario overlays with print-ready output. Fully unlocked Excel workbook — add your own peers and customise the multiple selection.

---

### 17. Precedent Transactions Model — £199

Analyse M&A deal comparables with transaction multiples including EV/Revenue, EV/EBITDA, and P/E. Includes premium analysis versus undisturbed share price, deal database with filtering, and implied valuation output. Suitable for M&A advisory, pitch books, and fairness opinions. Three scenario overlays with fully unlocked formulas. Professional formatting ready for client presentations.

---

### 18. LBO Model — £299

A leveraged buyout model with sources and uses, multi-tranche debt waterfall, and returns analysis. Calculates IRR and MOIC across multiple exit years with sensitivity tables on entry multiple, exit multiple, and leverage. Includes debt repayment schedules, cash sweep logic, and management equity rollover. Designed for private equity, leveraged finance, and M&A teams. Fully unlocked Excel workbook.

---

### 19. SOTP Valuation Model — £199

A sum-of-the-parts valuation model for conglomerates and diversified businesses. Values each segment using the most appropriate methodology (DCF, trading comps, or asset-based) and bridges to consolidated equity value. Includes holding company discount analysis and scenario overlays. Suitable for equity research, corporate strategy, and investment banking. Fully unlocked Excel workbook with print-ready output.

---

### 20. DDM (Dividend Discount) Model — £199

Value equity using projected dividend streams with a multi-stage growth dividend discount model. Includes cost of equity build via CAPM, payout ratio analysis, and sustainable growth rate calculation. Suitable for banks, insurance companies, utilities, and other dividend-paying sectors. Three scenario overlays with sensitivity on growth and discount rate assumptions. Fully unlocked Excel workbook.

---

### 21. Valuations Model (Multi-Method) — £299

A combined valuation workbook incorporating DCF, trading comps, and precedent transactions in a single integrated model. Produces a football field valuation chart and weighted blended output. Allows you to assign methodology weights and run three scenario overlays. Designed for M&A advisory, pitch books, and investment committee presentations. Fully unlocked with professional formatting and print-ready output.

---

### 22. 3-Statement Integrated Model — £249

A fully linked three-statement financial model with income statement, balance sheet, and cash flow statement. Revenue and cost driver assumptions feed through to all three statements with automatic balancing. Includes ratio analysis output, three scenario overlays, and a built-in CHECKS tab. Suitable for corporate finance, FP&A, and lending analysis. Fully unlocked Excel workbook with documentation.

---

### 23. Budget vs Actual Variance Model — £149

A monthly variance analysis model comparing budget to actual performance with structured commentary fields. Decomposes variances into volume, price, and mix components and tracks year-to-date performance. Designed for finance teams running monthly close and board reporting. Three scenario overlays with print-ready output formatted for management packs. Fully unlocked Excel workbook.

---

### 24. Rolling Forecast Model — £149

A dynamic 12-month rolling forecast model with automatic period roll-forward and actuals lock mechanism. Replaces static annual budgets with a continuously updated view of expected performance. Tracks forecast accuracy and provides trend analysis across rolling windows. Three scenario overlays with built-in integrity checks. Designed for FP&A teams moving to continuous planning. Fully unlocked Excel workbook.

---

### 25. Budget vs Forecast Model — £149

Track forecast accuracy against the original budget with side-by-side comparison of budget, latest forecast, and actuals. Includes variance waterfall charts, bridge analysis, and forecast bias tracking. Helps identify systematic over- or under-forecasting by line item. Three scenario overlays with print-ready output. Designed for FP&A teams and CFO reporting. Fully unlocked Excel workbook.

---

### 26. Cost Control Model — £149

A departmental cost tracking model with cost centre breakdown, headcount analysis, and non-staff cost monitoring. Calculates monthly run-rates, identifies cost savings opportunities, and tracks against budget. Suitable for finance business partners and cost centre managers. Three scenario overlays with variance analysis and print-ready output. Fully unlocked Excel workbook with built-in integrity checks.

---

### 27. Management Accounts Pack — £199

A board-ready management accounts template with P&L, balance sheet, and cash flow summaries. Includes a KPI dashboard with RAG status indicators, trend charts, and commentary sections. Formatted for direct inclusion in board packs with professional layout and A4 landscape printing. Three scenario overlays with built-in integrity checks. Designed for CFO offices and finance teams producing monthly reporting.

---

### 28. Working Capital Model — £149

Analyse and forecast working capital requirements using receivables, payables, and inventory drivers. Calculates cash conversion cycle metrics, identifies improvement opportunities, and sizes working capital facility requirements. Includes seasonal and cyclical adjustments with three scenario overlays. Suitable for treasury, FP&A, and corporate finance teams. Fully unlocked Excel workbook with print-ready output.

---

### 29. Capitalisation Model (IAS 38) — £99

An intangible asset capitalisation model compliant with IAS 38. Tracks research and development phases separately, calculates amortisation schedules by asset class, and includes compliance checks against the recognition criteria. Suitable for technology companies, pharma, and any business capitalising development costs. Three scenario overlays with fully unlocked formulas and print-ready disclosure output.

---

### 30. PPE Model (IAS 16) — £99

A fixed asset register and depreciation model compliant with IAS 16. Supports additions, disposals, and revaluations with straight-line and reducing balance depreciation methods. Produces net book value roll-forwards and disclosure note output. Suitable for finance teams managing property, plant, and equipment accounting. Three scenario overlays with fully unlocked formulas and built-in integrity checks.

---

### 31. Impairment Model (IAS 36) — £99

An impairment testing model compliant with IAS 36. Calculates value-in-use via discounted cash flow and fair value less costs of disposal, allocates impairment to cash-generating units, and tracks subsequent reversals. Produces disclosure-ready output for financial statements and audit files. Three scenario overlays with fully unlocked formulas. Suitable for year-end reporting and audit support.

---

### 32. Capex Model — £149

A capital expenditure planning and tracking model with project-level detail. Covers approval workflows, spend phasing, budget vs actual variance, and forecast to complete. Suitable for finance teams managing multi-project capital programmes. Three scenario overlays with summary dashboards and print-ready output. Fully unlocked Excel workbook with built-in integrity checks.

---

### 33. Debt Schedule Model — £199

A comprehensive debt schedule model with multi-tranche waterfall, covenant testing, and refinancing scenarios. Tests leverage, DSCR, and ICR covenants with breach flagging and cure mechanics. Includes prepayment analysis and refinancing scenario modelling. Suitable for leveraged finance, corporate treasury, and lending teams. Three scenario overlays with fully unlocked formulas and print-ready output.

---

### 34. Debt Amortisation Model — £149

A loan amortisation model supporting bullet, annuity, and sculpted repayment profiles across multiple tranches. Handles fixed and floating rate instruments with interest rate reset logic. Calculates total debt service, applies cash sweep mechanics, and produces summary repayment schedules. Three scenario overlays with built-in integrity checks. Designed for corporate treasury and leveraged finance teams.

---

### 35. Complete LTP Model — £999

A comprehensive Long-Term Plan model covering every aspect of the planning cycle — fully integrated across income, costs, balance sheet, capital, funding, and liquidity projections. Built for CFOs, FP&A heads, and board-level strategic planning at banks and financial institutions. Includes three scenario overlays with board-ready summary outputs, KPI dashboards, and executive reporting. Fully unlocked Excel workbook with documentation, integrity checks, and print-ready formatting. The most complete planning model in the SFS library.

---

## Notes for Lemon Squeezy Setup

- **Currency:** GBP (£) for all products
- **Product type:** Digital download (Excel .xlsx file)
- **Delivery:** Instant download after payment
- **Refund policy:** Non-refundable (free samples available for all models)
- **Tax:** Apply UK VAT rules for digital products
- **Each product should include:** The full Excel workbook + a brief PDF guide (if available)
- **Product images:** Use consistent dark-themed product mockups matching the SFS brand
- **Tags:** Tag each product with its category for filtering (e.g. "Banking & Lending", "Valuation")
