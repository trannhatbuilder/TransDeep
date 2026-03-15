"""
Translator
Orchestrates AI translation with deep analysis
"""

from config.settings import AI_ENGINES, DEFAULT_ENGINE, SOURCE_LANG, TARGET_LANG
from ai_engines.nvidia_engine import NvidiaEngine


class Translator:
    """
    Main translator class.
    Uses pluggable AI engines for translation.
    """

    # Deep analysis prompt template
    PROMPT_TEMPLATE = """You are a professional translator and language analyst.

📝 **SOURCE TEXT ({source_lang}):**
{text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please provide a DEEP translation analysis with the following format:

## 🌐 TRANSLATION
Translate the text naturally into {target_lang}. Keep the meaning accurate and natural-sounding.

## 📖 VOCABULARY
List important words/phrases with:
- Original word → Translation
- Part of speech
- Example usage (if helpful)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Format your response clearly with markdown. Be thorough but concise."""

    def __init__(self, engine_name: str = None):
        self.engine_name = engine_name or DEFAULT_ENGINE
        self.engine = self._create_engine(self.engine_name)

    def _create_engine(self, engine_name: str):
        """Factory method to create AI engine."""
        config = AI_ENGINES.get(engine_name)
        if not config:
            raise ValueError(f"Unknown engine: {engine_name}")

        provider = config["provider"]

        if provider == "nvidia":
            return NvidiaEngine(config)
        # Future engines:
        # elif provider == "google":
        #     return GeminiEngine(config)
        # elif provider == "openai":
        #     return OpenAIEngine(config)
        # elif provider == "deepseek":
        #     return DeepSeekEngine(config)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def translate(self, text: str) -> str:
        """
        Translate text with deep analysis.
        Returns formatted markdown result.
        """
        prompt = self.PROMPT_TEMPLATE.format(
            source_lang=SOURCE_LANG,
            target_lang=TARGET_LANG,
            text=text
        )

        result = self.engine.generate(prompt)
        return result

    def switch_engine(self, engine_name: str):
        """Switch to a different AI engine."""
        self.engine_name = engine_name
        self.engine = self._create_engine(engine_name)
        print(f"🔄 Switched to engine: {engine_name}")

    def get_current_engine_name(self) -> str:
        """Get display name of current engine."""
        config = AI_ENGINES.get(self.engine_name, {})
        return config.get("name", self.engine_name)
