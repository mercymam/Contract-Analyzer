import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def count_tokens(text: str, model: str, provider: str) -> int:
    if provider == "openai":
        return int(len(text) / 4)
    elif provider == "claude":
        return int(len(text) / 3.5)
    else:
        raise ValueError("Unsupported provider")

def truncate_to_fit(
    prompt: str,
    text: str,
    model: str,
    provider: str,
    target_chunk_tokens: int = 5000
) -> list[str]:
    key = f"{provider}:{model}"
    limit = TOKEN_LIMITS.get(key, target_chunk_tokens)
    logger.info(f"Truncating to {limit} tokens for model {model}")

    prompt_tokens = count_tokens(prompt, model, provider)
    chunk_size = limit - prompt_tokens

    avg_token_length = 4 if provider == "openai" else 3.5
    max_chars = int(chunk_size * avg_token_length)

    truncated_chunks = []
    while len(text) > 0:
        chunk = text[:max_chars]
        truncated_chunks.append(chunk)
        text = text[max_chars:]

    logger.info(f"Split into {len(truncated_chunks)} chunks of ~{chunk_size} tokens each")
    return truncated_chunks


TOKEN_LIMITS = {
    "openai:gpt-3.5-turbo": 4000, #max token limit 16385
    "openai:gpt-4": 2000, # max token limit 8192,
    "openai:gpt-4o": 8000, # 128000,
    "claude:claude-3-haiku": 200000,
    "claude:claude-3-sonnet": 200000,
    "claude:claude-3-opus": 100000 #  200000,
}
