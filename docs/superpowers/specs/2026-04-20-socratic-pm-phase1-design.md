# Socratic-PM Phase 1 Design: Plugin Skeleton & Router

**Date:** 2026-04-20  
**Status:** Design Approved  
**Scope:** Plugin installation structure, SKILL.md routing, mode stubs, data contract, config template

---

## Vision

Socratic-PM is a reusable Claude Code plugin that helps developers learn by managing project tasks while agents handle complementary roles. A developer chooses their learning focus (e.g., AI engineering), and agents manage project management, issue tracking, code review, and debugging. The plugin ties together:
- A markdown checklist (`docs/plan.md`) as source of truth
- GitHub Issues for task tracking
- Neo4j knowledge graph of API contracts and documentation
- AI agents for orchestration, scaffolding, review, and debugging

## Architecture

### Layer 1: Plugin Interface

**SKILL.md** — Single entry point router
- Frontmatter: skill metadata (name, description, version)
- Mode Registry Table: maps mode names to descriptions (9 modes total)
- Routing Logic: reads `{{mode}}` argument, loads `modes/{mode}.md` + injects `modes/_shared.md`
- Discovery: shows menu on `/socratic-pm` with no args, errors gracefully on unknown mode

**modes/_shared.md** — Always-injected context
- Socratic Constraints: agents write scaffolds only (type sigs, docstrings, pseudo-code), no implementation logic, output architectural guidance to chat
- Neo4j Node Schema: Package, Documentation, API_Reference nodes and their edges
- GitHub MCP Conventions: issue naming (`[PHASE-N] text`), body structure (description + Cypher query), label strategy (`phase-N`, `needs-james`)
- File Paths Reference: `docs/plan.md`, `docs/prd.md`, `docs/updates.md`, `data/issues.md`, `config/project.yml`

**modes/{mode}.md** (9 stubs)
- `plan.md` — display phase, progress, next unchecked item
- `issue.md` — create GitHub issues from unchecked plan items
- `checkpoint.md` — match merged PRs to issues, check off completed items in plan
- `context.md` — query Neo4j for API contracts by framework/topic
- `ingest.md` — populate Neo4j: packages, docs, API references
- `scaffold.md` — write boilerplate with type sigs, docstrings, pseudo-code
- `review.md` — structured code review output to chat (no file edits)
- `debug.md` — Socratic debugging: hypotheses, diagnostic steps (no file edits)
- `status.md` — run telemetry, show environment drift vs `docs/updates.md`

Each stub has minimal structure: frontmatter + "not yet implemented" body. Phases 2-6 fill in logic without changing structure.

**modes/_context.template.md** — User-filled project identity and architecture notes

### Layer 2: Data Contract (CLAUDE.md)

**User Layer** (preserved across plugin updates, but modifiable by agents at runtime):
- `docs/plan.md` — checklist source of truth (agents can check off items via checkpoint mode)
- `docs/prd.md` — requirements context (agents read, never write)
- `config/project.yml` — project configuration (user fills from example, agents read)
- `modes/_context.template.md` — user fills with project identity

**System Layer** (safe to overwrite on plugin update):
- `modes/{plan,issue,checkpoint,context,ingest,scaffold,review,debug,status}.md` — agent instructions
- `modes/_shared.md` — constraints and schema
- `scripts/` — telemetry.py, plan_parser.py, ingest.py (added in Phase 2+)

**Session-Init Checklist:**
- Verify `config/project.yml` exists; error if missing, point to `config/project.example.yml`
- Verify `docs/plan.md` is valid markdown; warn if malformed
- Check if Neo4j URI (from config) is reachable; warn if not, but don't block

### Layer 3: Project Configuration

**config/project.example.yml** — Template users copy to `config/project.yml`

```yaml
# Project Identity
project_name: "my-app"
repo: "https://github.com/user/my-app"
primary_language: "python"  # or javascript, go, etc.
package_manager: "uv"       # or npm, pip, poetry, etc.
frameworks:
  - name: "langgraph"
    version: "0.2.0"
  - name: "next.js"
    version: "15.0"

# Neo4j Connection (Phase 3+)
neo4j_uri: "bolt://localhost:7687"
neo4j_database: "neo4j"

# Developer Role (learning focus)
developer_role: "ai-engineering"  # or "frontend", "backend", etc.
```

Modes read this config to populate context: frameworks for ingest, role for coaching, repo for GitHub MCP integration.

## File Structure

```
.claude/skills/socratic-pm/
├── SKILL.md
├── CLAUDE.md
├── modes/
│   ├── _shared.md
│   ├── _context.template.md
│   ├── plan.md
│   ├── issue.md
│   ├── checkpoint.md
│   ├── context.md
│   ├── ingest.md
│   ├── scaffold.md
│   ├── review.md
│   ├── debug.md
│   └── status.md
└── config/
    └── project.example.yml
```

## Routing Example

```
User runs: /socratic-pm plan

SKILL.md:
  1. Parses mode="plan"
  2. Looks up "plan" in mode registry table
  3. Loads modes/_shared.md, then modes/plan.md
  4. Injects both into chat context
  5. Agent responds with stub content (or implemented logic in later phases)

User runs: /socratic-pm help

SKILL.md:
  1. Mode is empty/help
  2. Shows discovery menu with all 9 modes + descriptions from registry table
```

## Success Criteria (Testable Phase 1)

- [ ] `/socratic-pm` with no args shows discovery menu listing all 9 modes
- [ ] `/socratic-pm plan` loads modes/plan.md + modes/_shared.md, echoes stub content
- [ ] `/socratic-pm help` shows same discovery menu
- [ ] `/socratic-pm unknown` errors gracefully with suggestion to use help
- [ ] `config/project.example.yml` exists, is valid YAML, documents all required fields
- [ ] CLAUDE.md clearly delineates user vs system layers
- [ ] Session-init checks pass when `config/project.yml` exists and valid
- [ ] Session-init warns when Neo4j URI unreachable, but doesn't block

## Design Rationale

**Why Approach A (monolithic SKILL.md)?**
- Phase 1 is about validation, not discoverability at scale
- Self-contained, no runtime directory scanning
- Simpler to test and debug
- Can refactor to dynamic discovery (Approach B) in later phases without breaking existing modes

**Why separate _shared.md?**
- Avoids duplication across 9 mode files
- Single source of truth for constraints and schema
- Easy to update Neo4j schema or GitHub conventions in one place

**Why config/project.yml instead of environment variables?**
- Portable across machines (devs can commit project config, not secrets)
- Readable format for teams
- Can track config history in git (if not containing secrets)

**Why user layer + system layer split?**
- Protects user's project state when plugin is updated/reinstalled
- Allows safe upgrades without losing work
- Clear boundary: plugin updates can't clobber user projects

## Next Steps

After Phase 1 approval and implementation:
- **Phase 2:** Telemetry script + status mode validation
- **Phase 3:** Neo4j schema, ingestion, context queries
- **Phase 4:** Plan parser, GitHub issue orchestration, checkpoint logic
- **Phase 5:** Socratic engine (scaffold, review, debug modes)
- **Phase 6:** Polish, README, starter template, multi-tool support

---

**Design Document Approved:** [pending user review]
