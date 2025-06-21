import asyncio
import logging
from typing import Any

import tiktoken

from text_extractor.extract_text import extract_pdf_text

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def count_tokens(text: str, model: str, provider: str) -> int:
    if provider == "openai":
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    elif provider == "claude":
        return estimate_tokens_claude(text)
    else:
        raise ValueError("Unsupported provider")


def estimate_tokens_claude(text: str) -> int:
    # Claude token estimation: ~1 token = 3.5 characters (varies)
    return int(len(text) / 3.5)


def truncate_to_fit(prompt: str, text: str, model: str, provider: str, buffer: int = 1000) -> list[str]:
    key = f"{provider}:{model}"
    limit = TOKEN_LIMITS.get(key, 16000)
    logger.info(f"Truncating to {limit} tokens for model {model}")

    prompt_tokens = count_tokens(prompt, model, provider)
    max_text_tokens = limit - prompt_tokens - buffer  # leave space for response

    current_tokens = count_tokens(text, model, provider)

    if current_tokens <= max_text_tokens:
        logging.info(f"The text has {current_tokens} tokens, within limit of {max_text_tokens}")
        return [text]

    # Truncate by characters proportionally (conservatively)
    avg_token_length = 4 if provider == "openai" else 3.5
    max_chars = int(max_text_tokens * avg_token_length)

    truncated_chunks = []
    while len(text) > 0:
        chunk = text[:max_chars]
        truncated_chunks.append(chunk)
        text = text[max_chars:]

    logging.info(f"Text was too long and split into {len(truncated_chunks)} chunks.")
    return truncated_chunks


TOKEN_LIMITS = {
    "openai:gpt-3.5-turbo": 16385,
    "openai:gpt-4": 8192,
    "openai:gpt-4o": 128000,
    "claude:claude-3-haiku": 200000,
    "claude:claude-3-sonnet": 200000,
    "claude:claude-3-opus": 200000,
}
