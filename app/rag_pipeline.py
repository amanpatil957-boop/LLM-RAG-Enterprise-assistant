
import requests

from app.search_documents import search_documents


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"


def ask_question(question: str) -> dict:
    # Retrieve relevant chunks from MongoDB
    results = search_documents(question)

    if not results:
        return {
            "answer": "I couldn't find relevant information in the available documents.",
            "sources": [],
        }

    # Build context from the retrieved document chunks
    context_parts = []
    sources = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"Content: {result['text']}"
        )

        source_info = {
            "source": result["source"],
            "chunk_index": result["chunk_index"],
            "score": round(result["score"], 4),
        }

        if source_info not in sources:
            sources.append(source_info)

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an enterprise document assistant.

Answer the user's question using only the provided document context.
If the context does not contain the answer, clearly say that the
available documents do not provide enough information.
Do not invent facts.

Document context:
{context}

User question:
{question}
"""

    # Generate an answer using Ollama
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
        },
        timeout=180,
    )

    response.raise_for_status()
    data = response.json()

    return {
        "answer": data["message"]["content"],
        "sources": sources,
    }


if __name__ == "__main__":
    question = "How many annual paid leave days do employees get?"

    result = ask_question(question)

    print("\nQuestion:", question)
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    for source in result["sources"]:
        print(source)
