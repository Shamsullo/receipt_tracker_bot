from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, and_
from app.models.team import Team, TeamMember
from app.models.receipt import Receipt
from .base import BaseRepository


class TeamRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Team)

    async def get_user_team(self, user_id: int) -> Optional[Team]:
        stmt = (
            select(Team)
            .join(TeamMember)
            .where(TeamMember.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def is_admin(self, team_id: int, user_id: int) -> bool:
        stmt = select(TeamMember).where(
            and_(
                TeamMember.team_id == team_id,
                TeamMember.user_id == user_id,
                TeamMember.is_admin == True
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def add_member(
            self,
            team_id: int,
            user_id: int,
            is_admin: bool = False
    ) -> TeamMember:
        team_member = TeamMember(
            team_id=team_id,
            user_id=user_id,
            is_admin=is_admin
        )
        self.session.add(team_member)
        await self.session.commit()
        await self.session.refresh(team_member)
        return team_member

    async def get_team_receipts(
            self,
            team_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> List[Receipt]:
        stmt = (
            select(Receipt)
            .where(
                and_(
                    Receipt.team_id == team_id,
                    Receipt.date >= start_date,
                    Receipt.date <= end_date
                )
            )
            .order_by(Receipt.date)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()