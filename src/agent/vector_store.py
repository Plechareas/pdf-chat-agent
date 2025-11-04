import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# ✅ Always use a writable path (important for Streamlit Cloud)
chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="/tmp/chroma"  # Streamlit Cloud’s writable folder
    )
)

collection = chroma_client.get_or_create_collection("pdf_chunks")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(chunks):
    return [embedder.encode(chunk).tolist() for chunk in chunks]

def index_pdf_text(text):
    # Split text into chunks
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
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
