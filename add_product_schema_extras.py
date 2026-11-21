"""
Complete the Product structured data on every page so Google can use it.

Search Console (21 Nov 2026) flagged every Product as missing 'image', which
stops the page appearing as a merchant listing, and paid offers as missing a
return policy. This script, idempotent like add_analytics.py and
add_reading_links.py, fixes both in every page's JSON-LD:

- image: the model's own preview screenshot from images/previews/ (dashboard
  or outputs view first), matched on the page's data-ls-key / data-model-id;
  otherwise the plain brand card images/sfs-models-card.png.
- hasMerchantReturnPolicy on paid offers: returns not permitted, which is the
  site's policy ("all sales are final once the download link has been
  delivered"). Free (price 0) offers are left alone.

Never adds reviews or ratings: none exist. Run it after any page rebuild:

    cd financial-models-website && python3 add_product_schema_extras.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://sfsmodels.org"
CARD = f"{SITE}/images/sfs-models-card.png"
PREFER = re.compile(r"dashboard|output|summary", re.I)
POLICY = {
    "@type": "MerchantReturnPolicy",
    "applicableCountry": "GB",
    "returnPolicyCategory": "https://schema.org/MerchantReturnNotPermitted",
}
BLOCK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def preview_images():
    man = json.loads((ROOT / "images/previews/manifest.json").read_text())
    out = {}
    for key, shots in man.items():
        best = next((s for s in shots if PREFER.search(s["label"])), shots[0])
        out[key] = f"{SITE}/images/previews/{key}/{best['file']}"
    return out


def walk(node, image, counts):
    if isinstance(node, list):
        for n in node:
            walk(n, image, counts)
        return
    if not isinstance(node, dict):
        return
    if node.get("@type") == "Product" and "image" not in node:
        node["image"] = image
        counts["image"] += 1
    if node.get("@type") == "Offer":
        try:
            paid = float(str(node.get("price", "0")).replace(",", "")) > 0
        except ValueError:
            paid = False
        if paid and "hasMerchantReturnPolicy" not in node:
            node["hasMerchantReturnPolicy"] = dict(POLICY)
            counts["policy"] += 1
    for v in node.values():
        walk(v, image, counts)


def main():
    previews = preview_images()
    total = {"pages": 0, "image": 0, "policy": 0}
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text()
        if not re.search(r'"@type":\s*"Product"', text):
            continue
        keys = re.findall(r'data-(?:ls-key|model-id)="([^"]+)"', text)
        own = [previews[k] for k in dict.fromkeys(keys) if k in previews]
        # a single-model page uses its own screenshot; list pages use the card
        image = own[0] if len(set(keys) - {path.stem}) <= 1 and own else CARD
        counts = {"image": 0, "policy": 0}

        def fix(m):
            try:
                data = json.loads(m.group(2))
            except json.JSONDecodeError:
                return m.group(0)
            before = dict(counts)
            walk(data, image, counts)
            if counts == before:
                return m.group(0)
            return m.group(1) + "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n" + m.group(3)

        new = BLOCK.sub(fix, text)
        if new != text:
            path.write_text(new)
            total["pages"] += 1
            total["image"] += counts["image"]
            total["policy"] += counts["policy"]
            print(f"{path.name}: image {'own' if image != CARD else 'card'}, "
                  f"+{counts['image']} image, +{counts['policy']} return policy")
    print(f"done: {total['pages']} pages, {total['image']} images, {total['policy']} return policies")


if __name__ == "__main__":
    main()
