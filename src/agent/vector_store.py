import chromadb
from sentence_transformers import SentenceTransformer
import streamlit as st

# -----------------------------------------------------------------------------
# Create and cache the resources lazily.
# Streamlit will reuse them safely across reruns.
# -----------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def get_chroma_client():
    # Do NOT pass Settings — just use defaults.
    return chromadb.Client()

@st.cache_resource(show_spinner=False)
def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection("pdf_chunks")

@st.cache_resource(show_spinner=False)
def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

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
            documents=[chunks[i]],
        )

def search_similar(query, n_results=3):
    collection = get_collection()
    embedder = get_embedder()
    query_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=n_results)
    return results.get("documents", [[]])[0]
