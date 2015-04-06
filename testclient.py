#!/usr/bin/python

import config # import our configuration

import paho.mqtt.client as mqtt

mac = "DE:AD:00:00:BE:FF"

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
    newStr = str(msg.payload)
    # newStr = newStr.replace("b'","")
    newStr = newStr[2:-1]

    print("recv: topic=" + msg.topic + " payload=" + newStr)

    if(msg.topic == "sys"):
        handle_sys(client,newStr)
    elif(msg.topic == targeted_sys_ch):
        handle_targeted_sys(client,newStr)
    else: # Message we don't recognise...
        raise NotImplementedError()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.mqtt_server,1883,60)

client.loop_forever()
