from fastapi import FastAPI
from smart_support_agent.config import settings
from smart_support_agent.routes.api import router as api_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}