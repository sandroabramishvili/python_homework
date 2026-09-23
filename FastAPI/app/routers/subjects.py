from fastapi import APIRouter, Depends, HTTPException, status
from app.models.subjects import Subject
from app.schemas.subjects import SubjectCreate, SubjectResponse, SubjectUpdate
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=list[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    return subjects

@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):

    existing_subject = db.query(Subject).filter(Subject.name == subject.name).first()

    if existing_subject:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subject already exists with this name")

    new_subject = Subject(name=subject.name, duration=subject.duration)

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    return subject

@router.patch("/{subject_id}", response_model=SubjectResponse, status_code=status.HTTP_200_OK)
def update_subject(subject_id: int, subject: SubjectUpdate, db: Session = Depends(get_db)):
    subject_to_update = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    update_data = subject.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing_subject = db.query(Subject).filter(Subject.name == update_data["name"]).first()

        if existing_subject and existing_subject.id != subject_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subject already exists with this name")

    for field, value in update_data.items():
        setattr(subject_to_update, field, value)

    db.commit()
    db.refresh(subject_to_update)

    return subject_to_update


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject_to_delete = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    db.delete(subject_to_delete)
    db.commit()






