from pydantic import BaseModel
from typing import Optional


class LanguageCreate(BaseModel):
    language_name: str
    proficiency: str = "intermediate"


class LanguageUpdate(BaseModel):
    language_name: Optional[str] = None
    proficiency: Optional[str] = None


class LanguageOut(BaseModel):
    id: str
    profile_id: str
    language_name: str
    proficiency: str

    model_config = {"from_attributes": True}
