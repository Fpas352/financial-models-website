# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static marketing website for Banking Models Store — a business selling professional Excel-based financial models. Vanilla HTML/CSS/JS frontend with an optional Express backend for form handling. No build tools, no frameworks, no preprocessors.

## Commands

```bash
# Development server (Python — static files only, no form handling)
cd financial-models-website
python3 serve.py
# → http://localhost:3000

# Production server (Express — static files + API endpoints)
cd financial-models-website/backend
npm install          # first time only
node server.js       # or: npm start
# → http://localhost:3000

# Development with auto-reload (Node 18+)
npm run dev          # uses node --watch
```

There are no tests, linting, or build steps.

## Architecture

**Frontend (6 pages):** `index.html`, `models.html`, `pricing.html`, `about.html`, `contact.html`, `404.html`
- Single stylesheet: `css/style.css` — design system with CSS custom properties in `:root`
- Single script: `js/scripts.js` — 11 features (header, hamburger, smooth scroll, FAQ accordion, catalogue filters, form validation, scroll animations)
- All pages share the same header/footer markup (no templating — copy across files when changing nav)

**Backend (`backend/server.js`):** Express server serving static files from the parent directory + two form API endpoints:
- `POST /api/contact` — contact form (name, email, business_type, message)
- `POST /api/custom-model` — custom model request (business, sector, revenue, employees, description)
- `GET /api/submissions` — dev-only endpoint to view logged submissions
- `GET /api/health` — uptime check

**Form handling has two modes:**
1. **Client-side only (current):** `scripts.js` validates fields and shows a simulated success message after 1.2s timeout. No fetch call to backend.
2. **With backend:** Uncomment the `fetch()` block in `scripts.js` (commented near line 310) and remove the `setTimeout` simulation. Backend validates, logs to `backend/data/*.json`, and optionally emails via nodemailer.

## Key Patterns

**CSS design tokens** — All colours, shadows, radii, and transitions are CSS custom properties. Change `--navy`, `--gold`, etc. in `:root` to retheme.

**Responsive breakpoints:** `1024px` (tablet), `768px` (small tablet), `480px` (mobile). Hamburger menu activates at 768px.

**Catalogue filtering** — Cards on `models.html` have `data-category` attributes (space-separated). Filter buttons have `data-filter` attributes. JS matches filter against category with `.includes()`.

**FAQ accordion** — `.faq-item` gets `.open` class toggled by JS. CSS animates `max-height` on `.faq-answer`.

**SEO** — Each page has Open Graph tags, Twitter Cards, canonical URL, and JSON-LD schema (Organization on index, Product on models, FAQPage on pricing, ProfessionalService on contact). `robots.txt` and `sitemap.xml` are in the root.

## Gotchas

- **No shared templates.** Header and footer are duplicated in every HTML file. When changing navigation links, update all 6 pages.
- **Two product sets coexist.** `index.html` showcases 5 banking-specific models (Lending, Deposits, Treasury, Capital, Integrated) at $199–$699. `models.html` showcases 6 generic models (Startup, SaaS, Cash Flow, etc.) at £69–£199. These are intentionally separate product lines but the currency mismatch needs resolving before launch.
- **Form submissions are simulated.** The JS `setTimeout` fakes success without calling the backend. The Express endpoints work but aren't wired up on the frontend yet.
- **Backend requires `npm install`.** The server exits with a friendly error message if dependencies are missing.
- **`backend/data/` is gitignored.** Submission logs are created at runtime and never committed.

## Deployment

Currently deployed to GitHub Pages (static only): `https://fpas352.github.io/financial-models-website/`

For full-stack deployment (with form handling), host the Express backend on Railway/Render/Heroku and update the frontend fetch URLs to point to the backend origin. CORS is preconfigured for `bankingmodels.store` in production mode.
