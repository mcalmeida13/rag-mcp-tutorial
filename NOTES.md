# Notes

- User is building `rag-mcp-tutorial` hands-on (in `rag/`) alongside this teaching track — lessons should reference and reinforce that code, not duplicate it.
- Workspace intentionally lives in the same git repo as the code (user's explicit choice on 2026-07-17), even though this mixes teaching-material files with tutorial-code files.
- `CLAUDE.md` in this repo defines commit/tag conventions for *tutorial code steps* (ingestion, retrieval, MCP server, docs). Those conventions are not about teaching-workspace files (lessons, mission, notes) — don't auto-tag lesson commits under that scheme.
- As of 2026-07-17: the ingestion step (chunking + embeddings, `rag/ingest.py`) is already built and verified (8 docs → 41 chunks → 384-dim embeddings). Lesson 1 reinforces that work conceptually rather than introducing brand-new material.
