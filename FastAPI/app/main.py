from fastapi import FastAPI
from app.routers import subjects, students

app = FastAPI(
    title="Students & Subjects API",
    version="0.1.0",
    description="A simple API for managing students and subjects",
)

app.include_router(subjects.router)
app.include_router(students.router)