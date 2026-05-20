from pydantic import BaseModel


class MatchAnalysisRequest(BaseModel):
    job_offer_id: str


class MatchedSkill(BaseModel):
    name: str
    matched: bool
    category: str


class MatchResult(BaseModel):
    overall_score: int
    hard_skills_score: int
    soft_skills_score: int
    keywords_score: int
    seniority_alignment: int
    matched_skills: list[MatchedSkill]
    missing_skills: list[str]
    matched_experiences: list[str]
    optimization_suggestions: list[str]


class CVGenerateRequest(BaseModel):
    job_offer_id: str | None = None
