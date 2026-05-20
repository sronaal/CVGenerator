from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: list[str] = []
    url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    bullets: list[str] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[list[str]] = None
    url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    bullets: Optional[list[str]] = None


class ProjectOut(BaseModel):
    id: str
    profile_id: str
    name: str
    description: Optional[str]
    technologies: list[str]
    url: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    is_current: bool
    bullets: list[str]

    model_config = {"from_attributes": True}
