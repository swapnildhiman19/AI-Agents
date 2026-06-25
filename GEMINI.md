# Unified Agent Routing Protocol

## Context Minimization Mandate
- The model's available context space is strictly managed. Never execute uncompressed bash commands or raw filesystem reads (such as `cat`, `grep`, or `find`) when structured MCP tools are active.
- Prioritize structural intelligence over raw code reading to avoid context degradation.

## Query Routing Guidelines
1. **Spatial Exploration (Structure, Calls, Architecture):**
   - Use `codebase-memory` tools exclusively (`search_graph`, `trace_call_path`, `get_architecture`) at the beginning of any exploration task to isolate target coordinates.
2. **Temporal File Interactions (Reading & Content Extraction):**
   - When files must be examined, call `lean-ctx` tools (`ctx-read`) instead of standard file-reading operations.
   - Accept progressive representations (AST signatures or map structures) unless specific implementation details are mathematically necessary.
3. **Shell Interactions:**
   - Execute terminal inspections exclusively through `ctx-shell` to leverage compression patterns.

## Interaction Formatting
- Respond strictly using Token Dense Dialect (TDD) notations when resolving code symbols (e.g., use λ for functions and § for modules) to limit output token generation.
