# Neo4j Local Setup Guide

**Goal:** Set up a local Neo4j instance in `.socratic-pm/graph.db` with random port + browser access.

**Your task tomorrow:** Follow these steps and report back what worked / what broke.

---

## Step 1: Install Neo4j (if needed)

### Option A: Docker (Recommended)
```bash
# Pull Neo4j image
docker pull neo4j:latest

# Create project-local graph directory
mkdir -p .socratic-pm/graph

# Start Neo4j container with random port mapping
docker run -d \
  --name socratic-pm-neo4j \
  -e NEO4J_AUTH=neo4j/password \
  -v $(pwd)/.socratic-pm/graph:/data \
  -p 7474:7474 \
  -p 7687:7687 \
  neo4j:latest

# Get the mapped port (should be 7474 or 7687)
docker port socratic-pm-neo4j 7474
docker port socratic-pm-neo4j 7687
```

### Option B: Local Install (macOS/Linux)
```bash
# macOS via Homebrew
brew install neo4j

# Or download from https://neo4j.com/download-center/

# Start Neo4j (creates local data directory)
neo4j start
```

---

## Step 2: Verify Neo4j is Running

```bash
# Test connection
curl http://localhost:7474

# Should return HTML page (Neo4j Browser)
# Open browser: http://localhost:7474/
```

---

## Step 3: Apply Schema

```bash
# Connect to Neo4j and run schema
# Using neo4j-contrib/mcp-neo4j MCP server (if available)
# OR use cypher-shell

cypher-shell -u neo4j -p password < scripts/schema.cypher
```

---

## Step 4: Test Ingestion

```bash
# Install dependencies
pip install neo4j

# Run ingest pipeline (dry-run first)
python scripts/ingest.py --dry-run --project-root .

# If successful, run for real
python scripts/ingest.py --neo4j-uri bolt://localhost:7687 --project-root .
```

---

## Step 5: View Graph in Browser

```bash
# Open Neo4j Browser
open http://localhost:7474/

# Login: neo4j / password

# Run test query:
MATCH (p:Package) RETURN p LIMIT 10
```

---

## Troubleshooting Checklist

- [ ] Neo4j container/process running?
- [ ] Port 7474 and 7687 accessible?
- [ ] Schema constraints created without error?
- [ ] Ingest script completes (check JSON output)?
- [ ] Browser query returns Package nodes?

**If blocked:** Comment in teaching.md what failed, I'll help tomorrow.

---

## Next: MCP Integration

Once Neo4j is running, we integrate `neo4j-contrib/mcp-neo4j` so Claude Code can run Cypher queries directly in `/socratic-pm context`.

For now: just get it running locally.
