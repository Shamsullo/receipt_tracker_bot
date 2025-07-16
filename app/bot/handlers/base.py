# app/bot/handlers/base.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from app.core.logging import logger

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    try:
        await message.answer(
            "👋 Welcome! I'm your receipt management bot.\n\n"
            "Here's what I can do:\n"
            "/upload_receipt - Upload a new receipt\n"
            "/list_receipts - View your receipts\n"
            "/help - Show available commands"
        )
        logger.info(f"User {message.from_user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.answer(
            "Sorry, something went wrong. Please try again later.")