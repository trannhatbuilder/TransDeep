import threading
import time
import keyboard
from config.settings import HOTKEY


class HotkeyListener:
    """
    Listens for global hotkey and triggers callback.
    Default: Alt+C
    """

    def __init__(self, callback, hotkey: str = None):
        self.callback = callback
        self.hotkey = hotkey or HOTKEY
        self._thread = None
        self._running = False
        self._last_trigger = 0.0
        self._debounce_s = 0.5  # seconds

    def start(self):
        """Start listening for hotkey in background thread."""
        self._running = True
        try:
            # keyboard.add_hotkey returns a handler identifier on success
            self._hotkey_handle = keyboard.add_hotkey(self.hotkey, self._on_hotkey)
            print(f"🎹 Hotkey registered: {self.hotkey.upper()}")
        except Exception as e:
            # Provide informative debug message if registration fails
            self._hotkey_handle = None
            print(f"⚠️ Failed to register hotkey '{self.hotkey}': {e}")

    def _on_hotkey(self):
        """Called when hotkey is detected."""
        now = time.time()
        if now - self._last_trigger < self._debounce_s:
            return
        self._last_trigger = now
        # Debug ping
        print(f"🎹 Hotkey triggered: {self.hotkey}")
        # Run callback in a new thread to avoid blocking
        try:
            threading.Thread(target=self.callback, daemon=True).start()
        except Exception as e:
            print(f"⚠️ Error running hotkey callback: {e}")

    def stop(self):
        """Stop listening for hotkey."""
        self._running = False
        try:
            # Try to remove by handler if available, otherwise by hotkey string
            if hasattr(self, '_hotkey_handle') and self._hotkey_handle:
                keyboard.remove_hotkey(self._hotkey_handle)
            else:
                keyboard.remove_hotkey(self.hotkey)
        except Exception:
            pass
        print("🎹 Hotkey listener stopped")

    def update_hotkey(self, new_hotkey: str):
        """Change the hotkey at runtime."""
        self.stop()
        self.hotkey = new_hotkey
        self.start()
