// Socratic-PM GraphRAG Schema
// Neo4j Cypher schema definition for Package-Language-Docs-API graph

// ============================================================================
// NODE CONSTRAINTS & INDEXES
// ============================================================================

// Package node constraints
CREATE CONSTRAINT package_name_language_unique
  FOR (p:Package) REQUIRE (p.name, p.language) IS UNIQUE;

CREATE INDEX package_lookup
  FOR (p:Package) ON (p.name);

CREATE INDEX package_language
  FOR (p:Package) ON (p.language);

// Documentation node constraints
CREATE CONSTRAINT documentation_name_unique
  FOR (d:Documentation) REQUIRE d.name IS UNIQUE;

CREATE INDEX documentation_lookup
  FOR (d:Documentation) ON (d.name);

// API_Reference node constraints
CREATE CONSTRAINT api_reference_name_unique
  FOR (a:API_Reference) REQUIRE a.name IS UNIQUE;

CREATE INDEX api_reference_lookup
  FOR (a:API_Reference) ON (a.name);

// ============================================================================
// NODE PROPERTY SCHEMAS
// ============================================================================

// Package: Represents a package in a specific language with version tracking
// Properties:
//   name (String): Package name (e.g., "langgraph", "fastapi")
//   language (String): Language/runtime (python, typescript, javascript, go, etc.)
//   version (String): Current version in environment (e.g., "0.2.0")
//   deprecated (Boolean): Flag indicating if package removed from requirements
//   last_update (Integer): Unix timestamp of last ingest/resync

// Documentation: Language-specific documentation for a package
// Properties:
//   name (String): Unique identifier (e.g., "langgraph-python-docs")
//   data (String): Full documentation text/content

// API_Reference: API reference/signatures for a package
// Properties:
//   name (String): Unique identifier (e.g., "langgraph-python-api")
//   data (String): Full API reference text/signatures

// ============================================================================
// RELATIONSHIPS
// ============================================================================

// DOCUMENTS_PACKAGE: Documentation points to the Package it documents
// Direction: Documentation -> Package
// Semantics: "This documentation belongs to this package"

// DEFINES_API_FOR: API_Reference points to the Package it defines APIs for
// Direction: API_Reference -> Package
// Semantics: "These APIs belong to this package"

// ============================================================================
// QUERY PATTERNS (for reference)
// ============================================================================

// Find all docs and APIs for a package in a specific language:
// MATCH (p:Package {name: 'langgraph', language: 'python'})
// OPTIONAL MATCH (d:Documentation)-[:DOCUMENTS_PACKAGE]->(p)
// OPTIONAL MATCH (a:API_Reference)-[:DEFINES_API_FOR]->(p)
// RETURN p, d, a

// Find active (non-deprecated) packages:
// MATCH (p:Package {deprecated: false})
// RETURN p

// Check for version drift:
// MATCH (p:Package {deprecated: false})
// WHERE p.last_update < timestamp() - 604800000  // 7 days
// RETURN p.name, p.version, p.last_update
