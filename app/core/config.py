# app/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str

    # Database settings
    DATABASE_URL: str

    # Storage settings
    UPLOAD_DIR: Path = Path("uploads")

    # Tesseract settings
    TESSERACT_CMD: str = "tesseract"

    class Config:
        env_file = ".env"


settings = Settings()

# Create .env file in root directory:
"""
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://user:password@localhost:5432/payment_bot
TESSERACT_CMD=tesseract
"""