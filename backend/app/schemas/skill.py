from pydantic import BaseModel
from typing import Optional


class SkillCreate(BaseModel):
    name: str
    category: str = "hard"
    proficiency_level: int = 3
    years_of_experience: Optional[int] = None


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    proficiency_level: Optional[int] = None
    years_of_experience: Optional[int] = None


class SkillOut(BaseModel):
    id: str
    profile_id: str
    name: str
    category: str
    proficiency_level: int
    years_of_experience: Optional[int]

    model_config = {"from_attributes": True}
