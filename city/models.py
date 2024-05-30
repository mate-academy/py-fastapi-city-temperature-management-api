from sqlalchemy import Integer, Column, String, Text
from sqlalchemy.orm import relationship
from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    additional_info = Column(Text, nullable=True)

    temperatures = relationship("Temperature", back_populates="city")
