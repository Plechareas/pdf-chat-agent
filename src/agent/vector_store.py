import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# -----------------------------------------------------------------------------
#  Make ChromaDB safe for Streamlit Cloud (only one instance at a time)
# -----------------------------------------------------------------------------
def get_chroma_client():
    """Return a single shared Chroma client."""
    try:
        # Reuse the existing shared instance if it exists
        return chromadb.Client()
    except Exception:
        # If the above fails because of settings mismatch, clear & recreate
        return chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="/tmp/chroma"  # Writable path on Streamlit Cloud
            )
        )

chroma_client = get_chroma_client()
collection = chroma_client.get_or_create_collection("pdf_chunks")

# load the embedder once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------------------------------------------------
#  Vector-store helpers
# -----------------------------------------------------------------------------
def embed_texts(chunks):
    return [embedder.encode(chunk).tolist() for chunk in chunks]

def index_pdf_text(text):
    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    embeddings = embed_texts(chunks)
    for i, emb in enumerate(embeddings):
        collection.add(
            ids=[str(i)],
            embeddings=[emb],
            documents=[chunks[i]]
        )

def search_similar(query, n_results=3):
    query_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=n_results)
    return results.get("documents", [[]])[0]
