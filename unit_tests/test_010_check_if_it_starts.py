#!/usr/bin/python

# #########################################################
# Unit Test: Test If System Starts
# Purpose: Tests whether the system even starts
# Author: Max Bainrot (mbainrot)
# Date: 5th April 2015
# #########################################################

import unittest
import main

import config
import paho.mqtt.publish as publish
import time


class test_startup(unittest.TestCase):

    def setUp(self):
        print()

    def test_startup(self):
        self.thrd = main.fork_main()

        self.assertEqual(self.thrd.is_alive(), True)

    def tearDown(self):
        # Kill the server
        publish.single("abort", payload="abort", hostname=config.mqtt_server,
                       port=1883)

        # Wait long enough for it to shrivel up and DIE
        time.sleep(15)
