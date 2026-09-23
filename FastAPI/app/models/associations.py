from sqlalchemy import Table, Column, ForeignKey, DateTime, func
from app.database import Base

student_subjects = Table(
    "student_subjects",
    Base.metadata,
    Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True),
    Column("enrolled_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)
