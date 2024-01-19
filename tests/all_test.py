#!../env/bin/python

import logging
logging.disable()

import unittest
import unittest_logger
import unittest_convert
import unittest_quantity
import unittest_rootdir
import unittest_list_sections
import unittest_interface

suite = unittest.TestSuite()
tl=unittest.TestLoader()
#add test files
#suite.addTest(tl.loadTestsFromModule(unittest_logger))
suite.addTest(tl.loadTestsFromModule(unittest_convert))
suite.addTest(tl.loadTestsFromModule(unittest_quantity))
#TODO don't work in that order of rootdir and interface
#suite.addTest(tl.loadTestsFromModule(unittest_rootdir))
suite.addTest(tl.loadTestsFromModule(unittest_interface))
suite.addTest(tl.loadTestsFromModule(unittest_list_sections))
#run all
unittest.TextTestRunner(verbosity=2).run(suite)
