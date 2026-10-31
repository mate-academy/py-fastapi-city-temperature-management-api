from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationships, relationship

from city.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["City"] = relationship("City", back_populates="temperature")
    date_time: Mapped[datetime] = mapped_column(auto_now_add=True)
    temperature: Mapped[float] = mapped_column()
