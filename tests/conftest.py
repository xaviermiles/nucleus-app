import os
import tempfile

import pytest

from nucleus import create_app
from nucleus.db import init_db
from nucleus.utils import read_config


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})
    with app.app_context():
        init_db()

    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username=None, password=None):
        if username is None or password is None:
            # Default to primary user, as that is (supposed to be) always there
            cred = read_config()['primary_user']
        else:
            cred = {"username": username, "password": password}
        return self._client.post("/login", data=cred)

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
