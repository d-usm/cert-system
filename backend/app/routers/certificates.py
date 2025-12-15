# app/routers/certificates.py
import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_role

router = APIRouter(prefix="/certificates", tags=["certificates"])


def generate_serial(user_id: int, course_id: int) -> str:
    return f"CERT-{course_id}-{user_id}-{uuid.uuid4().hex[:8].upper()}"

@router.post("/issue/{user_id}/{course_id}", response_model=schemas.CertificateRead)
def issue_certificate(
    user_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "teacher")),
):
    # Проверяем, есть ли пользователь и курс
    user = db.query(models.User).filter(models.User.id == user_id).first()
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not user or not course:
        raise HTTPException(status_code=404, detail="User or course not found")

    # Можно добавить проверку: завершен ли курс
    progress = (
        db.query(models.CourseProgress)
        .filter(
            models.CourseProgress.user_id == user_id,
            models.CourseProgress.course_id == course_id,
        )
        .first()
    )
    if not progress or progress.progress < 100:
        raise HTTPException(
            status_code=400,
            detail="Course not completed yet",
        )

    # Проверяем, нет ли уже сертификата
    existing = (
        db.query(models.Certificate)
        .filter(
            models.Certificate.user_id == user_id,
            models.Certificate.course_id == course_id,
            models.Certificate.revoked.is_(False),
        )
        .first()
    )
    if existing:
        return existing

    serial = generate_serial(user_id, course_id)
    token = uuid.uuid4().hex

    cert = models.Certificate(
        user_id=user_id,
        course_id=course_id,
        serial=serial,
        token=token,
        pdf_path=None,
        issued_at=datetime.utcnow(),
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/my", response_model=List[schemas.CertificateRead])
def my_certificates(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    certs = (
        db.query(models.Certificate)
        .filter(
            models.Certificate.user_id == current_user.id,
            models.Certificate.revoked.is_(False),
        )
        .all()
    )
    return certs

