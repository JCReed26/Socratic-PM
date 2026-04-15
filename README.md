# Socratic-PM

A coding-agent-agnostic plugin and starter template that sits between you and your AI agent to manage the meta-work of software development — environment health, project planning, knowledge graph context, and developer accountability.

Instead of letting AI write your codebase for you, Socratic-PM enforces a constraint: the agent scaffolds structure, asks the right questions, and injects exact API contracts from a live knowledge graph. You write the logic. The result is a codebase you actually understand.

Works as a drop-in plugin for Claude Code, Cursor, Codex, Gemini CLI, and any coding agent that supports the skills directory convention. Also ships as a full starter template for new projects.

---

## UNDER CONSTRUCTION

In planning phase

---

## How It Works

One command, nine modes:

```
/socratic-pm                          → show command menu
/socratic-pm plan                     → read docs/plan.md, surface active task
/socratic-pm issue                    → convert unchecked plan items to GitHub Issues
/socratic-pm checkpoint               → scan merged PRs, check off resolved items
/socratic-pm context {framework}      → query Neo4j for exact API contracts
/socratic-pm ingest                   → detect frameworks, build knowledge graph
/socratic-pm scaffold {file}          → write boilerplate with pseudo-code TODOs
/socratic-pm review {file}            → structured Socratic code review to chat
/socratic-pm debug                    → guided debugging via Socratic questions
/socratic-pm status                   → telemetry: git, packages, env health
```

---

## Installation

### As a Plugin (drop into any project)

```bash
# Claude Code
git clone https://github.com/your-username/socratic-pm ~/.claude/skills/socratic-pm

# Cursor / Codex / Gemini CLI
# Clone into your agent's skills directory equivalent
```

The `/socratic-pm` command is immediately available in your next agent session. Bring your own `docs/plan.md`.

### As a Starter Template (new project)

```bash
git clone https://github.com/your-username/socratic-pm my-project
cd my-project
cp config/project.example.yml config/project.yml
# Fill in project_name, repo, frameworks, neo4j_uri
```

Then write your `docs/plan.md` and run `/socratic-pm ingest` to build the knowledge graph.

---

## The Five Engines

### 1. GraphRAG — Real Schema Design

Socratic-PM builds and queries a Neo4j knowledge graph with a strict node schema:

```cypher
(:Package {name, version, ecosystem})
(:Documentation {title, content, source_file})
(:API_Reference {function, signature, params, returns, version_pin})

(:API_Reference)-[:DEFINES_API_FOR]->(:Package)
(:Documentation)-[:DOCUMENTS]->(:Package)
```

`/socratic-pm ingest` detects your active frameworks from `pyproject.toml`, `package.json`, and lockfiles, parses your `docs/` into `Documentation` nodes, and fetches exact API contracts into `API_Reference` nodes. `/socratic-pm context {framework}` runs a Cypher traversal and injects the result into the agent's live context.

### 2. Closed-Loop Orchestration

`docs/plan.md` is the single source of truth. No hidden state directories.

```
/socratic-pm issue
  → plan_parser.py extracts unchecked items
  → GitHub Issue created per item
  → Issue body embeds the Cypher query the implementing agent must run

developer works → PR merged to main

/socratic-pm checkpoint
  → scans merged PRs, matches to open issues
  → checks off items in docs/plan.md automatically
```

The loop is deterministic and auditable. Every issue traces back to a plan item. Every resolution traces back to a PR.

### 3. Context Injection with Framework Detection

Before creating a GitHub Issue, Socratic-PM runs a context query for the relevant framework and embeds the exact Cypher query target into the issue description. The agent that picks up the issue knows precisely what to retrieve from the graph before writing a line of code — not a vague instruction, a specific graph traversal.

### 4. Socratic Scaffold

`/socratic-pm scaffold src/parser.py` writes a file with:

- Full function signatures with type annotations
- Docstrings stating what each function must accomplish — not how
- Step-by-step `# Step N:` pseudo-code as inline comments
- `pass` bodies — zero implementation logic
- A `__main__` block with example usage

The agent outputs to chat: why the structure is designed this way and what to focus on first. You read the file, understand the contract, and write the implementation. The agent never writes your logic for you.

### 5. Telemetry

`scripts/telemetry.py` is a standalone Python script with zero LLM dependency. Run it directly:

```bash
python scripts/telemetry.py
```

Outputs strict JSON: git branch, uncommitted changes, Python and Node versions, detected package manager, installed packages, active tool configs, and env drift warnings cross-referenced against `docs/updates.md`. `/socratic-pm status` calls it and formats the result in chat.

---

## The Socratic Constraint

Enforced via `modes/_shared.md`, injected into every mode:

- Agents may write scaffold files only — type signatures, docstrings, pseudo-code comments.
- Agents must not write implementation logic to any file.
- All code examples, API contracts, and architectural explanations go to chat.
- When a developer asks the agent to implement logic: the agent asks a Socratic question about what they already understand, then outputs a design spec — not code.

This is a deliberate architectural decision. The goal is a codebase you can defend in an interview because you wrote every line of logic yourself.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Plugin interface | Claude Code Skills / open agent skills standard |
| Knowledge graph | Neo4j + `neo4j-contrib/mcp-neo4j` MCP server |
| GitHub orchestration | GitHub MCP |
| Plan parsing | Python AST markdown parser (`scripts/plan_parser.py`) |
| Telemetry | Standalone Python script (`scripts/telemetry.py`) |
| Ingestion pipeline | Python + Cypher (`scripts/ingest.py`) |
| Subagent dispatch | Native coding agent subagent API |

---

## Project Structure

```
socratic-pm/
├── .claude/skills/socratic-pm/
│   └── SKILL.md                  # Entry point router
├── CLAUDE.md                      # Data contract + session init
├── modes/
│   ├── _shared.md                 # Socratic constraints + Neo4j schema (always loaded)
│   ├── _context.template.md       # User fills: project identity, architecture notes
│   └── {mode}.md                  # One file per mode — self-contained agent spec
├── scripts/
│   ├── ingest.py                  # Framework detection + Neo4j ingestion
│   ├── plan_parser.py             # Markdown AST → structured checklist JSON
│   ├── telemetry.py               # Env health → JSON (no LLM)
│   └── schema.cypher              # Neo4j constraints and indexes
├── config/
│   └── project.example.yml        # User config template
├── docs/                          # Source of truth (user layer — never auto-updated)
│   ├── plan.md
│   ├── prd.md
│   └── architecture.md
└── data/                          # Gitignored runtime state
    └── issues.md                  # Issue log (generated)
```

---

## Documentation

- [Architecture](docs/architecture.md) — 4-layer design, GraphRAG schema, orchestration flow
- [Product Requirements](docs/prd.md) — behavioral spec for all 9 modes, data contract, constraint policy
- [Implementation Plan](docs/plan.md) — 6 phases, each independently testable

---

## Roadmap

| Phase | Goal | Target |
|---|---|---|
| 1 | Plugin skeleton, SKILL.md router, all mode stubs | 4/18/26 |
| 2 | Telemetry script + status mode | 4/25/26 |
| 3 | Neo4j schema, ingest pipeline, context mode | 5/2/26 |
| 4 | Plan parser, issue generation, checkpoint loop | 5/9/26 |
| 5 | Scaffold, review, debug modes | 5/16/26 |
| 6 | Polish, SETUP.md, test suite, starter template | 5/23/26 |
