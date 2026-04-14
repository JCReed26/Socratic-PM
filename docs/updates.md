# Dependency & Environment Updates

Strict schema for logging package updates, architectural decisions, and API dependency requirements.

**Format:** `YYYY-MM-DD-HH:MM | file_path | specific_explanation`

## Entries

- 2026-04-07-18:00 | src/agents/server.py | fastapi requires uvicorn version x.y.z to utilize feature A in fastapi version x.y.z.

- 2026-04-13-00:00 | docs/* | ARCHITECTURAL PIVOT: Abandoned custom Textual TUI + LangChain DeepAgents standalone application. Rearchitected as a coding-agent-agnostic Claude Code plugin following the career-ops skill pattern. Rationale: (1) TUI engineering effort was disproportionate to AI engineering value; (2) Neo4j official MCP server (neo4j-contrib/mcp-neo4j) and neo4j-contrib/neo4j-skills eliminate the need for a custom database integration layer; (3) Plugin architecture enables dual distribution — drop into any project as a skill, or clone as a starter template; (4) All 5 core AI engineering concepts (GraphRAG with real schema design, closed-loop orchestration, context injection with framework detection, Socratic scaffold innovation, standalone telemetry tool) are preserved and in some cases strengthened. LangGraph and LangSmith dropped in favor of Claude Code subagent dispatch and native hooks for observability. Write restrictions enforced via modes/_shared.md Socratic constraint policy rather than OS-level filesystem boundaries.
