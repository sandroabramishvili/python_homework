from pydantic import BaseModel, Field
from datetime import datetime

class StudentsInSubject(BaseModel):
    id: int
    name: str
    last_name: str
    email: str

class SubjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    duration: int = Field(gt=0)

class SubjectResponse(BaseModel):
    id: int
    name: str
    duration: int
    students: list[StudentsInSubject]

class SubjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    duration: int | None = Field(default=None, gt=0)