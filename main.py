import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import Settings
from app.db.operations import DatabaseManager
from app.services.receipt_processor import ReceiptProcessor
from app.bot.handlers.team import register_team_handlers
from app.bot.handlers.receipt import register_receipt_handlers
from app.bot.middlewares.auth import AuthMiddleware

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Start the bot"),
        types.BotCommand(command="create_team",
                         description="Create a new team"),
        types.BotCommand(command="invite", description="Invite user to team"),
        types.BotCommand(command="upload_receipt",
                         description="Upload a receipt"),
        types.BotCommand(command="list_receipts",
                         description="List team receipts"),
        types.BotCommand(command="help", description="Show help message"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Load settings
    settings = Settings()

    # Initialize database
    db = DatabaseManager(settings.DATABASE_URL)
    await db.init_db()

    # Initialize services
    receipt_processor = ReceiptProcessor(db, settings.UPLOAD_DIR)

    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Create main router
    main_router = Router()

    # Register middleware
    main_router.message.middleware(AuthMiddleware(db))

    # Register handlers
    register_team_handlers(main_router, db)
    register_receipt_handlers(main_router, db, receipt_processor, settings)

    # Include router in dispatcher
    dp.include_router(main_router)

    # Set up command descriptions
    await set_commands(bot)

    # Start polling
    try:
        logger.info("Bot started")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())