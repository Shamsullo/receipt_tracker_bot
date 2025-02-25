# app/services/ocr/ocr_service.py
from pathlib import Path
from typing import Dict, Any
import pytesseract
from PIL import Image
import pdfplumber

from app.services.ocr.receipt_parcer import ReceiptParser


# app/services/ocr/exceptions.py
class OCRProcessingError(Exception):
    """Raised when OCR processing fails."""
    pass


class OCRService:
    def __init__(self):
        self.parser = ReceiptParser()

    async def process_document(self, file_path: Path) -> Dict[str, Any]:
        """Process document based on file type."""
        if file_path.suffix.lower() == '.pdf':
            return await self.process_pdf(file_path)
        return await self.process_image(file_path)

    async def process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Extract text from PDF and parse receipt data."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            return self.parser.parse_text(text)
        except Exception as e:
            raise OCRProcessingError(f"Error processing PDF: {str(e)}")

    async def process_image(self, file_path: Path) -> Dict[str, Any]:
        """Extract text from image and parse receipt data."""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(
                image,
                lang='rus+eng'
            )
            return self.parser.parse_text(text)
        except Exception as e:
            raise OCRProcessingError(f"Error processing image: {str(e)}")


    #
    # @staticmethod
    # def _parse_text(text: str) -> dict:
    #     # This is a simplified example - you'll need to adjust patterns
    #     # based on your actual receipt format
    #     date_pattern = r'\d{2}\.\d{2}\.\d{4}'
    #     amount_pattern = r'\d+[\.,]\d{2}'
    #
    #     date_match = re.search(date_pattern, text)
    #     amount_match = re.search(amount_pattern, text)
    #
    #     return {
    #         'date': datetime.strptime(date_match.group(),
    #                                   '%d.%m.%Y') if date_match else None,
    #         'amount': float(amount_match.group().replace(',',
    #                                                      '.')) if amount_match else None,
    #         'raw_text': text
    #     }
