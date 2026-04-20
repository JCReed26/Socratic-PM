---
name: status
description: Run telemetry and show environment drift
---

# Mode: status

Not yet implemented. Phase 2+ will add:
- Call scripts/telemetry.py (zero-LLM Python script)
- Parse JSON output: git branch, uncommitted changes, Python/Node versions, installed packages
- Compare against docs/updates.md for drift warnings
- Format as readable chat report with drift warnings flagged
