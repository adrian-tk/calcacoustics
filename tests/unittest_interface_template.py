#!../env/bin/python
import unittest
import sys
sys.path.append("..")
import logging
logging.disable(logging.CRITICAL)
import interface
import solver.sections.template as template

class TestInterface(unittest.TestCase):
    def setUp(self):
        self.inf=interface.Interface({'test': template.CalcBundle()})

    def test_get_name(self):
        """proper query for test interface returns object"""
        real_ans = self.inf.ask({
            "section": "test",
            "item": "name",
            "action": "get",
            "value": "whatever",
        })
        expected_ans = ([{
            "section": "test",
            "item": "name",
            "action": "answer",
            "value": "just template",
        }])

        self.assertEqual(real_ans, expected_ans)

    def test_get_list(self):
        real_ans = self.inf.ask({
            "section": "test",
            "item": "list_quantities",
            "action": "get",
            "value": "whatever",
        })
        expected_ans = ([{
            "section": "test",
            "item": "list_quantities",
            "action": "answer",
            "value": "just template",
        }])

        # check some expected values
        self.assertEqual(real_ans[0]['section'], "test")
        self.assertEqual(real_ans[0]['item'], "list_quantities")
        self.assertEqual(real_ans[0]['action'], "answer")
        self.assertEqual(real_ans[0]['value']['first']['name'],
                         "first number")
        self.assertEqual(real_ans[0]['value']['second']['unit'], "-")
        self.assertEqual(real_ans[0]['value']['sum']['value'], 0.0)
        self.assertEqual(real_ans[0]['value']['sum']['dependencies'],
                         "first, second")

    def test_set_value(self):
        """proper query for test interface returns object"""
        real_ans = self.inf.ask({
            "section": "test",
            "item": "first",
            "action": "set",
            "value": "1.0",
        })
        expected_ans = ([{
            "section": "test",
            "item": "first",
            "action": "confirm",
            "value": "1.0",
        }])

        self.assertEqual(real_ans, expected_ans)

    # change to test when error answer will be ready
    def est_section_nok(self):
        """proper query for test interface returns None"""
        ans = self.inf.ask({
            "section": "whatever",
            "item": "whatever",
            "action": "whatever",
            "value": "whatever",
        })

        self.assertEqual(ans, None)

if __name__=='__main__':
    sys.path.append("..")
    unittest.main()
