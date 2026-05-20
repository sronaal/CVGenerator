from sqlalchemy import Column, String, ForeignKey, Integer
from app.models.base import Base, TimestampMixin


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), default="hard")
    proficiency_level = Column(Integer, default=3)
    years_of_experience = Column(Integer)
