# HireLens

HireLens is a FastAPI-based resume analysis and job matching platform. It supports JWT authentication, candidate and job management, resume uploads, and AI-assisted matching using SentenceTransformers.

## Features

- JWT-based authentication and protected endpoints
- Candidate, job, and application CRUD flows
- Resume upload and simple extracted-skills endpoint
- Semantic job matching with SentenceTransformers fallback logic
- PostgreSQL-ready schema with Dockerized database

## Project structure

```text
hirelens/
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── src/
│   └── app/
└── tests/
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
docker compose up -d
```

### 3. Run the API

```bash
cd src
uvicorn app.main:app --reload
```

The docs will be available at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Default flow

1. Register a recruiter at `POST /auth/register`
2. Get token from `POST /auth/token`
3. Create candidate at `POST /candidates/`
4. Create job at `POST /jobs/`
5. Create application at `POST /applications/`
6. Match candidate to job at `GET /matching/candidate/{candidate_id}/job/{job_id}`

## Environment variables

Create a `.env` file if you want custom settings:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/hirelens
SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
UPLOADS_DIR=uploads
```

## Run tests

```bash
pytest -q
```

## Resume bullets

- Built a resume analysis platform that extracts skills and keywords from uploaded resumes using NLP-based parsing.
- Developed REST APIs with FastAPI covering authentication, resume uploads, profile management, and job-matching workflows.
- Implemented semantic similarity matching using SentenceTransformers to compare resumes against job descriptions and generate match scores.
- Designed normalized PostgreSQL schemas for candidate profiles, resumes, job postings and application workflows.
- Secured all endpoints using JWT-based authentication and role-based access control.
- Containerized the application with Docker for reproducible local development and deployment.
