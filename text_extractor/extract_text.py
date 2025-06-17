import logging
from pypdf import PdfReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fileNamePath = r"C:\Users\mercy\Downloads\Cv George Enike 1.pdf"

logger.info('Extracting text from PDF with filename: %s', fileNamePath)

reader = PdfReader(fileNamePath)
pageNumber = len(reader.pages)
text = ""

for i in range(pageNumber):
    page = reader.pages[i]
    text += page.extract_text()

logger.info('Successfully extracted text from PDF with filename: %s', fileNamePath)