# app/routers/courses.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user, require_role

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=schemas.CourseRead)
def create_course(
    course_in: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin", "teacher")),
):
    course = models.Course(
        title=course_in.title,
        description=course_in.description,
        created_by=current_user.id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/", response_model=List[schemas.CourseRead])
def list_courses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    courses = db.query(models.Course).filter(models.Course.is_active == True).all()
    return courses

