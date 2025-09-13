"""
src/utils/logger.py
Logging yardımcı fonksiyonları
"""

import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name="CivataDetection", level=logging.INFO):
    """Logger kurulumu"""
    
    # Logs klasörünü oluştur
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Log dosyası adı (tarih ile)
    log_filename = f"civata_detection_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = log_dir / log_filename
    
    # Logger oluştur
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Eğer handler'lar zaten varsa temizle
    if logger.handlers:
        logger.handlers.clear()
    
    # Formatter oluştur
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # İlk log mesajı
    logger.info("Logger başlatıldı")
    logger.info(f"Log dosyası: {log_filepath}")
    
    return logger

def log_system_info(logger):
    """Sistem bilgilerini logla"""
    import platform
    import psutil
    import cv2
    
    try:
        logger.info("=== SİSTEM BİLGİLERİ ===")
        logger.info(f"İşletim Sistemi: {platform.system()} {platform.release()}")
        logger.info(f"Python Versiyonu: {platform.python_version()}")
        logger.info(f"OpenCV Versiyonu: {cv2.__version__}")
        
        # CPU bilgisi
        logger.info(f"CPU: {platform.processor()}")
        logger.info(f"CPU Çekirdek Sayısı: {psutil.cpu_count()}")
        
        # Bellek bilgisi
        memory = psutil.virtual_memory()
        logger.info(f"Toplam RAM: {memory.total / (1024**3):.1f} GB")
        logger.info(f"Kullanılabilir RAM: {memory.available / (1024**3):.1f} GB")
        
        # Disk bilgisi
        disk = psutil.disk_usage('/')
        logger.info(f"Disk Alanı: {disk.free / (1024**3):.1f} GB boş / {disk.total / (1024**3):.1f} GB toplam")
        
        logger.info("=== SİSTEM BİLGİLERİ SONU ===")
        
    except Exception as e:
        logger.error(f"Sistem bilgisi alma hatası: {e}")

def log_detection_event(logger, event_type, details):
    """Tespit olaylarını logla"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    
    event_messages = {
        'detection_start': f"[{timestamp}] Tespit işlemi başlatıldı",
        'detection_stop': f"[{timestamp}] Tespit işlemi durduruldu", 
        'detection_pause': f"[{timestamp}] Tespit işlemi duraklatıldı",
        'detection_resume': f"[{timestamp}] Tespit işlemi devam ettirildi",
        'model_loaded': f"[{timestamp}] Model yüklendi: {details.get('model_path', 'N/A')}",
        'source_opened': f"[{timestamp}] Kaynak açıldı: {details.get('source', 'N/A')}",
        'damaged_detected': f"[{timestamp}] Hasarlı tespit edildi - ID: {details.get('track_id', 'N/A')}, Güven: {details.get('confidence', 'N/A'):.2f}",
        'image_saved': f"[{timestamp}] Görüntü kaydedildi: {details.get('filepath', 'N/A')}",
        'video_recording_start': f"[{timestamp}] Video kaydı başlatıldı: {details.get('filepath', 'N/A')}",
        'video_recording_stop': f"[{timestamp}] Video kaydı durduruldu",
        'error': f"[{timestamp}] HATA: {details.get('error', 'Bilinmeyen hata')}",
        'warning': f"[{timestamp}] UYARI: {details.get('warning', 'Bilinmeyen uyarı')}"
    }
    
    message = event_messages.get(event_type, f"[{timestamp}] Bilinmeyen olay: {event_type}")
    
    if event_type == 'error':
        logger.error(message)
    elif event_type == 'warning':
        logger.warning(message)
    else:
        logger.info(message)

def log_performance_metrics(logger, metrics):
    """Performans metriklerini logla"""
    try:
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        fps = metrics.get('fps', 0)
        total_detections = metrics.get('total_detections', 0)
        damaged_count = metrics.get('damaged_count', 0)
        memory_usage = metrics.get('memory_usage', 0)
        cpu_usage = metrics.get('cpu_usage', 0)
        
        logger.info(f"[{timestamp}] PERFORMANS - FPS: {fps:.1f}, "
                   f"Toplam Tespit: {total_detections}, "
                   f"Hasarlı: {damaged_count}, "
                   f"Bellek: {memory_usage:.1f}%, "
                   f"CPU: {cpu_usage:.1f}%")
                   
    except Exception as e:
        logger.error(f"Performans metrik loglama hatası: {e}")

def log_configuration(logger, config):
    """Konfigürasyon bilgilerini logla"""
    try:
        logger.info("=== KONFIGÜRASYON ===")
        logger.info(f"Model: {config.model_path}")
        logger.info(f"Güven Eşiği: {config.confidence_threshold}%")
        logger.info(f"IoU Eşiği: {config.iou_threshold}")
        logger.info(f"Kaynak Sayısı: {config.source_count}")
        
        for i, source in config.sources.items():
            source_type = "Kamera" if isinstance(source, int) else "Video"
            logger.info(f"Kaynak {i+1}: {source_type} - {source}")
            
        logger.info(f"Çıktı Klasörü: {config.output_dir}")
        logger.info(f"Kırpılmış Klasörü: {config.cropped_dir}")
        logger.info(f"Video Kaydı: {'Aktif' if config.record_video else 'Pasif'}")
        logger.info("=== KONFIGÜRASYON SONU ===")
        
    except Exception as e:
        logger.error(f"Konfigürasyon loglama hatası: {e}")

def log_memory_usage(logger):
    """Bellek kullanımını logla"""
    try:
        import psutil
        import os
        
        # Sistem bellek kullanımı
        memory = psutil.virtual_memory()
        system_memory_percent = memory.percent
        
        # Uygulama bellek kullanımı
        process = psutil.Process(os.getpid())
        app_memory_mb = process.memory_info().rss / (1024 * 1024)
        
        logger.info(f"Bellek Kullanımı - Sistem: {system_memory_percent:.1f}%, "
                   f"Uygulama: {app_memory_mb:.1f} MB")
                   
    except Exception as e:
        logger.error(f"Bellek kullanımı loglama hatası: {e}")

def create_error_report(logger, error, context=None):
    """Detaylı hata raporu oluştur"""
    import traceback
    import sys
    
    try:
        logger.error("=== HATA RAPORU ===")
        logger.error(f"Hata: {str(error)}")
        logger.error(f"Hata Tipi: {type(error).__name__}")
        
        if context:
            logger.error(f"Bağlam: {context}")
            
        # Stack trace
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_traceback:
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logger.error("Stack Trace:")
            for line in tb_lines:
                logger.error(line.strip())
                
        logger.error("=== HATA RAPORU SONU ===")
        
    except Exception as e:
        logger.error(f"Hata raporu oluşturma hatası: {e}")

def cleanup_old_logs(days_to_keep=30):
    """Eski log dosyalarını temizle"""
    try:
        log_dir = Path("logs")
        if not log_dir.exists():
            return
            
        current_time = datetime.now()
        deleted_count = 0
        
        for log_file in log_dir.glob("*.log"):
            # Dosya yaş bilgisini al
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            age_days = (current_time - file_time).days
            
            if age_days > days_to_keep:
                log_file.unlink()
                deleted_count += 1
                
        if deleted_count > 0:
            print(f"{deleted_count} eski log dosyası temizlendi")
            
    except Exception as e:
        print(f"Log temizleme hatası: {e}")

# Logger instance'ı global olarak kullanım için
app_logger = None

def get_logger():
    """Global logger instance'ını döndür"""
    global app_logger
    if app_logger is None:
        app_logger = setup_logger()
    return app_logger