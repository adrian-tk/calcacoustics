#!../env/bin/python

import unittest
import sys
sys.path.append("..")
from solver import logger
import logging

class TestLogger(unittest.TestCase):
    """test logger module"""
    
    # logging.NOTSET    0
    # logging.DEBUG     10
    # logging.INFO      20
    # logging.WARNING   30
    # logging.ERROR     40
    # logging.CRITICAL  50

    def setUp(self):
        self.root = logging.getLogger()
        self.logger=logging.getLogger('calac')
        self.logcom=logging.getLogger('calac.com')
        pass

    def test_check_loggers_default(self):
        # default all shall be warning 
        self.assertEqual(30, self.root.getEffectiveLevel())
        self.assertEqual(30, self.logger.getEffectiveLevel())
        self.assertEqual(30, self.logcom.getEffectiveLevel())

    def test_check_loggers_standard(self):
        logger.setlog('standard')
        self.assertEqual(20, self.root.getEffectiveLevel())
        self.assertEqual(20, self.logger.getEffectiveLevel())
        self.assertEqual(50, self.logcom.getEffectiveLevel())

    def test_check_loggers_standard(self):
        logger.setlog('debug')
        self.assertEqual(20, self.root.getEffectiveLevel())
        self.assertEqual(10, self.logger.getEffectiveLevel())
        self.assertEqual(40, self.logcom.getEffectiveLevel())

    def test_check_loggers_standard(self):
        logger.setlog('silent')
        self.assertEqual(50, self.root.getEffectiveLevel())
        self.assertEqual(50, self.logger.getEffectiveLevel())
        self.assertEqual(50, self.logcom.getEffectiveLevel())

    def test_check_loggers_standard(self):
        logger.setlog('all')
        self.assertEqual(10, self.root.getEffectiveLevel())
        self.assertEqual(10, self.logger.getEffectiveLevel())
        self.assertEqual(10, self.logcom.getEffectiveLevel())



if __name__ == '__main__':
    unittest.main()
