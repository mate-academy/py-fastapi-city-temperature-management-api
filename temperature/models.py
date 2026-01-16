import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), index=True)
    city: Mapped["City"] = relationship(
        "city.models.City", back_populates="temperatures"
    )
    date_time: Mapped[sqlalchemy.DateTime] = mapped_column(
        sqlalchemy.DateTime(timezone=True)
    )
    temperature: Mapped[float] = mapped_column()
