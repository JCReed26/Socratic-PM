# Socratic-PM

Socratic-PM is an asynchronous, terminal-based Project Manager and educational constraint engine for AI-assisted development. It sits between the human engineer and their local/remote AI agent fleet to manage the "Meta-Work"—environment configurations, package dependencies, and deterministic project planning.

Built with Python, Textual, and LangChain DeepAgents, Socratic-PM enforces developer accountability. Instead of "vibe coding" backend logic, the AI acts as a senior architect: explaining concepts, providing API contracts, and ensuring the human engineer types the code to build deep codebase comprehension.

## Features & Roadmap

- [ ] **Phase 1: Concurrency Runtime & TUI**
  - [ ] Asynchronous LangChain DeepAgents background worker queue.
  - [ ] Terminal UI (Textual) with a dedicated code viewer and editor layout.
  - [ ] Real-time environment telemetry (Git status, package managers, tool configs).
  - [ ] DeepAgents skills middleware for slash commands (e.g., `/npm`, `/docs`).

- [ ] **Phase 2: Project Management & Orchestration**
  - [ ] GitHub MCP integration for issue generation.
  - [ ] Deterministic Markdown AST parsing (reads `docs/` as the single source of truth).
  - [ ] Automated Git lifecycle management and task resolution tracking (PRs mapped to checklist items).

- [ ] **Phase 3: Educational Constraint Engine (Socratic Method)**
  - [ ] Strict output constraints: AI explains code and provides schemas, but does not overwrite core backend logic.
  - [ ] Guided architectural planning skills executed layer-by-layer.
  - [ ] Structural codebase breakdowns and function mapping.

- [ ] **Phase 4: Knowledge Graph (GraphRAG)**
  - [ ] Neo4j-backed database separating generic documentation from exact API references.
  - [ ] GraphRAG query injection into sub-agent GitHub Issues.
  - [ ] High-relevance context retrieval cross-referenced with the local `docs/` directory.

## Tech Stack

- **Agent Framework:** LangChain DeepAgents
- **Terminal Interface:** Textual (Python)
- **Knowledge Graph (GraphRAG):** Neo4j
- **Delegation/Orchestration:** GitHub MCP / PyGithub

## Documentation

For detailed architectural schemas, data flows, and project requirements, please refer to the `docs/` directory:
- [Product Requirements (PRD)](docs/prd.md)
- [Architecture](docs/architecture.md)
- [Implementation Plan](docs/plan.md)
