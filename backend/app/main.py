from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .jobs.routes import router as jobs_router
from .api.routes.resume import router as resume_router
from .api.routes.candidate import router as candidate_router
from .api.routes.profile import router as profile_router

from .core.database import Base, engine
from .models.candidate import Candidate


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Nivara API",
    description="AI-powered inclusive career platform",
    version="1.0.0",
)


# Allow the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Job intelligence
app.include_router(jobs_router)

# Candidate and resume management
app.include_router(resume_router)
app.include_router(candidate_router)
app.include_router(profile_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Nivara API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }