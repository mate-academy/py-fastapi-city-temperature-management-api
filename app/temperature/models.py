from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.engine import Base


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    temperature = Column(Integer, nullable=False)
    city_id = Column(Integer, ForeignKey("city.id"))

    city = relationship("City", back_populates="temperatures")

    def __repr__(self) -> str:
        return str(self.temperature)
