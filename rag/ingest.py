"""
Ingestion / indexing step of the RAG (Retrieval-Augmented Generation) tutorial.

This script builds the "index" half of RAG: it reads the sample documents in
docs/, splits each one into smaller overlapping chunks, turns every chunk
into a numeric vector (an embedding) using a small local sentence-transformer
model, and saves the chunks plus their embeddings to disk as a simple local
vector index (rag/index/chunks.json + rag/index/embeddings.npy).

It deliberately does NOT implement retrieval (searching the index for a
query) or generation (asking an LLM to answer using retrieved chunks) - those
are the subject of a later step in the tutorial. Ingestion only prepares the
data so that a future retrieval step has something to search over.
"""

import argparse
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

DOCS_DIR = Path("docs")
INDEX_OUTPUT_DIR = Path("rag/index")

# Chunking is measured in words, not characters, so a chunk never gets cut
# off in the middle of a word - that keeps the chunks readable when a
# student opens chunks.json to inspect them.
CHUNK_SIZE_WORDS = 50
CHUNK_OVERLAP_WORDS = 10

# A small, fast, well-known sentence-transformer model. It maps any piece of
# text to a 384-dimensional vector such that semantically similar text ends
# up with similar vectors - that's what makes similarity search possible.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents(docs_dir):
    """Read every .md/.txt file in docs_dir into a list of document dicts."""
    documents = []
    for file_path in sorted(docs_dir.glob("*")):
        if file_path.suffix not in (".md", ".txt"):
            continue
        documents.append(
            {
                "source_filename": file_path.name,
                "text": file_path.read_text(encoding="utf-8"),
            }
        )
    return documents


def chunk_text(text, chunk_size_words=CHUNK_SIZE_WORDS, overlap_words=CHUNK_OVERLAP_WORDS):
    """Split text into overlapping windows of chunk_size_words words each.

    Chunking exists because of two limits working together: embedding
    models and LLMs can only take in so much text at once (a context window
    limit), and - just as importantly for retrieval quality - a vector for
    an entire document blurs many different facts into one point in space,
    making it a poor match for any single specific query. Small, focused
    chunks embed to more specific vectors, which is why retrieval over
    chunks works better than retrieval over whole documents.
    """
    words = text.split()
    if not words:
        return []

    # The overlap is what keeps a sentence that happens to fall on a chunk
    # boundary intact in at least one chunk, instead of being split in half
    # and losing meaning in both pieces.
    step = chunk_size_words - overlap_words

    chunks = []
    for start in range(0, len(words), step):
        window = words[start : start + chunk_size_words]
        if not window:
            break
        chunks.append(" ".join(window))
        if start + chunk_size_words >= len(words):
            break
    return chunks


def build_chunk_records(documents):
    """Chunk every document and flatten the results into one list of records."""
    chunk_records = []
    for document in documents:
        document_chunks = chunk_text(document["text"])
        for chunk_index, chunk_text_value in enumerate(document_chunks):
            chunk_records.append(
                {
                    "chunk_id": f"{document['source_filename']}::{chunk_index}",
                    "source_filename": document["source_filename"],
                    "chunk_index": chunk_index,
                    "chunk_text": chunk_text_value,
                }
            )
    return chunk_records


def generate_chunk_embeddings(chunk_records, model):
    """Embed every chunk's text with the sentence-transformer model.

    Embeddings are computed explicitly here, as a single batch call, rather
    than hidden behind some other library's "just index this text" helper -
    the point of this tutorial step is to see exactly where the vectors in
    the vector index come from.
    """
    chunk_texts = [record["chunk_text"] for record in chunk_records]
    chunk_embeddings = model.encode(chunk_texts, show_progress_bar=False)
    return np.asarray(chunk_embeddings)


def save_index(chunk_records, chunk_embeddings, output_dir):
    """Write the chunk metadata/text and embeddings to disk.

    chunks.json and embeddings.npy are two parallel files: row i of
    embeddings.npy is the embedding for chunk_records[i]. Keeping them as
    plain JSON + a plain numpy array (instead of a database or a specialized
    vector-store library) means a student can open chunks.json in any text
    editor and see exactly what's being searched later, with no black box.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    chunks_path = output_dir / "chunks.json"
    chunks_path.write_text(json.dumps(chunk_records, indent=2), encoding="utf-8")

    embeddings_path = output_dir / "embeddings.npy"
    np.save(embeddings_path, chunk_embeddings)

    return chunks_path, embeddings_path


def print_ingestion_summary(documents, chunk_records, chunk_embeddings):
    """Print a short human-readable summary so a run's success is obvious at a glance."""
    embedding_dimension = chunk_embeddings.shape[1] if len(chunk_embeddings) else 0
    print("Ingestion complete.")
    print(f"  Documents processed: {len(documents)}")
    print(f"  Chunks created:      {len(chunk_records)}")
    print(f"  Embedding dimension: {embedding_dimension}")


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into a local vector index.")
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DOCS_DIR,
        help="Directory containing the .md/.txt documents to ingest (default: docs/).",
    )
    args = parser.parse_args()

    documents = load_documents(args.docs_dir)
    chunk_records = build_chunk_records(documents)

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    chunk_embeddings = generate_chunk_embeddings(chunk_records, model)

    chunks_path, embeddings_path = save_index(chunk_records, chunk_embeddings, INDEX_OUTPUT_DIR)
    print_ingestion_summary(documents, chunk_records, chunk_embeddings)
    print(f"  Index written to:    {chunks_path} and {embeddings_path}")


if __name__ == "__main__":
    main()
