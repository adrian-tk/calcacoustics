#!../env/bin/python
"""Script for run multiple tests

all tests included in test_list shall
be executed. In test list shall be basenames
of test script (without .py)
"""

import logging
logging.disable()
from importlib import import_module
import unittest

test_list = [
# ======put test modules here====== #
        #'unittest_logger',
        'unittest_convert',
        'unittest_quantity',
        #'unnecessery_module',
        'unittest_rootdir',
        'unittest_interface',
        'unittest_list_sections',
        'unittest_template',
# ======end of putting area======== #
        ]
# create dictionary {module name: loaded module}
test_dic = {}
for test_case in test_list:
    test_dic[test_case] = import_module(test_case)

# load test cases using dictionary values (loaded modules)
suite = unittest.TestSuite()
for val in test_dic.values():
    suite.addTest(unittest.TestLoader().loadTestsFromModule(val))

# run tests
unittest.TextTestRunner(verbosity=2).run(suite)
