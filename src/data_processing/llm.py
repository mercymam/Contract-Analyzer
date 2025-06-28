import asyncio
import os

import aiohttp
from dotenv import load_dotenv
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables from .env file
load_dotenv()


async def call_llm_api_parallel(prompt: str, chunks: list, provider="openai", model="gpt-3.5-turbo") -> str:
    """
    Calls the specified LLM API (OpenAI or Claude) with the given prompt and text.
    Prints the output from the LLM.

    Args:
        :param model: The prompt to send to the LLM.
        :param provider: "openai" or "claude".
        :param prompt: Model name for OpenAI (default: "gpt-3.5-turbo").
        :param chunks: The text to provide as context or input.
    """
    if provider == "openai":
        tasks = [call_openai_api_async(prompt, chunks, model, i) for i, chunk in enumerate(chunks)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        combined_response = ""
        for r in responses:
            if isinstance(r, Exception):
                logger.error(f"LLM chunk failed: {r}")
            else:
                combined_response += r
        return combined_response
    elif provider == "claude":
        return call_claude_api(prompt, chunks)
    else:
        raise ValueError("Provider must be either 'openai' or 'claude'.")


async def call_openai_api_async(prompt, text, model="gpt-3.5-turbo", chunk_index=0) -> str:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API key must be set in environment variable OPENAI_API_KEY.")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    }
    async with aiohttp.ClientSession() as client:
        async with client.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                response_text = result["choices"][0]["message"]["content"]
                logger.info(f"Chunk {chunk_index} response: {response_text[:100]}")
                return response_text
            else:
                error_body = await response.text()
                raise Exception(f"OpenAI API Error: {response.status} {error_body}")

def call_claude_api(prompt, text) -> str:
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if claude_api_key is None:
        raise ValueError("Claude API key must be set in environment variable CLAUDE_API_KEY.")
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": claude_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    # Claude expects a single prompt string
    full_prompt = f"{prompt}\n\n{text}"
    data = {
        "model": "claude-3-opus-20240229",  # You may want to make this configurable
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": full_prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        response_text = result["content"][0]["text"]
        logger.info(response_text)
        return response_text
    else:
        raise Exception(f"Claude API Error: {response.status_code} {response.text}")