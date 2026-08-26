from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from city_api.models import City
from database import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("City.id", ondelete="CASCADE"),
        nullable=False,
    )
    city: Mapped["City"] = relationship( "City", back_populates="temperature")
    date_time: Mapped[datetime]
    temperature: Mapped[float]
