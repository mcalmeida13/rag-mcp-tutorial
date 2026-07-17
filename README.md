# RAG + MCP Tutorial

Educational project teaching RAG and MCP concepts hands-on.

## Step 1: Ingestion

This first step builds only the **ingestion / indexing** half of a RAG (Retrieval-Augmented Generation) pipeline: turning a folder of documents into a local, searchable vector index. Retrieval (searching that index for a query) and generation (asking an LLM to answer using the retrieved chunks) are **not** built yet - they come in a later step.

### Key Concepts

- **Embedding** - a numeric vector representation of a piece of text, produced by a machine learning model, such that pieces of text with similar meaning end up with similar vectors. This is what makes "search by meaning" possible, instead of just keyword matching.
- **Chunking** - splitting a document into smaller, overlapping pieces before embedding them. This matters for two reasons: embedding models and LLMs can only process a limited amount of text at once (a context window), and a vector for a whole document blurs many different facts together, which hurts search precision compared to small, focused chunks.
- **Vector index (vector store)** - the place where chunk embeddings are kept alongside their original text and metadata (like which file they came from), so they can later be searched by similarity. In this step, the "vector store" is intentionally just two plain files: a JSON file of chunk text/metadata and a numpy array of embeddings, with matching row order.

### Project structure

```
rag-mcp-tutorial/
├── docs/              # sample documents to index (animal facts)
├── rag/
│   └── ingest.py      # chunking + embeddings + indexing script
├── requirements.txt
└── README.md
```

### How to run

1. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the ingestion script:
   ```
   python rag/ingest.py
   ```
   The first run downloads the `all-MiniLM-L6-v2` embedding model (~80MB), so it needs an internet connection once; subsequent runs use the cached model.
4. Expected output - a short summary like:
   ```
   Ingestion complete.
     Documents processed: 8
     Chunks created:      37
     Embedding dimension: 384
     Index written to:    rag/index/chunks.json and rag/index/embeddings.npy
   ```
   The exact chunk count may vary slightly, but you should see 8 documents and an embedding dimension of 384. The index files land in `rag/index/`, which is gitignored since it's generated output, not source.

### Next steps

Retrieval (searching this index for a query using cosine similarity) and generation (using an LLM to answer questions from retrieved chunks) will be added in a follow-up step - not built here.
