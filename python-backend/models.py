from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    picture = Column(String)
    provider = Column(String, default="google")  # google, github
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships (commented out due to database schema issues)
    # interviews = relationship("Interview", back_populates="user")

class Interview(Base):
    __tablename__ = "interview"
    
    id = Column(BigInteger, primary_key=True, index=True)
    job_title = Column(String(255))
    description = Column(Text)
    duration = Column(String(255))
    interview_type = Column(String(255))
    created_by = Column(String(255))
    user_name = Column(String(255))
    questions = Column(Text)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign key (commented out for now due to database schema)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True, default=1)
    
    # Relationships (commented out due to database schema issues)
    # user = relationship("User", back_populates="interviews")
