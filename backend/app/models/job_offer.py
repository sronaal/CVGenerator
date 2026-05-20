from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class JobOffer(Base, TimestampMixin):
    __tablename__ = "job_offers"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    parsed_json = Column(JSONB)
    title = Column(String(255))
    company = Column(String(255))
    seniority = Column(String(50))

    profile = relationship("Profile", back_populates="job_offers")
