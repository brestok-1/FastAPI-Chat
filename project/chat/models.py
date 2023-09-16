from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from project.users.database import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User", back_populates="messages")
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(4096), nullable=False)
