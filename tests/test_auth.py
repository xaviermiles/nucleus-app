import pytest
from flask import g, session

from nucleus.db import get_db
from nucleus.utils import read_config

PRIMARY_USER = read_config()['primary_user']


def test_initial_user_state(client, app):
    # No-one logged in
    rv = client.get("/")
    assert b"Current user: No-one" in rv.data

    sql_select = "SELECT id, username FROM user"
    with app.app_context():
        user_ids = get_db().execute(sql_select).fetchall()
        # There should only be single user ("primary user") in database
        assert len(user_ids) == 1
        assert user_ids[0][1] == PRIMARY_USER['username']


def test_register(client, app):
    username = "john"

    assert client.get("/auth/register").status_code == 200
    # Successful registration should redirect to login page
    response = client.post("/auth/register",
                           data={'username': username, 'password': 'password'})
    assert "http://localhost/auth/login" == response.headers['Location']
    # Check that user was inserted into database
    sql_select = f"SELECT COUNT(*) FROM user WHERE username = '{username}'"
    with app.app_context():
        assert get_db().execute(sql_select).fetchone()[0] == 1


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("", "a", b"Username is required."),
        ("a", "", b"Password is required."),
        (PRIMARY_USER['username'], PRIMARY_USER['password'],
         b"Username not available.")
    )
)
def test_register_invalid_inputs(client, username, password, message):
    response = client.post("auth/register",
                           data={'username': username, 'password': password})
    assert message in response.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200
    # (Currently) Login is designed to redirect to index page
    response = auth.login()
    assert response.headers['Location'] == "http://localhost/"
    # Check that user_id is set in session and username loaded into flask.g
    with client:
        client.get("/")
        assert session['user_id'] == 1
        assert g.user['username'] == PRIMARY_USER['username']


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "a", b"Incorrect username."),
        (PRIMARY_USER['username'], "", b"Incorrect password.")
    )
)
def test_login_invalid_inputs(auth, username, password, message):
    # TODO: test for blank inputs?
    response = auth.login(username, password)
    print(response.data)
    assert message in response.data


def logout(client, auth):
    auth.login()

    with client:
        response = auth.logout()
        assert "user_id" not in session
        # (Currently) Logout should redirect to index page
        assert response.headers['Location'] == "http://localhost/"
