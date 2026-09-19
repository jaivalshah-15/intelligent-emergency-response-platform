from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics import get_analytics


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


@router.get("/", response_model=AnalyticsResponse)
def analytics_route(
    db: Session = Depends(get_db)
):
    return get_analytics(db)