from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from models.question import Base


class UserResult(Base):
    __tablename__ = "user_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String)
    category = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<UserResult(user={self.username}, category='{self.category}', score={self.score})>"  # noqa: E501
