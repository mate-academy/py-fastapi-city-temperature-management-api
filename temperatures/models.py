from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from database import Base


class Temperature(Base):
    __tablename__ = 'temperatures'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("City")
