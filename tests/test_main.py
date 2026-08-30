import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.auth import get_password_hash
from app.database import Base, get_db
from app.main import app
from app.models import User

engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
    execution_options={"schema_translate_map": {"app": None}},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_module():
    db = TestingSessionLocal()
    if not db.query(User).filter(User.email == "test@example.com").first():
        db.add(User(email="test@example.com", hashed_password=get_password_hash("test1234"), role="recruiter"))
        db.commit()
    db.close()


def get_token():
    response = client.post("/auth/token", data={"username": "test@example.com", "password": "test1234"})
    return response.json()["access_token"]


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health/db")
    assert response.status_code == 200


def test_candidate_job_application_flow():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    candidate = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "Aarav Sharma",
            "email": "aarav@example.com",
            "phone": "9999999999",
            "resume_url": "https://example.com/resume.pdf",
            "skills": "Python, FastAPI, PostgreSQL",
            "experience_years": 3,
        },
    )
    assert candidate.status_code == 201
    candidate_id = candidate.json()["id"]

    job = client.post(
        "/jobs/",
        headers=headers,
        json={
            "title": "Backend Developer",
            "description": "Build APIs",
            "location": "Remote",
            "required_skills": "Python, FastAPI, Docker",
            "min_experience_years": 2,
        },
    )
    assert job.status_code == 201
    job_id = job.json()["id"]

    application = client.post(
        "/applications/",
        headers=headers,
        json={"candidate_id": candidate_id, "job_id": job_id, "status": "submitted"},
    )
    assert application.status_code == 201

    match = client.get(f"/matching/candidate/{candidate_id}/job/{job_id}", headers=headers)
    assert match.status_code == 200
    assert "match_score" in match.json()
