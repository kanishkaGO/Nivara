from fastapi import FastAPI

from .jobs.routes import router as jobs_router


app = FastAPI(title="Nivara Backend")


app.include_router(jobs_router)


@app.get("/")
def root():
    return {"message": "Nivara backend is running"}