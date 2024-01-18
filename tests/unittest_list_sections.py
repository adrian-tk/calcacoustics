#!../env/bin/python

import unittest
import sys
sys.path.append("../")
import os
import tempfile

from solver.list_sections import list_sections
#from common import rootdir

class TestRootDir(unittest.TestCase):
    """test list_section module

    creates directories, especially section directory with 
    .ini files, for checking output"""
    
    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        """ create enviroment with searched files and
        few recursive directories to copy tested file

        Class method is used to create direcroty only one
        time for all tests.

        root:
         +--foo.ini
         +--sec/
         +--solver/
             +--section/
                 +--bar.ini
             +--sections/
                 +--wrong.txt
                 +--very_wrong/
                 +--good.ini
                 +--also_good.ini
                 +--template.ini    # this one is not listed by default 
                 +--and with space.ini
                 +--tricky_one.ini.ini
                 +--good.one.with.dots.ini
                 +--this_one_is_wrong.ini.txt
                 +--wrong_wrong_wrong.paganini
                 +--ini
                 +--.ini
                 +--wrong_again.INI
                 +--terrible_wrong.ini/
        """
        cls.tmpdir = tempfile.TemporaryDirectory()
        with open(cls.tmpdir.name + '/foo.ini', 'x'): pass
        os.mkdir(os.path.join(cls.tmpdir.name, "sec"))
        os.mkdir(os.path.join(cls.tmpdir.name, "solver"))
        os.mkdir(os.path.join(cls.tmpdir.name + "/solver", "section"))
        with open(cls.tmpdir.name + '/solver/section/bar.ini', 'x'): pass
        os.mkdir(os.path.join(cls.tmpdir.name + "/solver", "sections"))
        os.mkdir(os.path.join(
            cls.tmpdir.name + "/solver/sections", "very_wrong"))
        os.mkdir(os.path.join(
            cls.tmpdir.name + "/solver/sections", "terrible_wrong.ini"))
        FILELIST = [
                'wrong.txt',
                'good.ini',
                'also_good.ini',
                'template.ini',
                'and with space.ini',
                'tricky_one.ini.ini',
                'good.one.with.dots',
                'this_one_is_wrong.ini.txt',
                'wrong_wrong_wrong.paganini',
                'ini',
                '.ini',
                'wrong_again.INI',
                ]
        for file in FILELIST:
            with open(cls.tmpdir.name + 
                      '/solver/sections/' + file,
                      'x'): pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        """clean up temporary stuff"""

        cls.tmpdir.cleanup()

    def notest_print(self):
        """script in root called from root
        """
        os.chdir(self.tmpdir.name)
        print(f'root: {os.listdir()}')
        os.chdir(self.tmpdir.name + '/solver')
        print(f'root/solver: {os.listdir()}')
        os.chdir(self.tmpdir.name + '/solver/sections')
        print(f'root/solver/sections: {os.listdir()}')

    def test_default(self):
        """default behavior
        
        expected: listed only basename of *.ini from solver/sections/
        """

        ls = list_sections(self.tmpdir.name + '/solver/sections/')
        FILELIST = [
                'good',
                'also_good',
                'and with space',
                'tricky_one.ini',
                ]
        self.assertEqual(ls, FILELIST)

if __name__ == '__main__':
    unittest.main()
