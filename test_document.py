
print("Test script started!")

from app.document_processor import extract_text

file_path = "documents/sample.txt"

try:
    text = extract_text(file_path)
    print("Document extracted successfully!")
    print("\nExtracted content:\n")
    print(text)

except Exception as error:
    print("Document extraction failed:", error)
