# Implementation Plan

Strict sequential phases. Each phase is independently testable before moving forward. Checklists map directly to GitHub issue generation states via `/socratic-pm issue`.

---

## Phase 1: Plugin Skeleton & Router

**Goal:** A working `/socratic-pm` command that routes correctly and loads mode files. Testable end-to-end before any AI engineering is built.

- [ ] Create `.claude/skills/socratic-pm/SKILL.md` with frontmatter, mode routing table, and discovery menu output.
- [ ] Create `modes/_shared.md` with the Socratic constraint policy and placeholder Neo4j schema section.
- [ ] Create stub mode files for all 9 modes (`plan.md`, `issue.md`, `checkpoint.md`, `context.md`, `ingest.md`, `scaffold.md`, `review.md`, `debug.md`, `status.md`) — each with a title and "not yet implemented" body.
- [ ] Create `CLAUDE.md` with data contract table (user layer vs. system layer), session-init checklist, and file index.
- [ ] Create `config/project.example.yml` with fields: `project_name`, `repo`, `primary_language`, `package_manager`, `frameworks`, `neo4j_uri`, `neo4j_database`.
- [ ] Create `modes/_context.template.md` — user fills this with project identity and architecture notes.
- [ ] Verify: `/socratic-pm` with no args shows the discovery menu. `/socratic-pm plan` loads `modes/plan.md` and echoes its stub content.

---

## Phase 2: Telemetry Script

**Goal:** A standalone, zero-LLM Python script that outputs valid JSON. Fully testable without the plugin.

- [ ] Write `scripts/telemetry.py`: detect git branch, uncommitted count, Python version, Node version, active venv, installed packages (pip/poetry/uv), presence of key config files.
- [ ] Output strict JSON schema: `{ git_branch, uncommitted_changes, python_version, node_version, package_manager, installed_packages: [], active_tools: [], env_drift_warnings: [] }`.
- [ ] Implement env drift detection: read `docs/updates.md` entries, compare against detected versions, populate `env_drift_warnings`.
- [ ] Implement `modes/status.md`: call `scripts/telemetry.py` via bash, parse JSON output, format as readable chat report with drift warnings flagged.
- [ ] Verify: `python scripts/telemetry.py` produces valid JSON in a clean terminal. `/socratic-pm status` renders the report in chat correctly.

---

## Phase 3: GraphRAG — Schema, Ingestion, Context Query

**Goal:** Neo4j running locally, documents ingested, Cypher queries returning real data.

- [ ] Write `scripts/schema.cypher`: define constraints and indexes for `Package`, `Documentation`, `API_Reference` nodes and `DEFINES_API_FOR`, `DOCUMENTS` edges.
- [ ] Configure `neo4j-contrib/mcp-neo4j` MCP server in the project's MCP config. Verify Claude Code can run a Cypher query against local Neo4j.
- [ ] Write `scripts/ingest.py`:
  - Scan `pyproject.toml` / `package.json` / lockfiles to detect active packages → create `Package` nodes.
  - Parse `docs/` markdown files → create `Documentation` nodes linked to relevant packages via `DOCUMENTS` edge.
  - Stub: create placeholder `API_Reference` nodes for detected packages (real fetch in next step).
- [ ] Extend `scripts/ingest.py` to fetch API references: parse docstrings from installed packages or fetch from Context7 MCP → create `API_Reference` nodes linked via `DEFINES_API_FOR`.
- [ ] Implement `modes/ingest.md`: orchestrate `ingest.py` execution, report counts of nodes written, surface any errors.
- [ ] Implement `modes/context.md`: accept topic argument, run Cypher traversal, return API contracts injected into chat.
- [ ] Verify: `/socratic-pm ingest` writes nodes. `/socratic-pm context langgraph` returns real API signatures from the graph.

---

## Phase 4: Deterministic Orchestration — Plan Parser, Issues, Checkpoint

**Goal:** Closed-loop workflow: plan.md → GitHub Issues → merged PR → plan.md checked off.

- [ ] Write `scripts/plan_parser.py`: AST markdown parser that returns structured JSON of all checklist items with fields: `phase`, `text`, `checked`, `line_number`.
- [ ] Create `data/issues.md` template: columns `item_text`, `issue_number`, `issue_url`, `status`, `resolved_pr`.
- [ ] Implement `modes/plan.md`: call `plan_parser.py`, output current phase summary, surface next unchecked item as the active task, show progress counts per phase.
- [ ] Implement `modes/issue.md`:
  - Run `plan_parser.py` → find unchecked items not yet in `data/issues.md`.
  - For each item: run context query for relevant framework, create GitHub Issue via GitHub MCP with embedded Cypher query in the body, log to `data/issues.md`.
  - Dispatch as subagent per item when 3+ items are pending.
- [ ] Implement `modes/checkpoint.md`:
  - Fetch merged PRs via GitHub MCP.
  - Match to `data/issues.md` open items by branch name pattern or PR description.
  - Check off resolved items in `docs/plan.md`.
  - Update `data/issues.md` status. Output resolution summary.
- [ ] Verify: `/socratic-pm issue` creates real GitHub Issues. Merging a test PR and running `/socratic-pm checkpoint` checks off the item in `docs/plan.md`.

---

## Phase 5: Socratic Engine — Scaffold, Review, Debug

**Goal:** The three modes that enforce developer accountability and learning. The core differentiator.

- [ ] Implement `modes/scaffold.md`:
  - Read `docs/plan.md` active task + `docs/prd.md` for requirements context.
  - Run `/socratic-pm context` for the relevant framework.
  - Write target file with: full type signatures, requirement-driven docstrings, step-by-step `# Step N:` pseudo-code, `pass` bodies, `__main__` usage example.
  - Output to chat: why the structure is designed this way, what the developer should focus on first.
- [ ] Implement `modes/review.md`: structured review output to chat — correctness, edge cases, architecture alignment, 3 Socratic questions for the developer. No file edits.
- [ ] Implement `modes/debug.md`: Socratic question sequence → ranked hypotheses → diagnostic steps. No file edits. If solution is obvious, describe it in chat and ask the developer to implement it.
- [ ] Verify: `/socratic-pm scaffold src/example.py` writes a valid boilerplate file with zero implementation logic. `/socratic-pm review src/example.py` produces a structured review without editing the file.

---

## Phase 6: Polish, README, and Starter Template

**Goal:** Production-ready plugin and cloneable template that a new developer can use in 5 minutes.

- [ ] Write `README.md`: installation (plugin path), starter template clone instructions, mode reference table, Neo4j setup steps, screenshot or demo GIF.
- [ ] Write `docs/SETUP.md`: step-by-step setup for Neo4j, MCP config, `config/project.yml` initialization, first ingest run.
- [ ] Add update checker to `CLAUDE.md` session-init: compare local `VERSION` file against remote tag, prompt user if update available.
- [ ] Write `test-all.sh`: runs `telemetry.py`, `plan_parser.py`, and a dry-run of `ingest.py` against fixture data. Outputs pass/fail per script.
- [ ] Verify: a clean clone of the repo with a fresh `config/project.yml` and a test `docs/plan.md` reaches a working `/socratic-pm plan` output in under 10 minutes of setup.
