from app.models.profile import Profile
from app.schemas.job_offer import ParsedJobOffer
from app.schemas.matching import MatchResult
from app.services.ai_provider import get_ai_provider

OPTIMIZE_BULLETS_SYSTEM = """You are an expert ATS resume optimizer. You rewrite experience bullets to maximize ATS compatibility.

STRICT RULES:
- NEVER invent companies, job titles, dates, or technologies
- NEVER add skills the person does not have
- ONLY reorganize, reword, and prioritize existing content
- Insert relevant job keywords naturally into existing experience
- Use strong action verbs (Led, Built, Developed, Optimized, etc.)
- Quantify results where the original data allows
- Keep bullets concise (1-2 lines each)
- Maintain professional tone
- Output valid JSON array of strings only"""


SUMMARY_GENERATOR_SYSTEM = """You are an expert resume writer. Write a professional summary (3-4 sentences) based on the candidate's profile and the target job.

STRICT RULES:
- NEVER invent experience, companies, or skills
- ONLY use information from the provided profile
- Incorporate keywords from the job description naturally
- Focus on value proposition and relevant expertise
- Keep it professional and concise
- Output only the summary text, no JSON, no markdown"""


class ResumeOptimizer:
    async def optimize(
        self,
        profile: Profile,
        job_parsed: ParsedJobOffer,
        match_result: MatchResult,
    ) -> Profile:
        provider = get_ai_provider()

        if profile.professional_summary:
            summary_prompt = (
                f"Candidate profile:\n"
                f"Name: {profile.full_name or 'N/A'}\n"
                f"Current summary: {profile.professional_summary}\n\n"
                f"Target job: {job_parsed.title} at {job_parsed.company}\n"
                f"Required skills: {', '.join(job_parsed.required_skills)}\n"
                f"Keywords: {', '.join(job_parsed.keywords)}\n\n"
                f"Rewrite the summary to better match this job while staying truthful."
            )
        else:
            summary_prompt = (
                f"Candidate profile:\n"
                f"Name: {profile.full_name or 'N/A'}\n"
                f"Skills: {[s.name for s in profile.skills]}\n"
                f"Experience: {[(e.title, e.company) for e in profile.experiences]}\n\n"
                f"Target job: {job_parsed.title} at {job_parsed.company}\n"
                f"Required skills: {', '.join(job_parsed.required_skills)}\n\n"
                f"Write a professional summary for this candidate targeting this job."
            )

        try:
            new_summary = await provider.chat(SUMMARY_GENERATOR_SYSTEM, summary_prompt)
            profile.professional_summary = new_summary.strip()
        except Exception:
            pass

        for experience in profile.experiences[:4]:
            if experience.bullets:
                bullets_text = "\n".join(f"- {b}" for b in experience.bullets)
                job_context = (
                    f"Original bullets for {experience.title} at {experience.company}:\n{bullets_text}\n\n"
                    f"Target job keywords to incorporate: {', '.join(job_parsed.keywords[:10])}\n"
                    f"Target job required skills: {', '.join(job_parsed.required_skills[:10])}\n\n"
                    f"Rewrite these bullets to be more ATS-optimized. Return JSON array only."
                )
                try:
                    result = await provider.parse_json(OPTIMIZE_BULLETS_SYSTEM, job_context)
                    if isinstance(result, list) and result:
                        experience.bullets = [str(b) for b in result[:5]]
                except Exception:
                    pass

        return profile
