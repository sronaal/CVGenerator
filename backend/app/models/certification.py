from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Certification(Base, TimestampMixin):
    __tablename__ = "certifications"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255))
    issue_date = Column(Date)
    expiry_date = Column(Date)
    credential_url = Column(String(500))

    profile = relationship("Profile", back_populates="certifications")
