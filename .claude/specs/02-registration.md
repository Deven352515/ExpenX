# Spec: Registration

## Overview
Implement user account creation for Spendly. The `GET /register` route and
`register.html` template already exist; this step wires up the `POST /register`
handler that validates form input, hashes the password, inserts a new user row,
and redirects to the login page on success. This is the entry point for all
future authenticated features — every other step assumes a user exists in the
database.

## Depends on
Step 01 — Database Setup (users table must exist, `get_db()` must work).

## Routes
- `GET /register` — render the registration form — public (already exists, no change)
- `POST /register` — process form submission — public

## Database changes
No new tables or columns. Uses the existing `users` table:
- `name` TEXT NOT NULL
- `email` TEXT NOT NULL UNIQUE
- `password_hash` TEXT NOT NULL
- `created_at` TEXT DEFAULT datetime('now')

## Templates
- **Modify:** `templates/register.html` — already renders `{{ error }}`; no structural
  changes needed unless the error display styling is missing from the stylesheet.
- **Modify:** `templates/login.html` — add a `{% if success %}` block to show a
  "Account created — please sign in" notice when `?registered=1` is present in
  the query string (handled in the GET `/login` route).

## Files to change
- `app.py`
  - Add `app.secret_key` (read from `os.environ.get('SECRET_KEY', 'dev-secret')`).
  - Convert the `register()` function to handle both GET and POST
    (`methods=["GET", "POST"]`).
  - Implement the POST handler (validate → check duplicate → insert → redirect).
  - Update the GET `/login` handler to pass `success=True` when
    `request.args.get('registered')` is set.

## Files to create
None — `register.html` already exists.

## New dependencies
No new pip packages. Uses only:
- `werkzeug.security.generate_password_hash` (already installed)
- `sqlite3` (standard library, via `get_db()`)
- `flask.request`, `flask.redirect`, `flask.url_for` (already in Flask)

## Rules for implementation
- No SQLAlchemy or ORMs — use `get_db()` and raw SQL only.
- Parameterised queries only — never concatenate user input into SQL strings.
- Hash passwords with `werkzeug.security.generate_password_hash` before INSERT.
- All templates extend `base.html`.
- Use CSS variables — never hardcode hex values.
- Validate all fields **server-side** even though the form has `required` attributes.
- Return HTTP 400 with the form re-rendered on validation failure (not a redirect).
- Catch `sqlite3.IntegrityError` to detect duplicate email — do not check with a
  SELECT first (race-condition prone).
- `app.secret_key` must be set before any session usage in later steps; set it
  here even though sessions are not used in this step.

## Server-side validation rules
| Field    | Rule                                      | Error message                        |
|----------|-------------------------------------------|--------------------------------------|
| name     | Non-empty after `.strip()`                | "Name is required."                  |
| email    | Non-empty after `.strip()`                | "Email address is required."         |
| password | Non-empty AND `len >= 8`                  | "Password must be at least 8 characters." |
| email    | UNIQUE constraint (IntegrityError)        | "An account with that email already exists." |

## Definition of done
- [ ] Submitting the form with all valid fields creates a new row in `users`.
- [ ] The new user's password is stored as a hash, not plain text.
- [ ] Successful registration redirects to `/login?registered=1`.
- [ ] The login page shows a success notice when `?registered=1` is in the URL.
- [ ] Submitting with an empty name re-renders the form with "Name is required."
- [ ] Submitting with a password shorter than 8 characters shows the password error.
- [ ] Submitting with an already-registered email shows the duplicate error.
- [ ] Registering the same email twice does not create two rows in the database.
- [ ] The app starts without errors (`python app.py`).
- [ ] All queries use parameterised SQL (no f-strings or `%` formatting in SQL).
