from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.engine import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    additional_info = Column(String(512))
    temperatures = relationship("Temperature", back_populates="city")

    def __repr__(self) -> str:
        return str(self.name)
