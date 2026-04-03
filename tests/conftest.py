import threading
import time
from contextlib import contextmanager

import pytest
from werkzeug.serving import make_server

from app import create_app, db


@pytest.fixture
def app():
    """Create shared test app."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "START_MONITOR": False,
    })

    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@contextmanager
def run_test_server(flask_app, host="127.0.0.1", port=5010):
    """Run a temporary local server for Selenium smoke tests."""
    server = make_server(host, port, flask_app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)
