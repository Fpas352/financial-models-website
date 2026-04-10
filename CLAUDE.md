# CLAUDE.md

## Working Style

Work autonomously from start to finish without asking for approval, confirmation, or permission at any step. Only stop if you hit a complete blocker where you genuinely cannot proceed without information you do not have. Never ask "shall I proceed?", "does this look right?", or "would you like me to continue?" — just continue.

## Project

Static marketing website for SFS Models — a business selling institutional-grade Excel-based financial models for banks, fintechs, and advisory firms. Vanilla HTML/CSS/JS frontend with an optional Express backend for form handling. No build tools, no frameworks, no preprocessors.

**Brand:** SFS Models | sfsmodels.com | sfsmodels362@gmail.com
**Aesthetic:** Dark Bloomberg/Goldman theme (#0A0C10 bg, #C9A84C gold accent)
**Fonts:** DM Sans (body) + DM Serif Display (headlines) via Google Fonts

## Target Audience

Primary: Banking industry professionals — FP&A teams, credit risk, ALM, treasury, regulatory reporting, technical accounting, M&A advisory, and private equity at banks and financial institutions.
Secondary: Corporate finance teams at non-bank corporates, advisory firms, and funds.
The tone across the site and all models should reflect institutional banking standards — precise, professional, no filler.

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
- Single script: `js/scripts.js` — sticky header, hamburger, smooth scroll, FAQ accordion, catalogue filters, form validation with fetch, multi-step form, scroll animations
- All pages share the same header/footer markup (no templating — copy across files when changing nav)
- Nav: logo "SFS" left, links (Models | Pricing | About | Contact) right, CTA "Request a Model"

**Backend (`backend/server.js`):** Express server serving static files from the parent directory + two form API endpoints:
- `POST /api/contact` — contact form (name, email, business_type, message)
- `POST /api/custom-model` — custom model request (name, email, business, sector, model_type, complexity, timeline, description)
- `GET /api/submissions` — dev-only endpoint to view logged submissions
- `GET /api/health` — uptime check

**Form handling:** `scripts.js` validates fields and submits via `fetch()` to backend endpoints. Falls back to simulated success if backend is unavailable (for static hosting).

## File Structure

- `/models/` — full production Excel models (34 total)
- `/samples/` — stripped sample versions for free download, named `[model]_sample.xlsx`
- `models.html` — main models page, organised by category with Buy and Free Sample buttons
- `pricing.html` — pricing page
- `about.html` — about page
- `contact.html` — contact and custom model enquiry page

## Sample Model Rules

Every model must have a corresponding sample in `/samples`. Samples must be genuinely inferior to the full model — good enough to demonstrate capability, not good enough to use professionally. The golden rule: a finance professional should be able to see what the model does but not be able to do their job with it. Each sample must contain an Upgrade tab as the final tab with purchase link placeholder [LEMON_SQUEEZY_LINK] and price placeholder [PRICE].

## Product Line

34 institutional-grade Excel models across 7 categories, all priced in £ GBP:

**Banking & Lending** — FP&A, credit and ALM teams
1. Lending Model
2. Deposits Model
3. Credit Analysis Model
4. Loan Pricing Model
5. IFRS 9 ECL Model
6. Deposit Pricing & NII Model

**Treasury & Capital Markets** — ALM, treasury and trading desks
7. Treasury / IRS Model
8. Bond Pricing & Yield Model
9. Duration & Rate Sensitivity Model
10. FX Hedging Model
11. LCR Model

**Risk & Regulatory** — CRO office and regulatory reporting
12. Capital / Regulatory Model
13. VaR Model
14. Stress Testing Model

**Valuation & Corporate Finance** — M&A, PE and equity research
15. DCF Valuation Model
16. Trading Comps Model
17. Precedent Transactions Model
18. LBO Model
19. SOTP Valuation Model
20. DDM (Dividend Discount) Model
21. Valuations Model (Multi-Method)

**FP&A & Management Reporting** — CFO office and finance teams
22. 3-Statement Integrated Model
23. Budget vs Actual Variance Model
24. Rolling Forecast Model
25. Budget vs Forecast Model
26. Cost Control Model
27. Management Accounts Pack
28. Working Capital Model

**Accounting & Fixed Assets** — Technical accounting and finance ops
29. Capitalisation Model (IAS 38)
30. PPE Model (IAS 16)
31. Impairment Model (IAS 36)
32. Capex Model

**Debt & Leverage** — Leveraged finance and corporate treasury
33. Debt Schedule Model
34. Debt Amortisation Model

Each model has a full paid version and a corresponding stripped sample version in `/samples` with `_sample` suffix.
Custom model tiers: Simple (£500–800), Standard (£800–1,500), Complex (£1,500+)

## Key Patterns

**CSS design tokens** — All colours, shadows, radii, and transitions are CSS custom properties. Key tokens: `--bg`, `--bg-surface`, `--bg-card`, `--gold`, `--text`, `--text-muted`, `--border`.

**Responsive breakpoints:** `1024px` (tablet), `768px` (small tablet), `480px` (mobile). Hamburger menu activates at 768px.

**Catalogue filtering** — Cards on `models.html` have `data-category` attributes. Filter buttons have `data-filter` attributes. JS matches filter against category with `.includes()`.

**Multi-step form** — `contact.html` has a 3-step custom model request form. Progress dots, step panels, and validation per step are handled in `scripts.js`. Review panel on step 3 populates from form values.

**FAQ accordion** — `.faq-item` gets `.open` class toggled by JS. CSS animates `max-height` on `.faq-answer`.

**SEO** — Each page has Open Graph tags, Twitter Cards, canonical URL, and JSON-LD schema. `robots.txt` and `sitemap.xml` point to sfsmodels.com.

## Gotchas

- **No shared templates.** Header and footer are duplicated in every HTML file. When changing navigation links, update all 6 pages.
- **Form submissions fall back gracefully.** If the Express backend isn't running, fetch fails silently and a simulated success message is shown. This is intentional for GitHub Pages static hosting.
- **Backend requires `npm install`.** The server exits with a friendly error message if dependencies are missing.
- **`backend/data/` is gitignored.** Submission logs are created at runtime and never committed.

## Deployment

Currently deployed to GitHub Pages (static only): `https://fpas352.github.io/financial-models-website/`

For full-stack deployment (with form handling), host the Express backend on Railway/Render/Heroku and update the frontend fetch URLs to point to the backend origin. CORS is preconfigured for `sfsmodels.com` in production mode.

All models are one-time purchases. No subscriptions, no recurring billing, no monthly plans. Never add subscription options to any page.