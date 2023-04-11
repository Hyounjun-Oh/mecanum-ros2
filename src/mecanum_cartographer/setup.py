from setuptools import setup
import glob
import os
package_name = 'mecanum_cartographer'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', '*.launch.py'))),
        ('share/' + package_name + '/config', glob.glob(os.path.join('config', '*.lua'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ohj',
    maintainer_email='ohj_980918@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
