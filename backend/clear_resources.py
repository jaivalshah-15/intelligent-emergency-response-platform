from app.db.session import SessionLocal
from app.models.resource import Resource
from app.models.assignment import ResourceAssignment

db = SessionLocal()

try:
    # Delete assignments first because they reference resources
    db.query(ResourceAssignment).delete(
        synchronize_session=False
    )

    # Delete all resources
    deleted = db.query(Resource).delete(
        synchronize_session=False
    )

    db.commit()

    print(f"Deleted {deleted} resources successfully.")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()