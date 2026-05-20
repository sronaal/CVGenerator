from pydantic import BaseModel
from datetime import date
from typing import Optional


class EducationCreate(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    gpa: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    honors: list[str] = []


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    gpa: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    honors: Optional[list[str]] = None


class EducationOut(BaseModel):
    id: str
    profile_id: str
    institution: str
    degree: Optional[str]
    field_of_study: Optional[str]
    gpa: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    honors: list[str]

    model_config = {"from_attributes": True}
