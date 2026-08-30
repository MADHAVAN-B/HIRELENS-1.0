from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Job, User
from app.schemas import JobCreate, JobOut

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobOut, status_code=201)
def create_job(job: JobCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    db_job = Job(**job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Job).order_by(Job.id.asc()).all()


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
