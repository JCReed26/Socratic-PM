---
name: socratic-pm
description: Project management and learning framework for developers. Manage plans, issues, code reviews, and debugging with AI agents while you focus on your learning role.
version: 0.1.0
---

# Socratic-PM Skill

Reusable Claude Code plugin for learning-first development. Route to different modes based on task.

## Mode Registry

| Mode | Purpose |
|------|---------|
| plan | View current phase, progress, next unchecked item |
| issue | Create GitHub issues from unchecked plan items |
| checkpoint | Match merged PRs to issues, check off completed items |
| context | Query Neo4j for API contracts by framework/topic |
| ingest | Populate Neo4j: packages, docs, API references |
| scaffold | Write boilerplate: type sigs, docstrings, pseudo-code |
| review | Structured code review output (no file edits) |
| debug | Socratic debugging: hypotheses, diagnostic steps (no file edits) |
| status | Run telemetry, show environment drift |

## Routing Logic

Reads `{{mode}}` argument:
- If mode exists in registry → load `modes/{mode}.md` + inject `modes/_shared.md`
- If no mode or "help" → show discovery menu with all modes + descriptions
- If mode not found → error with available modes suggestion

---

## Discovery Menu

```
/socratic-pm [mode]

Usage: /socratic-pm [mode]

Available modes:
  plan       View current phase, progress, next unchecked item
  issue      Create GitHub issues from unchecked plan items
  checkpoint Match merged PRs to issues, check off completed items
  context    Query Neo4j for API contracts by framework/topic
  ingest     Populate Neo4j: packages, docs, API references
  scaffold   Write boilerplate: type sigs, docstrings, pseudo-code
  review     Structured code review output (no file edits)
  debug      Socratic debugging: hypotheses, diagnostic steps (no file edits)
  status     Run telemetry, show environment drift

Try: /socratic-pm help
```
