from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.team import team_members


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)

    # Relationships
    teams = relationship(
        "Team",
        secondary=team_members,
        back_populates="members"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"