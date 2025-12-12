from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_current_user, require_role
from app.database import get_db
from app.models import CourseResult
from app.schemas import CourseResultCreate
from app.certificates_service import generate_certificate_pdf

router = APIRouter(prefix="/results", tags=["results"])


@router.post("/operator-mark")
def operator_mark(
    data: CourseResultCreate,
    current_user = Depends(require_role("operator", "admin")),
    db: Session = Depends(get_db),
):
    new = CourseResult(
        user_id=data.user_id,
        course_id=data.course_id,
        operator_id=current_user.id,
        status="completed_operator"
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"message": "marked", "result": new}


@router.post("/approve/{result_id}")
def approve_result(
    result_id: int,
    current_user = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    result = db.query(CourseResult).filter(CourseResult.id == result_id).first()

    if not result:
        raise HTTPException(404, "Result not found")

    result.status = "approved"
    db.commit()

    # Генерация сертификата
    cert = generate_certificate_pdf(result.user_id, result.course_id, db)

    result.status = "certificate_issued"
    db.commit()

    return {"message": "approved", "certificate": cert}

