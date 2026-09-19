from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.hospital import (
    create_hospital,
    get_hospital,
    get_hospitals,
    update_hospital,
)
from app.db.session import get_db
from app.schemas.hospital import (
    HospitalCreate,
    HospitalResponse,
    HospitalUpdate,
)


router = APIRouter(
    prefix="/api/hospitals",
    tags=["Hospitals"]
)


@router.post(
    "/",
    response_model=HospitalResponse
)
def create_hospital_route(
    hospital_data: HospitalCreate,
    db: Session = Depends(get_db)
):
    return create_hospital(
        db,
        hospital_data
    )


@router.get(
    "/",
    response_model=list[HospitalResponse]
)
def get_all_hospitals(
    db: Session = Depends(get_db)
):
    return get_hospitals(db)


@router.get(
    "/{hospital_id}",
    response_model=HospitalResponse
)
def get_single_hospital(
    hospital_id: int,
    db: Session = Depends(get_db)
):
    hospital = get_hospital(
        db,
        hospital_id
    )

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return hospital


@router.patch(
    "/{hospital_id}",
    response_model=HospitalResponse
)
def update_single_hospital(
    hospital_id: int,
    hospital_data: HospitalUpdate,
    db: Session = Depends(get_db)
):
    hospital = update_hospital(
        db,
        hospital_id,
        hospital_data
    )

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return hospital