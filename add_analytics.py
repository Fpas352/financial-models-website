"""
Inject the analytics snippet into every page on sfsmodels.org.

Run:
    cd financial-models-website && python3 add_analytics.py

Idempotent. Re-running replaces the existing block rather than stacking copies,
so it is safe to run after every build.

Two jobs:
  1. Injects the snippet into every .html file in the site.
  2. Patches the head template inside each build_*.py so regenerated pages keep
     it. Without step 2 the next `python3 build_blog_posts.py` silently strips
     analytics from all 15 blog posts.

Provider is set below. Default is Cloudflare Web Analytics: free, cookieless,
and therefore no consent banner is required under PECR / UK GDPR. GA4 is
supported but sets cookies, which means a consent banner and a privacy policy
change before it may lawfully run.

TOKEN is a placeholder until Fjordi creates the property. With the placeholder
in place the tag is inert by design: it does not load, does not phone home, and
does not look installed when it is not.
"""

from pathlib import Path
import argparse
import re

PROVIDER = "cloudflare"          # "cloudflare" | "ga4"
TOKEN = "7852444a13cc4cc78cdb4162c284e1de"    # set here, or pass --token on the command line

# The Cloudflare beacon token is not a secret. It ships in the page source of
# every site that uses it, so it is safe in this file and safe in chat. A GA4
# measurement ID is the same. Neither is an API key.

SENTINEL_OPEN = "<!-- SFS-ANALYTICS -->"
SENTINEL_CLOSE = "<!-- /SFS-ANALYTICS -->"

SITE = Path(__file__).parent
BUILD_SCRIPTS = [
    "build_blog_posts.py",
    "build_seo_landing_pages.py",
    "build_notify_landing_pages.py",
]


def snippet(for_template: bool = False) -> str:
    """The analytics block.

    `for_template=True` doubles every brace. The build scripts render their
    pages with str.format(), which treats a literal {"token": "..."} as a
    format field and dies with KeyError: '"token"'. Doubling escapes it back to
    a single brace in the rendered output.
    """
    s = _snippet_raw()
    return s.replace("{", "{{").replace("}", "}}") if for_template else s


def _snippet_raw() -> str:
    if TOKEN == "__ANALYTICS_TOKEN__":
        body = (
            "<!-- Analytics not yet live. Set TOKEN in add_analytics.py and "
            "re-run. Deliberately inert so an unconfigured site cannot look "
            "instrumented. -->"
        )
    elif PROVIDER == "cloudflare":
        body = (
            '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            f"data-cf-beacon='{{\"token\": \"{TOKEN}\"}}'></script>"
        )
    elif PROVIDER == "ga4":
        body = (
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={TOKEN}"></script>\n'
            "<script>window.dataLayer=window.dataLayer||[];"
            "function gtag(){dataLayer.push(arguments);}"
            "gtag('js',new Date());"
            f"gtag('config','{TOKEN}');</script>"
        )
    else:
        raise SystemExit(f"Unknown PROVIDER: {PROVIDER}")
    return f"{SENTINEL_OPEN}\n{body}\n{SENTINEL_CLOSE}"


BLOCK = re.compile(
    re.escape(SENTINEL_OPEN) + r".*?" + re.escape(SENTINEL_CLOSE),
    re.DOTALL,
)


def inject(text: str) -> tuple[str, bool]:
    """Insert or replace the analytics block immediately before </head>."""
    if BLOCK.search(text):
        return BLOCK.sub(lambda _: snippet(), text), True
    if "</head>" not in text:
        return text, False
    return text.replace("</head>", f"{snippet()}\n</head>", 1), True


def main() -> None:
    global TOKEN, PROVIDER

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--token", help="Cloudflare beacon token or GA4 measurement ID")
    ap.add_argument("--provider", choices=["cloudflare", "ga4"])
    args = ap.parse_args()

    if args.token:
        TOKEN = args.token.strip()
    if args.provider:
        PROVIDER = args.provider

    # Reject anything that is obviously a placeholder rather than a real token.
    # Without this a copy-pasted "PASTE_TOKEN_HERE" ships a dead beacon to every
    # page and the site looks instrumented when it measures nothing.
    if TOKEN != "__ANALYTICS_TOKEN__":
        looks_placeholder = (
            TOKEN.upper() == TOKEN and ("_" in TOKEN or " " in TOKEN)
        ) or TOKEN.lower() in {"token", "your_token", "paste_token_here"}
        valid = (
            re.fullmatch(r"[0-9a-f]{32}", TOKEN) if PROVIDER == "cloudflare"
            else re.fullmatch(r"G-[A-Z0-9]{8,12}", TOKEN)
        )
        if looks_placeholder or not valid:
            expected = (
                "a 32-character hex string, e.g. 3f8a1c9e40b2478da6e5c07b19fd23a4"
                if PROVIDER == "cloudflare" else "a GA4 ID, e.g. G-ABCD123456"
            )
            raise SystemExit(
                f"Refusing to install {TOKEN!r}: that is not a valid "
                f"{PROVIDER} token.\nExpected {expected}.\n"
                "Nothing was changed."
            )

    # Persist the value so a later bare run, or a run after a rebuild, keeps it.
    if TOKEN != "__ANALYTICS_TOKEN__":
        me = Path(__file__)
        src = me.read_text(encoding="utf-8")
        src = re.sub(r'^TOKEN = "[^"]*"', f'TOKEN = "{TOKEN}"', src, count=1, flags=re.M)
        src = re.sub(r'^PROVIDER = "[^"]*"', f'PROVIDER = "{PROVIDER}"', src, count=1, flags=re.M)
        me.write_text(src, encoding="utf-8")

    changed = skipped = 0

    for path in sorted(SITE.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated, ok = inject(original)
        if not ok:
            print(f"  no <head>, skipped: {path.relative_to(SITE)}")
            skipped += 1
            continue
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"pages: {changed} written, {skipped} skipped")

    # Patch the generators so a rebuild does not strip the tag.
    for name in BUILD_SCRIPTS:
        script = SITE / name
        if not script.exists():
            print(f"  missing build script: {name}")
            continue
        original = script.read_text(encoding="utf-8")
        block = snippet(for_template=True)
        if BLOCK.search(original):
            updated = BLOCK.sub(lambda _: block, original)
        else:
            # Every </head> in these files is a template literal, not real markup.
            updated = original.replace("</head>", f"{block}\n</head>")
        if updated != original:
            script.write_text(updated, encoding="utf-8")
            n = original.count("</head>")
            print(f"  patched {name} ({n} template{'s' if n != 1 else ''})")

    if TOKEN == "__ANALYTICS_TOKEN__":
        print(
            "\nTOKEN is still the placeholder, so nothing is being measured yet.\n"
            "Cloudflare Web Analytics, free, about three minutes:\n"
            "  1. dash.cloudflare.com > Analytics & Logs > Web Analytics > Add a site\n"
            "  2. Enter sfsmodels.org and copy the beacon token\n"
            "  3. Put it in TOKEN above, re-run this script, redeploy\n"
        )


if __name__ == "__main__":
    main()
