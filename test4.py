#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: May 5th, 2020
# Version: 1.0

# Import required libraries
import sys
import RPi.GPIO as GPIO
import time
from threading import Thread
from queue import *
import paho.mqtt.client as mqtt

global score
score = "8888"  # numbers and digits to display

delay = 0.005  # delay between digits refresh

q = Queue(maxsize=0)

# --------------------------------------------------------------------
# PINS MAPPING AND SETUP
# selDigit activates the 4 digits to be showed (0 is active, 1 is unactive)
# display_list maps segments to be activated to display a specific number inside the digit
# digitDP activates Dot led
# --------------------------------------------------------------------

selDigit = [40, 26, 38, 8]
# Digits:   1, 2, 3, 4

display_list = [36, 7, 12, 18, 22, 32, 10]  # define GPIO ports to use
# disp.List ref: A ,B ,C,D,E,F ,G

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Set all pins as output
GPIO.setwarnings(False)
for pin in display_list:
    GPIO.setup(pin, GPIO.OUT)  # setting pins for segments
for pin in selDigit:
    GPIO.setup(pin, GPIO.OUT)  # setting pins for digit selector
GPIO.setwarnings(True)

# DIGIT map as array of array ,
# so that arrSeg[0] shows 0, arrSeg[1] shows 1, etc
arrSeg = [
    [1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1],
]

# mqtt cridentials:
mqttUsername = "schardm"
mqttPassword = "4Oyhf3DAoSzxYc9QciX8"
mqttHost = "mqtt.hva-robots.nl"
mqttPort = 1883


# the on_connect function serves no function other than to check if it connected corectly
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# this function makes it so that when an mqtt message is received it will activate the servo function
def on_message(client, userdata, msg):
    if str(msg.topic) == "schardm/pointUpdate":
        score = str(msg.payload)[2:-1]
        print("The new score is: " + score)
        q.put(score)



# this creates the mqtt object and loads the on_connect and on_message functions into it
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# this sets up the connections with the mqtt server
mqttc.username_pw_set(mqttUsername, mqttPassword)
mqttc.connect(mqttHost, port=mqttPort)


# this subscribes the mqtt object to the predivined topic
def mqttSubscribe(topic):
    mqttc.subscribe(topic)
    print("subscribed to " + topic)


# this makes the mqtt code go on forever without need for a while true loop in the main code
def mqttLoop():
    mqttc.loop_forever()


# --------------------------------------------------------------------
# MAIN FUNCTIONS
# splitToDisplay(string) split a string containing numbers and dots in
#   an array to be showed
# showDisplay(array) activates DIGITS according to array. An array
#   element to space means digit deactivation
# --------------------------------------------------------------------


def setScore(newScore):
    score = newScore


def getScore():
    return score


def showDisplay(input):
    for i in range(0, 4):  # loop on 4 digits selectors (from 0 to 3 included)
        sel = [1, 1, 1, 1]
        sel[i] = 0
        GPIO.output(selDigit, sel)  # activates selected digit
        if input[i].replace(".", "") == " ":  # space disables digit
            GPIO.output(display_list, 0)
            continue
        numDisplay = int(input[i].replace(".", ""))
        GPIO.output(
            display_list, arrSeg[numDisplay]
        )  # segments are activated according to digit mapping
        time.sleep(delay)


# def splitToDisplay(toDisplay):  # splits string to digits to display
#     arrToDisplay = list(toDisplay)
#     for i in range(len(arrToDisplay)):
#         if arrToDisplay[i] == ".":
#             arrToDisplay[(i - 1)] = (
#                 arrToDisplay[(i - 1)] + arrToDisplay[i]
#             )  # dots are concatenated to previous array element
#     while "." in arrToDisplay:
#         arrToDisplay.remove(".")  # array items containing dot char alone are removed
#     return arrToDisplay


# --------------------------------------------------------------------
# MAIN LOOP
# persistence of vision principle requires that digits are powered
#   on and off at a specific speed. So main loop continuously calls
#   showDisplay function in an infinite loop to let it appear as
#   stable numbers display
# --------------------------------------------------------------------


def displayScore():
    while True:
        score = q.get()
        print('De score is '+score)
        showDisplay(score)


print("Starting threads")
SevSegThread = Thread(target=displayScore)
SevSegThread.start()
mqttThread = Thread(target=mqttLoop)
mqttThread.start()


# while True:
#     pass

# try:
#     while True:
#         showDisplay("2357")
#     # while True:
#     #     showDisplay(score)
# except KeyboardInterrupt:
#     showDisplay("    ")
#     print("interrupted!")
#     GPIO.cleanup()
