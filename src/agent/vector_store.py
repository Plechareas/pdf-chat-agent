import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------------------------------------------------------
# Use the existing shared Chroma instance (no settings arguments!)
# -----------------------------------------------------------------------------
_chroma_client = chromadb.Client()
_collection = _chroma_client.get_or_create_collection("pdf_chunks")
_embedder = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------------------------------------------------------
# Vector store helpers
# -----------------------------------------------------------------------------
def embed_texts(chunks):
    return [_embedder.encode(chunk).tolist() for chunk in chunks]

def index_pdf_text(text):
    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    embeddings = embed_texts(chunks)
    for i, emb in enumerate(embeddings):
        _collection.add(
            ids=[str(i)],
            embeddings=[emb],
            documents=[chunks[i]],
        )

def search_similar(query, n_results=3):
    query_emb = _embedder.encode(query).tolist()
    results = _collection.query(query_embeddings=[query_emb], n_results=n_results)
    return results.get("documents", [[]])[0]
