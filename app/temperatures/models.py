from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"), index=True
    )
    temperature: Mapped[float] = mapped_column()
    date_time: Mapped[datetime] = mapped_column(server_default=func.now())

    city = relationship("City", back_populates="temperatures")
