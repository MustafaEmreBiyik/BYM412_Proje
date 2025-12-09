# 🤖 HomeCleaner Bot - Proje İskeleti

**Proje Adı:** BYM412_Proje  
**Tarih:** 9 Aralık 2025  
**Durum:** Faz 1 - Robot Tanımı ve Gazebo Simülasyonu Tamamlandı

---

## 📂 Dizin Yapısı

```
BYM412_Proje/                          # ✅ ROS 2 Workspace Root
│
├── .git/                              # Git versiyon kontrol
│
└── src/                               # ✅ Source Space (ROS 2 Standard)
    │
    └── home_cleaner_bot_description/  # Ana ROS 2 paketi
        │
        ├── CMakeLists.txt             # CMake build yapılandırması
        ├── package.xml                # ROS 2 paket manifest dosyası
        │
        ├── launch/                    # Launch dosyaları
        │   └── gazebo.launch.py      # Gazebo + Robot başlatma
        │
        ├── urdf/                      # Robot tanım dosyaları
        │   └── home_cleaner.urdf.xacro # Robot URDF modeli (Xacro)
        │
        └── worlds/                    # Gazebo dünya dosyaları
            ├── my_home.sdf           # 2+1 Daire simülasyon ortamı
            └── LAYOUT_DIAGRAM.txt    # Daire yerleşim şeması

📝 Not: build/, install/, log/ dizinleri build sonrası oluşur (gitignore'da)
```

---

## 📋 Dosya Detayları

### 🔧 **Yapılandırma Dosyaları**

| Dosya | Açıklama | Durum |
|-------|----------|-------|
| `CMakeLists.txt` | CMake build sistemi yapılandırması | ✅ Tamamlandı |
| `package.xml` | ROS 2 paket bağımlılıkları ve metadata | ✅ Tamamlandı |

### 🚀 **Launch Dosyaları**

| Dosya | Açıklama | Durum |
|-------|----------|-------|
| `gazebo.launch.py` | Gazebo Harmonic + Robot + ROS Bridge | ✅ Tamamlandı |

**Başlatılan Bileşenler:**
- Gazebo Harmonic simülatörü
- Robot State Publisher (TF ağacı)
- Entity Spawner (robot yerleştirme)
- ROS-Gazebo Bridge (`/cmd_vel`, `/scan`, `/joint_states`)

### 🤖 **Robot Dosyaları**

| Dosya | Açıklama | Durum |
|-------|----------|-------|
| `home_cleaner.urdf.xacro` | Robot fiziksel modeli | ✅ Tamamlandı |

**Robot Özellikleri:**
- **Tip:** Differential Drive (2 tekerlek + 1 caster)
- **Boyutlar:** 0.4m × 0.3m × 0.1m (G × D × Y)
- **Sensörler:** 360° LIDAR (gpu_lidar, 3.5m menzil)
- **Gazebo Pluginleri:**
  - Differential Drive System
  - Joint State Publisher
  - GPU LIDAR Sensor

### 🏠 **Dünya Dosyaları**

| Dosya | Açıklama | Durum |
|-------|----------|-------|
| `my_home.sdf` | 2+1 Daire simülasyon ortamı | ✅ Tamamlandı |
| `LAYOUT_DIAGRAM.txt` | Daire planı ve koordinatlar | ✅ Tamamlandı |

**Ortam Özellikleri:**
- **Boyut:** 10m × 10m
- **Odalar:** 
  - Salon (5m × 10m)
  - Yatak Odası 1 (3m × 2.5m)
  - Yatak Odası 2 (3m × 2.5m)
  - Koridor (1.5m genişlik)
- **Duvar Yüksekliği:** 2.5m
- **Kapı Genişliği:** 0.9m (4 kapı)

---

## 📊 Proje Durumu Özeti

### ✅ **Tamamlanan Bileşenler**

| # | Bileşen | Açıklama |
|---|---------|----------|
| 1 | URDF Robot Modeli | Differential drive robot + LIDAR |
| 2 | Gazebo Entegrasyonu | Launch dosyası ve pluginler |
| 3 | ROS-Gazebo Bridge | `/cmd_vel`, `/scan`, `/joint_states` |
| 4 | Custom World | 2+1 daire simülasyon ortamı |
| 5 | TF Tree | Robot State Publisher yapılandırması |

### ❌ **Eksik Bileşenler (Öncelik Sırasına Göre)**

| # | Bileşen | Öncelik | Tahmini Süre |
|---|---------|---------|--------------|
| 1 | Docker Setup | 🔴 KRİTİK | 2-3 saat |
| 2 | SLAM Toolbox | 🔴 YÜKSEK | 2-3 saat |
| 3 | Nav2 Stack | 🔴 YÜKSEK | 4-6 saat |
| 4 | Coverage Planner | 🟡 ORTA | 6-8 saat |
| 5 | State Machine | 🟡 ORTA | 3-4 saat |
| 6 | Docking Station | 🟢 DÜŞÜK | 2-3 saat |

---

## 🔗 ROS 2 Bağımlılıkları

### **Mevcut Bağımlılıklar (`package.xml`):**
```xml
<depend>rclcpp</depend>
<depend>urdf</depend>
<depend>xacro</depend>
<depend>ros_gz_sim</depend>
<depend>ros_gz_bridge</depend>
```

### **Eklenecek Bağımlılıklar:**
```xml
<!-- SLAM için -->
<depend>slam_toolbox</depend>

<!-- Nav2 için -->
<depend>nav2_bringup</depend>
<depend>nav2_msgs</depend>

<!-- Mesaj tipleri -->
<depend>geometry_msgs</depend>
<depend>sensor_msgs</depend>
<depend>nav_msgs</depend>

<!-- Robot State Publisher -->
<depend>robot_state_publisher</depend>
```

---

## 🐳 Docker Yapısı (Planlanıyor)

```
BYM412_Proje/
├── Dockerfile                    # ROS 2 Humble + Gazebo Harmonic
├── docker-compose.yml            # Servis tanımları
├── .dockerignore                 # Build hariç tutma
└── docker/
    ├── entrypoint.sh            # Container başlatma scripti
    └── requirements.txt         # Python bağımlılıkları (varsa)
```

---

## 📁 Gelecek Dizin Yapısı (Önerilen)

```
BYM412_Proje/                        # ✅ Workspace Root
│
├── src/                             # ✅ Source Space
│   │
│   ├── home_cleaner_bot_description/    # ✅ Mevcut paket
│   │   ├── launch/
│   │   ├── urdf/
│   │   └── worlds/
│   │
│   ├── home_cleaner_bot_slam/           # SLAM paketi (yeni)
│   │   ├── config/
│   │   │   └── slam_params.yaml
│   │   └── launch/
│   │       ├── slam_online.launch.py
│   │       └── slam_offline.launch.py
│   │
│   ├── home_cleaner_bot_navigation/     # Nav2 paketi (yeni)
│   │   ├── config/
│   │   │   ├── nav2_params.yaml
│   │   │   ├── costmap_common.yaml
│   │   │   ├── local_costmap.yaml
│   │   │   └── global_costmap.yaml
│   │   ├── launch/
│   │   │   └── navigation.launch.py
│   │   └── maps/
│   │       ├── my_home.yaml
│   │       └── my_home.pgm
│   │
│   ├── home_cleaner_bot_coverage/       # Coverage planner (yeni)
│   │   ├── config/
│   │   │   └── coverage_params.yaml
│   │   ├── launch/
│   │   │   └── coverage.launch.py
│   │   └── scripts/
│   │       └── coverage_planner.py
│   │
│   └── home_cleaner_bot_bringup/        # Ana bringup paketi (yeni)
│       └── launch/
│           ├── full_system.launch.py
│           ├── mapping_mode.launch.py
│           ├── cleaning_mode.launch.py
│           └── docking_mode.launch.py
│
├── build/                           # Build artifacts (gitignore)
├── install/                         # Install space (gitignore)
├── log/                             # Build logs (gitignore)
│
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
└── PROJECT_STRUCTURE.md
```

---

## 🎯 Sonraki Adımlar

### **Hemen Yapılacaklar:**
1. ✅ Projeyi test et: `ros2 launch home_cleaner_bot_description gazebo.launch.py`
2. ⏭️ Docker setup oluştur
3. ⏭️ SLAM Toolbox paketi ekle

### **Bu Hafta:**
- [ ] Docker container oluştur ve test et
- [ ] Custom world'de SLAM testi yap
- [ ] İlk harita kaydet

### **Gelecek Hafta:**
- [ ] Nav2 entegrasyonu
- [ ] Coverage planner implementasyonu
- [ ] State machine geliştirme

---

## 📞 Takım İş Bölümü (Relay Race Model)

### **Low-Spec PC (Kodlama):**
- Launch dosyaları yazma
- Config dosyaları düzenleme
- Python script'leri geliştirme
- URDF düzenlemeleri
- Docker dosyaları oluşturma
- Dokümantasyon

### **High-Spec PC (Simülasyon):**
- Gazebo testleri
- SLAM haritalama
- Nav2 tuning
- Coverage testing
- Parametre optimizasyonu
- Performans testleri

---

**Son Güncelleme:** 9 Aralık 2025  
**Durum:** ✅ Faz 1 Tamamlandı | ⏭️ Faz 2 Başlıyor (Docker + SLAM)
