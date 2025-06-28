import logging
import asyncio

from pypdf import PdfReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def extract_pdf_text(file_path: str):
    logger.info('Extracting text from PDF with filename: %s', file_path)

    reader = await asyncio.to_thread(PdfReader, file_path)
    page_count = len(reader.pages)
    all_text = ""

    for i in range(page_count):
        page = reader.pages[i]
        text = await asyncio.to_thread(page.extract_text)
        all_text += text or ""

    logger.info('Successfully extracted text from PDF with filename: %s', file_path)
    return all_text
