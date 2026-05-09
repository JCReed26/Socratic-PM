from fastapi import APIRouter, HTTPException
from neo4j import GraphDatabase

router = APIRouter(prefix="/graph", tags=["graph"])

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "password")


@router.get("")
def get_graph():
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 200"
            )
            nodes: dict = {}
            edges: list = []
            for record in result:
                for node in [record["n"], record["m"]]:
                    if node is not None:
                        nid = node.element_id
                        if nid not in nodes:
                            nodes[nid] = {
                                "id": nid,
                                "labels": list(node.labels),
                                "properties": dict(node),
                            }
                if record["r"] is not None:
                    rel = record["r"]
                    edges.append(
                        {
                            "id": rel.element_id,
                            "type": rel.type,
                            "source": rel.start_node.element_id,
                            "target": rel.end_node.element_id,
                        }
                    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.close()

    return {"nodes": list(nodes.values()), "edges": edges}
