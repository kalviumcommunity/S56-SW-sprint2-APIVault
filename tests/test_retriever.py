"""
Unit and integration tests for VersionAwareRetriever service.

Verifies:
- Version-specific retrieval for FastAPI and Stripe API
- Strict version isolation (zero cross-version leakage)
- Strict product isolation (zero cross-product leakage)
- Accurate relevance ranking
- Irrelevant query handling / thresholding
- top_k limiting
- Preservation of all original source metadata
- Storage decoupling via dependency injection
"""

import sys
import unittest
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.models.schemas import DocumentChunk
from app.services.retriever import VersionAwareRetriever


class TestVersionAwareRetriever(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the retriever with the real processed_chunks.json."""
        cls.retriever = VersionAwareRetriever()
        if cls.retriever.total_chunks <= 0:
            raise AssertionError("Failed to load chunks from processed_chunks.json")


    def test_fastapi_v0_100_0_retrieval(self):
        """FastAPI v0.100.0 queries should retrieve Pydantic v1 and format string path parameter docs."""
        results = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.100.0",
            question="How does data validation work with Pydantic in FastAPI?",
            top_k=3,
        )
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].product_id, "fastapi")
        self.assertEqual(results[0].version, "v0.100.0")
        self.assertIn("Pydantic v1", results[0].content)

    def test_fastapi_v0_110_0_retrieval(self):
        """FastAPI v0.110.0 queries should retrieve Pydantic v2 migration notes and Annotated Path syntax."""
        results = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.110.0",
            question="What are the changes for Pydantic v2 and model_validator?",
            top_k=3,
        )
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].product_id, "fastapi")
        self.assertEqual(results[0].version, "v0.110.0")
        self.assertIn("@model_validator", results[0].content)

    def test_stripe_v2023_10_16_retrieval(self):
        """Stripe v2023-10-16 queries should retrieve create charge documentation."""
        results = self.retriever.retrieve(
            product_id="stripe-api",
            version="v2023-10-16",
            question="What are the required parameters to create a charge?",
            top_k=3,
        )
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].product_id, "stripe-api")
        self.assertEqual(results[0].version, "v2023-10-16")
        # Ensure it contains charge parameters
        combined_content = " ".join(r.content for r in results)
        self.assertIn("amount", combined_content)

    def test_stripe_v2024_04_01_retrieval(self):
        """Stripe v2024-04-01 queries should retrieve PaymentIntents and migration notice."""
        results = self.retriever.retrieve(
            product_id="stripe-api",
            version="v2024-04-01",
            question="How do I migrate from Charges to PaymentIntents?",
            top_k=3,
        )
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].product_id, "stripe-api")
        self.assertEqual(results[0].version, "v2024-04-01")
        self.assertIn("PaymentIntents", results[0].content)


    def test_no_cross_version_leakage(self):
        """
        Crucial Differentiator Test:
        Querying FastAPI v0.100.0 for 'Pydantic validation' must NEVER return
        v0.110.0 chunks, even though v0.110.0 heavily features 'Pydantic v2'.
        """
        results_v100 = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.100.0",
            question="Pydantic validation and path parameters",
            top_k=10,
        )
        for chunk in results_v100:
            self.assertEqual(
                chunk.version,
                "v0.100.0",
                f"Cross-version leakage detected! Found {chunk.version} chunk in v0.100.0 query."
            )
            self.assertNotIn("Pydantic v2", chunk.content)

        # Conversely, querying FastAPI v0.110.0 must only return v0.110.0 chunks
        results_v110 = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.110.0",
            question="Pydantic validation and path parameters",
            top_k=10,
        )
        for chunk in results_v110:
            self.assertEqual(
                chunk.version,
                "v0.110.0",
                f"Cross-version leakage detected! Found {chunk.version} chunk in v0.110.0 query."
            )

    def test_no_cross_product_leakage(self):
        """
        Querying Stripe API must NEVER return FastAPI chunks, even if query terms
        like 'parameters', 'path', 'request' match.
        """
        results = self.retriever.retrieve(
            product_id="stripe-api",
            version="v2023-10-16",
            question="parameters and routing endpoints",
            top_k=10,
        )
        for chunk in results:
            self.assertEqual(
                chunk.product_id,
                "stripe-api",
                f"Cross-product leakage detected! Found {chunk.product_id} chunk in stripe query."
            )

    def test_relevance_ranking(self):
        """The most specific section should rank first."""
        # Querying specifically about 'Data Validation'
        results = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.100.0",
            question="Data Validation with 422 Unprocessable Entity",
            top_k=3,
        )
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].section_title, "Data Validation")

    def test_irrelevant_question_returns_empty(self):
        """Completely irrelevant queries should return an empty list (insufficient evidence)."""
        results = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.100.0",
            question="How to bake a sourdough bread with chocolate chips?",
            top_k=3,
        )
        self.assertEqual(len(results), 0)

    def test_top_k_limiting(self):
        """top_k parameter should strictly limit the number of returned chunks."""
        results_1 = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.100.0",
            question="path parameters",
            top_k=1,
        )
        self.assertEqual(len(results_1), 1)

        results_2 = self.retriever.retrieve(
            product_id="fastapi",
            version="v0.100.0",
            question="path parameters",
            top_k=2,
        )
        self.assertLessEqual(len(results_2), 2)

    def test_source_metadata_preservation(self):
        """Retrieved chunks must retain all original source attribution metadata intact."""
        results = self.retriever.retrieve(
            product_id="stripe-api",
            version="v2024-04-01",
            question="How do I create a payment intent?",
            top_k=1,
        )
        self.assertEqual(len(results), 1)
        chunk = results[0]

        # Verify all metadata fields
        self.assertTrue(chunk.chunk_id)
        self.assertEqual(chunk.product_id, "stripe-api")
        self.assertEqual(chunk.version, "v2024-04-01")
        self.assertEqual(chunk.document_title, "Stripe API v2024-04-01 - Charges API & PaymentIntents")
        self.assertEqual(chunk.section_title, "Create a Payment Intent")
        self.assertEqual(chunk.source_path, "data/docs/stripe-api/v2024-04-01/charges.md")
        self.assertGreater(chunk.token_count, 0)
        self.assertIn("POST /v1/payment_intents", chunk.content)

    def test_invalid_and_empty_inputs(self):
        """Empty or non-existent inputs should safely return empty lists without crashing."""
        self.assertEqual(self.retriever.retrieve("", "v1.0", "question"), [])
        self.assertEqual(self.retriever.retrieve("fastapi", "", "question"), [])
        self.assertEqual(self.retriever.retrieve("fastapi", "v0.100.0", ""), [])
        self.assertEqual(self.retriever.retrieve("non-existent-product", "v1.0", "question"), [])
        self.assertEqual(self.retriever.retrieve("fastapi", "v999.99.99", "question"), [])

    def test_decoupled_storage_injection(self):
        """Retriever can be instantiated with in-memory chunks, allowing database decoupling."""
        mock_chunks = [
            DocumentChunk(
                chunk_id="test-1",
                product_id="custom-product",
                version="v1.0",
                document_title="Custom Docs",
                section_title="Custom Section",
                content="This is a custom injected test chunk about database connection pooling.",
                token_count=10,
                source_path="docs/custom.md",
            )
        ]
        injected_retriever = VersionAwareRetriever(chunks=mock_chunks)
        self.assertEqual(injected_retriever.total_chunks, 1)

        res = injected_retriever.retrieve("custom-product", "v1.0", "connection pooling")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].chunk_id, "test-1")


if __name__ == "__main__":
    unittest.main()
