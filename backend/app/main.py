from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Emergency Response Platform",
    description="Backend API for PS-9",
    version="1.0.0"
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "emergency-response-backend"
    }