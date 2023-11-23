#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import os
import configparser

import solver.speaker as speaker


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

    def test_save_to_file(self):
        # check default filename
        tmp_path = "speakers/"
        first_file="speakers/producer_model.ini"
        second_file="speakers/producer_model_1.ini"
        third_filename="lorem_ipsum.ini"
        third_file=tmp_path + third_filename

        # create file with default values
        self.s.save_to_file()
        # check default directory
        self.assertEqual(os.path.isdir(tmp_path), True)
        # check default filename
        self.assertEqual(os.path.isfile(first_file), True)
        svals=[]
        for key, val in self.s.par.items():
            svals.append(key)
        scp = configparser.ConfigParser()
        scp.read(first_file)
        for section in scp.sections():
            if section in svals:
                with self.subTest(i=section):
                    self.assertEqual(scp[section]['name'], self.s.par[section].name)
                    self.assertEqual(scp[section]['value'], '0.0')
                    self.assertEqual(scp[section]['unit'], self.s.par[section].unit)

        # create another file, and check it default name
        self.s.save_to_file()
        self.assertEqual(os.path.isfile(second_file), True)

        # create non default file, with nondefault values
        for key, val in self.s.par.items():
            svals.append(key)
            self.s.par[key].value = '5.4' # some 'random' value
        self.s.save_to_file(third_filename)
        scp = configparser.ConfigParser()
        scp.read(third_file)
        for section in scp.sections():
            if section in svals:
                with self.subTest(i=section):
                    self.assertEqual(scp[section]['name'], self.s.par[section].name)
                    self.assertEqual(scp[section]['value'], '5.4')
                    self.assertEqual(scp[section]['unit'], self.s.par[section].unit)

        # clean up
        try:
            os.remove(first_file)
            os.remove(second_file)
            os.remove(third_file)
            os.rmdir("speakers/")
        except:
            print("++++can't remove speakers directory+++++")


if __name__=='__main__':
    unittest.main()
