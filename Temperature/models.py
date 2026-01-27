from datetime import datetime

from sqlalchemy import DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from City.models import City


class Temperature(Base):
    __tablename__ = "Temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("Cities.id"))
    city: Mapped[City] = relationship(back_populates="temperatures")
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    temperature: Mapped[int] = mapped_column(Integer)
