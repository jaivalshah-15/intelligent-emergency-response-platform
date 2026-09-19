from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.assignment import ResourceAssignment
from app.models.resource import Resource


def create_assignment(
    db: Session,
    incident_id: int,
    resource_id: int
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        return None

    if resource.status != "AVAILABLE":
        return None

    assignment = ResourceAssignment(
        incident_id=incident_id,
        resource_id=resource_id,
        status="ASSIGNED",
    )

    resource.status = "ASSIGNED"

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def get_assignments(db: Session):
    return (
        db.query(ResourceAssignment)
        .order_by(
            ResourceAssignment.assigned_at.desc()
        )
        .all()
    )


def release_assignment(
    db: Session,
    assignment_id: int
):
    assignment = (
        db.query(ResourceAssignment)
        .filter(
            ResourceAssignment.id == assignment_id
        )
        .first()
    )

    if not assignment:
        return None

    resource = (
        db.query(Resource)
        .filter(
            Resource.id == assignment.resource_id
        )
        .first()
    )

    if resource:
        resource.status = "AVAILABLE"

    assignment.status = "RELEASED"
    assignment.released_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(assignment)

    return assignment