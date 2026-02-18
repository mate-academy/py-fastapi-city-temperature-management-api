from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]
    temperature: Mapped[float]
    city_id: Mapped[int] = mapped_column(
        ForeignKey("city.id", ondelete="CASCADE")
    )

    city = relationship("City", back_populates="temperatures")
