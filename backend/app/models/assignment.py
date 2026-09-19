from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResourceAssignment(Base):
    __tablename__ = "resource_assignments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
        index=True
    )

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ASSIGNED"
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    released_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )