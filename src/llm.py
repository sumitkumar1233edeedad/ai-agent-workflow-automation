"""Centralized LangChain OpenAI integration.

Provides configured ChatOpenAI instances supporting:
- OpenAI API (OPENAI_API_KEY, optional OPENAI_BASE_URL)
- OpenRouter API (OPENROUTER_API_KEY / openrouter_api_key)
- Safe fallback / Mocking for offline & test resilience
"""

import os
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

load_dotenv()


def get_chat_model(
    model: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
) -> Optional[ChatOpenAI]:
    """
    Initialize and return a LangChain ChatOpenAI instance.
    Checks OPENROUTER_API_KEY / openrouter_api_key first, then OPENAI_API_KEY.
    Returns None if no API key is configured.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("openrouter_api_key")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")

    if openrouter_key:
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        chosen_model = model or os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")
        return ChatOpenAI(
            api_key=openrouter_key,
            base_url=base_url,
            model=chosen_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif openai_key:
        base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENAI_API_BASE")
        chosen_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        kwargs = {
            "api_key": openai_key,
            "model": chosen_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if base_url:
            kwargs["base_url"] = base_url
        return ChatOpenAI(**kwargs)

    return None


def invoke_chat_model(
    messages: list[BaseMessage],
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> Optional[str]:
    """
    Safely invoke ChatOpenAI model. Returns text response or None on failure.
    """
    llm = get_chat_model(model=model, temperature=temperature)
    if not llm:
        return None
    try:
        response = llm.invoke(messages)
        return response.content.strip() if hasattr(response, "content") else str(response)
    except Exception as exc:
        print(f"[WARN] LangChain ChatOpenAI invocation failed: {exc}")
        return None
