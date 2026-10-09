# APIVault

<div align="center">

# Version-Aware Technical Documentation Assistant

[![CI Pipeline](https://github.com/pranjal-2507/S56-SW-sprint2-APIVault/actions/workflows/ci.yml/badge.svg)](https://github.com/pranjal-2507/S56-SW-sprint2-APIVault/actions/workflows/ci.yml)
![Tests](https://img.shields.io/badge/Tests-47%2F47%20Passing-brightgreen?style=flat-square)
![MRR](https://img.shields.io/badge/Retrieval%20MRR-1.0000-blue?style=flat-square)
![Leakage](https://img.shields.io/badge/Cross--Version%20Leakage-0.0%25-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Node](https://img.shields.io/badge/Node.js-20.x%20LTS-339933?style=flat-square&logo=node.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19.2+-61DAFB?style=flat-square&logo=react&logoColor=black)

<p align="center">
  <strong>Retrieve exact, version-isolated technical answers supported by verified documentation sources — zero hallucination, zero version confusion.</strong>
</p>

</div>

---

## Overview

**APIVault** is a specialized version-aware documentation question-answering assistant. When developers work with evolving frameworks and APIs, generic AI models frequently mix syntax across disparate releases (e.g. confusing Pydantic v1 with v2 in FastAPI, or mixing legacy Charge tokens with modern PaymentIntents in Stripe).

APIVault solves this by strictly isolating documentation retrieval to the developer's exact selected product and version, generating grounded answers with verbatim source attribution.

---

## Core Problem & Solution

| The Problem in Software Documentation | The APIVault Solution |
| :--- | :--- |
| **Cross-Version Confusion**: AI models mix deprecated and modern syntax across releases. | **Strict Pre-Filtering**: Queries are strictly isolated by `(product_id, version)` before retrieval scoring. |
| **Hallucinated Parameters**: Generic LLMs invent non-existent arguments or endpoints. | **Grounded Synthesis**: Answers are synthesized exclusively from indexed documentation chunks. |
| **Unverifiable Output**: Answers lack exact citations to original technical sources. | **Exact Source Attribution**: Every response returns document title, section, source path, and excerpts. |
| **Out-of-Context Migration**: Difficult to identify what changed between API versions. | **Version-Specific Corpus**: Curated documentation highlighting version differentials. |

---

## Key Differentiator

$$\text{Product} + \text{Version} \longrightarrow \text{Question} \longrightarrow \text{Version-Isolated Retrieval} \longrightarrow \text{Grounded Answer} \longrightarrow \text{Exact Sources}$$

* **Zero Cross-Version Leakage**: Queries for FastAPI `v0.100.0` will never receive or cite `v0.110.0` documentation.
* **Deterministic Lexical Retrieval**: BM25-style term frequency saturation, field-weighted scoring, and exact substring boosts without external vector database dependencies.
* **Full Citation Traceability**: Every answer cites exact local documentation paths and section headers.

---

## System Architecture

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                          React 19 + Vite Frontend                        │
│   • Product & Version Cascading Selectors                                │
│   • Grounded Answer & Source Attribution Inspector                       │
│   • Persistent Query History (localStorage with relative timestamps)     │
│   • 1-Click Markdown / Source Clipboard Export                           │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ HTTP JSON (POST /api/query)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           FastAPI Backend API                            │
│   • Dynamic Registry Loader (data/products.json)                         │
│   • Pydantic v2 Request Validation (HTTP 422 for malformed payloads)     │
│   • Health Checks & CORS Middleware                                      │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         VersionAwareRetriever                            │
│   1. Strict Pre-Filtering: chunk.product_id == P and chunk.version == V   │
│   2. Lexical Scoring: Section (3.0x), Title (1.5x), Content BM25 TF      │
│   3. Top-k Ranking & Relevance Threshold Filtering                       │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Ordered Chunks & Metadata
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                            AnswerGenerator                               │
│   1. Synthesizes answers strictly from retrieved documentation           │
│   2. Formats verbatim source citations, sections, and file paths         │
│   3. Fallback: returns explicit 'insufficient_documentation' if off-topic│
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 19, Vite 8, Vanilla CSS | Reactive user interface, state management, local storage persistence |
| **Backend API** | FastAPI, Uvicorn, Pydantic v2 | High-performance RESTful API endpoints, request validation |
| **Retrieval Engine** | Custom `VersionAwareRetriever` | Deterministic lexical scoring, BM25 saturation, version pre-filtering |
| **Data & Chunker** | Custom `MarkdownChunker` | Heading-aware chunking, token bounding, metadata preservation |
| **CI / Automation** | GitHub Actions | Automated matrix for unit tests, benchmark regression, frontend build |
| **Testing** | Python `unittest`, FastAPI `TestClient` | 47 automated tests covering validation, retrieval, generator, and API |

---

## Supported Products & Versions

| Product | Product ID | Version Tag | Release Date | Key Topics Covered |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | `fastapi` | `v0.100.0` | 2023-07-01 | Format string path params, Pydantic v1 validation (HTTP 422), `Depends()`, yield generators, `response_model` |
| **FastAPI** | `fastapi` | `v0.110.0` | 2024-03-01 | `typing.Annotated` dependencies, Pydantic v2 migration (`@model_validator`), `lifespan` context managers, return type inference |
| **Stripe API** | `stripe-api` | `v2023-10-16` | 2023-10-16 | `POST /v1/charges`, card source tokens (`tok_visa`), customer management, charge refund parameters |
| **Stripe API** | `stripe-api` | `v2024-04-01` | 2024-04-01 | `POST /v1/payment_intents` migration, `SetupIntents`, `PaymentMethods`, customer search syntax, dispute evidence submission |

---

## Quick Start

### Prerequisites
* **Python**: 3.11 or higher
* **Node.js**: 18.x or 20.x LTS (with npm)

### 1. One-Command Development Startup (Recommended)

From the project root directory:

```bash
# Starts both FastAPI Backend (8000) and Vite Frontend (5173)
python start.py
```

* **Frontend Web Application**: [http://localhost:5173](http://localhost:5173)
* **Backend API Base**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **API Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

Press `Ctrl+C` in your terminal to cleanly shut down both servers.

---

### 2. Running Services Individually

```bash
# Option A: Run Backend Only (Port 8000)
python start.py --backend
# (or: cd backend && python -m uvicorn app.main:app --reload --port 8000)

# Option B: Run Frontend Only (Port 5173)
python start.py --frontend
# (or: cd frontend && npm run dev)
```

---

### 3. Running Tests & Ingestion Pipeline

```bash
# Run complete test suite (47 tests including benchmark regression)
python -m unittest discover tests -v

# Run standalone retrieval benchmark evaluation
python backend/scripts/benchmark.py

# Re-run data chunking & ingestion pipeline (updates data/processed_chunks.json)
python backend/scripts/ingest.py

# Build frontend production bundle
cd frontend && npm run build
```

---

## REST API Reference

### 1. Health Check
* **Method**: `GET /api/health`
* **Description**: Returns API health status and application version.
* **Sample Response**:
  ```json
  {
    "status": "ok",
    "app": "APIVault",
    "version": "1.0.0"
  }
  ```

### 2. Product & Version Registry
* **Method**: `GET /api/products`
* **Description**: Returns dynamic list of registered products, metadata, and available versions from `data/products.json`.
* **Sample Response**:
  ```json
  [
    {
      "id": "fastapi",
      "name": "FastAPI",
      "description": "High performance web framework for building APIs with Python.",
      "versions": [
        { "version": "v0.100.0", "release_date": "2023-07-01", "doc_dir": "docs/fastapi/v0.100.0" },
        { "version": "v0.110.0", "release_date": "2024-03-01", "doc_dir": "docs/fastapi/v0.110.0" }
      ]
    }
  ]
  ```

### 3. Documentation Query
* **Method**: `POST /api/query`
* **Description**: Queries version-specific documentation and returns grounded answer with exact source citations.
* **Sample Request Body**:
  ```json
  {
    "product_id": "fastapi",
    "version": "v0.110.0",
    "question": "How do lifespan events work in FastAPI?",
    "top_k": 3
  }
  ```
* **Sample Response Body**:
  ```json
  {
    "status": "success",
    "product_id": "fastapi",
    "version": "v0.110.0",
    "question": "How do lifespan events work in FastAPI?",
    "answer": "In FastAPI v0.110.0, the legacy @app.on_event(\"startup\") and @app.on_event(\"shutdown\") decorators are replaced by the lifespan context manager...",
    "confidence": 0.85,
    "sources": [
      {
        "chunk_id": "ea91210a9fac1489",
        "product_id": "fastapi",
        "version": "v0.110.0",
        "document_title": "FastAPI v0.110.0 - Dependency Injection & Lifespan",
        "section_title": "Lifespan Events Context Manager",
        "source_path": "data/docs/fastapi/v0.110.0/dependencies.md",
        "excerpt": "In FastAPI v0.110.0, the legacy @app.on_event(\"startup\") and @app.on_event(\"shutdown\") decorators are replaced by the lifespan context manager."
      }
    ]
  }
  ```

---

## Benchmark Evaluation Results

Evaluated across **23 deterministic test cases** using `backend/scripts/benchmark.py`:

| Evaluation Metric | Measured Value | SLA Target | Status |
| :--- | :--- | :--- | :--- |
| **Mean Reciprocal Rank (MRR)** | **1.0000** | $\ge 0.95$ | **PASS** |
| **Hit Rate@1** | **100.0%** (15/15) | $\ge 95\%$ | **PASS** |
| **Hit Rate@3** | **100.0%** (15/15) | $\ge 95\%$ | **PASS** |
| **Precision@1** | **100.0%** | $\ge 90\%$ | **PASS** |
| **Irrelevant Query Rejection Rate** | **100.0%** (4/4 True Negatives) | $100\%$ | **PASS** |
| **Version/Product Isolation** | **100.0%** (0% Leakage) | $100\%$ | **PASS** |
| **Avg Retrieval Latency** | **0.27 ms** | $< 10.0\text{ ms}$ | **PASS** |
| **Avg E2E Generation Latency** | **0.35 ms** | $< 50.0\text{ ms}$ | **PASS** |

---

## Continuous Integration (CI)

Automated project validation is configured via GitHub Actions in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

Every push and pull request to `main` executes:
1. **Backend Tests & Benchmark**: Sets up Python 3.11 with pip caching, installs dependencies, and runs all 47 unit & benchmark tests (`python -m unittest discover tests -v`).
2. **Frontend Build & Validation**: Sets up Node.js 20 with npm caching, installs dependencies (`npm ci`), and verifies production compilation (`npm run build`).

---

## Project Structure

```text
.github/
  └── workflows/
      └── ci.yml             # GitHub Actions CI workflow definition
backend/
  ├── app/
  │   ├── models/schemas.py  # Pydantic data schemas (Chunk, Query, Answer)
  │   ├── services/
  │   │   ├── retriever.py   # VersionAwareRetriever service
  │   │   ├── generator.py   # AnswerGenerator service
  │   │   ├── chunker.py     # MarkdownChunker service
  │   │   └── data_validator.py # Product & chunk registry validator
  │   └── main.py            # FastAPI application & REST endpoints
  ├── requirements.txt       # Backend dependencies
  └── scripts/
      ├── ingest.py          # Documentation chunking & ingestion script
      └── benchmark.py       # Retrieval benchmark evaluation suite
data/
  ├── docs/                  # Version-tagged Markdown documentation
  │   ├── fastapi/           # v0.100.0, v0.110.0 documentation
  │   └── stripe-api/        # v2023-10-16, v2024-04-01 documentation
  ├── products.json          # Product & version registry metadata
  └── processed_chunks.json  # Ingested 33-chunk documentation index
docs/
  ├── APIVault_PRD.md        # Product Requirements Document
  └── SPRINT2_DELIVERABLES.md # Sprint 2 Deliverables & Verification Summary
frontend/
  ├── src/                   # React components & UI logic
  ├── package.json           # Frontend dependencies & scripts
  └── vite.config.js         # Vite configuration
tests/                       # Automated test suite (47 unit/benchmark tests)
start.py                     # Unified single-command dev server launcher
start.bat                    # Windows startup script
start.sh                     # Unix/macOS startup script
README.md                    # Project documentation
```

---

## License

This project is developed as part of **Sprint 2** of the Software Engineering sprint deliverables.
