import streamlit as st
import random
from agent.pdf_loader import extract_text_from_pdf
from agent.vector_store import index_pdf_text, search_similar
from agent.llm_client import answer_question

st.set_page_config(page_title="📄 Chat with your PDF", layout="centered")

st.title("📄 Chat with your PDF")
st.caption("Powered by Groq Llama 3.1 — chat with your document instantly")

# --- Initialize state ---
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
if "used_questions" not in st.session_state:
    st.session_state.used_questions = []
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None

# --- All possible suggestions ---
ALL_SUGGESTIONS = [
    "Can you summarize this document?",
    "What are the main topics discussed?",
    "List the key insights or conclusions.",
    "Who is the author and what’s their main argument?",
    "What are the pros and cons mentioned?",
    "Give me a short executive summary.",
    "What evidence or data does the author provide?",
    "What’s the overall purpose of this document?",
]

# --- File upload ---
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# --- Handle PDF changes (new upload or removal) ---
if uploaded_file is not None:
    # If new file or replaced file
    if uploaded_file.name != st.session_state.last_uploaded_filename:
        st.session_state.chat_history = []
        st.session_state.used_questions = []
        st.session_state.pdf_text = None
        st.session_state.last_uploaded_filename = uploaded_file.name
        with st.spinner("📄 Extracting and indexing text..."):
            text = extract_text_from_pdf(uploaded_file)
            st.session_state.pdf_text = text
            index_pdf_text(text)
        st.success(f"✅ '{uploaded_file.name}' indexed successfully! Start asking below 👇")
else:
    # File removed
    if st.session_state.pdf_text is not None:
        st.session_state.chat_history = []
        st.session_state.used_questions = []
        st.session_state.pdf_text = None
        st.session_state.last_uploaded_filename = None
        st.info("📁 No PDF loaded. Please upload a document to begin.")

# --- If a PDF is loaded ---
if st.session_state.pdf_text:
    st.divider()
    st.markdown("### 💬 Chat with your document")

    # --- Display chat history ---
    for q, a in st.session_state.chat_history:
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 Agent:** {a}")
        st.markdown("---")

    # --- Dynamic suggested questions ---
    st.markdown("#### 🧠 Suggested Questions:")
    available = [q for q in ALL_SUGGESTIONS if q not in st.session_state.used_questions]
    if available:
        suggestions = random.sample(available, min(3, len(available)))
    else:
        suggestions = ["No more suggestions — try your own question!"]

    cols = st.columns(len(suggestions))
    for i, col in enumerate(cols):
        with col:
            if st.button(f"💡 {suggestions[i]}"):
                if "No more suggestions" not in suggestions[i]:
                    st.session_state.pending_question = suggestions[i]
                    st.session_state.used_questions.append(suggestions[i])
                    st.session_state.user_question = suggestions[i]
                    st.session_state.auto_ask = True
                    st.rerun()

    # --- Handle chat input or clicked suggestion ---
    user_question = None
    if st.session_state.get("auto_ask"):
        user_question = st.session_state.get("user_question")
        st.session_state.auto_ask = False
    else:
        user_question = st.chat_input("Ask something about the document...")

    if user_question:
        with st.spinner("🤖 Thinking..."):
            context = search_similar(user_question)
            answer = answer_question(context, user_question)
        st.session_state.chat_history.append((user_question, answer))
        st.rerun()

else:
    st.info("⬆️ Upload a PDF to start chatting.")
