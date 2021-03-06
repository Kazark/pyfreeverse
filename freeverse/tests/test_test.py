#!/usr/bin/python3

import unittest

from freeverse import test

class TestStepTests(unittest.TestCase):
    def test_step_has_description(self):
        step = test.Step('True', lambda: True)
        self.assertEqual('True', step.description())

    def test_runs_zero_argument_test_step(self):
        stepResult = test.Step('True', lambda: True).run()
        self.assertTrue(stepResult)

    def test_passes_previous_step_result_to_one_argument_test_step(self):
        stepResult = test.Step('description', lambda x: x).run(7)
        self.assertEqual(7, stepResult)

    def test_partially_applies_previous_step_result_to_two_argument_test_step(self):
        stepResult = test.Step('Power function', lambda x, y: pow(x, y)).run(2)
        self.assertEqual(8, stepResult(3))

    def test_partially_applies_previous_step_result_to_two_argument_test_step(self):
        stepResult = test.Step('Power function', lambda x, y, z: x + y + z).run(1)
        self.assertEqual(6, stepResult(2, 3))

    @unittest.skip('This is a known issue')
    def test_does_not_blow_up_when_trying_to_introspect_on_builtin_function(self):
        stepResult = test.Step('Power function', pow).run(2)
        self.assertEqual(8, stepResult(3))

class TestCaseTests(unittest.TestCase):
    def test_runs_set_of_one_test(self):
        testResult = test.Case([test.Step('True', lambda: True)]).run()
        self.assertTrue(testResult.message())

    def test_passes_result_of_one_step_into_the_next(self):
        testResult = test.Case([
            test.Step('1024', lambda: 1024),
            test.Step('plus 313', lambda x: x + 313)
        ]).run()
        self.assertEqual(1337, testResult.message())

    def test_considers_test_to_have_passed_if_last_step_returns_empty_string(self):
        testResult = test.Case([
            test.Step('1024', lambda: 1024),
            test.Step('plus 313', lambda x: '')
        ]).run()
        self.assertTrue(testResult.passed())

    def test_considers_test_to_have_failed_if_last_step_returns_failure_message(self):
        testResult = test.Case([
            test.Step('1024', lambda: 1024),
            test.Step('plus 313', lambda x: 'failure message')
        ]).run()
        self.assertFalse(testResult.passed())

    def test_considers_test_to_have_failed_if_a_step_blew_up(self):
        testResult = test.Case([
            test.Step('1024', lambda: blow_up),
            test.Step('plus 313', lambda x: '')
        ]).run()
        self.assertFalse(testResult.passed())

class TestSuiteTests(unittest.TestCase):
    def test_returns_one_result_for_each_test_case(self):
        cases = [
            test.Case([test.Step("One", lambda: 1)]),
            test.Case([test.Step("Two", lambda: 2)]),
            test.Case([test.Step("Three", lambda: 3)])
        ]

        result = test.Suite(cases).run()

        self.assertEqual(3, len(result))
