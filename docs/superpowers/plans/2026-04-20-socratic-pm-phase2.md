# Socratic-PM Phase 2: Telemetry & Status Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement zero-LLM telemetry script and status mode to detect environment drift (version changes, unexpected git state).

**Architecture:** Two-layer approach: (1) `scripts/telemetry.py` gathers environment state deterministically (git, Python, Node, packages), (2) `modes/status.md` parses output, compares against `docs/updates.md` template, reports drift to chat. No LLM calls in telemetry.

**Tech Stack:** Python 3.12+ (subprocess, json, sys), Git CLI, standard library.

---

### Task 1: Create scripts package structure

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/telemetry.py` (stub)

- [ ] **Step 1: Create scripts directory and __init__.py**

```bash
mkdir -p /Users/jcreed/Documents/GitHub/Socratic-PM/scripts
touch /Users/jcreed/Documents/GitHub/Socratic-PM/scripts/__init__.py
```

- [ ] **Step 2: Verify directory exists**

```bash
ls -la /Users/jcreed/Documents/GitHub/Socratic-PM/scripts/
```

Expected: `__init__.py` present.

- [ ] **Step 3: Commit**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
git add scripts/__init__.py
git commit -m "feat(phase2): create scripts package"
```

---

### Task 2: Implement telemetry.py script

**Files:**
- Create: `scripts/telemetry.py`

- [ ] **Step 1: Write telemetry.py**

Create `/Users/jcreed/Documents/GitHub/Socratic-PM/scripts/telemetry.py`:

```python
#!/usr/bin/env python3
"""
Zero-LLM telemetry script. Gathers environment state deterministically.
Returns JSON with: git branch, uncommitted changes count, Python version, Node version, installed packages.
"""

import json
import subprocess
import sys
from pathlib import Path

def get_git_info():
    """Get current git branch and uncommitted changes count."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except subprocess.CalledProcessError:
        branch = None

    try:
        status_output = subprocess.check_output(
            ["git", "status", "--porcelain"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        uncommitted_changes = len([line for line in status_output.split("\n") if line])
    except subprocess.CalledProcessError:
        uncommitted_changes = None

    return {"branch": branch, "uncommitted_changes": uncommitted_changes}

def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

def get_node_version():
    """Get Node.js version."""
    try:
        version = subprocess.check_output(
            ["node", "--version"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return version  # Returns "v20.x.x" format
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_installed_packages():
    """Get list of top 10 most important packages (by import frequency)."""
    packages = []
    important_packages = [
        "pip", "setuptools", "wheel", "langgraph", "langchain",
        "fastapi", "pydantic", "sqlalchemy", "psycopg", "pytest"
    ]
    
    for pkg in important_packages:
        try:
            result = subprocess.check_output(
                [sys.executable, "-m", "pip", "show", pkg],
                stderr=subprocess.DEVNULL
            ).decode()
            for line in result.split("\n"):
                if line.startswith("Version:"):
                    version = line.split("Version: ")[1].strip()
                    packages.append({"name": pkg, "version": version})
                    break
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    return packages

def main():
    """Gather telemetry and output JSON."""
    telemetry = {
        "git": get_git_info(),
        "python_version": get_python_version(),
        "node_version": get_node_version(),
        "packages": get_installed_packages(),
    }
    print(json.dumps(telemetry, indent=2))

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make executable**

```bash
chmod +x /Users/jcreed/Documents/GitHub/Socratic-PM/scripts/telemetry.py
```

- [ ] **Step 3: Test telemetry.py runs and outputs valid JSON**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
python3 scripts/telemetry.py
```

Expected: JSON output with git, python_version, node_version, packages fields.

- [ ] **Step 4: Commit**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
git add scripts/telemetry.py
git commit -m "feat(phase2): implement telemetry.py script"
```

---

### Task 3: Create docs/updates.md template

**Files:**
- Create: `docs/updates.md`

- [ ] **Step 1: Write docs/updates.md template**

Create `/Users/jcreed/Documents/GitHub/Socratic-PM/docs/updates.md`:

```markdown
# Environment Updates Log

Track expected environment state here. Status mode compares actual state against these values and flags drift.

## Expected Environment

### Python
- Version: 3.12.x
- Last updated: 2026-04-20

### Node.js
- Version: v20.x.x (if used)
- Last updated: 2026-04-20

### Key Packages
- langgraph: 0.2.0+
- langchain: 0.1.x+
- fastapi: 0.104.x+
- pydantic: 2.x+

## Known Constraints
- No Python 3.11 or earlier (async features required)
- Node.js optional, only needed if frontend tooling active

## Drift Warnings
If status mode reports:
- Python version mismatch: Run `python3 --version`, upgrade if outdated
- Unexpected branch: Switch to main before running /socratic-pm
- Uncommitted changes: Commit or stash before proceeding
```

- [ ] **Step 2: Commit**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
git add docs/updates.md
git commit -m "feat(phase2): add docs/updates.md environment tracking template"
```

---

### Task 4: Implement status.md mode logic

**Files:**
- Modify: `modes/status.md`

- [ ] **Step 1: Replace status.md stub with implementation**

Replace `/Users/jcreed/Documents/GitHub/Socratic-PM/.claude/skills/socratic-pm/modes/status.md` with:

```markdown
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

\`\`\`
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
\`\`\`

## Drift Example

\`\`\`
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
\`\`\`
```

- [ ] **Step 2: Verify file updated**

```bash
cat /Users/jcreed/Documents/GitHub/Socratic-PM/.claude/skills/socratic-pm/modes/status.md
```

Expected: New implementation (not "Not yet implemented").

- [ ] **Step 3: Commit**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
git add .claude/skills/socratic-pm/modes/status.md
git commit -m "feat(phase2): implement status mode with telemetry integration"
```

---

### Task 5: Test status mode end-to-end

**Files:**
- Test: Manual invocation of `/socratic-pm status`

- [ ] **Step 1: Manually run telemetry.py to verify output**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
python3 scripts/telemetry.py | python3 -m json.tool
```

Expected: Valid JSON with git, python_version, node_version, packages.

- [ ] **Step 2: Test /socratic-pm status in new Claude session**

In Claude Code, run:
```
/socratic-pm status
```

Expected: Readable report showing environment state, drift warnings if applicable.

- [ ] **Step 3: Commit final state**

```bash
cd /Users/jcreed/Documents/GitHub/Socratic-PM
git status
```

Expected: Clean working tree.

---

## Success Criteria (Phase 2 Complete)

- [ ] `scripts/telemetry.py` exists, is executable, outputs valid JSON
- [ ] `docs/updates.md` documents expected environment state
- [ ] `modes/status.md` implemented with drift detection logic
- [ ] `/socratic-pm status` works and shows readable report
- [ ] All commits pushed to phase-2/telemetry-status branch
