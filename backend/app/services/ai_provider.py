import json
import httpx
from abc import ABC, abstractmethod
from app.config import get_settings

settings = get_settings()


class AIProvider(ABC):
    @abstractmethod
    async def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        pass

    async def parse_json(self, system: str, user: str) -> dict:
        response = await self.chat(system, user, json_mode=True)
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        return json.loads(cleaned)


class OllamaProvider(AIProvider):
    def __init__(self):
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model

    async def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
        }
        if json_mode:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["message"]["content"]


class GeminiProvider(AIProvider):
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    async def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        prompt = f"{system}\n\n---\n\n{user}"
        if json_mode:
            prompt += "\n\nRespond with valid JSON only. No markdown, no explanation."

        response = await self.model.generate_content_async(prompt)
        return response.text


def get_ai_provider() -> AIProvider:
    provider_type = settings.ai_provider.lower()
    if provider_type == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when using gemini provider")
        return GeminiProvider()
    return OllamaProvider()
