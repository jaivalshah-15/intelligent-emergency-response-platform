from sqlalchemy.orm import Session

from app.models.duplicate import DuplicateCandidate


def create_duplicate_candidate(
    db: Session,
    incident_id: int,
    possible_duplicate_id: int,
    similarity_score: float,
    matching_factors: str
):
    candidate = DuplicateCandidate(
        incident_id=incident_id,
        possible_duplicate_id=possible_duplicate_id,
        similarity_score=similarity_score,
        matching_factors=matching_factors,
        status="PENDING",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def get_duplicate_candidates(
    db: Session,
    incident_id: int | None = None
):
    query = db.query(DuplicateCandidate)

    if incident_id is not None:
        query = query.filter(
            DuplicateCandidate.incident_id == incident_id
        )

    return query.all()


def get_duplicate_candidate(
    db: Session,
    candidate_id: int
):
    return (
        db.query(DuplicateCandidate)
        .filter(
            DuplicateCandidate.id == candidate_id
        )
        .first()
    )


def update_duplicate_status(
    db: Session,
    candidate_id: int,
    status: str
):
    candidate = get_duplicate_candidate(
        db,
        candidate_id
    )

    if not candidate:
        return None

    candidate.status = status

    db.commit()
    db.refresh(candidate)

    return candidate