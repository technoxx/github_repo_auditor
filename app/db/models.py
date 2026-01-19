from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(),
)



class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repo = Column(String, nullable=False)
    score = Column(Integer)
    grade = Column(String)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="audits")