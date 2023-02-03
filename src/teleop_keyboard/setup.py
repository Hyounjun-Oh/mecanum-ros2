from setuptools import setup

package_name = 'teleop_keyboard'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hyounjun Oh',
    maintainer_email='ohj_980918@naver.com',
    description='모바일 로봇을 조작하기위해 키보드 입력을 받는다.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'teleop_keyboard = teleop_keyboard.teleop_keyboard:main'
        ],
    },
)
