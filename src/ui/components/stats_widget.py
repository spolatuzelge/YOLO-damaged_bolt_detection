"""
src/ui/components/stats_widget.py
İstatistikler widget'ı
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import time

class StatsWidget(QWidget):
    """İstatistikler widget'ı"""
    
    def __init__(self):
        super().__init__()
        self.start_time = None
        self.stats_data = {}
        self.init_ui()
        
        # Timer for runtime update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_runtime)
        self.timer.start(1000)  # Her saniye güncelle
        
    def init_ui(self):
        """UI oluştur"""
        group = QGroupBox("İstatistikler")
        layout = QVBoxLayout(group)
        
        # Genel istatistikler
        general_layout = QVBoxLayout()
        
        # Çalışma süresi
        runtime_layout = QHBoxLayout()
        runtime_layout.addWidget(QLabel("Çalışma Süresi:"))
        self.runtime_label = QLabel("00:00:00")
        self.runtime_label.setStyleSheet("font-weight: bold; color: #2980b9;")
        runtime_layout.addWidget(self.runtime_label)
        runtime_layout.addStretch()
        general_layout.addLayout(runtime_layout)
        
        # Toplam tespit
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("Toplam Tespit:"))
        self.total_label = QLabel("0")
        self.total_label.setStyleSheet("font-weight: bold; color: #27ae60;")
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        general_layout.addLayout(total_layout)
        
        # Hasarlı tespit
        damaged_layout = QHBoxLayout()
        damaged_layout.addWidget(QLabel("Hasarlı Tespit:"))
        self.damaged_label = QLabel("0")
        self.damaged_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        damaged_layout.addWidget(self.damaged_label)
        damaged_layout.addStretch()
        general_layout.addLayout(damaged_layout)
        
        # Kaydedilen görüntü
        saved_layout = QHBoxLayout()
        saved_layout.addWidget(QLabel("Kaydedilen:"))
        self.saved_label = QLabel("0")
        self.saved_label.setStyleSheet("font-weight: bold; color: #f39c12;")
        saved_layout.addWidget(self.saved_label)
        saved_layout.addStretch()
        general_layout.addLayout(saved_layout)
        
        layout.addLayout(general_layout)
        
        # Performans istatistikleri
        perf_group = QGroupBox("Performans")
        perf_layout = QVBoxLayout(perf_group)
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_label = QLabel("0")
        self.fps_label.setStyleSheet("font-weight: bold; color: #9b59b6;")
        fps_layout.addWidget(self.fps_label)
        fps_layout.addStretch()
        perf_layout.addLayout(fps_layout)
        
        # Model güven eşiği
        conf_layout = QHBoxLayout()
        conf_layout.addWidget(QLabel("Güven Eşiği:"))
        self.conf_label = QLabel("50%")
        self.conf_label.setStyleSheet("font-weight: bold; color: #34495e;")
        conf_layout.addWidget(self.conf_label)
        conf_layout.addStretch()
        perf_layout.addLayout(conf_layout)
        
        # İşlem yükü (progress bar)
        load_layout = QVBoxLayout()
        load_layout.addWidget(QLabel("İşlem Yükü:"))
        self.load_progress = QProgressBar()
        self.load_progress.setRange(0, 100)
        self.load_progress.setValue(0)
        self.load_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        load_layout.addWidget(self.load_progress)
        perf_layout.addLayout(load_layout)
        
        layout.addWidget(perf_group)
        
        # Ana layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group)
        
    def update_stats(self, stats):
        """İstatistikleri güncelle"""
        self.stats_data = stats
        
        # Değerleri güncelle
        self.total_label.setText(str(stats.get('total_detections', 0)))
        self.damaged_label.setText(str(stats.get('damaged_count', 0)))
        self.saved_label.setText(str(stats.get('damaged_count', 0)))  # Kaydedilen = hasarlı
        self.fps_label.setText(f"{stats.get('fps', 0):.1f}")
        self.conf_label.setText(f"{stats.get('model_conf', 50)}%")
        
        # İşlem yükü (FPS'e göre tahmin)
        fps = stats.get('fps', 0)
        load_percentage = min(100, max(0, int((fps / 30) * 100)))
        self.load_progress.setValue(load_percentage)
        
        # Başlangıç zamanını ayarla
        if self.start_time is None:
            self.start_time = time.time()
            
    def update_runtime(self):
        """Çalışma süresini güncelle"""
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            runtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.runtime_label.setText(runtime_str)
            
    def reset_stats(self):
        """İstatistikleri sıfırla"""
        self.start_time = None
        self.stats_data = {}
        
        self.runtime_label.setText("00:00:00")
        self.total_label.setText("0")
        self.damaged_label.setText("0")
        self.saved_label.setText("0")
        self.fps_label.setText("0")
        self.conf_label.setText("50%")
        self.load_progress.setValue(0)
        
    def start_timing(self):
        """Zamanlama başlat"""
        self.start_time = time.time()
        
    def stop_timing(self):
        """Zamanlama durdur"""
        self.start_time = None