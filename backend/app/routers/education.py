from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.education import Education
from app.models.user import User
from app.schemas.education import EducationCreate, EducationUpdate, EducationOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/profiles/me/education", tags=["education"])


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("", response_model=EducationOut)
async def create_education(
    body: EducationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    entry = Education(profile_id=profile.id, **body.model_dump())
    db.add(entry)
    await db.flush()
    return entry


@router.get("", response_model=list[EducationOut])
async def list_education(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Education)
        .where(Education.profile_id == profile.id)
        .order_by(Education.end_date.desc().nulls_last())
    )
    return result.scalars().all()


@router.put("/{education_id}", response_model=EducationOut)
async def update_education(
    education_id: str,
    body: EducationUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Education).where(Education.id == education_id, Education.profile_id == profile.id)
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(entry, key, value)

    await db.flush()
    return entry


@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    education_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Education).where(Education.id == education_id, Education.profile_id == profile.id)
    )
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")

    await db.delete(entry)
    await db.flush()
