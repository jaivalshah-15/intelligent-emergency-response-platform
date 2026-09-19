from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.duplicate import (
    get_duplicate_candidates,
    get_duplicate_candidate,
    update_duplicate_status,
)
from app.db.session import get_db
from app.schemas.duplicate import (
    DuplicateCandidateResponse,
    DuplicateStatusUpdate,
)


router = APIRouter(
    prefix="/api/duplicates",
    tags=["Duplicates"]
)


@router.get(
    "/",
    response_model=list[DuplicateCandidateResponse]
)
def get_duplicates(
    incident_id: int | None = None,
    db: Session = Depends(get_db)
):
    return get_duplicate_candidates(
        db,
        incident_id
    )


@router.get(
    "/{candidate_id}",
    response_model=DuplicateCandidateResponse
)
def get_duplicate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    candidate = get_duplicate_candidate(
        db,
        candidate_id
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Duplicate candidate not found"
        )

    return candidate


@router.patch(
    "/{candidate_id}/status",
    response_model=DuplicateCandidateResponse
)
def change_duplicate_status(
    candidate_id: int,
    status_data: DuplicateStatusUpdate,
    db: Session = Depends(get_db)
):
    if status_data.status not in [
        "PENDING",
        "CONFIRMED",
        "REJECTED"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid duplicate status"
        )

    candidate = update_duplicate_status(
        db,
        candidate_id,
        status_data.status
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Duplicate candidate not found"
        )

    return candidate