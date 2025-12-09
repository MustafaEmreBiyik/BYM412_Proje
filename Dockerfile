# Temel İmaj: ROS 2 Humble (Desktop Full)
FROM osrf/ros:humble-desktop-full

# Ortam Değişkenleri
ENV ROS_DISTRO=humble
ENV DEBIAN_FRONTEND=noninteractive

# 1. Gerekli Paketlerin Kurulumu
RUN apt-get update && apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-ros-gz \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-robot-localization \
    ros-humble-xacro \
    ros-humble-joint-state-publisher-gui \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 2. Çalışma Alanını (Workspace) Hazırla
WORKDIR /root/ros2_ws/src
# Proje dosyalarını konteyner içine kopyala
COPY . .

# 3. Bağımlılıkları Çöz ve Derle
WORKDIR /root/ros2_ws
RUN . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install

# 4. Kaynak Dosyalarını Tanıt (Source)
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc

# 5. Konteyner Başladığında Çalışacak Komut
# Varsayılan olarak bash açar, ama istersen launch dosyasını da tetikleyebilirsin
CMD ["bash"]
