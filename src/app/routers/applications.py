from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Application, Candidate, Job, User
from app.schemas import ApplicationCreate, ApplicationOut

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationOut, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    candidate = db.query(Candidate).filter(Candidate.id == payload.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = db.query(Job).filter(Job.id == payload.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    app_row = Application(**payload.model_dump())
    db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return app_row


@router.get("/", response_model=list[ApplicationOut])
def list_applications(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Application).order_by(Application.id.asc()).all()
