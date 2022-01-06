import pandas as pd
from flask import Blueprint, render_template, g

from nucleus.auth import login_required
from nucleus.db import get_db

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("")
@login_required
def index():
    details = get_user_details()
    details_html = details.to_html(index=False) if details.shape[0] > 0 else ""
    return render_template("profile.html", user_details=details_html)


def get_user_details():
    """Returns information about users.

    Returns:
     - If not logged in, nothing
     - If logged in as non-admin, only information about the current user
     - If logged in as admin, information about all users
    """
    if not g.user:
        return pd.DataFrame()
    sql_select_info = "SELECT username,admin,signup_dt FROM user"
    if not g.user['admin']:
        sql_select_info += f" WHERE username='{g.user['username']}'"
    response = get_db().execute(sql_select_info).fetchall()
    details = pd.DataFrame(response,
                           columns=['Username', 'Admin?', 'Signed up'])
    details['Admin?'] = details['Admin?'] == 1
    details['Signed up'] = pd.to_datetime(details['Signed up'],
                                          format='%Y-%m-%d %H:%M:%S.%f') \
                             .dt.strftime('%I:%m%p %d/%m/%y')
    return details
