"""
src/ui/components/video_widget.py
Video görüntüleme widget'ı
"""

import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QFont

class VideoWidget(QWidget):
    """Video görüntüleme widget'ı"""
    
    frame_clicked = pyqtSignal(tuple)  # (x, y) koordinatları
    
    def __init__(self, title="Video"):
        super().__init__()
        self.title = title
        self.current_frame = None
        self.init_ui()
        
    def init_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Başlık
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                border-radius: 5px;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title_label)
        
        # Video görüntü alanı
        self.video_label = QLabel()
        self.video_label.setMinimumSize(480, 360)
        self.video_label.setScaledContents(True)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 10px;
                color: white;
                font-size: 14px;
            }
        """)
        self.video_label.setText("Video bekleniyor...")
        self.video_label.mousePressEvent = self.on_video_click
        
        layout.addWidget(self.video_label)
        
        # Durum bilgisi
        self.status_label = QLabel("Hazır")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #27ae60;
                color: white;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
    def update_frame(self, frame):
        """Frame'i güncelle"""
        try:
            if frame is None:
                return
                
            self.current_frame = frame.copy()
            
            # OpenCV BGR'den RGB'ye çevir
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # QImage oluştur
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # QPixmap'e çevir ve göster
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)
            
            # Durum güncelle
            self.status_label.setText(f"Aktif - {w}x{h}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #27ae60;
                    color: white;
                    padding: 5px;
                    border-radius: 3px;
                    font-weight: bold;
                }
            """)
            
        except Exception as e:
            self.show_error(f"Frame güncelleme hatası: {str(e)}")
            
    def show_error(self, error_message):
        """Hata göster"""
        self.video_label.setText(f"HATA:\n{error_message}")
        self.status_label.setText("Hata")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #e74c3c;
                color: white;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
        """)
        
    def show_waiting(self):
        """Bekleme durumu göster"""
        self.video_label.setText("Video bekleniyor...")
        self.status_label.setText("Bekleniyor")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #f39c12;
                color: white;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
        """)
        
    def on_video_click(self, event):
        """Video tıklandığında"""
        if self.current_frame is not None:
            # Tıklanan pozisyonu al
            pos = event.position()
            x, y = int(pos.x()), int(pos.y())
            
            # Gerçek frame koordinatlarına çevir
            label_size = self.video_label.size()
            frame_h, frame_w = self.current_frame.shape[:2]
            
            # Ölçekleme faktörlerini hesapla
            scale_x = frame_w / label_size.width()
            scale_y = frame_h / label_size.height()
            
            # Gerçek koordinatlar
            real_x = int(x * scale_x)
            real_y = int(y * scale_y)
            
            # Sinyal gönder
            self.frame_clicked.emit((real_x, real_y))
            
    def clear(self):
        """Widget'ı temizle"""
        self.video_label.clear()
        self.video_label.setText("Video bekleniyor...")
        self.current_frame = None
        self.show_waiting()