# app/routers/certificates.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_role

router = APIRouter(prefix="/certificates", tags=["certificates"])
router = APIRouter(prefix="/verify", tags=["verify"])


def generate_serial(user_id: int, course_id: int) -> str:
    return f"CERT-{course_id}-{user_id}-{uuid.uuid4().hex[:8].upper()}"

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
            models.Certificate.revoked == False,
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
        pdf_path=None,  # позже добавим путь к сгенерированному PDF
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.get("/verify/{token}", response_model=schemas.CertificateRead)
def verify_certificate(
    token: str,
    db: Session = Depends(get_db),
):
    cert = db.query(models.Certificate).filter(models.Certificate.token == token).first()
    if not cert or cert.revoked:
        raise HTTPException(status_code=404, detail="Certificate not found or revoked")
    return cert


@router.get("/my", response_model=List[schemas.CertificateRead])
def my_certificates(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    certs = (
        db.query(models.Certificate)
        .filter(models.Certificate.user_id == current_user.id)
        .all()
    )
    return certs

