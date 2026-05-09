from pathlib import Path
from fastapi import APIRouter, HTTPException
from ingest import IngestionPipeline

router = APIRouter(prefix="/ingest", tags=["ingest"])

NEO4J_URI = "bolt://localhost:7687"
PROJECT_ROOT = Path(__file__).parent.parent.parent


@router.post("")
def trigger_ingest():
    pipeline = IngestionPipeline(
        project_root=PROJECT_ROOT,
        neo4j_uri=NEO4J_URI,
    )
    try:
        stats = pipeline.run()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return stats
