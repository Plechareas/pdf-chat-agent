import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = chroma_client.create_collection("pdf_chunks")


def embed_texts(texts):
    """"Get embeddings using ollama"""
    return embedder.encode(texts).tolist()

def chunk_text(text:str, chunk_size=1000, overlap=200):
    """"Split long text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def index_pdf_text(pdf_text: str):
    chunks = chunk_text(pdf_text)
    embeddings = embed_texts(chunks)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    print(f"Indexed {len(chunks)} chunks locally.")


def search_similar(query:str, top_k=5):
    query_emb = embed_texts([query])[0]
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    return results["documents"][0]