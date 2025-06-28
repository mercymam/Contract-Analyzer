import logging
import asyncio

from pypdf import PdfReader
from src.data_processing.llm import call_llm_api_parallel
from src.data_processing.truncator import truncate_to_fit
from src.database_communications.dynamoDb import upload_to_dynamodb
from src.prompt.prompt import tenancy_analysis_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_pdf_text_in_batches(file_path: str, file_identifier: str, batch_size: int = 5) -> list[str]:
    logger.info('Extracting text for file Id: %s from PDF in batches: %s', file_identifier, file_path)

    reader = await asyncio.to_thread(PdfReader, file_path)
    page_count = len(reader.pages)

    batches = 0
    status = "updating"
    ai_responses = ""

    for start in range(0, page_count, batch_size):
        end = min(start + batch_size, page_count)
        logger.info(f"Processing for file Id: {file_identifier} pages {start} to {end - 1} out of {page_count}")

        # Extract each batch concurrently
        batch_texts = await asyncio.gather(
            *[asyncio.to_thread(reader.pages[i].extract_text) for i in range(start, end)]
        )
        batch_combined = "".join(filter(None, batch_texts))
        truncated_text = truncate_to_fit(tenancy_analysis_prompt, batch_combined, provider="openai", model="gpt-3.5-turbo")
        ai_response = await call_llm_api_parallel(tenancy_analysis_prompt, truncated_text, file_identifier)
        logger.info(f"Successfuly gotten AI response for file Id: {file_identifier} and batch {batches}")
        if end == page_count:
            status = "completed"
        upload_to_dynamodb(file_identifier, ai_response, status)
        batches += 1
        ai_responses += " " + ai_response

    logger.info(f'Successfully extracted all {batches} text for file Id: {file_identifier} and batches from {file_path}')
    return ai_responses
