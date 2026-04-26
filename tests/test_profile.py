import pytest
from werkzeug.security import check_password_hash
from database.db import get_user_by_id, get_user_by_email


class TestProfileRequiresLogin:
    def test_get_redirects_to_login(self, client):
        response = client.get("/profile")
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

    def test_post_redirects_to_login(self, client):
        response = client.post("/profile", data={"name": "X"})
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]


class TestProfileGet:
    def test_renders_200(self, logged_in_client):
        response = logged_in_client.get("/profile")
        assert response.status_code == 200

    def test_shows_user_name(self, logged_in_client, registered_user):
        response = logged_in_client.get("/profile")
        assert registered_user["name"].encode() in response.data

    def test_shows_user_email(self, logged_in_client, registered_user):
        response = logged_in_client.get("/profile")
        assert registered_user["email"].encode() in response.data

    def test_not_stub_string(self, logged_in_client):
        response = logged_in_client.get("/profile")
        assert b"coming in Step 4" not in response.data


class TestProfileUpdateName:
    def test_updates_name_and_redirects(self, app, logged_in_client, registered_user):
        response = logged_in_client.post(
            "/profile",
            data={"name": "Updated Name", "new_password": "", "confirm_password": ""},
        )
        assert response.status_code == 302
        assert "/profile" in response.headers["Location"]

        with app.app_context():
            user = get_user_by_id(registered_user["id"])
        assert user["name"] == "Updated Name"

    def test_blank_name_rejected(self, logged_in_client):
        response = logged_in_client.post(
            "/profile",
            data={"name": "", "new_password": "", "confirm_password": ""},
        )
        assert response.status_code == 400
        assert b"cannot be blank" in response.data

    def test_whitespace_only_name_rejected(self, logged_in_client):
        response = logged_in_client.post(
            "/profile",
            data={"name": "   ", "new_password": "", "confirm_password": ""},
        )
        assert response.status_code == 400


class TestProfileUpdatePassword:
    def test_matching_passwords_update_hash(self, app, logged_in_client, registered_user):
        logged_in_client.post(
            "/profile",
            data={"name": registered_user["name"], "new_password": "newpass456", "confirm_password": "newpass456"},
        )
        with app.app_context():
            user = get_user_by_email(registered_user["email"])
        assert check_password_hash(user["password_hash"], "newpass456")

    def test_mismatched_passwords_rejected(self, app, logged_in_client, registered_user):
        response = logged_in_client.post(
            "/profile",
            data={"name": registered_user["name"], "new_password": "aaa", "confirm_password": "bbb"},
        )
        assert response.status_code == 400
        assert b"do not match" in response.data

        with app.app_context():
            user = get_user_by_email(registered_user["email"])
        assert check_password_hash(user["password_hash"], "password123")

    def test_blank_passwords_do_not_change_hash(self, app, logged_in_client, registered_user):
        logged_in_client.post(
            "/profile",
            data={"name": "New Name", "new_password": "", "confirm_password": ""},
        )
        with app.app_context():
            user = get_user_by_email(registered_user["email"])
        assert check_password_hash(user["password_hash"], "password123")


class TestNavbar:
    def test_profile_link_visible_when_logged_in(self, logged_in_client):
        response = logged_in_client.get("/")
        assert b'href="/profile"' in response.data or b"profile" in response.data

    def test_profile_link_hidden_when_logged_out(self, client):
        response = client.get("/")
        assert b'href="/profile"' not in response.data
