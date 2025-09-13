# YOLO Hasarlı Cıvata Tespit Sistemi - Kullanıcı Kılavuzu

## 📋 İçindekiler
1. [Kurulum](#kurulum)
2. [İlk Çalıştırma](#ilk-çalıştırma)
3. [Arayüz Tanıtımı](#arayüz-tanıtımı)
4. [Model Ayarları](#model-ayarları)
5. [Kaynak Yapılandırması](#kaynak-yapılandırması)
6. [Tespit İşlemi](#tespit-işlemi)
7. [Sonuçlar ve Çıktılar](#sonuçlar-ve-çıktılar)
8. [Sorun Giderme](#sorun-giderme)

---

## 🚀 Kurulum

### Sistem Gereksinimleri
- **İşletim Sistemi**: Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Python**: 3.8 veya üzeri
- **RAM**: Minimum 8GB (16GB önerilen)
- **GPU**: CUDA destekli (opsiyonel ama performans için önerilen)
- **Disk**: 2GB boş alan
- **Kamera**: USB kamera (canlı tespit için)

### Kurulum Adımları

1. **Python Kurulumu**
   ```bash
   # Python versiyonunu kontrol edin
   python --version  # veya python3 --version
   ```

2. **Proje Dosyalarını İndirin**
   ```bash
   # Proje klasörüne gidin
   cd civata_detection_system
   ```

3. **Otomatik Kurulum (Önerilen)**
   ```bash
   # Kurulum scriptini çalıştırın
   python scripts/setup.py
   ```

4. **Manuel Kurulum**
   ```bash
   # Virtual environment oluşturun (opsiyonel)
   python -m venv venv
   
   # Virtual environment'ı aktifleştirin
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Gereksinimleri kurun
   pip install -r requirements.txt
   ```

---

## 🎯 İlk Çalıştırma

### 1. Uygulamayı Başlatın
```bash
# Terminal/Command Prompt'da
python main.py

# Veya Windows'da
start_app.bat

# Veya Linux/Mac'te
./start_app.sh
```

### 2. İlk Yapılandırma
- Uygulama açıldığında boş bir arayüz göreceksiniz
- İlk olarak bir YOLO model dosyası seçmeniz gerekir
- Ardından video kaynaklarınızı yapılandırın

---

## 🖥️ Arayüz Tanıtımı

### Sol Panel (Kontrol Paneli)
- **Model Ayarları**: YOLO model seçimi ve güven eşiği
- **Kaynak Ayarları**: Kamera/video seçimi ve kaynak sayısı
- **Kontrol Butonları**: Başlat, Durdur, Duraklat, Sıfırla
- **İstatistikler**: Anlık performans ve tespit verileri
- **Sistem Logları**: İşlem geçmişi ve hata mesajları

### Sağ Panel (Video Görüntüleme)
- **Video Widget(ları)**: Gerçek zamanlı görüntü
- **Tespit Kutucukları**: Yeşil (Hasarsız), Kırmızı (Hasarlı)
- **Track ID'leri**: Her nesne için benzersiz kimlik
- **Timestamp**: Video kaydı için tarih damgası

---

## 🤖 Model Ayarları

### YOLO Model Seçimi

1. **"Model Seç" butonuna tıklayın**
2. **Desteklenen formatlar**:
   - `.pt` dosyaları (PyTorch - önerilen)
   - `.onnx` dosyaları (ONNX Runtime)
3. **Model yerleştirme**:
   - Modeli `data/models/` klasörüne koyun
   - Veya herhangi bir konumdan seçin

### Güven Eşiği Ayarlama

- **Varsayılan**: %50
- **Düşük değer** (%20-40): Daha fazla tespit, daha fazla yanlış pozitif
- **Yüksek değer** (%60-80): Daha az tespit, daha yüksek kesinlik
- **Önerilen**: %50-60 arası

### Model Gereksinimleri

```python
# Model sınıfları şu şekilde olmalı:
# 0: Hasarsız (Normal cıvata)
# 1: Hasarlı (Defektli cıvata)
```

---

## 📹 Kaynak Yapılandırması

### Kaynak Tipi Seçimi

#### 1. Kamera Modu
- **Kullanım**: Gerçek zamanlı tespit
- **Avantajlar**: 
  - Canlı izleme
  - Otomatik video kayıt
  - Timestamp ekleme
- **Ayarlama**:
  1. "Kamera" seçin
  2. Kamera ID girin (genellikle 0, 1, 2...)
  3. Kamera test edilir ve açılır

#### 2. Video Dosyası Modu
- **Kullanım**: Önceden çekilmiş videolar
- **Desteklenen formatlar**: MP4, AVI, MOV, MKV
- **Ayarlama**:
  1. "Video Dosyası" seçin
  2. "Kaynak Seç" ile dosya seçin
  3. Video yüklenir ve oynatılır

### Kaynak Sayısı

#### Tek Kaynak (1)
- **Kullanım**: Standart kullanım
- **Görünüm**: Tek video penceresi
- **Performans**: Yüksek FPS

#### Çift Kaynak (2) 
- **Kullanım**: Çoklu kamera sistemi
- **Görünüm**: Altlı-üstlü düzen
- **Örnek Senaryolar**:
  - İki farklı açıdan görüntüleme
  - Farklı üretim hatları
  - Yedek kamera sistemi

---

## 🔍 Tespit İşlemi

### Tespit Başlatma

1. **Ön Kontroller**:
   - ✅ Model seçildi mi?
   - ✅ Kaynak yapılandırıldı mı?
   - ✅ Kamera bağlı mı?

2. **"Başlat" Butonuna Tıklayın**
   - Sistem model yükler
   - Kameralar/videolar açılır
   - Tespit işlemi başlar

### Tespit Süreci

#### Görsel Göstergeler
- **Yeşil Kutucuk**: Hasarsız cıvata tespit edildi
- **Kırmızı Kutucuk**: Hasarlı cıvata tespit edildi
- **Track ID**: Her nesne için benzersiz numara
- **Güven Skoru**: Tespit kesinliği (%0-100)

#### Tracking Sistemi
```
ID:1 → Hasarsız cıvata takip ediliyor
ID:2 → Hasarlı cıvata tespit edildi ve kaydedildi
ID:3 → Yeni nesne takibe alındı
```

### Kontrol Seçenekleri

- **Duraklat**: İşlemi geçici durdur
- **Devam Et**: Duraklatılan işlemi sürdür
- **Durdur**: İşlemi tamamen sonlandır
- **Sıfırla**: Tüm sayaçları ve verileri temizle

---

## 📊 Sonuçlar ve Çıktılar

### Otomatik Kayıtlar

#### 1. Hasarlı Cıvata Görüntüleri
- **Konum**: `data/cropped/`
- **Format**: JPG
- **Adlandırma**: `damaged_bolt_src0_id5_20240617_143052_123.jpg`
- **İçerik**: Sadece hasarlı tespit edilen bounding box alanı

#### 2. Video Kayıtları (Kamera Modu)
- **Konum**: `data/outputs/`
- **Format**: MP4
- **Adlandırma**: `camera_0_20240617_143052.mp4`
- **Özellikler**:
  - Sol üst köşede timestamp
  - Tüm tespit kutucukları dahil
  - Orijinal çözünürlük

#### 3. Log Dosyaları
- **Konum**: `logs/`
- **Format**: TXT
- **Adlandırma**: `civata_detection_20240617.log`
- **İçerik**:
  - Sistem olayları
  - Tespit logları
  - Hata mesajları
  - Performans metrikleri

### İstatistik Takibi

#### Gerçek Zamanlı Metrikler
- **Çalışma Süresi**: HH:MM:SS formatında
- **Toplam Tespit**: Tüm nesneler (hasarlı + hasarsız)
- **Hasarlı Tespit**: Sadece defektli cıvatalar
- **Kaydedilen**: Başarıyla kaydedilen görüntü sayısı
- **FPS**: Saniyedeki frame sayısı
- **İşlem Yükü**:
