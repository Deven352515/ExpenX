# Spec: Profile Page Design

## Overview
This feature implements the `/profile` page for Spendly. It converts the existing stub route into a fully functional page where a logged-in user can view their account details (display name, email address, member-since date) and update them — specifically, change their display name and/or set a new password. The page requires authentication; unauthenticated visitors are redirected to `/login`. After this step the navbar gains a "Profile" link for signed-in users, completing the authenticated navigation shell before expense features are built.

## Depends on
- Step 01 — Database Setup (`users` table must exist with `name`, `email`, `password_hash`, `created_at` columns)
- Step 02 — Registration (`create_user` in place)
- Step 03 — Login and Logout (`session["user_id"]` set on login; `session.clear()` on logout)

## Routes
- `GET /profile` — render profile page with current user data — logged-in only
- `POST /profile` — handle name-change and/or password-change form submission — logged-in only

## Database changes
No new tables or columns. The existing `users` table already holds all required fields.

Two new helper functions will be added to `database/db.py`:
- `get_user_by_id(user_id: int)` — fetch a single user row by primary key
- `update_user(user_id: int, name: str, password_hash: str | None)` — update name (always) and optionally update `password_hash` when a new password is provided

## Templates
- **Create:** `templates/profile.html` — extends `base.html`; two sections:
  1. Account info card — read-only display of email and member-since date
  2. Edit form — fields for display name, new password, confirm new password; password fields are optional (leave blank to keep current password)
- **Modify:** `templates/base.html` — add a "Profile" link in `.nav-links` alongside the existing "Sign out" link (visible only when `session.user_id` is set)

## Files to change
- `app.py` — implement `profile()` as a GET+POST handler with login guard
- `database/db.py` — add `get_user_by_id()` and `update_user()` helpers
- `templates/base.html` — add Profile nav link for authenticated users

## Files to create
- `templates/profile.html` — profile view and edit form
- `tests/conftest.py` — pytest fixtures shared across test files
- `tests/test_profile.py` — test suite for the profile feature

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never use f-strings or `.format()` in SQL
- New passwords hashed with `werkzeug.security.generate_password_hash` before storing
- Login guard: if `session.get("user_id")` is falsy, `redirect(url_for("login"))`
- Use CSS variables — never hardcode hex values; follow the design system in `style.css`
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode paths
- Name field is required and must not be blank after `.strip()`
- Password change is optional: only update `password_hash` when both `new_password` and `confirm_password` are provided
- If new passwords are provided they must match; if they do not, flash an error and re-render the form
- After a successful update, flash a success message and redirect back to `GET /profile` (Post/Redirect/Get pattern)
- `get_user_by_id` and `update_user` belong in `database/db.py`, not inline in the route
- Profile page layout must use existing CSS variables (`--paper-card`, `--border`, `--radius-md`, `--accent`, etc.) — no new CSS files unless necessary

## Definition of done
- [ ] Visiting `GET /profile` while logged out redirects to `/login`
- [ ] Visiting `GET /profile` while logged in renders the page without errors
- [ ] The page displays the current user's name, email, and member-since date
- [ ] Submitting the form with a new name (and blank password fields) updates the display name and flashes a success message
- [ ] After a name update, refreshing `GET /profile` shows the updated name
- [ ] Submitting with matching new passwords updates the password; subsequent login with the new password succeeds
- [ ] Submitting with mismatched new passwords shows an error flash and does not update anything
- [ ] Submitting with a blank name shows an error flash and does not update anything
- [ ] The navbar shows a "Profile" link for logged-in users that navigates to `/profile`
- [ ] The `/profile` route no longer returns the raw stub string
