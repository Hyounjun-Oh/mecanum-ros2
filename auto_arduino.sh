#!/bin/bash

# 아두이노 스케치 파일 경로
front_sketch="mecanum-ros2/arduino_code/motor_control_front_final_float/motor_control_front_final_float.ino"
rear_sketch="mecanum-ros2/arduino_code/motor_control_rear_final_float/motor_control_rear_final_float.ino"

# 아두이노 보드 타입
board_type_1="arduino:avr:mega"
board_type_2="arduino:avr:mega"

# 아두이노 포트
front_port="/dev/ttyFrontArduino"
rear_port="/dev/ttyRearArduino"

# 아두이노 스케치 컴파일 및 업로드
arduino-cli compile --fqbn $board_type_2 $front_sketch
arduino-cli upload -p $front_port -b $board_type_1 $front_sketch
arduino-cli compile --fqbn $board_type_1 $rear_sketch
arduino-cli upload -p $rear_port -b $board_type_2 $rear_sketch
