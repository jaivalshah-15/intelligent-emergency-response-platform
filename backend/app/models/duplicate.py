from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DuplicateCandidate(Base):
    __tablename__ = "duplicate_candidates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
        index=True
    )

    possible_duplicate_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
        index=True
    )

    similarity_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    matching_factors: Mapped[str | None] = mapped_column(
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