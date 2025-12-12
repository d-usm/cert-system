# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .config import settings
from fastapi.security import HTTPBearer
from fastapi.openapi.models import APIKey, SecuritySchemeType
from .routers import auth, courses, certificates, results
from fastapi.middleware.cors import CORSMiddleware
from .routers import operator
from .routers import auth, courses, certificates, operator, exams, admin, verify
from fastapi.staticfiles import StaticFiles
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
app.mount("/certificates", StaticFiles(directory="certificates"), name="certificates")
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
