#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import solver.enclosure as enclosure

class TestEnclosure(unittest.TestCase):

    def setUp(self):
        self.e=enclosure.Enclosure()

    def test_calc_int_dim(self):
        self.e.thick.setval(1, 'cm')
        self.e.ext_dims['x'].setval(10, 'cm')
        self.e.ext_dims['y'].setval(20, 'cm')
        self.e.ext_dims['z'].setval(30, 'cm')
        self.e.calc_int_dim()
        self.assertAlmostEqual(self.e.int_dims['x'].getval('cm'), 8)
        self.assertAlmostEqual(self.e.int_dims['y'].getval('cm'), 18)
        self.assertAlmostEqual(self.e.int_dims['z'].getval('cm'), 28)
        self.assertAlmostEqual(self.e.int_dims['v'].getval('l'), 4.032)

if __name__=='__main__':
    unittest.main()
