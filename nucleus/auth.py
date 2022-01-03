import functools
import datetime

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from nucleus.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    # TODO: should provide message about being redirected
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Fetch user details from database to flask.g variable."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
    

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Handle attempts to log in to existing user account."""
    # TODO: shouldn't load page if user already logged in
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = get_db().execute("SELECT * FROM user WHERE username = ?",
                                (username,)) \
                       .fetchone()

        error = None
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # TODO: how to redirect to page immediately before this page?
            return redirect(url_for("landing_page.index"))

        flash(error)

    return render_template("auth.html", mode="Log In")


@bp.route("/logout")
def logout():
    """Log out of current user account."""
    session.clear()
    # TODO: how to redirect to page immediately before this page?
    return redirect(url_for("landing_page.index"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Handle attempts to register new user."""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        id = db.execute("SELECT id FROM user WHERE username = ?", (username,)) \
               .fetchone()
        if id is not None:
            error = f"User {username} is already registered."

        if error is None:
            current_dt = datetime.datetime.now()
            db.execute(
                "INSERT INTO user (username, password, signup_dt)"
                " VALUES (?, ?, ?)",
                (username, generate_password_hash(password), current_dt)
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth.html", mode="Register")
