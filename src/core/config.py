"""
src/core/config.py
Uygulama konfigürasyon sınıfı
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Union

class Config:
    """Uygulama konfigürasyon sınıfı"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        
        # Varsayılan değerler
        self.model_path = ""
        self.confidence_threshold = 50  # %50
        self.iou_threshold = 0.45
        self.source_count = 1
        self.sources = {}  # {index: source_path_or_camera_id}
        
        # Klasör yolları
        self.output_dir = "data/outputs"
        self.cropped_dir = "data/cropped"
        self.models_dir = "data/models"
        self.logs_dir = "logs"
        
        # Video kayıt ayarları
        self.record_video = True
        self.video_fps = 30
        self.video_codec = "mp4v"
        
        # Tespit ayarları
        self.max_det = 300  # Maksimum tespit sayısı
        self.track_thresh = 0.5  # Tracking eşiği
        self.track_buffer = 30  # Tracking buffer
        self.match_thresh = 0.8  # Matching eşiği
        
        # UI ayarları
        self.window_width = 1400
        self.window_height = 900
        self.video_width = 640
        self.video_height = 480
        
        # Sınıf bilgileri
        self.class_names = ["Hasarsız", "Hasarlı"]
        self.class_colors = [(0, 255, 0), (0, 0, 255)]  # BGR format
        
        # Konfigürasyonu yükle
        self.load_config()
        
    def load_config(self):
        """Konfigürasyon dosyasından ayarları yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    
                # Değerleri güncelle
                for key, value in config_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                        
                print(f"Konfigürasyon yüklendi: {self.config_file}")
            else:
                print("Konfigürasyon dosyası bulunamadı, varsayılan değerler kullanılıyor")
                self.save_config()  # Varsayılan konfigürasyonu kaydet
                
        except Exception as e:
            print(f"Konfigürasyon yükleme hatası: {e}")
            print("Varsayılan değerler kullanılıyor")
            
    def save_config(self):
        """Konfigürasyonu dosyaya kaydet"""
        try:
            # Kaydedilecek değerleri hazırla
            config_data = {
                'model_path': self.model_path,
                'confidence_threshold': self.confidence_threshold,
                'iou_threshold': self.iou_threshold,
                'source_count': self.source_count,
                'sources': self.sources,
                'output_dir': self.output_dir,
                'cropped_dir': self.cropped_dir,
                'models_dir': self.models_dir,
                'logs_dir': self.logs_dir,
                'record_video': self.record_video,
                'video_fps': self.video_fps,
                'video_codec': self.video_codec,
                'max_det': self.max_det,
                'track_thresh': self.track_thresh,
                'track_buffer': self.track_buffer,
                'match_thresh': self.match_thresh,
                'window_width': self.window_width,
                'window_height': self.window_height,
                'video_width': self.video_width,
                'video_height': self.video_height,
                'class_names': self.class_names,
                'class_colors': self.class_colors
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
                
            print(f"Konfigürasyon kaydedildi: {self.config_file}")
            
        except Exception as e:
            print(f"Konfigürasyon kaydetme hatası: {e}")
            
    def validate_model_path(self):
        """Model dosyasının geçerliliğini kontrol et"""
        if not self.model_path:
            return False, "Model dosyası seçilmedi"
            
        if not os.path.exists(self.model_path):
            return False, f"Model dosyası bulunamadı: {self.model_path}"
            
        valid_extensions = ['.pt', '.onnx', '.engine']
        if not any(self.model_path.lower().endswith(ext) for ext in valid_extensions):
            return False, f"Desteklenmeyen model formatı. Desteklenen: {valid_extensions}"
            
        return True, "Model dosyası geçerli"
        
    def validate_sources(self):
        """Kaynakların geçerliliğini kontrol et"""
        if not self.sources:
            return False, "Hiç kaynak seçilmedi"
            
        for i in range(self.source_count):
            if i not in self.sources:
                return False, f"Kaynak {i+1} seçilmedi"
                
            source = self.sources[i]
            
            # Video dosyası kontrolü
            if isinstance(source, str):
                if not os.path.exists(source):
                    return False, f"Video dosyası bulunamadı: {source}"
                    
                valid_video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
                if not any(source.lower().endswith(ext) for ext in valid_video_extensions):
                    return False, f"Desteklenmeyen video formatı: {source}"
                    
            # Kamera ID kontrolü
            elif isinstance(source, int):
                if source < 0:
                    return False, f"Geçersiz kamera ID: {source}"
                    
        return True, "Tüm kaynaklar geçerli"
        
    def ensure_directories(self):
        """Gerekli klasörleri oluştur"""
        directories = [
            self.output_dir,
            self.cropped_dir,
            self.models_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                print(f"Klasör hazırlandı: {directory}")
            except Exception as e:
                print(f"Klasör oluşturma hatası ({directory}): {e}")
                
    def get_output_filename(self, source_id, extension="mp4"):
        """Çıktı dosyası adı oluştur"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"output_src{source_id}_{timestamp}.{extension}"
        
    def get_cropped_filename(self, source_id, track_id, extension="jpg"):
        """Kırpılmış görüntü dosyası adı oluştur"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        return f"damaged_bolt_src{source_id}_id{track_id}_{timestamp}.{extension}"
        
    def update_source(self, index, source):
        """Belirli bir kaynağı güncelle"""
        if 0 <= index < self.source_count:
            self.sources[index] = source
            self.save_config()
        else:
            raise ValueError(f"Geçersiz kaynak indeksi: {index}")
            
    def remove_source(self, index):
        """Belirli bir kaynağı kaldır"""
        if index in self.sources:
            del self.sources[index]
            self.save_config()
            
    def clear_sources(self):
        """Tüm kaynakları temizle"""
        self.sources.clear()
        self.save_config()
        
    def get_tracker_config(self):
        """Tracker konfigürasyonu döndür"""
        return {
            'track_thresh': self.track_thresh,
            'track_buffer': self.track_buffer,
            'match_thresh': self.match_thresh,
            'frame_rate': self.video_fps
        }
        
    def get_detection_config(self):
        """Tespit konfigürasyonu döndür"""
        return {
            'conf': self.confidence_threshold / 100,
            'iou': self.iou_threshold,
            'max_det': self.max_det,
            'classes': None,  # Tüm sınıflar
            'agnostic_nms': False,
            'retina_masks': False
        }
        
    def __str__(self):
        """Konfigürasyon bilgilerini string olarak döndür"""
        return f"""
Konfigürasyon Bilgileri:
- Model: {self.model_path or 'Seçilmedi'}
- Güven Eşiği: {self.confidence_threshold}%
- IoU Eşiği: {self.iou_threshold}
- Kaynak Sayısı: {self.source_count}
- Kaynaklar: {self.sources}
- Çıktı Klasörü: {self.output_dir}
- Kırpılmış Klasörü: {self.cropped_dir}
- Video Kaydı: {'Aktif' if self.record_video else 'Pasif'}
- Video FPS: {self.video_fps}
        """