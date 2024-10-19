from sqlalchemy import Column, String, Float, Integer, Enum as SQLEnum, DateTime, JSON
from app.database import Base
from datetime import datetime
import uuid
import enum

class ReviewStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class ReviewType(enum.Enum):
    PRODUCT = "product"
    STORE = "store"
    SERVICE = "service"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    review_type = Column(SQLEnum(ReviewType), nullable=False)
    target_id = Column(String(36), nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String(1000), nullable=False, default="")
    status = Column(SQLEnum(ReviewStatus), nullable=False, default=ReviewStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.utcnow)
    extra = Column(JSON, nullable=False, default=dict)

class ReviewSummary(Base):
    __tablename__ = "review_summaries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target_id = Column(String(36), nullable=False)
    review_type = Column(SQLEnum(ReviewType), nullable=False)
    average_rating = Column(Float, nullable=False, default=0.0)
    total_reviews = Column(Integer, nullable=False, default=0)
    rating_distribution = Column(JSON, nullable=False, default=dict)
    extra = Column(JSON, nullable=False, default=dict)