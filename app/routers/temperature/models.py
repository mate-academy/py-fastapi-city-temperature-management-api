from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

import app.routers.cities.models as models

class Temperature(Base):
    __tablename__ = "Temperature"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("City.id", ondelete="CASCADE"), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped["models.City"] = relationship("City", back_populates="temperatures")