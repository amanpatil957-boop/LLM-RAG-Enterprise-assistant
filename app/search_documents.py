
from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from .env")

# Load the same model used to generate stored embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def search_documents(question: str, limit: int = 2):
    # Convert the question into a 384-dimensional vector
    query_vector = model.encode(question).tolist()

    client = MongoClient(MONGODB_URI)

    try:
        collection = client["enterprise_assistant"]["document_chunks"]

        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": 20,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source": 1,
                    "chunk_index": 1,
                    "text": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ])

        return list(results)

    finally:
        client.close()


if __name__ == "__main__":
    question = "How many annual paid leave days do employees get?"

    print("Question:", question)
    print("\nRetrieved documents:\n")

    results = search_documents(question)

    if not results:
        print("No matching documents found.")
    else:
        for result in results:
            print("Source:", result["source"])
            print("Chunk:", result["chunk_index"])
            print("Similarity score:", round(result["score"], 4))
            print("Text:", result["text"])
            print("-" * 50)
