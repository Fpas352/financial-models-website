#!/usr/bin/env python3
"""Turn the 9 stale "coming soon" landing pages into pages that can take money.

Fill checkout_url for each model in wire_up_models.json, then:

    python3 wire_up_models.py --dry-run     # show what would change
    python3 wire_up_models.py               # write it

Refuses to touch a page whose checkout_url is empty, so a half-filled config
cannot produce a page with a Buy button that goes nowhere.
"""
import json, re, sys, shutil, pathlib

DRY = "--dry-run" in sys.argv
ROOT = pathlib.Path(__file__).parent
CFG = json.loads((ROOT / "wire_up_models.json").read_text())

def buy_block(slug, price, url, tabs):
    return f'''  <!-- PURCHASE -->
  <section class="section" style="background:var(--bg-alt, #0f1117);">
    <div class="container" style="max-width:540px; text-align:center;">
      <h2>Get the model</h2>
      <p style="margin-bottom:1.5rem;">Excel (.xlsx) &middot; {tabs} tabs &middot; open formulas, no VBA &middot; same-day delivery</p>
      <a href="{url}" target="_blank" rel="noopener" class="btn btn-primary" style="width:100%; justify-content:center;">Buy Model - &pound;{price:,}</a>
      <p style="color:var(--text-muted); font-size:0.85rem; margin-top:1rem;">14-day money-back guarantee &middot; one-time purchase, no subscription &middot; questions to sfsmodels362@gmail.com</p>
    </div>
  </section>'''

def wire(slug, m):
    path = ROOT / f"{slug}.html"
    if not path.exists():
        return f"SKIP {slug}: no such page"
    url, price, tabs = m.get("checkout_url", ""), m["price"], m["tabs"]
    if not url:
        return f"SKIP {slug}: checkout_url empty, nothing written"
    if "lemonsqueezy.com/checkout" not in url:
        return f"SKIP {slug}: checkout_url does not look like a Lemon Squeezy link"

    h = orig = path.read_text()

    # 1. drop the Coming soon badge
    h = re.sub(r'\s*<p style="background:#C9A84C[^>]*>Coming soon</p>', "", h)

    # 2. replace the whole notify section with a purchase section
    h = re.sub(r'  <!-- NOTIFY FORM -->.*?</section>',
               buy_block(slug, price, url, tabs), h, flags=re.S)

    # 3. JSON-LD: PreOrder -> InStock, and carry a real price
    h = h.replace('"availability": "https://schema.org/PreOrder",',
                  f'"availability": "https://schema.org/InStock",\n    "price": "{price}",\n    "priceCurrency": "GBP",')

    # 4. strip launch-date and expected-pricing language anywhere it survives
    h = re.sub(r'\s*&middot;\s*expected pricing\s*&pound;[\d,]+', "", h)
    h = re.sub(r'\s*&middot;\s*Q[1-4] \d{4} launch target', "", h)
    h = h.replace("Notify when available.", "Available now.")
    h = re.sub(r'>Coming soon<', "><", h)

    if h == orig:
        return f"NOOP {slug}: nothing matched, inspect by hand"
    if not DRY:
        shutil.copy(path, path.with_suffix(".html.bak"))
        path.write_text(h)
    return f"{'WOULD WIRE' if DRY else 'WIRED'} {slug} at GBP {price:,}"

def main():
    results = [wire(s, m) for s, m in CFG["models"].items()]
    for r in results:
        print("  " + r)
    done = sum(1 for r in results if "WIRED" in r)
    print(f"\n{done}/{len(results)} pages wired.")
    if done < len(results):
        print("Fill the remaining checkout_url values in wire_up_models.json and re-run.")
    if done and not DRY:
        print("Backups written as *.html.bak. Next: add matching cards to models.html")
        print("and update the homepage counter, which currently reads 35.")

if __name__ == "__main__":
    main()
