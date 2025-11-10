import os
import requests

API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '')}",
    "Content-Type": "application/json",
}

def answer_question(context, question):
    """Ask Groq’s Mixtral model about a piece of text."""
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

    try:
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions about a document.",
                },
                {"role": "user", "content": prompt},
            ],
            # Groq follows the OpenAI schema. Use 'max_tokens', 'temperature', etc.
            "max_tokens": 200,
            "temperature": 0.2,
        }

        resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        if resp.status_code != 200:
            # print server error message for debugging
            return f"[Groq error {resp.status_code}] {resp.text}"

        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"[Error contacting Groq] {e}"
