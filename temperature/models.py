from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class DBTemperature(Base):
    __tablename__ = "temperature"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True
    )
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), nullable=False)
    date_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    city = relationship("DBCity", back_populates="temperatures")
