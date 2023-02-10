import serial
import time

ser = serial.Serial('COM8', 9800, timeout=1)
time.sleep(2)
f = open('GYRO.txt', 'w')
ser.baudrate = 9800

while 1:
    line = ser.readline()
    if line:
        string = line.decode('utf-8').strip()
        print(string)
        print(string, file=f)

ser.close()
