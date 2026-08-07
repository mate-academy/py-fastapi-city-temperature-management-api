from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.city import City


class Temperature(Base):
    __tablename__ = "temperature"
    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped[City] = relationship(back_populates="temperature")
    date_time: Mapped[datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()
