import requests

from app.config import settings
from app.exceptions import OllamaConnectionError
from app.logger import logger
import json

def generate_response(prompt: str) -> str:
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            settings.OLLAMA_URL,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        logger.info("Response received")

        return response.json()["response"]

    except requests.exceptions.RequestException as exc:
        logger.error("Connection failed")
        raise OllamaConnectionError("Unable to connect to Ollama.") from exc 

def stream_response(prompt: str):

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
    }

    try:
        response = requests.post(
            settings.OLLAMA_URL,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT,
            stream=True,
        )

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            if "response" in data:
                yield data["response"]

            if data.get("done"):
                break

    except requests.exceptions.RequestException as exc:
        logger.exception("Streaming connection failed")
        raise OllamaConnectionError("Unable to connect to Ollama.") from exc