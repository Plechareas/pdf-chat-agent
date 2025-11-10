import streamlit as st
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

    # --- Recommended questions ---
    st.markdown("#### 🧠 Suggested Questions:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Summarize this document"):
            st.session_state.pending_question = "Can you summarize this document?"
    with col2:
        if st.button("📑 What are the main topics?"):
            st.session_state.pending_question = "What are the main topics in this document?"
    with col3:
        if st.button("💡 Key insights or conclusions?"):
            st.session_state.pending_question = "What are the key insights or conclusions?"

    # If the user clicked a suggestion, set it as question
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
