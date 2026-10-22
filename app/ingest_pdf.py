
from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient

from document_processor import extract_text
from chunker import chunk_text
from embedding_generator import generate_embedding

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing from .env")

# Manufacturing PDF path
pdf_path = PROJECT_ROOT / "documents" / "manufacturing_report.pdf"

if not pdf_path.exists():
    raise FileNotFoundError(
        f"Please place the PDF here: {pdf_path}"
    )

# Extract PDF text
text = extract_text(str(pdf_path))
print("PDF text extracted successfully.")

# Split text into chunks
chunks = chunk_text(text, chunk_size=500, overlap=100)
print(f"Total chunks created: {len(chunks)}")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

    collection = client["enterprise_assistant"]["document_chunks"]

    # Prevent duplicate ingestion of this PDF on repeated runs
    collection.delete_many({"source": pdf_path.name})

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        collection.insert_one({
            "source": pdf_path.name,
            "chunk_index": index,
            "text": chunk,
            "embedding": embedding
        })

        print(f"Stored chunk {index + 1}/{len(chunks)}")

    print("Manufacturing PDF ingestion completed!")

finally:
    client.close()
