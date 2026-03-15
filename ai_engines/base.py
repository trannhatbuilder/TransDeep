"""
Base AI Engine
Abstract class for all AI engines
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseEngine(ABC):
    """
    Abstract base class for AI translation engines.
    All engines must implement the generate() method.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get("model", "")
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.3)
        self.top_p = config.get("top_p", 0.9)

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate response from AI model.

        Args:
            prompt: The translation prompt

        Returns:
            Generated text response
        """
        pass

    def get_name(self) -> str:
        """Get display name of this engine."""
        return self.config.get("name", "Unknown Engine")

    def __str__(self):
        return f"{self.__class__.__name__}({self.get_name()})"
