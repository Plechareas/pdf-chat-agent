import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# -----------------------------------------------------------------------------
# Global singletons
# -----------------------------------------------------------------------------
_chroma_client = None
_collection = None
_embedder = None


def get_chroma_client():
    """Return a single shared Chroma client instance."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="/tmp/chroma"  # Safe writable path for Streamlit Cloud
            )
        )
    return _chroma_client


def get_collection():
    """Return or create the shared Chroma collection."""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection("pdf_chunks")
    return _collection


def get_embedder():
    """Return the shared sentence transformer."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


# -----------------------------------------------------------------------------
#  Vector-store helpers
# -----------------------------------------------------------------------------
def embed_texts(chunks):
    embedder = get_embedder()
    return [embedder.encode(chunk).tolist() for chunk in chunks]


def index_pdf_text(text):
    collection = get_collection()
    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    embeddings = embed_texts(chunks)
    for i, emb in enumerate(embeddings):
        collection.add(
            ids=[str(i)],
            embeddings=[emb],
            documents=[chunks[i]]
        )


def search_similar(query, n_results=3):
    collection = get_collection()
    embedder = get_embedder()
    query_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=n_results)
    return results.get("documents", [[]])[0]
