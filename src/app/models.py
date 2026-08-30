from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="recruiter")
    created_at = Column(DateTime, default=datetime.utcnow)


class Candidate(Base):
    __tablename__ = "candidates"
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    resume_url = Column(String(500), nullable=True)
    skills = Column(Text, nullable=True)
    experience_years = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("app.candidates.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=True)
    extracted_skills = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="resumes")


class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    required_skills = Column(Text, nullable=True)
    min_experience_years = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = {"schema": "app"}

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("app.candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("app.jobs.id"), nullable=False)
    status = Column(String(50), nullable=False, default="submitted")
    match_score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="applications")
    job = relationship("Job", back_populates="applications")
