from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Education(Base, TimestampMixin):
    __tablename__ = "education"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255))
    field_of_study = Column(String(255))
    gpa = Column(String(20))
    start_date = Column(Date)
    end_date = Column(Date)
    honors = Column(JSONB, default=list)

    profile = relationship("Profile", back_populates="education_entries")
