import json
import os
import unittest
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fairshare.settings")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from django.test import Client, SimpleTestCase

from api.repository import reset_store


class ApiTests(SimpleTestCase):
    def setUp(self):
        reset_store()
        self.client = Client()

    def json(self, response):
        return json.loads(response.content)

    def csrf_headers(self):
        # Django's test client does not enforce CSRF by default. This header is
        # included here to document the contract used by real clients.
        return {"HTTP_X_CSRFTOKEN": "test-token"}

    def register(self, username="maya", name="Maya Chen"):
        return self.client.post(
            "/api/auth/register/",
            data={"username": username, "password": "secret-password", "name": name},
            content_type="application/json",
            **self.csrf_headers(),
        )

    def expense_payload(self, **overrides):
        payload = {
            "title": "Dinner at Luigi's",
            "total": "100.00",
            "date": "2026-09-14",
            "note": "Team dinner",
            "splitType": "custom",
            "payer": "Anna",
            "participants": [
                {"name": "Anna", "share": "50.00"},
                {"name": "Bob", "share": "30.00"},
                {"name": "Chris", "share": "20.00"},
            ],
        }
        payload.update(overrides)
        return payload

    def create_expense(self, **overrides):
        return self.client.post(
            "/api/expenses/",
            data=self.expense_payload(**overrides),
            content_type="application/json",
            **self.csrf_headers(),
        )

    def test_register_login_me_and_logout(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.json(response), {"username": "maya", "name": "Maya Chen"})

        me = self.client.get("/api/auth/me/")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(self.json(me)["username"], "maya")

        logout = self.client.post("/api/auth/logout/", **self.csrf_headers())
        self.assertEqual(logout.status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)

        login = self.client.post(
            "/api/auth/login/",
            data={"username": "maya", "password": "secret-password"},
            content_type="application/json",
            **self.csrf_headers(),
        )
        self.assertEqual(login.status_code, 200)

    def test_duplicate_registration_and_bad_login_are_rejected(self):
        self.register()
        duplicate = self.register()
        self.assertEqual(duplicate.status_code, 400)
        self.assertIn("username", self.json(duplicate)["errors"])

        bad_login = self.client.post(
            "/api/auth/login/",
            data={"username": "maya", "password": "wrong"},
            content_type="application/json",
        )
        self.assertEqual(bad_login.status_code, 401)

    def test_private_endpoints_require_authentication(self):
        self.assertEqual(self.client.get("/api/expenses/").status_code, 401)
        self.assertEqual(self.create_expense().status_code, 401)

    def test_create_equal_split_calculates_decimal_remainder(self):
        self.register()
        response = self.create_expense(
            total="10.00",
            splitType="equal",
            participants=[{"name": "Anna"}, {"name": "Bob"}, {"name": "Chris"}],
        )
        self.assertEqual(response.status_code, 201)
        data = self.json(response)
        self.assertEqual([item["share"] for item in data["participants"]], ["3.33", "3.33", "3.34"])
        self.assertEqual(sum(float(item["share"]) for item in data["participants"]), 10.0)

    def test_create_custom_split_and_result_shape(self):
        self.register()
        response = self.create_expense()
        self.assertEqual(response.status_code, 201)
        data = self.json(response)
        self.assertEqual(data["splitType"], "custom")
        self.assertEqual(data["payer"], "Anna")
        self.assertTrue(data["participants"][0]["isPayer"])
        self.assertEqual(data["createdAt"][-1:], "Z")

    def test_invalid_custom_total_is_rejected_atomically(self):
        self.register()
        response = self.create_expense(
            participants=[
                {"name": "Anna", "share": "60.00"},
                {"name": "Bob", "share": "30.00"},
                {"name": "Chris", "share": "20.00"},
            ]
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", self.json(response)["errors"])
        self.assertEqual(self.json(self.client.get("/api/expenses/")), [])

    def test_invalid_participants_and_payer_are_rejected(self):
        self.register()
        response = self.create_expense(
            payer="Nobody",
            participants=[{"name": "Anna", "share": "100.00"}],
        )
        self.assertEqual(response.status_code, 400)
        errors = self.json(response)["errors"]
        self.assertIn("participants", errors)

        response = self.create_expense(
            participants=[
                {"name": "Anna", "share": "100.00"},
                {"name": "Anna", "share": "0.00"},
            ]
        )
        self.assertEqual(response.status_code, 400)

    def test_list_is_owner_scoped_and_limit_is_supported(self):
        self.register("maya")
        self.create_expense(title="Maya expense")
        self.client.post("/api/auth/logout/", **self.csrf_headers())
        self.register("jon", "Jon Doe")
        self.create_expense(title="Jon expense")

        response = self.client.get("/api/expenses/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["title"] for item in self.json(response)], ["Jon expense"])

    def test_get_and_delete_expense_are_owner_scoped(self):
        self.register("maya")
        created = self.create_expense()
        expense_id = self.json(created)["id"]
        self.assertEqual(self.client.get(f"/api/expenses/{expense_id}/").status_code, 200)

        self.client.post("/api/auth/logout/", **self.csrf_headers())
        self.register("jon", "Jon Doe")
        self.assertEqual(self.client.get(f"/api/expenses/{expense_id}/").status_code, 404)
        self.assertEqual(self.client.delete(f"/api/expenses/{expense_id}/", **self.csrf_headers()).status_code, 404)

    def test_delete_removes_expense(self):
        self.register()
        expense_id = self.json(self.create_expense())["id"]
        response = self.client.delete(f"/api/expenses/{expense_id}/", **self.csrf_headers())
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.client.get(f"/api/expenses/{expense_id}/").status_code, 404)
