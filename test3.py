#this code was made by Mike Schardijn 28-5-2023

#I coppied the mqtt code from timo.lambregts@hva.nl  
#paho-mqtt documentation:
#https://www.cloudmqtt.com/docs/python.html

#I used the servo library from gpiozero because that only allows the servo to move in a 
#90* range, which is exactly what is needed for the candy dispenser
#gpiozero servo documentation:
#https://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=gpiozero%20servo#servo 

#the threading library is used to make this code run on a background thread so as to not interfere with any other code
#threading library documentation
#https://docs.python.org/3/library/threading.html 

#the threading and gpiozero libraries already come with the raspberrypi os,
#to install the paho library you need to type the following in the linux terminal:
#pip3 install paho-mqtt

import paho.mqtt.client as mqtt
from time import sleep
from threading import Thread

#this creates the servo object which will be used to controll the servo
servoPin = 15
#servo = Servo(servoPin)
score = 0
#mqtt cridentials:
mqttUsername = "schardm"
mqttPassword = "4Oyhf3DAoSzxYc9QciX8"
mqttHost = "mqtt.hva-robots.nl"
mqttPort = 1883

#the mqtt topic used for the servo
dispenseCandyTopic = "schardm/dispenseCandy"

#the on_connect function serves no function other than to check if it connected corectly
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

#this function makes it so that when an mqtt message is received it will activate the servo function
def on_message(client, userdata, msg):
     global score
     print("message received")
     score += 1

#this creates the mqtt object and loads the on_connect and on_message functions into it
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

#this sets up the connections with the mqtt server
mqttc.username_pw_set(mqttUsername, mqttPassword)
mqttc.connect(mqttHost, port=mqttPort)

#this subscribes the mqtt object to the predivined topic
def mqttSubscribe(topic):
    mqttc.subscribe(topic)
    print("subscribed to " + topic)

#this makes the mqtt code go on forever without need for a while true loop in the main code
def mqttLoop():
    global score
    mqttSubscribe(dispenseCandyTopic)
    print("gaat nu loop in")
    mqttc.loop_forever()

#this is the first thing that happens when the thread is created, it puts the servo at 90*, sets up the mqtt object and puts it in a loop
def servoThreadSetup():
    print("servo to max")
    print("test")
    print("test2")
    while(True):
        global score
        print(score)
        sleep(2)

#the lines below make a thread which will run 
#in the back ground as soon as this file is imported
servoThread=Thread(target=servoThreadSetup)
mqttThread=Thread(target=mqttLoop)
servoThread.start()
mqttThread.start()

#this thread will run forever until the program is stopped
while True:
    pass