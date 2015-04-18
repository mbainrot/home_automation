#!/usr/bin/python

# #########################################################
# Unit Test: Test System Queue
# Purpose: Tests whether the system queue works
# Author: Max Bainrot (mbainrot)
# Date: 5th April 2015
# #########################################################


import unittest
import main
import config
import threading
import time

# Extra stuff for mqtt
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


class test_system_queue(unittest.TestCase):
    strData = ""
    topic = ""
    client = ""

    def _on_message(self, client, userdata, msg):
        self.strData = msg.payload.decode(encoding='ascii')

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def _maintain_mqtt(head, khead):
        head.run = True
        while head.run:
            head.client.loop()

    def setUp(self):
        self.strData = ""

        client = mqtt.Client()
        self.client = client
        self.topic = "sys_ack"
        client.on_connect = self._on_connect
        client.on_message = self._on_message

        client.connect(config.mqtt_server, 1883, 60)

        t = threading.Thread(target=self._maintain_mqtt, args=(self,))
        t.start()

        self.thread = t

        self.thrd = main.fork_main()

        # Test Specifc Stuff

    def _send_delayed_message(self, delay, topic, message):
        time.sleep(delay)
        self.client.publish(topic, message)

    def test_system_queue(self):
        print("testing...")

        kargs = {'topic': "sys",  # 'self': self,
                 'message': "!unittest|4567",
                 'delay': 1.0}

        t = threading.Thread(target=self._send_delayed_message, kwargs=(kargs))
        t.start()

        abortts = int(time.time()) + 15
        while (self.strData == ""):
            self.client.loop()

            if time.time() > abortts:
                self.assertEqual(False, True, "Timed out")

        res = (self.strData == "!hello")

        self.assertEqual(res, True, self.strData + " != '!hello'")

    def tearDown(self):
        self.run = False
        self.client.disconnect()

        # Kill the server
        publish.single("abort", payload="abort", hostname=config.mqtt_server,
                       port=1883)

        # Wait long enough for it to shrivel up and DIE
        time.sleep(15)
