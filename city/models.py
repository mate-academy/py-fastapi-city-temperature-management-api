from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    additional_info = Column(String(511))

    temperatures = relationship('Temperature', back_populates='city')
