from __future__ import annotations

import requests

from app.config import OLLAMA_URL

class OllamaError(RuntimeError):
    pass

class OllamaServiceError(Exception):
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

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "stream": False,
                "keep_alive": "15m",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "options": {
                    "temperature": 0.2,
                },
            },
            timeout=(30, 1800),
        )
        response.raise_for_status()
    except requests.exceptions.ReadTimeout as exc:
        raise OllamaServiceError(
            "Ollama took too long to generate a response. "
            "Try again, use a smaller model, or increase resources."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise OllamaServiceError(
            "The request to Ollama timed out. "
            "Try again or switch to a smaller model."
        ) from exc
    except requests.exceptions.ConnectionError as exc:
        raise OllamaServiceError(
            "Could not connect to the Ollama server. "
            "Please make sure Ollama is running and ready."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise OllamaServiceError(
            f"Ollama request failed: {exc}"
        ) from exc

    payload = response.json()
    content = payload.get("message", {}).get("content", "").strip()
    if not content:
        raise OllamaError("Ollama returned an empty response")
    print("[autoreadme] Received response from Ollama", flush=True)
    return content
