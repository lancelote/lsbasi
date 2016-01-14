# coding=utf-8

import unittest

from calc1 import Interpreter, Token, INTEGER


class TokenTest(unittest.TestCase):

    def setUp(self):
        self.token = Token(INTEGER, 1)

    def test_str_method_returns_correct_result(self):
        self.assertEqual(self.token.__str__(), 'Token(INTEGER, 1)')

    def test_repr_method_returns_correct_result(self):
        self.assertEqual(self.token.__repr__(), 'Token(INTEGER, 1)')


class TestInterpreter(unittest.TestCase):

    def test_can_sum_two_numbers(self):
        self.assertEqual(Interpreter('1 + 2').expr(), 3)
        self.assertEqual(Interpreter('3 + 1').expr(), 4)

    def test_can_subtract_two_numbers(self):
        self.assertEqual(Interpreter('1 - 2').expr(), -1)
        self.assertEqual(Interpreter('1 - 1').expr(), 0)
        self.assertEqual(Interpreter('5 - 2').expr(), 3)

    def test_can_deal_with_multi_digit_numbers(self):
        self.assertEqual(Interpreter('43 - 21').expr(), 22)
        self.assertEqual(Interpreter('1230 + 213').expr(), 1443)

    def test_can_handle_white_spaces(self):
        self.assertEqual(Interpreter('3-1').expr(), 2)
        self.assertEqual(Interpreter('3    -  1').expr(), 2)

    def test_incorrect_syntax_raises_error(self):
        self.assertRaises(Exception, Interpreter('3 -').expr)
        self.assertRaises(Exception, Interpreter('3 - a').expr)
