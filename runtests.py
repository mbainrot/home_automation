#!/usr/bin/python

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

res = None

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('./unit_tests')
    res = unittest.TextTestRunner(verbosity=2, failfast=True).run(all_tests)

sys.exit(not res.wasSuccessful())
