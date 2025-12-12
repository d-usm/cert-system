# Certificate Management System

## Backend

- Python / FastAPI
- PostgreSQL
- Генерация сертификатов (PDF + QR)
- Роли: admin / operator / student
- Верификация сертификатов по публичному токену

### Запуск backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
uvicorn app.main:app --host 0.0.0.0 --port 8000
