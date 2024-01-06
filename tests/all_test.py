#!../env/bin/python


import logging
logging.disable()

import unittest
import unittest_logger
import unittest_convert
import unittest_speaker
import unittest_quantity
import unittest_enclosure
import unittest_interface

suite = unittest.TestSuite()
tl=unittest.TestLoader()
#add test files
suite.addTest(tl.loadTestsFromModule(unittest_logger))
suite.addTest(tl.loadTestsFromModule(unittest_interface))
suite.addTest(tl.loadTestsFromModule(unittest_convert))
suite.addTest(tl.loadTestsFromModule(unittest_quantity))
suite.addTest(tl.loadTestsFromModule(unittest_enclosure))
suite.addTest(tl.loadTestsFromModule(unittest_speaker))
#run all
unittest.TextTestRunner(verbosity=2).run(suite)
