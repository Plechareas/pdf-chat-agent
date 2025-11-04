from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -----------------------------------------------------------------------------
# Simple FAISS-based in-memory vector store (no Chroma needed)
# -----------------------------------------------------------------------------
_embedder = SentenceTransformer("all-MiniLM-L6-v2")

_index = None
_chunks = []


def embed_texts(chunks):
    return np.array([_embedder.encode(chunk) for chunk in chunks]).astype("float32")


def index_pdf_text(text):
    global _index, _chunks
    _chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
    vectors = embed_texts(_chunks)
    _index = faiss.IndexFlatL2(vectors.shape[1])
    _index.add(vectors)


def search_similar(query, n_results=3):
    if _index is None or not _chunks:
        return ["⚠️ No PDF indexed yet."]
    q_vec = np.array([_embedder.encode(query)]).astype("float32")
    distances, indices = _index.search(q_vec, n_results)
    return [_chunks[i] for i in indices[0]]
