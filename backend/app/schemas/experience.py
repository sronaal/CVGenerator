from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExperienceCreate(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    bullets: list[str] = []
    raw_description: Optional[str] = None


class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    bullets: Optional[list[str]] = None
    raw_description: Optional[str] = None


class ExperienceOut(BaseModel):
    id: str
    profile_id: str
    company: str
    title: str
    location: Optional[str]
    start_date: date
    end_date: Optional[date]
    is_current: bool
    bullets: list[str]
    raw_description: Optional[str]

    model_config = {"from_attributes": True}
