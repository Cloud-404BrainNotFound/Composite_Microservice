from sqlalchemy import Column, String, Float, Integer, Enum as SQLEnum, DateTime, JSON, Boolean
from app.database import Base
from datetime import datetime
import uuid
import enum

class NotificationType(enum.Enum):
    EMAIL = "email"
    SMS = "sms"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    content = Column(String(1000), nullable=False, default="")
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    extra = Column(JSON, nullable=False, default={})

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    body = Column(String(1000), nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    extra = Column(JSON, nullable=False, default={})