# app/schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# --- AUTH / USER ---

class UserBase(BaseModel):
    fullname: str
    email: EmailStr
    phone: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# --- COURSE ---

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int
    created_by: Optional[int]
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


# --- PROGRESS ---

class ProgressUpdate(BaseModel):
    progress: float  # 0–100


class ProgressRead(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress: float
    completed_at: Optional[datetime]
    last_update: datetime

    class Config:
        orm_mode = True


# --- CERTIFICATE ---

class CertificateRead(BaseModel):
    exam_id: int | None = None
    id: int
    user_id: int
    course_id: int
    serial: str
    token: str
    pdf_path: Optional[str]
    issued_at: datetime
    revoked: bool

    class Config:
        from_attributes = True

class CourseResultCreate(BaseModel):
    user_id: int
    course_id: int


class CourseResultRead(BaseModel):
    id: int
    user_id: int
    course_id: int
    operator_id: int | None
    status: str

    class Config:
        from_attributes = True
#--------EXAMS-----------------#
class ExamResultCreate(BaseModel):
    student_id: int
    course_id: int
    is_passed: bool


class ExamResultRead(BaseModel):
    id: int
    student_id: int
    course_id: int
    is_passed: bool
    operator_id: int

    class Config:
        orm_mode = True
class ExamResultAdmin(BaseModel):
    id: int
    student_id: int
    course_id: int
    is_passed: bool
    approved: bool | None
    created_at: datetime
    operator_id: int | None = None

    class Config:
        orm_mode = True

