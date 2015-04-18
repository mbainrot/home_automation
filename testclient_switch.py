#!/usr/bin/python

import config  # import our configuration

import paho.mqtt.client as mqtt
import threading
import os

mac = "DE:AD:BE:EF:FE:ED"

targeted_sys_ch = "sys_" + mac
targeted_inp_ch = "input_" + mac
targeted_out_ch = "output_" + mac


def handle_sys(client, msg):
    parts = msg.split("|")  # FIXME (finish implementation)  # noqa

    if(msg == "!reregister"):
        client.publish("sys", "!register|"+mac)


def handle_targeted_sys(client, msg):
    parts = msg.split("|")

    if(msg == "!registered"):
        # We're now registered!

        # Register to our channels
        # client.subscribe("input")
        client.subscribe("output")
        client.subscribe(targeted_inp_ch)
        client.subscribe(targeted_out_ch)

    if(msg == "!send_caps"):
        # We're requested to send our capabilities - in this case
        # we're a 4 way light switch!
        client.publish(targeted_sys_ch, "!capability|switch1|pressed")
        client.publish(targeted_sys_ch, "!capability|switch2|pressed")
        client.publish(targeted_sys_ch, "!capability|switch3|pressed")
        client.publish(targeted_sys_ch, "!capability|switch4|pressed")

    if(len(parts) == 2):
        cmd, arg = parts

        if(cmd == "!ping"):
            client.publish(targeted_sys_ch, "!pong|"+arg)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("sys")
    client.subscribe(targeted_sys_ch)

    client.publish("sys", "!register|"+mac)


def on_message(client, userdata, msg):
    newStr = msg.payload.decode(encoding='ascii')

    # print("recv: topic=" + msg.topic + " payload=" + newStr)

    if(msg.topic == "sys"):
        handle_sys(client, newStr)
    elif(msg.topic == targeted_sys_ch):
        handle_targeted_sys(client, newStr)
    else:  # Message we don't recognise...
        strVoid = ""  # noqa


def trigger_event(component, event):
    client.publish(targeted_inp_ch, component + "|" + event)


def _maintain_mqtt():
    while client.run:
        client.loop()


# Setup test client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.run = True

client.connect(config.mqtt_server, 1883, 60)

t = threading.Thread(target=_maintain_mqtt)
t.start()

while client.run is True:
    os.system('clear')
    for n in range(1, 5):
        print(str(n) + ") press switch " + str(n))

    print("q) to quit")

    inpt = input("Please select: ")

    if(inpt == "1" or inpt == "2" or inpt == "3" or inpt == "4"):
        trigger_event("switch"+inpt, "pressed")

    if(inpt == "q"):
        client.run = False
