from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.experience import Experience
from app.models.user import User
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/profiles/me/experiences", tags=["experiences"])


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("", response_model=ExperienceOut)
async def create_experience(
    body: ExperienceCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    experience = Experience(profile_id=profile.id, **body.model_dump())
    db.add(experience)
    await db.flush()
    return experience


@router.get("", response_model=list[ExperienceOut])
async def list_experiences(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Experience)
        .where(Experience.profile_id == profile.id)
        .order_by(Experience.start_date.desc())
    )
    return result.scalars().all()


@router.put("/{experience_id}", response_model=ExperienceOut)
async def update_experience(
    experience_id: str,
    body: ExperienceUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Experience).where(Experience.id == experience_id, Experience.profile_id == profile.id)
    )
    experience = result.scalar_one_or_none()
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(experience, key, value)

    await db.flush()
    return experience


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    experience_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Experience).where(Experience.id == experience_id, Experience.profile_id == profile.id)
    )
    experience = result.scalar_one_or_none()
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")

    await db.delete(experience)
    await db.flush()
