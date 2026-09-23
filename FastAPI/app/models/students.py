from app.database import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.associations import student_subjects

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    subjects: Mapped[list["Subject"]] = relationship(secondary=student_subjects, back_populates="students")

    def __str__(self):
        return f"{self.name} {self.last_name}"

    