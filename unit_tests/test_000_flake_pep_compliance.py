#!/usr/bin/python

# #########################################################
# Unit Test: Test flake8 Compliance
# Purpose: Tests whether the system complies with flake8
# This tests for
# - Saneness (picks up undefined stuff)
# - PEP compliance
# Author: Max Bainrot (mbainrot)
# Date: 6th April 2015
# #########################################################

import unittest

import flake8.main
import os


class test_flake_pep_compliance(unittest.TestCase):

    def setUp(self):
        self.files = ()

        searchPath = os.path.dirname(os.path.realpath(__file__)) + '/../'

        for file in os.listdir(searchPath):
            if file.endswith(".py"):
                self.files += (file,)

        print("I have a total of " + str(len(self.files)) +
              " file(s) to process")

    def test_compliance(self):
        for file in self.files:
            print("Checking file: " + file)
            res = flake8.main.check_file(file, ignore=('E501'))

            if res > 0:
                strErrorBuffer = "\n"
                strErrorBuffer += "File: \"" + file + "\" failed with " + \
                                  str(res) + " validation errors" + "\n"
                self.assertEqual(True, False, strErrorBuffer)

    def tearDown(self):
        strVoid = ""  # noqa
