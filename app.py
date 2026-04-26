import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id, update_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    if request.method != "POST":
        abort(405)

    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name:
        flash("Name is required.")
        return render_template("register.html"), 400
    if not email:
        flash("Email address is required.")
        return render_template("register.html"), 400
    if not password:
        flash("Password is required.")
        return render_template("register.html"), 400
    if password != confirm_password:
        flash("Passwords do not match.")
        return render_template("register.html"), 400

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        flash("Email already registered.")
        return render_template("register.html"), 400

    flash("Account created — please sign in.")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        flash("Email is required.", "error")
        return render_template("login.html"), 400
    if not password:
        flash("Password is required.", "error")
        return render_template("login.html"), 400

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.", "error")
        return render_template("login.html"), 401

    session["user_id"] = user["id"]
    flash(f"Hello, welcome back {user['name']}!", "success")
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = get_user_by_id(user_id)
    if user is None:
        session.clear()
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("profile.html", user=user)

    name             = request.form.get("name", "").strip()
    new_password     = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name:
        flash("Display name cannot be blank.", "error")
        return render_template("profile.html", user=user), 400

    password_hash = None
    if new_password or confirm_password:
        if new_password != confirm_password:
            flash("New passwords do not match.", "error")
            return render_template("profile.html", user=user), 400
        password_hash = generate_password_hash(new_password)

    update_user(user_id, name, password_hash)
    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile"))


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
