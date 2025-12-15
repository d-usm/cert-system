from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserRead, UserBase
from ..deps import require_role
from ..security import hash_password, generate_password

router = APIRouter(prefix="/operator", tags=["operator"])

@router.get("/students")
def list_students(
    db: Session = Depends(get_db),
    current_user = Depends(require_role("operator", "admin"))
):
    students = (
        db.query(User)
        .filter(User.role == "student")
        .order_by(User.id.asc())
        .all()
    )

    return [
        {
            "id": s.id,
            "fullname": s.fullname,
            "email": s.email,
            "phone": s.phone,
            "created_at": s.created_at
        }
        for s in students
    ]

@router.post("/create-student")
def create_student(
    student: UserBase,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("operator", "admin"))
):
    # Проверяем, существует ли email
    existing = db.query(User).filter(User.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    generated_password = generate_password()

    new_student = User(
        fullname=student.fullname,
        email=student.email,
        phone=student.phone,
        password_hash=hash_password(generated_password),
        role="student",
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "student": {
            "id": new_student.id,
            "fullname": new_student.fullname,
            "email": new_student.email,
            "phone": new_student.phone,
            "role": new_student.role,
        },
        "password": generated_password,
    }

