from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.team_service import TeamService
from app.services.user_service import UserService


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Get services from middleware data
        session: AsyncSession = data['session']
        user_service: UserService = data['user_service']
        team_service: TeamService = data['team_service']

        # Skip auth for start command
        if event.text and event.text.startswith('/start'):
            # Ensure user is registered even for start command
            await user_service.get_or_create_user(
                telegram_id=event.from_user.id,
                username=event.from_user.username or "",
                full_name=event.from_user.full_name or ""
            )
            return await handler(event, data)

        # Check if user exists and get their team
        user_team = await team_service.get_user_team(event.from_user.id)

        if not user_team:
            await event.reply(
                "You're not a member of any team. "
                "Create a team with /create_team or ask for invitation."
            )
            return None

        # Add team to handler data for convenience
        data['user_team'] = user_team

        return await handler(event, data)
