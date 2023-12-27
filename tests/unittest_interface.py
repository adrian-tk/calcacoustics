#!../env/bin/python
import unittest
import sys
sys.path.append("..")
import interface
import logging
class Dummy():
    """dummy class to imitate solver's object
    Just return some data
    """
    def __init__(self):
        self.name = "dummy object"
        self.par={
                'first':{
                    'name': 'first parameter',
                    'value': 3.0,
                    'unit': 'd',
                    'desc':"some parameter for testing purposes",
                    'calculate': False
                    },
                'second':{
                    'name': 'second parameter',
                    'value': 4.0,
                    'unit': 'k',
                    'desc':"other parameter for testing purposes",
                    'calculate': False
                    },
                }
        def recalculate(self):
            return True
        #def set_val(self):
        #    return 9.81
        def save_to_file(self):
            pass
        def read_from_file(self):
            pass

class TestInterface(unittest.TestCase):
    def setUp(self):
        self.inf=interface.Interface({'dummy': Dummy()})
        #print(self.inf.sections['dummy'].par)

    def test_section(self):
        """proper query for dummy interface returns object"""
        real_ans = self.inf.section({
            "section": "dummy",
            "item": "whatever",
            "action": "whatever",
            "value": "whatever",
        })
        expected_ans = self.inf.sections['dummy']

        self.assertEqual(real_ans, expected_ans)

    def test_section_nok(self):
        """proper query for dummy interface returns None"""
        ans = self.inf.section({
            "section": "whatever",
            "item": "whatever",
            "action": "whatever",
            "value": "whatever",
        })

        self.assertEqual(ans, None)


    def test_send_to_speaker_ok(self):

        real_ans = self.inf.send({
            "section": "speaker",
            "item": "version",
            "action": "get",
            "value": None,
        })
        # remove version number from answer
        #real_ans['value'] = real_ans['value'][:7]

        expected_ans = {
            "section": "speaker",
            "item": "version",
            "action": "answer",
            "value": "0.1",
        }

        self.assertEqual(real_ans, expected_ans)

    def test_send_to_speaker_NOK(self):

        real_ans = self.inf.send({
            "section": "wrong",
            "item": "whatever",
            "action": "get",
            "value": None,
        })

        expected_ans = ("there is no wrong for section GUI sent")

        self.assertEqual(real_ans, expected_ans)


if __name__=='__main__':
    unittest.main()
