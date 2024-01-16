""" functions for looking root directory of scripts

sometimes modules might be used from different places, and this shall
return proper path for looking files eg. .ini
"""

import glob
import sys
sys.path.append("..")

# root directory contain following files and directories
FILES = ['tests', 'solver', 'requirements.txt']

def prefix():
    """return relative directory of root from subdirectiories"""

    rootdir = ''
    lookdir = rootdir + '*'
    upper = '../'
    worklist = []
    max_search = 4
    while max_search > 0:
        for path in glob.glob(lookdir):
            worklist.append(path.split('/')[-1])
        if set(FILES).issubset(worklist):
            max_search = 0
        if max_search > 0:
            worklist = []
            lookdir = upper + lookdir
        max_search = max_search -1
    return (lookdir[:-1])

if __name__ == '__main__':
    if False:
        print(prefix())
    else:
        # if used with nut (no unit test) don't make test
        # important to not fall into infinite loop when testing
        # beacuse file is copied and started as a new process
        if len(sys.argv) == 1 or sys.argv[1] != 'nut':
        # full test from unittest in tests directory
            import unittest
            from tests import unittest_rootdir
            suite = unittest.TestSuite()
            suite.addTest(
                    unittest.TestLoader().loadTestsFromModule(
                        unittest_rootdir
                    )
            )
            unittest.TextTestRunner(verbosity=2).run(suite)
        else:
            # if used with nut don't start test, only return prefix
            print(prefix())
