from pathlib import Path
import aiofiles
from app.core.config import settings


class FileStorageService:
    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir

    async def save_file(self, file_data: bytes, filename: str) -> Path:
        file_path = self.upload_dir / filename
        self.upload_dir.mkdir(exist_ok=True)

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_data)
        return file_path

    async def get_file_path(self, filename: str) -> Path:
        return self.upload_dir / filename