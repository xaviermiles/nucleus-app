import datetime
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from nucleus import utils


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Clear the existing data and create fresh tables.

    Adds primary/super user, as specified in config file.
    """
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    primary_user = utils.read_config()['primary_user']
    password_hash = generate_password_hash(primary_user['password'])
    current_dt = datetime.datetime.now()
    db.execute(
        "INSERT INTO user (username, password, admin, signup_dt)"
        " VALUES (?, ?, ?, ?)",
        (primary_user['username'], password_hash, True, current_dt)
    )

    db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialise the sqlite database."""
    init_db()
    click.echo("Database initialised.")


def init_app(app):
    """Initialise app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
