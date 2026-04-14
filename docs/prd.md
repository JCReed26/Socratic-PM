# Product Requirements Document

## 1. Plugin Interface & Distribution

### 1.1 Dual Distribution Model
- **Plugin:** The `.claude/skills/socratic-pm/` directory installs into any existing project. The skill becomes available as `/socratic-pm` in that project's coding agent session alongside other installed plugins.
- **Starter Template:** The full repository ships as a cloneable project template. Includes pre-wired skill, docs structure, config templates, and scripts. Developer fills in `docs/plan.md` with their project and the system is ready to orchestrate.
- **Agent Agnostic:** SKILL.md follows the open agent skills standard. Compatible with Claude Code, Cursor, Codex, Gemini CLI, and any coding agent that supports the skills directory convention.

### 1.2 SKILL.md Router
- **Requirement:** Single entry point. Reads `{{mode}}` argument. Routes to correct mode file. Contains zero business logic.
- **Modes:** `plan`, `issue`, `checkpoint`, `context`, `ingest`, `scaffold`, `review`, `debug`, `status`.
- **Discovery:** Invoking `/socratic-pm` with no arguments displays the command menu.
- **Subagent delegation:** Modes that require parallel execution or heavy I/O dispatch subagents with `_shared.md` + mode file content injected into the prompt.

### 1.3 Data Contract
- **User Layer (never auto-updated):** `docs/plan.md`, `docs/prd.md`, `docs/architecture.md`, `config/project.yml`, `modes/_context.md`, `data/*`.
- **System Layer (safe to update):** `SKILL.md`, `modes/_shared.md`, all other mode files, `scripts/*`, `CLAUDE.md`.
- **Rule:** All user customizations (project identity, tech stack, team conventions) live in `config/project.yml` and `modes/_context.md`. System updates never touch these files.

---

## 2. The 9 Modes — Behavioral Requirements

### 2.1 `plan` — Status Reader
- Read `docs/plan.md` via `scripts/plan_parser.py`.
- Output: current phase, count of completed vs. unchecked items, the single next unchecked item surfaced as the active task.
- Must not modify any file.

### 2.2 `issue` — Orchestration Trigger
- Run `plan_parser.py` to extract all unchecked items.
- For each unchecked item without an existing open GitHub Issue (check `data/issues.md`):
  1. Run `/socratic-pm context {relevant framework}` to retrieve the Cypher query target.
  2. Create a GitHub Issue via GitHub MCP. Issue title = plan item text. Issue body = phase context + embedded Cypher query string the implementing agent must run + Socratic constraint reminder.
  3. Log the issue number and URL to `data/issues.md`.
- Dispatch as subagent per issue for parallelism when 3+ items are pending.

### 2.3 `checkpoint` — Resolution Loop
- Fetch recent merged PRs and commits to main via GitHub MCP.
- Match branch names (pattern: `socratic-pm/{issue-number}-{slug}`) and PR descriptions to open issues in `data/issues.md`.
- For each matched resolution:
  1. Check off the corresponding item in `docs/plan.md`.
  2. Mark the issue as closed in `data/issues.md`.
- Output resolution summary to chat.

### 2.4 `context` — GraphRAG Query
- Accept a topic or framework name as argument.
- Run Cypher traversal against Neo4j: `MATCH (p:Package {name: $topic})-[:DEFINES_API_FOR]-(a:API_Reference) RETURN a`.
- Return exact API contracts, version pins, and usage patterns injected into chat context.
- If Neo4j is not reachable, fall back to reading `docs/` directory and output a warning.

### 2.5 `ingest` — Knowledge Graph Pipeline
- Trigger: developer runs `/socratic-pm ingest` after adding new docs or dependencies.
- Execute `scripts/ingest.py`:
  1. Detect active frameworks: scan `pyproject.toml`, `package.json`, lockfiles, `docs/`.
  2. Parse `docs/` markdown files → `Documentation` nodes.
  3. Fetch API references for detected packages → `API_Reference` nodes.
  4. Write graph to Neo4j via `neo4j-contrib/mcp-neo4j` MCP server.
- Output: count of nodes written, packages detected, any ingestion errors.

### 2.6 `scaffold` — Socratic Boilerplate
- Accept a target file path as argument.
- Read `docs/plan.md` and `docs/prd.md` for task context. Run `context` mode for relevant API contracts.
- Write the file with:
  - Full function signatures with type annotations.
  - Docstrings stating what the function must accomplish (not how).
  - Step-by-step pseudo-code as inline `# Step N:` comments.
  - Zero implementation logic — all bodies are `pass` or `raise NotImplementedError`.
  - A `__main__` block with example usage demonstrating expected inputs and outputs.
- Output to chat: a Socratic summary explaining why the structure is designed this way and what the developer should focus on when implementing.

### 2.7 `review` — Socratic Code Review
- Read the specified file(s).
- Output a structured review to chat: correctness, edge cases, adherence to `docs/architecture.md` patterns, questions for the developer to consider.
- Must not edit any file.

### 2.8 `debug` — Guided Debugging
- Begin with structured Socratic questions: "What did you expect to happen? What actually happened? What have you ruled out?"
- Based on developer responses, output ranked hypotheses with diagnostic steps.
- Must not edit any file. If a fix is obvious, describe it in chat — do not apply it.

### 2.9 `status` — Telemetry Report
- Execute `scripts/telemetry.py`.
- telemetry.py outputs JSON: `{ git_branch, uncommitted_changes, python_version, node_version, detected_package_manager, installed_packages, active_tools, env_drift_warnings }`.
- Format the JSON into a readable chat report. Flag any env drift warnings prominently.

---

## 3. GraphRAG Schema

```cypher
// Nodes
(:Package {name: String, version: String, ecosystem: String})
(:Documentation {title: String, content: String, source_file: String})
(:API_Reference {function: String, signature: String, params: String, returns: String, version_pin: String, source_url: String})

// Edges
(:API_Reference)-[:DEFINES_API_FOR]->(:Package)
(:Documentation)-[:DOCUMENTS]->(:Package)
```

- **Ingestion source for Documentation nodes:** local `docs/` markdown files.
- **Ingestion source for API_Reference nodes:** parsed docstrings, official API reference pages, or lockfile-pinned versions cross-referenced with Context7 MCP.
- **Query pattern for issue embedding:** `MATCH (p:Package {name: $framework})-[:DEFINES_API_FOR]-(a:API_Reference {function: $fn}) RETURN a.signature, a.params, a.version_pin`.

---

## 4. Socratic Constraint Policy

Enforced via `modes/_shared.md` — injected into every mode's context:

- Agents may write to: `data/`, `scripts/` (utility scripts only), and scaffold target files (boilerplate only).
- Agents must not write implementation logic to any file.
- Agents must not write to `docs/plan.md` except the `checkpoint` mode checking off resolved items.
- All code examples, API contracts, architectural explanations, and design guidance are output to chat.
- When a developer asks the agent to implement logic for them: respond with a Socratic question about what they already understand, then output a design spec to chat rather than writing the code.

---

## 5. Telemetry Script Requirements

`scripts/telemetry.py` is a standalone Python script with zero LLM dependency:

- Detects: git branch, uncommitted file count, Python version, Node version, active virtual environment, installed packages (pip/poetry/uv), package manager health, presence of key tool configs (`.env`, `pyproject.toml`, `package.json`, `neo4j.conf`).
- Outputs: strict JSON to stdout.
- Testable in isolation: `python scripts/telemetry.py` produces valid JSON with no agent involved.
- Env drift detection: compares detected package versions against versions recorded in `docs/updates.md`. Flags mismatches.
