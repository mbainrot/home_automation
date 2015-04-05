#!/usr/bin/python

# #########################################################
# Unit Test: Test If System Starts
# Purpose: Tests whether the system even starts
# Author: Max Bainrot (mbainrot)
# Date: 5th April 2015
# #########################################################

import unittest
import main

class test_startup(unittest.TestCase):

    def setUp(self):
        strVoid = ""

    def test_startup(self):
        self.thrd = main.fork_main()

        self.assertEqual(self.thrd.is_alive(),True)

    def tearDown(self):
        strVoid = ""
