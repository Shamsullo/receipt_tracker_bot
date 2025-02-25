from typing import Optional, List, Tuple
from datetime import datetime
from app.models.team import Team
from app.models.receipt import Receipt
from app.repositories.team import TeamRepository
from app.repositories.user import UserRepository
from .base import BaseService


class TeamService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.team_repository = TeamRepository(session)
        self.user_repository = UserRepository(session)

    async def create_team(
            self,
            telegram_id: int,
            team_name: str
    ) -> Tuple[Team, str]:
        """Create a new team and add creator as admin."""
        user = await self.user_repository.get_by_telegram_id(telegram_id)
        if not user:
            return None, "User not found"

        # Check if user already in team
        existing_team = await self.team_repository.get_user_team(user.id)
        if existing_team:
            return None, "User already belongs to a team"

        try:
            team = await self.team_repository.create(name=team_name)
            await self.team_repository.add_member(
                team.id,
                user.id,
                is_admin=True
            )
            return team, "Team created successfully"
        except Exception as e:
            return None, f"Failed to create team: {str(e)}"

    async def invite_member(
            self,
            admin_telegram_id: int,
            username: str
    ) -> Tuple[bool, str]:
        """Invite a user to team."""
        admin = await self.user_repository.get_by_telegram_id(
            admin_telegram_id)
        if not admin:
            return False, "Admin not found"

        team = await self.team_repository.get_user_team(admin.id)
        if not team:
            return False, "Admin is not in any team"

        if not await self.team_repository.is_admin(team.id, admin.id):
            return False, "User is not team admin"

        user = await self.user_repository.get_by_username(username)
        if not user:
            return False, "User not found"

        # Check if user already in a team
        existing_team = await self.team_repository.get_user_team(user.id)
        if existing_team:
            return False, "User already belongs to a team"

        try:
            await self.team_repository.add_member(
                team.id,
                user.id,
                is_admin=False
            )
            return True, "User invited successfully"
        except Exception as e:
            return False, f"Failed to invite user: {str(e)}"

    async def get_user_team(
            self,
            telegram_id: int
    ) -> Optional[Team]:
        """Get user's team."""
        user = await self.user_repository.get_by_telegram_id(telegram_id)
        if not user:
            return None
        return await self.team_repository.get_user_team(user.id)

    async def get_team_receipts(
            self,
            team_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> List[Receipt]:
        """Get team receipts for date range."""
        return await self.team_repository.get_team_receipts(
            team_id,
            start_date,
            end_date
        )

    async def is_team_admin(
            self,
            telegram_id: int,
            team_id: int
    ) -> bool:
        """Check if user is team admin."""
        user = await self.user_repository.get_by_telegram_id(telegram_id)
        if not user:
            return False
        return await self.team_repository.is_admin(team_id, user.id)