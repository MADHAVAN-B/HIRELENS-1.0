from typing import List

try:
    from sentence_transformers import SentenceTransformer
    _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    _MODEL = None


def _split_skills(skills_text: str | None) -> list[str]:
    if not skills_text:
        return []
    return sorted({part.strip().lower() for part in skills_text.split(",") if part.strip()})


def compute_match(candidate_skills: str | None, job_skills: str | None, candidate_exp: int, min_exp: int) -> dict:
    candidate_list = _split_skills(candidate_skills)
    job_list = _split_skills(job_skills)

    matched = sorted(set(candidate_list) & set(job_list))
    missing = sorted(set(job_list) - set(candidate_list))

    overlap_score = (len(matched) / len(job_list) * 100.0) if job_list else 0.0
    exp_bonus = 10.0 if candidate_exp >= min_exp else max(0.0, 10.0 - ((min_exp - candidate_exp) * 5.0))

    semantic_bonus = 0.0
    if _MODEL and candidate_skills and job_skills:
        emb = _MODEL.encode([candidate_skills, job_skills], normalize_embeddings=True)
        semantic_bonus = float((emb[0] @ emb[1]) * 10.0)

    score = round(min(100.0, overlap_score + exp_bonus + semantic_bonus), 2)
    feedback = (
        f"Matched skills: {', '.join(matched) if matched else 'none'}. "
        f"Missing skills: {', '.join(missing) if missing else 'none'}."
    )

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "feedback": feedback,
    }
