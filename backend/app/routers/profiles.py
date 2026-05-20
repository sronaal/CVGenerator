from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.experience import Experience
from app.models.education import Education
from app.models.skill import Skill
from app.models.certification import Certification
from app.models.project import Project
from app.models.language import Language
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut, ProfileFullOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])


@router.post("", response_model=ProfileOut)
async def create_profile(
    body: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = await db.execute(select(Profile).where(Profile.user_id == user.id))
    if existing.unique().scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists")

    profile = Profile(user_id=user.id, **body.model_dump())
    db.add(profile)
    await db.flush()
    return profile


@router.get("/me", response_model=ProfileFullOut)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.unique().scalar_one_or_none()
    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)
        await db.flush()
        await db.refresh(profile)

    exp_result = await db.execute(select(Experience).where(Experience.profile_id == profile.id))
    edu_result = await db.execute(select(Education).where(Education.profile_id == profile.id))
    skill_result = await db.execute(select(Skill).where(Skill.profile_id == profile.id))
    cert_result = await db.execute(select(Certification).where(Certification.profile_id == profile.id))
    proj_result = await db.execute(select(Project).where(Project.profile_id == profile.id))
    lang_result = await db.execute(select(Language).where(Language.profile_id == profile.id))

    profile.experiences = exp_result.scalars().all()
    profile.education_entries = edu_result.scalars().all()
    profile.skills = skill_result.scalars().all()
    profile.certifications = cert_result.scalars().all()
    profile.projects = proj_result.scalars().all()
    profile.languages = lang_result.scalars().all()

    return profile


@router.put("/me", response_model=ProfileOut)
async def update_profile(
    body: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.unique().scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)

    await db.flush()
    return profile
