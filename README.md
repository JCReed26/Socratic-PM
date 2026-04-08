# Socratic-PM

This terminal based Orchestration Tool sits between the human engineer and their fleet of AI Agents (Claude, Cursor, Jules, Warp) to manage the "Meta-Work": package depencies, tool configurations, and project level logic planning. 

## Status & Checklist

- [ ] **Phase 1: TUI Chat Bot**
  - [ ] DeepAgent integration for stateful loops.
  - [ ] Basic TUI for env status
     
- [ ] **Phase 2: Data Pipelines**
  - [ ] Pipeline to get packages from package managers in global or env
  - [ ] Pipeline to get configs from coding tools in global or env
  - [ ] TUI pages to manage configs
        
- [ ] **Phase 3: GraphRAG**
  - [ ] Neo4j GraphRAG setup to distinguish libraries vs coding tools
  - [ ] Neo4j GraphRAG two databases, temp for env repos, global for global
  - [ ] Open up tool in a repo and view graph for that repo in temp and also view global 
  - [ ] Agent ability to utilize GraphRAG and set skills for code assist and dependency management
  - [ ] temp store update workflow
        
- [ ] **Phase 4: Orchestrator**
  - [ ] Github connection and TUI settings page
  - [ ] Systematic Github orchestration protocols for Human Agent collaboration
  - [ ] Agent can create an issues, assign issues, review prs, and manage branches. Local and Remote.
        
- [ ] **Phase 5: Thought Provoking Project Manager**
  - [ ] Skills to ask engineers proper questions and follow structured guide to solving problems
  - [ ] Skills to utilize the graphRAG to get docs and api code to give to the engineer

## Tech Stack

**Framework:** Langchain deepagents
**GraphRAG:** Neo4j
**Interface:** Textual
