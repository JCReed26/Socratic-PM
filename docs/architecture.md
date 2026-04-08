# Socratic-PM Architecture

Strict separation of concerns across a 4-layer terminal application.

## Layer 1: Concurrency & Interface

- **TUI (Textual):** Main thread. Manages rendering, layout routing, and the dedicated code viewer/editor.
- **Agent Worker:** Background asyncio thread/queue running LangChain DeepAgents. Prevents UI blocking.
- **Telemetry:** Deterministic polling of system state (git branch, package manager health, coding tools).
- **Navigation:** DeepAgents skills middleware triggers slash commands to open config panes.

## Layer 2: Deterministic Orchestration

- **State:** Derived 100% from the `docs/` directory. 
- **Task Delegation:** 
  - AST parser reads `docs/plan.md`.
  - GitHub MCP generates issues based on unchecked lists.
  - Issue descriptions contain rigid instructions on what to query the GraphRAG for.
- **Resolution:** Agent pushes code -> PR merged to main -> PM agent reads repository state -> checks off `docs/plan.md`.

## Layer 3: Socratic Engine

- **Goal:** Developer accountability and learning.
- **Constraint:** Agents must not write backend Python files. They must output function schemas, code examples, and file structures to the TUI.
- **Execution:** Human developer physically types the core logic.
- **Skills:** DeepAgents utilizes a skills directory to inject guided architectural questions layer by layer before allowing implementation.

## Layer 4: Relational Context (GraphRAG)

- **Database:** Neo4j.
- **Schema:** Strict separation of `Documentation` nodes and `API Reference` nodes, linked back to their parent packages.
- **Context Pipeline:** The PM prioritizes reading the local `docs/` directory for project relevance, cross-referencing with GraphRAG to pull exact API contracts and version requirements for sub-agents.
