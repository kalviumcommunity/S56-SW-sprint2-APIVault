"""
APIVault Backend API Entry Point.

Exposes RESTful HTTP endpoints for:
- Health check (/api/health)
- Dynamic Product & Version registry listing (/api/products)
- Grounded, Version-Aware documentation querying (/api/query)
"""

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import (
    GeneratedAnswer,
    HealthResponse,
    ProductMetadata,
    QueryRequest,
)
from app.services.generator import AnswerGenerator
from app.services.retriever import VersionAwareRetriever

# Initialize FastAPI App
app = FastAPI(
    title="APIVault API",
    description="Version-Aware Technical Documentation Assistant API",
    version="1.0.0",
)

# Configure CORS for Frontend Development and Production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate Retrieval & Answer Generation Services
retriever = VersionAwareRetriever()
answer_generator = AnswerGenerator(retriever=retriever)


def load_products_registry() -> List[ProductMetadata]:
    """Reads product and version registry dynamically from data/products.json."""
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent.parent
    products_path = project_root / "data" / "products.json"

    if not products_path.exists():
        return []

    with open(products_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [ProductMetadata(**item) for item in data]


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    """Returns the API health status and version information."""
    return HealthResponse(status="ok", app="APIVault", version="1.0.0")


@app.get("/api/products", response_model=List[ProductMetadata], tags=["Products"])
def list_products() -> List[ProductMetadata]:
    """Returns all available products and their supported versions from the data registry."""
    products = load_products_registry()
    return products


@app.post("/api/query", response_model=GeneratedAnswer, tags=["Query"])
def query_documentation(request: QueryRequest) -> GeneratedAnswer:
    """
    Processes a developer query for a specific product and version.
    Performs version-aware documentation retrieval and generates a grounded answer
    with exact source citations.
    """
    clean_product = request.product_id.strip()
    clean_version = request.version.strip()
    clean_question = request.question.strip()

    if not clean_product or not clean_version or not clean_question:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="product_id, version, and question must not be blank.",
        )

    # Route request through AnswerGenerator (which coordinates VersionAwareRetriever)
    result = answer_generator.generate(
        product_id=clean_product,
        version=clean_version,
        question=clean_question,
        top_k=request.top_k or 3,
    )
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
