# RAG & MCP Resources

## Knowledge

- [Paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — Lewis et al., NeurIPS 2020](https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf)
  The original RAG paper. Use for: the foundational definition of RAG as parametric + non-parametric memory, and why retrieval reduces hallucination.
- [Wikipedia: Retrieval-augmented generation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
  Neutral, regularly updated overview. Use for: a fast, jargon-light refresher on RAG's moving parts before tackling the original paper.
- [Anthropic Engineering: "Contextual Retrieval"](https://www.anthropic.com/engineering/contextual-retrieval)
  Explains why naive chunking loses context and how contextual embeddings/BM25 fix it (up to 67% fewer retrieval failures in their tests). Use for: deepening the chunking lesson once the basics are solid.
- [Sentence Transformers: Quickstart docs](https://www.sbert.net/docs/quickstart.html)
  Official docs for the embedding library used in `rag/ingest.py`. Use for: the API surface (`model.encode`, batching, similarity helpers).
- [Hugging Face: all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
  The exact embedding model used in this project. Use for: embedding dimension (384), training method (contrastive loss over 1B+ sentence pairs), speed/quality tradeoffs vs. larger models.
- [modelcontextprotocol.io: "What is the Model Context Protocol?"](https://modelcontextprotocol.io/docs/getting-started/intro)
  Official MCP documentation. Use for: the client-server architecture and the "USB-C for AI apps" framing of why MCP standardizes tool/data access.
- [Anthropic: "Introducing the Model Context Protocol"](https://www.anthropic.com/news/model-context-protocol)
  Original announcement. Use for: motivating why MCP exists (fragmented, one-off integrations) before the getting-started lesson.

## Wisdom (Communities)

- [MCP Discord](https://discord.com/invite/model-context-protocol-1312302100125843476)
  ~13k members; the official community for MCP builders. Use for: real-time help building/debugging MCP servers and seeing what others are integrating.
- r/MachineLearning
  High-signal, well-moderated general ML subreddit. Use for: broader RAG/embedding discussion once you have concrete implementation questions to bring.

## Gaps

- No verified high-trust community specifically for RAG (as opposed to MCP) has been found yet. Revisit once the retrieval/generation step is built and there are concrete implementation questions to bring to a community.
