from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id: Column[int] = Column(
        Integer, ForeignKey("city.id", ondelete="CASCADE"), nullable=False
    )
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("City", back_populates="temperatures")

    __table_args__ = (UniqueConstraint("city_id", "date_time", name="uix_city_date"),)
