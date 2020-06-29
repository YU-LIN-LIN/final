import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
import serial
mqttc = paho.Client()

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x167\r\n".encode())
char = s.read(3)
print("Set MY 0x167.")
print(char.decode())

s.write("ATDL 0x267\r\n".encode())
char = s.read(3)
print("Set DL 0x267.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

s.write(bytes("\r", 'UTF-8'))
time.sleep(1.0)
for i in range(0, int(10)):
    s.write(bytes("/getAcc/run\r", 'UTF-8'))
    time.sleep(1.0)  

x = []
y = []
z = []
time1 = []
log = []
num = []
for i in range(0, int(20)):
    print(i)
    line=s.readline()
    x.append(line)
    line=s.readline() # Read an echo string from K66F terminated with '\n'
    y.append(line)
    line=s.readline() # Read an echo string from K66F terminated with '\n'
    z.append(line)
    line=s.readline() # Read an echo string from K66F terminated with '\n'
    time1.append(line)
    line=s.readline() # Read an echo string from K66F terminated with '\n'
    log.append(line)
    num.append(int(2))

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect

mqttc.connect(host, port=1883, keepalive=60)

for i in range(0, int(20)):
    #mesg = "Hello, world!"
    mesg = x[i] + y [i] + z[i] + log[i] + time1[i]
    mqttc.publish(topic, mesg)
    print(mesg)
#    mesg = y[i]
#    mqttc.publish(topic, mesg)
#    print(mesg)
#    mesg = z[i]
#    mqttc.publish(topic, mesg)
#    print(mesg)
#    mesg = log[i]
#    mqttc.publish(topic, mesg)
#    print(mesg)
    
    time.sleep(1)

# draw
t = np.arange(0,10,0.5) 


plt.plot(t,num, color = "blue", linewidth = 1, linestyle = "-", label = "x")
#plt.set_xlabel('number')
#plt.set_ylabel('timestamp')
plt.show()