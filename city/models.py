from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from engine import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True)
    additional_info = Column(String(255))

    city = relationship("Temperature", backref="cities")
