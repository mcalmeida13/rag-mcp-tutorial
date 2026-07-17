# Mission: RAG & MCP

## Why
Build real, production-grade RAG pipelines and MCP tool integrations for use at work — moving from "I've read about RAG" to "I can design, build, and debug one, and expose it as an MCP-compatible tool."

## Success looks like
- Explain, from memory, how embeddings + chunking + a vector index turn documents into a searchable knowledge base
- Implement a cosine-similarity retrieval step and connect it to an LLM for generation
- Build an MCP server that exposes a working tool (e.g. `search_documents`) to an MCP client
- Debug a retrieval-quality problem (e.g. why a query returns the wrong chunk) by reasoning about chunking/embedding choices
- Explain MCP's client-server model well enough to design a new tool integration at work

## Constraints
- Learning happens alongside the hands-on `rag-mcp-tutorial` coding project in this same repo — lessons should reinforce and deepen what's being built in `rag/`, not duplicate it
- Sessions are self-paced and asynchronous — no fixed schedule assumed

## Out of scope
- Fine-tuning or training custom embedding models
- Production vector-database infrastructure at scale (sharding, replication, managed services)
- Advanced/agentic RAG architectures (graph-RAG, re-ranking, hybrid search) — revisit once the fundamentals are solid
