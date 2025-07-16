# main.py
import asyncio
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.handlers.team import setup_team_handlers
from app.core.config import settings
from app.core.logging import logger
from app.bot.handlers import base, setup_receipt_handlers
from app.bot.middlewares.auth import AuthMiddleware
from app.services.user_service import UserService
from app.services.receipt_service import ReceiptService
from app.services.team_service import TeamService


async def main():
    logger.info("Starting bot...")

    # Initialize database
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
    )

    # Create session factory
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Initialize services
    user_service = UserService(async_session)
    receipt_service = ReceiptService(async_session,
                                     upload_dir=settings.UPLOAD_DIR)
    team_service = TeamService(async_session)

    # Setup routers
    receipt_router = setup_receipt_handlers(receipt_service, team_service,
                                            settings)
    team_router = setup_team_handlers(team_service)

    # Include all routers
    dp.include_router(base.router)
    dp.include_router(receipt_router)  # Add receipt router
    dp.include_router(team_router)  # Add team router

    # Setup database session middleware
    @dp.update.outer_middleware()
    async def database_middleware(handler, event, data):
        async with async_session() as session:
            data["session"] = session
            data["user_service"] = user_service
            data["receipt_service"] = receipt_service
            data["team_service"] = team_service
            return await handler(event, data)


    # Setup middleware
    dp.update.outer_middleware(AuthMiddleware())

    try:
        # Start polling
        logger.info("Bot started")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())