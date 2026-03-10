import json
import os
from typing import Dict, Generator, List

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_TIMEOUT_SECONDS = 60
SESSION = requests.Session()


def _get_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY in environment variables.")

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def ask_model(model: str, messages: List[Dict[str, str]]) -> Dict:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }

    try:
        response = SESSION.post(
            BASE_URL,
            json=payload,
            headers=_get_headers(),
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"error": {"message": f"HTTP request failed: {exc}"}}
    except ValueError as exc:
        return {"error": {"message": f"Invalid JSON response: {exc}"}}


def stream_model_text(
    model: str,
    messages: List[Dict[str, str]],
) -> Generator[str, None, None]:
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
    }

    with SESSION.post(
        BASE_URL,
        json=payload,
        headers=_get_headers(),
        stream=True,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue

            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue

            payload_str = decoded[6:]
            if payload_str.strip() == "[DONE]":
                break

            try:
                chunk = json.loads(payload_str)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    yield delta
            except (KeyError, ValueError, TypeError):
                continue


def extract_assistant_text(response: Dict) -> str:
    if "choices" not in response:
        return f"[Error] {response.get('error', {}).get('message', 'Unknown error')}"

    return response["choices"][0]["message"].get("content", "")


