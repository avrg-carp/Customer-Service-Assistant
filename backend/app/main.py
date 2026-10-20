from fastapi import FastAPI

app = FastAPI(title="Front-line Assistant (RAG)")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
