import argparse
from agent.pdf_loader import extract_text_from_pdf
from agent.vector_store import index_pdf_text
from agent.chat_agent import chat_with_pdf

def main():
    parser = argparse.ArgumentParser(description="Chat with your PDF locally")
    parser.add_argument("--pdf", type=str, required=True, help="Path to the PDF file")
    args = parser.parse_args()

    print("📄 Extracting text from PDF...")
    text = extract_text_from_pdf(args.pdf)

    print("🧠 Indexing PDF content...")
    index_pdf_text(text)

    print("✅ Ready! Type your question (or 'exit' to quit):")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break
        print("🤖 Thinking...")
        answer = chat_with_pdf(query)
        print(f"\nAgent: {answer}\n")

if __name__ == "__main__":
    main()