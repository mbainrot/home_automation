#!/usr/bin/python

# #########################################################
# Unit Test: Test device registration
# Purpose: Tests whether a given device can register
# Author: Max Bainrot (mbainrot)
# Date: 6th April 2015
# Test Detail:
# #########################################################

import unittest
import main

import config
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import time
import os

class test_device_reg(unittest.TestCase):

    def setUp(self):
        # Setup our variables
        self.mac_address = "DE:AD:BE:EF:CA:DE"  # Our fake mac address

        deviceFile = config.working_dir + '/devices/' + self.mac_address

        if(os.path.exists(deviceFile)):
            os.rm(deviceFile)

        self.thrd = main.fork_main()  # Start the server

    def test_device_reg_step_1(self):
        c = test_device_reg_step_1(config,self.mac_address)

        res = c.start()

        self.assertEqual(True,res,res)

    def tearDown(self):
        # Kill the server
        publish.single("abort",payload="abort",hostname=config.mqtt_server,port=1883)

        # Wait long enough for it to shrivel up and DIE
        time.sleep(15)


class test_device_reg_step_1():
    def __init__(self, config, mac):
        # Set our working bits
        self.mac_address = mac
        self.config = config
        self.bStop = False

        self.client = mqtt.Client()

        # Compute extra variables
        self.targeted_sys = "sys_" + self.mac_address

    def start(self):
        client = self.client
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(config.mqtt_server,1883,60)

        self.client = client

        while self.bStop is False:
            client.loop()

        # Compute and return result here :)
        if(not os.path.exists(config.working_dir + '/devices/' + self.mac_address)):
            return (False,"Failed to create devices file")

        return True

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        client.subscribe("sys")
        client.subscribe(self.targeted_sys)

        client.publish("sys","!register|"+ self.mac_address)

    def on_message(self, client, userdata, msg):
        newStr = msg.payload.decode(encoding='ascii')

        print("recv: topic=" + msg.topic + " payload=" + newStr)

        if(msg.topic == "sys"):
            self.handle_sys(client,newStr)
        elif(msg.topic == self.targeted_sys):
            self.handle_targeted_sys(client,newStr)
        else: # Message we don't recognise...
            raise NotImplementedError()

    def handle_sys(self,client,msg):
        parts = msg.split("|")  # FIXME (finish implementation)  # noqa

        if(msg == "!reregister"):
            client.publish("sys","!register|"+self.mac_address)

    def handle_targeted_sys(self,client,msg):
        parts = msg.split("|")

        if(msg == "!registered"):
            # We're now registered!

            # Register to our channels
            client.subscribe("input")
            client.subscribe("output")
            # client.subscribe(targeted_inp_ch)
            # client.subscribe(targeted_out_ch)


            threading.Timer(10, self.timer_bStop).start()

        if(len(parts) == 2):
            cmd,arg = parts

            if(cmd == "!ping"):
                client.publish(self.targeted_sys,"!pong|"+arg)

    def timer_bStop(self):
        self.bStop = True

