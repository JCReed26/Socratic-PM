# Socratic-PM Plugin: Data Contract & Session Init

## Data Contract: User Layer vs System Layer

**User Layer** (preserved on plugin reinstall, but modifiable by agents at runtime):
- `docs/plan.md` — checklist source of truth. Agents (checkpoint mode) can check off completed items via this file.
- `docs/prd.md` — requirements context. Agents read, never write.
- `config/project.yml` — project configuration. User fills from config/project.example.yml. Agents read, never write.
- `modes/_context.template.md` — user-filled project identity and architecture notes.

**System Layer** (safe to auto-update on plugin reinstall):
- `modes/plan.md, issue.md, checkpoint.md, context.md, ingest.md, scaffold.md, review.md, debug.md, status.md` — agent instructions for each mode.
- `modes/_shared.md` — shared constraints, Neo4j schema, GitHub conventions.
- `scripts/telemetry.py, plan_parser.py, ingest.py` — Phase 2+ Python utilities (zero-LLM, fully deterministic).

## Session-Init Checklist

Run on every `/socratic-pm` invocation:

- [ ] **Verify `config/project.yml` exists**
  - If missing: Error message suggesting copy from `config/project.example.yml`
  - If exists: Parse as YAML, verify required fields: `project_name`, `repo`, `primary_language`, `neo4j_uri`

- [ ] **Verify `docs/plan.md` is valid markdown**
  - Parse checklist items
  - Warn (but don't block) if malformed

- [ ] **Check Neo4j URI reachable (Phase 3+)**
  - Read `neo4j_uri` from `config/project.yml`
  - Test connection via MCP
  - Warn if unreachable, but don't block execution

---

## File Index

**Within Skill (`.claude/skills/socratic-pm/`):**
```
.claude/skills/socratic-pm/
├── SKILL.md                    → Router + mode registry
├── CLAUDE.md                   → This file (data contract)
├── modes/
│   ├── _shared.md              → Constraints, schema, conventions (always injected)
│   ├── _context.template.md    → Template: user copies to project root as modes/_context.md
│   ├── plan.md                 → Mode: view plan status
│   ├── issue.md                → Mode: create issues
│   ├── checkpoint.md           → Mode: close issues, check plan
│   ├── context.md              → Mode: query Neo4j
│   ├── ingest.md               → Mode: populate Neo4j
│   ├── scaffold.md             → Mode: write boilerplate
│   ├── review.md               → Mode: code review
│   ├── debug.md                → Mode: Socratic debugging
│   └── status.md               → Mode: telemetry + drift
├── scripts/
│   ├── __init__.py             → Package marker
│   ├── telemetry.py            → Zero-LLM environment telemetry (called by status mode)
│   ├── plan_parser.py           → Phase 4+ (plan checklist parser)
│   └── ingest.py                → Phase 3+ (Neo4j ingestion)
└── config/
    └── project.example.yml     → Template: user copies to project root as `config/project.yml`

**At Project Root (user-created from skill templates):**
```
project-root/
├── docs/
│   ├── plan.md                 → Checklist source of truth (user creates/maintains)
│   ├── prd.md                  → Requirements context (user creates/maintains)
│   └── updates.md              → Environment tracking (user creates from skill template)
├── config/
│   └── project.yml             → Project config (user creates by copying `project.example.yml` from skill)
└── data/
    └── issues.md               → Issue mapping (created by issue mode at runtime)
```
