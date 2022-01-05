import sqlite3

import pytest
from werkzeug.security import check_password_hash, generate_password_hash

from nucleus.db import get_db
from nucleus.utils import read_config


def test_init_db_command(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=["init-db"])
    assert "Database initialised." in result.output

    # Should be just primary user in database
    sql_select = "SELECT id,username,admin,password FROM user"
    with app.app_context():
        user_data = get_db().execute(sql_select).fetchall()
        assert len(user_data) == 1
        expected_cred = read_config()['primary_user']
        assert user_data[0][0:3] == (
            1,
            expected_cred['username'],
            True
        )
        assert check_password_hash(user_data[0][3], expected_cred['password'])


def test_get_and_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)
