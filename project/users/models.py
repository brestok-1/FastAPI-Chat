from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from project.users.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    messages = relationship("Message", back_populates='user', cascade="all, delete-orphan")