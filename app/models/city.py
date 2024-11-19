from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.dependencies import Base


class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    additional_info = Column(String(511))

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete, delete-orphan",
    )
