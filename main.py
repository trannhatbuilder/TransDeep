import sys
import signal
import threading
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

from core.hotkey import HotkeyListener
from ui.tray import SystemTray
from ui.popup import TranslationPopup
from core.translator import Translator
from core.clipboard import ClipboardReader
from config.settings import DEFAULT_ENGINE


class TranslationController(QObject):
    """Controller for thread-safe translation operations."""
    
    # Signal for thread-safe translation requests
    translate_requested = pyqtSignal(str)
    
    def __init__(self, clipboard, translator, popup):
        super().__init__()
        self.clipboard = clipboard
        self.translator = translator
        self.popup = popup
        self._is_translating = False
        self._last_request_time = 0.0
        self._min_request_interval = 0.5  # seconds
        self.latest_clipboard_text = ""
        self._last_translated_text = ""
        
        # Connect signal to slot (thread-safe)
        self.translate_requested.connect(self._handle_translate_request)
    
    def request_translation(self, text: str = None):
        """Request translation from any thread.

        If `text` is None, uses the most recently seen clipboard text.
        """
        now = time.time()
        if now - self._last_request_time < self._min_request_interval:
            return

        # Prefer explicit text, otherwise use cached clipboard text or read it now
        # If no clipboard text, attempt to programmatically copy the current selection
        text_to_translate = (text or self.latest_clipboard_text or
                     self.clipboard.get_selected_or_copy())
        if not text_to_translate or not text_to_translate.strip():
            return

        # Avoid translating the same text repeatedly
        if text_to_translate.strip() == self._last_translated_text:
            return

        self._last_request_time = now

        # Emit signal for thread-safe main thread handling
        self.translate_requested.emit(text_to_translate)

    # Debugging: track calls
    def _debug_request(self):
        print("DEBUG: request_translation called")
    
    def _handle_translate_request(self, text: str):
        """Handle translation request in main thread."""
        if self._is_translating:
            return

        if not text or not text.strip():
            return

        self._is_translating = True
        # Cache the text we are about to translate (prevents duplicates)
        self.latest_clipboard_text = text
        self.popup.show_loading_signal.emit(text)
        # Run translation in background thread
        threading.Thread(
            target=self._translate_async,
            args=(text,),
            daemon=True
        ).start()
    
    def _translate_async(self, text):
        """Run translation in background to avoid blocking UI."""
        try:
            result = self.translator.translate(text)
            # Update UI from main thread
            self.popup.update_result(result)
        except Exception as e:
            self.popup.show_error(str(e))
        finally:
            # mark translation finished and remember last translated text
            self._is_translating = False
            try:
                self._last_translated_text = text.strip()
            except Exception:
                pass

def main():
    """Main entry point for TransDeep."""
    # Enable Ctrl+C in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("TransDeep")
    app.setApplicationDisplayName("TransDeep - AI Deep Translation")

    # Initialize components
    clipboard = ClipboardReader()
    translator = Translator(engine_name=DEFAULT_ENGINE)
    popup = TranslationPopup()
    tray = SystemTray(app, popup)
    
    # Create controller for thread-safe operations
    controller = TranslationController(clipboard, translator, popup)

    def on_hotkey_triggered():
        controller.request_translation()

    # Start hotkey listeners for Alt+C and Ctrl+C
    try:
        hotkey_listener_alt = HotkeyListener(callback=on_hotkey_triggered, hotkey='alt+c')
        hotkey_listener_alt.start()
    except Exception as e:
        print(f"⚠️ Hotkey initialization failed: {e}")

    # Show popup automatically when user copies text (Ctrl+C)
    qt_clipboard = app.clipboard()

    def _on_clipboard_change():
        try:
            # Read current clipboard selection/text and cache it.
            # Do NOT auto-trigger translation here — user will press Alt+C to translate.
            text = clipboard.get_selected_text()
            if text and text.strip():
                controller.latest_clipboard_text = text
        except Exception as e:
            print(f"⚠️ Clipboard handler error: {e}")

    try:
        qt_clipboard.dataChanged.connect(_on_clipboard_change)
    except Exception:
        # Fallback: use a polling timer if signal connect fails
        poll_timer = QTimer()
        _last_clip = ""

        def _poll_clipboard():
            nonlocal _last_clip
            try:
                txt = clipboard.get_selected_text()
                if txt != _last_clip:
                    _last_clip = txt
                    if txt and txt.strip():
                        controller.latest_clipboard_text = txt
            except Exception:
                pass

        poll_timer.timeout.connect(_poll_clipboard)
        poll_timer.start(500)

    # Floating icon removed as requested. No icon will appear.

    # Show tray icon
    tray.show()

    # Process events timer (for signal handling)
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    print("🚀 TransDeep is running!")
    print("📋 Select text and press Alt+C to translate")
    print("🔽 Check system tray for options")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
