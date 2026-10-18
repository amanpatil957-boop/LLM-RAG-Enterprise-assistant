
from pathlib import Path
import sys

from dotenv import load_dotenv
from pymongo import MongoClient

from document_processor import extract_text
from chunker import chunk_text
from embedding_generator import generate_embedding

# Load environment variables from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

import os

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from the .env file")

# Read the sample document
document_path = PROJECT_ROOT / "documents" / "sample.txt"
text = extract_text(str(document_path))

# Split text into chunks
chunks = chunk_text(text, chunk_size=200, overlap=40)

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_URI)
db = client["enterprise_assistant"]
collection = db["document_chunks"]

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

    # Generate and store each chunk
    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        collection.insert_one({
            "source": document_path.name,
            "chunk_index": index,
            "text": chunk,
            "embedding": embedding
        })

        print(f"Stored chunk {index + 1}/{len(chunks)}")

    print("All chunks and embeddings stored successfully!")

finally:
    client.close()
