"""
src/ui/main_window.py
Ana pencere UI sınıfı
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QLabel, QComboBox, QSpinBox, QGroupBox,
                             QFileDialog, QMessageBox, QProgressBar, QTextEdit,
                             QSplitter, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QFont, QIcon

from .components.video_widget import VideoWidget
from .components.control_panel import ControlPanel
from .components.stats_widget import StatsWidget
from ..core.detection_thread import DetectionThread
from ..utils.styles import MAIN_STYLE

class MainWindow(QMainWindow):
    """Ana pencere sınıfı"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.detection_thread = None
        self.video_widgets = []
        self.source_count = 1
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """UI bileşenlerini oluştur"""
        self.setWindowTitle("YOLO Hasarlı Cıvata Tespit Sistemi v1.0")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Sol panel (kontroller)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 0)
        
        # Sağ panel (video görüntüleme)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
        # Stil uygula
        self.setStyleSheet(MAIN_STYLE)
        
    def create_left_panel(self):
        """Sol kontrol panelini oluştur"""
        panel = QFrame()
        panel.setFixedWidth(350)
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # Başlık
        title = QLabel("Kontrol Paneli")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Model seçimi grubu
        model_group = self.create_model_group()
        layout.addWidget(model_group)
        
        # Kaynak seçimi grubu
        source_group = self.create_source_group()
        layout.addWidget(source_group)
        
        # Kontrol butonları
        control_panel = ControlPanel()
        self.control_panel = control_panel
        layout.addWidget(control_panel)
        
        # İstatistikler
        stats_widget = StatsWidget()
        self.stats_widget = stats_widget
        layout.addWidget(stats_widget)
        
        # Log alanı
        log_group = self.create_log_group()
        layout.addWidget(log_group)
        
        layout.addStretch()
        return panel
        
    def create_model_group(self):
        """Model seçim grubunu oluştur"""
        group = QGroupBox("Model Ayarları")
        layout = QVBoxLayout(group)
        
        # Model dosyası seçimi
        model_layout = QHBoxLayout()
        self.model_path_label = QLabel("Model seçilmedi")
        self.model_path_label.setWordWrap(True)
        model_button = QPushButton("Model Seç")
        model_button.clicked.connect(self.select_model)
        
        model_layout.addWidget(self.model_path_label, 1)
        model_layout.addWidget(model_button)
        layout.addLayout(model_layout)
        
        # Güven eşiği
        conf_layout = QHBoxLayout()
        conf_layout.addWidget(QLabel("Güven Eşiği:"))
        self.conf_spinbox = QSpinBox()
        self.conf_spinbox.setRange(1, 100)
        self.conf_spinbox.setValue(50)
        self.conf_spinbox.setSuffix("%")
        conf_layout.addWidget(self.conf_spinbox)
        layout.addLayout(conf_layout)
        
        return group
        
    def create_source_group(self):
        """Kaynak seçim grubunu oluştur"""
        group = QGroupBox("Kaynak Ayarları")
        layout = QVBoxLayout(group)
        
        # Kaynak tipi
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Kaynak Tipi:"))
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Kamera", "Video Dosyası"])
        self.source_combo.currentTextChanged.connect(self.on_source_type_changed)
        source_layout.addWidget(self.source_combo)
        layout.addLayout(source_layout)
        
        # Kaynak sayısı
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Kaynak Sayısı:"))
        self.source_count_combo = QComboBox()
        self.source_count_combo.addItems(["1", "2"])
        self.source_count_combo.currentTextChanged.connect(self.on_source_count_changed)
        count_layout.addWidget(self.source_count_combo)
        layout.addLayout(count_layout)
        
        # Kaynak seçimi butonları
        self.source_buttons_layout = QVBoxLayout()
        self.update_source_buttons()
        layout.addLayout(self.source_buttons_layout)
        
        return group
        
    def create_log_group(self):
        """Log grubu oluştur"""
        group = QGroupBox("Sistem Logları")
        layout = QVBoxLayout(group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        return group
        
    def create_right_panel(self):
        """Sağ video panelini oluştur"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        self.video_layout = QVBoxLayout(panel)
        self.video_layout.setSpacing(10)
        
        # Başlangıçta bir video widget'ı oluştur
        self.update_video_widgets()
        
        return panel
        
    def update_video_widgets(self):
        """Video widget'larını güncelle"""
        # Mevcut widget'ları temizle
        for widget in self.video_widgets:
            widget.deleteLater()
        self.video_widgets.clear()
        
        # Yeni widget'lar oluştur
        for i in range(self.source_count):
            video_widget = VideoWidget(f"Kaynak {i+1}")
            self.video_widgets.append(video_widget)
            self.video_layout.addWidget(video_widget)
            
    def update_source_buttons(self):
        """Kaynak seçim butonlarını güncelle"""
        # Mevcut butonları temizle
        for i in reversed(range(self.source_buttons_layout.count())):
            child = self.source_buttons_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        # Yeni butonlar oluştur
        for i in range(self.source_count):
            button = QPushButton(f"Kaynak {i+1} Seç")
            button.clicked.connect(lambda checked, idx=i: self.select_source(idx))
            self.source_buttons_layout.addWidget(button)
            
    def select_model(self):
        """Model dosyası seç"""
        # Varsayılan olarak src/models klasörünü aç
        default_path = "src/models"
        if not os.path.exists(default_path):
            os.makedirs(default_path, exist_ok=True)
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "YOLO Model Dosyası Seç",
            default_path,  # Başlangıç klasörü
            "Model Dosyaları (*.pt *.onnx);;PyTorch Modeli (*.pt);;ONNX Modeli (*.onnx);;Tüm Dosyalar (*)"
        )
        
        if file_path:
            # Model uyumluluğunu kontrol et
            from ..utils.model_loader import check_model_compatibility
            
            compatibility = check_model_compatibility(file_path)
            
            if not compatibility['compatible']:
                warnings_text = '\n'.join(compatibility['warnings'])
                reply = QMessageBox.question(
                    self, 
                    "Model Uyarısı", 
                    f"Model dosyasında sorunlar tespit edildi:\n\n{warnings_text}\n\nYine de devam etmek istiyor musunuz?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
            
            model_filename = os.path.basename(file_path)
            self.model_path_label.setText(f"Model: {model_filename} ({compatibility['size_mb']} MB)")
            self.config.model_path = file_path
            
            # Uyumluluk bilgilerini logla
            self.log_message(f"Model seçildi: {model_filename}")
            self.log_message(f"Format: {compatibility['format']}, Boyut: {compatibility['size_mb']} MB")
            
            if compatibility['warnings']:
                for warning in compatibility['warnings']:
                    self.log_message(f"UYARI: {warning}")
            else:
                self.log_message("✅ Model uyumluluk kontrolü başarılı")
            
    def select_source(self, index):
        """Kaynak seç"""
        source_type = self.source_combo.currentText()
        
        if source_type == "Video Dosyası":
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                f"Video Dosyası Seç - Kaynak {index+1}",
                "",
                "Video Dosyaları (*.mp4 *.avi *.mov *.mkv);;Tüm Dosyalar (*)"
            )
            
            if file_path:
                # Video dosyası seçildi
                self.config.sources[index] = file_path
                
                # Kullanıcıya bilgi ver
                filename = os.path.basename(file_path)
                from datetime import datetime
                today_folder = datetime.now().strftime("%d%m%Y")
                
                self.log_message(f"Video seçildi: {filename}")
                self.log_message(f"Video çalışma sırasında src/source/{today_folder}/ klasörüne kopyalanacak")
                
        else:
            # Kamera seçimi için dialog
            camera_id, ok = self.get_camera_id()
            if ok:
                self.config.sources[index] = camera_id
                from datetime import datetime
                today_folder = datetime.now().strftime("%d%m%Y")
                
                self.log_message(f"Kamera {camera_id} seçildi (Kaynak {index+1})")
                self.log_message(f"Kamera kaydı src/source/{today_folder}/ klasörüne yapılacak")
                
    def get_camera_id(self):
        """Kamera ID seçimi için basit dialog"""
        from PyQt6.QtWidgets import QInputDialog
        
        camera_id, ok = QInputDialog.getInt(
            self, 
            "Kamera Seçimi", 
            "Kamera ID (genellikle 0, 1, 2...):",
            0, 0, 10, 1
        )
        
        return camera_id, ok
        
    def on_source_type_changed(self, source_type):
        """Kaynak tipi değiştiğinde"""
        self.log_message(f"Kaynak tipi değiştirildi: {source_type}")
        
    def on_source_count_changed(self, count):
        """Kaynak sayısı değiştiğinde"""
        self.source_count = int(count)
        self.config.source_count = self.source_count
        self.update_video_widgets()
        self.update_source_buttons()
        self.log_message(f"Kaynak sayısı değiştirildi: {count}")
        
    def setup_connections(self):
        """Sinyal bağlantılarını kur"""
        if hasattr(self, 'control_panel'):
            self.control_panel.start_clicked.connect(self.start_detection)
            self.control_panel.stop_clicked.connect(self.stop_detection)
            self.control_panel.pause_clicked.connect(self.pause_detection)
            
    def start_detection(self):
        """Tespit işlemini başlat"""
        if not self.config.model_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir model seçin!")
            return
            
        if not self.config.sources:
            QMessageBox.warning(self, "Uyarı", "Lütfen kaynak seçin!")
            return
        
        # Model dosyası kontrolü
        if not os.path.exists(self.config.model_path):
            QMessageBox.critical(self, "Hata", f"Model dosyası bulunamadı:\n{self.config.model_path}")
            return
            
        try:
            self.log_message("Tespit işlemi başlatılıyor...")
            self.log_message(f"Model: {self.config.model_path}")
            self.log_message(f"Kaynak sayısı: {self.config.source_count}")
            
            # Tespit thread'ini oluştur ve başlat
            self.detection_thread = DetectionThread(self.config)
            self.detection_thread.frame_ready.connect(self.update_frame)
            self.detection_thread.detection_stats.connect(self.update_stats)
            self.detection_thread.log_message.connect(self.log_message)
            self.detection_thread.error_occurred.connect(self.handle_error)
            
            self.detection_thread.start()
            self.log_message("Tespit işlemi başlatıldı")
            
            # UI durumunu güncelle
            if hasattr(self, 'control_panel'):
                self.control_panel.is_running = True
                self.control_panel.update_button_states()
            
        except Exception as e:
            self.handle_error(f"Tespit başlatma hatası: {str(e)}")
            self.log_message(f"Detaylı hata: {repr(e)}")
            
    def stop_detection(self):
        """Tespit işlemini durdur"""
        if self.detection_thread and self.detection_thread.isRunning():
            self.detection_thread.stop()
            self.detection_thread.wait()
            self.log_message("Tespit işlemi durduruldu")
            
    def pause_detection(self):
        """Tespit işlemini duraklat/devam ettir"""
        if self.detection_thread:
            self.detection_thread.toggle_pause()
            status = "duraklatıldı" if self.detection_thread.is_paused else "devam ettirildi"
            self.log_message(f"Tespit işlemi {status}")
            
    def update_frame(self, frame_data):
        """Frame'i güncelle"""
        source_id, frame = frame_data
        if source_id < len(self.video_widgets):
            self.video_widgets[source_id].update_frame(frame)
            
    def update_stats(self, stats):
        """İstatistikleri güncelle"""
        if hasattr(self, 'stats_widget'):
            self.stats_widget.update_stats(stats)
            
    def log_message(self, message):
        """Log mesajı ekle"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.append(formatted_message)
        
        # Auto-scroll
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def handle_error(self, error_message):
        """Hata işleme"""
        self.log_message(f"HATA: {error_message}")
        QMessageBox.critical(self, "Hata", error_message)
        
    def closeEvent(self, event):
        """Pencere kapatılırken"""
        if self.detection_thread and self.detection_thread.isRunning():
            self.detection_thread.stop()
            self.detection_thread.wait()
        event.accept()