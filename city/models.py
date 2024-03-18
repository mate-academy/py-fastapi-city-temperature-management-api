from sqlalchemy.orm import Mapped, mapped_column, relationship

from city.utils import str256
from database import Base


class CityDB(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str256] = mapped_column()
    additional_info: Mapped[str256] = mapped_column()

    temperature = relationship("TemperatureDB", back_populates="city")
