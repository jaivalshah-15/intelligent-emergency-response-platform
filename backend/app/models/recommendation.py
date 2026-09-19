from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResourceRecommendation(Base):
    __tablename__ = "resource_recommendations"

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

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    distance_km: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )