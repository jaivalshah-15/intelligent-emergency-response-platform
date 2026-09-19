import pytest

from app.crud.assignment import (
    create_assignment,
    release_assignment,
)
from app.db.session import SessionLocal
from app.models.incident import Incident
from app.models.resource import Resource


def test_assignment_changes_resource_status():
    db = SessionLocal()

    try:
        incident = (
            db.query(Incident)
            .filter(Incident.status == "ACTIVE")
            .first()
        )

        resource = (
            db.query(Resource)
            .filter(Resource.status == "AVAILABLE")
            .first()
        )

        if not incident or not resource:
            pytest.skip(
                "Need at least one ACTIVE incident and one AVAILABLE resource"
            )

        assignment = create_assignment(
            db=db,
            incident_id=incident.id,
            resource_id=resource.id,
        )

        assert assignment is not None

        db.refresh(resource)
        assert resource.status == "ASSIGNED"

        # Release so the test does not leave the resource assigned
        released = release_assignment(
            db=db,
            assignment_id=assignment.id,
        )

        assert released is not None

        db.refresh(resource)
        assert resource.status == "AVAILABLE"

    finally:
        db.close()