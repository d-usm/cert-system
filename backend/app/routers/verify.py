from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/verify", tags=["verify"])

@router.get("/{token}")
def verify_certificate(token: str, db: Session = Depends(get_db)):
    cert = db.query(models.Certificate).filter(models.Certificate.public_token == token).first()

    if not cert:
        return {
            "valid": False,
            "message": "Сертификат недействителен или не существует"
        }

    student = db.query(models.User).filter(models.User.id == cert.student_id).first()
    course = db.query(models.Course).filter(models.Course.id == cert.course_id).first()

    return {
        "valid": True,
        "fullname": student.fullname,
        "course": course.title,
        "date": cert.created_at.strftime("%Y-%m-%d"),
        "pdf_url": f"/{cert.file_path}",
        "public_token": token
    }

