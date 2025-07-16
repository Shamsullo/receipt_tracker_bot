# app/bot/middlewares/auth.py
from typing import Dict, Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.core.logging import logger


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        try:
            # Get session and user service from data
            user_service: UserService = data['user_service']

            # Get user info from the event
            if isinstance(event, Message):
                user = event.from_user
            elif isinstance(event, CallbackQuery):
                user = event.from_user
            else:
                return await handler(event, data)

            # Check and register user if needed
            telegram_user = await user_service.get_or_create_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )

            # Add user to data dict for handlers
            data['user'] = telegram_user

            return await handler(event, data)

        except Exception as e:
            logger.error(f"Error in auth middleware: {e}")
            raise  e

            if isinstance(event, Message):
                await event.answer(
                    "Sorry, something went wrong. Please try again later.")
            return None
