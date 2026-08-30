# HireLens

HireLens is a recruitment backend API built with FastAPI. It supports user authentication, candidate management, job posting, applications, and candidate-job matching.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Docker
- Pytest

## Features
- User registration and login
- JWT-based authentication
- Create and manage candidates
- Create and manage jobs
- Submit job applications
- Candidate-job matching endpoint
- Automated tests

## Run Locally
```powershell
docker compose up -d
cd src
uvicorn app.main:app --reload
```

## API Docs
Open: `http://127.0.0.1:8000/docs`

## Run Tests
```powershell
pytest -q
```

## Status
Backend working, tests passing.