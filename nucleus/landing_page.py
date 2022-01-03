from flask import Blueprint, render_template

bp = Blueprint("landing_page", __name__)


@bp.route("/")
def index():
    return render_template("index.html")
