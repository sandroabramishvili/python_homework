from database import Base
from sqlalchemy import String, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

class Movie(Base):
    __tablename__ = 'movies'
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(100), nullable=False)
    genre:Mapped[str] = mapped_column(String(100), nullable=False)
    year:Mapped[int] = mapped_column(Integer, nullable=False)
    rating:Mapped[float] = mapped_column(Float, nullable=False)
    description:Mapped[str | None] = mapped_column(Text, nullable=True)



