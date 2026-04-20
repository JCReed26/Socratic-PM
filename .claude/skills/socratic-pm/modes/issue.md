---
name: issue
description: Create GitHub issues from unchecked plan items
---

# Mode: issue

Not yet implemented. Phase 4+ will add:
- Run plan_parser.py to find unchecked items
- For each unchecked item not yet in data/issues.md:
  - Run /socratic-pm context for relevant framework
  - Create GitHub Issue via GitHub MCP with embedded Cypher query
  - Log to data/issues.md
- Dispatch as subagent per item when 3+ items pending
