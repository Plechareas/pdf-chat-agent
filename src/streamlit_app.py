import streamlit as st
from agent.pdf_loader import extract_text_from_pdf
from agent.vector_store import index_pdf_text, search_similar
from agent.llm_client import answer_question

st.set_page_config(page_title="PDF Chat Agent", page_icon="📄", layout="wide")
st.title("📄 Chat with your PDF")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Extracting and indexing PDF..."):
        text = extract_text_from_pdf("temp.pdf")
        index_pdf_text(text)
        st.success("PDF indexed successfully! Ask below 👇")

    query = st.text_input("Ask something about the document:")
    if query:
        with st.spinner("Thinking..."):
            docs = search_similar(query)
            context = "\n\n".join(docs)
            answer = answer_question(context, query)
        st.markdown(f"**Answer:** {answer}")
