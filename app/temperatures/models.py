from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"), index=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    temperature: Mapped[float]

    city: Mapped["City"] = relationship("City", back_populates="temperatures")
