from pydantic import BaseModel
from typing import Optional


class JobOfferParseRequest(BaseModel):
    raw_text: str


class JobOfferOut(BaseModel):
    id: str
    profile_id: str
    raw_text: str
    title: Optional[str]
    company: Optional[str]
    seniority: Optional[str]
    parsed_json: Optional[dict]

    model_config = {"from_attributes": True}


class ParsedJobOffer(BaseModel):
    title: str = ""
    company: str = ""
    seniority: str = ""
    required_skills: list[str] = []
    optional_skills: list[str] = []
    keywords: list[str] = []
    responsibilities: list[str] = []
    soft_skills: list[str] = []
