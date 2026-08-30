import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import settings
from app.database import get_db
from app.models import Candidate, Resume, User

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload/{candidate_id}")
def upload_resume(candidate_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    uploads_dir = Path(settings.uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    file_path = uploads_dir / file.filename
    content = file.file.read()
    file_path.write_bytes(content)

    text = content.decode("utf-8", errors="ignore")
    extracted_skills = ", ".join(sorted({token.strip() for token in candidate.skills.split(",") if token.strip()})) if candidate.skills else ""

    resume = Resume(candidate_id=candidate.id, file_name=file.filename, extracted_text=text, extracted_skills=extracted_skills)
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"message": "Resume uploaded successfully", "resume_id": resume.id, "file_name": resume.file_name}


@router.get("/extract-skills/{candidate_id}")
def extract_skills(candidate_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    latest_resume = db.query(Resume).filter(Resume.candidate_id == candidate.id).order_by(Resume.id.desc()).first()
    if not latest_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    skills = [item.strip() for item in (latest_resume.extracted_skills or candidate.skills or "").split(",") if item.strip()]
    return {"candidate_id": candidate.id, "skills": skills}
