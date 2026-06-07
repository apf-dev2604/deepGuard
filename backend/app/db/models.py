from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="viewer", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    scans = relationship("Scan", back_populates="user")

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    original_filename = Column(String(500), nullable=False)
    stored_filename = Column(String(500), nullable=False)
    file_path = Column(Text, nullable=False)
    file_type = Column(String(100), nullable=False)
    modality = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    prediction = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=True)
    report_path = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="scans")
