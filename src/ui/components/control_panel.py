"""
src/ui/components/control_panel.py
Kontrol paneli widget'ı
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

class ControlPanel(QWidget):
    """Kontrol paneli widget'ı"""
    
    # Sinyaller
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False
        self.init_ui()
        
    def init_ui(self):
        """UI oluştur"""
        group = QGroupBox("Kontrol Butonları")
        layout = QVBoxLayout(group)
        
        # Ana kontrol butonları
        main_buttons_layout = QHBoxLayout()
        
        # Başlat butonu
        self.start_button = QPushButton("Başlat")
        self.start_button.clicked.connect(self.on_start_clicked)
        self.start_button.setStyleSheet(self.get_button_style("#27ae60"))
        main_buttons_layout.addWidget(self.start_button)
        
        # Durdur butonu
        self.stop_button = QPushButton("Durdur")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet(self.get_button_style("#e74c3c"))
        main_buttons_layout.addWidget(self.stop_button)
        
        layout.addLayout(main_buttons_layout)
        
        # İkincil kontrol butonları
        secondary_buttons_layout = QHBoxLayout()
        
        # Duraklat/Devam butonu
        self.pause_button = QPushButton("Duraklat")
        self.pause_button.clicked.connect(self.on_pause_clicked)
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet(self.get_button_style("#f39c12"))
        secondary_buttons_layout.addWidget(self.pause_button)
        
        # Sıfırla butonu
        self.reset_button = QPushButton("Sıfırla")
        self.reset_button.clicked.connect(self.on_reset_clicked)
        self.reset_button.setStyleSheet(self.get_button_style("#9b59b6"))
        secondary_buttons_layout.addWidget(self.reset_button)
        
        layout.addLayout(secondary_buttons_layout)
        
        # Ana layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group)
        
    def get_button_style(self, color):
        """Buton stili döndür"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #7f8c8d;
                color: #bdc3c7;
            }}
        """
        
    def lighten_color(self, color):
        """Rengi açık ton yap"""
        color_map = {
            "#27ae60": "#2ecc71",
            "#e74c3c": "#f1c40f",
            "#f39c12": "#f1c40f",
            "#9b59b6": "#af7ac5"
        }
        return color_map.get(color, color)
        
    def darken_color(self, color):
        """Rengi koyu ton yap"""
        color_map = {
            "#27ae60": "#229954",
            "#e74c3c": "#c0392b",
            "#f39c12": "#d68910",
            "#9b59b6": "#8e44ad"
        }
        return color_map.get(color, color)
        
    def on_start_clicked(self):
        """Başlat butonuna tıklandığında"""
        self.is_running = True
        self.is_paused = False
        self.update_button_states()
        self.start_clicked.emit()
        
    def on_stop_clicked(self):
        """Durdur butonuna tıklandığında"""
        self.is_running = False
        self.is_paused = False
        self.update_button_states()
        self.stop_clicked.emit()
        
    def on_pause_clicked(self):
        """Duraklat butonuna tıklandığında"""
        if self.is_running:
            self.is_paused = not self.is_paused
            self.update_button_states()
            self.pause_clicked.emit()
            
    def on_reset_clicked(self):
        """Sıfırla butonuna tıklandığında"""
        self.reset_clicked.emit()
        
    def update_button_states(self):
        """Buton durumlarını güncelle"""
        if self.is_running:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.pause_button.setEnabled(True)
            
            if self.is_paused:
                self.pause_button.setText("Devam Et")
            else:
                self.pause_button.setText("Duraklat")
        else:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.pause_button.setEnabled(False)
            self.pause_button.setText("Duraklat")
            
    def reset_states(self):
        """Durumları sıfırla"""
        self.is_running = False
        self.is_paused = False
        self.update_button_states()