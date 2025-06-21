# Contract-Analyzer

A tool for analyzing contracts using LLM APIs (OpenAI and Claude).

## Setup

1. **Install UV**

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies from `pyproject.toml`:**
   ```bash
   uv pip install .
   ```

   Alternatively, you can add new dependencies with:
   ```bash
   uv pip install <package-name>
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     CLAUDE_API_KEY=your_claude_api_key_here
     ```

## Usage

The `call_llm_api` function now reads API keys from environment variables, so you no longer need to pass them as arguments:

```python
from src.data_processing.llm import call_llm_api

# For OpenAI
call_llm_api("Summarize the following text:", "Your text here", provider="openai")

# For Claude
call_llm_api("Summarize the following text:", "Your text here", provider="claude")
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI provider)
- `CLAUDE_API_KEY`: Your Claude API key (required for Claude provider)



> **Note:**  
> - `uv` is a fast Python package manager and virtual environment tool.  
> - The `uv add -r requirements.txt` command is equivalent to `uv pip install -r requirements.txt`.  
> - If you already have a `pyproject.toml`, you can use `uv pip install .` to install your project in editable mode.

For more details, see the [uv documentation](https://github.com/astral-sh/uv).