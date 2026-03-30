// ============================================================
// Banking Models Store — Node.js + Express Backend
// ============================================================
//
// FILE:    backend/server.js
// PURPOSE: Production-ready Express server that:
//   1. Serves all static files from the website root
//   2. POST /api/contact       — contact form submissions
//   3. POST /api/custom-model  — custom model request form
//   4. GET  /api/submissions   — view logged submissions (dev)
//
// SETUP:
//   cd financial-models-website/backend
//   npm install                 (first time only)
//   node server.js
//   → http://localhost:3000
//
// ENVIRONMENT VARIABLES (optional — set in .env file):
//   PORT               Server port (default: 3000)
//   NODE_ENV           'production' or 'development'
//   MAIL_HOST          SMTP host for nodemailer
//   MAIL_PORT          SMTP port (default: 587)
//   MAIL_USER          SMTP username / email
//   MAIL_PASS          SMTP password / app password
//   MAIL_TO            Recipient email for notifications
//
// DEPENDENCIES: express, cors, helmet, express-rate-limit,
//               dotenv, nodemailer (optional)
// ============================================================


// ----------------------------------------------------------
// 1. IMPORTS & CONFIGURATION
// ----------------------------------------------------------

const path = require('path');
const fs   = require('fs');

// Check for required dependencies before proceeding
try {
  require.resolve('express');
} catch {
  console.error('');
  console.error('  Missing dependencies. Run this first:');
  console.error('');
  console.error('    cd ' + __dirname);
  console.error('    npm install');
  console.error('');
  process.exit(1);
}

const express    = require('express');
const cors       = require('cors');
const helmet     = require('helmet');
const rateLimit  = require('express-rate-limit');

// Load .env file if present (for local dev)
try { require('dotenv').config(); } catch { /* dotenv not installed — skip */ }

const app  = express();
const PORT = process.env.PORT || 3000;
const ENV  = process.env.NODE_ENV || 'development';

// Paths
const STATIC_DIR      = path.join(__dirname, '..');
const SUBMISSIONS_DIR = path.join(__dirname, 'data');
const CONTACT_LOG     = path.join(SUBMISSIONS_DIR, 'contact-submissions.json');
const CUSTOM_LOG      = path.join(SUBMISSIONS_DIR, 'custom-model-submissions.json');

// Create data directory if it doesn't exist
if (!fs.existsSync(SUBMISSIONS_DIR)) {
  fs.mkdirSync(SUBMISSIONS_DIR, { recursive: true });
}


// ----------------------------------------------------------
// 2. MIDDLEWARE
// ----------------------------------------------------------

// Security headers (XSS protection, content-type sniffing, etc.)
app.use(helmet({
  contentSecurityPolicy: false, // Disabled to allow inline styles/scripts
  crossOriginEmbedderPolicy: false,
}));

// CORS — restrict in production
app.use(cors({
  origin: ENV === 'production'
    ? ['https://bankingmodels.store', 'https://www.bankingmodels.store']
    : '*',
  methods: ['GET', 'POST'],
}));

// Parse JSON and URL-encoded request bodies
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));

// Request logging (simple, coloured output)
app.use((req, res, next) => {
  if (req.method !== 'GET' || req.url.startsWith('/api')) {
    const timestamp = new Date().toISOString().slice(11, 19);
    console.log(`[${timestamp}] ${req.method} ${req.url}`);
  }
  next();
});


// ----------------------------------------------------------
// 3. RATE LIMITING
// Prevents spam and abuse on form endpoints.
// - General: 100 requests per 15 minutes per IP
// - Forms:   5 submissions per 15 minutes per IP
// ----------------------------------------------------------

const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max:      100,              // 100 requests per window
  message:  { error: 'Too many requests. Please try again later.' },
  standardHeaders: true,
  legacyHeaders:   false,
});

const formLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max:      5,                // 5 form submissions per window
  message:  { error: 'Too many submissions. Please wait 15 minutes and try again.' },
  standardHeaders: true,
  legacyHeaders:   false,
});

app.use(generalLimiter);


// ----------------------------------------------------------
// 4. VALIDATION HELPERS
// Reusable validation functions for form data.
// ----------------------------------------------------------

/**
 * Validates an email address format.
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
  if (!email || typeof email !== 'string') return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim());
}

/**
 * Sanitises a string to prevent basic XSS.
 * Strips HTML tags and trims whitespace.
 * @param {string} str
 * @returns {string}
 */
function sanitise(str) {
  if (!str || typeof str !== 'string') return '';
  return str.replace(/<[^>]*>/g, '').trim();
}

/**
 * Validates required fields and returns an array of error messages.
 * Each rule: { field, value, label, type }
 * Types: 'required', 'email', 'maxLength', 'oneOf'
 *
 * @param {Array} rules - Validation rules
 * @returns {Array} Error messages (empty if all valid)
 */
function validate(rules) {
  const errors = [];

  for (const rule of rules) {
    const { field, value, label, type, options, max } = rule;

    switch (type) {
      case 'required':
        if (!value || !String(value).trim()) {
          errors.push({ field, message: `${label} is required.` });
        }
        break;

      case 'email':
        if (!isValidEmail(value)) {
          errors.push({ field, message: `Please enter a valid email address.` });
        }
        break;

      case 'maxLength':
        if (value && String(value).length > max) {
          errors.push({ field, message: `${label} must be under ${max} characters.` });
        }
        break;

      case 'oneOf':
        if (value && !options.includes(value)) {
          errors.push({ field, message: `${label} has an invalid value.` });
        }
        break;
    }
  }

  return errors;
}


// ----------------------------------------------------------
// 5. SUBMISSION LOGGER
// Appends form submissions to a local JSON file.
// Each form type has its own log file in backend/data/.
//
// In production, replace this with:
//   - A database (PostgreSQL, MongoDB, etc.)
//   - An email notification (see nodemailer section below)
//   - A CRM integration (HubSpot, Pipedrive, etc.)
//   - A webhook to Slack, Discord, etc.
// ----------------------------------------------------------

/**
 * Appends a submission to a JSON log file.
 * Thread-safe for single-process use.
 *
 * @param {string} logPath - Path to the JSON log file
 * @param {Object} data    - The submission data to log
 */
function logSubmission(logPath, data) {
  let submissions = [];

  // Read existing submissions
  if (fs.existsSync(logPath)) {
    try {
      const raw = fs.readFileSync(logPath, 'utf8');
      submissions = JSON.parse(raw);
    } catch {
      // File corrupted — start fresh
      console.warn(`Warning: ${path.basename(logPath)} was corrupted. Starting fresh.`);
      submissions = [];
    }
  }

  // Append new submission with metadata
  submissions.push({
    ...data,
    id:        `sub_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    timestamp: new Date().toISOString(),
    ip:        data._ip || 'unknown',
  });

  // Write back to file
  fs.writeFileSync(logPath, JSON.stringify(submissions, null, 2));

  return submissions.length;
}


// ----------------------------------------------------------
// 6. OPTIONAL: EMAIL NOTIFICATIONS VIA NODEMAILER
//
// Sends an email notification when a form is submitted.
// Requires MAIL_* environment variables to be set.
//
// To enable:
//   1. npm install nodemailer
//   2. Create a .env file with your SMTP credentials:
//        MAIL_HOST=smtp.gmail.com
//        MAIL_PORT=587
//        MAIL_USER=your-email@gmail.com
//        MAIL_PASS=your-app-password
//        MAIL_TO=hello@bankingmodels.store
//   3. For Gmail, use an App Password (not your login password):
//        https://myaccount.google.com/apppasswords
//
// Alternatives to Gmail SMTP:
//   - SendGrid: smtp.sendgrid.net (free tier: 100 emails/day)
//   - Mailgun:  smtp.mailgun.org
//   - AWS SES:  email-smtp.eu-west-1.amazonaws.com
//   - Resend:   smtp.resend.com
// ----------------------------------------------------------

let transporter = null;

try {
  const nodemailer = require('nodemailer');

  if (process.env.MAIL_HOST && process.env.MAIL_USER) {
    transporter = nodemailer.createTransport({
      host:   process.env.MAIL_HOST,
      port:   parseInt(process.env.MAIL_PORT) || 587,
      secure: parseInt(process.env.MAIL_PORT) === 465, // true for 465, false for 587
      auth: {
        user: process.env.MAIL_USER,
        pass: process.env.MAIL_PASS,
      },
    });

    // Verify connection on startup
    transporter.verify()
      .then(() => console.log('Mail: SMTP connection verified'))
      .catch(err => {
        console.warn('Mail: SMTP connection failed —', err.message);
        transporter = null;
      });
  }
} catch {
  // nodemailer not installed — email notifications disabled
}

/**
 * Sends an email notification for a form submission.
 * Silently fails if nodemailer is not configured.
 *
 * @param {string} subject - Email subject line
 * @param {string} html    - Email body (HTML)
 */
async function sendNotification(subject, html) {
  if (!transporter) return;

  const mailTo = process.env.MAIL_TO || process.env.MAIL_USER;

  try {
    await transporter.sendMail({
      from:    `"Banking Models Store" <${process.env.MAIL_USER}>`,
      to:      mailTo,
      subject: subject,
      html:    html,
    });
    console.log(`Mail: Notification sent → ${mailTo}`);
  } catch (err) {
    console.error('Mail: Failed to send —', err.message);
  }
}

/**
 * Builds an HTML email from form submission data.
 * @param {string} formType - 'Contact' or 'Custom Model'
 * @param {Object} data     - The form data
 * @returns {string} HTML email body
 */
function buildEmailHTML(formType, data) {
  const rows = Object.entries(data)
    .filter(([key]) => !key.startsWith('_')) // Exclude internal fields
    .map(([key, value]) => {
      const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      return `<tr><td style="padding:8px 12px;font-weight:600;color:#334155;border-bottom:1px solid #e2e8f0;">${label}</td><td style="padding:8px 12px;color:#475569;border-bottom:1px solid #e2e8f0;">${value || '—'}</td></tr>`;
    })
    .join('');

  return `
    <div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;">
      <div style="background:#0a1628;color:#d4a843;padding:20px 24px;border-radius:8px 8px 0 0;">
        <h2 style="margin:0;font-size:18px;">New ${formType} Submission</h2>
      </div>
      <table style="width:100%;border-collapse:collapse;background:#fff;border:1px solid #e2e8f0;">
        ${rows}
      </table>
      <div style="padding:16px 24px;background:#f8fafc;border-radius:0 0 8px 8px;border:1px solid #e2e8f0;border-top:none;">
        <p style="margin:0;font-size:13px;color:#94a3b8;">
          Received at ${new Date().toLocaleString('en-GB', { timeZone: 'Europe/London' })} GMT
        </p>
      </div>
    </div>
  `;
}


// ----------------------------------------------------------
// 7. API ROUTES
// ----------------------------------------------------------


// ---- POST /api/contact ----
// Handles the contact form on contact.html.
// Fields: name*, email*, business_type, message*
// ----------------------------------------------------------

app.post('/api/contact', formLimiter, (req, res) => {

  // Sanitise all inputs
  const data = {
    name:          sanitise(req.body.name),
    email:         sanitise(req.body.email),
    business_type: sanitise(req.body.business_type),
    message:       sanitise(req.body.message),
  };

  // Validate
  const errors = validate([
    { field: 'name',    value: data.name,    label: 'Name',    type: 'required'  },
    { field: 'email',   value: data.email,   label: 'Email',   type: 'required'  },
    { field: 'email',   value: data.email,   label: 'Email',   type: 'email'     },
    { field: 'message', value: data.message, label: 'Message', type: 'required'  },
    { field: 'message', value: data.message, label: 'Message', type: 'maxLength', max: 5000 },
    { field: 'business_type', value: data.business_type, label: 'Business type', type: 'oneOf',
      options: ['', 'bank', 'fintech', 'consultancy', 'corporate', 'startup', 'investor', 'education', 'other'] },
  ]);

  if (errors.length) {
    return res.status(400).json({ success: false, errors });
  }

  // Log to console
  console.log('\n--- New Contact Submission ---');
  console.log(`  Name:     ${data.name}`);
  console.log(`  Email:    ${data.email}`);
  console.log(`  Type:     ${data.business_type || '(not specified)'}`);
  console.log(`  Message:  ${data.message.substring(0, 100)}${data.message.length > 100 ? '...' : ''}`);
  console.log('-----------------------------\n');

  // Log to file
  const count = logSubmission(CONTACT_LOG, { ...data, _ip: req.ip });

  // Send email notification (non-blocking)
  sendNotification(
    `New Contact: ${data.name}`,
    buildEmailHTML('Contact', data)
  );

  // Respond
  res.json({
    success: true,
    message: 'Thank you! We\'ll be in touch within 24 hours.',
    meta:    { submissionNumber: count },
  });
});


// ---- POST /api/custom-model ----
// Handles the custom model request form on models.html.
// Fields: business*, sector*, revenue, employees, description*
// ----------------------------------------------------------

app.post('/api/custom-model', formLimiter, (req, res) => {

  // Sanitise all inputs
  const data = {
    business:    sanitise(req.body.business),
    sector:      sanitise(req.body.sector),
    revenue:     sanitise(req.body.revenue),
    employees:   sanitise(req.body.employees),
    description: sanitise(req.body.description),
  };

  // Valid dropdown values
  const validSectors = [
    '', 'banking', 'fintech', 'insurance', 'saas', 'ecommerce',
    'real-estate', 'healthcare', 'energy', 'manufacturing',
    'professional-services', 'other',
  ];

  const validRevenue = [
    '', 'pre-revenue', '0-500k', '500k-2m', '2m-10m', '10m-50m', '50m+',
  ];

  const validEmployees = [
    '', '1-10', '11-50', '51-200', '201-500', '500+',
  ];

  // Validate
  const errors = validate([
    { field: 'business',    value: data.business,    label: 'Business name', type: 'required'  },
    { field: 'sector',      value: data.sector,      label: 'Sector',        type: 'required'  },
    { field: 'sector',      value: data.sector,      label: 'Sector',        type: 'oneOf', options: validSectors },
    { field: 'description', value: data.description, label: 'Description',   type: 'required'  },
    { field: 'description', value: data.description, label: 'Description',   type: 'maxLength', max: 10000 },
    { field: 'revenue',     value: data.revenue,     label: 'Revenue range', type: 'oneOf', options: validRevenue },
    { field: 'employees',   value: data.employees,   label: 'Employees',     type: 'oneOf', options: validEmployees },
  ]);

  if (errors.length) {
    return res.status(400).json({ success: false, errors });
  }

  // Log to console
  console.log('\n--- New Custom Model Request ---');
  console.log(`  Business:  ${data.business}`);
  console.log(`  Sector:    ${data.sector}`);
  console.log(`  Revenue:   ${data.revenue || '(not specified)'}`);
  console.log(`  Employees: ${data.employees || '(not specified)'}`);
  console.log(`  Brief:     ${data.description.substring(0, 100)}${data.description.length > 100 ? '...' : ''}`);
  console.log('-------------------------------\n');

  // Log to file
  const count = logSubmission(CUSTOM_LOG, { ...data, _ip: req.ip });

  // Send email notification (non-blocking)
  sendNotification(
    `New Custom Model Request: ${data.business}`,
    buildEmailHTML('Custom Model Request', data)
  );

  // Respond
  res.json({
    success: true,
    message: 'Request received! We\'ll send you a scope and quote within 24 hours.',
    meta:    { submissionNumber: count },
  });
});


// ---- GET /api/submissions ----
// Development-only endpoint to view all submissions.
// Disabled in production for security.
// ----------------------------------------------------------

app.get('/api/submissions', (req, res) => {

  // Block in production
  if (ENV === 'production') {
    return res.status(403).json({ error: 'Not available in production.' });
  }

  const readLog = (logPath) => {
    if (!fs.existsSync(logPath)) return [];
    try {
      return JSON.parse(fs.readFileSync(logPath, 'utf8'));
    } catch {
      return [];
    }
  };

  res.json({
    contact:      readLog(CONTACT_LOG),
    custom_model: readLog(CUSTOM_LOG),
    total:        readLog(CONTACT_LOG).length + readLog(CUSTOM_LOG).length,
  });
});


// ---- GET /api/health ----
// Simple health check endpoint for uptime monitoring.
// ----------------------------------------------------------

app.get('/api/health', (req, res) => {
  res.json({
    status:  'ok',
    uptime:  Math.floor(process.uptime()),
    env:     ENV,
    mail:    transporter ? 'configured' : 'disabled',
  });
});


// ----------------------------------------------------------
// 8. STATIC FILE SERVING
// ----------------------------------------------------------

// Block access to the backend directory
app.use('/backend', (req, res) => {
  res.status(403).send('Forbidden');
});

// Serve static files from the website root
app.use(express.static(STATIC_DIR, {
  extensions: ['html'],     // Enable clean URLs (/models → /models.html)
  index:      'index.html', // Default file for directory requests
  maxAge:     ENV === 'production' ? '1d' : 0, // Cache static assets in production
}));

// 404 fallback — serve a friendly error page
app.use((req, res) => {
  // If the request was for an API endpoint, return JSON
  if (req.url.startsWith('/api')) {
    return res.status(404).json({ error: 'Endpoint not found.' });
  }

  // Otherwise serve the 404 HTML page (or fallback)
  const notFoundPage = path.join(STATIC_DIR, '404.html');
  if (fs.existsSync(notFoundPage)) {
    res.status(404).sendFile(notFoundPage);
  } else {
    res.status(404).send(`
      <!DOCTYPE html>
      <html lang="en">
      <head><meta charset="UTF-8"><title>404</title>
      <style>
        body { font-family: Inter, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; background: #f8fafc; color: #0a1628; }
        .box { text-align: center; }
        h1 { font-size: 4rem; margin: 0; color: #d4a843; }
        p { color: #475569; margin: 12px 0 24px; }
        a { color: #3b82f6; text-decoration: none; font-weight: 600; }
        a:hover { text-decoration: underline; }
      </style></head>
      <body><div class="box">
        <h1>404</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/">Back to Home</a>
      </div></body>
      </html>
    `);
  }
});


// ----------------------------------------------------------
// 9. ERROR HANDLING
// ----------------------------------------------------------

// Global error handler — catches unhandled errors in routes
app.use((err, req, res, next) => {
  console.error('Server error:', err.message);

  res.status(500).json({
    error: ENV === 'production'
      ? 'Something went wrong. Please try again later.'
      : err.message,
  });
});


// ----------------------------------------------------------
// 10. START SERVER
// ----------------------------------------------------------

app.listen(PORT, () => {
  console.log('');
  console.log('  Banking Models Store');
  console.log('  ────────────────────────────────────');
  console.log(`  Server:  http://localhost:${PORT}`);
  console.log(`  Env:     ${ENV}`);
  console.log(`  Mail:    ${transporter ? 'enabled' : 'disabled (set MAIL_* env vars)'}`);
  console.log(`  Logs:    ${SUBMISSIONS_DIR}`);
  console.log('  ────────────────────────────────────');
  console.log('');
});
