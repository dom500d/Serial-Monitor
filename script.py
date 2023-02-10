import serial
import time
import math
import matplotlib as plt
from matplotlib import pyplot

ser = serial.Serial('COM8', 9800, timeout=1)
time.sleep(2)
f = open('GYRO.txt', 'w')
ser.baudrate = 9800
figure = pyplot.figure()
ax = figure.add_subplot(1,1,1)
xs = []
ys = []
zs = []
ts = []

# From https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
def euler_from_quaternion(x, y, z, w):
    t0 = 2.0 * (2 * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = 2.0 * (2 * y - z * x)
    t2 = 1.0 if t2 > 1 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    roll_x = roll_x * 180 / math.pi
    pitch_y = pitch_y * 180 / math.pi
    yaw_z = yaw_z * 180 / math.pi

    return roll_x, pitch_y, yaw_z

def plot(ts, x1, y1, z1):
    ts.append(time.time() - start)
    xs.append(x1)
    ys.append(y1)
    zs.append(z1)
    ax.clear()
    ax.plot(ts, xs, ts, ys, ts, zs)

try:
    while True:
        start = time.time()
        while 1:
            line = ser.readline()
            if line.strip():
                string = line.strip().decode('utf-8')
                f.write(string)
                f.write("\n")
                print(string)
                string = string.split(",")
                x = float(string[0])
                y = float(string[1])
                z = float(string[2])
                w = float(string[3])
                roll, pitch, yaw = euler_from_quaternion(x, y, z, w)
                plot(ts, roll, pitch, yaw)
                pyplot.pause(0.05)
except KeyboardInterrupt:
    ser.close()
    f.close()
    pass



