# Agent Directives

Strict operating procedures for AI agents functioning within the `Socratic-PM` repository.

## 1. Domain Write Constraints
**AI coding agents are strictly prohibited from writing, editing, or generating logic for:**
- GraphRAG infrastructure (Neo4j mappings, ingestion scripts).
- DeepAgents configuration and execution loops.
- Core orchestration and GitHub issue generation logic.

**Permitted Write Domain:**
- `src/tui/`: Frontend Terminal User Interface components written in Python/Textual.
- Markdown files (when instructed to update documentation states).

## 2. Orchestration & State
- All task state is deterministic and derived from the `docs/` directory.
- Do not create hidden directories (e.g., `.socratic/`) for state management.
- Checklists in `docs/plan.md` and `docs/prd.md` represent exact binary states for the project orchestrator.

## 3. The Socratic Method
- The agent's primary role regarding backend logic is educational.
- When assisting with logic outside of the `src/tui/` directory, agents must output code examples, API contracts, and structural plans to the chat interface.
- Do not automatically overwrite backend Python files. The human engineer must type the implementation to ensure codebase accountability and disaster recovery knowledge.

## 4. DeepAgents Skills
- All dynamic commands (e.g., slash commands) and guided task questioning must utilize the LangChain DeepAgents skills middleware.
- Skills should be modularly defined in the agent skills directory.
