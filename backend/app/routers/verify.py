from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter(prefix="/verify", tags=["verify"])


@router.get("/{token}")
def verify_certificate(token: str, db: Session = Depends(get_db)):
    cert = (
        db.query(models.Certificate)
        .filter(
            models.Certificate.token == token,
            models.Certificate.revoked.is_(False),
        )
        .first()
    )

    if not cert:
        return {
            "valid": False,
            "message": "Сертификат недействителен или не существует",
        }

    student = db.query(models.User).filter(models.User.id == cert.user_id).first()
    course = db.query(models.Course).filter(models.Course.id == cert.course_id).first()

    issued_date = cert.issued_at or cert.created_at

    return {
        "valid": True,
        "fullname": student.fullname if student else None,
        "course": course.title if course else None,
        "date": issued_date.strftime("%Y-%m-%d") if issued_date else None,
        "pdf_url": f"/{cert.pdf_path}" if cert.pdf_path else None,
        "public_token": token,
    }

