from typing import Optional
from sqlalchemy import select
from app.models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, User)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_from_telegram(
            self,
            telegram_id: int,
            username: str,
            full_name: str
    ) -> User:
        user = await self.create(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name
        )
        return user