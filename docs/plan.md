# Implementation Plan

Strict sequential phases for building Socratic-PM. Checklists map directly to GitHub issue generation states.

## Phase 1: Concurrency Runtime & TUI
- [ ] Initialize Textual application shell with a dedicated code viewer and editor layout.
- [ ] Implement DeepAgents background worker thread (asyncio/queue) to prevent UI blocking during agent generation.
- [ ] Implement telemetry polling (git branch status, local package manager health, coding tool configs) and route data to UI status indicators.
- [ ] Scaffold the DeepAgents skills middleware directory to handle slash commands (e.g., `/npm`, `/docs`).

## Phase 2: Project Management & Orchestration
- [ ] Implement GitHub MCP server connection.
- [ ] Build AST markdown parser to read `docs/prd.md` and `docs/plan.md`.
- [ ] Implement the issue generation skill: convert unchecked plan items into GitHub Issues containing specific DeepAgents retrieval instructions.
- [ ] Implement the task resolution loop: scan merged PRs/commits to main and automatically check off items in `docs/plan.md`.

## Phase 3: Socratic Engine & Skills Middleware
- [ ] Define the core Socratic prompt constraints (output code to TUI, do not overwrite backend files).
- [ ] Create guided planning skills that prompt the user with architectural questions layer by layer before code execution.
- [ ] Build structural file breakdown skills to explain required functions, state constraints, and data flows.

## Phase 4: Neo4j GraphRAG Integration
- [ ] Initialize Neo4j local instance.
- [ ] Build ingestion pipeline schema mapping `Documentation` nodes to `API Reference` nodes linked by `DOCUMENTS` relationships.
- [ ] Expose GraphRAG queries to the Orchestrator to inject version-specific API context into GitHub issues.
- [ ] Implement query synthesis allowing DeepAgents to cross-reference the local `docs/` directory with the GraphRAG for high-relevance data retrieval.
