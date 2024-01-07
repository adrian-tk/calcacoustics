class CallExternalFile():

    def __init__(self, path_file_for_test):
        import logging
        logging.disable(logging.CRITICAL)
        import unittest
        import os
        import importlib
        file_name = (os.path.basename(path_file_for_test))
        module_name = os.path.splitext(file_name)[0]
        test_case_module = "unittest_" + module_name
        try:
            module = importlib.import_module("tests." + test_case_module)
        except Exception as err:
            print(f"can't import {test_case_module}")
            print(err)
            print(f"is file {test_case_module}.py exist?")
        suite = unittest.TestSuite()
        suite.addTest(
            unittest.TestLoader().loadTestsFromModule(module))
        unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    import os
    import sys
    os.chdir("../solver/sections")
    sys.path.append('../../')
    print(os.getcwd())
    CallExternalFile("template") 
