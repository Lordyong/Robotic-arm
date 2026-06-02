import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_arm')
    world_file = os.path.join(pkg_dir, 'worlds', 'empty_world.sdf')
    
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', '--render-engine', 'ogre', world_file],
            output='screen'
        ),
    ])
