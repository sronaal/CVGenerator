import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.models.generated_cv import GeneratedCV
from app.models.user import User
from app.schemas.matching import CVGenerateRequest
from app.schemas.job_offer import ParsedJobOffer
from app.dependencies import get_current_user
from app.services.ats_matcher import ATSMatcher
from app.services.resume_optimizer import ResumeOptimizer
from app.services.docx_generator import DOCXGenerator

router = APIRouter(prefix="/api/v1/generate", tags=["generate"])

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("")
async def generate_cv(
    body: CVGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)

    job_parsed: ParsedJobOffer | None = None
    job_offer = None
    if body.job_offer_id:
        existing_cv = await db.execute(
            select(GeneratedCV).where(
                GeneratedCV.profile_id == profile.id,
                GeneratedCV.job_offer_id == body.job_offer_id,
            ).order_by(GeneratedCV.created_at.desc())
        )
        if existing_cv := existing_cv.scalar_one_or_none():
            return {
                "cv_id": existing_cv.id,
                "file_path": existing_cv.file_path,
                "matching_score": existing_cv.matching_score,
                "message": "CV already generated",
            }

        result = await db.execute(
            select(JobOffer).where(
                JobOffer.id == body.job_offer_id,
                JobOffer.profile_id == profile.id,
            )
        )
        job_offer = result.scalar_one_or_none()
        if not job_offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job offer not found")
        if job_offer.parsed_json:
            job_parsed = ParsedJobOffer(**job_offer.parsed_json)

    if job_parsed:
        matcher = ATSMatcher()
        match_result = await matcher.compute_match(profile, job_offer.parsed_json, db)

        optimizer = ResumeOptimizer()
        optimized_profile = await optimizer.optimize(profile, job_parsed, match_result)
    else:
        optimized_profile = profile

    template_path = Path(__file__).parent.parent.parent.parent / "2025-template_bullet.docx"
    if not template_path.exists():
        raise HTTPException(status_code=status.HTTP_500, detail="CV template not found")

    generator = DOCXGenerator(str(template_path))
    output_filename = f"cv_{profile.id}_{user.id[:8]}.docx"
    output_path = OUTPUT_DIR / output_filename

    generator.generate(optimized_profile, job_parsed, str(output_path))

    generated_cv = GeneratedCV(
        profile_id=profile.id,
        job_offer_id=job_offer.id if job_offer else None,
        matching_score=match_result.overall_score if job_parsed else None,
        file_path=str(output_path),
    )
    db.add(generated_cv)
    await db.flush()

    return {
        "cv_id": generated_cv.id,
        "file_path": str(output_path),
        "matching_score": match_result.overall_score if job_parsed else None,
        "message": "CV generated successfully",
    }


@router.get("/{cv_id}/download")
async def download_cv(
    cv_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(GeneratedCV).where(GeneratedCV.id == cv_id))
    generated_cv = result.scalar_one_or_none()
    if not generated_cv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found")

    file_path = Path(generated_cv.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV file not found on disk")

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/history")
async def get_cv_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(GeneratedCV)
        .where(GeneratedCV.profile_id == profile.id)
        .order_by(GeneratedCV.created_at.desc())
    )
    cvs = result.scalars().all()
    return [
        {
            "id": cv.id,
            "matching_score": cv.matching_score,
            "created_at": cv.created_at,
            "file_path": cv.file_path,
        }
        for cv in cvs
    ]
