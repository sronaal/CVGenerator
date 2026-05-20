from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"

    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    location = Column(String(255))
    linkedin_url = Column(String(500))
    portfolio_url = Column(String(500))
    professional_summary = Column(Text)

    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    education_entries = relationship("Education", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    languages = relationship("Language", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    job_offers = relationship("JobOffer", back_populates="profile", cascade="all, delete-orphan", lazy=False)
    generated_cvs = relationship("GeneratedCV", back_populates="profile", cascade="all, delete-orphan", lazy=False)
