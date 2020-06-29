import time
import matplotlib.pyplot as plt
import numpy as np
import serial
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)
x=[]

for i in range(40):
    line=s.readline()
    x.append(line)

# draw
t = np.arange(0,40,1)
plt.plot(t,x)
plt.show()

for i in range(40):
    print(x[i])