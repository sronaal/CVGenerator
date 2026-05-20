from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base, TimestampMixin


class Language(Base, TimestampMixin):
    __tablename__ = "languages"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    language_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), default="intermediate")
