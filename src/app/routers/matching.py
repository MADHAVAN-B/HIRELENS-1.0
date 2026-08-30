from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Candidate, Job, User
from app.schemas import MatchResponse
from app.services.matching import compute_match

router = APIRouter(prefix="/matching", tags=["matching"])


@router.get("/candidate/{candidate_id}/job/{job_id}", response_model=MatchResponse)
def match_candidate_to_job(candidate_id: int, job_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    match = compute_match(candidate.skills, job.required_skills, candidate.experience_years, job.min_experience_years)
    return {
        "candidate_id": candidate.id,
        "job_id": job.id,
        **match,
    }
