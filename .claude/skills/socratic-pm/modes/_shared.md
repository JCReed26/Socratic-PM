# Socratic-PM Shared Context

Always injected before every mode file. Contains constraints, schema, and conventions.

## Socratic Constraints (Non-Negotiable)

- **Agents write scaffolds only:** Type signatures, docstrings, step-by-step pseudo-code as comments. Never implementation logic.
- **All architectural guidance goes to chat:** Examples, API contracts, design patterns output to chat. Do not edit code files with explanations.
- **Code reviews output to chat:** Never edit files. Produce structured feedback: correctness, edge cases, architecture alignment, 3 Socratic questions.
- **Debugging output to chat:** Socratic questions → ranked hypotheses → diagnostic steps. Never edit files. If solution is obvious, describe in chat and ask developer to implement.

## Neo4j Node Schema (Reference)

Used by context and ingest modes:

```
Node: Package
  - Properties: name (string), version (string), repo_url (string)
  - Purpose: Represents a library/framework in the project

Node: Documentation
  - Properties: title (string), content (text), framework (string)
  - Purpose: Conceptual explanation (patterns, best practices)

Node: API_Reference
  - Properties: signature (string), params (json), return_type (string), version (string)
  - Purpose: Exact API contract (function signatures, types)

Edge: DEFINES_API_FOR
  - From: API_Reference → To: Package
  - Purpose: Links API contract to its parent package

Edge: DOCUMENTS
  - From: Documentation → To: Package
  - Purpose: Links conceptual docs to its parent package
```

## GitHub MCP Conventions (issue/checkpoint modes)

**Issue Naming:**
```
[PHASE-N] Item text from docs/plan.md
```

**Issue Body Structure:**
```
## Description
[Item description from plan + context from `/socratic-pm context` call]

## Implementation Notes
[Embedded Cypher query for context mode]

```cypher
MATCH (pkg:Package)-[:DEFINES_API_FOR]->(api:API_Reference)
WHERE pkg.name IN ["framework1", "framework2"]
RETURN api.signature, api.params, api.return_type
```
```

**Labels:**
- `phase-N` (maps to phase in plan)
- `needs-james` (for items requiring founder review)

## File Path Reference (All Modes)

**At Project Root** (user creates from skill templates):
- `docs/plan.md` — source of truth checklist
- `docs/prd.md` — requirements context
- `docs/updates.md` — version tracking for env drift detection (copy from skill's `../docs/updates.md`)
- `data/issues.md` — issue-to-item mapping (created by issue mode at runtime)
- `config/project.yml` — project config (user copies from skill's `../config/project.example.yml`)

**Within Skill** (relative references):
- `../scripts/telemetry.py` — called by status mode
- `../config/project.example.yml` — template for user's project config
- `../docs/updates.md` — template for user's environment tracking
