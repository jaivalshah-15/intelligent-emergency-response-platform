from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.resource import (
    create_resource,
    get_resource,
    get_resources,
    update_resource,
)
from app.db.session import get_db
from app.schemas.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)


router = APIRouter(
    prefix="/api/resources",
    tags=["Resources"]
)


@router.post(
    "/",
    response_model=ResourceResponse
)
def create_resource_route(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db)
):
    return create_resource(
        db,
        resource_data
    )


@router.get(
    "/",
    response_model=list[ResourceResponse]
)
def get_all_resources(
    db: Session = Depends(get_db)
):
    return get_resources(db)


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse
)
def get_single_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = get_resource(
        db,
        resource_id
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource


@router.patch(
    "/{resource_id}",
    response_model=ResourceResponse
)
def update_single_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db)
):
    resource = update_resource(
        db,
        resource_id,
        resource_data
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource