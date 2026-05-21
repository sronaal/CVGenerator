from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.models.user import User
from app.schemas.matching import MatchAnalysisRequest, MatchResult
from app.dependencies import get_current_user
from app.services.ats_matcher import ATSMatcher

router = APIRouter(prefix="/api/v1/matching", tags=["matching"])


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.unique().scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("/analyze", response_model=MatchResult)
async def analyze_match(
    body: MatchAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)

    result = await db.execute(
        select(JobOffer).where(
            JobOffer.id == body.job_offer_id,
            JobOffer.profile_id == profile.id,
        )
    )
    job_offer = result.scalar_one_or_none()
    if not job_offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job offer not found")

    if not job_offer.parsed_json:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job offer not parsed yet")

    matcher = ATSMatcher()
    match_result = await matcher.compute_match(profile, job_offer.parsed_json, db)
    return match_result
