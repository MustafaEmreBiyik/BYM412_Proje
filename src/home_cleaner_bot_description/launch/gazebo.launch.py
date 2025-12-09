import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'home_cleaner_bot_description'
    pkg_share = get_package_share_directory(pkg_name)
    
    # 1. Robot Modelini (URDF) İşle
    urdf_file = os.path.join(pkg_share, 'urdf', 'home_cleaner.urdf.xacro')
    doc = xacro.process_file(urdf_file)
    robot_desc = {'robot_description': doc.toxml()}

    # 2. Gazebo Harmonic'i Başlat (Custom 2+1 Apartment World)
    # '-r' simülasyonu çalışır durumda başlatır
    world_file = os.path.join(pkg_share, 'worlds', 'my_home.sdf')
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_file]}.items(),
    )

    # 3. Robotu Sahneye Yerleştir (Spawn) - Living Room'da başlat
    create_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'home_cleaner_bot',
                   '-x', '-2.0',
                   '-y', '0.0',
                   '-z', '0.1'], # Living Room center'da spawn
        output='screen'
    )

    # 4. Robot Durum Yayıncısı (TF'ler için)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_desc]
    )

    # 5. Köprü (Bridge): ROS ile Gazebo arasındaki mesajları çevirir
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/model/home_cleaner_bot/joint_state@sensor_msgs/msg/JointState@gz.msgs.Model', # <-- YENİ EKLENEN SATIR
        ],
        remappings=[
            ('/model/home_cleaner_bot/joint_state', 'joint_states'), # <-- YENİ EKLENEN SATIR
        ],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        create_entity,
        bridge
    ])
