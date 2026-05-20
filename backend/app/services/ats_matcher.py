from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.models.skill import Skill
from app.models.experience import Experience
from app.schemas.matching import MatchResult, MatchedSkill
from app.utils.skill_normalizer import normalize_skills_list, find_skill_matches


class ATSMatcher:
    async def compute_match(
        self,
        profile: Profile,
        job_parsed: dict,
        db: AsyncSession,
    ) -> MatchResult:
        result = await db.execute(
            select(Skill).where(Skill.profile_id == profile.id)
        )
        user_skills = result.scalars().all()

        user_skill_names = [s.name for s in user_skills]
        required_skills = job_parsed.get("required_skills", [])
        optional_skills = job_parsed.get("optional_skills", [])
        keywords = job_parsed.get("keywords", [])
        soft_skills = job_parsed.get("soft_skills", [])
        all_required = required_skills + optional_skills + keywords + soft_skills

        all_required_normalized = normalize_skills_list(all_required)
        user_skills_normalized = normalize_skills_list(user_skill_names)

        hard_matches = find_skill_matches(user_skill_names, required_skills + keywords)
        soft_matches = find_skill_matches(user_skill_names, soft_skills)

        hard_total = len(required_skills) + len(keywords)
        hard_matched = sum(1 for m in hard_matches if m["matched"])
        hard_score = int((hard_matched / hard_total * 100)) if hard_total > 0 else 0

        soft_total = len(soft_skills)
        soft_matched = sum(1 for m in soft_matches if m["matched"])
        soft_score = int((soft_matched / soft_total * 100)) if soft_total > 0 else 0

        keyword_total = len(keywords)
        keyword_matched = sum(1 for m in hard_matches if m["matched"] and m["normalized"] in normalize_skills_list(keywords))
        keyword_score = int((keyword_matched / keyword_total * 100)) if keyword_total > 0 else 0

        seniority = job_parsed.get("seniority", "").lower()
        seniority_alignment = self._compute_seniority_alignment(seniority, user_skills)

        overall_score = int(
            hard_score * 0.40
            + soft_score * 0.20
            + keyword_score * 0.25
            + seniority_alignment * 0.15
        )

        matched_skills = []
        missing_skills = []
        for m in hard_matches + soft_matches:
            matched_skills.append(MatchedSkill(
                name=m["name"],
                matched=m["matched"],
                category="soft" if m["normalized"] in normalize_skills_list(soft_skills) else "hard",
            ))
            if not m["matched"]:
                missing_skills.append(m["name"])

        exp_result = await db.execute(
            select(Experience)
            .where(Experience.profile_id == profile.id)
            .order_by(Experience.start_date.desc())
        )
        experiences = exp_result.scalars().all()
        matched_experiences = [e.title for e in experiences[:4]]

        optimization_suggestions = []
        if hard_score < 60:
            optimization_suggestions.append("Consider highlighting transferable skills from existing experience")
        if soft_score < 50:
            optimization_suggestions.append("Add soft skills examples demonstrated through project outcomes")
        if keyword_score < 70:
            optimization_suggestions.append("Incorporate more job-specific keywords into experience descriptions")
        if not optimization_suggestions:
            optimization_suggestions.append("Profile is well-aligned with the job requirements")

        return MatchResult(
            overall_score=overall_score,
            hard_skills_score=hard_score,
            soft_skills_score=soft_score,
            keywords_score=keyword_score,
            seniority_alignment=seniority_alignment,
            matched_skills=matched_skills,
            missing_skills=list(set(missing_skills)),
            matched_experiences=matched_experiences,
            optimization_suggestions=optimization_suggestions,
        )

    def _compute_seniority_alignment(self, required_seniority: str, user_skills: list) -> int:
        seniority_levels = {
            "entry": 1,
            "junior": 1,
            "mid": 2,
            "mid-level": 2,
            "senior": 3,
            "lead": 4,
            "principal": 5,
            "staff": 5,
            "director": 6,
            "vp": 7,
            "c-level": 8,
        }

        required_level = seniority_levels.get(required_seniority.lower(), 2)

        total_years = sum(s.years_of_experience or 0 for s in user_skills)
        avg_years = total_years / len(user_skills) if user_skills else 0

        if avg_years >= 8:
            user_level = 5
        elif avg_years >= 5:
            user_level = 4
        elif avg_years >= 3:
            user_level = 3
        elif avg_years >= 1:
            user_level = 2
        else:
            user_level = 1

        diff = abs(user_level - required_level)
        if diff == 0:
            return 100
        elif diff == 1:
            return 75
        elif diff == 2:
            return 50
        else:
            return 25
