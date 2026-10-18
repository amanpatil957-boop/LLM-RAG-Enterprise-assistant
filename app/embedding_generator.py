
from sentence_transformers import SentenceTransformer


# Load a lightweight embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    """Convert text into a numerical vector."""
    embedding = model.encode(text)
    return embedding.tolist()


if __name__ == "__main__":
    sample_text = "Employees are entitled to 20 days of annual paid leave."

    vector = generate_embedding(sample_text)

    print("Embedding generated successfully!")
    print("Vector dimensions:", len(vector))
    print("First 5 values:", vector[:5])
