# Implementation Plan

Strict sequential phases for building Socratic-PM. Checklists map directly to GitHub issue generation states.

## Phase 1: Concurrency Runtime & TUI
- [ ] Initialize Textual application shell with chat interface, code viewer, and editor layout.
- [ ] Implement DeepAgents background worker thread (asyncio/queue) to prevent UI blocking during agent generation.
- [ ] Scaffold the DeepAgents skills middleware directory to handle basic slash commands.

## Phase 2: Environment Governance & Data Pipelines
- [ ] Implement telemetry polling scripts (local package manager health, coding tool configs, git branch).
- [ ] Route telemetry data to UI status indicators and configuration panes.
- [ ] Build parsing pipelines to extract active packages and configs (this data feeds directly into the GraphRAG ingestion in Phase 3).

## Phase 3: GraphRAG & Socratic Engine
- [ ] Initialize Neo4j local instance and build ingestion schema (mapping `Documentation` nodes to `API Reference` nodes).
- [ ] Define core Socratic prompt constraints (explain code, output schemas to TUI, do not overwrite backend logic).
- [ ] Create guided planning skills that prompt the user with architectural questions layer by layer based on GraphRAG context.

## Phase 4: Deterministic Orchestration & GitHub
- [ ] Implement GitHub MCP server connection.
- [ ] Build AST markdown parser to read `docs/prd.md` and `docs/plan.md`.
- [ ] Implement issue generation skill: convert unchecked plan items into GitHub Issues with specific GraphRAG query targets.
- [ ] Implement task resolution loop: scan merged PRs/commits to main and automatically check off items in `docs/plan.md`.
