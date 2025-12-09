import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_name = 'home_cleaner_bot_description'
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Config dosyasının yerini bul
    slam_config_file = os.path.join(pkg_share, 'config', 'mapper_params_online_async.yaml')

    # 2. Gazebo'yu başlat
    world_file_name = 'my_home.sdf'
    world_path = os.path.join(pkg_share, 'worlds', world_file_name)
    
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_path]}.items()
    )

    # 3. SLAM Toolbox'ı Başlat (Haritalama)
    start_async_slam_toolbox_node = Node(
        parameters=[
          slam_config_file,
          {'use_sim_time': True}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen'
    )

    # 4. RViz'i Başlat
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        gazebo_sim,
        start_async_slam_toolbox_node,
        rviz
    ])
