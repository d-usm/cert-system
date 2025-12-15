# Certificate Management System

## Backend

- Python / FastAPI
- PostgreSQL
- Генерация сертификатов (PDF + QR)
- Роли: admin / operator / student
- Верификация сертификатов по публичному токену

### Запуск backend

1. Скопируйте файл окружения:

```bash
cp backend/.env.example backend/.env
```

и при необходимости обновите значения `DATABASE_URL`, `JWT_SECRET_KEY`, `PUBLIC_BASE_URL` и `CERTIFICATES_DIR`.

2. Установите зависимости и запустите сервер:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
uvicorn app.main:app --host 0.0.0.0 --port 8000
