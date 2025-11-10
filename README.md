📄 PDF Chat Agent

Chat with any PDF using AI — powered by Groq Llama 3.1 models.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pdf-chat-agent-ezlibcmwk8txpxn96pyo5a.streamlit.app/)

Built with Python, ChromaDB, SentenceTransformers, and Ollama.
No API keys. No cloud dependencies. Just pure local AI magic. 🧠✨

🚀 Overview

The PDF Chat Agent lets you upload any PDF and have a conversation with its content.
It extracts, embeds, and searches the document — answering your questions using a local AI model.

Unlike most ChatGPT-based PDF tools, this one runs completely offline:

🧩 Embeddings: via sentence-transformers (no OpenAI API)

🤖 LLM: powered by Ollama
 with models like Mistral, Phi-3, or Llama 3

🗂️ Vector store: handled locally by ChromaDB

🖥️ Interface: via Streamlit

✨ Features

✅ Upload any PDF
✅ Ask natural-language questions
✅ Works entirely offline — no API keys required
✅ Uses free local models via Ollama
✅ Easy to run on WSL, macOS, or Linux
✅ Clean and simple web interface

🧰 Tech Stack
Layer	Tool
Language	Python 3.10+
AI Model (LLM)	Ollama (Mistral, Phi-3, etc.)
Embeddings	SentenceTransformers (all-MiniLM-L6-v2)
Vector DB	ChromaDB
Frontend	Streamlit
PDF Parser	PyMuPDF (fitz)
⚙️ Installation
🐧 1. Clone the repo
git clone https://github.com/<your-username>/pdf-chat-agent.git
cd pdf-chat-agent

🧱 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

📦 3. Install dependencies
pip install -r requirements.txt

🧠 4. Install Ollama and pull a local model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral


(You can replace mistral with phi or llama3 if you prefer.)

🧩 Usage
💻 Run in the terminal
python src/main.py --pdf data/example.pdf


Ask questions like:

You: Summarize section 2
You: What is the main topic of this document?
You: Who wrote it?

🌐 Run with Streamlit (web UI)
streamlit run src/streamlit_app.py


Then open your browser at:
👉 http://localhost:8501

⭐ If you like this project, consider giving it a star on GitHub!
