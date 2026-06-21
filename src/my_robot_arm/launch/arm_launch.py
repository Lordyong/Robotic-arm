import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_arm')
    world_file = os.path.join(pkg_dir, 'worlds', 'empty_world.sdf')

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', '--render-engine', 'ogre', world_file],
            output='screen'
        ),
        TimerAction(
            period=5.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
                         'joint_state_broadcaster'],
                    output='screen'
                ),
            ]
        ),
        TimerAction(
            period=6.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
                         'arm_controller'],
                    output='screen'
                ),
            ]
        ),
    ])