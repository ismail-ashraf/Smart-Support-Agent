from fastapi import APIRouter, UploadFile, File, HTTPException
from smart_support_agent.schemas import (
    IngestResponse,
    QueryRequest,
    QueryResponse
)
from smart_support_agent.services.parser import DocumentParser
from smart_support_agent.services.qdrant_service import qdrant_service

router = APIRouter()
parser = DocumentParser()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        chunks = parser.parse_file(content, file.filename)

        if not chunks:
            raise HTTPException(status_code=400, detail="No content could be extracted from file.")

        added_count = qdrant_service.upsert_chunks(chunks)
        doc_id = chunks[0]["doc_id"]

        return IngestResponse(
            chunks_added=added_count,
            doc_id=doc_id,
            message=f"Successfully indexed {added_count} chunks from {file.filename}."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    try:
        # FastAPI performs retrieval only and returns passages with relevance scores to n8n[cite: 2]
        passages = qdrant_service.search_similar(request.question, top_k=4)
        top_score = passages[0].score if passages else 0.0

        return QueryResponse(passages=passages, top_score=top_score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))