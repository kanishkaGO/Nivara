from fastapi import FastAPI

app = FastAPI(
    title="Nivara API",
    description="AI-powered inclusive career platform",
    version="1.0.0"
)


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