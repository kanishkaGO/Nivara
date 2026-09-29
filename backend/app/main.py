from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.resume import router as resume_router
from app.api.routes.candidate import router as candidate_router
from app.api.routes.profile import router as profile_router

from app.core.database import Base, engine
from app.models.candidate import Candidate


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Nivara API",
    description="AI-powered inclusive career platform",
    version="1.0.0"
)


# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(resume_router)
app.include_router(candidate_router)
app.include_router(profile_router)


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