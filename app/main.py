from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag_pipeline import ask_question

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Ask questions about company documents.",
    version="1.0.0",
)
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class QuestionRequest(BaseModel):
    question: str


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "indexx.html")

@app.get("/health")
def health():
    return {"status": "healthy"}



@app.post("/ask")
def ask(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        print("DEBUG: /ask received:", question, flush=True)
        return ask_question(question)
    except Exception:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to answer the question. "
                "Check the backend terminal for details."
            ),
        )

