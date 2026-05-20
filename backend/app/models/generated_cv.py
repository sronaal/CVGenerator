from sqlalchemy import Column, String, ForeignKey, Integer
from app.models.base import Base, TimestampMixin


class GeneratedCV(Base, TimestampMixin):
    __tablename__ = "generated_cvs"

    profile_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    job_offer_id = Column(String, ForeignKey("job_offers.id"), nullable=True)
    matching_score = Column(Integer)
    file_path = Column(String(500))
