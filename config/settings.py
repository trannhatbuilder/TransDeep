"""
TransDeep - Configuration Settings
API keys, model configs, and app settings
"""

# ═══════════════════════════════════════════════
#  AI ENGINE CONFIGURATION
# ═══════════════════════════════════════════════

AI_ENGINES = {
    "nvidia_llama4": {
        "name": "Llama 4 Maverick (NVIDIA)",
        "provider": "nvidia",
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "api_key": "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",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "max_tokens": 4096,
        "temperature": 0.3,
        "top_p": 0.9,
    },
    # ── Future engines ──────────────────────────
    # "gemini_pro": {
    #     "name": "Gemini Pro",
    #     "provider": "google",
    #     "model": "gemini-pro",
    #     "api_key": "YOUR_GEMINI_API_KEY",
    #     "base_url": "https://generativelanguage.googleapis.com/v1",
    # },
    # "openai_gpt4": {
    #     "name": "GPT-4",
    #     "provider": "openai",
    #     "model": "gpt-4",
    #     "api_key": "YOUR_OPENAI_API_KEY",
    #     "base_url": "https://api.openai.com/v1",
    # },
    # "deepseek": {
    #     "name": "DeepSeek",
    #     "provider": "deepseek",
    #     "model": "deepseek-chat",
    #     "api_key": "YOUR_DEEPSEEK_API_KEY",
    #     "base_url": "https://api.deepseek.com/v1",
    # },
}

# Default engine
DEFAULT_ENGINE = "nvidia_llama4"

# ═══════════════════════════════════════════════
#  HOTKEY CONFIGURATION
# ═══════════════════════════════════════════════

HOTKEY = "alt+c"  # Default hotkey, customizable

# ═══════════════════════════════════════════════
#  TRANSLATION SETTINGS
# ═══════════════════════════════════════════════

SOURCE_LANG = "English"
TARGET_LANG = "Vietnamese"

# ═══════════════════════════════════════════════
#  UI SETTINGS
# ═══════════════════════════════════════════════

POPUP_WIDTH = 700
POPUP_HEIGHT = 550
POPUP_OPACITY = 0.97
THEME = "dark"  # "dark" or "light"
