from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "recruiter"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CandidateCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    skills: Optional[str] = None
    experience_years: int = 0


class CandidateOut(CandidateCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class JobCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    required_skills: Optional[str] = None
    min_experience_years: int = 0


class JobOut(JobCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ApplicationCreate(BaseModel):
    candidate_id: int
    job_id: int
    status: str = "submitted"


class ApplicationOut(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: str
    match_score: Optional[float] = None
    feedback: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MatchResponse(BaseModel):
    candidate_id: int
    job_id: int
    match_score: float
    missing_skills: list[str]
    matched_skills: list[str]
    feedback: str
