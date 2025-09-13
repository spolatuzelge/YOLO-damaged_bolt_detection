"""
YOLO Hasarlı Cıvata Tespit Sistemi
Ana uygulama dosyası
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

# Yerel modülleri import et
from src.ui.main_window import MainWindow
from src.core.config import Config
from src.utils.logger import setup_logger

class CivataDetectionApp(QApplication):
    """Ana uygulama sınıfı"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Uygulama ayarları
        self.setApplicationName("YOLO Cıvata Tespit Sistemi")
        self.setApplicationVersion("1.0")
        self.setOrganizationName("YourCompany")
        
        # Gerekli klasörleri kontrol et ve oluştur
        self.ensure_directories()
        
        # Logger'ı başlat
        self.logger = setup_logger()
        
        # Konfigürasyonu yükle
        self.config = Config()
        
        # Ana pencereyi oluştur
        self.main_window = None
        self.init_ui()
        
    def ensure_directories(self):
        """Gerekli klasörleri kontrol et ve oluştur"""
        directories = [
            "src/models",
            "src/source",
            "src/core", 
            "src/ui/components",
            "src/utils",
            "data/cropped",
            "logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Bugünün klasörünü oluştur
        today_folder = datetime.now().strftime("%d%m%Y")
        today_path = Path(f"src/source/{today_folder}")
        today_path.mkdir(parents=True, exist_ok=True)
        
    def init_ui(self):
        """UI'yi başlat"""
        try:
            self.main_window = MainWindow(self.config)
            self.main_window.show()
            self.logger.info("Uygulama başarıyla başlatıldı")
        except Exception as e:
            self.logger.error(f"UI başlatma hatası: {e}")
            sys.exit(1)

def main():
    """Ana fonksiyon"""
    # Gerekli dizinleri oluştur
    os.makedirs("src/models", exist_ok=True)
    os.makedirs("data/cropped", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Bugünün klasörünü oluştur
    today_folder = datetime.now().strftime("%d%m%Y")
    os.makedirs(f"src/source/{today_folder}", exist_ok=True)
    
    app = CivataDetectionApp(sys.argv)
    
    # Uygulama stilini ayarla
    app.setStyle('Fusion')
    
    # Ana döngüyü başlat
    sys.exit(app.exec())

if __name__ == "__main__":
    main()