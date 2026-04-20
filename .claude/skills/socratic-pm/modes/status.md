---
name: status
description: Run telemetry and show environment drift
---

# Mode: status

Display current environment state and flag deviations from expected (docs/updates.md).

## Process

1. Run `scripts/telemetry.py` to gather: git branch, uncommitted changes, Python version, Node version, installed packages
2. Parse JSON output
3. Compare against expected state in `docs/updates.md`
4. Output readable report to chat with drift warnings:
   - ⚠️ Python 3.11.x but docs/updates.md expects 3.12.x
   - ⚠️ Branch: phase-2/feature but uncommitted changes: 3 files
   - ✅ langgraph 0.2.0 matches expected

## Example Output

```
Environment Status Report (2026-04-20 14:32:00)

✅ Git
  Branch: main
  Uncommitted changes: 0 files

✅ Python
  Version: 3.12.5 (expected: 3.12.x)

✅ Node
  Version: v20.11.0 (expected: v20.x.x)

✅ Packages
  langgraph 0.2.0 (expected: 0.2.0+)
  langchain 0.1.14 (expected: 0.1.x+)
  fastapi 0.104.1 (expected: 0.104.x+)
  pydantic 2.5.0 (expected: 2.x+)

No drift detected. Environment ready.
```

## Drift Example

```
⚠️ Git
  Branch: phase-2/feature (unexpected — typically work on main/task branches)
  Uncommitted changes: 5 files (⚠️ commit before /socratic-pm issue)

✅ Python
  Version: 3.12.5 (expected: 3.12.x)

❌ Node
  Version: v18.18.0 (expected: v20.x.x — upgrade recommended)

✅ Packages
  (All match expected versions)

Recommended action: Commit changes, switch to main, upgrade Node.
```
