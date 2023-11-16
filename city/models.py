from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(Text)

    temperature = relationship("Temperature", back_populates="city")
