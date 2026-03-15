"""
System Tray
Tray icon with menu for TransDeep
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt


class SystemTray:
    """
    System tray icon with context menu.
    Features:
    - Show/hide popup
    - Change hotkey
    - Quit application
    """

    def __init__(self, app: QApplication, popup):
        self.app = app
        self.popup = popup
        self.tray = QSystemTrayIcon()

        self._setup_icon()
        self._setup_menu()

        # Double-click to show popup
        self.tray.activated.connect(self._on_activated)

    def _setup_icon(self):
        """Create tray icon (generated, no file needed)."""
        # Create a simple icon programmatically
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background circle
        painter.setBrush(QColor("#4f46e5"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(4, 4, 56, 56, 14, 14)

        # Text "T"
        painter.setPen(QColor("#ffffff"))
        font = QFont("Arial", 28, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "T")

        painter.end()

        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip("TransDeep - AI Deep Translation\nAlt+C to translate")

    def _setup_menu(self):
        """Create tray context menu."""
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #252745;
                color: #e2e8f0;
                border: 1px solid #3d3f6e;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #4f46e5;
            }
            QMenu::separator {
                background-color: #2d2f4e;
                height: 1px;
                margin: 4px 8px;
            }
        """)

        # Title (disabled, just for display)
        title_action = QAction("🌐 TransDeep v1.0", menu)
        title_action.setEnabled(False)
        menu.addAction(title_action)

        menu.addSeparator()

        # Show popup
        show_action = QAction("📖 Show Translator", menu)
        show_action.triggered.connect(self.popup.show)
        menu.addAction(show_action)

        menu.addSeparator()

        # Hotkey info
        hotkey_action = QAction("🎹 Hotkey: Alt+C", menu)
        hotkey_action.setEnabled(False)
        menu.addAction(hotkey_action)

        menu.addSeparator()

        # Quit
        quit_action = QAction("❌ Quit", menu)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)

    def _on_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.popup.show()
            self.popup.raise_()

    def show(self):
        """Show tray icon."""
        self.tray.show()
        # self.tray.showMessage(
        #     "TransDeep",
        #     "🚀 Running! Select text and press Alt+C",
        #     QSystemTrayIcon.MessageIcon.Information,
        #     3000
        # )
