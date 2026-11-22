"""
Add a "Watch the walkthrough" video section to model landing pages.

Idempotent, like add_linkedin_follow.py: safe to run any number of times. The
section sits straight after the page hero. It shows the YouTube thumbnail with
a play button and only loads the player (from youtube-nocookie.com) when the
visitor clicks, so pages stay fast and no YouTube cookies are set until then.
Each page also gets VideoObject structured data for search.

Video IDs come from marketing/video_production/_upload/youtube_ids.csv. Run it
after any rebuild of the landing pages (build_model_landing_pages.py rewrites
five of these pages from scratch):

    cd financial-models-website && python3 add_walkthrough_videos.py
"""

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
IDS = ROOT.parent / "marketing" / "video_production" / "_upload" / "youtube_ids.csv"
MARK = "<!-- SFS-WALKTHROUGH -->"
END = "<!-- /SFS-WALKTHROUGH -->"

# product key -> landing page
PAGES = {
    "ifrs9-ecl": "ifrs9-cecl-model-excel.html",
    "cecl": "cecl-model-excel.html",
    "irrbb": "irrbb-model-excel.html",
    "ifrs9-loan-level": "ifrs9-loan-level-ecl-model-excel.html",
    "credit-stress-test": "credit-stress-test-model-excel.html",
    "ifrs16-lease": "ifrs16-lease-model-excel.html",
}


def section(vid, model, minutes, published="2026-11-20"):
    thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    return f"""{MARK}
  <section class="section" id="walkthrough">
    <div class="container" style="max-width:860px;">
      <h2>Watch the walkthrough</h2>
      <p style="line-height:1.7; margin-top:0.5rem;">The {html.escape(model)}, tab by tab, in about {minutes} minutes: what each tab does, one assumption changed live, and the integrity checks.</p>
      <div class="sfs-video" data-yt="{vid}" role="button" tabindex="0" aria-label="Play the {html.escape(model)} walkthrough video"
           style="position:relative; margin-top:1.25rem; aspect-ratio:16/9; border-radius:10px; overflow:hidden; cursor:pointer; background:#0f1117 url('{thumb}') center/cover no-repeat; box-shadow:0 8px 30px rgba(0,0,0,0.35);">
        <span style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center;">
          <span style="width:76px; height:76px; border-radius:50%; background:#C9A84C; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 18px rgba(0,0,0,0.4);">
            <span style="display:block; width:0; height:0; margin-left:6px; border-left:24px solid #0f1117; border-top:15px solid transparent; border-bottom:15px solid transparent;"></span>
          </span>
        </span>
      </div>
      <p style="margin-top:0.75rem; font-size:0.9rem; opacity:0.75;">Plays from YouTube. <a href="https://youtu.be/{vid}" target="_blank" rel="noopener" style="color:#C9A84C;">Open on YouTube &rarr;</a></p>
    </div>
  </section>
  <script>
  document.querySelectorAll('.sfs-video').forEach(function (el) {{
    function play() {{
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + el.dataset.yt + '?autoplay=1&rel=0&cc_load_policy=0';
      f.title = el.getAttribute('aria-label');
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.style.cssText = 'position:absolute; inset:0; width:100%; height:100%; border:0;';
      el.innerHTML = '';
      el.appendChild(f);
    }}
    el.addEventListener('click', play, {{ once: true }});
    el.addEventListener('keydown', function (e) {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); play(); }} }});
  }});
  </script>
  <script type="application/ld+json">{json.dumps({
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": f"{model}: walkthrough", "description": f"The {model}, tab by tab, in Excel.",
        "thumbnailUrl": thumb, "uploadDate": f"{published}T00:00:00+00:00",
        "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}",
        "contentUrl": f"https://www.youtube.com/watch?v={vid}"})}</script>
  {END}
"""


def main():
    rows = {r["key"]: r for r in csv.DictReader(IDS.open())}
    ids = {k: r["youtube_id"] for k, r in rows.items()}
    src = (ROOT / "ls-config.js").read_text()
    for key, page in PAGES.items():
        if key not in ids:
            print(f"  skip {page}: no video yet")
            continue
        p = ROOT / page
        s = p.read_text()
        name = re.search(rf'"{re.escape(key)}":\s*\{{[^}}]*?name:\s*"([^"]+)"', src).group(1)
        block = section(ids[key], name, 2.5 if key != "ifrs9-loan-level" else 3, rows[key]["published"])
        if MARK in s:                                   # replace the existing block
            s = re.sub(re.escape(MARK) + r".*?" + re.escape(END) + r"\n", block, s, flags=re.S)
        else:                                           # insert after the hero
            i = s.index('<section class="page-hero"')
            j = s.index("</section>", i) + len("</section>")
            s = s[:j] + "\n\n  " + block + s[j:]
        p.write_text(s)
        print(f"  {page}: {ids[key]}")
    previews(ids, src)


# ── Preview Models page ──────────────────────────────────────────────────────
# Since 22 Nov 2026 each video is a tile in its model's row on previews.html,
# written by build_previews_gallery.py from the same youtube_ids.csv. The old
# "Watch the walkthroughs" block at the top of the page is removed if present.
PMARK, PEND = "<!-- SFS-WALKTHROUGHS -->", "<!-- /SFS-WALKTHROUGHS -->"


def previews(ids, src):
    p = ROOT / "previews.html"
    s = p.read_text()
    if PMARK in s:
        s = re.sub(r"\n*  " + re.escape(PMARK) + r".*?" + re.escape(PEND) + r"\n", "\n", s, flags=re.S)
        p.write_text(s)
        print("  previews.html: removed the top walkthrough block")
    print("  previews.html: videos are tiles in each model's row (run build_previews_gallery.py)")


if __name__ == "__main__":
    main()
