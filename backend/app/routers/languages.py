from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.language import Language
from app.models.user import User
from app.schemas.language import LanguageCreate, LanguageUpdate, LanguageOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/profiles/me/languages", tags=["languages"])


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.unique().scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("", response_model=LanguageOut)
async def create_language(
    body: LanguageCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    lang = Language(profile_id=profile.id, **body.model_dump())
    db.add(lang)
    await db.flush()
    return lang


@router.get("", response_model=list[LanguageOut])
async def list_languages(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Language)
        .where(Language.profile_id == profile.id)
        .order_by(Language.language_name)
    )
    return result.scalars().all()


@router.put("/{language_id}", response_model=LanguageOut)
async def update_language(
    language_id: str,
    body: LanguageUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Language).where(Language.id == language_id, Language.profile_id == profile.id)
    )
    lang = result.scalar_one_or_none()
    if not lang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lang, key, value)

    await db.flush()
    return lang


@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_language(
    language_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Language).where(Language.id == language_id, Language.profile_id == profile.id)
    )
    lang = result.scalar_one_or_none()
    if not lang:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Language not found")

    await db.delete(lang)
    await db.flush()
