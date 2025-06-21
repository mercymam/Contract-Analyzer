import os
from dotenv import load_dotenv
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables from .env file
load_dotenv()


def call_llm_api(prompt, text, provider="openai", model="gpt-3.5-turbo") -> str:
    """
    Calls the specified LLM API (OpenAI or Claude) with the given prompt and text.
    Prints the output from the LLM.

    Args:
        prompt (str): The prompt to send to the LLM.
        text (str): The text to provide as context or input.
        provider (str): "openai" or "claude".
        model (str): Model name for OpenAI (default: "gpt-3.5-turbo").
    """
    if provider == "openai":
        return call_openai_api(prompt, text, model)
    elif provider == "claude":
        return call_claude_api(prompt, text)
    else:
        raise ValueError("Provider must be either 'openai' or 'claude'.")


def call_openai_api(prompt, text, model) -> str:
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
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        response_text = result["choices"][0]["message"]["content"]
        logger.info(response_text)
        return response_text
    else:
        raise Exception(f"OpenAI API Error: {response.status_code} {response.text}")


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