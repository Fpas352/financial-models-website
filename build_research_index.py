#!/usr/bin/env python3
"""Build /research/index.html: the Method Notes page.

Reads research/notes.json, which build_method_notes.py writes when it renders
the PDFs. To add a note: write it in build_method_notes.py, run that script,
then run this one, then python3 add_analytics.py.

The URL stays /research/ so links already sent out keep working. The old
UK Banking Market Review edition (research/uk-banking-review-2026-w37.*) stays
at its own URL but is no longer listed here.
"""
import json, html
from pathlib import Path
HERE = Path(__file__).parent
notes = sorted(json.loads((HERE / "research" / "notes.json").read_text()), key=lambda n: n["no"])
h = html.escape


def card(n):
    return f'''
    <article class="note">
      <div class="note-meta">No. {n["no"]} &middot; {h(n["topic"])} &middot; {h(n["date_label"])} &middot; PDF</div>
      <h2><a href="{h(n["pdf"])}">{h(n["title"])}</a></h2>
      <p>{h(n["summary"])}</p>
      <p class="note-links"><a href="{h(n["pdf"])}" class="btn btn-primary btn-sm">Download PDF</a>
        <a href="/{h(n["model_url"])}" class="note-model">{"Applies to: the full model catalogue" if n["model_url"] == "models.html" else "Related model: " + h(n["model_name"])}</a></p>
    </article>'''


items = "".join(card(n) for n in notes)
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Method Notes: How Banking Models Are Built | SFS Models</title>
<meta name="description" content="Methodology notes from SFS Models on IFRS 9 staging and SICR, lifetime PD and forward-looking adjustments, and credit stress testing of capital, with worked figures. Free PDF downloads.">
<link rel="canonical" href="https://sfsmodels.org/research/">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23C9A84C'/><text x='16' y='23' font-family='system-ui' font-size='20' font-weight='700' fill='%230A0C10' text-anchor='middle'>S</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
<style>
  .notes-wrap {{ max-width: 780px; }}
  .notes-intro {{ color: var(--text-muted, #8A8880); margin-bottom: 0.5rem; }}
  .note {{ border-top: 1px solid rgba(201,168,76,0.25); padding: 2rem 0; }}
  .note h2 {{ font-family: "DM Serif Display", Georgia, serif; font-size: 1.7rem; line-height: 1.25; margin: 0.35rem 0 0.6rem; }}
  .note h2 a {{ color: var(--text, #E8E6E0); text-decoration: none; }}
  .note h2 a:hover {{ color: #C9A84C; }}
  .note-meta {{ color: #C9A84C; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.02em; }}
  .note p {{ color: var(--text-muted, #8A8880); }}
  .note-links {{ display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem 1.25rem; margin-top: 1rem; }}
  .note-model {{ color: #C9A84C; font-weight: 600; text-decoration: none; }}
  .note-model:hover {{ text-decoration: underline; }}
  .notes-about {{ color: var(--text-muted, #8A8880); font-size: 0.95rem; border-top: 1px solid rgba(201,168,76,0.25); padding-top: 1.5rem; }}
  .notes-about a {{ color: #C9A84C; font-weight: 600; }}
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
          <li><a href="/research/" class="active">Method Notes</a></li>
          <li><a href="/about.html">About</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
        <div class="nav-cta">
          <a href="/contact.html" class="btn btn-primary btn-sm">Get a Custom Model</a>
        </div>
        <button class="hamburger" aria-label="Menu" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </nav>
    </div>
  </header>
<main id="main-content">
<section class="page-hero"><div class="container"><h1>Method Notes</h1><p>Methodology notes on how our banking models are built. Each note covers one modelling question, with worked figures from the demo data supplied with the related model. Free to download as PDF.</p></div></section>
<section class="section"><div class="container notes-wrap">
{items}
  <div class="notes-about">
    <p>Written by SFS Models. The figures in each note are taken from the demo data in the related model and can be checked against its free sample. The notes describe general methodology and are not accounting, regulatory or investment advice.</p>
    <p>Suggestions for future notes are welcome through the <a href="/contact.html">contact page</a>.</p>
  </div>
</div></section>
</main>
<footer class="site-footer"><div class="container"><div class="footer-bottom"><span>&copy; 2026 SFS Models. All rights reserved.</span><span><a href="/terms.html">Terms</a> &middot; <a href="/privacy.html">Privacy</a> &middot; London, UK &middot; sfsmodels362@gmail.com &middot; <!-- SFS-LINKEDIN --><a href="https://www.linkedin.com/company/sfs-models/" target="_blank" rel="noopener">LinkedIn</a></span></div></div></footer>
<script src="/js/scripts.js"></script>
</body>
</html>
'''
(HERE / "research" / "index.html").write_text(page, encoding="utf-8")
print(f"Wrote research/index.html ({len(notes)} note(s))")
