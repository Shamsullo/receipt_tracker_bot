from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class ReceiptServiceInterface(ABC):
    @abstractmethod
    async def save_file(self, file_data: bytes, filename: str) -> Path:
        pass

    @abstractmethod
    async def process_receipt(
            self,
            team_id: int,
            user_id: int,
            file_data: bytes,
            filename: str
    ) -> Dict[str, Any]:
        pass