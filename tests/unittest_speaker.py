#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import speaker

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

class TestSpeaker(unittest.TestCase):
    def setUp(self):
        self.s=speaker.Speaker()

    def test_default(self):
        for key, y in self.s.par.items():
            with self.subTest(x=key):
                #check if default is 0
                self.assertEqual(self.s.par[key].value, 0.0,
                                 f"default value in {key} is not 0.0")
                #check if name and desc are not empty
                self.assertNotEqual(self.s.par[key].name, "",
                                    f"name in {key} is empty")
                self.assertEqual(self.s.par[key].short_name, "")
                self.assertNotEqual(self.s.par[key].desc, "",
                                    f"description in {key} is empty")

    def test_key_as_short_name(self):
        for key, val in self.s.par.items():
            with self.subTest(x=key):
                self.assertEqual(self.s.par[key].short_name, "")
        self.s.key_as_short_name()
        for key, val in self.s.par.items():
            with self.subTest(x=key):
                self.assertEqual(self.s.par[key].short_name, key)


if __name__=='__main__':
    unittest.main()
