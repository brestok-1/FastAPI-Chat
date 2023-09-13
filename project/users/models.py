from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from project.database import Base


class User(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(128), unique=True)
    messages = relationship("Message", back_populates='user', cascade="all, delete-orphan")
