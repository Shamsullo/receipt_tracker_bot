# app/db/models_old.py
import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, \
    Numeric, \
    Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

team_members = Table(
    'team_members',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('is_admin', Boolean, default=False)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    teams = relationship("Team", secondary=team_members,
                         back_populates="members")


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    members = relationship("User", secondary=team_members,
                           back_populates="teams")
    receipts = relationship("Receipt", back_populates="team")


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    uploaded_by = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)
    amount = Column(Numeric(10, 2))
    operation_number = Column(String)
    sender = Column(String)
    receiver = Column(String)
    status = Column(String)
    file_path = Column(String)
    creation_at = Column(DateTime,  default=lambda: datetime.utcnow())
    notes = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    fee = Column(Numeric(10, 2), nullable=True)

    team = relationship("Team", back_populates="receipts")
