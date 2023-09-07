from sqlalchemy.orm import relationship

from engine import Base
from sqlalchemy import Column, Integer, String


class DBCity(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), nullable=False, unique=True)
    additional_info = Column(String(1023), nullable=False, unique=False)

    city_id = relationship("Temperature", back_populates="cities")


