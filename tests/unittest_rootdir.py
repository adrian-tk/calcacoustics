#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import glob
import subprocess
import os
import shutil
import tempfile
from common import rootdir

class TestRootDir(unittest.TestCase):
    """test rootdir module"""
    
    def setUp(self):
        """ create enviroment with searched files and
        few recursive directories to copy tested file

        if rootdir.FILES contains: foo.txt, bar.txt:

        root:
         +--foo.txt
         +--bar.txt
         +--one/
         |   +--foo.txt
         |   +--two/
         |     +--three/
         +another_one

        rootdir.py will be copied to root, one, two, and
        working directory will be change and
        desired output will be checked
        proper working is to output root directory from actual directory
        ie when we are in root/one/two it shall be ../../
        only foo.txt without bar.txt shall be ignored
        """

        self.tmpdir = tempfile.TemporaryDirectory()
        os.mkdir(os.path.join(self.tmpdir.name, "one"))
        os.mkdir(os.path.join(self.tmpdir.name, "another_one"))
        os.mkdir(os.path.join(self.tmpdir.name + "/one", "two"))
        os.mkdir(os.path.join(self.tmpdir.name + "/one/two", "three"))
        #create files in root
        self.files_dic={}    # for holding searched files
        for tfile in rootdir.FILES:
            self.files_dic[tfile] = \
                    open(self.tmpdir.name + "/" + tfile, "x")
        # create foo.txt(first file in rootdir.FILES) in root/one
        self.another = open(
                self.tmpdir.name + "/one/" + rootdir.FILES[0], "x"
                )

    def tearDown(self):
        """clean up temporary stuff"""

        for tfile in self.files_dic.values():
            tfile.close()
        self.another.close()
        self.tmpdir.cleanup()

    def test_prefix_root_root(self):
        """script in root called from root
        """
        script = (shutil.copy(
                        rootdir.__file__,
                        self.tmpdir.name
                        )
                  )
        os.chdir(self.tmpdir.name)
        ans = subprocess.run(
                    ["python3", script, "nut"],
                    capture_output=True,
                    text = True
                    )
        self.assertEqual(ans.stdout, '\n')

    def test_prefix_root_one(self):
        """script in root called from one
        """
        script = (shutil.copy(
                        rootdir.__file__,
                        self.tmpdir.name
                        )
                  )
        os.chdir(self.tmpdir.name + '/one')
        ans = subprocess.run(
                    ["python3", script, "nut"],
                    capture_output=True,
                    text = True
                    )
        self.assertEqual(ans.stdout, '../\n')

    def test_prefix_root_another_one(self):
        """script in root called from another_one
        """
        script = (shutil.copy(
                        rootdir.__file__,
                        self.tmpdir.name
                        )
                  )
        os.chdir(self.tmpdir.name + '/another_one')
        ans = subprocess.run(
                    ["python3", script, "nut"],
                    capture_output=True,
                    text = True
                    )
        self.assertEqual(ans.stdout, '../\n')

    def test_prefix_one_one(self):
        """script in one called from one
        """
        script = (shutil.copy(
                        rootdir.__file__,
                        self.tmpdir.name + '/one'
                        )
                  )
        os.chdir(self.tmpdir.name + '/one')
        ans = subprocess.run(
                    ["python3", script, "nut"],
                    capture_output=True,
                    text = True
                    )
        self.assertEqual(ans.stdout, '../\n')

    def test_prefix_one_root(self):
        """script in one called from root
        """
        script = (shutil.copy(
                        rootdir.__file__,
                        self.tmpdir.name + '/one'
                        )
                  )
        os.chdir(self.tmpdir.name)
        ans = subprocess.run(
                    ["python3", script, "nut"],
                    capture_output=True,
                    text = True
                    )
        self.assertEqual(ans.stdout, '\n')

    def test_prefix_one_one(self):
        """script in one called from three
        """
        script = (shutil.copy(
                        rootdir.__file__,
                        self.tmpdir.name + '/one'
                        )
                  )
        os.chdir(self.tmpdir.name + '/one/two/three')
        ans = subprocess.run(
                    ["python3", script, "nut"],
                    capture_output=True,
                    text = True
                    )
        self.assertEqual(ans.stdout, '../../../\n')

if __name__ == '__main__':
    unittest.main()
