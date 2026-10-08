"""
Unit and integration tests for APIVault FastAPI HTTP endpoints.

Verifies:
- GET /api/health
- GET /api/products
- POST /api/query (FastAPI v0.100.0, FastAPI v0.110.0, Stripe API)
- Validation errors (HTTP 422 for missing or empty inputs)
- Insufficient documentation handling via API
- Exact source attribution retention in JSON responses
- Absence of cross-version leakage via API
- CORS headers
"""

import sys
import unittest
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app


class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a TestClient instance for the FastAPI application."""
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        """GET /api/health should return HTTP 200 with status 'ok' and application name."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["app"], "APIVault")
        self.assertIn("version", data)

    def test_products_endpoint(self):
        """GET /api/products should return dynamic products and versions from products.json."""
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0)

        # Verify fastapi product and its versions
        fastapi_prod = next((p for p in products if p["id"] == "fastapi"), None)
        self.assertIsNotNone(fastapi_prod)
        self.assertEqual(fastapi_prod["name"], "FastAPI")
        versions = [v["version"] for v in fastapi_prod["versions"]]
        self.assertIn("v0.100.0", versions)
        self.assertIn("v0.110.0", versions)

        # Verify stripe product
        stripe_prod = next((p for p in products if p["id"] == "stripe-api"), None)
        self.assertIsNotNone(stripe_prod)

    def test_query_fastapi_v0_100_0_success(self):
        """POST /api/query for FastAPI v0.100.0 returns grounded Pydantic v1 answer and sources."""
        payload = {
            "product_id": "fastapi",
            "version": "v0.100.0",
            "question": "How does data validation work in FastAPI?",
            "top_k": 3,
        }
        response = self.client.post("/api/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["product_id"], "fastapi")
        self.assertEqual(data["version"], "v0.100.0")
        self.assertIn("Pydantic v1", data["answer"])
        self.assertNotIn("Pydantic v2", data["answer"])
        self.assertGreater(len(data["sources"]), 0)

        source = data["sources"][0]
        self.assertEqual(source["product_id"], "fastapi")
        self.assertEqual(source["version"], "v0.100.0")
        self.assertTrue(source["chunk_id"])
        self.assertTrue(source["source_path"])

    def test_query_fastapi_v0_110_0_success(self):
        """POST /api/query for FastAPI v0.110.0 returns Pydantic v2 / Annotated answer."""
        payload = {
            "product_id": "fastapi",
            "version": "v0.110.0",
            "question": "What are the changes for Pydantic v2 and model_validator?",
            "top_k": 3,
        }
        response = self.client.post("/api/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["product_id"], "fastapi")
        self.assertEqual(data["version"], "v0.110.0")
        self.assertIn("Pydantic v2", data["answer"])
        self.assertIn("@model_validator", data["answer"])
        self.assertNotIn("Pydantic v1", data["answer"])

    def test_query_stripe_v2023_success(self):
        """POST /api/query for Stripe API v2023-10-16 returns charges endpoint info."""
        payload = {
            "product_id": "stripe-api",
            "version": "v2023-10-16",
            "question": "How do I create a charge?",
        }
        response = self.client.post("/api/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["product_id"], "stripe-api")
        self.assertEqual(data["version"], "v2023-10-16")
        self.assertIn("/v1/charges", data["answer"])

    def test_query_stripe_v2024_setup_intents(self):
        """POST /api/query for Stripe API v2024-04-01 returns setup intents info."""
        payload = {
            "product_id": "stripe-api",
            "version": "v2024-04-01",
            "question": "How do I use SetupIntents for saving payment methods?",
        }
        response = self.client.post("/api/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["product_id"], "stripe-api")
        self.assertEqual(data["version"], "v2024-04-01")
        self.assertIn("/v1/setup_intents", data["answer"])
        self.assertGreater(len(data["sources"]), 0)

    def test_query_insufficient_documentation(self):
        """POST /api/query with irrelevant question returns status 'insufficient_documentation'."""
        payload = {
            "product_id": "fastapi",
            "version": "v0.100.0",
            "question": "What is the capital of France and best recipe for cheesecake?",
        }
        response = self.client.post("/api/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "insufficient_documentation")
        self.assertEqual(data["confidence"], 0.0)
        self.assertEqual(data["sources"], [])
        self.assertIn("Insufficient documentation available", data["answer"])

    def test_query_validation_errors(self):
        """POST /api/query with missing or blank fields returns HTTP 422 Unprocessable Entity."""
        # Missing question
        res1 = self.client.post("/api/query", json={"product_id": "fastapi", "version": "v0.100.0"})
        self.assertEqual(res1.status_code, 422)

        # Blank string question
        res2 = self.client.post("/api/query", json={"product_id": "fastapi", "version": "v0.100.0", "question": "   "})
        self.assertEqual(res2.status_code, 422)

        # Blank product_id
        res3 = self.client.post("/api/query", json={"product_id": "  ", "version": "v0.100.0", "question": "test"})
        self.assertEqual(res3.status_code, 422)

    def test_same_question_returns_version_specific_results(self):
        """The same question must retrieve documentation from the selected version only."""
        question = "How does data validation work in FastAPI?"

        responses = {}
        for version in ("v0.100.0", "v0.110.0"):
            response = self.client.post(
                "/api/query",
                json={
                    "product_id": "fastapi",
                    "version": version,
                    "question": question,
                    "top_k": 3,
                },
            )
            self.assertEqual(response.status_code, 200)
            responses[version] = response.json()

        older = responses["v0.100.0"]
        newer = responses["v0.110.0"]

        self.assertNotEqual(older["answer"], newer["answer"])
        self.assertIn("Pydantic v1", older["answer"])
        self.assertIn("Pydantic v2", newer["answer"])
        self.assertTrue(older["sources"])
        self.assertTrue(newer["sources"])
        self.assertTrue(all(source["version"] == "v0.100.0" for source in older["sources"]))
        self.assertTrue(all(source["version"] == "v0.110.0" for source in newer["sources"]))

    def test_no_cross_version_leakage_via_api(self):
        """Querying FastAPI v0.100.0 via API must never return v0.110.0 chunks or answers."""
        payload = {
            "product_id": "fastapi",
            "version": "v0.100.0",
            "question": "Pydantic validation parameters",
            "top_k": 5,
        }
        response = self.client.post("/api/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        for source in data["sources"]:
            self.assertEqual(source["version"], "v0.100.0")
            self.assertNotEqual(source["version"], "v0.110.0")

    def test_cors_headers_present(self):
        """Verifies CORS headers are returned for cross-origin frontend requests."""
        response = self.client.get("/api/health", headers={"Origin": "http://localhost:5173"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access-control-allow-origin", response.headers)


if __name__ == "__main__":
    unittest.main()
