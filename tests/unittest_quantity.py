#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import quantity


def some_val(a):
    """Return some values of the desired type

    Examples:
        >>> some_val(0.0)
        666.0
        >>> some_val(34)
        666
        >>> some_val("15")
        "lorem ipsum"

    Args:
        a (str or float or int), only the type is important

    Returns:
        str or float or int: this same type as args
    """

    match str(type(a))[8:-2]:
        case "str":
            return "lorem ipsum"
        case "float":
            return 666.0
        case "int":
            return 666
        case other:
            return a
        
        
class TestQuantity(unittest.TestCase):
    def setUp(self):
        self.q=quantity.quantity()

    def test_default(self):
        self.assertEqual(self.q.name, '')
        self.assertEqual(self.q.value, 0.0 )
        self.assertEqual(self.q.unit, '')
        self.assertEqual(self.q.desc, '')
        self.assertEqual(self.q.short_name, '')

    def test_getval(self):
        self.q.value=1000
        self.q.unit="l"
        self.assertEqual(self.q.getval("l"), 1000)
        self.assertEqual(self.q.getval("m3"), 1.0)

    def test_setval(self):
        self.q.setval(50, "l")
        self.assertEqual(self.q.value, 50)
        self.assertEqual(self.q.unit, "l")

    def test_convert(self):
        self.q.value=1000
        self.q.unit="l"
        self.q.convert("l")
        self.assertEqual(self.q.value, 1000)
        self.assertEqual(self.q.unit, "l")
        self.q.convert("m3")
        self.assertEqual(self.q.value, 1)
        self.assertEqual(self.q.unit, "m3")
        self.q.setval(500, "l")
        self.assertEqual(self.q.getval("m3"), 0.5)
    def test_dictionary(self):
        #put a attributes to test here
        names=['name', 'short_name', 'value', 'unit', 'desc']

        dic=self.q.dictionary()
        for name in names:
            with self.subTest(i=name):
                #check def value
                obj=getattr(self.q, name)
                self.assertEqual(obj, dic[name])
                #set some val, and check again
                setattr(self.q, name, some_val(obj))
                obj=getattr(self.q, name)
                dic=self.q.dictionary()
                self.assertEqual(obj, dic[name])

if __name__=='__main__':
    unittest.main()
