"""
TransDeep UI Styles
Dark theme with modern design
"""

DARK_THEME = """
/* ══════════════════════════════════════════
   TransDeep Dark Theme
   ══════════════════════════════════════════ */

QWidget {
    background-color: #1a1b2e;
    color: #e2e8f0;
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', sans-serif;
    font-size: 13px;
}

/* ── Main Window ───────────────────────── */
QMainWindow, QDialog {
    background-color: #1a1b2e;
    border: 1px solid #2d2f4e;
    border-radius: 12px;
}

/* ── Labels ────────────────────────────── */
QLabel {
    color: #e2e8f0;
    background: transparent;
}

QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #818cf8;
}

QLabel#sourceLabel {
    font-size: 12px;
    color: #94a3b8;
    padding: 4px 8px;
    background-color: #252745;
    border-radius: 6px;
}

QLabel#statusLabel {
    font-size: 11px;
    color: #64748b;
}

/* ── Text Display ──────────────────────── */
QTextEdit, QTextBrowser {
    background-color: #0f1021;
    color: #e2e8f0;
    border: 1px solid #2d2f4e;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    line-height: 1.6;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

QTextBrowser a {
    color: #818cf8;
}

/* ── Buttons ───────────────────────────── */
QPushButton {
    background-color: #2d2f4e;
    color: #e2e8f0;
    border: 1px solid #3d3f6e;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #3d3f6e;
    border-color: #818cf8;
}

QPushButton:pressed {
    background-color: #4f46e5;
}

QPushButton#copyButton {
    background-color: #4f46e5;
    border-color: #6366f1;
    color: white;
}

QPushButton#copyButton:hover {
    background-color: #6366f1;
}

QPushButton#closeButton {
    background-color: transparent;
    border: none;
    color: #64748b;
    font-size: 18px;
    min-width: 32px;
    max-width: 32px;
    padding: 4px;
}

QPushButton#closeButton:hover {
    color: #ef4444;
    background-color: #2d2f4e;
    border-radius: 6px;
}

/* ── Combo Box ─────────────────────────── */
QComboBox {
    background-color: #252745;
    color: #e2e8f0;
    border: 1px solid #3d3f6e;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    min-width: 180px;
}

QComboBox:hover {
    border-color: #818cf8;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #252745;
    color: #e2e8f0;
    border: 1px solid #3d3f6e;
    border-radius: 6px;
    selection-background-color: #4f46e5;
}

/* ── Scroll Bar ────────────────────────── */
QScrollBar:vertical {
    background-color: #1a1b2e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #3d3f6e;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #818cf8;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ── Loading Animation ─────────────────── */
QLabel#loadingLabel {
    color: #818cf8;
    font-size: 14px;
    font-weight: bold;
}

/* ── Separator ─────────────────────────── */
QFrame#separator {
    background-color: #2d2f4e;
    max-height: 1px;
}

/* ── Menu ──────────────────────────────── */
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
"""

LIGHT_THEME = """
/* Light theme - Future implementation */
QWidget {
    background-color: #ffffff;
    color: #1e293b;
    font-family: 'Segoe UI', sans-serif;
}
"""
