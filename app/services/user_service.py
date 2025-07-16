# app/services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.models.user import User
from app.core.logging import logger


class UserService:
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def get_or_create_user(
            self,
            user_id: int,
            username: str | None,
            first_name: str | None,
            last_name: str | None
    ) -> User:
        async with self.session_factory() as session:
            repository = UserRepository(session)
            user = await repository.get_by_telegram_id(user_id)

            if not user:
                user = await repository.create(
                    telegram_id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                await session.commit()
                logger.info(f"Created new user: {user_id}")

            return user

    async def get_user(self, user_id: int) -> User | None:
        async with self.session_factory() as session:
            repository = UserRepository(session)
            return await repository.get_by_telegram_id(user_id)
