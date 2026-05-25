from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.job_offer import JobOffer
from app.models.user import User
from app.schemas.job_offer import JobOfferParseRequest, JobOfferOut, ParsedJobOffer
from app.dependencies import get_current_user
from app.services.job_parser import parse_job_offer_with_ai

router = APIRouter(prefix="/api/v1/job-offers", tags=["job-offers"])


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("/parse", response_model=JobOfferOut)
async def parse_job_offer(
    body: JobOfferParseRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)

    existing = await db.execute(
        select(JobOffer).where(
            JobOffer.profile_id == profile.id,
            JobOffer.raw_text == body.raw_text,
        )
    )
    existing_offer = existing.scalar_one_or_none()
    if existing_offer:
        return existing_offer

    parsed: ParsedJobOffer = await parse_job_offer_with_ai(body.raw_text)

    job_offer = JobOffer(
        profile_id=profile.id,
        raw_text=body.raw_text,
        parsed_json=parsed.model_dump(),
        title=parsed.title,
        company=parsed.company,
        seniority=parsed.seniority,
    )
    db.add(job_offer)
    await db.flush()
    return job_offer


@router.get("", response_model=list[JobOfferOut])
async def list_job_offers(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(JobOffer)
        .where(JobOffer.profile_id == profile.id)
        .order_by(JobOffer.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{job_offer_id}", response_model=JobOfferOut)
async def get_job_offer(
    job_offer_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(JobOffer).where(
            JobOffer.id == job_offer_id,
            JobOffer.profile_id == profile.id,
        )
    )
    job_offer = result.scalar_one_or_none()
    if not job_offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job offer not found")
    return job_offer


@router.delete("/{job_offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_offer(
    job_offer_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(JobOffer).where(
            JobOffer.id == job_offer_id,
            JobOffer.profile_id == profile.id,
        )
    )
    job_offer = result.scalar_one_or_none()
    if not job_offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job offer not found")

    await db.delete(job_offer)
    await db.flush()
