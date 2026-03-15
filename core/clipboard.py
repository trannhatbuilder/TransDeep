import platform
import subprocess
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMimeData


class ClipboardReader:
    """Reads selected/copied text from system clipboard."""

    def __init__(self):
        self.system = platform.system()

    def get_selected_text(self) -> str:
        """
        Get the currently selected text.
        On Linux: reads PRIMARY selection (selected text)
        On Windows: reads clipboard (Ctrl+C text)
        """
        try:
            if self.system == "Linux":
                return self._get_linux_selection()
            else:
                return self._get_clipboard_text()
        except Exception as e:
            print(f"⚠️ Clipboard error: {e}")
            return ""

    def _get_clipboard_text(self) -> str:
        """Get text from system clipboard (Windows/fallback)."""
        clipboard = QApplication.clipboard()
        if clipboard:
            text = clipboard.text()
            return text if text else ""
        return ""

    def _get_linux_selection(self) -> str:
        """
        Get PRIMARY selection on Linux.
        This is the text that's currently highlighted/selected.
        """
        try:
            # Try xclip first (PRIMARY selection)
            result = subprocess.run(
                ["xclip", "-selection", "primary", "-o"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        except subprocess.TimeoutExpired:
            pass

        try:
            # Fallback: xsel
            result = subprocess.run(
                ["xsel", "--primary", "--output"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        except subprocess.TimeoutExpired:
            pass

        # Final fallback: Qt clipboard
        return self._get_clipboard_text()

    def copy_to_clipboard(self, text: str):
        """Copy text to system clipboard."""
        clipboard = QApplication.clipboard()
        if clipboard:
            mime_data = QMimeData()
            mime_data.setText(text)
            clipboard.setMimeData(mime_data)

    def get_selected_or_copy(self, wait: float = 0.25) -> str:
        """
        Return selected text. If none found, attempt to simulate Ctrl+C to copy
        the current selection into the clipboard, then return clipboard text.
        """
        # Fast path: if clipboard already has text, return it
        try:
            txt = self.get_selected_text()
            if txt and txt.strip():
                return txt
        except Exception:
            pass

        # Try to simulate a copy (Ctrl+C) and wait briefly for clipboard update
        try:
            # Keyboard simulation may require the 'keyboard' package; import locally
            import keyboard
            key_combo = 'ctrl+c'
            # On macOS, use command+c (not strongly supported in this project)
            if platform.system() == 'Darwin':
                key_combo = 'command+c'

            keyboard.press_and_release(key_combo)

            end = time.time() + wait
            while time.time() < end:
                txt = self._get_clipboard_text()
                if txt and txt.strip():
                    return txt
                time.sleep(0.02)
        except Exception:
            # If simulation fails, fall back to reading clipboard directly
            pass

        return self._get_clipboard_text()
