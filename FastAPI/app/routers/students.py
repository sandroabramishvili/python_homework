from fastapi import APIRouter, Depends, HTTPException, status
from app.models.students import Student
from app.models.subjects import Subject
from app.schemas.students import StudentCreate, StudentResponse, StudentUpdate
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    existing_student = db.query(Student).filter(Student.email == student.email).first()

    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists with this email")

    new_student = Student(name=student.name, last_name=student.last_name, email=student.email)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return student

@router.patch("/{student_id}", response_model=StudentResponse, status_code=status.HTTP_200_OK)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    student_to_update = db.query(Student).filter(Student.id == student_id).first()

    if not student_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    update_data = student.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_student = db.query(Student).filter(Student.email == update_data["email"]).first()

        if existing_student and existing_student.id != student_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already exists with this email")

    for field, value in update_data.items():
        setattr(student_to_update, field, value)

    db.commit()
    db.refresh(student_to_update)

    return student_to_update


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_to_delete = db.query(Student).filter(Student.id == student_id).first()

    if not student_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    db.delete(student_to_delete)
    db.commit()


@router.post("/{student_id}/subjects/{subject_id}", response_model=StudentResponse)
def enroll_student(student_id: int, subject_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    if subject in student.subjects:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is already enrolled in this subject")

    student.subjects.append(subject)

    db.commit()
    db.refresh(student)

    return student


@router.delete("/{student_id}/subjects/{subject_id}", response_model=StudentResponse)
def unenroll_student(student_id: int, subject_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    subject = next((s for s in student.subjects if s.id == subject_id), None)

    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student is not enrolled in this subject")

    student.subjects.remove(subject)

    db.commit()
    db.refresh(student)

    return student
