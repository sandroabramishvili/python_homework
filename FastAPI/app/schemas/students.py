from pydantic import BaseModel

class SubjectsForStudent(BaseModel):
    id: int
    name: str
    duration: int

class StudentCreate(BaseModel):
    name: str
    last_name: str
    email: str

class StudentResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    subjects: list[SubjectsForStudent]

class StudentUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: str | None = None