from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    temperature: Mapped[float]
    date_time: Mapped[datetime]
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))

    city = relationship("DBCity", back_populates="temperatures")
