from app.schemas.job_offer import ParsedJobOffer
from app.services.ai_provider import get_ai_provider

JOB_PARSER_SYSTEM = """You are an expert job offer analyzer. Your task is to extract structured information from job descriptions.

Rules:
- Extract only what is explicitly stated or clearly implied
- Identify hard skills (technical skills, tools, frameworks, languages)
- Identify soft skills (communication, leadership, teamwork, etc.)
- Determine seniority level (entry, mid, senior, lead, principal, etc.)
- Extract keywords that ATS systems would look for
- List main responsibilities
- Separate required skills from optional/nice-to-have skills

Respond with valid JSON matching the exact schema provided."""


async def parse_job_offer_with_ai(raw_text: str) -> ParsedJobOffer:
    provider = get_ai_provider()

    user_prompt = f"Analyze this job offer and return structured JSON:\n\n{raw_text}"

    result = await provider.parse_json(JOB_PARSER_SYSTEM, user_prompt)

    return ParsedJobOffer(
        title=result.get("title", ""),
        company=result.get("company", ""),
        seniority=result.get("seniority", ""),
        required_skills=result.get("required_skills", []),
        optional_skills=result.get("optional_skills", []),
        keywords=result.get("keywords", []),
        responsibilities=result.get("responsibilities", []),
        soft_skills=result.get("soft_skills", []),
    )
