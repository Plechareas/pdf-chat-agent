from .vector_store import search_similar
from .llm_client import answer_question

def chat_with_pdf(query: str) -> str:
    docs = search_similar(query)
    context = "\n\n".join(docs)
    return answer_question(context,query)