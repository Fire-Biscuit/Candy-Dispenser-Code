from threading import Thread
from time import sleep
from gpiozero import Servo
import paho.mqtt.client as mqtt
import random
servo = Servo(15)
mqttTopic = "schardm/test"

mqttc = mqtt.Client()

def setup():

    def on_message(client, userdata, msg):
        print(msg.topic)
        if str(msg.topic) == mqttTopic:
            servoFunction()

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_subscribe(client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
    mqttc.username_pw_set("schardm", "4Oyhf3DAoSzxYc9QciX8")
    mqttc.connect("mqtt.hva-robots.nl", port=1883)
    
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.subscribe(mqttTopic)
    print(mqttc.is_connected)

def servoFunction():
    if True:
        servo.min()
        print("begin")
        sleep(1)
        servo.max()
        print("eind")

def servoMain():
    setup()
    while True:
        mqttc.loop_forever
        mqttc.loop
        sleep(5)
        print(".")
        print(random.randint(0,9)) 

servoThread=Thread(target=servoMain)
servoThread.start()

while True:
    pass