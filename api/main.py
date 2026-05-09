import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent / ".claude" / "skills" / "socratic-pm" / "scripts"
    ),
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import ingest, graph

app = FastAPI(title="Socratic-PM GraphRAG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(graph.router)


@app.get("/health")
def health():
    return {"status": "ok"}
