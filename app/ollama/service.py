from __future__ import annotations

import requests

from app.config import OLLAMA_URL

class OllamaError(RuntimeError):
    pass

def list_models() -> list[str]:
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=30)
    response.raise_for_status()
    payload = response.json()
    return [model["name"] for model in payload.get("models", [])]

def ensure_model(model: str) -> None:
    if model in list_models():
        print(f"[autoreadme] Found existing model: {model}")
        return

    print(f"[autoreadme] Model: {model} not found. Downloading from Ollama. Please wait a while...")
    response = requests.post(
        f"{OLLAMA_URL}/api/pull",
        json={"name": model, "stream": False},
        timeout=600,
    )
    response.raise_for_status()

def generate_markdown(model: str, system_prompt: str, user_prompt: str) -> str:
    print("[autoreadme] Sending request to Ollama...", flush=True)
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "options": {
                "temperature": 0.2,
            },
        },
        timeout=600,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload.get("message", {}).get("content", "").strip()
    if not content:
        raise OllamaError("Ollama returned an empty response")
    print("[autoreadme] Received response from Ollama", flush=True)
    return content
