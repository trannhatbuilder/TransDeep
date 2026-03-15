"""
NVIDIA Build AI Engine
Uses NVIDIA's API with Llama 4 Maverick model
"""

from typing import Dict, Any
from openai import OpenAI
from .base import BaseEngine


class NvidiaEngine(BaseEngine):
    """
    NVIDIA Build API Engine.
    Uses OpenAI-compatible API endpoint.
    Model: meta/llama-4-maverick-17b-128e-instruct
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        print(f"✅ NVIDIA Engine initialized: {self.model}")

    def generate(self, prompt: str) -> str:
        """
        Generate translation using NVIDIA's Llama 4 Maverick.

        Args:
            prompt: Translation prompt with instructions

        Returns:
            AI-generated translation and analysis
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are TransDeep, an expert translator. "
                            "Provide deep, clear translations with vocabulary "
                            "and relevant context. Always respond in a clear, "
                            "well-formatted manner using markdown."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
            )

            result = response.choices[0].message.content
            return result if result else "⚠️ Empty response from AI"

        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "unauthorized" in error_msg.lower():
                return "❌ API Key invalid. Check config/settings.py"
            elif "429" in error_msg:
                return "⏳ Rate limit exceeded. Please wait and try again."
            elif "timeout" in error_msg.lower():
                return "⏰ Request timed out. Check your internet connection."
            else:
                return f"❌ Translation error: {error_msg}"
