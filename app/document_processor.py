
from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_text(file_path: str) -> str:
    """Extract text from PDF, DOCX, or TXT files."""

    path = Path(file_path)
    extension = path.suffix.lower()

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if extension == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif extension == ".docx":
        document = Document(str(path))
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    elif extension == ".txt":
        text = path.read_text(encoding="utf-8")

    else:
        raise ValueError(
            "Supported formats: PDF, DOCX, TXT"
        )

    if not text.strip():
        raise ValueError(
            "No readable text found in this document."
        )

    return text.strip()


if __name__ == "__main__":
    print("Document processor is ready.")
