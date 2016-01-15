# coding=utf-8
# pylint: disable=invalid-name

import unittest

from calc1 import Lexer, Interpreter, Token, INTEGER


class TokenTest(unittest.TestCase):

    def setUp(self):
        self.token = Token(INTEGER, 1)

    def test_str_method_returns_correct_result(self):
        self.assertEqual(self.token.__str__(), 'Token(INTEGER, 1)')

    def test_repr_method_returns_correct_result(self):
        self.assertEqual(self.token.__repr__(), 'Token(INTEGER, 1)')


class TestInterpreter(unittest.TestCase):

    def test_can_handle_addition(self):
        self.assertEqual(Interpreter(Lexer('1 + 2')).expr(), 3)
        self.assertEqual(Interpreter(Lexer('3 + 1')).expr(), 4)

    def test_can_handle_subtraction(self):
        self.assertEqual(Interpreter(Lexer('1 - 2')).expr(), -1)
        self.assertEqual(Interpreter(Lexer('1 - 1')).expr(), 0)
        self.assertEqual(Interpreter(Lexer('5 - 2')).expr(), 3)

    def test_can_multiplication(self):
        self.assertEqual(Interpreter(Lexer('2*5')).expr(), 10)
        self.assertEqual(Interpreter(Lexer('12*3')).expr(), 36)

    def test_can_division(self):
        self.assertEqual(Interpreter(Lexer('20/5')).expr(), 4)
        self.assertEqual(Interpreter(Lexer('7/2')).expr(), 3)

    def test_can_deal_with_multi_digit_numbers(self):
        self.assertEqual(Interpreter(Lexer('43 - 21')).expr(), 22)
        self.assertEqual(Interpreter(Lexer('1230 + 213')).expr(), 1443)

    def test_can_handle_white_spaces(self):
        self.assertEqual(Interpreter(Lexer('3-1')).expr(), 2)
        self.assertEqual(Interpreter(Lexer('3    -  1')).expr(), 2)

    def test_incorrect_syntax_raises_error(self):
        self.assertRaises(Exception, Interpreter(Lexer('3 -')).expr)
        self.assertRaises(Exception, Interpreter(Lexer('3 - a')).expr)

    def test_can_handle_arbitrary_sequence(self):
        self.assertEqual(Interpreter(Lexer('3 + 2 - 1 + 4')).expr(), 8)
        self.assertEqual(Interpreter(Lexer('6/2*3')).expr(), 9)
