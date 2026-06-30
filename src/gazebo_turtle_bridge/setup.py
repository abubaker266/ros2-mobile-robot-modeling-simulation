from setuptools import setup
import os
from glob import glob

package_name = 'gazebo_turtle_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # This line ensures your launch files are actually installed
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abubakr',
    maintainer_email='abubakr@email.com',
    description='Bridge between Gazebo robot cmd_vel and turtlesim cmd_vel',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # EXECUTABLE_NAME = PACKAGE_NAME.FILE_NAME:FUNCTION
            'cmd_vel_bridge = gazebo_turtle_bridge.turtle_bridge_node:main',
        ],
    },
)
