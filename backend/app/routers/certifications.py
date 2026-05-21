from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.profile import Profile
from app.models.certification import Certification
from app.models.user import User
from app.schemas.certification import CertificationCreate, CertificationUpdate, CertificationOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/profiles/me/certifications", tags=["certifications"])


async def _get_profile(db: AsyncSession, user: User) -> Profile:
    result = await db.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.unique().scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("", response_model=CertificationOut)
async def create_certification(
    body: CertificationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    cert = Certification(profile_id=profile.id, **body.model_dump())
    db.add(cert)
    await db.flush()
    return cert


@router.get("", response_model=list[CertificationOut])
async def list_certifications(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Certification)
        .where(Certification.profile_id == profile.id)
        .order_by(Certification.issue_date.desc().nulls_last())
    )
    return result.scalars().all()


@router.put("/{certification_id}", response_model=CertificationOut)
async def update_certification(
    certification_id: str,
    body: CertificationUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Certification).where(
            Certification.id == certification_id,
            Certification.profile_id == profile.id,
        )
    )
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cert, key, value)

    await db.flush()
    return cert


@router.delete("/{certification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certification(
    certification_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    profile = await _get_profile(db, user)
    result = await db.execute(
        select(Certification).where(
            Certification.id == certification_id,
            Certification.profile_id == profile.id,
        )
    )
    cert = result.scalar_one_or_none()
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")

    await db.delete(cert)
    await db.flush()
