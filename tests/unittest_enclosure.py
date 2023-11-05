#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import enclosure

class TestEnclosure(unittest.TestCase):

    def setUp(self):
        self.e=enclosure.Enclosure()

    def test_default(self):
        #check if all val are present and set to zero
        names=['Vs', 'we', 'he', 'de', 'thick',
               'we','he','de','v_int','stuffed']
        for name in names:
            with self.subTest(i=name):
                obj=getattr(self.e, name)
                self.assertEqual(getattr(obj, "value"), 0.0,
                                 f"{name} is not zero")

    def test_int_dim(self):
        self.e.thick.setval(1, 'cm')
        ans=self.e.int_dim(1)
        self.assertEqual(ans, 0.98)
        self.e.thick.setval(10, 'cm')
        ans=self.e.int_dim(1)
        self.assertEqual(ans, 0.8)

    def test_int_vol(self):
        self.e.thick.setval(1.6, 'cm')
        self.e.we.setval(20, 'cm')
        self.e.he.setval(1.2, 'm')
        self.e.de.setval(100, 'mm')
        self.e.int_vol()
        self.assertAlmostEqual(self.e.v_int.getval('l'), 13.343232)

if __name__=='__main__':
    unittest.main()
