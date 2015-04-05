#!/usr/bin/python

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
