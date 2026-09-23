from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base
from app.models.associations import student_subjects


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    duration: Mapped[int] = mapped_column(Integer)
    students: Mapped[list["Student"]] = relationship(secondary=student_subjects, back_populates="subjects")

    def __str__(self):
            return self.name

