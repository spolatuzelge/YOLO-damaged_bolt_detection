"""
src/utils/styles.py
PyQt6 için stil tanımlamaları
"""

# Ana uygulama stili
MAIN_STYLE = """
QMainWindow {
    background-color: #ecf0f1;
    color: #2c3e50;
}

QWidget {
    background-color: #ecf0f1;
    color: #2c3e50;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #bdc3c7;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #2c3e50;
    font-weight: bold;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-height: 15px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #7f8c8d;
    color: #bdc3c7;
}

QLabel {
    color: #2c3e50;
    font-size: 12px;
}

QComboBox {
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px 10px;
    background-color: white;
    min-width: 100px;
}

QComboBox:hover {
    border-color: #3498db;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 1px;
    border-left-color: #bdc3c7;
    border-left-style: solid;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QComboBox::down-arrow {
    image: url(down_arrow.png);
    width: 10px;
    height: 10px;
}

QSpinBox {
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px;
    background-color: white;
    min-width: 80px;
}

QSpinBox:hover {
    border-color: #3498db;
}

QTextEdit {
    border: 2px solid #bdc3c7;
    border-radius: 6px;
    background-color: #ffffff;
    padding: 8px;
    font-family: 'Consolas', monospace;
    font-size: 11px;
}

QProgressBar {
    border: 2px solid #bdc3c7;
    border-radius: 6px;
    text-align: center;
    font-weight: bold;
    background-color: #ecf0f1;
}

QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 4px;
}

QFrame {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 8px;
}

QSplitter::handle {
    background-color: #bdc3c7;
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 6px;
}

QSplitter::handle:vertical {
    height: 6px;
}

QScrollBar:vertical {
    background-color: #ecf0f1;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #bdc3c7;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #95a5a6;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QToolTip {
    background-color: #2c3e50;
    color: white;
    border: 1px solid #34495e;
    border-radius: 4px;
    padding: 4px;
    font-size: 11px;
}
"""

# Özel buton stilleri
BUTTON_STYLES = {
    'success': """
        QPushButton {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 12px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #2ecc71;
        }
        QPushButton:pressed {
            background-color: #229954;
        }
        QPushButton:disabled {
            background-color: #7f8c8d;
            color: #bdc3c7;
        }
    """,
    
    'danger': """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 12px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #f1c40f;
        }
        QPushButton:pressed {
            background-color: #c0392b;
        }
        QPushButton:disabled {
            background-color: #7f8c8d;
            color: #bdc3c7;
        }
    """,
    
    'warning': """
        QPushButton {
            background-color: #f39c12;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 12px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #f1c40f;
        }
        QPushButton:pressed {
            background-color: #d68910;
        }
        QPushButton:disabled {
            background-color: #7f8c8d;
            color: #bdc3c7;
        }
    """,
    
    'info': """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 12px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #5dade2;
        }
        QPushButton:pressed {
            background-color: #2980b9;
        }
        QPushButton:disabled {
            background-color: #7f8c8d;
            color: #bdc3c7;
        }
    """,
    
    'purple': """
        QPushButton {
            background-color: #9b59b6;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 12px;
            min-height: 20px;
        }
        QPushButton:hover {
            background-color: #af7ac5;
        }
        QPushButton:pressed {
            background-color: #8e44ad;
        }
        QPushButton:disabled {
            background-color: #7f8c8d;
            color: #bdc3c7;
        }
    """
}

# Video widget stilleri
VIDEO_WIDGET_STYLE = """
QWidget {
    background-color: #2c3e50;
    border-radius: 10px;
}

QLabel {
    background-color: #34495e;
    border: 2px solid #3498db;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    font-weight: bold;
    padding: 20px;
}
"""

# Log widget stilleri
LOG_WIDGET_STYLE = """
QTextEdit {
    background-color: #2c3e50;
    color: #ecf0f1;
    border: 2px solid #34495e;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    padding: 8px;
}

QScrollBar:vertical {
    background-color: #34495e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #7f8c8d;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #95a5a6;
}
"""

# İstatistik widget stilleri
STATS_WIDGET_STYLE = """
QGroupBox {
    font-weight: bold;
    border: 2px solid #3498db;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 15px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    color: #2c3e50;
    font-weight: bold;
    font-size: 13px;
}

QLabel {
    color: #2c3e50;
    font-size: 12px;
}

QProgressBar {
    border: 2px solid #bdc3c7;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    background-color: #ecf0f1;
    min-height: 20px;
}

QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 3px;
}
"""

def apply_dark_theme():
    """Koyu tema stilleri"""
    return """
    QMainWindow, QWidget {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    
    QGroupBox {
        border: 2px solid #34495e;
        background-color: #34495e;
        color: #ecf0f1;
    }
    
    QTextEdit {
        background-color: #2c3e50;
        color: #ecf0f1;
        border: 2px solid #34495e;
    }
    
    QComboBox, QSpinBox {
        background-color: #34495e;
        color: #ecf0f1;
        border: 2px solid #7f8c8d;
    }
    """

def get_status_style(status_type):
    """Durum renkleri"""
    status_colors = {
        'success': '#27ae60',
        'error': '#e74c3c', 
        'warning': '#f39c12',
        'info': '#3498db',
        'default': '#7f8c8d'
    }
    
    color = status_colors.get(status_type, status_colors['default'])
    
    return f"""
    QLabel {{
        background-color: {color};
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
    }}
    """