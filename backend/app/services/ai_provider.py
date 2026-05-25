import json
import re
import httpx
import structlog
from abc import ABC, abstractmethod
from app.config import get_settings
from app.services.cache import AICache

settings = get_settings()
logger = structlog.get_logger()


def compress_input(text: str, max_line_length: int = 500) -> str:
    text = re.sub(r"\s+", " ", text)
    lines = text.split("\n")
    compressed = []
    for line in lines:
        line = line.strip()
        if len(line) > max_line_length:
            line = line[:max_line_length] + "..."
        if line:
            compressed.append(line)
    return "\n".join(compressed)


class AIProvider(ABC):
    def __init__(self):
        self.cache = AICache()

    @abstractmethod
    async def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        pass

    async def parse_json(self, system: str, user: str) -> dict:
        cleaned_user = compress_input(user)
        cached = await self.cache.get_prompt(system, cleaned_user)
        if cached is not None:
            logger.info("ai_cache_hit", mode="parse_json")
            return json.loads(cached)

        response = await self.chat(system, cleaned_user, json_mode=True)

        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1].split("```")[0].strip()

        result = json.loads(cleaned)
        await self.cache.set_prompt(system, cleaned_user, json.dumps(result))
        return result


class OllamaProvider(AIProvider):
    def __init__(self):
        super().__init__()
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model

    async def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        cleaned_user = compress_input(user)
        cached = await self.cache.get_prompt(system, cleaned_user)
        if cached is not None:
            logger.info("ai_cache_hit", provider="ollama")
            return cached

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": cleaned_user},
            ],
            "stream": False,
            "options": {"temperature": 0.1},
        }
        if json_mode:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            result = data["message"]["content"]

        await self.cache.set_prompt(system, cleaned_user, result)
        return result


class GeminiProvider(AIProvider):
    def __init__(self):
        super().__init__()
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)
        self.max_tokens = settings.gemini_max_tokens

    async def chat(self, system: str, user: str, json_mode: bool = False) -> str:
        cleaned_user = compress_input(user)
        cached = await self.cache.get_prompt(system, cleaned_user)
        if cached is not None:
            logger.info("ai_cache_hit", provider="gemini")
            return cached

        prompt = f"{system}\n\n---\n\n{cleaned_user}"
        if json_mode:
            prompt += "\n\nRespond with valid JSON only. No markdown, no explanation."

        response = await self.model.generate_content_async(
            prompt,
            generation_config={
                "max_output_tokens": self.max_tokens,
                "temperature": 0.1,
            },
        )
        result = response.text

        await self.cache.set_prompt(system, cleaned_user, result)
        return result


def get_ai_provider() -> AIProvider:
    provider_type = settings.ai_provider.lower()
    if provider_type == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when using gemini provider")
        return GeminiProvider()
    return OllamaProvider()
