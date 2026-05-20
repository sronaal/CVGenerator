from pydantic import BaseModel
from datetime import date
from typing import Optional


class CertificationCreate(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_url: Optional[str] = None


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_url: Optional[str] = None


class CertificationOut(BaseModel):
    id: str
    profile_id: str
    name: str
    issuing_organization: Optional[str]
    issue_date: Optional[date]
    expiry_date: Optional[date]
    credential_url: Optional[str]

    model_config = {"from_attributes": True}
