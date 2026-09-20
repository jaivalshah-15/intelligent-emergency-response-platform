from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.resource import Resource
from app.models.assignment import ResourceAssignment

db = SessionLocal()

resources = [
    # Ambulances
    {
        "name": "Ambulance 1",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.3072,
        "longitude": 73.1812
    },
    {
        "name": "Ambulance 2",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.3075,
        "longitude": 73.1815
    },
    {
        "name": "Ambulance 3",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.3080,
        "longitude": 73.1820
    },
    {
        "name": "Ambulance 4",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.3085,
        "longitude": 73.1825
    },
    {
        "name": "Ambulance 5",
        "resource_type": "AMBULANCE",
        "status": "AVAILABLE",
        "latitude": 22.3090,
        "longitude": 73.1830
    },

    # Fire Trucks
    {
        "name": "Fire Truck 1",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.3072,
        "longitude": 73.1812
    },
    {
        "name": "Fire Truck 2",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.3068,
        "longitude": 73.1808
    },
    {
        "name": "Fire Truck 3",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.3064,
        "longitude": 73.1804
    },
    {
        "name": "Fire Truck 4",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.3060,
        "longitude": 73.1800
    },
    {
        "name": "Fire Truck 5",
        "resource_type": "FIRE_TRUCK",
        "status": "AVAILABLE",
        "latitude": 22.3056,
        "longitude": 73.1796
    },

    # Flood Rescue Equipment
    {
        "name": "Flood Rescue Equipment 1",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.3072,
        "longitude": 73.1812
    },
    {
        "name": "Flood Rescue Equipment 2",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.3076,
        "longitude": 73.1816
    },
    {
        "name": "Flood Rescue Equipment 3",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.3080,
        "longitude": 73.1820
    },
    {
        "name": "Flood Rescue Equipment 4",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.3084,
        "longitude": 73.1824
    },
    {
        "name": "Flood Rescue Equipment 5",
        "resource_type": "FLOOD_RESCUE_EQUIPMENT",
        "status": "AVAILABLE",
        "latitude": 22.3088,
        "longitude": 73.1828
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

    # Reset resource ID numbering
    db.execute(
        text("ALTER SEQUENCE resources_id_seq RESTART WITH 1")
    )

    # Add the 15 resources
    for data in resources:
        resource = Resource(**data)
        db.add(resource)

    db.commit()

    print("15 resources added successfully.")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()
