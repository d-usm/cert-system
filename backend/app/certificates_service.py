import os
from fpdf import FPDF
from datetime import datetime
from uuid import uuid4
from app.models import Certificate, User, Course


CERT_DIR = "certificates"

os.makedirs(CERT_DIR, exist_ok=True)


def generate_certificate_pdf(user_id, course_id, db):
    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()

    token = uuid4().hex

    # создаём запись сертификата в БД
    cert = Certificate(
        user_id=user_id,
        course_id=course_id,
        token=token,
        serial=f"CERT-{user_id}-{course_id}-{token[:6]}",
        issued_at=datetime.utcnow(),
        pdf_path=None
    )

    db.add(cert)
    db.commit()
    db.refresh(cert)

    # путь к PDF
    pdf_path = f"{CERT_DIR}/{cert.id}.pdf"

    # генерируем PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt="Certificate of Completion", ln=True, align="C")

    pdf.set_font("Arial", size=14)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Awarded to: {user.fullname}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"For completing course: {course.title}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Serial: {cert.serial}", ln=True, align="C")

    pdf.output(pdf_path)

    cert.pdf_path = pdf_path
    db.commit()

    return cert

