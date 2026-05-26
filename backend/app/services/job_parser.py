from app.schemas.job_offer import ParsedJobOffer
from app.services.ai_provider import get_ai_provider
from app.services.cache import AICache
from app.utils.text_cleaner import clean_text

JOB_PARSER_SYSTEM = """You are an expert job offer analyzer. Extract structured information from job descriptions.

Rules:
- Extract only what is explicitly stated or clearly implied
- Never invent information

Return valid JSON matching this exact schema:
{
  "title": "Software Engineer",
  "company": "Google",
  "seniority": "senior",
  "required_skills": ["Python", "React"],
  "optional_skills": ["AWS"],
  "keywords": ["microservices", "distributed systems"],
  "responsibilities": ["Build APIs", "Lead team"],
  "soft_skills": ["communication", "leadership"]
}

Use empty string "" for missing text fields, empty list [] for missing array fields."""


async def parse_job_offer_with_ai(raw_text: str) -> ParsedJobOffer:
    cache = AICache()
    cleaned = clean_text(raw_text)

    cached_result = await cache.get_parse(cleaned)
    if cached_result is not None:
        return ParsedJobOffer(**cached_result)

    provider = get_ai_provider()
    user_prompt = f"Analyze this job offer and return structured JSON:\n\n{cleaned}"

    result = await provider.parse_json(JOB_PARSER_SYSTEM, user_prompt)

    parsed = ParsedJobOffer(
        title=result.get("title", ""),
        company=result.get("company", ""),
        seniority=result.get("seniority", ""),
        required_skills=result.get("required_skills", []),
        optional_skills=result.get("optional_skills", []),
        keywords=result.get("keywords", []),
        responsibilities=result.get("responsibilities", []),
        soft_skills=result.get("soft_skills", []),
    )

    await cache.set_parse(cleaned, parsed.model_dump())
    return parsed
