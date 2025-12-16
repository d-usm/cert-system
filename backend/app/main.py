# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, SecuritySchemeType
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, SessionLocal
from . import models
from .security import hash_password
from .routers import admin, auth, certificates, courses, exams, operator, results, verify
Base.metadata.create_all(bind=engine)
bearer_scheme = HTTPBearer()
# Создаем таблицы (на проде лучше Alembic)


#app = FastAPI(title=settings.PROJECT_NAME)
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_extra={
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"BearerAuth": []}],
    }
)
app.include_router(results.router)
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(certificates.router)
app.include_router(operator.router)
app.include_router(exams.router)
app.include_router(admin.router)
app.include_router(verify.router)
app.mount("/certificates", StaticFiles(directory=settings.CERTIFICATES_DIR), name="certificates")
@app.get("/")
def root():
    return {"message": "Certificate System API"}

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://172.16.205.71:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def ensure_default_admin():
    """
    Создаёт дефолтного админа, если в .env заданы ADMIN_EMAIL/ADMIN_PASSWORD.
    Это нужно, чтобы после развертывания можно было войти без ручного добавления
    записи в БД. Если пользователь с таким email уже есть — ничего не делаем.
    """

    if not settings.ADMIN_EMAIL or not settings.ADMIN_PASSWORD:
        return

    with SessionLocal() as db:  # type: Session
        existing = (
            db.query(models.User)
            .filter(models.User.email == settings.ADMIN_EMAIL)
            .first()
        )
        if existing:
            return

        admin_user = models.User(
            fullname=settings.ADMIN_FULLNAME,
            email=settings.ADMIN_EMAIL,
            phone=None,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
        )
        db.add(admin_user)
        db.commit()


ensure_default_admin()
