from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import require_role
from .. import models, schemas
import os
from reportlab.pdfgen import canvas
from datetime import datetime
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import secrets
import os
from datetime import datetime
from ..database import get_db
from .. import models

router = APIRouter(prefix="/admin", tags=["admin"])


# 1. Получить список экзаменов, ожидающих утверждения
@router.get("/pending-exams")
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
    certs = db.query(models.Certificate).all()
    output = []

    for cert in certs:
        student = db.query(models.User).filter(models.User.id == cert.student_id).first()
        course = db.query(models.Course).filter(models.Course.id == cert.course_id).first()

        output.append({
            "id": cert.id,
            "fullname": student.fullname,
            "email": student.email,
            "course": course.title,
            "date": cert.created_at.strftime("%Y-%m-%d"),
            "pdf_url": f"/{cert.file_path}",
            "public_token": cert.public_token
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

    # отметили как утвержденный
    exam.approved = True
    db.commit()

    # 1. Генерируем уникальный токен
    public_token = secrets.token_urlsafe(32)

    # 2. Папка для сертификатов
    cert_dir = "certificates"
    os.makedirs(cert_dir, exist_ok=True)

    # 3. QR-код
    verify_url = f"http://172.16.205.71:8000/verify/{public_token}"
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
        student_id=exam.student_id,
        course_id=exam.course_id,
        file_path=file_path,
        public_token=public_token,
    )
    db.add(cert)
    db.commit()

    return {
        "status": "approved",
        "public_token": public_token,
        "verify_url": verify_url
    }
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

