#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import glob
import subprocess
import os
import shutil
import tempfile
from solver.sections import template

class TestRootDir(unittest.TestCase):
    """test template module"""
    
    def setUp(self):
        self.obj = template.CalcBundle()
        pass

    def tearDown(self):
        pass

    def test_init(self):
        """checking __init__ function"""

        self.assertEqual(self.obj.name, "just template")
        self.assertEqual(self.obj.section_name, "template")
        self.assertEqual(
                list(self.obj.par.keys()),
                ['first', 'second', 'sum'])
        self.assertEqual(
                list(self.obj.dep.keys()),
                ['sum'])
        # check if a input path is ok
        # it might be different in "../.."
        # so only keyword in lists are checked
        # TODO / or \ in win
        path_list = self.obj.input_path.split('/')
        path_check = ['input', 'template']
        self.assertTrue(set(path_check).issubset(path_list))

    def test_cal_sum(self):
        """checking sum function"""
        ans = self.obj.cal_sum(1, 2.14)
        self.assertAlmostEqual(ans, 3.14)

    def test_read_from_file(self):
        """reading from input ini file"""

        self.obj.read_from_file([
            "../../input/template/some_template.ini",
            "../input/template/some_template.ini",
            ])
        self.assertAlmostEqual(self.obj.par['first'].value, 3.0)
        self.assertAlmostEqual(self.obj.par['second'].value, 0.14)
        self.assertAlmostEqual(self.obj.par['sum'].value, 0.0)
        
    def test_change_non_calculated_values(self):
        for element in self.obj.par:
            if not self.obj.par[element].calculate:
                self.obj.par[element].value=0.32
        self.assertAlmostEqual(self.obj.par['first'].value, 0.32)
        self.assertAlmostEqual(self.obj.par['second'].value, 0.32)
        self.assertAlmostEqual(self.obj.par['sum'].value, 0.0)

    def test_calculate_sum(self):
        self.obj.par['first'].value=0.5
        self.obj.par['second'].value=1.5
        ans = self.obj.recalculate('first')
        self.assertAlmostEqual(self.obj.par['first'].value, 0.5)
        self.assertAlmostEqual(self.obj.par['second'].value, 1.5)
        self.assertAlmostEqual(self.obj.par['sum'].value, 2.0)
        # ans shall be list of values to recalculate
        self.assertEqual(ans, ['sum'])

if __name__ == '__main__':
    unittest.main()
