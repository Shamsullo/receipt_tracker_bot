# app/bot/handlers/__init__.py
from app.bot.handlers import base
from app.bot.handlers.receipt import setup_receipt_handlers

__all__ = ['base', 'setup_receipt_handlers']