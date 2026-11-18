"""
Add a "Follow SFS Models on LinkedIn" link to every page footer.

Idempotent, like add_analytics.py: safe to run any number of times. It patches
every .html in the site and the footer templates inside the build_*.py
generators, so pages they regenerate keep the link. Run it after any build:

    cd financial-models-website && python3 add_linkedin_follow.py

Two footer shapes exist:
  - full footer: a paragraph is added under the brand blurb in .footer-brand
  - compact footer (404, blog and research indexes): a "LinkedIn" link is
    added to the .footer-bottom line after the email address
"""

from pathlib import Path

ROOT = Path(__file__).parent
URL = "https://www.linkedin.com/company/sfs-models/"
MARK = "<!-- SFS-LINKEDIN -->"

BRAND_ANCHOR = "Pre-built or custom.</p>"
BRAND_ADD = (
    BRAND_ANCHOR
    + f'\n          {MARK}<p class="footer-follow" style="margin-top:0.75rem;">'
    + f'<a href="{URL}" target="_blank" rel="noopener" style="color:#C9A84C;">'
    + "Follow SFS Models on LinkedIn &rarr;</a></p>"
)

BOTTOM_ANCHOR = "sfsmodels362@gmail.com</span>"
BOTTOM_ADD = (
    f'sfsmodels362@gmail.com &middot; {MARK}<a href="{URL}" target="_blank" '
    'rel="noopener">LinkedIn</a></span>'
)


def patch(text):
    if MARK in text:
        return text, False
    if BRAND_ANCHOR in text:
        return text.replace(BRAND_ANCHOR, BRAND_ADD), True
    if BOTTOM_ANCHOR in text:
        return text.replace(BOTTOM_ANCHOR, BOTTOM_ADD), True
    return text, False


def main():
    targets = sorted(
        list(ROOT.glob("*.html"))
        + list(ROOT.glob("blog/*.html"))
        + list(ROOT.glob("research/*.html"))
        + list(ROOT.glob("build_*.py"))
    )
    done, skipped = [], []
    for p in targets:
        text = p.read_text(encoding="utf-8")
        new, changed = patch(text)
        if changed:
            p.write_text(new, encoding="utf-8")
            done.append(p.relative_to(ROOT).as_posix())
        elif MARK not in text:
            skipped.append(p.relative_to(ROOT).as_posix())
    print(f"patched {len(done)}")
    if skipped:
        print("no footer found (left alone):", ", ".join(skipped))


if __name__ == "__main__":
    main()
