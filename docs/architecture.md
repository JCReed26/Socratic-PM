# Socratic-PM Architecture

Coding-agent-agnostic plugin with strict separation of concerns across 4 layers. Installs into any project via `.claude/skills/` (Claude Code), `.cursor/skills/`, or equivalent. Also ships as a standalone starter template.

## Layer 1: Plugin Interface

- **SKILL.md:** Single entry point router. Reads the `{{mode}}` argument and determines which mode file to load. No logic lives here — routing only.
- **CLAUDE.md:** Data contract defining which files belong to the user layer (never auto-updated) vs. the system layer (safe to update). Runs session-init checks on first message.
- **modes/_shared.md:** Always-loaded context injected before every mode. Contains the Socratic write constraints, Neo4j node schema, and GitHub MCP conventions.
- **modes/{mode}.md:** Task-specific agent instructions. Loaded on demand. Each file is a self-contained agent context — not a script, a reasoning spec.
- **Subagent Delegation:** Heavy or parallel tasks (issue generation per item, large ingestion runs) are dispatched as subagents with `_shared.md` + the relevant mode file injected into the subagent prompt.

## Layer 2: Deterministic Orchestration

- **State:** Derived exclusively from the `docs/` directory. No hidden state directories.
- **plan_parser.py:** AST markdown parser that reads `docs/plan.md` and extracts unchecked items with their parent phase context.
- **Issue Generation (`issue` mode):**
  1. plan_parser.py identifies unchecked items.
  2. GitHub MCP creates a GitHub Issue per item.
  3. Each issue description embeds the specific Neo4j Cypher query the implementing agent must run to retrieve relevant API contracts before writing code.
- **Resolution Loop (`checkpoint` mode):**
  1. Scan merged PRs and commits to main branch.
  2. Match branch names and commit messages to open issue numbers.
  3. Modify `docs/plan.md` to check off resolved items.
  4. Post resolution summary to chat.

## Layer 3: Socratic Engine

- **Goal:** Developer accountability, codebase comprehension, and retention.
- **Constraint (enforced via `_shared.md`):** Agents may write scaffold files only — type signatures, docstrings, and pseudo-code TODO comments. Agents must not write implementation logic. All design explanations, API examples, and architectural guidance are output to chat.
- **scaffold mode:** Writes a valid file with full type annotations, docstrings describing what the function must accomplish, and step-by-step pseudo-code as inline comments. The developer reads the file and implements the logic themselves.
- **review mode:** Outputs a structured code review to chat. Never edits the file.
- **debug mode:** Runs guided Socratic questioning — asks the developer what they expect vs. what they observe, outputs hypotheses and diagnostic steps. Never edits the file.
- **Iterative Loop:** scaffold → developer implements → review → developer refines → checkpoint resolves the issue.

## Layer 4: Relational Context (GraphRAG)

- **Database:** Neo4j, connected via the official `neo4j-contrib/mcp-neo4j` MCP server.
- **Node Schema:**
  - `Node: Package` — a library or framework in the project's dependency graph.
  - `Node: Documentation` — conceptual explanation of a Package (how it works, patterns, best practices).
  - `Node: API_Reference` — exact API contract for a Package (function signatures, parameters, return types, version pins).
  - `Edge: DEFINES_API_FOR` — links an `API_Reference` node to its parent `Package`.
  - `Edge: DOCUMENTS` — links a `Documentation` node to its parent `Package`.
- **Ingestion Pipeline (`ingest` mode + `scripts/ingest.py`):**
  1. Detects active frameworks by scanning `docs/`, `pyproject.toml`, `package.json`, and lockfiles.
  2. Parses local `docs/` markdown into `Documentation` nodes.
  3. Fetches or reads API references and creates `API_Reference` nodes linked to detected packages.
  4. Writes the graph to Neo4j via Cypher.
- **Context Retrieval (`context` mode):**
  - Accepts a topic or framework name.
  - Runs a Cypher traversal: Package → API_Reference → Documentation.
  - Returns exact API contracts, version requirements, and usage patterns.
  - Output is injected into the current agent context or embedded into GitHub Issue descriptions.
