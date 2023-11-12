#!../env/bin/python
import unittest
import sys
sys.path.append("..")
import interface

class TestInterface(unittest.TestCase):
    def setUp(self):
        self.inf=interface.Interface()

    def test_send_to_speaker_ok(self):

        real_ans = self.inf.send({
            "section": "speaker",
            "item": "version",
            "action": "get",
            "value": None,
        })
        # remove version number from answer
        real_ans['value'] = real_ans['value'][:7]

        expected_ans = {
            "section": "speaker",
            "item": "version",
            "action": "answer",
            "value": "speaker",
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
