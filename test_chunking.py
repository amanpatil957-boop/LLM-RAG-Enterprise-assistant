
from app.document_processor import extract_text
from app.chunker import chunk_text

# Read the sample document
file_path = "documents/sample.txt"
text = extract_text(file_path)

# Split the extracted text into chunks
chunks = chunk_text(text, chunk_size=200, overlap=40)

print("Document processing and chunking successful!")
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk)
