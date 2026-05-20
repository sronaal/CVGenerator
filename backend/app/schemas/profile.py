from pydantic import BaseModel, model_validator
from typing import Optional, Any


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

    @model_validator(mode="before")
    @classmethod
    def normalize_relations(cls, data: Any) -> Any:
        if hasattr(data, "experiences"):
            data.experiences = list(data.experiences) if data.experiences else []
        if hasattr(data, "education_entries"):
            data.education_entries = list(data.education_entries) if data.education_entries else []
        if hasattr(data, "skills"):
            data.skills = list(data.skills) if data.skills else []
        if hasattr(data, "certifications"):
            data.certifications = list(data.certifications) if data.certifications else []
        if hasattr(data, "projects"):
            data.projects = list(data.projects) if data.projects else []
        if hasattr(data, "languages"):
            data.languages = list(data.languages) if data.languages else []
        return data
