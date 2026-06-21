import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_arm')
    world_file = os.path.join(pkg_dir, 'worlds', 'simple_empty.sdf')
    urdf_file = os.path.join(pkg_dir, 'urdf2', 'simulator_testing.urdf')

    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', '--render-engine', 'ogre', world_file],
            output='screen'
        ),
        ExecuteProcess(
            cmd=['ros2', 'run', 'robot_state_publisher', 'robot_state_publisher',
                 '--ros-args', '-p', f'robot_description:={robot_desc}'],
            output='screen'
        ),
        TimerAction(
            period=5.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'run', 'ros_gz_sim', 'create',
                         '-name', 'simulator_testing',
                         '-topic', 'robot_description'],
                    output='screen'
                ),
            ]
        ),
        TimerAction(
            period=8.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
                         'joint_state_broadcaster'],
                    output='screen'
                ),
            ]
        ),
        TimerAction(
            period=9.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
                         'arm_controller'],
                    output='screen'
                ),
            ]
        ),
    ])
