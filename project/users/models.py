from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from project.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    username = Column(String(128), nullable=False, unique=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    messages = relationship("Message", back_populates="user")
    first_message_id = Column(Integer, nullable=True)
