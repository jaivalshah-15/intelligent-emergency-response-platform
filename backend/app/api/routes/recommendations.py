from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.incident import get_incident
from app.crud.recommendation import (
    create_recommendation,
    get_recommendation,
    get_recommendations,
    update_recommendation_status,
)
from app.db.session import get_db
from app.models.resource import Resource
from app.schemas.recommendation import (
    RecommendationResponse,
    RecommendationStatusUpdate,
)
from app.services.resource_recommender import (
    recommend_resources,
)


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)


@router.get(
    "/",
    response_model=list[RecommendationResponse]
)
def get_all_recommendations(
    incident_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_recommendations(
        db,
        incident_id
    )


@router.get(
    "/{incident_id}",
    response_model=list[RecommendationResponse]
)
def get_incident_recommendations(
    incident_id: int,
    db: Session = Depends(get_db)
):
    return get_recommendations(
        db,
        incident_id
    )


@router.post(
    "/generate/{incident_id}",
    response_model=list[RecommendationResponse]
)
def generate_recommendations(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = get_incident(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    resources = (
        db.query(Resource)
        .filter(
            Resource.status == "AVAILABLE"
        )
        .all()
    )

    recommendations = recommend_resources(
        incident,
        resources
    )

    created = []

    for recommendation in recommendations:
        item = create_recommendation(
            db=db,
            incident_id=incident.id,
            resource_id=recommendation["resource"].id,
            score=recommendation["score"],
            distance_km=recommendation["distance_km"],
            reason=recommendation["reason"],
        )

        created.append(item)

    return created


@router.patch(
    "/{recommendation_id}/status",
    response_model=RecommendationResponse
)
def change_recommendation_status(
    recommendation_id: int,
    status_data: RecommendationStatusUpdate,
    db: Session = Depends(get_db)
):
    if status_data.status not in [
        "PENDING",
        "ACCEPTED",
        "REJECTED",
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid recommendation status"
        )

    recommendation = update_recommendation_status(
        db,
        recommendation_id,
        status_data.status
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return recommendation