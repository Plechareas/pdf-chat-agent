import streamlit as st
import random
from agent.pdf_loader import extract_text_from_pdf
from agent.vector_store import index_pdf_text, search_similar
from agent.llm_client import answer_question

st.set_page_config(page_title="📄 Chat with your PDF", layout="centered")

st.title("📄 Chat with your PDF")
st.caption("Powered by Groq Llama 3.1 — chat with your document instantly")

# --- Session State ---
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
if "used_questions" not in st.session_state:
    st.session_state.used_questions = []

# All possible suggestions (pool)
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

# --- PDF Upload ---
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("📄 Extracting text..."):
        text = extract_text_from_pdf(uploaded_file)
        st.session_state.pdf_text = text
        index_pdf_text(text)
    st.success("✅ PDF indexed successfully!")

# --- If PDF is uploaded ---
if st.session_state.pdf_text:
    st.divider()

    st.markdown("### 💬 Ask a question about your document")

    # Display chat history
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Agent:** {a}")
        st.markdown("---")

    # --- Dynamic Suggested Questions ---
    st.markdown("#### 🧠 Suggested Questions:")

    # Filter out ones already used
    available_suggestions = [q for q in ALL_SUGGESTIONS if q not in st.session_state.used_questions]

    # Randomly pick up to 3 new ones
    if len(available_suggestions) > 0:
        current_suggestions = random.sample(available_suggestions, min(3, len(available_suggestions)))
    else:
        current_suggestions = ["No more suggestions — try your own question!"]

    # Show as buttons
    cols = st.columns(len(current_suggestions))
    for i, col in enumerate(cols):
        with col:
            if st.button(f"💡 {current_suggestions[i]}"):
                st.session_state.pending_question = current_suggestions[i]
                st.session_state.used_questions.append(current_suggestions[i])
                st.rerun()

    # If user clicked a suggestion, use it
    if st.session_state.pending_question:
        user_question = st.session_state.pending_question
        st.session_state.pending_question = None
    else:
        # Normal chat input
        user_question = st.chat_input("Ask something about the document...")

    # --- Handle question ---
    if user_question:
        with st.spinner("🤖 Thinking..."):
            context = search_similar(user_question)
            answer = answer_question(context, user_question)

        st.session_state.chat_history.append((user_question, answer))
        st.rerun()

else:
    st.info("⬆️ Upload a PDF to start chatting.")
