from sqlalchemy import Column, String, ForeignKey, Text, Boolean, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    technologies = Column(JSONB, default=list)
    url = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    bullets = Column(JSONB, default=list)

    profile = relationship("Profile", back_populates="projects")
