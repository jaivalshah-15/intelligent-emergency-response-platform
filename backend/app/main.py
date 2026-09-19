from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.api.routes.incidents import router as incidents_router
from app.api.routes.duplicates import router as duplicates_router
from app.api.routes.websocket import router as websocket_router
from app.api.routes.resources import router as resources_router
from app.api.routes.hospitals import router as hospitals_router
from app.api.routes.teams import router as teams_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.recommendations import (
    router as recommendations_router
)
from app.api.routes.assignments import (
    router as assignments_router
)
from app.api.routes.alerts import (
    router as alerts_router
)
from app.api.routes.ai_assistance import (
    router as ai_assistance_router
)

app = FastAPI(
    title="Intelligent Emergency Response Platform",
    description="Backend API for PS-9",
    version="1.0.0"
)

app.include_router(incidents_router)
app.include_router(duplicates_router)
app.include_router(recommendations_router)
app.include_router(assignments_router)
app.include_router(alerts_router)
app.include_router(resources_router)
app.include_router(hospitals_router)
app.include_router(teams_router)
app.include_router(websocket_router)
app.include_router(ai_assistance_router)
app.include_router(analytics_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "emergency-response-backend"
    }