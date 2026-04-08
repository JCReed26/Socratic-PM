# Product Requirements Document

## 1. Data Schemas & State Management

### 1.1 TUI Frontend (Textual)
- **Requirement:** Decoupled terminal interface running on the main thread, supporting a dedicated code viewer and editor pane.
- **State:** Consumes JSON telemetry from background workers regarding environment status (global/local packages, active tools, git branch).
- **Routing:** DeepAgents skills middleware processes slash commands to trigger specific UI config panes.

### 1.2 Asynchronous Agent Runtime
- **Requirement:** LangChain DeepAgents instantiated in background worker threads/queues.
- **Capabilities:** Must process LLM I/O asynchronously, allowing the user to navigate the TUI, read code, or use slash commands while agents generate responses.
- **Skills:** Relies on dynamically loaded DeepAgents skills to execute distinct actions (e.g., querying GitHub, reading environment configs).

### 1.3 Project Manager Orchestrator
- **Requirement:** A strictly deterministic markdown parser that controls project delegation.
- **Data Source:** Reads exclusively from the `docs/` directory. No secondary hidden state directories.
- **Execution:** 
  1. Parses `docs/plan.md` for incomplete tasks.
  2. Uses GitHub MCP to generate issues.
  3. Appends specific GraphRAG queries and agent constraints into the issue description.
  4. Monitors the repository for merged branches solving the issue.
  5. Modifies the markdown file to check off completed items.

### 1.4 Knowledge Graph (GraphRAG)
- **Requirement:** Neo4j database separating conceptual docs from API definitions.
- **Data Schema:** 
  - `Node: Package`
  - `Node: Documentation`
  - `Node: API_Reference`
  - `Edge: DEFINES_API_FOR`
- **Logic:** The orchestrator correlates strict local requirements from `docs/` with the GraphRAG to retrieve exact implementation parameters for assigned agents.

## 2. API Contracts & Behavior

### 2.1 The Socratic Constraint
- The application will output backend code examples, function definitions, and file structures exclusively to the TUI interface.
- The human engineer is required to manually implement core engineering files to guarantee codebase comprehension and retention.
- AI file-system write access is restricted primarily to the `src/tui/` directory.

### 2.2 Telemetry Parsing
- Local and global environments are scanned deterministically.
- Output schema maps tool configurations, package manager health, and active plugins to visual dashboard components to identify environment drift immediately.
