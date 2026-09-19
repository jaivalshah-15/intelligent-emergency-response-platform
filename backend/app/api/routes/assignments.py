from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.assignment import (
    create_assignment,
    get_assignments,
    release_assignment,
)
from app.db.session import get_db
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentResponse,
)


router = APIRouter(
    prefix="/api/assignments",
    tags=["Assignments"]
)


@router.post(
    "/",
    response_model=AssignmentResponse
)
def assign_resource(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db)
):
    assignment = create_assignment(
        db=db,
        incident_id=assignment_data.incident_id,
        resource_id=assignment_data.resource_id,
    )

    if not assignment:
        raise HTTPException(
            status_code=400,
            detail="Resource is unavailable or does not exist"
        )

    return assignment


@router.get(
    "/",
    response_model=list[AssignmentResponse]
)
def get_all_assignments(
    db: Session = Depends(get_db)
):
    return get_assignments(db)


@router.patch(
    "/{assignment_id}/release",
    response_model=AssignmentResponse
)
def release_resource(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = release_assignment(
        db,
        assignment_id
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return assignment