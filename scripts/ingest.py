#!/usr/bin/env python3
"""
Socratic-PM GraphRAG Ingestion Pipeline

Deterministic script (zero-LLM) that:
1. Detects active languages from lockfiles (Python, JS/TS, Go, etc.)
2. Extracts packages from each language's package manager
3. Fetches API documentation for each package
4. Creates/updates nodes in Neo4j (.socratic-pm/graph.db)
5. Detects version changes and marks deprecated packages

Usage:
    python scripts/ingest.py [--dry-run] [--neo4j-uri bolt://localhost:7687]

Output:
    JSON with counts: {packages_created, packages_updated, packages_deprecated, docs_fetched, apis_fetched}
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# Try to import neo4j; fail gracefully with instructions
try:
    from neo4j import GraphDatabase
except ImportError:
    print("ERROR: neo4j-python-driver not installed")
    print("Install with: pip install neo4j")
    sys.exit(1)


class IngestionPipeline:
    """Handles language detection, package extraction, doc fetching, and Neo4j writes."""

    def __init__(self, project_root: Path, neo4j_uri: str, dry_run: bool = False):
        self.project_root = project_root
        self.neo4j_uri = neo4j_uri
        self.dry_run = dry_run
        self.driver = None
        self.stats = {
            "packages_created": 0,
            "packages_updated": 0,
            "packages_deprecated": 0,
            "docs_fetched": 0,
            "apis_fetched": 0,
            "errors": [],
        }

    def connect(self):
        """Initialize Neo4j connection."""
        if not self.dry_run:
            try:
                self.driver = GraphDatabase.driver(
                    self.neo4j_uri, auth=("neo4j", "password")
                )
                self.driver.verify_connectivity()
            except Exception as e:
                self.stats["errors"].append(f"Neo4j connection failed: {e}")
                raise

    def close(self):
        """Close Neo4j connection."""
        if self.driver and not self.dry_run:
            self.driver.close()

    def detect_languages(self) -> dict[str, list[str]]:
        """
        Scan lockfiles to detect active languages and packages.

        Returns:
            {language: [package_names], ...}
            e.g., {"python": ["langgraph", "fastapi"], "typescript": ["express"]}
        """
        detected = {}

        # Python: requirements.txt, pyproject.toml, poetry.lock
        python_packages = self._extract_python_packages()
        if python_packages:
            detected["python"] = python_packages

        # JavaScript/TypeScript: package.json, package-lock.json, yarn.lock
        js_packages = self._extract_js_packages()
        if js_packages:
            detected["typescript"] = js_packages  # Treat JS/TS as single language

        # Go: go.mod
        go_packages = self._extract_go_packages()
        if go_packages:
            detected["go"] = go_packages

        return detected

    def _extract_python_packages(self) -> list[str]:
        """Extract packages from Python lockfiles."""
        packages = []

        # Try requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        pkg_name = re.split(r"[=<>!]", line)[0].strip()
                        if pkg_name:
                            packages.append(pkg_name)

        # Try pyproject.toml
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            with open(pyproject) as f:
                in_deps = False
                for line in f:
                    if "[project]" in line or "[tool.poetry.dependencies]" in line:
                        in_deps = True
                    elif in_deps and line.strip().startswith("["):
                        in_deps = False
                    elif in_deps and "=" in line:
                        pkg_name = line.split("=")[0].strip().strip("\"'")
                        if pkg_name and pkg_name != "python":
                            packages.append(pkg_name)

        return list(set(packages))  # Deduplicate

    def _extract_js_packages(self) -> list[str]:
        """Extract packages from JavaScript lockfiles."""
        packages = []

        pkg_json = self.project_root / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json) as f:
                    data = json.load(f)
                    deps = data.get("dependencies", {})
                    dev_deps = data.get("devDependencies", {})
                    packages = list(deps.keys()) + list(dev_deps.keys())
            except json.JSONDecodeError:
                self.stats["errors"].append("Failed to parse package.json")

        return list(set(packages))

    def _extract_go_packages(self) -> list[str]:
        """Extract packages from Go mod file."""
        packages = []

        go_mod = self.project_root / "go.mod"
        if go_mod.exists():
            with open(go_mod) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("require"):
                        continue
                    if " " in line and not line.startswith("//"):
                        pkg_name = line.split()[0]
                        if pkg_name:
                            packages.append(pkg_name)

        return list(set(packages))

    def fetch_package_info(self, package_name: str, language: str) -> dict[str, Any]:
        """
        Fetch version and basic info for a package.

        Returns:
            {version: "x.y.z", found: bool, ...}
        """
        version = None

        if language == "python":
            try:
                result = subprocess.run(
                    ["pip", "show", package_name],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    for line in result.stdout.split("\n"):
                        if line.startswith("Version:"):
                            version = line.split(":", 1)[1].strip()
                            break
            except Exception as e:
                self.stats["errors"].append(
                    f"Failed to fetch {package_name} version: {e}"
                )

        elif language == "typescript":
            pkg_json = self.project_root / "package.json"
            if pkg_json.exists():
                try:
                    with open(pkg_json) as f:
                        data = json.load(f)
                        deps = {
                            **data.get("dependencies", {}),
                            **data.get("devDependencies", {}),
                        }
                        if package_name in deps:
                            version = deps[package_name].lstrip("^~")
                except json.JSONDecodeError:
                    pass

        return {"version": version, "found": version is not None}

    def fetch_documentation(self, package_name: str, language: str) -> str:
        """
        Stub: Fetch documentation for a package.

        In production, this would:
        - Call Context7 MCP for official docs
        - Parse docstrings from installed package
        - Fetch from PyPI / npm registry

        For now, returns a placeholder.
        """
        self.stats["docs_fetched"] += 1
        return f"[Documentation for {package_name}-{language}]\nTo be fetched from Context7 or package docstrings."

    def fetch_api_reference(self, package_name: str, language: str) -> str:
        """
        Stub: Fetch API reference for a package.

        In production, this would:
        - Parse docstrings from installed package
        - Call Context7 MCP for API reference
        - Extract from __init__.py or similar

        For now, returns a placeholder.
        """
        self.stats["apis_fetched"] += 1
        return f"[API Reference for {package_name}-{language}]\nTo be fetched from package exports or Context7."

    def upsert_package_node(
        self, package_name: str, language: str, version: str
    ) -> str:
        """
        Create or update a Package node in Neo4j.

        Returns: "created", "updated", or "error"
        """
        if self.dry_run:
            return "created (dry-run)"

        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MERGE (p:Package {name: $name, language: $language})
                    ON CREATE SET p.version = $version,
                                  p.deprecated = false,
                                  p.last_update = timestamp()
                    ON MATCH SET p.version = $version,
                                 p.last_update = timestamp(),
                                 p.deprecated = false
                    RETURN p.version AS prev_version
                    """,
                    name=package_name,
                    language=language,
                    version=version or "unknown",
                )
                prev = result.single()
                if prev and prev["prev_version"] != (version or "unknown"):
                    self.stats["packages_updated"] += 1
                    return "updated"
                else:
                    self.stats["packages_created"] += 1
                    return "created"
        except Exception as e:
            self.stats["errors"].append(f"Failed to upsert package {package_name}: {e}")
            return "error"

    def upsert_documentation_node(
        self, package_name: str, language: str, doc_content: str
    ) -> bool:
        """Create or update a Documentation node and link to Package."""
        if self.dry_run:
            return True

        try:
            with self.driver.session() as session:
                doc_name = f"{package_name}-{language}-docs"
                session.run(
                    """
                    MERGE (d:Documentation {name: $name})
                    ON CREATE SET d.data = $data
                    ON MATCH SET d.data = $data
                    WITH d
                    MATCH (p:Package {name: $package_name, language: $language})
                    MERGE (d)-[:DOCUMENTS_PACKAGE]->(p)
                    """,
                    name=doc_name,
                    data=doc_content,
                    package_name=package_name,
                    language=language,
                )
                return True
        except Exception as e:
            self.stats["errors"].append(f"Failed to create documentation node: {e}")
            return False

    def upsert_api_reference_node(
        self, package_name: str, language: str, api_content: str
    ) -> bool:
        """Create or update an API_Reference node and link to Package."""
        if self.dry_run:
            return True

        try:
            with self.driver.session() as session:
                api_name = f"{package_name}-{language}-api"
                session.run(
                    """
                    MERGE (a:API_Reference {name: $name})
                    ON CREATE SET a.data = $data
                    ON MATCH SET a.data = $data
                    WITH a
                    MATCH (p:Package {name: $package_name, language: $language})
                    MERGE (a)-[:DEFINES_API_FOR]->(p)
                    """,
                    name=api_name,
                    data=api_content,
                    package_name=package_name,
                    language=language,
                )
                return True
        except Exception as e:
            self.stats["errors"].append(f"Failed to create API reference node: {e}")
            return False

    def mark_removed_packages_deprecated(self, detected_packages: dict[str, list[str]]):
        """Mark packages no longer in lockfiles as deprecated."""
        if self.dry_run:
            return

        try:
            with self.driver.session() as session:
                # Get all active packages from graph
                all_packages = session.run(
                    "MATCH (p:Package {deprecated: false}) RETURN p.name AS name, p.language AS language"
                )

                for record in all_packages:
                    pkg_name = record["name"]
                    lang = record["language"]

                    # Check if still in detected packages
                    if (
                        lang not in detected_packages
                        or pkg_name not in detected_packages[lang]
                    ):
                        session.run(
                            "MATCH (p:Package {name: $name, language: $language}) SET p.deprecated = true",
                            name=pkg_name,
                            language=lang,
                        )
                        self.stats["packages_deprecated"] += 1
        except Exception as e:
            self.stats["errors"].append(f"Failed to mark deprecated packages: {e}")

    def run(self):
        """Execute full ingestion pipeline."""
        print("[1/5] Detecting languages and packages...")
        detected = self.detect_languages()
        print(f"  Found: {detected}")

        if not detected:
            print("  No packages detected. Exiting.")
            return self.stats

        print("[2/5] Connecting to Neo4j...")
        self.connect()

        print("[3/5] Upserting package nodes...")
        for language, packages in detected.items():
            for pkg_name in packages:
                info = self.fetch_package_info(pkg_name, language)
                self.upsert_package_node(pkg_name, language, info.get("version"))

        print("[4/5] Creating documentation and API nodes...")
        for language, packages in detected.items():
            for pkg_name in packages:
                doc_content = self.fetch_documentation(pkg_name, language)
                api_content = self.fetch_api_reference(pkg_name, language)
                self.upsert_documentation_node(pkg_name, language, doc_content)
                self.upsert_api_reference_node(pkg_name, language, api_content)

        print("[5/5] Marking removed packages as deprecated...")
        self.mark_removed_packages_deprecated(detected)

        print("\nIngestion complete.")
        self.close()
        return self.stats


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Socratic-PM GraphRAG ingestion pipeline"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print plan without writing to Neo4j"
    )
    parser.add_argument(
        "--neo4j-uri",
        default="bolt://localhost:7687",
        help="Neo4j connection URI",
    )
    parser.add_argument("--project-root", default=".", help="Project root directory")

    args = parser.parse_args()

    pipeline = IngestionPipeline(
        project_root=Path(args.project_root),
        neo4j_uri=args.neo4j_uri,
        dry_run=args.dry_run,
    )

    stats = pipeline.run()
    print(json.dumps(stats, indent=2))
    return 0 if not stats["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
