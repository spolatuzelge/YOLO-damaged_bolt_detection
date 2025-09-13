"""
src/utils/model_loader.py
Basit YOLO model yükleyici
"""

import torch
import os
from ultralytics import YOLO

def load_yolo_model_safe(model_path):
    """
    Basit YOLO model yükleme
    
    Args:
        model_path (str): Model dosyası yolu
        
    Returns:
        YOLO: Yüklenmiş YOLO modeli
    """
    
    if not os.path.exists(model_path):
        raise Exception(f"Model dosyası bulunamadı: {model_path}")
    
    # PyTorch 2.6+ için basit düzeltme
    original_load = torch.load
    torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})
    
    try:
        model = YOLO(model_path)
        print(f"✅ Model yüklendi: {model_path}")
        return model
    finally:
        torch.load = original_load

def check_model_compatibility(model_path):
    """Basit model kontrolü"""
    
    result = {
        'exists': os.path.exists(model_path),
        'format': 'PyTorch' if model_path.endswith('.pt') else 'ONNX',
        'size_mb': round(os.path.getsize(model_path) / (1024*1024), 2) if os.path.exists(model_path) else 0,
        'compatible': True,
        'warnings': []
    }
    
    if not result['exists']:
        result['warnings'].append("Model dosyası bulunamadı")
        result['compatible'] = False
    
    return result

if __name__ == "__main__":
    # Test
    model_path = "src/models/best.pt"
    try:
        model = load_yolo_model_safe(model_path)
        print(f"Model sınıfları: {model.names}")
    except Exception as e:
        print(f"Hata: {e}")

def check_model_compatibility(model_path):
    """
    Model dosyasının uyumluluğunu kontrol et
    
    Args:
        model_path (str): Model dosyası yolu
        
    Returns:
        dict: Uyumluluk bilgileri
    """
    
    import os
    from pathlib import Path
    
    result = {
        'exists': False,
        'format': None,
        'size_mb': 0,
        'pytorch_version': torch.__version__,
        'compatible': False,
        'warnings': []
    }
    
    try:
        # Dosya varlık kontrolü
        if not os.path.exists(model_path):
            result['warnings'].append(f"Model dosyası bulunamadı: {model_path}")
            return result
            
        result['exists'] = True
        
        # Dosya boyutu
        file_size = os.path.getsize(model_path)
        result['size_mb'] = round(file_size / (1024 * 1024), 2)
        
        # Format kontrolü
        file_ext = Path(model_path).suffix.lower()
        if file_ext == '.pt':
            result['format'] = 'PyTorch'
        elif file_ext == '.onnx':
            result['format'] = 'ONNX'
        else:
            result['warnings'].append(f"Desteklenmeyen format: {file_ext}")
            return result
            
        # Boyut kontrolü
        if result['size_mb'] < 1:
            result['warnings'].append("Model dosyası çok küçük, bozuk olabilir")
        elif result['size_mb'] > 1000:
            result['warnings'].append("Model dosyası çok büyük, yükleme yavaş olabilir")
            
        # Temel uyumluluk
        if result['format'] in ['PyTorch', 'ONNX'] and result['size_mb'] > 1:
            result['compatible'] = True
            
    except Exception as e:
        result['warnings'].append(f"Kontrol hatası: {str(e)}")
        
    return result

# Test fonksiyonu
def test_model_loading():
    """Model yükleme testleri"""
    
    print("🧪 Model Yükleme Test Başlıyor...")
    print(f"PyTorch Versiyonu: {torch.__version__}")
    
    # Test modeli indir (küçük YOLOv8n)
    try:
        print("📥 Test modeli indiriliyor...")
        test_model = YOLO('yolov8n.pt')  # Otomatik indirilir
        print("✅ Test modeli başarıyla yüklendi!")
        
        # Model bilgilerini göster
        print(f"Model tipi: {type(test_model)}")
        print(f"Model sınıfları: {test_model.names}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test modeli yüklenemedi: {e}")
        return False

if __name__ == "__main__":
    test_model_loading()