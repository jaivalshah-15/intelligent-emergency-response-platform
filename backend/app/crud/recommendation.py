from sqlalchemy.orm import Session

from app.models.recommendation import ResourceRecommendation


def create_recommendation(
    db: Session,
    incident_id: int,
    resource_id: int,
    score: float,
    distance_km: float | None,
    reason: str
):
    recommendation = ResourceRecommendation(
        incident_id=incident_id,
        resource_id=resource_id,
        score=score,
        distance_km=distance_km,
        reason=reason,
        status="PENDING",
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


def get_recommendations(
    db: Session,
    incident_id: int | None = None
):
    query = db.query(ResourceRecommendation)

    if incident_id is not None:
        query = query.filter(
            ResourceRecommendation.incident_id
            == incident_id
        )

    return query.order_by(
        ResourceRecommendation.score.desc()
    ).all()


def get_recommendation(
    db: Session,
    recommendation_id: int
):
    return (
        db.query(ResourceRecommendation)
        .filter(
            ResourceRecommendation.id
            == recommendation_id
        )
        .first()
    )


def update_recommendation_status(
    db: Session,
    recommendation_id: int,
    status: str
):
    recommendation = get_recommendation(
        db,
        recommendation_id
    )

    if not recommendation:
        return None

    recommendation.status = status

    db.commit()
    db.refresh(recommendation)

    return recommendation