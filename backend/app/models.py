# app/models.py
from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, ForeignKey, Text, Float, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="student")  # admin, teacher, student
    ldap_uid = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    courses_created = relationship("Course", back_populates="creator")
    progresses = relationship("CourseProgress", back_populates="user")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    creator = relationship("User", back_populates="courses_created")
    progresses = relationship("CourseProgress", back_populates="course")


class CourseProgress(Base):
    __tablename__ = "course_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    progress = Column(Float, default=0.0)  # 0–100
    completed_at = Column(DateTime, nullable=True)
    last_update = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progresses")
    course = relationship("Course", back_populates="progresses")

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_user_course"),
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exam_results.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    public_token = Column(String, unique=True, index=True)
class CourseResult(Base):
    __tablename__ = "course_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(String, default="pending")  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id])
    course = relationship("Course", foreign_keys=[course_id])
    operator = relationship("User", foreign_keys=[operator_id])
  
class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    is_passed = Column(Boolean, default=False)
    approved = Column(Boolean, default=None)

    operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

