from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.retrieve import router as retrieve_router
from app.api.upload import router as upload_router

app = FastAPI(
    title="Hybrid Retrieval Enterprise Document Intelligence Engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(retrieve_router)

@app.get("/")
def root():
    return {
        "message": "Backend is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}