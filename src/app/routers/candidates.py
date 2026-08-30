from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Candidate, User
from app.schemas import CandidateCreate, CandidateOut

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("/", response_model=CandidateOut, status_code=201)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    existing = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Candidate email already exists")
    db_candidate = Candidate(**candidate.model_dump())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.get("/", response_model=list[CandidateOut])
def list_candidates(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Candidate).order_by(Candidate.id.asc()).all()


@router.get("/{candidate_id}", response_model=CandidateOut)
def get_candidate(candidate_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate
