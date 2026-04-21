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

<p>The problem: this formula assumes all of year <code>t</code>'s cash flow arrives on December 31st of year <code>t</code>. In reality, cash flows arrive throughout the year &mdash; roughly evenly. The "average" cash arrives at mid-year (June 30th).</p>

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

<p>If your explicit forecast ends in year 5 and you've used mid-year discounting for years 1&ndash;5, the terminal value (which represents value FROM year 6 onwards) should be discounted at:</p>

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

<p>Sum the PVs of years 1&ndash;n + discounted terminal value = enterprise value.</p>

<p>For our <a href="/dcf-model-excel.html">DCF Model</a>, we built in a toggle on the INPUTS tab &mdash; switch between mid-year and end-of-year and the entire model recalibrates.</p>

<h2>Common mistakes</h2>

<ol>
<li><strong>Discounting terminal value at year n + 1 instead of n.</strong> TV represents value at end of year n, so discount it at year n (or year n &minus; 0.5 for mid-year).</li>
<li><strong>Using mid-year for one year and end-of-year for others.</strong> Be consistent across all years in the explicit forecast.</li>
<li><strong>Ignoring stub periods.</strong> If your valuation date isn't year-end, the first period is a stub (e.g., 7 months). Adjust the discount factor for the stub period accordingly.</li>
<li><strong>Mid-year on a project that ends in year 5.</strong> If the business has a defined termination (project finance), don't use mid-year for the final year &mdash; use the actual cash receipt timing.</li>
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
        "body": """<p>Most US bank ALM models still use deposit beta assumptions calibrated against the 2014&ndash;2019 rate cycle. The 2022&ndash;2025 cycle showed those calibrations were materially wrong. Banks running stale betas understated their NII risk by ~3x heading into the SVB crisis.</p>

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

<p>The previous decade (2010&ndash;2021) was characterised by ZIRP and modest rate moves. Deposit betas calibrated against this period showed:</p>

<ul>
<li>Retail savings: 20&ndash;30%</li>
<li>Commercial deposits: 30&ndash;50%</li>
<li>Institutional / brokered: 60&ndash;80%</li>
</ul>

<p>When rates rose 525bps over 2022&ndash;2023, actual betas were materially higher:</p>

<ul>
<li>Retail savings: 35&ndash;50% (up from 20&ndash;30%)</li>
<li>Commercial deposits: 70&ndash;90% (up from 30&ndash;50%)</li>
<li>Uninsured commercial: 80&ndash;95% (the SVB cohort)</li>
</ul>

<p>The reason: depositors had access to better rate alternatives (T-bills, money market funds yielding 5%+) and digital channels made it easy to move money.</p>

<h2>Why this matters for ALM models</h2>

<p>ALM models project NII under interest rate scenarios. Two key levers:</p>

<ol>
<li>Asset side: how fast do loan yields reprice</li>
<li>Liability side: how fast do deposit rates reprice (driven by deposit beta)</li>
</ol>

<p>If your model assumes 30% beta when actual beta is 80%, in a +200bps shock your modelled NII is materially overstated. Your EVE / NII shock numbers are similarly distorted.</p>

<p>For the 2022&ndash;23 cycle, banks running 2019-vintage betas were modelling NII benefits of ~10&ndash;15%. Actual NII benefits were closer to 3&ndash;5% &mdash; and for some banks (those with high uninsured commercial mix), NII actually compressed.</p>

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

<p>Calibrate against your bank's actual experience over the rising rate cycle. Don't blend with pre-2022 data &mdash; the rate environment was structurally different (digital access, money market yields, etc.).</p>

<p><strong>3. Flex beta in scenarios.</strong></p>

<p>Base case = 2022&ndash;2025 actuals. Adverse scenario = 1.2x base (faster pass-through under stress). Severely adverse = 1.5x base (run-off scenario).</p>

<p><strong>4. Re-calculate EVE / NII shock.</strong></p>

<p>Re-run your standard shock scenarios (+200bps parallel, etc.) with new betas. Expect your numbers to look materially worse than the previous cycle's output. That's the point &mdash; the previous cycle's output was wrong.</p>

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
        "body": """<p>INDIRECT() is one of those small Excel modelling habits that causes outsized pain when models get inherited. It's convenient for building flexible references &mdash; <code>=INDIRECT("'"&amp;A1&amp;"'!B5")</code> &mdash; but it has three properties that should disqualify it from any model that anyone other than the original builder will use.</p>

<h2>1. It's volatile</h2>

<p>Every recalculation re-evaluates every INDIRECT in the workbook. On a 50-tab model with 200 INDIRECT calls, this is the difference between a 0.5s recalc and a 30s recalc. Volatile functions also trigger recalculation when totally unrelated cells change, which makes audits painful.</p>

<h2>2. It breaks silently when sheets are renamed</h2>

<p>No #REF! error. Just wrong numbers. The user has no idea anything went wrong &mdash; the formula still "works", it just points at nothing now and returns 0 or #REF! that's lost in a sea of other values.</p>

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
    items = []
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
