from fastapi import FastAPI

from app.api.routes.resume import router as resume_router


app = FastAPI(
    title="Nivara API",
    description="AI-powered inclusive career platform",
    version="1.0.0"
)


app.include_router(resume_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Nivara API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }