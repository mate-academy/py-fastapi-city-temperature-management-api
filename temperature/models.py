from sqlalchemy import Column, Integer, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    temperature = Column(Integer)
    city_id = Column(Integer, ForeignKey("cites.id"))

    city = relationship("City", back_populates="temperatures")
