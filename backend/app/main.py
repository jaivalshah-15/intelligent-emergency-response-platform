from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.incidents import router as incidents_router


app = FastAPI(
    title="Intelligent Emergency Response Platform",
    description="Backend API for PS-9",
    version="1.0.0"
)


origins = [
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(incidents_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "emergency-response-backend"
    }