import spidev
import struct
import time
import Jetson.GPIO as GPIO

def main():
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 2000000
    CS0 = 24
    CS1 = 26
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(CS0, GPIO.OUT)
    GPIO.setup(CS1, GPIO.OUT)
    GPIO.output(CS0, GPIO.HIGH)
    GPIO.output(CS1, GPIO.HIGH)
    while 1:        
        try:
            GPIO.output(CS0, GPIO.LOW)
            trans_value = [50.0, 100.0]
            data = bytearray(struct.pack('f', trans_value))
            resp = spi.xfer()
        except KeyboardInterrupt:
            GPIO.cleanup(CS0)
            GPIO.cleanup(CS1)
            spi.close()
            print("키보드 인터럽트 발생! 종료.")
        finally:
            GPIO.cleanup(CS0)
            GPIO.cleanup(CS1)
            spi.close() 


if __name__ == '__main__':
    main()