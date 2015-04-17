#!/usr/bin/python

import config # import our configuration

import paho.mqtt.client as mqtt

import threading
import os
import time

mac = "DE:ED:00:00:BE:EF"

targeted_sys_ch = "sys_" + mac
targeted_inp_ch = "input_" + mac
targeted_out_ch = "output_" + mac



def handle_sys(client,msg):
    parts = msg.split("|")  # FIXME (finish implementation)  # noqa

    if(msg == "!reregister"):
        client.publish("sys","!register|"+mac)

def handle_targeted_sys(client,msg):
    parts = msg.split("|")

    if(msg == "!registered"):
        # We're now registered!

        # Register to our channels
        client.subscribe("input")
        client.subscribe("output")
        client.subscribe(targeted_inp_ch)
        client.subscribe(targeted_out_ch)



    if(len(parts) == 2):
        cmd,arg = parts

        if(cmd == "!ping"):
            client.publish(targeted_sys_ch,"!pong|"+arg)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("sys")
    client.subscribe(targeted_sys_ch)

    client.publish("sys","!register|"+mac)

def on_message(client, userdata, msg):
    newStr = msg.payload.decode(encoding='ascii')

    #print("recv: topic=" + msg.topic + " payload=" + newStr)

    if(msg.topic == "sys"):
        handle_sys(client,newStr)
    elif(msg.topic == targeted_sys_ch):
        handle_targeted_sys(client,newStr)
    elif(msg.topic == targeted_out_ch):
        handle_targeted_output(client,msg,newStr)
    else: # Message we don't recognise...
        strVoid = ""

def handle_targeted_output(client,msg,smsg):
    parts = smsg.split("|")

    # expected msg = component|cmd

    print("recv " + smsg)

    print("parts len " + str(len(parts)))

    if(len(parts) == 2):
        component = parts[0]
        cmd = parts[1]

        if(cmd == "on"):
            if(component == "bulb1"):
                client.bulb_1 = 1
            if(component == "bulb2"):
                client.bulb_2 = 1
            if(component == "bulb3"):
                client.bulb_3 = 1
            if(component == "bulb4"):
                client.bulb_4 = 1

        if(cmd == "off"):
            if(component == "bulb1"):
                client.bulb_1 = 0
            if(component == "bulb2"):
                client.bulb_2 = 0
            if(component == "bulb3"):
                client.bulb_3 = 0
            if(component == "bulb4"):
                client.bulb_4 = 0

def _maintain_mqtt():
    while client.run:
        # os.system('clear')

        client.loop()

def _update_gui():
    while client.run:
        os.system('clear')
        render_lightbulbs()
        time.sleep(0.5)

def render_lightbulbs():
    for n in range(0,4):
        if(client.bulb_1 == 1):
            print(" ###### ",end="")
        else:
            print("        ",end="")

        if(client.bulb_2 == 1):
            print(" ###### ",end="")
        else:
            print("        ",end="")

        if(client.bulb_3 == 1):
            print(" ###### ",end="")
        else:
            print("        ",end="")

        if(client.bulb_4 == 1):
            print(" ###### ",end="")
        else:
            print("        ",end="")

        print("")

    print(" BULB 1 ",end="")
    print(" BULB 2 ",end="")
    print(" BULB 3 ",end="")
    print(" BULB 4 ",end="")

    print("")


client = mqtt.Client()
client.run = True
client.on_connect = on_connect
client.on_message = on_message

client.bulb_1 = 1
client.bulb_2 = 1
client.bulb_3 =1
client.bulb_4 = 1

client.connect(config.mqtt_server,1883,60)

t = threading.Thread(target=_maintain_mqtt)
t.start()

t2 = threading.Thread(target=_update_gui)
t2.start()

while client.run == True:
    print("q) to quit")

    inpt = input("Please select: ")

    if(inpt == "q"):
        client.run = False
