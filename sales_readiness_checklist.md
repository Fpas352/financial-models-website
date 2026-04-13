# Sales Readiness Checklist — SFS Models

**Audit date:** 10 April 2026
**Site:** sfsmodels.com (Netlify static hosting)
**Payment processor:** Lemon Squeezy

---

## Website & Content

- ✅ All 10 HTML pages load without errors
- ✅ Navigation links consistent across all pages (Models | Free Samples | About | Contact)
- ✅ Footer links point to correct section IDs on models.html
- ✅ All internal anchor links resolve (#banking-lending, #treasury-capital-markets, etc.)
- ✅ Model count consistent: 35 models across 8 categories (all pages)
- ✅ Email address consistent: sfsmodels362@gmail.com (all pages, backend, CLAUDE.md)
- ✅ Terms & Conditions page live (terms.html) with footer link on every page
- ✅ Thank-you page (thankyou.html) ready for post-purchase redirect
- ✅ 404 page configured via netlify.toml
- ✅ All CSS variables resolve (no undefined `--color-muted` etc.)
- ✅ Search functionality working on models.html
- ✅ Responsive hamburger menu, sticky header, FAQ accordion all functional
- ✅ SEO tags (Open Graph, Twitter Cards, JSON-LD, canonical URLs) present on all pages
- ✅ robots.txt and sitemap.xml present

---

## Lemon Squeezy Integration

- ❌ **Buy URLs not set** — all 35 `buyUrl` entries in ls-config.js are `PASTE_LS_URL_HERE`
- ❌ **Free sample URLs not set** — all 34 `freeUrl` entries in ls-config.js are `PASTE_LS_FREE_URL_HERE` (Complete LTP has no free sample URL yet)
- ⚠️ **Lemon Squeezy products not created** — need to create all 35 products in LS dashboard (use lemon_squeezy_product_sheet.md as reference)
- ⚠️ **Thank-you redirect** — configure each LS product to redirect to `https://sfsmodels.com/thankyou.html` after purchase
- ⚠️ **Checkout overlay** — `lemon.js` script is loaded on thankyou.html; verify it's on all pages that have buy buttons (models.html, pricing.html, free-samples.html)
- ✅ ls-config.js structure correct with all 35 model entries and correct prices

---

## Product Files

- ⚠️ **Full models (.xlsx)** — verify all 35 production Excel files exist in `/models/` and are final versions
- ⚠️ **Sample models (.xlsx)** — verify all sample files exist in `/samples/` with `_sample.xlsx` suffix
- ⚠️ **Upload to Lemon Squeezy** — each product needs its .xlsx file attached as the digital download
- ⚠️ **Complete LTP Model** — confirm the full and sample .xlsx files are built and ready

---

## Analytics & Tracking

- ❌ **Google Analytics ID missing** — `PASTE_GA4_ID_HERE` placeholder in all 10 HTML files:
  - index.html
  - models.html
  - pricing.html
  - about.html
  - contact.html
  - free-samples.html
  - free-sample.html
  - thankyou.html
  - terms.html
  - 404.html

---

## Forms & Backend

- ✅ Contact form (`/api/contact`) validates and submits via fetch()
- ✅ Custom model form (`/api/custom-model`) validates and submits via fetch()
- ✅ Forms fall back to simulated success when backend is unavailable (correct for static hosting)
- ⚠️ **Formspree URL missing** — free-sample.html email capture form has no real endpoint configured
- ⚠️ **No real form backend on Netlify** — contact and custom model forms will show simulated success only. Options:
  - Use Netlify Forms (add `netlify` attribute to `<form>`)
  - Use Formspree or similar third-party
  - Deploy Express backend separately (Railway/Render)

---

## Domain & Hosting

- ✅ Netlify site deployed and accessible
- ⚠️ **Custom domain not configured** — site is on `effulgent-nasturtium-50da4e.netlify.app`, needs `sfsmodels.com` pointed to Netlify
- ⚠️ **SSL certificate** — will auto-provision once custom domain is added in Netlify
- ✅ netlify.toml configured with 404 redirect

---

## Pricing Consistency

- ✅ All prices match between models.html, pricing.html, free-samples.html, and ls-config.js
- ✅ All prices in GBP (£)
- ✅ Pricing tiers: £49–£149 (individual models), £999 (Complete LTP)
- ✅ Custom model tiers listed: Simple (£500–800), Standard (£800–1,500), Complex (£1,500+)
- ✅ No subscription options anywhere (one-time purchases only)

---

## Pre-Launch Action Items (in order)

1. ❌ Get GA4 Measurement ID → replace `PASTE_GA4_ID_HERE` in all 10 HTML files
2. ❌ Create all 35 products in Lemon Squeezy dashboard (names, prices, descriptions from lemon_squeezy_product_sheet.md)
3. ❌ Upload .xlsx files to each Lemon Squeezy product
4. ❌ Copy each product's checkout URL → replace `PASTE_LS_URL_HERE` in ls-config.js
5. ❌ Copy each free sample's URL → replace `PASTE_LS_FREE_URL_HERE` in ls-config.js
6. ❌ Set thank-you redirect URL on each LS product
7. ⚠️ Configure form handling (Netlify Forms, Formspree, or separate backend)
8. ⚠️ Point sfsmodels.com to Netlify (DNS)
9. ⚠️ Verify SSL certificate provisions after domain setup
10. ⚠️ Test end-to-end: buy a model → receive email → download → open in Excel
