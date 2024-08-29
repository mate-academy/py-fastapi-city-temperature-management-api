from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temprerature"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column()
    temperature: Mapped[float] = mapped_column()
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))

    city = relationship("City", back_populates="temperature")
