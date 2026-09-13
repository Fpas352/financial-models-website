"""
Build blog posts for sfsmodels.org. Each post targets one long-tail SEO keyword.

Run:
    cd financial-models-website && python3 build_blog_posts.py

Output: HTML files in /blog/.
"""

from pathlib import Path

POSTS = [
    {
        "slug": "mid-year-discounting-dcf",
        "title": "How to Calculate Mid-Year Discounting in a DCF Model",
        "h1": "How to Calculate Mid-Year Discounting in a DCF Model",
        "keyword": "mid year discounting dcf",
        "meta_desc": "Mid-year discounting in DCF models corrects the systematic ~5% under-valuation from end-of-year discounting. Formulas, Excel implementation, common mistakes.",
        "published": "2026-04-21",
        "summary": "End-of-year discounting under-discounts cash flows by half a year of WACC. Mid-year discounting fixes this. Here's the formula, the Excel implementation, and the common mistakes.",
        "product_link": "/dcf-model-excel.html",
        "product_name": "DCF Model Excel Template",
        "body": """<p>If you've built a DCF model in Excel and used standard end-of-year discounting, you're systematically under-valuing the business by approximately half a year of WACC. On a growth business, that's a 5-10% understatement of enterprise value. Mid-year discounting fixes this.</p>

<h2>What is mid-year discounting?</h2>

<p>In a standard DCF, you discount each year's free cash flow (FCF) back to present value using:</p>

<pre><code>PV = FCF / (1 + WACC)^t</code></pre>

<p>Where <code>t</code> is the number of years from the valuation date.</p>

<p>The problem: this formula assumes all of year <code>t</code>'s cash flow arrives on December 31st of year <code>t</code>. In reality, cash flows arrive throughout the year - roughly evenly. The "average" cash arrives at mid-year (June 30th).</p>

<p>Mid-year discounting adjusts for this by discounting cash flows by half a period less:</p>

<pre><code>PV = FCF / (1 + WACC)^(t - 0.5)</code></pre>

<p>For a 5-year forecast at 10% WACC, mid-year discounting gives you ~4.7% higher PV vs end-of-year. On a $1bn EV business, that's $47m of value.</p>

<h2>When to use mid-year vs end-of-year</h2>

<p><strong>Use mid-year when:</strong></p>
<ul>
<li>Cash flows arrive evenly throughout the year (most operating businesses)</li>
<li>You're presenting valuations to investment committees who expect mid-year (standard at most US PE firms)</li>
<li>Public company valuations (most sell-side equity research uses mid-year)</li>
</ul>

<p><strong>Use end-of-year when:</strong></p>
<ul>
<li>Cash flows are heavily back-loaded (project finance, infrastructure concessions where cash arrives at completion milestones)</li>
<li>You're modelling for tax-driven structures where year-end timing matters</li>
<li>The receiving institution has a stated convention (some EU banks default to end-of-year)</li>
</ul>

<h2>The terminal value adjustment</h2>

<p>Most DCF builders forget that mid-year discounting also affects terminal value. Two adjustments:</p>

<p><strong>1. Discount the terminal value back further.</strong></p>

<p>If your explicit forecast ends in year 5 and you've used mid-year discounting for years 1-5, the terminal value (which represents value FROM year 6 onwards) should be discounted at:</p>

<pre><code>TV PV = TV / (1 + WACC)^(5 - 0.5) = TV / (1 + WACC)^4.5</code></pre>

<p>NOT <code>TV / (1 + WACC)^5</code>.</p>

<p><strong>2. The terminal value formula doesn't change.</strong></p>

<p>The Gordon growth formula gives you the value AS OF the end of the explicit forecast period. So whether you use mid-year or end-of-year, the TV formula itself is:</p>

<pre><code>TV = FCF(year n+1) / (WACC - g)</code></pre>

<p>Only the discount factor applied to bring TV back to present value changes.</p>

<h2>Implementing mid-year discounting in Excel</h2>

<p>Add a "discount factor" row to your DCF tab that applies mid-year automatically:</p>

<pre><code>Year:           1     2     3     4     5
FCF:            100   120   140   160   180
Discount factor: 1/(1+WACC)^0.5  1/(1+WACC)^1.5  1/(1+WACC)^2.5  ...

PV = FCF &times; Discount factor</code></pre>

<p>Sum the PVs of years 1-n + discounted terminal value = enterprise value.</p>

<p>For our <a href="/dcf-model-excel.html">DCF Model</a>, we built in a toggle on the INPUTS tab - switch between mid-year and end-of-year and the entire model recalibrates.</p>

<h2>Common mistakes</h2>

<ol>
<li><strong>Discounting terminal value at year n + 1 instead of n.</strong> TV represents value at end of year n, so discount it at year n (or year n &minus; 0.5 for mid-year).</li>
<li><strong>Using mid-year for one year and end-of-year for others.</strong> Be consistent across all years in the explicit forecast.</li>
<li><strong>Ignoring stub periods.</strong> If your valuation date isn't year-end, the first period is a stub (e.g., 7 months). Adjust the discount factor for the stub period accordingly.</li>
<li><strong>Mid-year on a project that ends in year 5.</strong> If the business has a defined termination (project finance), don't use mid-year for the final year - use the actual cash receipt timing.</li>
</ol>

<h2>Free DCF model</h2>

<p>If you want to skip the build, our <a href="/free-sample.html">free DCF Lite</a> has both end-of-year and mid-year discounting available as a switch.</p>

<p>For the full version with three-statement integration, terminal value cross-check, and 8 integrity checks: <a href="/dcf-model-excel.html">DCF Model Excel Template</a>.</p>
""",
    },
    {
        "slug": "deposit-beta-calibration",
        "title": "Deposit Beta in Bank ALM Models: 2022-2025 Calibration",
        "h1": "Deposit Beta in Bank ALM Models: The 2022-2025 Calibration Problem",
        "keyword": "deposit beta calibration",
        "meta_desc": "Deposit beta assumptions calibrated against 2014-2019 are wrong by ~3x for the post-2022 cycle. How to recalibrate by deposit tier and reflect the SVB lessons.",
        "published": "2026-04-21",
        "summary": "Most US bank ALM models use deposit beta from the 2014-2019 cycle. Actual betas in 2022-2025 ran 2-3x higher. The recalibration framework, by tier, with EVE/NII shock implications.",
        "product_link": "/bank-financial-model.html",
        "product_name": "Bank Long-Term Plan Model",
        "body": """<p>Most US bank ALM models still use deposit beta assumptions calibrated against the 2014-2019 rate cycle. The 2022-2025 cycle showed those calibrations were materially wrong. Banks running stale betas understated their NII risk by ~3x heading into the SVB crisis.</p>

<h2>What is deposit beta?</h2>

<p>Deposit beta is the percentage of a base rate (typically Fed Funds for US, Bank Rate for UK) that gets passed through to the rate paid on a deposit product.</p>

<p>If Fed Funds rises 100bps and a savings account rate rises 30bps, the deposit beta is 30%.</p>

<p>Deposit beta varies dramatically by:</p>
<ul>
<li><strong>Product type:</strong> instant access &lt; notice &lt; fixed term</li>
<li><strong>Customer type:</strong> retail &lt; small business &lt; commercial &lt; institutional</li>
<li><strong>Insurance status:</strong> insured (FDIC-covered) &lt; uninsured</li>
<li><strong>Channel:</strong> branch &lt; online &lt; broker</li>
</ul>

<h2>What 2022-2025 changed</h2>

<p>The previous decade (2010-2021) was characterised by ZIRP and modest rate moves. Deposit betas calibrated against this period showed:</p>

<ul>
<li>Retail savings: 20-30%</li>
<li>Commercial deposits: 30-50%</li>
<li>Institutional / brokered: 60-80%</li>
</ul>

<p>When rates rose 525bps over 2022-2023, actual betas were materially higher:</p>

<ul>
<li>Retail savings: 35-50% (up from 20-30%)</li>
<li>Commercial deposits: 70-90% (up from 30-50%)</li>
<li>Uninsured commercial: 80-95% (the SVB cohort)</li>
</ul>

<p>The reason: depositors had access to better rate alternatives (T-bills, money market funds yielding 5%+) and digital channels made it easy to move money.</p>

<h2>Why this matters for ALM models</h2>

<p>ALM models project NII under interest rate scenarios. Two key levers:</p>

<ol>
<li>Asset side: how fast do loan yields reprice</li>
<li>Liability side: how fast do deposit rates reprice (driven by deposit beta)</li>
</ol>

<p>If your model assumes 30% beta when actual beta is 80%, in a +200bps shock your modelled NII is materially overstated. Your EVE / NII shock numbers are similarly distorted.</p>

<p>For the 2022-23 cycle, banks running 2019-vintage betas were modelling NII benefits of ~10-15%. Actual NII benefits were closer to 3-5% - and for some banks (those with high uninsured commercial mix), NII actually compressed.</p>

<h2>How to recalibrate</h2>

<p><strong>1. Segment deposits by beta tier.</strong></p>

<p>Don't average across the whole book. Split into:</p>
<ul>
<li>Insured retail (low beta)</li>
<li>Insured commercial (medium beta)</li>
<li>Uninsured commercial (high beta)</li>
<li>Brokered / wholesale (highest beta)</li>
</ul>
<p>Each gets its own beta assumption.</p>

<p><strong>2. Use 2022-2025 actuals as base case.</strong></p>

<p>Calibrate against your bank's actual experience over the rising rate cycle. Don't blend with pre-2022 data - the rate environment was structurally different (digital access, money market yields, etc.).</p>

<p><strong>3. Flex beta in scenarios.</strong></p>

<p>Base case = 2022-2025 actuals. Adverse scenario = 1.2x base (faster pass-through under stress). Severely adverse = 1.5x base (run-off scenario).</p>

<p><strong>4. Re-calculate EVE / NII shock.</strong></p>

<p>Re-run your standard shock scenarios (+200bps parallel, etc.) with new betas. Expect your numbers to look materially worse than the previous cycle's output. That's the point - the previous cycle's output was wrong.</p>

<h2>What about the deposit beta floor?</h2>

<p>Some banks model a "floor" beta below which the deposit rate doesn't fall in a falling rate environment. For example, retail savings rates might have a 0.10% floor regardless of how low Fed Funds goes.</p>

<p>The floor matters in falling-rate scenarios. If you model 30% beta on the way up but ignore the floor on the way down, your NII benefit in a rate cut scenario is overstated.</p>

<p>For a complete bank long-term plan model that handles deposit beta tiering, EVE / NII shock, and floor logic, see our <a href="/bank-financial-model.html">Bank Long-Term Plan Model</a>.</p>

<h2>What to do if you can't recalibrate immediately</h2>

<p>If your ALM model is stuck on old betas and a recalibration is months away, the interim hack: apply a "beta haircut" to your modelled NII benefit.</p>

<p>For US regional banks, halving the modelled NII shock benefit gets you roughly to where the recalibrated number would land. Not perfect, but better than presenting a number you know is wrong.</p>
""",
    },
    {
        "slug": "stop-using-indirect-excel",
        "title": "INDIRECT() in Excel: Why You Should Stop Using It",
        "h1": "INDIRECT() in Excel: Why You Should Stop Using It",
        "keyword": "excel indirect alternative",
        "meta_desc": "INDIRECT() is volatile, breaks silently when sheets are renamed, and can't be traced. Four alternatives by use case for cleaner financial models.",
        "published": "2026-04-21",
        "summary": "INDIRECT() is the most overused finance modelling function. Three specific problems and four alternatives by use case.",
        "product_link": "/models.html",
        "product_name": "SFS Models Catalogue",
        "body": """<p>INDIRECT() is one of those small Excel modelling habits that causes outsized pain when models get inherited. It's convenient for building flexible references - <code>=INDIRECT("'"&amp;A1&amp;"'!B5")</code> - but it has three properties that should disqualify it from any model that anyone other than the original builder will use.</p>

<h2>1. It's volatile</h2>

<p>Every recalculation re-evaluates every INDIRECT in the workbook. On a 50-tab model with 200 INDIRECT calls, this is the difference between a 0.5s recalc and a 30s recalc. Volatile functions also trigger recalculation when totally unrelated cells change, which makes audits painful.</p>

<h2>2. It breaks silently when sheets are renamed</h2>

<p>No #REF! error. Just wrong numbers. The user has no idea anything went wrong - the formula still "works", it just points at nothing now and returns 0 or #REF! that's lost in a sea of other values.</p>

<h2>3. It can't be traced</h2>

<p>F2 doesn't show you what cell INDIRECT is pointing at. F5 &rarr; Special &rarr; Precedents doesn't follow it. You have to mentally evaluate the string concatenation to figure out where the reference goes. In a model audit, this is hours of additional work per page.</p>

<h2>What to use instead</h2>

<p><strong>For cross-sheet references where the sheet is fixed:</strong></p>
<p>Just use a normal reference. <code>='Lending'!B5</code>. No INDIRECT needed.</p>

<p><strong>For lookups across multiple sheets where the sheet name varies:</strong></p>
<p>Use a single consolidation tab that pulls all sheets via fixed references, then INDEX/MATCH against the consolidation. One layer of indirection, fully traceable.</p>

<p><strong>For "sometimes show this, sometimes show that":</strong></p>
<p>CHOOSE or INDEX with a switch cell. Both traceable. Both non-volatile.</p>

<pre><code>=CHOOSE(MATCH(scenario_cell, {"Base","Upside","Downside"}, 0),
        Base_value, Upside_value, Downside_value)</code></pre>

<p><strong>If you genuinely need a dynamic sheet reference (rare):</strong></p>
<p>Build a helper column with the actual values and INDEX/MATCH against that. Avoid INDIRECT.</p>

<h2>The general principle</h2>

<p>In a model that other people will inherit, traceability beats convenience every time. Anything that breaks F5 &rarr; Special &rarr; Precedents is a future bug factory.</p>

<p>For our entire <a href="/models.html">model catalogue</a>, we have a hard rule: no INDIRECT, no INDIRECT.EXT, no OFFSET (similarly volatile and untraceable). Every reference is either direct or via INDEX/MATCH against a fixed range.</p>

<p>It takes 5% more upfront work and saves 50% of audit time. Always worth it.</p>
""",
    },
    {
        "slug": "ccar-stress-capital-buffer-2026",
        "title": "The CCAR Stress Capital Buffer Trap for the 2026 Cycle",
        "h1": "The CCAR Stress Capital Buffer Trap for the 2026 Cycle",
        "keyword": "stress capital buffer ccar",
        "meta_desc": "The 2026 CCAR cycle introduces revised SCB rules that make dividends a binding capital input. Most regional banks haven't updated their models. What changes and how to fix it.",
        "published": "2026-04-22",
        "summary": "Revised SCB rules for the 2026 CCAR cycle make planned dividends a binding input to capital adequacy. Most regional bank models still treat dividends as a pure use of capital. Here's what changes and what to fix.",
        "product_link": "/bank-stress-test-model.html",
        "product_name": "Bank Stress Test Model",
        "body": """<p>The 2026 CCAR cycle is the first under the revised stress capital buffer (SCB) rules. Most US regional banks are still running their 2024 framework. The gap between the two will show up at the next examination cycle.</p>

<h2>What is the Stress Capital Buffer?</h2>

<p>The SCB is the bank-specific buffer above the regulatory minimum CET1 ratio (4.5%) plus the global capital conservation buffer (2.5%). For US banks subject to CCAR, the SCB is calibrated based on the bank's projected capital decline under the supervisory severely adverse scenario.</p>

<p>SCB = Maximum projected capital decline + 4 quarters of planned common stock dividends.</p>

<p>That last component - planned dividends - is what changed for 2026.</p>

<h2>What changed for 2026</h2>

<p>Under the previous methodology, planned dividends in the SCB calculation were measured as a static four-quarter sum at submission time. Under the revised methodology, the four-quarter dividend sum is calculated dynamically across the stress horizon.</p>

<p>The practical effect: as your projected dividends change quarter-by-quarter under stress, your SCB recalibrates. Higher dividends = larger SCB = higher minimum CET1 you must maintain.</p>

<p>This makes dividends a <strong>binding input to capital adequacy</strong>, not just a use of capital. If your model treats dividends as a flow to be subtracted from CET1 each quarter (the standard approach), you're missing the buffer feedback loop.</p>

<h2>What breaks in most internal models</h2>

<p>Three patterns we see consistently when reviewing regional bank stress test models:</p>

<ol>
<li><strong>Dividends modelled as a pure use of capital.</strong> Each quarter, dividends reduce CET1. The SCB is a separate input on the capital ratio tab. The two don't talk to each other.</li>
<li><strong>SCB modelled as a single static add-on.</strong> The buffer is a number entered on INPUTS and held constant across the stress horizon. Quarter-by-quarter recalculation isn't built in.</li>
<li><strong>PPNR projections still using 2018-vintage models.</strong> Pre-COVID rate environments don't tell you anything useful about 2024-26. Net interest margin under stress in the new regime depends heavily on deposit beta calibration (see <a href="/blog/deposit-beta-calibration.html">our piece on deposit beta</a>).</li>
</ol>

<h2>The fix: quarterly SCB recalculation</h2>

<p>The model structure that handles the new methodology:</p>

<ul>
<li><strong>One INPUTS tab</strong> with quarterly dividend assumptions (not annual aggregate)</li>
<li><strong>One CAPITAL_ACTIONS tab</strong> calculating the rolling 4-quarter dividend sum at each quarter</li>
<li><strong>One SCB tab</strong> calculating the SCB at each quarter as: max projected capital decline (across remaining horizon from this quarter) + rolling 4-quarter dividend sum</li>
<li><strong>One CAPITAL_RATIOS tab</strong> calculating CET1 ratio against the time-varying SCB-inclusive minimum</li>
<li><strong>MDA logic</strong> that auto-restricts dividends when the CET1 ratio falls below P1 + buffers, which then feeds back into the SCB calculation in the next iteration</li>
</ul>

<p>The feedback loop between dividends and SCB is what makes the new methodology operationally complex. Done right, the model converges quickly. Done wrong (using iterative calculation), it spirals.</p>

<p>Our trick: model the MDA restriction as a function of <em>prior quarter's</em> capital ratio, not current. This breaks the circularity cleanly. Same principle as our universal "no circularities" rule for bank models.</p>

<h2>Walked example: $50bn regional bank</h2>

<p>Consider a $50bn regional bank planning $1.2bn in annual dividends ($300m/quarter).</p>

<p><strong>Under old methodology:</strong> SCB calculation includes $1.2bn dividend addition. Maximum projected CET1 decline (say 250bps over 9 quarters) drives a buffer of, say, 3.5%.</p>

<p><strong>Under new methodology:</strong> at each quarter, the rolling 4-quarter dividend sum is recalculated. If projected stress causes dividend cuts (per MDA), the SCB declines - but lagging the actual decline. The bank may face a higher SCB during the recovery phase than under the old methodology.</p>

<p>Practical impact: the bank's modelled CET1 decline may now breach the 5.125% AT1 trigger floor when it didn't under the old framework. That's a material capital plan change that needs to land before the 2026 cycle, not during it.</p>

<h2>What to do now</h2>

<ol>
<li><strong>Audit your current capital plan model.</strong> Search for "SCB" in formulas. If it appears as a static cell on INPUTS, you're on the old methodology.</li>
<li><strong>Rebuild capital_actions and SCB calculations as quarterly time series.</strong> Don't shortcut to annual.</li>
<li><strong>Recalibrate PPNR.</strong> Use 2022-2025 actuals as the base, not 2018-2019.</li>
<li><strong>Recalibrate deposit beta.</strong> The 2022-23 cycle showed actual betas were 2-3x your old assumptions. See <a href="/blog/deposit-beta-calibration.html">deposit beta calibration</a>.</li>
<li><strong>Run the model end-to-end on the 2025 supervisory severely adverse scenario.</strong> If your output looks materially worse than your 2024 submission, you're calibrated correctly. If it looks the same, something's wrong.</li>
</ol>

<h2>The model that handles this</h2>

<p>Our <a href="/bank-stress-test-model.html">Bank Stress Test Model</a> is built for the new methodology natively - quarterly SCB recalculation, dividend-as-input, recalibratable PPNR, MDA feedback loop. Tested against the 2025 supervisory severely adverse scenario.</p>
""",
    },
    {
        "slug": "cecl-methodology-drift",
        "title": "Why Most CECL Models Drift After Year 2 (And How to Fix It)",
        "h1": "Why Most CECL Models Drift After Year 2 (And How to Fix It)",
        "keyword": "cecl methodology drift",
        "meta_desc": "CECL went live for SEC filers in 2020. Five years later, most US bank methodologies have quietly drifted away from regulatory expectations. The four drift patterns examiners are flagging and how to fix each.",
        "published": "2026-04-22",
        "summary": "CECL adoption was 2020. Five years on, methodologies have drifted. Examiners are flagging four specific patterns: stale R&S forecast horizons, undefended reversion paths, ungrounded Q-factors, and outdated pool segmentation. How to fix each.",
        "product_link": "/ifrs9-cecl-model-excel.html",
        "product_name": "IFRS 9 / CECL ECL Model",
        "body": """<p>CECL (ASC 326) went live for SEC filers in 2020 and for non-SEC filers in 2023. Most banks built their methodology in the adoption window and haven't materially refreshed it since. That's a problem - OCC and FDIC examiners are now flagging methodology drift as a systemic issue, particularly at regional banks with CRE concentration.</p>

<h2>The four drift patterns</h2>

<h3>1. Reasonable & Supportable forecast horizon hasn't been re-justified</h3>

<p>CECL requires a Reasonable &amp; Supportable (R&amp;S) forecast period - the window over which you can defensibly project macro variables. After R&amp;S, you revert to historical loss rates.</p>

<p>Most banks picked 1-2 years at adoption and haven't revisited it. In 2020, with COVID uncertainty, 1 year was defensible. In 2026, with a clearer macro outlook, you might justify 2-3 years - but you must document why.</p>

<p><strong>Examiner flag:</strong> "Why is your R&amp;S period still 1 year? What changed since adoption to justify the same window?" If you don't have a written answer, you have a finding.</p>

<p><strong>Fix:</strong> annual R&amp;S period review, board-approved. Document the macro backdrop justification each year.</p>

<h3>2. Reversion path is an Excel formula nobody can defend</h3>

<p>After the R&amp;S period, you must revert from forecast loss rates to historical mean. Most banks implemented this as a linear interpolation in Excel and never wrote the methodology document.</p>

<p>The reversion path matters: a steep reversion in year 2 vs a gentle reversion over years 2-5 produces materially different lifetime ECL.</p>

<p><strong>Examiner flag:</strong> "Show me the methodology document for your reversion path. Why linear vs exponential? Why over this duration?"</p>

<p><strong>Fix:</strong> document the reversion methodology explicitly. Common defensible approaches:</p>
<ul>
<li>Linear over R&amp;S+1 to year 5 (simple, defensible if no specific macro view)</li>
<li>Exponential decay (industry-standard for some portfolios)</li>
<li>Step-function aligned to forecast cycles (e.g., revert at end of forecast)</li>
</ul>

<h3>3. Q-factor adjustments don't tie to specific defensible signals</h3>

<p>The Q-factor (qualitative adjustment) is where most banks bury the macro overlay. The amount is defensible only if it ties to a specific external signal.</p>

<p>"Macro deterioration" isn't a number. "+10bps to allowance reflecting CRE office vacancy increase from 14% to 19% per CBRE Q4 2025 report" is a number.</p>

<p><strong>Examiner flag:</strong> "What's the source for your +5bps Q-factor on the C&amp;I book?" If you can't cite an external data source, the Q-factor will be challenged.</p>

<p><strong>Fix:</strong> every Q-factor entry must have:</p>
<ul>
<li>An external data source (Fed, Bloomberg, CBRE, BLS, etc.)</li>
<li>A documented rule connecting the data signal to the Q-factor magnitude</li>
<li>Evidence of historical back-testing (does the rule produce sensible numbers in past cycles?)</li>
</ul>

<h3>4. Pool segmentation hasn't evolved with portfolio mix</h3>

<p>Your 2020 CRE pool segmentation (owner-occupied / income-producing / construction) may have been adequate then. In 2026, with the office sector deterioration creating a wholly different risk profile, you might need to subdivide income-producing into office / multifamily / retail / industrial.</p>

<p><strong>Examiner flag:</strong> "Why is your office CRE pooled with multifamily?" If you don't have a defensible reason, that's a finding.</p>

<p><strong>Fix:</strong> annual segmentation review. If a sub-segment has materially different risk characteristics from the parent pool, separate it.</p>

<h2>The annual methodology refresh framework</h2>

<p>Build this into your CECL governance:</p>

<ol>
<li><strong>Annual R&amp;S period review</strong> - 1 page, board-approved, justifies the chosen horizon</li>
<li><strong>Annual reversion methodology review</strong> - 1 page, justifies the chosen reversion shape and duration</li>
<li><strong>Quarterly Q-factor review</strong> - line-by-line update of each Q-factor with external data citation</li>
<li><strong>Annual pool segmentation review</strong> - assesses whether the current pools are still risk-coherent</li>
<li><strong>Annual back-test</strong> - compares the prior year's allowance against actual losses, identifies methodology gaps</li>
</ol>

<p>This isn't optional. Examiners explicitly ask for the documentation. If it doesn't exist, you have a finding.</p>

<h2>The model that supports this</h2>

<p>Our <a href="/ifrs9-cecl-model-excel.html">IFRS 9 / CECL ECL Model</a> builds in the documentation framework: Q-factor cells include source citation columns, R&amp;S and reversion parameters live in a single methodology tab, and pool segmentation is rebuildable without breaking the calculation layer.</p>

<p>Audit-ready by construction. Methodology document is the same workbook you use to compute the allowance.</p>
""",
    },
    {
        "slug": "python-openpyxl-financial-model",
        "title": "Building Financial Models Programmatically with Python and openpyxl",
        "h1": "Building Financial Models Programmatically with Python and openpyxl",
        "keyword": "openpyxl financial model",
        "meta_desc": "How we build 18 institutional-grade Excel financial models programmatically using Python and openpyxl. Patterns, gotchas, and the standard helper library.",
        "published": "2026-04-22",
        "summary": "Hand-edited Excel models are unmaintainable at scale. Python + openpyxl makes the build script the source of truth. Here's our standard pattern: helpers, named ranges, the no-circularity rule, and how we validate all 18 models in one command.",
        "product_link": "/models.html",
        "product_name": "SFS Models Catalogue",
        "body": """<p>Every financial model in our catalogue is generated by a Python script using openpyxl. We never edit the .xlsx files by hand. The build script is the source of truth.</p>

<p>This isn't a hipster tooling choice - it's the only way to maintain a catalogue of 18 institutional-grade models without going insane. Here's the pattern.</p>

<h2>Why scripts as source of truth</h2>

<p>Hand-edited Excel files have four problems at scale:</p>

<ol>
<li><strong>No version control</strong>. Git can store .xlsx but can't diff it. You can see <em>that</em> the file changed but not <em>what</em> changed.</li>
<li><strong>Style drift</strong>. Five models, five slightly different formats. Looks unprofessional.</li>
<li><strong>Cascading bugs</strong>. Fix a formula in one model, forget to fix it in the other 17.</li>
<li><strong>No testing</strong>. You can't unit-test a hand-edited Excel file. You can unit-test a Python script that generates one.</li>
</ol>

<p>Build scripts solve all four. Each model has a build_<em>name</em>_v<em>n</em>.py file. Run the script, get the .xlsx. Change the script, regenerate. Commit the script to git.</p>

<h2>The standard helper library</h2>

<p>Every build script imports the same set of helpers:</p>

<pre><code class="language-python">from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.workbook.defined_name import DefinedName

# Style constants
NAVY       = "1F3864"
MID_BLUE   = "2E75B6"
WHITE      = "FFFFFF"
BLUE_FONT  = "0000FF"   # hardcoded inputs
BLACK_FONT = "000000"   # formulas
YELLOW_BG  = "FFFDE7"   # input cell fill
GREEN_PASS = "C6EFCE"   # CHECKS pass
RED_FAIL   = "FFC7CE"   # CHECKS fail
GREEN_TOT  = "E2EFDA"   # total row fill

# Number formats
FMT_GBP    = '#,##0;(#,##0);"-"'
FMT_GBPm   = '#,##0.0,,"m";(#,##0.0,,"m");"-"'
FMT_PCT    = '0.0%;(0.0%);"-"'
FMT_BPS    = '0" bps";(0" bps");"-"'
FMT_DATE   = 'mmm-yy'

def inp(ws, row, col, value, fmt=FMT_GBP):
    # Hardcoded input cell: blue font, yellow fill.
    c = ws.cell(row=row, column=col, value=value)
    c.font = Font(name="Arial", size=10, color=BLUE_FONT)
    c.fill = PatternFill("solid", fgColor=YELLOW_BG)
    c.number_format = fmt
    return c

def calc(ws, row, col, formula, fmt=FMT_GBP):
    # Formula cell: black font, no fill.
    c = ws.cell(row=row, column=col, value=formula)
    c.font = Font(name="Arial", size=10, color=BLACK_FONT)
    c.number_format = fmt
    return c

def label(ws, row, col, text, indent=0, bold=False):
    # Text label cell.
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(name="Arial", size=10, bold=bold)
    c.alignment = Alignment(horizontal="left", indent=indent)
    return c

def section_header(ws, row, col_start, col_end, text):
    # Dark navy section header.
    c = ws.cell(row=row, column=col_start, value=text)
    c.font = Font(name="Arial", size=10, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=NAVY)
    for col in range(col_start + 1, col_end + 1):
        ws.cell(row=row, column=col).fill = PatternFill("solid", fgColor=NAVY)
    return c
</code></pre>

<p>Three functions handle 80% of cell creation: <code>inp()</code> for hardcoded inputs (blue/yellow), <code>calc()</code> for formulas (black, no fill), <code>label()</code> for text. Consistency across all 18 models comes for free.</p>

<h2>Common openpyxl gotchas</h2>

<h3>Named ranges API changed</h3>

<p>The old <code>wb.defined_names.definedName</code> API is deprecated. Use string-key iteration:</p>

<pre><code class="language-python"># CORRECT
for name in wb.defined_names:
    dn = wb.defined_names[name]

# WRONG (raises AttributeError in current openpyxl)
for dn in wb.defined_names.definedName:
    ...
</code></pre>

<h3>Formulas are strings, not evaluated</h3>

<p>openpyxl writes formula strings to cells but doesn't evaluate them. The cell's value when read back is the formula text, not the result. To get evaluated values, you need to either:</p>

<ul>
<li>Open the file in Excel/LibreOffice (which triggers recalc on save)</li>
<li>Run the file through <code>libreoffice --headless --convert-to xlsx</code> to force recalc</li>
<li>Use a separate library like <code>pycel</code> (limited support) or <code>formulas</code> (better but slow)</li>
</ul>

<p>Our validation pipeline runs every model through headless LibreOffice to force recalc, then reads the values back. Catches formula bugs before shipping.</p>

<h3>Performance with large workbooks</h3>

<p>openpyxl in default (cell-by-cell) mode is slow for large workbooks. For models with &gt;10,000 formula cells, use write-only mode or batch the cell creation.</p>

<p>Bigger payoff: avoid creating empty cells. openpyxl tracks every accessed cell, so even reading <code>ws.cell(row=1000, col=1)</code> in an empty area inflates the file. Only touch cells you intend to populate.</p>

<h2>The no-circularity rule</h2>

<p>The hardest discipline in financial modelling: avoiding circular references.</p>

<p>The classic case in banking: interest income depends on the loan balance, but the loan balance depends on interest income (interest gets capitalised, or the cash book grows from interest received).</p>

<p>The naive fix - turn on Excel's iterative calculation - works but creates a brittle model. Audit teams reject models that depend on iterative calculation because they can produce different results based on iteration count.</p>

<p>The clean fix: <strong>always reference prior period balance, never current</strong>.</p>

<pre><code class="language-python"># Cell layout: opening, drawdown, repayment, interest, closing
# For row 12 (period 2):
calc(ws, 12, 5, '=I11')              # opening = prior closing
calc(ws, 12, 8, '=E12*rate/12')      # interest on opening
calc(ws, 12, 9, '=E12+F12-G12+H12')  # closing = opening + flows + interest
</code></pre>

<p>This pattern works for: lending interest, deposit interest, capital constraints (current period capital from prior period), provision charges. Circular by reference, sequential by construction.</p>

<h2>Validation: the CHECKS tab</h2>

<p>Every model has a CHECKS tab with 30-40 integrity tests:</p>

<ul>
<li>BS balances (assets = liabilities + equity)</li>
<li>CF closing ties to BS cash</li>
<li>Debt schedule closing ties to BS debt</li>
<li>Total interest from debt schedule = total interest in IS</li>
<li>Scenario switches working (Upside &gt; Base on key metrics)</li>
<li>No negative equity in Base scenario</li>
</ul>

<p>Each check returns "PASS" or "FAIL" with conditional formatting (green/red). The whole catalogue is validated by:</p>

<pre><code class="language-bash">cd models &amp;&amp; python3 validate_all.py</code></pre>

<p>If any model has a failing CHECK, the build fails. Catches bugs before shipping.</p>

<h2>The full pipeline</h2>

<ol>
<li>Edit build_<em>name</em>_v<em>n</em>.py</li>
<li>Run <code>python3 build_<em>name</em>_v<em>n</em>.py</code> - outputs .xlsx</li>
<li>Run <code>python3 validate_all.py</code> - opens each .xlsx through LibreOffice headless and reads CHECKS tab</li>
<li>If validation passes, commit the build script + .xlsx to git</li>
<li>Push - CI rebuilds and re-validates as a sanity check</li>
</ol>

<p>This is how we ship 18 institutional-grade models with two engineers (effectively just me) and zero production bugs in 18 months.</p>

<h2>Should you do this?</h2>

<p>If you're building 1-2 financial models, no - openpyxl is overkill, just use Excel directly.</p>

<p>If you're building 5+ models that share styling, structure, or reusable calculations, yes - the upfront investment in helpers pays back within the third model.</p>

<p>Our entire <a href="/models.html">catalogue of 18 models</a> uses this approach. If you're curious about the helper library or have specific openpyxl questions, ping us via <a href="/contact.html">contact</a>.</p>
""",
    },
    {
        "slug": "lbo-model-debt-sizing",
        "title": "LBO Model Debt Sizing: How to Structure the Debt Stack",
        "h1": "LBO Model Debt Sizing: How to Structure the Debt Stack",
        "keyword": "lbo model debt sizing",
        "meta_desc": "How to size the debt stack in an LBO model. Senior debt, mezzanine, PIK, DSCR constraints, leverage multiples, and the debt sculpting mechanics PE firms actually use.",
        "published": "2026-05-07",
        "summary": "Debt sizing in an LBO model is not a single calculation - it's an iterative constraint problem with credit ratios, leverage multiples, and coverage tests all biting at once. Here's how PE professionals actually structure the debt stack.",
        "product_link": "/lbo-model-excel.html",
        "product_name": "LBO Model Excel Template",
        "body": """<p>Most LBO model tutorials start with a fixed debt amount and work backwards to returns. In practice, the debt stack is determined by constraints - and identifying which constraint bites first is the core of the debt sizing exercise.</p>

<h2>The four debt sizing constraints</h2>

<p>Every leveraged buyout is constrained by at least one of these four limits. Often two or three bind simultaneously:</p>

<ol>
<li><strong>Leverage multiple</strong> - Senior lenders quote a maximum Debt / EBITDA (e.g. 4.5x senior, 6.0x total). This gives you the headline quantum.</li>
<li><strong>DSCR floor</strong> - Lenders require minimum debt service coverage (typically 1.10x-1.25x). In Year 1, stressed EBITDA minus capex must cover P&amp;I payments.</li>
<li><strong>Fixed charge coverage</strong> - Similar to DSCR but includes finance leases, rent, and sometimes management fees.</li>
<li><strong>Equity minimum</strong> - Most PE deals require 30-40% equity as a minimum. Regulatory capital (for financial institution targets) can push this higher.</li>
</ol>

<h2>Building the debt schedule in order</h2>

<p>The correct build sequence is: senior debt first, then mezzanine/subordinated, then PIK/seller notes. Each layer is sized against what the coverage ratios allow after the prior layer.</p>

<h3>Step 1: Senior term loan (TLB)</h3>

<pre><code>Senior debt = MIN(
    Entry EBITDA × Senior leverage cap,
    (EBITDA - Capex - Tax) / DSCR floor × (1 / annual P+I %)
)</code></pre>

<p>The second term is often harder to calculate because P+I % depends on the debt quantum (circular). Solve by iteration: start at the leverage cap and step down until DSCR clears.</p>

<h3>Step 2: Revolving credit facility (RCF)</h3>

<p>The RCF sits pari passu with the TLB but is typically excluded from the leverage calculation at close (drawn = 0). Size it as 0.5-1.0x EBITDA for operational liquidity. The RCF tightens the effective DSCR through its commitment fee, which is a fixed charge regardless of drawdown.</p>

<h3>Step 3: Mezzanine / unitranche</h3>

<p>After senior is maxed, test whether adding a mezzanine tranche is feasible. Mezzanine lenders look at total leverage (typically cap at 6.0-7.0x in today's market) and interest coverage (EBITDA / total interest &ge; 2.0x). PIK mezzanine is tested on cash coverage only (excluding PIK coupon), which is why sponsors prefer it when coverage is tight.</p>

<h3>Step 4: Seller note / PIK toggle</h3>

<p>Any remaining valuation gap is filled with seller paper (PIK or deferred cash). Seller notes typically sit outside the restricted group covenants, making them effectively equity-like from the senior lender perspective.</p>

<h2>The debt schedule mechanics</h2>

<p>The critical modelling rule: calculate interest on the opening balance, not the closing balance. Using closing balance creates a circular reference. The correct formula for each period:</p>

<pre><code>Opening balance  = Prior period closing
Scheduled repayment = Amortisation schedule (% or fixed)
Cash sweep       = Excess free cash flow above mandatory debt service
Interest charge  = Opening balance × (rate / 12)
Closing balance  = Opening + Drawdown - Repayment - Sweep</code></pre>

<p>The cash sweep is where most LBO models get it wrong. The sweep applies to free cash flow after mandatory P&amp;I, before dividends, but after capex and working capital. The sweep rate (50%, 75%, 100%) is negotiated - build it as a INPUTS parameter, not a hardcode.</p>

<h2>Covenant headroom testing</h2>

<p>Three covenant tests to build into the model alongside the debt schedule:</p>

<table>
<thead><tr><th>Covenant</th><th>Typical threshold</th><th>Test formula</th></tr></thead>
<tbody>
<tr><td>Net leverage</td><td>&le; 5.5x</td><td>Net Debt / LTM EBITDA</td></tr>
<tr><td>Interest cover</td><td>&ge; 2.0x</td><td>LTM EBITDA / LTM Cash Interest</td></tr>
<tr><td>Fixed charge cover</td><td>&ge; 1.1x</td><td>(EBITDA - Capex - Tax) / (P&amp;I + Leases)</td></tr>
</tbody>
</table>

<p>Flag a breach (FAIL) if any covenant threshold is breached in any period. Build this into your CHECKS tab with RAG formatting so a breach is immediately visible.</p>

<h2>What changes the returns more than anything else</h2>

<p>Sensitivity analysis almost always shows the same result: entry multiple and exit multiple dwarf everything else in their impact on IRR. But debt sizing affects the equity cheque, which determines how hard the leverage effect works.</p>

<p>The mechanical relationship: for every 1.0x of additional leverage at entry (holding purchase price constant), equity invested decreases proportionally. On a 5-year hold with flat EBITDA, 1.0x extra leverage adds approximately 300-500bps to IRR, before interest cost drag.</p>

<p>Above the DSCR floor, the limit on leverage is almost always the senior lender's leverage cap - not the economics. The economics almost always want more debt than the credit market will provide.</p>

<h2>Building this in Excel</h2>

<p>The debt schedule should have one row per tranche, one column per period. Build it bottom-up:</p>

<ol>
<li>INPUTS tab: all covenant thresholds, leverage caps, interest rates, amortisation %, cash sweep %</li>
<li>Debt schedule tab: tranche-by-tranche roll-forward with interest and repayment</li>
<li>Covenant check tab: test each covenant each period, flag any breach</li>
<li>Returns tab: equity bridge from entry to exit using debt paydown + EBITDA growth + multiple</li>
</ol>

<p>Our <a href="/lbo-model-excel.html">LBO Model</a> covers all of this - senior TLB, RCF, mezzanine, PIK, covenant testing, cash sweep, and equity returns waterfall. Open formulas, no VBA.</p>
""",
    },
    {
        "slug": "wacc-calculation-banking",
        "title": "WACC for Banks: Why the Standard Formula Breaks Down",
        "h1": "WACC for Banks: Why the Standard Formula Breaks Down",
        "keyword": "wacc calculation for banks",
        "meta_desc": "WACC doesn't work for banks. Why the textbook formula breaks down for financial institutions, what to use instead, and how to value a bank correctly.",
        "published": "2026-05-07",
        "summary": "The textbook WACC formula assumes debt is a funding choice. For banks, debt (deposits) is the product. This one difference invalidates WACC for bank valuation - and most analysts apply it anyway.",
        "product_link": "/bank-financial-model.html",
        "product_name": "Bank Long-Term Plan Model",
        "body": """<p>The WACC formula works by weighting the cost of each funding layer against its proportion of total capital. The insight is that debt is cheaper than equity (because interest is tax-deductible and debt ranks senior), so optimal capital structure includes some leverage.</p>

<p>For non-financial companies, this is clean. A manufacturing business borrows to fund plant and equipment. The amount it borrows is a financing decision, separate from what it does with the money.</p>

<p>For banks, this distinction collapses entirely. Here's why.</p>

<h2>The bank problem: debt is the product</h2>

<p>A bank's "debt" is overwhelmingly customer deposits. Those deposits are not a funding choice - they are the product. The bank takes in deposits, pays a rate, and lends them out at a higher rate. The spread is the business.</p>

<p>If you apply WACC to a bank, you're saying: deposits are cheap funding that creates a tax shield, and the bank should optimise its debt-to-equity ratio to minimise WACC. But the bank cannot choose to have fewer deposits (or more) for its WACC. The deposit base is a function of the business - customers, rates, products, competition. It is not a capital structure decision.</p>

<p>The second problem: WACC-based DCF discounts free cash flow to the firm (FCFF). FCFF = EBIT(1-t) + D&amp;A - Capex - Working capital change. For a bank, &ldquo;working capital change&rdquo; includes changes in loans, deposits, securities - i.e., the entire balance sheet. The resulting FCFF is near-zero in a growing bank (all cash flow is reinvested into the loan book) and wildly volatile.</p>

<h2>What bank analysts use instead</h2>

<p>Three methodologies dominate bank valuation:</p>

<h3>1. Dividend Discount Model (DDM)</h3>

<p>Discount dividends (or distributable earnings) to equity at the cost of equity only - not WACC. This sidesteps the debt problem entirely by valuing equity directly.</p>

<pre><code>Value of equity = D₁ / (Ke - g)</code></pre>

<p>Where <code>D₁</code> is next year's expected dividend, <code>Ke</code> is cost of equity, and <code>g</code> is the long-run dividend growth rate.</p>

<p>For banks in a steady state with consistent payout ratios, this gives sensible results. The problem: few banks are in steady state. Regulatory capital requirements, balance sheet growth, and stress test buffers all create lumpy dividend capacity that breaks the Gordon Growth assumption.</p>

<h3>2. Excess Returns Model</h3>

<p>Value = Book equity + PV of excess returns</p>

<p>Where excess return = (ROE - Ke) × Book equity each period.</p>

<p>This is theoretically elegant: a bank trading at 1.0x book has no excess returns in the market's view. A bank at 2.0x book is expected to generate sustainable ROE above its cost of equity. It avoids the deposit/debt confusion because you never calculate FCFF - you work directly from equity returns.</p>

<h3>3. Price-to-Tangible Book Value (P/TBV)</h3>

<p>Not a DCF at all - a market multiples approach. P/TBV is the dominant bank valuation multiple because tangible book value is the regulatory capital base that constrains growth. The implied relationship:</p>

<pre><code>P/TBV = (ROE - g) / (Ke - g)</code></pre>

<p>A bank with ROE = Ke trades at 1.0x TBV. A bank with ROE &gt; Ke trades above 1.0x. US regional banks typically trade at 0.8x-1.5x TBV depending on ROE and growth expectations.</p>

<h2>The correct cost of equity for a bank</h2>

<p>Even though you're using Ke rather than WACC, estimating Ke for a bank has its own complications:</p>

<p><strong>Beta</strong>: Bank betas are measured against total equity, but regulatory leverage constraints mean the asset beta is essentially fixed. High reported betas in bank stocks often reflect financial leverage and regulatory risk, not underlying business risk.</p>

<p><strong>Risk-free rate</strong>: Use the 10-year government bond yield in the bank's reporting currency. For US banks: 10-year UST. For UK banks: 10-year gilt. Don't mix currencies.</p>

<p><strong>ERP</strong>: The equity risk premium for banks is typically slightly higher than the market ERP due to the opacity of bank balance sheets and tail risk from regulatory capital requirements. Add 0.5-1.0% to a standard market ERP as a starting point.</p>

<p><strong>Size premium</strong>: For community banks and regional banks below $10bn assets, add an additional 1-3% for illiquidity and concentration risk. Not needed for G-SIBs.</p>

<h2>What about a bank-specific DCF?</h2>

<p>It's possible to build a DCF for a bank if you frame it correctly: discount free cash flow to equity (not FCFF) at the cost of equity. Free cash flow to equity for a bank is:</p>

<pre><code>FCFE = Net income
     - Increase in required equity capital
     + Change in excess capital above regulatory minimum</code></pre>

<p>The "required equity capital" term is the key: as the bank grows its loan book, it must retain capital to maintain its CET1 ratio above the regulatory minimum. This retained capital is not distributable - it belongs to the regulators, not shareholders.</p>

<p>This is why bank ROE consistently understates economic returns unless you adjust for the capital that's trapped under regulatory requirements.</p>

<h2>For modellers working with banks</h2>

<p>If you're building a financial model for a bank acquisition, a long-term plan, or a stress test:</p>

<ul>
<li>Don't attempt a WACC-based valuation</li>
<li>Build the P&amp;L and balance sheet first, then derive distributable earnings after capital constraints</li>
<li>Use P/TBV as your primary valuation anchor, with DDM or excess returns as cross-checks</li>
<li>Track CET1 ratio at every period - it's the binding constraint on distributions</li>
</ul>

<p>Our <a href="/bank-financial-model.html">Bank Long-Term Plan Model</a> is built around this framework: full balance sheet projection, capital adequacy at every period, distributable earnings calculation, and ROE/ROA/P/TBV outputs. Not a generic three-statement model with a bank skin - a genuine bank planning tool.</p>
""",
    },
    {
        "slug": "excel-financial-model-best-practices",
        "title": "Excel Financial Model Best Practices: The 12 Rules That Actually Matter",
        "h1": "Excel Financial Model Best Practices: The 12 Rules That Actually Matter",
        "keyword": "excel financial model best practices",
        "meta_desc": "The 12 Excel financial modelling best practices that separate institutional-grade models from templates. Colour coding, no INDIRECT, circular references, named ranges, and more.",
        "published": "2026-05-07",
        "summary": "Most best-practice lists are generic. These 12 rules come from building 18 institutional-grade models and watching finance teams use them under pressure. They're ranked by how often violating them causes real problems.",
        "product_link": "/models.html",
        "product_name": "SFS Models Financial Model Catalogue",
        "body": """<p>There are hundreds of Excel modelling guides. Most repeat the same obvious advice. This list comes from a different place: watching real finance teams break real models under real time pressure, then fixing the fallout.</p>

<p>These 12 rules are ranked by the cost of getting them wrong - not by how frequently they appear in textbooks.</p>

<h2>1. Colour-code every single cell</h2>

<p>Blue font for hardcoded inputs, black for formulas, green for cross-sheet links. No exceptions.</p>

<p>When a model breaks at 11pm before a board presentation, the first question is: which cell is hardcoded? If your model uses black font everywhere, that question takes an hour. With colour coding, it takes 30 seconds.</p>

<p>The convention that matters most: blue font on a yellow fill for hardcoded inputs. Anyone who opens the model for the first time knows exactly where to look.</p>

<h2>2. Never use INDIRECT</h2>

<p>INDIRECT returns the reference implied by a text string. It breaks silently when a sheet is renamed. It breaks when rows are inserted. It is not tracked by Excel's dependency engine, so auditing tools miss it.</p>

<p>The common use case: dynamic sheet references (<code>=INDIRECT(A1&amp;"!B5")</code>). Replace with CHOOSE + static references, or restructure so the data is on one sheet.</p>

<pre><code>=INDIRECT(A1&"!B5")          -- BREAKS when sheet is renamed
=CHOOSE(scenario, Sheet1!B5, Sheet2!B5, Sheet3!B5)  -- CORRECT</code></pre>

<h2>3. Inputs on one tab only</h2>

<p>Every hardcoded assumption lives on the INPUTS tab. Not on calculation sheets. Not in formula strings. Not buried in named ranges scattered across the workbook.</p>

<p>The test: can someone change every assumption in the model without leaving the INPUTS tab? If yes, the model passes. If no, find the strays.</p>

<p>The practical consequence: users don't need to understand the model's structure to run sensitivities. They change one tab, outputs update. This is the difference between a tool someone will actually use and one they'll rebuild from scratch.</p>

<h2>4. Interest on prior-period balance, always</h2>

<p>Calculate interest charges on the opening (prior-period closing) balance, not the current period's closing balance. This eliminates circularity in every debt, deposit, and loan roll-forward without enabling iterative calculation.</p>

<pre><code>Opening balance   = Prior closing (no circular)
Interest charge   = Opening × rate
Closing balance   = Opening + drawdown - repayment + interest</code></pre>

<p>Models that use closing balance for interest require iterative calculation. Iterative calculation is non-deterministic (result depends on iteration count), rejected by audit teams, and breaks on copy-paste into new workbooks.</p>

<h2>5. IFERROR on every division</h2>

<p>Always. No exceptions. <code>=IFERROR(A/B, 0)</code> or <code>=IFERROR(A/B, "-")</code> depending on whether zero or a dash is the correct display for undefined.</p>

<p>The failure mode: a model built with bare divisions fails on the first zero-denominator input. In a model with 5,000 formula cells, one #DIV/0! propagates to hundreds of dependent cells. The model looks broken. It takes an hour to diagnose.</p>

<h2>6. Format negatives in parentheses, not with a minus sign</h2>

<p>Finance convention: negative numbers are displayed as (1,234) not -1,234. Use format strings that include the parenthesis format:</p>

<pre><code>#,##0;(#,##0);"-"</code></pre>

<p>The semicolons separate: positive format; negative format; zero format. The zero format shows a dash rather than "0" - standard for financial statements.</p>

<p>A model presented to a CFO that shows negative numbers with minus signs looks like a student spreadsheet. The format string is a three-character fix.</p>

<h2>7. Named ranges for everything referenced more than once</h2>

<p>Any cell that multiple formulas reference should have a named range. <code>BaseRate</code>, <code>ScenarioSelect</code>, <code>StartDate</code>, <code>WACCBase</code>.</p>

<p>The practical benefit: when you need to find all formulas that reference a key assumption, <code>Ctrl+F</code> on the named range name finds them all. With cell references (<code>INPUTS!$B$12</code>), you hope you got every instance.</p>

<p>Named ranges also survive row and column insertion, unlike absolute cell references that silently point to the wrong cell if a row is inserted above them.</p>

<h2>8. Maximum 3 levels of IF nesting</h2>

<p>Nested IFs beyond three levels are untestable. No one can read them. They break on edge cases that the author didn't consider when writing the formula.</p>

<pre><code>=IF(A=1, x, IF(A=2, y, IF(A=3, z, "")))   -- 3 levels: acceptable
=IF(A=1, x, IF(A=2, y, IF(A=3, z, IF(A=4, w, ""))))   -- 4 levels: refactor</code></pre>

<p>The refactor options: CHOOSE (for numeric indices), INDEX/MATCH (for lookup tables), IFS (Excel 2016+), or helper columns that break the logic into readable steps.</p>

<h2>9. Freeze panes on every data tab</h2>

<p>Freeze row 1-2 (headers and column labels) and column A (row labels) on every calculation sheet. <code>=View &gt; Freeze Panes &gt; Freeze at B3</code>.</p>

<p>The failure mode: a model where scrolling right loses the row labels, or scrolling down loses the column headers, is impossible to use in a meeting. The user loses track of which row they're looking at, which period they're in.</p>

<p>This takes 30 seconds per tab. There is no excuse for missing it.</p>

<h2>10. A CHECKS tab with explicit pass/fail</h2>

<p>Every model should have a tab called CHECKS (or equivalent) with explicit integrity tests. The minimum set:</p>

<ul>
<li>Balance sheet balances: Assets = Liabilities + Equity</li>
<li>Cash flow closing = balance sheet cash</li>
<li>Debt schedule closing ties to balance sheet debt</li>
<li>Interest from debt schedule = interest in P&amp;L</li>
</ul>

<p>Each check is a formula that returns "PASS" or "FAIL" with conditional formatting (green/red). When someone hands you a model, you look at the CHECKS tab first. All green = model integrity is intact. Any red = find the error before using any output.</p>

<h2>11. No hardcoded numbers in formula cells</h2>

<p>A formula that reads <code>=B5*0.35</code> has a hardcoded 0.35. What is 0.35? A tax rate? A fee? An assumption made in 2021 that was never updated? Nobody knows.</p>

<p>Every number in a formula should come from a named range or an INPUTS cell reference. The formula should read <code>=B5*TaxRate</code> or <code>=B5*INPUTS!$C$18</code>. The value lives in one place. When it changes, you change it once.</p>

<h2>12. Print setup before you consider the model done</h2>

<p>Every tab should print cleanly on A4 landscape. Set:</p>

<ul>
<li>Orientation: landscape</li>
<li>Scale: fit to page width (1 page wide, height free)</li>
<li>Print titles: rows 1:2 repeat on every page</li>
<li>Margins: 0.5cm left/right, 0.6cm top/bottom</li>
</ul>

<p>This is not aesthetic. A finance director who can't print the model cleanly for a board pack will not use it again. It takes 5 minutes per tab.</p>

<h2>The test that catches everything else</h2>

<p>Give the model to someone who didn't build it. Tell them nothing. Ask them to change one assumption and tell you what the output is.</p>

<p>If they can do it in under 10 minutes without asking you a question, the model is user-ready. If they can't, something from this list is missing.</p>

<p>Browse our <a href="/models.html">full model catalogue</a> - all 18 models are built to this standard. Open formulas, no VBA, CHECKS tab all green, print-ready on first open.</p>
""",
    },
    {
        "slug": 'ifrs9-staging-sicr',
        "title": 'IFRS 9 Staging: When 12-Month ECL Becomes Lifetime ECL',
        "h1": 'IFRS 9 Staging: When 12-Month ECL Becomes Lifetime ECL',
        "keyword": 'ifrs 9 significant increase in credit risk',
        "meta_desc": 'IFRS 9 stage 2 transfer is the judgement that moves the provision. How to define SICR, set thresholds, avoid the 30-day backstop trap, and build staging that survives audit.',
        "published": '2026-09-07',
        "summary": 'Stage 2 is where the provision actually moves. A loan transferring from stage 1 to stage 2 can multiply its ECL by ten overnight, and the trigger is a judgement, not a number handed to you.',
        "product_link": '/ifrs9-cecl-model-excel.html',
        "product_name": 'IFRS 9 ECL Model',
        "body": """<p>Most of the argument about an IFRS 9 provision is not about PD, LGD or discounting. It is about staging. A loan sitting in stage 1 carries 12 months of expected loss. The same loan in stage 2 carries lifetime expected loss. On a 7-year amortising facility that is not a marginal change, it is frequently a five to ten times increase in the provision for that exposure.</p>

<p>So the question that moves your numbers is narrow: what counts as a significant increase in credit risk?</p>

<h2>What the standard actually requires</h2>

<p>IFRS 9 asks you to compare credit risk <em>at the reporting date</em> against credit risk <em>at initial recognition</em>, for the remaining life of the instrument. Two things follow from that sentence, and both are routinely got wrong.</p>

<p>First, it is a relative test, not an absolute one. A borrower can be objectively poor quality and still sit in stage 1, provided it was equally poor quality when you wrote the loan. A BB facility originated as BB has not deteriorated. Absolute-quality thresholds fail the standard.</p>

<p>Second, it is lifetime PD you compare, not 12-month PD. A facility can show a flat 12-month PD while its lifetime PD has moved materially, because the deterioration is expected to bite in year three. If your staging test runs on 12-month PD because that is the number your rating system produces monthly, you will transfer late.</p>

<h2>Setting the threshold</h2>

<p>The standard gives you no number. In practice three approaches are defensible, and the choice matters more than the calibration.</p>

<p><strong>Relative PD movement.</strong> Transfer when lifetime PD has increased by more than a set multiple of origination PD. The trap is that a fixed multiple is brutal at the good end and toothless at the poor end. A move from 0.10% to 0.25% is a 150% increase and almost certainly noise. A move from 8% to 14% is a 75% increase and is a genuine problem. A single multiple cannot serve both.</p>

<p><strong>Absolute PD movement with a relative floor.</strong> Combine the two: transfer if lifetime PD has risen by more than X percentage points <em>and</em> by more than Y percent of its origination level. This is the most common design at UK banks and it survives challenge better than either test alone.</p>

<p><strong>Rating-notch movement.</strong> Transfer on a drop of N notches from origination grade. Operationally simple, and it maps onto how credit officers already think, which matters when the staging output has to be explained. The weakness is that notch width is not constant across the scale, so a two-notch move means different things at different points.</p>

<h2>The 30-day backstop is a floor, not a policy</h2>

<p>IFRS 9 carries a rebuttable presumption that credit risk has increased significantly once a payment is more than 30 days past due. A surprising number of models treat this as the staging rule.</p>

<p>It is not. It is the backstop that catches what your primary test missed. If your 30-day trigger is doing most of the transferring, your quantitative test is not working, and that is exactly what an auditor will look for. Run the diagnostic: what share of your stage 2 population arrived there through the PD test, and what share through days past due alone? If the second number is above roughly a third, the primary test is too slack.</p>

<h2>Transfers back, and why they are asymmetric in practice</h2>

<p>Staging is symmetric in the standard. An exposure that recovers moves back to stage 1. In practice most institutions apply a probation period, commonly three to six months of performance, before allowing the transfer back.</p>

<p>That is defensible, but it has a modelling consequence people miss: it makes your stage 2 population sticky, so provision releases lag provision charges through a cycle. If your model transfers back instantly, your ECL will look more volatile than your peers' and you will be asked why.</p>

<h2>Where the model usually breaks</h2>

<p>Three failures account for most of the staging problems worth finding.</p>

<p><strong>No origination PD stored.</strong> The comparison is against initial recognition, so you need the PD at origination for every live exposure. Banks that started IFRS 9 without that field end up proxying it from the origination rating grade, which is workable but must be disclosed and will be challenged.</p>

<p><strong>Staging applied after the ECL calculation.</strong> The stage determines whether you use 12-month or lifetime ECL, so it has to be resolved first. A model that calculates both and then picks is fine. A model that calculates 12-month ECL and then scales it up for stage 2 exposures is not, because lifetime ECL is not a multiple of 12-month ECL.</p>

<p><strong>No reconciliation of stage movement.</strong> Your provision movement should decompose into: new lending, repayments, stage transfers, model and assumption changes, and write-offs. If stage transfers are not an explicit line, nobody can explain the provision to the audit committee, and the number becomes unpresentable regardless of whether it is right.</p>

<h2>The practical test</h2>

<p>Take one facility that transferred to stage 2 this month. Trace it: origination PD, current lifetime PD, which trigger fired, what the ECL was before and after, and where that movement appears in the provision walk. If you cannot do that in under five minutes, the staging logic is buried somewhere it should not be.</p>

<p>Our <a href="/ifrs9-cecl-model-excel.html">IFRS 9 ECL Model</a> carries stage 1, 2 and 3 allocation with the transfer logic on its own tab, lifetime and 12-month ECL calculated in parallel rather than scaled, and a macro overlay applied after staging. Every stage movement lands in the provision reconciliation.</p>""",
    },
    {
        "slug": 'ifrs9-ecl-model-excel-build',
        "title": 'How to Build an IFRS 9 ECL Model in Excel',
        "h1": 'How to Build an IFRS 9 ECL Model in Excel',
        "keyword": 'ifrs 9 ecl model excel',
        "meta_desc": 'The tab structure, the PD/LGD/EAD mechanics and the reconciliations an IFRS 9 ECL model in Excel needs before anyone will sign it off. Written from bank practice.',
        "published": '2026-09-07',
        "summary": 'An ECL model is not hard arithmetic. It is hard bookkeeping. Most of them fail review not because the loss numbers are wrong, but because nobody can trace how a provision moved between two dates.',
        "product_link": '/ifrs9-cecl-model-excel.html',
        "product_name": 'IFRS 9 ECL Model',
        "body": """<p>The expected credit loss calculation itself is a line of arithmetic. Probability of default times loss given default times exposure at default, discounted. Anyone can write that formula.</p>

<p>What makes an ECL model hard is everything around that line: getting the staging right before you calculate, holding lifetime and 12-month views in parallel, applying a forward-looking overlay without destroying the audit trail, and being able to explain in a committee why the provision moved by the amount it moved. Build for the explanation, not the arithmetic.</p>

<h2>The tab structure that works</h2>

<p>One workable layout, in dependency order.</p>

<p><strong>INPUTS.</strong> Every assumption, nothing else. Segment definitions, PD term structures, LGD by collateral type, EAD parameters and credit conversion factors, discount rates, staging thresholds, macroeconomic scenarios and their weights. If a number can be argued about, it lives here in a blue cell, not buried in a formula three tabs away.</p>

<p><strong>PORTFOLIO.</strong> The exposure data as received: facility, segment, origination date, origination PD or grade, current balance, undrawn commitment, collateral, days past due. This tab is a landing zone, so it should contain no formulas at all. Keeping it inert is what lets you swap a month's data without touching the model.</p>

<p><strong>STAGING.</strong> The stage 1, 2 and 3 allocation, with each trigger evaluated in its own column so you can see which one fired. Quantitative test, backstop, and any qualitative flags, then the resulting stage. Do this before any ECL is calculated.</p>

<p><strong>PD_TERM.</strong> Marginal and cumulative PD by period out to maturity, per segment and scenario. This is the tab that turns a point-in-time PD into the lifetime curve the standard needs.</p>

<p><strong>ECL_12M</strong> and <strong>ECL_LIFETIME.</strong> Both calculated for every exposure, always. Then the stage picks which one flows through. Calculating only the one you think you need is where models become impossible to challenge.</p>

<p><strong>OVERLAY.</strong> The forward-looking adjustment, applied as an explicit, separately visible layer. Never blended into the base PD.</p>

<p><strong>RECONCILIATION.</strong> The provision walk from opening to closing, decomposed.</p>

<p><strong>CHECKS.</strong> Everything that has to tie.</p>

<h2>Lifetime is not a multiple of 12-month</h2>

<p>The most common structural error is calculating a 12-month ECL and scaling it by some factor for stage 2 exposures.</p>

<p>Lifetime ECL is the sum, across every remaining period, of the marginal probability of default in that period, times LGD, times expected exposure at that point, discounted back at the effective interest rate. Three things vary across those periods and none of them scale linearly: the marginal PD follows a term structure, the exposure amortises, and the discount factor compounds.</p>

<p>For an amortising loan the exposure profile alone can make lifetime ECL a smaller multiple than intuition suggests, because the largest default probabilities in later years apply to a much smaller balance. Scale factors get this backwards on precisely the facilities where the provision matters most.</p>

<h2>The scenario weighting most models get wrong</h2>

<p>IFRS 9 requires a probability-weighted outcome, not a best estimate. That means running the ECL under each macroeconomic scenario and weighting the <em>results</em>.</p>

<p>Running the model once on probability-weighted <em>inputs</em> is not the same thing and is not compliant. Because the relationship between macro variables and loss is convex, weighting the inputs systematically understates ECL. The gap widens exactly when it matters, in the tail.</p>

<p>Structurally this means your ECL tabs need a scenario dimension from the outset. Retrofitting one into a model built for a single case is a rebuild, so decide early.</p>

<h2>Overlays, and keeping them defensible</h2>

<p>Post-model adjustments are a fact of life. New risks appear faster than models can be recalibrated. The problem is not having overlays, it is having overlays nobody can dismantle later.</p>

<p>Keep every overlay as a separate, named line with its own rationale, its own quantum, and the population it applies to. When the underlying model is recalibrated, you need to be able to remove the overlay cleanly. An overlay buried inside a PD assumption cannot be removed without unpicking the whole calibration, and tends to survive for years after the risk it addressed has gone.</p>

<h2>The reconciliation is the deliverable</h2>

<p>The single most useful tab is the provision walk. Opening ECL, then:</p>

<ul>
<li>new lending originated in the period</li>
<li>repayments, maturities and write-offs</li>
<li>stage transfers, ideally split by direction</li>
<li>changes in risk parameters within stage</li>
<li>model and methodology changes</li>
<li>overlay movements</li>
<li>closing ECL</li>
</ul>

<p>If those components do not sum to the movement, something is wrong, and finding out at the reconciliation is far cheaper than finding out in committee. This is also the tab that gets projected on the wall, so it is worth more layout care than the calculation engines behind it.</p>

<h2>Checks that must pass</h2>

<p>Sum of exposures by stage equals total portfolio. Sum of ECL by stage equals total provision. Every stage 3 exposure has a lifetime calculation. No PD outside 0 to 1. No negative ECL. Scenario weights sum to exactly 1. Provision walk ties opening to closing. Every one of these has caught a real error in a real model.</p>

<p>Our <a href="/ifrs9-cecl-model-excel.html">IFRS 9 ECL Model</a> is built on this structure, with lifetime and 12-month ECL calculated in parallel, scenario weighting applied to results rather than inputs, and the provision walk as a standing output.</p>""",
    },
    {
        "slug": 'reverse-stress-testing-bank',
        "title": 'Reverse Stress Testing: Finding the Scenario That Breaks the Bank',
        "h1": 'Reverse Stress Testing: Finding the Scenario That Breaks the Bank',
        "keyword": 'reverse stress testing bank',
        "meta_desc": 'Reverse stress testing starts from failure and works backwards. How to define the failure point, search for the scenarios that reach it, and make the output usable by a board.',
        "published": '2026-09-07',
        "summary": 'Ordinary stress testing asks what happens if things get bad. Reverse stress testing asks what would have to happen for the bank to stop being viable. The second question is harder and more useful.',
        "product_link": '/bank-stress-test-model.html',
        "product_name": 'Bank Stress Test Model',
        "body": """<p>A normal stress test starts with a scenario and produces a capital ratio. You pick an unemployment path and a house price fall, run them through, and see what CET1 does. The output is reassuring almost by construction, because the scenario was chosen to be severe but survivable.</p>

<p>Reverse stress testing inverts it. You start at the point of non-viability and work backwards to find what could get you there. The question is not "how bad is a severe recession" but "what precisely would have to go wrong, and is that combination as implausible as we are assuming?"</p>

<h2>Defining failure before you search for it</h2>

<p>The exercise is meaningless without a precise failure condition, and it is rarely a single number. Candidates worth defining explicitly:</p>

<p><strong>Capital.</strong> CET1 falls below the point where the business model stops working. That is usually well above the 4.5% minimum, because a bank hits its MDA restriction and loses access to funding markets long before it hits Pillar 1. Setting the trigger at the regulatory minimum produces a comfortable, useless answer.</p>

<p><strong>Liquidity.</strong> The bank cannot meet outflows over a defined survival horizon. Often the binding constraint in practice, and frequently reached faster than the capital one.</p>

<p><strong>Business model.</strong> Losses do not exhaust capital, but the franchise stops generating enough return to justify holding it. Harder to quantify, and the one most often skipped.</p>

<p>Pick the definition, write it down, and get it agreed before running anything. Most of the value in the exercise is created in this conversation rather than in the modelling.</p>

<h2>Searching backwards</h2>

<p>Forward stress testing is one calculation. Reverse stress testing is a search across a space of scenarios, and the space is large.</p>

<p>The tractable approach is to reduce it to the handful of drivers that actually move your outcome, then search over those. For most lenders that is credit losses on the largest portfolio, funding cost, and one concentration. Fix the others at base, then find the combination of your chosen drivers that reaches the failure point.</p>

<p>Two properties make the result useful. First, express the answer in units a credit officer recognises: a default rate on the commercial book, a fall in a specific collateral value, a deposit outflow over a number of days. "A 4.2 standard deviation shock" is not actionable. Second, find the <em>closest</em> failure scenario, not any failure scenario. Anything is fatal if it is extreme enough. The question is what the least extreme fatal combination looks like, because that is the one worth defending against.</p>

<h2>The output that changes decisions</h2>

<p>Done properly this produces a small number of statements a board can act on. Something in the shape of: the bank stops being viable if commercial real estate defaults reach a given rate while collateral values fall by a given percentage, sustained over a given period.</p>

<p>Then the useful conversation begins. How far is that from what we saw in 2008, or in 2020? What would we see first if we were heading there? Which of our current limits would have bound before we arrived, and did any of them get relaxed recently?</p>

<p>That last question is the one that justifies the exercise. Reverse stress testing regularly finds that a limit framework was calibrated against a scenario milder than the one that actually breaks the bank.</p>

<h2>Where it goes wrong</h2>

<p><strong>Choosing a comfortable answer.</strong> If the failure scenario you report is obviously absurd, you have either set the failure point too low or searched only where you were confident nothing lived. A scenario nobody can argue with is a scenario nobody learns from.</p>

<p><strong>Ignoring second-order effects.</strong> The path to failure is rarely one variable. Credit losses raise funding costs, which compress margin, which slows capital generation, which restricts new lending, which shrinks the earning asset base. A model with no feedback finds the failure point too far out.</p>

<p><strong>Treating it as a compliance artefact.</strong> Reverse stress testing appears in ICAAP because supervisors ask for it, and it is easy to produce something that satisfies the requirement and informs nothing. The test of a real exercise is whether it changed a limit, a hedge or an appetite statement.</p>

<h2>Building it</h2>

<p>You do not need separate machinery. If your capital projection already runs scenarios from a single switch, reverse stress testing is a search loop over that engine: vary the drivers, evaluate the failure condition, keep the least extreme combination that trips it. What you do need is a projection where the drivers are genuinely parameterised rather than hardcoded, and where the failure condition is a formula rather than a judgement made by reading the output.</p>

<p>Our <a href="/bank-stress-test-model.html">Bank Stress Test Model</a> runs base, adverse and severe scenarios through P&amp;L, capital and liquidity from one switch, with the capital and liquidity failure conditions calculated rather than eyeballed, and board-ready output.</p>""",
    },
    {
        "slug": 'icaap-model-guide',
        "title": 'ICAAP: A Practical Guide for Finance Teams',
        "h1": 'ICAAP: A Practical Guide for Bank Finance Teams',
        "keyword": 'icaap model',
        "meta_desc": 'What ICAAP actually requires, how to structure your capital adequacy assessment, what examiners look for, and how to build the capital model that supports it.',
        "published": '2026-05-11',
        "summary": 'Most ICAAP submissions fail at the model layer, not the narrative layer. The regulator already knows your capital ratios. What they want to see is whether your capital model is robust enough to trust under stress. This guide covers the mechanics.',
        "product_link": '/bank-stress-test-model.html',
        "product_name": 'Bank Stress Test Model',
        "body": """<p>The Internal Capital Adequacy Assessment Process (ICAAP) is the Pillar 2 submission in which a bank demonstrates to its regulator that it holds sufficient capital to absorb the risks it faces - under both base and stress conditions. In the UK, the PRA reviews ICAAP annually. In the EU, the ECB's SREP cycle uses it. For US banks under the Fed's Enhanced Prudential Standards, the internal capital plan serves a similar function.</p>

    <p>Getting ICAAP right is not primarily a writing exercise. The regulator can read. What they scrutinise is the capital model underpinning the narrative - how risks are quantified, how scenarios are constructed, and whether the numbers are credible.</p>

    <h2>What ICAAP must demonstrate</h2>

    <p>At its core, ICAAP answers one question: <em>if adverse conditions materialise, does the bank have enough capital to absorb losses while remaining viable?</em></p>

    <p>The regulator's framework for answering this question has three components:</p>

    <ol>
      <li><strong>Risk identification and quantification.</strong> Every material risk the bank faces must be identified, quantified where possible, and allocated a capital charge. Risks not captured by Pillar 1 RWA (market risk, credit concentration, IRRBB, operational risk, etc.) must be covered by Pillar 2A add-ons.</li>
      <li><strong>Stress testing.</strong> Capital adequacy must be tested under at least one adverse scenario that is plausible and severe. The scenario must stress the bank's specific vulnerabilities, not just apply a generic macro shock.</li>
      <li><strong>Capital plan.</strong> The bank must project its capital position over a 3-5 year horizon, showing that ratios remain above regulatory minima under base and stress conditions even as the business plan evolves.</li>
    </ol>

    <h2>The capital model structure</h2>

    <p>The capital model is the engine. Without a credible model, the narrative is just words. A workable ICAAP capital model has five layers:</p>

    <table>
      <tr><th>Layer</th><th>What it contains</th><th>Key outputs</th></tr>
      <tr><td>Capital base</td><td>CET1 instruments, retained earnings, OCI, deductions (goodwill, DTA, intangibles)</td><td>CET1, T1, Total Capital</td></tr>
      <tr><td>Credit RWA</td><td>EAD by exposure class &times; risk weight (Standardised or IRB)</td><td>Credit RWA by book</td></tr>
      <tr><td>Market RWA</td><td>VaR &times; multiplier &times; 12.5 (or Standardised approach)</td><td>Market RWA</td></tr>
      <tr><td>Operational RWA</td><td>Basic Indicator Approach: 15% &times; 3-year average gross income &times; 12.5</td><td>Op risk RWA</td></tr>
      <tr><td>Pillar 2A / buffers</td><td>SREP add-ons, capital conservation buffer, countercyclical buffer, SyRB</td><td>Total requirement, headroom</td></tr>
    </table>

    <p>The ratio that matters: <strong>CET1 ratio = CET1 capital &divide; Total RWA</strong>. The capital plan must show this stays above the combined buffer requirement (4.5% Pillar 1 + Pillar 2A + buffers) throughout the plan period, including in the stress scenario.</p>

    <h2>The stress scenario: what makes one credible</h2>

    <p>This is where most ICAAP submissions are weakest. Generic stress scenarios - "GDP falls 3%, unemployment rises to 8%" - don't demonstrate that you understand your specific vulnerabilities.</p>

    <p>A credible adverse scenario has three properties:</p>

    <p><strong>1. It's bank-specific.</strong> If your book is 60% commercial real estate, the scenario needs a CRE shock. If you're deposit-funded with high deposit beta, a rate-shock scenario that stresses NIM is essential. The regulator knows your balance sheet. Apply a scenario that would actually hurt you.</p>

    <p><strong>2. It's internally consistent.</strong> A rate spike scenario that also has a property crash and a recession needs to show how those three forces interact. GDP and unemployment need to move in the same direction. Credit losses need to be a function of the macro shock, not an independent assumption.</p>

    <p><strong>3. The loss estimates are defensible.</strong> PD migration, LGD haircuts, NIM compression, PPNR deterioration - each needs a documented methodology. "Stressed PD = base PD &times; 2" is not a methodology.</p>

    <h2>Capital planning: the forward view</h2>

    <p>The capital plan projects CET1 ratio and RWA over 3-5 years under base and stress scenarios. The key mechanics:</p>

    <p><strong>Capital generation:</strong> Net income &minus; dividends &minus; share buybacks = retained earnings added to CET1. Stress NIM, credit losses, and PPNR simultaneously and the NI line deteriorates quickly. Banks that model stress NI as "base NI &times; 0.7" are guessing.</p>

    <p><strong>RWA migration:</strong> Credit RWA expands in stress as PDs rise (under IRB) or as loans migrate to higher risk weight buckets. A bank with a £2bn book and 70% average risk weight has £1.4bn credit RWA. Under stress, PD migration can push this to £1.8-2.0bn before you've made a single new loan.</p>

    <p><strong>The ratio trough:</strong> The capital plan should explicitly show the trough CET1 ratio under the stress scenario and the headroom above the regulatory minimum at that trough. If the trough is below the combined buffer requirement, the plan needs to show a management action (capital raise, dividend cut, RWA reduction) that restores the ratio.</p>

    <h2>Pillar 2A: how to quantify risks not in Pillar 1</h2>

    <p>Pillar 2A covers risks that Pillar 1 RWA doesn't fully capture. The most common P2A additions:</p>

    <ul>
      <li><strong>Credit concentration risk.</strong> Single-name, sector, and geographic concentrations above the Herfindahl-Hirschman Index thresholds. Standardised add-on: typically 1-3% of the concentrated exposure.</li>
      <li><strong>IRRBB (interest rate risk in the banking book).</strong> EVE sensitivity under the six prescribed shocks (parallel up/down, steepener, flattener, short up, short down). P2A = capital needed to cover the EVE decline in the outlier scenario.</li>
      <li><strong>Operational risk top-up.</strong> If BIA underestimates operational risk (e.g., large pending legal cases, cyber exposure), the P2A submission should quantify the gap.</li>
      <li><strong>Model risk.</strong> If the capital model itself has material uncertainty, regulators increasingly expect a model risk charge. Not universal, but growing.</li>
    </ul>

    <h2>Common ICAAP model failures</h2>

    <p>Based on what regulators publicly flag in their supervisory assessments:</p>

    <ul>
      <li><strong>Static balance sheet in the stress scenario.</strong> A bank that holds £500m of CRE loans doesn't hold that same £500m throughout the stress. Runoff, refinancing, and new origination all change the exposure. The stressed capital plan needs a dynamic balance sheet.</li>
      <li><strong>Stress loss = base loss &times; multiplier.</strong> This is the first thing an examiner will challenge. If your stressed credit losses are exactly 2x base, the justification needs to be airtight. More credible: PD/LGD migration driven by the macro scenario.</li>
      <li><strong>RWA held constant in stress.</strong> Standardised RWA can change if the mix shifts. IRB RWA expands automatically under stress as PDs rise. A fixed RWA line in the stress scenario signals the model isn't dynamic.</li>
      <li><strong>No management actions documented.</strong> The regulator expects to see the levers available - dividend suspension, capital raise, RWA optimisation, asset disposal - and a timeline for exercising them. Without this, the stress scenario has no credible resolution.</li>
    </ul>

    <h2>ICAAP model in Excel: what it needs to do</h2>

    <p>For most mid-tier banks (£5bn-£50bn assets), the ICAAP model lives in Excel. It needs to:</p>

    <ul>
      <li>Calculate CET1, T1, Total Capital from an auditable base</li>
      <li>Build credit RWA by exposure class with risk weight inputs</li>
      <li>Calculate market and op risk RWA per the Standardised approach</li>
      <li>Apply P2A add-ons and buffer requirements to produce the overall capital requirement</li>
      <li>Project all of the above over 5 years under Base, Adverse, and Severely Adverse scenarios using a single scenario switch</li>
      <li>Show the trough ratio and headroom in the output summary</li>
      <li>Pass a CHECKS tab that validates all balance sheet, debt schedule, and ratio integrity</li>
    </ul>

    <div class="blog-cta">
      <h3>ICAAP Model - Excel Template</h3>
      <p>Institutional-grade ICAAP model built for mid-tier bank Finance and Capital teams. Covers Pillar 1 RWA (credit, market, op risk), Pillar 2A quantification, capital plan projection, and stress testing with a single scenario switch. Fully open formulas, CHECKS tab, print-ready layout.</p>
      <p><a href="/icaap-model-excel.html" class="btn btn-primary">View the ICAAP Model &rarr;</a></p>
    </div>

    <h2>ILAAP: the liquidity counterpart</h2>

    <p>ICAAP covers capital adequacy. ILAAP - the Internal Liquidity Adequacy Assessment Process - covers liquidity adequacy. Both are required by the PRA (and equivalent regulators elsewhere) and are reviewed together in the SREP cycle.</p>

    <p>The interaction matters: a bank can be adequately capitalised and illiquid at the same time. The 2023 SVB failure was fundamentally a liquidity crisis in a bank that was technically solvent. ICAAP alone doesn't protect against that. If you need to build ILAAP alongside ICAAP, the structure is similar but the focus is on LCR, NSFR, and survival horizon under a combined stress scenario. See our <a href="/ilaap-model-excel.html">ILAAP model</a> for the liquidity-side equivalent.</p>

    <h2>Summary</h2>

    <p>ICAAP quality is determined by the capital model, not the narrative. The model needs to be dynamic (balance sheet evolves under stress), scenario-driven (not just base &times; multiplier), and internally consistent (capital generation, RWA migration, and management actions all linked). If the model doesn't pass those tests, the SREP reviewers will find the weakness.</p>

    <p>For a free DCF model to see our build quality before committing, <a href="/free-samples.html">download a sample here</a>.</p>

    <p style="color:var(--text-muted); font-size: 0.85rem; margin-top: 3rem;">Published 2026-05-11. SFS Models builds institutional-grade Excel financial models for bank Finance, Capital, and Treasury teams. <a href="/models.html">View all models.</a></p>""",
    },
    {
        "slug": 'ilaap-liquidity-model',
        "title": 'ILAAP: The Practical Guide to Internal Liquidity Adequacy Assessment',
        "h1": 'ILAAP: A Practical Guide to Internal Liquidity Adequacy Assessment',
        "keyword": 'ilaap liquidity adequacy assessment',
        "meta_desc": 'How ILAAP works, what it must demonstrate, the difference from ICAAP, LCR vs NSFR vs survival horizon, and how to structure the liquidity model that supports it.',
        "published": '2026-05-11',
        "summary": "A bank can be adequately capitalised and still fail within days if it can't fund its liabilities. ILAAP is the regulatory framework that tests whether a bank can survive a liquidity stress. Here's what it requires and how to build the model that supports it.",
        "product_link": '/models.html',
        "product_name": 'SFS Model Catalogue',
        "body": """<p>The Internal Liquidity Adequacy Assessment Process (ILAAP) is the liquidity counterpart to ICAAP. Where ICAAP asks "does the bank have enough capital to absorb losses?", ILAAP asks "does the bank have enough liquidity to survive a stress event without external support?"</p>

    <p>The 2023 Silicon Valley Bank failure illustrated this distinction with brutal clarity. SVB was technically solvent on a held-to-maturity basis. It failed because a deposit run over 48 hours exhausted its liquidity. ICAAP alone doesn't protect against that. ILAAP is the framework designed to catch it early.</p>

    <p>In the UK, ILAAP is required for PRA-supervised banks and building societies under SS24/15. In the EU, SSM banks submit it alongside ICAAP as part of the SREP cycle. For US banks, the LCR rule and the internal liquidity stress testing requirements under the Liquidity Coverage Ratio final rule serve a broadly similar function.</p>

    <h2>What ILAAP must demonstrate</h2>

    <p>An ILAAP submission must demonstrate that the bank:</p>
    <ol>
      <li><strong>Understands its liquidity risk profile</strong> - where its funding comes from, how stable it is, where concentrations exist</li>
      <li><strong>Maintains sufficient HQLA</strong> to survive a 30-day combined stress (LCR compliance)</li>
      <li><strong>Has a stable funding structure</strong> over the medium term (NSFR compliance)</li>
      <li><strong>Can survive a stressed period</strong> of at least 30 days on an intraday basis without accessing external markets</li>
      <li><strong>Has an adequate ILAAP buffer</strong> of High Quality Liquid Assets beyond what LCR requires</li>
    </ol>

    <h2>The three regulatory metrics</h2>

    <table>
      <tr><th>Metric</th><th>What it measures</th><th>Minimum</th><th>Stress horizon</th></tr>
      <tr><td>LCR (Liquidity Coverage Ratio)</td><td>HQLA &divide; Net stressed outflows over 30 days</td><td>100%</td><td>30 days</td></tr>
      <tr><td>NSFR (Net Stable Funding Ratio)</td><td>Available Stable Funding &divide; Required Stable Funding</td><td>100%</td><td>1 year</td></tr>
      <tr><td>Survival horizon</td><td>Days of liquidity under combined stress</td><td>Internal minimum (typically 30-90 days)</td><td>Bank-specific</td></tr>
    </table>

    <p>LCR is the primary near-term metric. It requires banks to hold enough High Quality Liquid Assets (HQLA) to cover net cash outflows over a 30-day stress scenario. HQLA is cash, central bank reserves, Level 1 government bonds, and qualifying Level 2 assets with haircuts.</p>

    <p>NSFR is the structural funding metric. It asks whether the funding structure is stable enough to support the asset base over a 12-month horizon. Long-term assets must be funded by long-term liabilities; short-term wholesale funding creates NSFR pressure.</p>

    <h2>The ILAAP stress scenario</h2>

    <p>The ILAAP stress scenario is typically a combined market and idiosyncratic stress - a simultaneous market-wide liquidity squeeze and a bank-specific run driven by a loss of confidence.</p>

    <p>The prescribed outflow rates for retail deposits in LCR are:</p>
    <ul>
      <li>Stable retail deposits (fully insured, established relationship): 3-5% run-off</li>
      <li>Less stable retail deposits: 10-15% run-off</li>
      <li>SME deposits: 5-10% run-off</li>
      <li>Non-financial corporate: 25% run-off</li>
      <li>Financial institution deposits: 100% run-off</li>
      <li>Unsecured wholesale funding &lt;30 days: 100% run-off</li>
    </ul>

    <p>For ILAAP's internal stress scenario, the bank typically applies more severe rates than the LCR minimum - especially for uninsured commercial deposits and wholesale funding. Post-SVB, any bank with significant uninsured commercial deposits should be stress-testing at 40-60%+ run-off for that cohort in the adverse case.</p>

    <h2>The survival horizon</h2>

    <p>The survival horizon is the number of days a bank can continue to meet its obligations under the internal stress scenario before the HQLA buffer is exhausted. It's calculated as:</p>

    <pre><code>For each day t:
  Net_outflows(t) = Outflows(t) - Inflows(t) [based on stressed run-off rates]
  HQLA_buffer(t) = HQLA_buffer(t-1) - Net_outflows(t)

Survival_horizon = first day t where HQLA_buffer(t) ≤ 0</code></pre>

    <p>The internal minimum is typically 30 days (to match the LCR horizon) but regulators expect banks to target 45-90 days for meaningful headroom. A bank that hits its minimum at exactly 31 days has no margin.</p>

    <h2>HQLA composition and haircuts</h2>

    <p>Not all liquid assets count equally in HQLA. The regulatory haircuts:</p>

    <table>
      <tr><th>Asset class</th><th>Level</th><th>Haircut</th><th>Cap</th></tr>
      <tr><td>Cash, central bank reserves</td><td>Level 1</td><td>0%</td><td>None</td></tr>
      <tr><td>Sovereign / central bank bonds (0% RW)</td><td>Level 1</td><td>0%</td><td>None</td></tr>
      <tr><td>Non-0% RW sovereign bonds</td><td>Level 2A</td><td>15%</td><td>40% of total HQLA</td></tr>
      <tr><td>Covered bonds (AA-)</td><td>Level 2A</td><td>15%</td><td>40% of total HQLA</td></tr>
      <tr><td>Qualifying RMBS, corporate bonds</td><td>Level 2B</td><td>25-50%</td><td>15% of total HQLA</td></tr>
    </table>

    <p>A bank holding mostly Level 2B assets (e.g., corporate bond portfolio) will find its HQLA meaningfully lower than the face value. This is a common modelling gap - teams count the portfolio at market value without applying the haircut, overstating LCR.</p>

    <h2>Funding structure analysis</h2>

    <p>Beyond the 30-day LCR, ILAAP requires demonstrating that the funding structure is sustainable. The key analysis:</p>

    <p><strong>Maturity mismatch.</strong> What proportion of funding is short-term (&lt;30 days, &lt;3 months, &lt;1 year) vs long-term? A large maturity mismatch means the bank is refinancing frequently - which creates rollover risk if wholesale markets close.</p>

    <p><strong>Funding concentration.</strong> Reliance on a small number of large depositors is an ILAAP weakness. The PRA expects analysis of the top 20 depositors' balances as a percentage of total funding. Single depositors &gt;1% of funding should be individually stress-tested.</p>

    <p><strong>Intraday liquidity.</strong> Under Basel III intraday liquidity rules, ILAAP should also demonstrate the bank can meet intraday payment obligations without relying on incoming payments to fund outflows. This requires real-time payment system data - it's the most data-intensive part of ILAAP.</p>

    <h2>Common ILAAP model failures</h2>

    <ul>
      <li><strong>Run-off rates not bank-specific.</strong> Using LCR minimum run-off rates as the ILAAP stress rate misses the point. ILAAP should use rates calibrated to your deposit mix, depositor behaviour, and concentration. Post-SVB, regulators expect to see evidence of that calibration.</li>
      <li><strong>Static funding base in the stress.</strong> The model should project the funding book day-by-day, applying run-off rates and capturing any contractual maturities. A static LCR ratio isn't the same as a dynamic survival horizon.</li>
      <li><strong>Contingent funding not modelled.</strong> HQLA includes assets that can be monetised in stress - repo facilities, FHLB (US) or central bank standing facilities (UK). These need to be modelled at their stressed availability, not par value. A repo facility with a 10% overcollateralisation requirement only provides 90p of liquidity per £1 of collateral.</li>
      <li><strong>ILAAP buffer = LCR surplus.</strong> Regulators increasingly view the ILAAP buffer as a separate management buffer above LCR, not just whatever's left after hitting 100% LCR. Framing it as the surplus overstates the actual headroom.</li>
    </ul>

    <h2>The ILAAP model in Excel</h2>

    <p>An ILAAP model needs to:</p>
    <ul>
      <li>Calculate HQLA by asset class with Level 1/2A/2B haircuts applied</li>
      <li>Project net outflows day-by-day over 30 days using stressed run-off rates by product and depositor type</li>
      <li>Calculate LCR: HQLA &divide; Net stressed outflows, vs 100% minimum</li>
      <li>Calculate NSFR: Available Stable Funding &divide; Required Stable Funding, vs 100% minimum</li>
      <li>Project the survival horizon under the combined stress scenario</li>
      <li>Show the maturity profile of assets vs liabilities by time bucket</li>
      <li>Flag concentration risks (top 20 depositors, wholesale &gt;X% of total)</li>
      <li>Switch between scenarios (Base, Stress, Severe Stress) from a single INPUTS dropdown</li>
    </ul>

    <div class="blog-cta">
      <h3>ILAAP Model - Excel Template</h3>
      <p>Institutional-grade ILAAP model for bank Treasury and ALM teams. Covers LCR (HQLA with haircuts, net stressed outflows), NSFR, survival horizon projection, maturity analysis, and funding concentration. Full scenario switching, open formulas, CHECKS tab.</p>
      <p><a href="/ilaap-model-excel.html" class="btn btn-primary">View the ILAAP Model &rarr;</a></p>
    </div>

    <h2>ICAAP and ILAAP: running them together</h2>

    <p>In the SREP cycle, regulators review ICAAP and ILAAP together. The interaction matters: a capital stress that drives losses can deplete HQLA (cash used to absorb losses is HQLA reduced). Conversely, a liquidity stress that requires asset fire-sales can drive capital losses if assets are sold below book value.</p>

    <p>For a complete Pillar 2 submission, you need both. ICAAP covering the capital adequacy question, ILAAP covering the liquidity question, and a section that addresses the interaction between the two. See our <a href="/icaap-model-excel.html">ICAAP model</a> for the capital-side counterpart.</p>

    <p style="color:var(--text-muted); font-size: 0.85rem; margin-top: 3rem;">Published 2026-05-11. SFS Models builds institutional-grade Excel financial models for bank Treasury, ALM, and Capital teams. <a href="/models.html">View all models.</a></p>""",
    },
    {
        "slug": 'pe-fund-waterfall-model',
        "title": 'Private Equity Fund Waterfalls: American vs European Structure',
        "h1": 'Private Equity Fund Waterfalls: American vs European Structure',
        "keyword": 'pe fund waterfall american vs european',
        "meta_desc": 'How PE fund distribution waterfalls work. American vs European structure, preferred return, catch-up, carried interest, clawback - with Excel implementation notes.',
        "published": '2026-05-11',
        "summary": "The distribution waterfall is the mechanism that determines how a PE fund splits returns between LPs and the GP. Getting it wrong means either LPs get less than they should, or the GP takes carry they haven't earned. Here's the full mechanics.",
        "product_link": '/lbo-model-excel.html',
        "product_name": 'LBO Model',
        "body": """<p>A private equity fund waterfall is a sequence of distribution tiers that determines the order and proportion in which proceeds from fund realisations are paid to Limited Partners (LPs) and the General Partner (GP). Every PE fund has one. The terms are negotiated at fund formation and written into the LPA (Limited Partnership Agreement). Once set, they govern every distribution for the life of the fund.</p>

    <p>The two dominant structures - American and European - differ in one critical way: timing of when the GP receives carried interest.</p>

    <h2>The four standard tiers</h2>

    <p>Most waterfall structures have four tiers, applied in sequence:</p>

    <table>
      <tr><th>Tier</th><th>Recipient</th><th>What it covers</th></tr>
      <tr><td>1. Return of capital</td><td>LPs</td><td>LPs receive back 100% of contributed capital (including management fees paid to GP)</td></tr>
      <tr><td>2. Preferred return</td><td>LPs</td><td>LPs receive a preferred return (hurdle rate) on contributed capital - typically 8% p.a., compounding</td></tr>
      <tr><td>3. GP catch-up</td><td>GP</td><td>GP receives 100% of distributions until the GP has received a defined % of total profit (typically 20% of total profit, not just profit above the hurdle)</td></tr>
      <tr><td>4. Carried interest split</td><td>80/20 LP/GP</td><td>Remaining distributions split: 80% to LPs, 20% to GP (standard carry)</td></tr>
    </table>

    <p>The hurdle rate (preferred return) is the critical threshold. Until LPs have received their capital back plus the hurdle, the GP receives nothing from Tier 2 onwards. Only after the hurdle is cleared does the GP catch-up mechanism activate.</p>

    <h2>American waterfall: deal-by-deal carry</h2>

    <p>The American (or deal-by-deal) waterfall calculates and distributes carry on each deal as it exits, rather than waiting for the fund as a whole to return capital and the hurdle.</p>

    <p><strong>How it works:</strong></p>
    <ol>
      <li>Deal 1 exits with a 3x return</li>
      <li>LPs receive their pro-rata capital back for Deal 1</li>
      <li>LPs receive the hurdle on that capital</li>
      <li>GP receives catch-up on Deal 1 profits</li>
      <li>Remaining profits split 80/20 LP/GP</li>
      <li>→ GP gets carry from Deal 1 now, regardless of what happens to Deals 2-10</li>
    </ol>

    <p><strong>The problem:</strong> If Deals 2-5 subsequently lose money, LPs have already paid carry on Deal 1. Without a clawback provision, the GP keeps that carry even though the fund overall may not have cleared the hurdle. This is why American structures typically include clawback provisions - contractual obligations for the GP to return carry if the fund fails to hit the hurdle on a whole-fund basis at wind-down.</p>

    <p><strong>Who uses it:</strong> Common in US PE funds. More GP-friendly (accelerates carry). Requires strong clawback language to protect LPs.</p>

    <h2>European waterfall: whole-fund carry</h2>

    <p>The European (or whole-fund) waterfall requires the fund to return all LP capital and clear the hurdle across the entire fund before the GP is entitled to any carry.</p>

    <p><strong>How it works:</strong></p>
    <ol>
      <li>All realisations from all deals go into the fund distribution pool</li>
      <li>First: all LPs receive 100% of total contributed capital returned</li>
      <li>Second: LPs receive the preferred return on all contributed capital</li>
      <li>Third: GP catch-up on total fund profits</li>
      <li>Fourth: 80/20 split on remaining profits</li>
    </ol>

    <p><strong>The effect:</strong> The GP receives no carry until every LP has their capital back plus the hurdle. If early exits are strong but later deals lose, the losses must be recovered before GP sees any carry. This is more LP-protective by design.</p>

    <p><strong>Who uses it:</strong> Standard in European PE. Increasingly common in US VC. More LP-friendly, fewer clawback disputes.</p>

    <h2>Worked example</h2>

    <p>Fund size: £100m. Management fee: 2% p.a. on committed capital (£2m/year, 5-year investment period = £10m total fees, deducted from LP capital). Hurdle: 8% p.a. compounded. Carry: 20%. Deal-by-deal vs whole-fund.</p>

    <p><strong>Scenario:</strong> Fund has three deals. Deal A returns £80m on £40m invested (2x). Deal B returns £30m on £40m invested (0.75x - a loss). Deal C is not yet exited.</p>

    <p>Under <strong>American waterfall</strong>: Deal A exit triggers carry calculation on Deal A. LP gets £40m capital back + 8% hurdle on £40m over hold period. GP gets catch-up and then 20% carry on Deal A profits. Deal B's loss doesn't affect what's already been paid.</p>

    <p>Under <strong>European waterfall</strong>: Deal A proceeds go into the pool. LP capital returned = £40m (Deal A) + £40m (Deal B) + management fees = £90m+ before any preferred return. Deal A's profits must absorb Deal B's losses. Only after the whole fund has returned capital and the hurdle does the GP see carry.</p>

    <h2>The catch-up mechanic</h2>

    <p>The catch-up clause is frequently misunderstood. It does NOT give the GP 100% of all distributions forever. It gives the GP 100% of distributions temporarily, until the GP has received exactly 20% of total fund profit (or whatever the carry percentage is).</p>

    <p>Example: Total fund profit after returning capital and paying the preferred return = £50m. GP's 20% carry = £10m. The catch-up period continues until the GP has received £10m. After that, the 80/20 split applies to all remaining distributions.</p>

    <p>In Excel, the catch-up is typically modelled as:</p>
    <pre><code>GP_catchup = MIN(distributions_available, MAX(0, target_GP_carry - GP_carry_received_so_far))</code></pre>

    <p>Where <code>target_GP_carry = total_fund_profit × carry_rate</code> and the calculation is iterative if distributions happen over multiple periods.</p>

    <h2>Clawback provisions</h2>

    <p>A clawback requires the GP (or the GP's principals) to return carry that was received if, at fund wind-down, the GP has received more carry than it was entitled to on a whole-fund basis.</p>

    <p>Clawbacks are common in American waterfall funds. The practical challenge: by the time the fund winds down, principals may have left the firm, taxes on carry distributions have been paid, and recovering cash years later is difficult. Good LP due diligence checks whether the clawback is guaranteed by the principals personally or just the GP entity (which may have limited assets).</p>

    <h2>Building a waterfall model in Excel</h2>

    <p>A fund waterfall model needs to handle:</p>
    <ul>
      <li><strong>Capital account tracking:</strong> LP contributions by period, management fees deducted, total LP contributed capital</li>
      <li><strong>Preferred return accumulation:</strong> 8% compounded on unreturned capital (XIRR logic, not simple interest)</li>
      <li><strong>Deal proceeds allocation:</strong> which deal proceeds go to which LP (by ownership %)</li>
      <li><strong>Tier-by-tier waterfall:</strong> MAX(0, ...) and MIN(available, remaining_entitlement) at each tier</li>
      <li><strong>Carry ledger:</strong> running total of carry paid vs earned, to catch clawback positions</li>
      <li><strong>IRR and MOIC:</strong> LP net IRR (after fees and carry), GP net IRR, fund gross IRR</li>
    </ul>

    <p>The trickiest part is the catch-up, because it requires knowing total fund profit before you can calculate the GP's entitlement - which creates a forward reference in a period-by-period model. The cleanest solution: calculate the catch-up in two passes, or restructure the model so fund-level totals are calculated first, then allocated to periods.</p>

    <div class="blog-cta">
      <h3>PE Fund Waterfall Model - Excel Template</h3>
      <p>Institutional-grade PE fund model covering American and European waterfall structures, preferred return, catch-up, carried interest, clawback, GP and LP IRR, and MOIC. Switchable between waterfall types from the INPUTS tab. Fully open formulas, CHECKS tab, deal-level and fund-level outputs.</p>
      <p><a href="/pe-fund-waterfall-model-excel.html" class="btn btn-primary">View the PE Fund Waterfall Model &rarr;</a></p>
    </div>

    <h2>LBO vs fund waterfall: the key difference</h2>

    <p>A common point of confusion: the LBO model waterfall is not the same as the fund waterfall. The LBO waterfall allocates equity returns among the different capital tranches in a single deal (common equity, preferred equity, management equity). The fund waterfall allocates fund-level distributions between LPs and the GP across all deals.</p>

    <p>They're both waterfalls, but at different levels of aggregation. A complete PE fund model needs both: the LBO waterfall for each deal, feeding into the fund waterfall for overall LP/GP economics. If you're building one level only, make sure you're clear about which level the question is asking about.</p>

    <p style="color:var(--text-muted); font-size: 0.85rem; margin-top: 3rem;">Published 2026-05-11. SFS Models builds institutional-grade Excel financial models for PE firms, bank Finance teams, and investment managers. <a href="/models.html">View all models.</a></p>""",
    },
]


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | SFS Models Blog</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://sfsmodels.org/blog/{slug}.html">

<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://sfsmodels.org/blog/{slug}.html">
<meta property="og:site_name" content="SFS Models">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "description": "{meta_desc}",
  "datePublished": "{published}",
  "dateModified": "{published}",
  "author": {{ "@type": "Organization", "name": "SFS Models", "url": "https://sfsmodels.org" }},
  "publisher": {{ "@type": "Organization", "name": "SFS Models", "url": "https://sfsmodels.org" }},
  "mainEntityOfPage": "https://sfsmodels.org/blog/{slug}.html"
}}
</script>

<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23C9A84C'/><text x='16' y='23' font-family='system-ui' font-size='20' font-weight='700' fill='%230A0C10' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<style>
.blog-post {{ max-width: 720px; margin: 0 auto; padding: 2rem 0; }}
.blog-post h1 {{ font-family: 'DM Serif Display', serif; font-size: 2.4rem; line-height: 1.15; margin-bottom: 0.5rem; }}
.blog-post .meta {{ color: var(--text-muted); font-size: 0.9rem; margin-bottom: 2rem; }}
.blog-post .summary {{ font-size: 1.15rem; line-height: 1.55; padding: 1rem 1.25rem; border-left: 3px solid #C9A84C; background: rgba(201,168,76,0.05); margin-bottom: 2rem; }}
.blog-post h2 {{ font-family: 'DM Serif Display', serif; font-size: 1.55rem; margin-top: 2.2rem; margin-bottom: 0.6rem; }}
.blog-post p, .blog-post li {{ line-height: 1.7; font-size: 1.02rem; }}
.blog-post pre {{ background: rgba(0,0,0,0.06); padding: 0.9rem 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.92rem; }}
.blog-post code {{ font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace; }}
.blog-post a {{ color: #C9A84C; }}
.blog-cta {{ margin: 3rem 0; padding: 1.5rem; border: 1px solid #C9A84C; border-radius: 8px; }}
.blog-cta h3 {{ margin-top: 0; font-family: 'DM Serif Display', serif; }}
</style>
<!-- SFS-ANALYTICS -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "7852444a13cc4cc78cdb4162c284e1de"}}'></script>
<!-- /SFS-ANALYTICS -->
</head>
<body>

<a href="#main-content" class="skip-link">Skip to main content</a>

<header class="site-header">
  <div class="container">
    <nav class="nav-inner">
      <a href="/index.html" class="logo">SFS Models</a>
      <ul class="nav-links">
        <li><a href="/models.html">Models</a></li>
        <li><a href="/previews.html">Preview Models</a></li>
        <li><a href="/free-samples.html">Free Samples</a></li>
        <li><a href="/about.html">About</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
      <div class="nav-cta">
        <a href="/contact.html" class="btn btn-primary btn-sm">Get a Custom Model</a>
      </div>
      <button class="hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </nav>
  </div>
</header>

<main id="main-content">
  <article class="container blog-post">
    <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom: 0.5rem;"><a href="/" style="color:var(--text-muted);">Home</a> &middot; <a href="/blog/" style="color:var(--text-muted);">Blog</a></p>
    <h1>{h1}</h1>
    <p class="meta">Published {published} &middot; SFS Models</p>
    <p class="summary">{summary}</p>

    {body}

    <div class="blog-cta">
      <h3>Get the {product_name}</h3>
      <p>The model that puts the principles in this post into practice. Bank-grade build, open formulas, no VBA. Same-day delivery.</p>
      <p><a href="{product_link}" class="btn btn-primary">View {product_name}</a> &nbsp; <a href="/free-sample.html" class="btn btn-secondary">Try Free Sample</a></p>
    </div>

    <p style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(0,0,0,0.1); font-size:0.95rem;">SFS Models builds institutional-grade Excel financial models for banking and finance professionals. <a href="/models.html">Browse the catalogue</a> or get the <a href="/free-sample.html">free sample</a>.</p>
  </article>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/index.html" class="logo">SFS Models</a>
        <p>Institutional-grade financial models for banks, fintechs, and advisory firms. Pre-built or custom.</p>
      </div>
      <div class="footer-col">
        <h4>Models</h4>
        <ul>
          <li><a href="/models.html#banking-lending">Banking &amp; Lending</a></li>
          <li><a href="/models.html#treasury-capital-markets">Treasury</a></li>
          <li><a href="/models.html#risk-regulatory">Risk &amp; Regulatory</a></li>
          <li><a href="/models.html#valuation-corporate-finance">Valuation</a></li>
          <li><a href="/models.html#fpa-management-reporting">FP&amp;A</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/about.html">About</a></li>
          <li><a href="/about.html#methodology">Methodology</a></li>
          <li><a href="/pricing.html#faq">FAQ</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 SFS Models. All rights reserved.</span>
      <span><a href="/terms.html">Terms &amp; Conditions</a> &middot; <a href="/privacy.html">Privacy Policy</a> &middot; London, UK &middot; sfsmodels362@gmail.com</span>
    </div>
  </div>
</footer>

<script src="/js/scripts.js"></script>
</body>
</html>
"""


def main():
    out_dir = Path(__file__).parent / "blog"
    out_dir.mkdir(exist_ok=True)
    for p in POSTS:
        html = PAGE_TEMPLATE.format(**p)
        out_path = out_dir / f"{p['slug']}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"Wrote blog/{p['slug']}.html ({len(html):,} bytes)")

    # Build a simple /blog/index.html
    # Weekly research editions (The UK Banking Market Review) lead the list.
    # Newest first. Each is a static page under /research/, built outside this
    # script by the uk-banking-review pipeline; add one entry per edition.
    RESEARCH = [
        {"url": "/research/uk-banking-review-2026-w37.html",
         "title": "The UK Banking Market Review, Week 37 2026",
         "summary": "Free weekly review. High-LTV lending at a 2008 high, Aldermore's accounts taken apart as bids arrive, the repricing split and bank tax proposals, with last week's calls graded.",
         "published": "2026-09-13"},
    ]
    items = []
    for r in RESEARCH:
        items.append(
            f'<li style="margin-bottom:1.5rem;"><a href="{r["url"]}" style="color:#C9A84C; font-size:1.15rem; font-weight:600;">{r["title"]}</a><br><span style="color:var(--text-muted); font-size:0.95rem;">{r["summary"]}</span><br><span style="color:var(--text-muted); font-size:0.85rem;">Published {r["published"]}</span></li>'
        )
    for p in POSTS:
        items.append(
            f'<li style="margin-bottom:1.5rem;"><a href="/blog/{p["slug"]}.html" style="color:#C9A84C; font-size:1.15rem; font-weight:600;">{p["title"]}</a><br><span style="color:var(--text-muted); font-size:0.95rem;">{p["summary"]}</span><br><span style="color:var(--text-muted); font-size:0.85rem;">Published {p["published"]}</span></li>'
        )
    index_body = "\n".join(items)
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog | SFS Models</title>
<meta name="description" content="Banking, finance, and modelling articles from SFS Models. Bank-grade Excel financial models for finance professionals.">
<link rel="canonical" href="https://sfsmodels.org/blog/">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23C9A84C'/><text x='16' y='23' font-family='system-ui' font-size='20' font-weight='700' fill='%230A0C10' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css">
<!-- SFS-ANALYTICS -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "7852444a13cc4cc78cdb4162c284e1de"}}'></script>
<!-- /SFS-ANALYTICS -->
</head>
<body>
<a href="#main-content" class="skip-link">Skip to main content</a>
<header class="site-header"><div class="container"><nav class="nav-inner"><a href="/index.html" class="logo">SFS Models</a><ul class="nav-links"><li><a href="/models.html">Models</a></li><li><a href="/previews.html">Preview Models</a></li><li><a href="/free-samples.html">Free Samples</a></li><li><a href="/about.html">About</a></li><li><a href="/contact.html">Contact</a></li></ul></nav></div></header>
<main id="main-content">
<section class="page-hero"><div class="container"><h1>Blog</h1><p>Banking, finance, and modelling articles. New posts weekly.</p></div></section>
<section class="section"><div class="container" style="max-width:760px;"><ul style="list-style:none; padding:0;">
{index_body}
</ul></div></section>
</main>
<footer class="site-footer"><div class="container"><div class="footer-bottom"><span>&copy; 2026 SFS Models. All rights reserved.</span><span><a href="/terms.html">Terms</a> &middot; <a href="/privacy.html">Privacy</a> &middot; London, UK &middot; sfsmodels362@gmail.com</span></div></div></footer>
</body>
</html>
"""
    (out_dir / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Wrote blog/index.html ({len(index_html):,} bytes)")


if __name__ == "__main__":
    main()
