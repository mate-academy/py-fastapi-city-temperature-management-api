from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    additional_info: Mapped[str] = mapped_column(nullable=True)
