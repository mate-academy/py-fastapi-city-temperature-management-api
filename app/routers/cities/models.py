from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

import app.routers.temperature.models as models

class City(Base):
    __tablename__ = "City"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)
    temperatures: Mapped[list["models.Temperature"]] = relationship("Temperature",
                                                             back_populates="city",
                                                             cascade="all, delete-orphan")