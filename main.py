# main.py
import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.handlers.receipt import setup_receipt_handlers
from app.bot.handlers.team import setup_team_handlers
from app.core.logging import logger
from app.bot.middlewares.auth import AuthMiddleware
from app.core.config import settings
from app.services.receipt_service import ReceiptService
from app.services.team_service import TeamService


async def main():
    logger.info("Starting bot...")

    # Initialize database
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # Initialize services
    team_service = TeamService(async_session)

    receipt_service = ReceiptService(async_session, upload_dir=Path(settings.UPLOAD_DIR))

    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register middlewares
    dp.message.middleware(AuthMiddleware())

    # Setup and register handlers
    receipt_router = setup_receipt_handlers(
        receipt_service=receipt_service,
        team_service=team_service,
        settings=settings
    )
    team_router = setup_team_handlers(team_service=team_service)

    # Register routers
    dp.include_router(receipt_router)
    dp.include_router(team_router)

    # Start polling
    try:
        logger.info("Bot started")
        await dp.start_polling(bot)
    finally:
        logger.info("Bot stopped")
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
