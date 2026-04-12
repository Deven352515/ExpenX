    # CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — a personal expense tracking web application built as a student learning project. The stack is intentionally minimal (no frontend frameworks) to teach core web development.

## Commands

```bash
# Run the development server (port 5001)
python app.py

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a single test by name
pytest -k "test_login"
```

## Tech Stack

- **Backend:** Flask 3.1.3, Werkzeug 3.1.6
- **Templating:** Jinja2 (server-side rendered, no SPA)
- **Database:** SQLite (via `database/db.py` — not yet implemented)
- **Frontend:** Vanilla HTML/CSS/JS — no frameworks by design
- **Testing:** pytest + pytest-flask

## Architecture

### Routing
All routes are Flask decorator-based in `app.py`. Every route calls `render_template()`. POST handlers for forms are not yet implemented — the forms in `register.html` and `login.html` already have `method="POST"` but their handlers are placeholders.

Placeholder routes to implement: `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.

### Templates
Jinja2 template inheritance: all pages extend `templates/base.html` which provides the navbar and footer. Page-specific content goes in the `{% block content %}` block.

### CSS Design System
CSS custom properties are defined in `static/css/style.css`. Use these variables — do not introduce hardcoded values:

- Colors: `--ink`, `--accent` (dark green), `--accent-2` (warm orange), `--danger`, `--paper`
- Typography: `--font-display` (DM Serif Display), `--font-body` (DM Sans)
- Layout: `--max-width: 1200px`, `--auth-width: 440px`
- Radii: `--radius-sm`, `--radius-md`, `--radius-lg`

Landing-page-specific styles live in `static/css/landing.css`.

### Database Module
`database/db.py` is a placeholder. The expected pattern is to implement `get_db()`, `init_db()`, and `seed_db()` functions using Python's built-in `sqlite3` module and Flask's `g` object for per-request connection management.

### JavaScript
JavaScript is vanilla only. Complex UI interactions (like the YouTube modal on the landing page) are written as inline `<script>` tags in the relevant template.
