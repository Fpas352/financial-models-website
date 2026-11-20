"""
Add a "Further reading" section to model landing pages, linking each model to
the blog posts and method notes that explain the method behind it.

Idempotent, like add_walkthrough_videos.py and add_linkedin_follow.py: safe to
run any number of times. The section sits just before "About SFS Models". A
link already present elsewhere on the page is not repeated. Run it after any
rebuild of the landing pages:

    cd financial-models-website && python3 add_reading_links.py

Blog titles come from build_blog_posts.py and method-note titles from
research/notes.json, so renamed posts or notes update on the next run.
"""

import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
MARK = "<!-- SFS-READING -->"
END = "<!-- /SFS-READING -->"

# landing page -> (blog slugs, method-note slugs), most relevant first
READING = {
    "irrbb-model-excel.html": (["deposit-beta-calibration"], ["nmd-slotting-delta-eve", "irrbb-standardised-measurement"]),
    "deposit-pricing-nii-model-excel.html": (["deposit-beta-calibration"], ["nmd-slotting-delta-eve"]),
    "bank-deposits-model-excel.html": (["deposit-beta-calibration"], ["nmd-slotting-delta-eve"]),
    "nim-variance-model-excel.html": (["deposit-beta-calibration"], []),
    "ifrs9-cecl-model-excel.html": (["ifrs9-staging-sicr", "ifrs9-ecl-model-excel-build", "cecl-methodology-drift"], ["sicr-staging-triggers", "lifetime-pd-forward-looking"]),
    "ifrs9-loan-level-ecl-model-excel.html": (["ifrs9-staging-sicr", "ifrs9-ecl-model-excel-build"], ["sicr-staging-triggers", "lifetime-pd-forward-looking"]),
    "cecl-model-excel.html": (["cecl-methodology-drift"], []),
    "credit-stress-test-model-excel.html": (["reverse-stress-testing-bank", "ccar-stress-capital-buffer-2026"], ["credit-stress-test-capital"]),
    "bank-stress-test-model.html": (["ccar-stress-capital-buffer-2026", "reverse-stress-testing-bank", "icaap-model-guide"], ["credit-stress-test-capital"]),
    "icaap-model-excel.html": (["icaap-model-guide", "reverse-stress-testing-bank"], ["credit-stress-test-capital"]),
    "bank-capital-model-excel.html": (["icaap-model-guide"], ["credit-stress-test-capital"]),
    "basel-iv-rwa-model-excel.html": (["icaap-model-guide"], []),
    "ilaap-model-excel.html": (["ilaap-liquidity-model"], []),
    "lcr-model-excel.html": (["ilaap-liquidity-model"], []),
    "dcf-model-excel.html": (["mid-year-discounting-dcf"], []),
    "multi-method-valuation-model-excel.html": (["mid-year-discounting-dcf"], []),
    "lbo-model-excel.html": (["lbo-model-debt-sizing", "pe-fund-waterfall-model"], []),
    "debt-schedule-model-excel.html": (["lbo-model-debt-sizing"], []),
    "pe-fund-waterfall-model-excel.html": (["pe-fund-waterfall-model"], []),
    "dividend-discount-model-excel.html": (["wacc-calculation-banking"], []),
    "bank-financial-model.html": (["deposit-beta-calibration", "wacc-calculation-banking"], ["bank-model-build-standards"]),
    "three-statement-model-excel.html": (["excel-financial-model-best-practices"], ["bank-model-build-standards"]),
    "loan-portfolio-model-excel.html": ([], ["bank-model-build-standards"]),
}


def blog_titles():
    spec = importlib.util.spec_from_file_location("blog", ROOT / "build_blog_posts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {p["slug"]: p["title"] for p in mod.POSTS}


def note_titles():
    notes = json.loads((ROOT / "research" / "notes.json").read_text())
    return {n["slug"]: n["title"] for n in notes}


def section(links):
    items = "\n".join(
        f'        <li><a href="{href}" style="color:#C9A84C;">&rarr; {html.escape(label)}</a></li>'
        for label, href in links)
    return f"""{MARK}
  <section class="section">
    <div class="container" style="max-width:760px;">
      <h2>Further reading</h2>
      <p style="line-height:1.7; margin-top:0.5rem;">The method behind the model, written up.</p>
      <ul style="list-style:none; padding:0; margin-top:1.25rem; display:grid; gap:0.75rem;">
{items}
      </ul>
    </div>
  </section>
  {END}
"""


def main():
    blogs, notes = blog_titles(), note_titles()
    anchor = re.compile(r'\n\s*(?:<!--[^>]*-->\s*)?<section[^>]*>\s*<div[^>]*>\s*<h2>About SFS Models</h2>')
    for page, (blog_slugs, note_slugs) in READING.items():
        path = ROOT / page
        text = path.read_text()
        text = re.sub(r"\n\n  " + re.escape(MARK) + r".*?" + re.escape(END) + r"\n", "", text, flags=re.S)
        links = [(f"Blog: {blogs[s]}", f"/blog/{s}.html") for s in blog_slugs]
        links += [(f"Method note (PDF): {notes[s]}", f"/research/notes/{s}.pdf") for s in note_slugs]
        links = [(l, h) for l, h in links if f'href="{h}"' not in text]
        if links:
            m = anchor.search(text)
            if not m:
                raise SystemExit(f"{page}: no 'About SFS Models' section to anchor on")
            text = text[:m.start()] + "\n\n  " + section(links) + text[m.start():]
        path.write_text(text)
        print(f"{page}: {len(links)} link(s)")


if __name__ == "__main__":
    main()
