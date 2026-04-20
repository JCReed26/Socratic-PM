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
