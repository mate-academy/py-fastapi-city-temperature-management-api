from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Temperature_app.models import DBTemperature
from project_settings.database import Base


class DBCity(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(176), unique=True)
    additional_info = Column(String())
    temperatures = relationship(
        argument=DBTemperature,
        back_populates="city",
    )
