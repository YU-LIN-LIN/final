import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
import serial
mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

i = 0
x = []
y = []
z = []
log = []

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    info = msg.payload
    print(info.split())
    x.append(float(info.split()[0]))
    y.append(float(info.split()[1]))
    z.append(float(info.split()[2]))
    log.append(float(info.split()[3]))
    print(x[len(x) - 1])
    if (len(x) - 1) == 19 :
        t = np.arange(0,10,0.5) 
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(t,x, color = "blue", linewidth = 1, linestyle = "-", label = "x")
        ax[0].plot(t,y, color = "red", linewidth = 1, linestyle = "-", label = "y")
        ax[0].plot(t,z, color = "green", linewidth = 1, linestyle = "-", label = "z")
        # Show legend
        ax[0].legend(loc='lower left', frameon=False)
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Acc vector')
        for i in range(0, 20) :
            ax[1].plot([i/2, i/2], [0, log[i]], color = 'blue', linewidth = 1, linestyle="-") 
            ax[1].scatter([i/2,], [log[i],], 70, color = 'blue')
        ax[1].plot([0, 10], [0, 0], color = "red", linewidth = 1, linestyle = "-")
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel('Tilt')
        plt.show()
    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

mqttc.loop_forever()