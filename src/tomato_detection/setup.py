from setuptools import setup

package_name = 'tomato_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jetson',
    maintainer_email='jetson@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'tomato_detection_node=tomato_detection.tomato_detection_node:main',
        'tomato_detection_node_new=tomato_detection.tomato_detection_node_new:main',
        'tomato_detection_node_new_3=tomato_detection.tomato_detection_node_new_3:main'
        ],
    },
)
