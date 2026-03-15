"""
Translation Popup Window
Shows translation results with deep analysis
"""

import markdown
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextBrowser, QComboBox, QFrame,
    QApplication, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QCursor

from config.settings import AI_ENGINES, POPUP_WIDTH, POPUP_HEIGHT, POPUP_OPACITY
from ui.styles import DARK_THEME


class TranslationPopup(QWidget):
    """
    Popup window that shows translation results.
    Features:
    - Dark theme with rounded corners
    - Markdown rendering
    - Copy button
    - Model selector dropdown
    - Loading animation
    """

    # Signals for thread-safe UI updates
    result_ready = pyqtSignal(str)
    error_ready = pyqtSignal(str)
    show_loading_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._current_result = ""
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._loading_dots = 0

    def _setup_window(self):
        """Configure window properties."""
        self.setWindowTitle("TransDeep")
        self.setFixedSize(POPUP_WIDTH, POPUP_HEIGHT)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Window
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(POPUP_OPACITY)
        self.setStyleSheet(DARK_THEME)

    def _setup_ui(self):
        """Build the UI layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(8)

        # ── Header ──────────────────────────
        header = QHBoxLayout()

        # Title
        title = QLabel("🌐 TransDeep")
        title.setObjectName("titleLabel")
        header.addWidget(title)

        header.addStretch()

        # Model selector
        self.model_combo = QComboBox()
        for key, cfg in AI_ENGINES.items():
            self.model_combo.addItem(cfg["name"], key)
        header.addWidget(self.model_combo)

        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.clicked.connect(self.hide)
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        header.addWidget(self.close_btn)

        main_layout.addLayout(header)

        # ── Source Text Label ───────────────
        self.source_label = QLabel("")
        self.source_label.setObjectName("sourceLabel")
        self.source_label.setWordWrap(True)
        self.source_label.setMaximumHeight(60)
        main_layout.addWidget(self.source_label)

        # ── Separator ──────────────────────
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(separator)

        # ── Result Area ────────────────────
        self.result_browser = QTextBrowser()
        self.result_browser.setOpenExternalLinks(True)
        self.result_browser.setFont(QFont("Segoe UI", 12))
        main_layout.addWidget(self.result_browser, 1)

        # ── Loading Label (hidden by default) ──
        self.loading_label = QLabel("⏳ Translating")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.hide()
        main_layout.addWidget(self.loading_label)

        # ── Footer ─────────────────────────
        footer = QHBoxLayout()

        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        footer.addWidget(self.status_label)

        footer.addStretch()

        # Copy button
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setObjectName("copyButton")
        self.copy_btn.clicked.connect(self._copy_result)
        self.copy_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        footer.addWidget(self.copy_btn)

        main_layout.addLayout(footer)

        # ── Loading Timer ──────────────────
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self._animate_loading)

    def _connect_signals(self):
        """Connect thread-safe signals."""
        self.result_ready.connect(self._on_result_ready)
        self.error_ready.connect(self._on_error_ready)
        self.show_loading_signal.connect(self.show_loading)

    def show_loading(self, source_text: str):
        """Show popup with loading state."""
        # Truncate long text for display
        display_text = source_text[:150] + "..." if len(source_text) > 150 else source_text
        self.source_label.setText(f"📝 {display_text}")

        self.result_browser.hide()
        self.loading_label.show()
        self.loading_label.setText("⏳ Translating")
        self._loading_dots = 0
        self.loading_timer.start(500)

        self.status_label.setText("⏳ Processing...")
        self.copy_btn.setEnabled(False)
        self.close_btn.setEnabled(False)  # Disable close button during loading

        # Position near cursor
        self._position_near_cursor()
        self.show()
        self.raise_()
        self.activateWindow()
        self.setWindowState(Qt.WindowState.WindowActive)

    def _animate_loading(self):
        """Animate loading dots."""
        self._loading_dots = (self._loading_dots + 1) % 4
        dots = "." * self._loading_dots
        self.loading_label.setText(f"⏳ Translating{dots}")

    def update_result(self, result: str):
        """Thread-safe: emit signal to update result. Filters out GRAMMAR ANALYSIS section (robust)."""
        import re
        # Remove any GRAMMAR ANALYSIS section (with or without emoji, with or without markdown headers)
        pattern = r"(^|\n)#+ ?[🔍]?[ ]*GRAMMAR ANALYSIS[\s\S]*?(?=(\n#+ |\Z))"
        filtered_result = re.sub(pattern, '\n', result, flags=re.IGNORECASE)
        self.result_ready.emit(filtered_result)

    def show_error(self, error: str):
        """Thread-safe: emit signal to show error."""
        self.error_ready.emit(error)

    def _on_result_ready(self, result: str):
        """Update UI with translation result (main thread)."""
        self.loading_timer.stop()
        self.loading_label.hide()
        self.result_browser.show()

        # Convert markdown to HTML
        html = markdown.markdown(
            result,
            extensions=['extra', 'codehilite', 'nl2br']
        )

        # Add custom CSS for rendered markdown
        styled_html = f"""
        <style>
            body {{ color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }}
            h2 {{ color: #818cf8; margin-top: 16px; font-size: 15px; }}
            h3 {{ color: #a5b4fc; margin-top: 12px; font-size: 14px; }}
            ul {{ padding-left: 20px; }}
            li {{ margin: 4px 0; color: #cbd5e1; }}
            code {{ background: #252745; padding: 2px 6px; border-radius: 4px;
                    color: #fbbf24; font-family: 'Fira Code', monospace; }}
            strong {{ color: #f1f5f9; }}
            hr {{ border-color: #2d2f4e; }}
            p {{ line-height: 1.7; }}
        </style>
        {html}
        """

        self.result_browser.setHtml(styled_html)
        self._current_result = result
        self.status_label.setText("✅ Translation complete")
        self.copy_btn.setEnabled(True)
        self.close_btn.setEnabled(True)  # Re-enable close button

    def _on_error_ready(self, error: str):
        """Show error message (main thread)."""
        self.loading_timer.stop()
        self.loading_label.hide()
        self.result_browser.show()
        self.result_browser.setHtml(
            f'<p style="color: #ef4444; font-size: 14px;">❌ {error}</p>'
        )
        self.status_label.setText("❌ Error occurred")
        self.close_btn.setEnabled(True)  # Re-enable close button

    def _copy_result(self):
        """Copy result text to clipboard."""
        if hasattr(self, '_current_result'):
            clipboard = QApplication.clipboard()
            clipboard.setText(self._current_result)
            self.copy_btn.setText("✅ Copied!")
            QTimer.singleShot(2000, lambda: self.copy_btn.setText("📋 Copy"))

    def _position_near_cursor(self):
        """Position popup near mouse cursor."""
        # For debugging, position at center of screen instead
        screen = QApplication.primaryScreen()
        if screen:
            screen_geo = screen.availableGeometry()
            x = (screen_geo.width() - self.width()) // 2
            y = (screen_geo.height() - self.height()) // 2
            self.move(x, y)

    def mousePressEvent(self, event):
        """Enable window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        """Handle window dragging."""
        if hasattr(self, '_drag_pos') and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
