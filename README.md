# 🌐 TransDeep - AI Deep Translation

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-Latest-green?logo=qt&logoColor=white)](https://www.riverbankcomputing.com/software/pyqt/)
[![NVIDIA API](https://img.shields.io/badge/NVIDIA%20API-Integration-76b900?logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)

**Professional AI-powered translation with deep linguistic analysis**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration)

</div>

---

## 📋 Overview

**TransDeep** is a lightweight desktop application that provides **instant, deep AI-powered translations** with detailed linguistic analysis. Select any text and press **Alt+C** to get:

- 🌍 Accurate natural language translation
- 📖 Vocabulary breakdown with examples
- ⚡ Instant results via system hotkey
- 🎨 Modern dark theme UI
- 🔧 Extensible AI engine architecture

Powered by **NVIDIA's Llama 4 Maverick** model for high-quality translations.

---

## ✨ Features

### 🎯 Core Features
- **Global Hotkey Translation** - Press `Alt+C` anywhere to translate selected text
- **Deep Analysis** - Provides translation + vocabulary breakdown + context
- **System Tray Integration** - Runs quietly in system tray with minimal footprint
- **Dark Modern UI** - Clean, professional interface with rounded corners
- **Thread-Safe Operation** - Non-blocking UI with background translation

### 🔌 Technical Features
- **Pluggable AI Engines** - Extensible architecture for multiple AI providers
- **Real-time Clipboard Support** - Automatically detects selected/copied text
- **Markdown Formatting** - Results displayed with proper formatting
- **Cross-Platform** - Windows, macOS, Linux support
- **Error Handling** - Graceful error messages and fallback mechanisms

### 🎨 UI Features
- **Frameless Window** - Modern flat design aesthetic
- **Shadow Effects** - Professional drop shadow effects
- **Animated Loading** - Visual feedback during translation
- **Model Selector** - Switch between AI models on the fly
- **Copy Results** - One-click copy to clipboard
- **Transparent Background** - Clean, non-intrusive popup

---

## 🚀 Installation

### Prerequisites
- **Python** 3.8 or higher
- **pip** package manager
- **NVIDIA API Key** (get free tier from [build.nvidia.com](https://build.nvidia.com/))

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd TransDeep
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key
Edit `config/settings.py` and add your NVIDIA API key:
```python
AI_ENGINES = {
    "nvidia_llama4": {
        ...
        "api_key": "YOUR_NVIDIA_API_KEY_HERE",
        ...
    }
}
```

### Step 5: Run Application
```bash
python main.py
```

---

## 📖 Usage

### Basic Translation
1. **Select Text** - Highlight any text you want to translate
2. **Press Hotkey** - Press `Alt+C` (default)
3. **View Results** - Translation popup appears with deep analysis
4. **Copy Results** - Click "📋 Copy" button to save to clipboard

### From System Tray
- **Single Click** - Show tray menu
- **Double Click** - Open translator window
- **Right Click** - View options (Show Translator, Hotkey info, Quit)

### Model Selection
Change AI model in the popup:
1. Click the model dropdown in the popup header
2. Select desired AI engine
3. Start new translation with selected model

---

## ⚙️ Configuration

### `config/settings.py` - Main Configuration

```python
# AI Engine Settings
DEFAULT_ENGINE = "nvidia_llama4"  # Active translation engine

# Language Settings
SOURCE_LANG = "English"           # Source language
TARGET_LANG = "Vietnamese"        # Target language

# Hotkey Configuration
HOTKEY = "alt+c"                  # Global translation hotkey

# UI Settings
POPUP_WIDTH = 700                 # Popup window width (px)
POPUP_HEIGHT = 550                # Popup window height (px)
POPUP_OPACITY = 0.97              # Window transparency (0-1)
THEME = "dark"                    # UI theme ("dark" or "light")
```

### Adding New AI Engines

Add to `AI_ENGINES` in `config/settings.py`:
```python
AI_ENGINES = {
    "your_engine": {
        "name": "Display Name",
        "provider": "provider_name",
        "model": "model-id",
        "api_key": "YOUR_API_KEY",
        "base_url": "https://api.example.com/v1",
        "max_tokens": 4096,
        "temperature": 0.3,
        "top_p": 0.9,
    }
}
```

Then implement corresponding engine class in `ai_engines/`:
```python
from .base import BaseEngine

class YourEngine(BaseEngine):
    def __init__(self, config):
        super().__init__(config)
        # Initialize your API client
    
    def generate(self, prompt: str) -> str:
        # Implement translation logic
        return result
```

---

## 🏗️ Project Structure

```
TransDeep/
├── 📄 main.py                 # Application entry point
├── 📄 README.md               # This file
├── 📊 requirements.txt        # Python dependencies
│
├── 🗂️ config/
│   └── settings.py            # Global configuration
│
├── 🗂️ core/                   # Core functionality
│   ├── clipboard.py           # Clipboard reader (multi-OS)
│   ├── hotkey.py              # Global hotkey listener
│   └── translator.py          # Translation orchestrator
│
├── 🗂️ ai_engines/             # AI engine implementations
│   ├── base.py                # Abstract base class
│   └── nvidia_engine.py       # NVIDIA Llama 4 engine
│
└── 🗂️ ui/                     # User interface
    ├── popup.py               # Translation result popup
    ├── tray.py                # System tray icon
    ├── floating_icon.py       # Floating UI elements
    └── styles.py              # CSS-like theme definitions
```

---

## 🔧 Architecture

### Component Overview

```
┌─────────────────────────────────────────────┐
│     main.py (Application Entry)             │
└────────────────────┬────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐  ┌──────────┐ ┌─────────┐
   │Hotkey   │  │Clipboard │ │Translator
   │Listener │  │Reader    │ │& Engine
   └────┬────┘  └────┬─────┘ └────┬────┘
        │            │             │
        └────────────┼─────────────┘
                     ▼
         ┌──────────────────────┐
         │Translation Popup UI  │
         │ (PyQt6 Widget)       │
         └─────────┬────────────┘
                   ▼
         ┌──────────────────────┐
         │System Tray Icon      │
         └──────────────────────┘
```

### Data Flow

1. **Hotkey Detection** → HotkeyListener detects `Alt+C`
2. **Text Capture** → ClipboardReader gets selected text
3. **Translation Request** → TranslationController processes request
4. **AI Processing** → Translator sends prompt to AI Engine
5. **UI Update** → Results displayed in popup via PyQt6 signals
6. **User Interaction** → Copy/close buttons in popup

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `PyQt6` | Latest | GUI framework |
| `PyQt6-WebEngine` | Latest | HTML rendering in popup |
| `openai` | Latest | NVIDIA API client |
| `keyboard` | Latest | Global hotkey support |
| `pyside6` | Latest | Alternative Qt bindings |

Install all via `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🎯 Supported AI Engines

| Engine | Provider | Model | Status |
|--------|----------|-------|--------|
| **Llama 4 Maverick** | NVIDIA | meta/llama-4-maverick-17b-128e-instruct | ✅ Active |
| Gemini Pro | Google | gemini-pro | 🔄 Planned |
| GPT-4 | OpenAI | gpt-4 | 🔄 Planned |
| DeepSeek | DeepSeek | deepseek-chat | 🔄 Planned |

---

## 🛠️ Troubleshooting

### ❌ Hotkey Not Working
```
Solution: Ensure "run as administrator" (Windows) or grant accessibility permissions (macOS/Linux)
```

### ⚠️ API Key Invalid
```
1. Check settings.py - ensure API key is correct
2. Verify API key is active at build.nvidia.com
3. Check network connectivity
```

### 📎 Clipboard Not Reading
```
Linux: Install xclip or xsel
  sudo apt install xclip
Windows/macOS: Usually works out of the box
```

### 🔇 Translation Slow
```
- Check internet connection
- Try smaller text chunks
- NVIDIA API may have rate limits (free tier: 40 req/day)
```

---

## 📝 Translation Features

### Input
- **Format**: Plain text (any language)
- **Length**: Up to 4096 tokens per request
- **Special**: Handles code, URLs, emojis naturally

### Output Format
Results include:
```
## 🌐 TRANSLATION
[Natural language translation]

## 📖 VOCABULARY
- Word1 → Translation1
- Word2 → Translation2
[Additional context]
```

### Customizing Prompts
Edit `PROMPT_TEMPLATE` in `core/translator.py`:
```python
PROMPT_TEMPLATE = """Your custom prompt here with {source_lang}, {target_lang}, {text} placeholders"""
```

---

## 🔐 Security & Privacy

⚠️ **Important Notes:**
- **API Keys**: Never commit API keys to version control
- **Text Data**: Translation requests sent to NVIDIA API servers
- **Local Caching**: No persistent local caching of translations
- **Clipboard Protection**: Sensitive information should be reviewed before translation

### Best Practices
```bash
# Use .gitignore for sensitive data
echo "config/settings.py" >> .gitignore

# Use environment variables for API keys (optional)
export NVIDIA_API_KEY="your_key_here"
```

---

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- 🌍 Additional language support
- 🔌 New AI engine integrations
- 🎨 Light theme implementation
- 🧪 Unit tests & CI/CD
- 📚 Documentation improvements

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Average Translation Time** | 2-5 seconds |
| **Memory Usage** | ~200-300 MB |
| **Startup Time** | ~1-2 seconds |
| **API Rate Limit** | 40 req/day (free tier) |
| **Max Token Size** | 4096 tokens per request |

---

## 🎓 Learning Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [NVIDIA Build API](https://build.nvidia.com/)
- [Llama Model Info](https://www.llama.com/)
- [Keyboard Library](https://github.com/boppreh/keyboard)

---

## 👨‍💻 Author

**Tran Nhon Nhat**

---

<div align="center">

**Made with ❤️ for language enthusiasts and developers**

Questions? Issues? [Open an issue](../../issues) or contact the team.

</div>
