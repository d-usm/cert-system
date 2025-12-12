from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user, require_role

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("/record", response_model=schemas.ExamResultRead)
def record_exam(
    data: schemas.ExamResultCreate,
    db: Session = Depends(get_db),
    operator=Depends(require_role("operator")),
):
    student = db.query(models.User).filter(models.User.id == data.student_id).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(models.Course).filter(models.Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    exam = models.ExamResult(
    student_id=data.student_id,
    course_id=data.course_id,
    is_passed=data.is_passed,
    operator_id=operator.id
)

    db.add(exam)
    db.commit()
    db.refresh(exam)

    return exam

