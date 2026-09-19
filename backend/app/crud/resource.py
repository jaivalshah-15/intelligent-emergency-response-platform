from sqlalchemy.orm import Session

from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate


def create_resource(
    db: Session,
    resource_data: ResourceCreate
):
    resource = Resource(
        name=resource_data.name,
        resource_type=resource_data.resource_type,
        status=resource_data.status,
        latitude=resource_data.latitude,
        longitude=resource_data.longitude,
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


def get_resources(db: Session):
    return db.query(Resource).all()


def get_resource(
    db: Session,
    resource_id: int
):
    return (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )


def update_resource(
    db: Session,
    resource_id: int,
    resource_data: ResourceUpdate
):
    resource = get_resource(db, resource_id)

    if not resource:
        return None

    data = resource_data.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(resource, key, value)

    db.commit()
    db.refresh(resource)

    return resource