#!/usr/bin/env python3
"""Write the screenshot galleries, facts line and free-sample button into
previews.html as static HTML.

Reads images/previews/manifest.json and images/previews/facts.json (both made
by ../tools/build_preview_images.py from the upload-ready workbooks) and the
free-sample checkout links in ls-config.js. For every model block it writes:

  * a gallery: the chart (or the dashboard if there is no chart) as a large
    lead tile, then inputs, calculation, dashboard and checks, each captioned
    with what it shows; a model with only four pictures gets a free-sample
    tile in the empty slot
  * a facts line under the description: tabs, integrity checks, scenarios
  * a "Free sample" button under "Buy Model"

Safe to re-run: generated parts sit between <!--shots-->, <!--facts--> and
<!--sample--> markers and are replaced each time. A model missing from the
manifest is left as it is.

    python3 build_previews_gallery.py
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
PAGE = HERE / "previews.html"
MANIFEST = HERE / "images/previews/manifest.json"
FACTS = HERE / "images/previews/facts.json"
LS = HERE / "ls-config.js"

TAG = {"inputs": "Inputs", "engine": "Calculation", "outputs": "Dashboard",
       "chart": "Chart", "checks": "Controls"}


def free_urls():
    out = {}
    for m in re.finditer(r'"([a-z0-9-]+)":\s*\{(.*?)\n\s*\}', LS.read_text(), re.S):
        f = re.search(r'freeUrl:\s*"([^"]+)"', m.group(2))
        if f:
            out[m.group(1)] = f.group(1)
    return out


def role_of(i, shot):
    """Role of a manifest entry; older entries carry no role, so infer it."""
    if shot.get("role"):
        return shot["role"]
    lab = shot["label"]
    if lab == "Checks":
        return "checks"
    if i == 0:
        return "inputs"
    if lab.endswith("headline figures"):
        return "outputs"
    return "engine" if i == 1 else "chart"


def and_join(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def caption(role, shot, fact):
    lab = shot["label"]
    if role == "inputs":
        return "Every assumption on one tab"
    if role == "engine":
        return f"{lab} tab, every formula open"
    if role == "outputs":
        return "Headline figures"
    if role == "checks" and fact and fact["checks"]:
        n = fact["checks"]
        return f"{n} integrity checks, all passing" if not fact["failing"] else f"{n} integrity checks"
    if role == "checks":
        return "Integrity checks"
    return lab.split("\n")[0]


def takeaway(role, shot):
    """Second line of a chart's two-line title: the point the chart makes."""
    if role != "chart" or "\n" not in shot["label"]:
        return ""
    return shot["label"].split("\n", 1)[1].strip()


def tile(key, model, shot, role, fact, lead):
    base = f"images/previews/{key}/"
    cap = caption(role, shot, fact)
    alt = f"{model}: {shot['label'].replace(chr(10), '. ')}"
    note = takeaway(role, shot)
    cls = "preview-shot preview-shot--lead" if lead else "preview-shot"
    return (f'<figure class="{cls}" data-src="{base}{shot["file"]}" tabindex="0" role="button" '
            f'aria-label="Enlarge {html.escape(alt)}">'
            f'<img src="{base}{shot["thumb"]}" alt="{html.escape(alt)}" width="720" height="480" '
            f'loading="lazy" decoding="async">'
            f'<figcaption><span>{TAG[role]}</span>{html.escape(cap)}'
            + (f'<small>{html.escape(note)}</small>' if note else '') + '</figcaption></figure>')


def gallery(key, model, shots, fact, free):
    roles = [role_of(i, s) for i, s in enumerate(shots)]
    lead = next((i for want in ("chart", "outputs", "engine")
                 for i, r in enumerate(roles) if r == want), 0)
    order = [lead] + [i for i in range(len(shots)) if i != lead]
    parts = [tile(key, model, shots[i], roles[i], fact, i == lead) for i in order]
    if len(parts) == 4 and free:                   # fill the empty slot in the grid
        parts.append(
            f'<a class="preview-cta" href="{free}" target="_blank" rel="noopener" data-model-id="{key}">'
            f'<strong>See every tab</strong>'
            f'<span>The free sample has every tab, chart and check, with real results on demo data.</span>'
            f'<em>Download the free sample &rarr;</em></a>')
    return "<!--shots-->" + "".join(parts) + "<!--/shots-->"


def facts_line(fact):
    bits = [f'{fact["tabs"]} tabs']
    if fact["checks"]:
        bits.append(f'{fact["checks"]} integrity checks' + ("" if fact["failing"] else ", all passing"))
    if fact["scenarios"]:
        bits.append(f'{and_join(fact["scenarios"])} scenarios')
    bits.append("open formulas, no macros")
    return ('<!--facts--><p class="preview-model__facts">'
            + " &middot; ".join(html.escape(b) for b in bits) + "</p><!--/facts-->")


def main():
    page = PAGE.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text())
    facts = json.loads(FACTS.read_text()) if FACTS.exists() else {}
    free = free_urls()
    done, kept = [], []

    def fill(m):
        info, between, key, shots_html, close = (m.group(1), m.group(2), m.group(3),
                                                 m.group(4), m.group(5))
        shots = manifest.get(key) or []
        fact = facts.get(key)
        # info block: facts line after the description, sample button after Buy
        info = re.sub(r"<!--facts-->.*?<!--/facts-->|<!--sample-->.*?<!--/sample-->", "", info,
                      flags=re.S)
        if fact:
            info = re.sub(r'(<p class="preview-model__desc">.*?</p>)',
                          lambda d: d.group(1) + facts_line(fact), info, count=1, flags=re.S)
        if key in free:
            info = re.sub(r'(class="preview-model__buy">Buy Model</a>)',
                          lambda d: d.group(1) + f'<!--sample--><a href="{free[key]}" target="_blank" '
                          f'rel="noopener" class="preview-model__sample" data-model-id="{key}">'
                          f'Free sample</a><!--/sample-->', info, count=1)
        if not shots or "thumb" not in shots[0]:   # not rendered yet: keep fallback
            kept.append(key)
            return info + between + shots_html + close
        model = html.unescape(re.search(r"<h3>(.*?)</h3>", info).group(1))
        done.append(key)
        return info + between + gallery(key, model, shots, fact, free.get(key)) + close

    pattern = re.compile(
        r'(<div class="preview-model__info">(?:(?!preview-model__info).)*?)'
        r'(</div>\s*<div class="preview-gallery" data-model="([a-z0-9-]+)">)'
        r'((?:<!--shots-->.*?<!--/shots-->)|(?:.*?))'
        r'(</div>\n      </div>)', re.S)
    page = pattern.sub(fill, page)
    PAGE.write_text(page, encoding="utf-8")
    print(f"galleries written: {len(done)}; left as they were: {len(kept)} {kept}")


if __name__ == "__main__":
    main()
