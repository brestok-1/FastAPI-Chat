from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from project.database import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User", back_populates="messages")
    username = Column(String(128), ForeignKey("users.username"))
    text = Column(String(4096), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
