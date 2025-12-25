from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag import RAGPipeline
import traceback

app = FastAPI(title="NLPAssist+ API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all. In prod, restrict.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Pipeline (Singup)
rag_pipeline = RAGPipeline()
# Ingest on startup for simplicity
rag_pipeline.ingest_documents()

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to NLPAssist+ API"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Query text cannot be empty.")
        
        result = rag_pipeline.generate_answer(request.text)
        # Deduplicate sources
        unique_sources = list(set(result["sources"]))
        return QueryResponse(answer=result["answer"], sources=unique_sources)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def trigger_ingest():
    try:
        rag_pipeline.ingest_documents()
        return {"status": "success", "message": "Documents ingested."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
