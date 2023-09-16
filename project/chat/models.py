from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from project.users.database import Base


class Message(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User", back_populates='bookmarks')
    text = Column(String(4096), nullable=False)