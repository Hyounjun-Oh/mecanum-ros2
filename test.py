import struct
import serial
import time
# 시리얼 포트와 전송 속도를 설정합니다.
ser = serial.Serial('/dev/ttyACM1', 115200)

# 두 개의 실수 값을 전송하는 함수를 정의합니다.
def send_floats_data(data1, data2):
    # 실수 값을 이진 데이터로 변환합니다.
    data1_bytes = struct.pack('f', data1)
    data2_bytes = struct.pack('f', data2)
    # 이진 데이터를 시리얼 포트를 통해 전송합니다.
    ser.write(data1_bytes + data2_bytes)

# 예시 데이터를 전송합니다.
while(1):
    send_floats_data(3.14, 2.72)
    time.sleep(1)
