# Socratic-PM

Socratic-PM is an asynchronous, terminal-based Project Manager and educational constraint engine for AI-assisted development. It sits between the human engineer and their local/remote AI agent fleet to manage the "Meta-Work"—environment configurations, package dependencies, and deterministic project planning.

Built with Python, Textual, and LangChain DeepAgents, Socratic-PM enforces developer accountability. Instead of "vibe coding" backend logic, the AI acts as a senior architect: explaining concepts, providing API contracts, and ensuring the human engineer types the code to build deep codebase comprehension.

## Features & Roadmap

- [ ] **Phase 1: Concurrency Runtime & TUI**
  - [ ] Asynchronous LangChain DeepAgents background worker queue.
  - [ ] Terminal UI (Textual) with basic chat, code viewer, and editor layout.
  - [ ] DeepAgents skills middleware for basic slash commands.

- [ ] **Phase 2: Environment Governance & Data Pipelines**
  - [ ] Real-time environment telemetry (Git status, package managers, tool configs).
  - [ ] Package and config parsers to map dependencies (serves as the data ingestion pipeline for GraphRAG).
  - [ ] TUI configuration panes and environment status dashboard.

- [ ] **Phase 3: Knowledge Graph & Socratic Engine**
  - [ ] Neo4j-backed database separating generic documentation from exact API references.
  - [ ] Strict output constraints: AI explains code and provides schemas without overwriting core backend logic.
  - [ ] Guided architectural planning and Socratic questioning skills.

- [ ] **Phase 4: Deterministic Orchestration & GitHub Integration**
  - [ ] Deterministic Markdown AST parsing (reads `docs/` as the single source of truth).
  - [ ] GitHub MCP integration for project issue generation.
  - [ ] Automated Git lifecycle management and task resolution tracking (PRs mapped directly to checklist items).

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

---

### Roadmap

Completion Goal: 5/31/26

Phase 1: due: 4/18

Phase 2: due 4/25

Phase 3: due 5/9

Phase 4: due 5/23
