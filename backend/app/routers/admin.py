import os
import os
import secrets
from datetime import datetime

import qrcode
from fastapi import APIRouter, Depends, HTTPException
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from .. import models, schemas
from ..config import settings
from ..database import get_db
from ..deps import require_role

router = APIRouter(prefix="/admin", tags=["admin"])


# 1. Получить список экзаменов, ожидающих утверждения
@router.get("/pending-exams", response_model=list[schemas.ExamResultAdmin])
def get_pending_exams(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    exams = (
        db.query(models.ExamResult)
        .filter(models.ExamResult.approved.is_(None))
        .all()
    )
    return exams

#@router.get("/certificates")
#def list_certificates(
#    db: Session = Depends(get_db),
#    user=Depends(require_role("admin"))
#):
#    certs = db.query(models.Certificate).all()
#    return certs
@router.get("/certificates")
def list_certificates(db: Session = Depends(get_db), admin=Depends(require_role("admin"))):
    certs = db.query(models.Certificate).filter(models.Certificate.revoked.is_(False)).all()
    output = []

    for cert in certs:
        student = db.query(models.User).filter(models.User.id == cert.user_id).first()
        course = db.query(models.Course).filter(models.Course.id == cert.course_id).first()

        output.append({
            "id": cert.id,
            "fullname": student.fullname,
            "email": student.email,
            "course": course.title,
            "date": (cert.issued_at or cert.created_at).strftime("%Y-%m-%d"),
            "pdf_url": f"/{cert.pdf_path}" if cert.pdf_path else None,
            "public_token": cert.token,
        })

    return output


# 2. Утвердить экзамен и создать сертификат

@router.post("/approve/{exam_id}")
def approve_exam(
        exam_id: int,
        db: Session = Depends(get_db),
        admin = Depends(require_role("admin"))
):

    exam = db.query(models.ExamResult).filter(models.ExamResult.id == exam_id).first()
    if not exam:
        raise HTTPException(404, "Экзамен не найден")

    if not exam.is_passed:
        raise HTTPException(400, "Экзамен не сдан")

    if exam.approved:
        raise HTTPException(400, "Уже утверждено")

    existing_cert = (
        db.query(models.Certificate)
        .filter(
            models.Certificate.exam_id == exam.id,
            models.Certificate.revoked.is_(False),
        )
        .first()
    )
    if existing_cert:
        return {
            "status": "approved",
            "public_token": existing_cert.token,
            "verify_url": f"{settings.PUBLIC_BASE_URL.rstrip('/')}/verify/{existing_cert.token}",
        }

    # отметили как утвержденный
    exam.approved = True
    db.commit()

    # 1. Генерируем уникальный токен
    public_token = secrets.token_urlsafe(32)

    # 2. Папка для сертификатов
    cert_dir = settings.CERTIFICATES_DIR
    os.makedirs(cert_dir, exist_ok=True)

    # 3. QR-код
    verify_url = f"{settings.PUBLIC_BASE_URL.rstrip('/')}/verify/{public_token}"
    qr_img = qrcode.make(verify_url)
    qr_path = f"{cert_dir}/{public_token}_qr.png"
    qr_img.save(qr_path)

    # 4. Путь к PDF
    file_path = f"{cert_dir}/{public_token}.pdf"

    # 5. Получаем данные
    student = db.query(models.User).filter(models.User.id == exam.student_id).first()
    course = db.query(models.Course).filter(models.Course.id == exam.course_id).first()

    # 6. Генерация PDF
    c = canvas.Canvas(file_path)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(150, 750, "СЕРТИФИКАТ")

    c.setFont("Helvetica", 14)
    c.drawString(100, 700, "Настоящий сертификат подтверждает, что")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 675, student.fullname)

    c.setFont("Helvetica", 14)
    c.drawString(100, 650, "успешно завершил курс:")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 625, course.title)

    c.drawString(100, 600, f"Дата выдачи: {datetime.utcnow().strftime('%Y-%m-%d')}")

    # 7. Вставка QR в PDF
    qr_img_reader = ImageReader(qr_path)
    c.drawImage(qr_img_reader, 400, 500, width=150, height=150)

    c.save()

    # 8. Сохраняем сертификат в БД
    cert = models.Certificate(
        exam_id=exam.id,
        user_id=exam.student_id,
        course_id=exam.course_id,
        pdf_path=file_path,
        token=public_token,
        serial=f"CERT-{exam.student_id}-{exam.course_id}-{public_token[:8].upper()}",
        issued_at=datetime.utcnow(),
    )
    db.add(cert)
    db.commit()

    return {
        "status": "approved",
        "public_token": public_token,
        "verify_url": verify_url
    }
