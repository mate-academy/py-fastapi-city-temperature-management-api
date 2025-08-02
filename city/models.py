from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    additional_info = Column(String(511), nullable=True)

    # Add this line to establish a relationship with the Temperature model
    temperatures = relationship(
        "Temperature",
        back_populates="city",
        cascade="all, delete",
        passive_deletes=True
    )
