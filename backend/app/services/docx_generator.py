import copy
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from typing import Optional

from app.models.profile import Profile
from app.schemas.job_offer import ParsedJobOffer


class DOCXGenerator:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def generate(
        self,
        profile: Profile,
        job_parsed: Optional[ParsedJobOffer],
        output_path: str,
    ):
        doc = Document(self.template_path)

        self._clear_template_content(doc)
        self._fill_header(doc, profile)
        self._fill_education(doc, profile)
        self._fill_experience(doc, profile)
        self._fill_projects(doc, profile)
        self._fill_skills(doc, profile, job_parsed)
        self._fill_languages(doc, profile)

        doc.save(output_path)

    def _clear_template_content(self, doc: Document):
        paragraphs_to_clear = []
        for para in doc.paragraphs:
            text = para.text.strip().lower()
            if not text:
                continue
            if any(marker in text for marker in [
                "harvard university",
                "study abroad",
                "high school",
                "note:",
                "beginning with your most recent",
                "begin each line with an action verb",
                "quantify where possible",
                "do not use personal pronouns",
                "with your next-most recent",
                "this section can be formatted similarly",
                "if this section is more relevant",
                "technical: list computer software",
                "language: list foreign languages",
                "laboratory: list scientific",
                "interests: list activities",
                "experience",
                "leadership & activities",
                "skills & interests",
            ]):
                paragraphs_to_clear.append(para)

        for para in paragraphs_to_clear:
            para.clear()

    def _add_paragraph_with_style(self, doc, text: str, style_name: str):
        para = doc.add_paragraph()
        para.style = doc.styles[style_name]
        run = para.add_run(text)
        return para, run

    def _add_heading(self, doc, text: str):
        para = doc.add_paragraph()
        para.style = doc.styles["Heading 1"]
        run = para.add_run(text)
        run.bold = True
        return para

    def _add_normal_line(self, doc, text: str, bold_prefix: str = ""):
        para = doc.add_paragraph()
        para.style = doc.styles["Normal"]
        if bold_prefix:
            run = para.add_run(bold_prefix)
            run.bold = True
            run = para.add_run(f"\t{text}")
        else:
            run = para.add_run(text)
        return para

    def _add_body_line(self, doc, text: str):
        para = doc.add_paragraph()
        para.style = doc.styles["Body Text"]
        run = para.add_run(text)
        return para

    def _add_bullet(self, doc, text: str):
        para = doc.add_paragraph()
        para.style = doc.styles["List Paragraph"]
        run = para.add_run(text)
        return para

    def _fill_header(self, doc: Document, profile: Profile):
        name_para = doc.paragraphs[0]
        name_para.clear()
        run = name_para.add_run(profile.full_name or "Your Name")
        run.bold = True
        run.font.size = Pt(16)

        contact_line = []
        if profile.location:
            contact_line.append(profile.location)
        if profile.email:
            contact_line.append(profile.email)
        if profile.phone:
            contact_line.append(profile.phone)

        contact_text = " • ".join(contact_line)
        if profile.linkedin_url:
            contact_text += f" • {profile.linkedin_url}"
        if profile.portfolio_url:
            contact_text += f" • {profile.portfolio_url}"

        if len(doc.paragraphs) > 1:
            contact_para = doc.paragraphs[1]
            contact_para.clear()
            run = contact_para.add_run(contact_text)
            run.font.size = Pt(9)

    def _fill_education(self, doc: Document, profile: Profile):
        if not profile.education_entries:
            return

        self._add_heading(doc, "Education")

        for edu in profile.education_entries:
            self._add_normal_line(doc, edu.institution, bold_prefix="")

            details_parts = []
            if edu.degree:
                details_parts.append(edu.degree)
            if edu.field_of_study:
                details_parts.append(edu.field_of_study)
            if edu.gpa:
                details_parts.append(f"GPA: {edu.gpa}")

            details_text = ", ".join(details_parts)
            if edu.start_date or edu.end_date:
                date_parts = []
                if edu.start_date:
                    date_parts.append(edu.start_date.strftime("%b %Y"))
                if edu.end_date:
                    date_parts.append(edu.end_date.strftime("%b %Y"))
                details_text += f"\t{' – '.join(date_parts)}"

            if details_text:
                self._add_body_line(doc, details_text)

            if edu.honors:
                self._add_body_line(doc, f"Honors: {', '.join(edu.honors)}")

    def _fill_experience(self, doc: Document, profile: Profile):
        sorted_exps = sorted(
            profile.experiences,
            key=lambda e: e.start_date or datetime.min.date(),
            reverse=True,
        )

        if not sorted_exps:
            return

        self._add_heading(doc, "Experience")

        for exp in sorted_exps:
            self._add_normal_line(doc, exp.location or "", bold_prefix=exp.company)

            date_str = ""
            if exp.start_date:
                date_str = exp.start_date.strftime("%b %Y")
            date_str += " – "
            if exp.is_current:
                date_str += "Present"
            elif exp.end_date:
                date_str += exp.end_date.strftime("%b %Y")

            self._add_normal_line(doc, date_str, bold_prefix=exp.title)

            if exp.bullets:
                for bullet in exp.bullets:
                    self._add_bullet(doc, bullet)

    def _fill_projects(self, doc: Document, profile: Profile):
        if not profile.projects:
            return

        self._add_heading(doc, "Projects")

        for project in profile.projects:
            self._add_normal_line(doc, "", bold_prefix=project.name)

            if project.technologies:
                self._add_body_line(doc, f"Technologies: {', '.join(project.technologies)}")

            if project.bullets:
                for bullet in project.bullets:
                    self._add_bullet(doc, bullet)
            elif project.description:
                self._add_body_line(doc, project.description)

    def _fill_skills(self, doc: Document, profile: Profile, job_parsed: Optional[ParsedJobOffer]):
        if not profile.skills:
            return

        self._add_heading(doc, "Skills")

        hard_skills = [s for s in profile.skills if s.category == "hard"]
        soft_skills_list = [s for s in profile.skills if s.category == "soft"]
        technical_skills = [s for s in profile.skills if s.category == "technical"]

        all_technical = technical_skills + hard_skills

        if all_technical:
            skill_names = [s.name for s in all_technical]
            self._add_body_line(doc, f"Technical: {', '.join(skill_names)}")

        if soft_skills_list:
            skill_names = [s.name for s in soft_skills_list]
            self._add_body_line(doc, f"Professional: {', '.join(skill_names)}")

    def _fill_languages(self, doc: Document, profile: Profile):
        if not profile.languages:
            return

        lang_entries = [f"{l.language_name} ({l.proficiency})" for l in profile.languages]
        self._add_body_line(doc, f"Languages: {', '.join(lang_entries)}")
