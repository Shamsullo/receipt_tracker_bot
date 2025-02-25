import pytesseract
from PIL import Image
import pdfplumber
import re

# Function to extract transaction details
def extract_transaction_details(text):
    details = {}

    # Regular expressions for extracting relevant fields
    # Regular expressions to extract key transaction details
    date_match = re.search(
        r"Дата и время[:\s]+(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})", text)
    transaction_id_match = re.search(
        r"(?:Номер операции|Номер транзакции)[:\s]*(\d+)", text)
    amount_match = re.search(r"(?:Сумма операции|Сумма)[:\s]+([\d,.]+)", text)
    sender_match = re.search(
        r"(?:Счет отправителя|Счет зачисления)[:\s]*(\d+)", text)
    status_match = re.search(r"(ИСПОЛНЕНО|Успешный|ОПЕРАЦИЯ ВЫПОЛНЕНА)", text,
                             re.IGNORECASE)
    bank_match = re.search(r"(?:ОАО|ЗАО|АО)\s*«?([А-Яа-яA-Za-z\s]+)»?", text)


    if date_match and date_match:
        details["datetime"] = f"{date_match.group(1)} {date_match.group(1)}"
    if transaction_id_match:
        details["transaction_id"] = transaction_id_match.group(1)
    if amount_match:
        details["amount"] = amount_match.group(1)
    if sender_match:
        details["sender_account"] = sender_match.group(1)
    if status_match:
        details["status"] = status_match.group(1)
    if bank_match:
        details["bank"] = bank_match.group(1)

    return details

# Function to extract text from an image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="rus")  # Russian language support
    return text

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

# Example usage:
image_path = "/Users/shams/Downloads/Telegram/03.02.25_Receipt.pdf"
# image_path = "/Users/shams/Desktop/2025-02-18 22.21.10.jpg"
# text_from_image = extract_text_from_image(image_path)
text_from_pdf = extract_text_from_pdf(image_path)
# transaction_details = extract_transaction_details(text_from_image)
print(text_from_pdf)
transaction_details = extract_transaction_details(text_from_pdf)

# Print extracted details
print(transaction_details)
