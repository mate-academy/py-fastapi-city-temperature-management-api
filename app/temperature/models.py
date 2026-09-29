from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), index=True
    )
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    temperature: Mapped[float] = mapped_column(Float)

    city: Mapped["City"] = relationship(  # noqa: F821
        back_populates="temperatures"
    )
