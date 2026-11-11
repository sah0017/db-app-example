# Shared setup for the tests. pytest finds this file automatically
# and passes the fixtures below to any test that names them as a parameter.
#
# Only fixtures that EVERY feature uses belong here. A fixture for one
# feature (for example, one that cleans up the rows its tests add) goes in
# that feature's own test file, so teammates don't edit this file at once.
#
# The tests use the same MySQL database as the app (set in .env), so every
# test must delete any rows it adds. See tests/test_actors.py for the pattern.

import pytest

from app import app as flask_app

CSRF_TOKEN = "test-token"

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        yield flask_app

# A test client sends requests to the app without starting a server
@pytest.fixture
def client(app):
    return app.test_client()

# A test client whose session already holds a CSRF token,
# so its POST requests can include a matching csrf_token field
@pytest.fixture
def csrf_client(client):
    with client.session_transaction() as session:
        session['csrf_token'] = CSRF_TOKEN
    return client
