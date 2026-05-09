---
name: ingest
description: Populate Neo4j with Package nodes (Python script) then enrich with Documentation and API_Reference nodes via Context7 MCP
---

# Mode: ingest

Two-phase pipeline. Phase 1 is deterministic Python. Phase 2 is Context7 MCP running natively in this Claude session.

---

## Phase 1 — Write Package Nodes (Python)

Determine the project root. Default to the current working directory.

Read `config/project.yml` to get `neo4j_uri` (default: `bolt://localhost:7687`).

Run:

```bash
uv run python .claude/skills/socratic-pm/scripts/ingest.py \
  --packages-only \
  --neo4j-uri <neo4j_uri> \
  --project-root <project_root>
```

Print the returned JSON stats. If `errors` is non-empty, surface each error and stop.

Capture the detected package list from the `[1/5]` output line (format: `Found: {'python': [...], ...}`). Parse this to get language → package list mapping.

---

## Phase 2 — Fetch Docs via Context7 (Claude native)

For each package in the detected list, attempt Context7 lookup. Run sequentially.

**For each package `<pkg>` in `<language>`:**

1. Resolve the library ID:
   - Call `mcp__plugin_context7_context7__resolve-library-id` with `libraryName: "<pkg>"`
   - If no match or error → log `SKIP: <pkg> (not in Context7)` and continue

2. Fetch documentation:
   - Call `mcp__plugin_context7_context7__query-docs` with the resolved library ID
   - Use `topic: "API reference functions classes"` and `tokens: 8000`

3. Extract structured data from the docs response:
   - `summary`: first paragraph or package description (1-3 sentences)
   - `signatures`: public function/class signatures with type hints extracted from code blocks
   - `source_url`: the `sourceUrl` or `docsUrl` field from the Context7 response

4. Append to `doc_records` list:
   ```json
   {"package": "<pkg>", "language": "<language>", "summary": "...", "signatures": [...], "source_url": "..."}
   ```

---

## Phase 3 — Write Doc/API Nodes (Python)

Once all packages are processed, pipe collected records to the write-back command:

```bash
echo '<doc_records_json>' | uv run python .claude/skills/socratic-pm/scripts/ingest.py \
  --write-docs \
  --neo4j-uri <neo4j_uri>
```

Print the returned stats: `docs_written`, `apis_written`, `errors`.

---

## Output Summary

After all three phases, print:

```
Ingest complete.

Phase 1 — Package nodes:
  created:    N
  updated:    N
  deprecated: N

Phase 2 — Context7 lookup:
  resolved:   N / <total>
  skipped:    N (not in Context7 index)

Phase 3 — Doc/API nodes:
  docs written: N
  apis written: N

Errors: N
```

If any errors exist, list them below the table.

---

## Edge Cases

- **Neo4j not reachable**: Phase 1 fails with a connection error. Tell user: `docker compose up -d`
- **Package not in Context7**: Log as SKIP, continue. Common for internal/private packages.
- **`config/project.yml` missing**: Use default `bolt://localhost:7687` and warn.
- **`uv` not found**: Fall back to `python` directly and warn.
