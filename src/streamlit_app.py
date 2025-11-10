import streamlit as st
from agent.pdf_loader import extract_text_from_pdf
from agent.vector_store import index_pdf_text, search_similar
from agent.llm_client import answer_question

st.set_page_config(page_title="📄 Chat with your PDF", layout="centered")

st.title("📄 Chat with your PDF")
st.caption("Powered by Groq Llama 3.1 — chat with your document instantly")

# Persistent state for conversation
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Handle PDF upload
if uploaded_file is not None:
    with st.spinner("📄 Extracting text..."):
        text = extract_text_from_pdf(uploaded_file)
        st.session_state.pdf_text = text
        index_pdf_text(text)
    st.success("✅ PDF indexed successfully! Ask below 👇")

# Display conversation if PDF is uploaded
if st.session_state.pdf_text:
    # Show conversation history
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Agent:** {a}")
        st.markdown("---")

    # Always show a new input prompt after each answer
    user_question = st.chat_input("Ask something about the document...")

    if user_question:
        with st.spinner("🤖 Thinking..."):
            # Find relevant content in the PDF
            context = search_similar(user_question)
            # Get the model’s answer
            answer = answer_question(context, user_question)

        # Store Q&A in history
        st.session_state.chat_history.append((user_question, answer))

        # Rerun immediately so it shows up and re-displays input box again
        st.rerun()
else:
    st.info("⬆️ Upload a PDF to start chatting.")
