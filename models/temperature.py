from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"))
    datetime: Mapped[datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)

    city = relationship("City", back_populates="temperatures")
