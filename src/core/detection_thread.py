"""
src/core/detection_thread.py
YOLO model ile tespit işlemlerini yapan thread sınıfı
"""

import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
import time
import os

from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
from ultralytics import YOLO
from collections import defaultdict
from ..utils.model_loader import load_yolo_model_safe

class DetectionThread(QThread):
    """YOLO tespit işlemlerini yapan thread"""
    
    # Sinyaller
    frame_ready = pyqtSignal(tuple)  # (source_id, frame)
    detection_stats = pyqtSignal(dict)  # istatistikler
    log_message = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.model = None
        self.caps = []
        self.is_running = False
        self.is_paused = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        
        # Takip için değişkenler
        self.trackers = []
        self.tracked_objects = defaultdict(dict)  # {source_id: {track_id: info}}
        self.damage_count = 0
        self.total_detections = 0
        
        # Video kayıt için
        self.video_writers = []
        self.should_record = False
        
        # Sınıf adları
        self.class_names = ["Hasarlı","Hasarsız"]
        
    def run(self):
        """Ana thread döngüsü"""
        try:
            self.is_running = True
            self.log_message.emit("Thread başlatıldı")
            
            # Model yükle
            if not self.load_model():
                return
                
            # Kaynakları başlat
            if not self.init_sources():
                return
                
            # Ana işlem döngüsü
            self.process_loop()
            
        except Exception as e:
            self.error_occurred.emit(f"Thread hatası: {str(e)}")
        finally:
            self.cleanup()
            
    def load_model(self):
        """YOLO modelini yükle - basit versiyon"""
        try:
            self.log_message.emit(f"Model yükleniyor: {self.config.model_path}")
            
            # Model dosyası kontrolü
            if not os.path.exists(self.config.model_path):
                raise Exception(f"Model dosyası bulunamadı: {self.config.model_path}")
            
            # Basit model yükleme
            self.model = load_yolo_model_safe(self.config.model_path)
            
            # Basit model kontrolü
            if self.model is None:
                raise Exception("Model yüklenemedi")
            
            self.log_message.emit("✅ Model başarıyla yüklendi")
            
            # Model sınıflarını logla
            if hasattr(self.model, 'names'):
                self.log_message.emit(f"Model sınıfları: {self.model.names}")
            
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Model yükleme hatası: {str(e)}")
            return False
            
    def init_sources(self):
        """Video kaynaklarını başlat"""
        try:
            self.caps = []
            self.video_writers = []
            
            # Bugünün klasörünü oluştur
            from datetime import datetime
            today_folder = datetime.now().strftime("%d%m%Y")
            self.source_dir = f"src/source/{today_folder}"
            os.makedirs(self.source_dir, exist_ok=True)
            
            # Sources dictionary'den değerleri al
            source_list = []
            for i in range(self.config.source_count):
                if i in self.config.sources:
                    source_list.append(self.config.sources[i])
                else:
                    self.error_occurred.emit(f"Kaynak {i} tanımlanmamış!")
                    return False
            
            for i, source in enumerate(source_list):
                processed_source = source
                
                if isinstance(source, str):
                    # Video dosyası - klasöre kopyala
                    if os.path.exists(source):
                        import shutil
                        filename = os.path.basename(source)
                        # Aynı isimde dosya varsa üzerine yazma
                        target_path = os.path.join(self.source_dir, filename)
                        
                        if not os.path.exists(target_path):
                            shutil.copy2(source, target_path)
                            self.log_message.emit(f"Video kopyalandı: {target_path}")
                        else:
                            self.log_message.emit(f"Video zaten mevcut: {target_path}")
                        
                        processed_source = target_path
                    
                    cap = cv2.VideoCapture(processed_source)
                    self.log_message.emit(f"Video dosyası açıldı: {processed_source}")
                    
                elif isinstance(source, int):
                    # Kamera
                    cap = cv2.VideoCapture(source)
                    self.should_record = True
                    self.log_message.emit(f"Kamera {source} açıldı")
                    processed_source = source
                    
                if not cap.isOpened():
                    self.error_occurred.emit(f"Kaynak {i} açılamadı: {processed_source}")
                    return False
                    
                # Video özelliklerini ayarla
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)
                
                self.caps.append(cap)
                
                # Video kayıt için writer oluştur (sadece kamera için)
                if isinstance(source, int) and self.should_record:
                    self.init_video_writer(i, cap)
                else:
                    self.video_writers.append(None)
                    
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Kaynak başlatma hatası: {str(e)}")
            return False
            
    def init_video_writer(self, source_id, cap):
        """Video kayıt için writer oluştur"""
        try:
            # Çıktı dosyası adı - kaynak klasörüne kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"camera_{source_id}_{timestamp}.mp4"
            output_path = os.path.join(self.source_dir, output_filename)
            
            # Video özelliklerini al
            fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Writer oluştur
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            if writer.isOpened():
                self.video_writers.append(writer)
                self.log_message.emit(f"Video kaydı başlatıldı: {output_path}")
            else:
                self.video_writers.append(None)
                self.log_message.emit(f"Video writer oluşturulamadı: {output_path}")
                
        except Exception as e:
            self.video_writers.append(None)
            self.log_message.emit(f"Video writer hatası: {str(e)}")
            
    def process_loop(self):
        """Ana işlem döngüsü"""
        while self.is_running:
            # Pause kontrolü
            self.mutex.lock()
            if self.is_paused:
                self.condition.wait(self.mutex)
            self.mutex.unlock()
            
            if not self.is_running:
                break
                
            # Her kaynaktan frame al ve işle
            for source_id, cap in enumerate(self.caps):
                if not self.is_running:
                    break
                    
                ret, frame = cap.read()
                if not ret:
                    self.log_message.emit(f"Kaynak {source_id} frame alınamadı")
                    continue
                    
                # Frame'i işle
                processed_frame = self.process_frame(frame, source_id)
                
                # Tarih damgası ekle (kamera için)
                if source_id < len(self.video_writers) and self.video_writers[source_id]:
                    processed_frame = self.add_timestamp(processed_frame)
                    
                # Video kaydet (kamera için)
                if source_id < len(self.video_writers) and self.video_writers[source_id]:
                    self.video_writers[source_id].write(processed_frame)
                    
                # UI'ye gönder
                self.frame_ready.emit((source_id, processed_frame))
                
            # FPS kontrolü
            time.sleep(1/30)  # ~30 FPS
            
    def process_frame(self, frame, source_id):
        """Frame'i YOLO ile işle"""
        try:
            # YOLO ile tespit yap
            results = self.model.track(
                frame, 
                conf=self.config.confidence_threshold/100,
                persist=True,
                tracker="bytetrack.yaml"
            )
            
            # Sonuçları işle
            if results and len(results) > 0:
                result = results[0]
                processed_frame = self.draw_detections(frame.copy(), result, source_id)
                
                # İstatistikleri güncelle
                self.update_statistics(result)
            else:
                processed_frame = frame.copy()
                
            return processed_frame
            
        except Exception as e:
            self.log_message.emit(f"Frame işleme hatası: {str(e)}")
            return frame
            
    def draw_detections(self, frame, result, source_id):
        """Tespit sonuçlarını frame üzerine çiz"""
        try:
            if result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()
                
                # Track ID'leri varsa al
                track_ids = None
                if result.boxes.id is not None:
                    track_ids = result.boxes.id.cpu().numpy()
                
                for i, (box, conf, cls) in enumerate(zip(boxes, confs, classes)):
                    x1, y1, x2, y2 = map(int, box)
                    class_name = self.class_names[int(cls)]
                    
                    # Track ID
                    track_id = int(track_ids[i]) if track_ids is not None else -1
                    
                    # Renk seçimi (Hasarlı: kırmızı, Hasarsız: yeşil)
                    color = (0, 0, 255) if class_name == "Hasarlı" else (0, 255, 0)
                    
                    # Bounding box çiz
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Label oluştur
                    label = f"{class_name} {conf:.2f}"
                    if track_id != -1:
                        label += f" ID:{track_id}"
                        
                    # Label pozisyonu
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                    label_y = y1 - 10 if y1 - 10 > 10 else y1 + 30
                    
                    # Label arka planı
                    cv2.rectangle(frame, (x1, label_y - label_size[1] - 5), 
                                (x1 + label_size[0], label_y + 5), color, -1)
                    
                    # Label yazısı
                    cv2.putText(frame, label, (x1, label_y), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    # Hasarlı tespit edilirse kırp ve kaydet
                    if class_name == "Hasarlı" and track_id != -1:
                        self.save_damaged_crop(frame, box, track_id, source_id)
                        
            return frame
            
        except Exception as e:
            self.log_message.emit(f"Çizim hatası: {str(e)}")
            return frame
            
    def save_damaged_crop(self, frame, box, track_id, source_id):
        """Hasarlı tespit edilen bölgeyi kırp ve kaydet"""
        try:
            # Aynı ID'yi tekrar kaydetme
            if track_id in self.tracked_objects[source_id]:
                return
                
            x1, y1, x2, y2 = map(int, box)
            
            # Kırpılacak bölgeyi genişlet (padding)
            padding = 20
            h, w = frame.shape[:2]
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(w, x2 + padding)
            y2 = min(h, y2 + padding)
            
            # Kırp
            cropped = frame[y1:y2, x1:x2]
            
            if cropped.size > 0:
                # Dosya adı oluştur
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"damaged_bolt_src{source_id}_id{track_id}_{timestamp}.jpg"
                filepath = Path("data/cropped") / filename
                
                # Kaydet
                cv2.imwrite(str(filepath), cropped)
                
                # Takip et
                self.tracked_objects[source_id][track_id] = {
                    'timestamp': timestamp,
                    'filepath': str(filepath),
                    'bbox': box
                }
                
                self.damage_count += 1
                self.log_message.emit(f"Hasarlı cıvata kaydedildi: {filename}")
                
        except Exception as e:
            self.log_message.emit(f"Kırpma hatası: {str(e)}")
            
    def add_timestamp(self, frame):
        """Frame'e tarih damgası ekle"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Timestamp pozisyonu (sol üst köşe)
            position = (10, 30)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            color = (255, 255, 255)  # Beyaz
            thickness = 2
            
            # Arka plan için siyah dikdörtgen
            text_size = cv2.getTextSize(timestamp, font, font_scale, thickness)[0]
            cv2.rectangle(frame, (5, 5), (text_size[0] + 15, text_size[1] + 15), (0, 0, 0), -1)
            
            # Timestamp yazısı
            cv2.putText(frame, timestamp, position, font, font_scale, color, thickness)
            
            return frame
            
        except Exception as e:
            self.log_message.emit(f"Timestamp ekleme hatası: {str(e)}")
            return frame
            
    def update_statistics(self, result):
        """İstatistikleri güncelle"""
        try:
            if result.boxes is not None:
                self.total_detections += len(result.boxes)
                
                # Sınıf bazında sayım
                classes = result.boxes.cls.cpu().numpy()
                damaged_count = sum(1 for cls in classes if int(cls) == 1)  # Hasarlı
                
                # İstatistik dictionary'si oluştur
                stats = {
                    'total_detections': self.total_detections,
                    'damaged_count': self.damage_count,
                    'current_damaged': damaged_count,
                    'fps': 30,  # Yaklaşık FPS
                    'model_conf': self.config.confidence_threshold
                }
                
                # UI'ye gönder
                self.detection_stats.emit(stats)
                
        except Exception as e:
            self.log_message.emit(f"İstatistik güncelleme hatası: {str(e)}")
            
    def stop(self):
        """Thread'i durdur"""
        self.is_running = False
        self.is_paused = False
        self.condition.wakeAll()
        
    def toggle_pause(self):
        """Pause/Resume"""
        self.mutex.lock()
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.condition.wakeAll()
        self.mutex.unlock()
        
    def cleanup(self):
        """Kaynakları temizle"""
        try:
            # Kameraları kapat
            for cap in self.caps:
                if cap.isOpened():
                    cap.release()
                    
            # Video writer'ları kapat
            for writer in self.video_writers:
                if writer is not None:
                    writer.release()
                    
            self.log_message.emit("Kaynaklar temizlendi")
            
        except Exception as e:
            self.log_message.emit(f"Temizleme hatası: {str(e)}")