from sqlalchemy.orm import Session

from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate


def create_hospital(
    db: Session,
    hospital_data: HospitalCreate
):
    hospital = Hospital(
        name=hospital_data.name,
        address=hospital_data.address,
        latitude=hospital_data.latitude,
        longitude=hospital_data.longitude,
        total_beds=hospital_data.total_beds,
        available_beds=hospital_data.available_beds,
        emergency_capacity=hospital_data.emergency_capacity,
        status=hospital_data.status,
    )

    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    return hospital


def get_hospitals(db: Session):
    return db.query(Hospital).all()


def get_hospital(
    db: Session,
    hospital_id: int
):
    return (
        db.query(Hospital)
        .filter(Hospital.id == hospital_id)
        .first()
    )


def update_hospital(
    db: Session,
    hospital_id: int,
    hospital_data: HospitalUpdate
):
    hospital = get_hospital(
        db,
        hospital_id
    )

    if not hospital:
        return None

    data = hospital_data.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(hospital, key, value)

    db.commit()
    db.refresh(hospital)

    return hospital