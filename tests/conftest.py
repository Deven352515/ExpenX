import pytest
from app import app as flask_app
from database.db import init_db, create_user


@pytest.fixture()
def app(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setattr("database.db.DB_PATH", str(db_file))
    flask_app.config.update(TESTING=True, SECRET_KEY="test-secret")
    with flask_app.app_context():
        init_db()
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def registered_user(app):
    with app.app_context():
        user_id = create_user("Test User", "test@example.com", "password123")
    return {"id": user_id, "name": "Test User", "email": "test@example.com", "password": "password123"}


@pytest.fixture()
def logged_in_client(client, registered_user):
    with client.session_transaction() as sess:
        sess["user_id"] = registered_user["id"]
    return client
