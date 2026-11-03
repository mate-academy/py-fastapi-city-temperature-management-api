from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    additional_info: Mapped[str] = mapped_column(nullable=True)

    temperature: Mapped["temperature"] = relationship(back_populates="cities")