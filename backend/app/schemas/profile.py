from pydantic import BaseModel
from typing import Optional


class ProfileCreate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    professional_summary: Optional[str] = None


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    professional_summary: Optional[str] = None


class ProfileOut(BaseModel):
    id: str
    user_id: str
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[str]
    portfolio_url: Optional[str]
    professional_summary: Optional[str]

    model_config = {"from_attributes": True}


class ProfileFullOut(ProfileOut):
    experiences: list = []
    education_entries: list = []
    skills: list = []
    certifications: list = []
    projects: list = []
    languages: list = []
