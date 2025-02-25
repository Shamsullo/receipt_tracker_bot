from typing import Optional
from app.models.user import User
from app.repositories.user import UserRepository
from .base import BaseService


class UserService(BaseService):
    def __init__(self, session):
        super().__init__(session)
        self.user_repository = UserRepository(session)

    async def get_or_create_user(
            self,
            telegram_id: int,
            username: str,
            full_name: str
    ) -> User:
        """Get existing user or create new one from Telegram data."""
        user = await self.user_repository.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.user_repository.create_from_telegram(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name
            )
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID."""
        return await self.user_repository.get_by_telegram_id(telegram_id)

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return await self.user_repository.get_by_username(username)

    async def update_user_info(
            self,
            telegram_id: int,
            username: str,
            full_name: str
    ) -> Optional[User]:
        """Update user information."""
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return await self.user_repository.update(
                user.id,
                username=username,
                full_name=full_name
            )
        return None