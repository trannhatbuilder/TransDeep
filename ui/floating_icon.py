from PyQt6.QtWidgets import QWidget, QPushButton, QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QCursor

class FloatingIcon(QWidget):
    def __init__(self, on_click_callback):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(48, 48)
        self.button = QPushButton("🌐", self)
        self.button.setGeometry(0, 0, 48, 48)
        self.button.setStyleSheet("font-size: 28px; border-radius: 24px; background: #6366f1; color: white;")
        self.button.clicked.connect(on_click_callback)
        self.hide()

    def show_near_cursor(self):
        pos = QCursor.pos()
        self.move(pos + QPoint(20, 20))
        self.show()

    def hide_icon(self):
        self.hide()
