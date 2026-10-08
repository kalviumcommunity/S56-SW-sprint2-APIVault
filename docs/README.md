# APIVault Documentation

Project documentation is stored here, including the PRD and technical notes.

## Current documentation dataset

The current MVP dataset contains two products with two versions each:

- FastAPI: `v0.100.0`, `v0.110.0`
- Stripe API: `v2023-10-16`, `v2024-04-01`

Each registered version has Markdown documentation under `data/docs/`. The ingestion pipeline validates the registry before generating `data/processed_chunks.json`.

The processed dataset currently contains 33 chunks. Each chunk preserves its product ID, version, source path, document/section metadata, content, and token count. Validation also checks chunk IDs, source files, and registered product/version pairs.

## Data workflow

`Markdown docs -> products.json validation -> chunking -> processed_chunks.json -> version-aware retrieval`

This keeps retrieval strictly scoped to the selected product and version.

## Final Integration Verification

The API is validated end-to-end for version isolation: the same FastAPI question is queried against `v0.100.0` and `v0.110.0`, and the returned answer and source metadata remain tied to the selected version. This protects the project's core requirement of version-specific answers with exact source attribution.
