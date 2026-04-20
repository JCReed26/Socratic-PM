---
name: ingest
description: Populate Neo4j with packages, docs, and API references
---

# Mode: ingest

Not yet implemented. Phase 3+ will add:
- Run scripts/ingest.py to:
  - Scan pyproject.toml / package.json / lockfiles for packages
  - Parse docs/ markdown into Documentation nodes
  - Fetch/read API references, create API_Reference nodes
  - Write to Neo4j via Cypher
- Report counts of nodes written
- Surface errors
