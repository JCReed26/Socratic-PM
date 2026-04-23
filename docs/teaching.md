# Learning Log: Socratic-PM GraphRAG (Phase 3)

Track what was taught, how it worked, feedback, and improvements for future skill writing.

## Phase 3: GraphRAG — Schema, Ingestion, Context Query

**Learning Goal:** Understand Neo4j fundamentals, graph design for documentation retrieval, and building deterministic ingestion pipelines.

**Timeframe:** Phase 3 development (2026-04-23+)

---

## Topics Covered

### 1. Neo4j Fundamentals
- **What:** Property graph database with nodes, edges (relationships), and properties.
- **How It Works:** [to be filled in as we build]
- **Key Insight:** [to be filled in]
- **Feedback & Improvements:** [to be filled in]

### 2. Graph Schema Design for Docs — Package-Language Separation
- **What:** Nodes structured as `Package-Language` (e.g., `langgraph-python`, `fastapi-python`) to separate API references by language syntax. Docs connect to language-specific API nodes, avoiding wrong package/version reference.
- **Design Pattern:** 
  - Node names match import statements from codebase files
  - Version locked to environment (from `/socratic-pm status`)
  - Edges: `Documentation` → `DOCUMENTS` → `Package-Language-API`
  - Query specifies package to ensure correct reference retrieval
- **How It Works:** [to be filled in as we build]
- **Key Insight:** [to be filled in]
- **Feedback & Improvements:** [to be filled in]

### 3. Deterministic Ingestion Pipeline
- **What:** Python script that reads lockfiles, parses docs, fetches APIs, and populates Neo4j without LLM.
- **How It Works:** [to be filled in as we build]
- **Key Insight:** [to be filled in]
- **Feedback & Improvements:** [to be filled in]

### 4. Cypher Queries for Context Retrieval
- **What:** Graph traversal queries to find relevant API docs by topic.
- **How It Works:** [to be filled in as we build]
- **Key Insight:** [to be filled in]
- **Feedback & Improvements:** [to be filled in]

---

## Socratic Teaching Moments

### Design Decisions (Phase 3 Foundation)

**Language-Specific Ingestion:**
- Only ingest languages actually used in project (Python if in requirements.txt, JS/TS if in package.json)
- Multi-language projects: ingest both naturally (if langgraph in both .py and .js files → both nodes created)
- Resync script catches graph up when requirements/package.json changes

**Deprecated Package Handling:**
- Keep removed packages in graph, mark with `deprecated: true` property
- Useful for debugging: "Was this package removed? Could that explain the bug?"
- Checkpoint skill surfaces during debugging context

**Multi-Version Resolution:**
- Human selects primary version file when conflicts exist
- Status skill updated to display: `Primary Version File: requirements.txt (langgraph==0.2.0)`
- Graph uses human's choice as canonical

**Resync Automation:**
- Checkpoint skill detects changes to requirements/package.json
- Auto-triggers resync (no manual `/socratic-pm resync` needed)
- Keeps graph synchronized with codebase evolution

### Work Completed (Apr 22, 2026)

**Designed by James:**
- [x] Schema design (Package, Documentation, API_Reference nodes; DOCUMENTS_PACKAGE, DEFINES_API_FOR edges)
- [x] Node properties finalized (name, language, version, deprecated, last_update, data)

**Implemented by Claude:**
- [x] `scripts/schema.cypher` — Full Neo4j schema with constraints, indexes, and query patterns
- [x] `scripts/ingest.py` — Deterministic pipeline: detect languages, extract packages, fetch docs/APIs, upsert nodes, mark deprecated

**Scaffolded for James to Execute (Tomorrow):**
- [ ] Local Neo4j setup: Docker or local install, schema application, ingest test, browser verification
- [ ] MCP integration: Connect neo4j-contrib/mcp-neo4j for `/socratic-pm context` Cypher queries

### Break Points for Your Practice
Tomorrow:
- [ ] Follow `docs/NEO4J_SETUP.md` to get Neo4j running locally
- [ ] Test `python scripts/ingest.py` against Socratic-PM project
- [ ] Verify graph nodes in Neo4j Browser
- [ ] Report back: what worked, what broke, questions

### Questions Asked to Guide Learning
- What breaks if you delete a node that docs still reference?
- Multi-version: create separate nodes, prompt human, or tag edges?
- When does resync run: manual, file watch, or session init?
- Should deprecated nodes be excluded from queries or included with warnings?

---

## Feedback Log

### From James
- [to be filled in]

### Reasoning on Improvements
- [to be filled in]

---

## Key Files Created / Modified
- `scripts/schema.cypher` — Neo4j schema definition
- `scripts/ingest.py` — Deterministic ingestion pipeline
- `modes/ingest.md` — Socratic instruction for ingestion
- `modes/context.md` — Socratic instruction for context queries

---

## Next Review
When Phase 3 is complete, use this log to:
1. Extract clear explanations for the skill prompt
2. Identify where teaching questions guided learning (for Socratic constraints)
3. Note what feedback shaped architectural decisions
4. Document the "why" behind design choices for future AI engineers
