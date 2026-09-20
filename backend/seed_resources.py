from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.resource import Resource
from app.models.assignment import ResourceAssignment

db = SessionLocal()

resources = [
    # =========================
    # 5 AMBULANCES
    # =========================

    {
        "name": "Nadiad Ambulance 1",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.6916,
        "longitude": 72.8634
    },
    {
        "name": "Nadiad Ambulance 2",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.6920,
        "longitude": 72.8640
    },
    {
        "name": "Nadiad Ambulance 3",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.6925,
        "longitude": 72.8645
    },
    {
        "name": "Nadiad Ambulance 4",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.6930,
        "longitude": 72.8650
    },
    {
        "name": "Nadiad Ambulance 5",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.6935,
        "longitude": 72.8655
    },

    # =========================
    # 5 FIRE TRUCKS
    # =========================

    {
        "name": "Nadiad Fire Truck 1",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.6918,
        "longitude": 72.8637
    },
    {
        "name": "Nadiad Fire Truck 2",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.6923,
        "longitude": 72.8642
    },
    {
        "name": "Nadiad Fire Truck 3",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.6928,
        "longitude": 72.8647
    },
    {
        "name": "Nadiad Fire Truck 4",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.6933,
        "longitude": 72.8652
    },
    {
        "name": "Nadiad Fire Truck 5",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.6938,
        "longitude": 72.8657
    },

    # =========================
    # 5 FLOOD RESCUE EQUIPMENT
    # =========================

    {
        "name": "Nadiad Flood Rescue Equipment 1",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.6919,
        "longitude": 72.8638
    },
    {
        "name": "Nadiad Flood Rescue Equipment 2",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.6924,
        "longitude": 72.8643
    },
    {
        "name": "Nadiad Flood Rescue Equipment 3",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.6929,
        "longitude": 72.8648
    },
    {
        "name": "Nadiad Flood Rescue Equipment 4",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.6934,
        "longitude": 72.8653
    },
    {
        "name": "Nadiad Flood Rescue Equipment 5",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.6939,
        "longitude": 72.8658
    }
]

try:
    # Delete existing assignments
    db.query(ResourceAssignment).delete(
        synchronize_session=False
    )

    # Delete all existing resources
    db.query(Resource).delete(
        synchronize_session=False
    )

    # Reset auto-increment ID
    db.execute(
        text("ALTER SEQUENCE resources_id_seq RESTART WITH 1")
    )

    # Add the 15 permanent resources
    for data in resources:
        resource = Resource(**data)
        db.add(resource)

    db.commit()

    print("15 resources added successfully.")
    print("5 Ambulances")
    print("5 Fire Trucks")
    print("5 Flood Rescue Equipment")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()