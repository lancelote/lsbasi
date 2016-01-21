# coding=utf-8
# pylint: disable=invalid-name

import unittest

from spi import Lexer, Parser, Interpreter, Token, INTEGER
from spi import infix2postfix, infix2lisp


class TokenTest(unittest.TestCase):

    def setUp(self):
        self.token = Token(INTEGER, 1)

    def test_str_method_returns_correct_result(self):
        self.assertEqual(self.token.__str__(), 'Token(INTEGER, 1)')

    def test_repr_method_returns_correct_result(self):
        self.assertEqual(self.token.__repr__(), 'Token(INTEGER, 1)')


class TestInterpreter(unittest.TestCase):

    @staticmethod
    def compute(task):
        lexer = Lexer(task)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        return result

    def test_can_handle_addition(self):
        self.assertEqual(self.compute('1 + 2'), 3)
        self.assertEqual(self.compute('3 + 1'), 4)

    def test_can_handle_subtraction(self):
        self.assertEqual(self.compute('1 - 2'), -1)
        self.assertEqual(self.compute('1 - 1'), 0)
        self.assertEqual(self.compute('5 - 2'), 3)

    def test_can_multiplication(self):
        self.assertEqual(self.compute('2*5'), 10)
        self.assertEqual(self.compute('12*3'), 36)

    def test_can_division(self):
        self.assertEqual(self.compute('20/5'), 4)
        self.assertEqual(self.compute('7/2'), 3)

    def test_can_deal_with_multi_digit_numbers(self):
        self.assertEqual(self.compute('43 - 21'), 22)
        self.assertEqual(self.compute('1230 + 213'), 1443)

    def test_can_handle_white_spaces(self):
        self.assertEqual(self.compute('3-1'), 2)
        self.assertEqual(self.compute('3    -  1'), 2)

    def test_incorrect_syntax_raises_error(self):
        self.assertRaises(SyntaxError, self.compute, '3 -')
        self.assertRaises(SyntaxError, self.compute, '1 (1 + 2)')

    def test_incorrect_characters_raises_error(self):
        self.assertRaises(ValueError, self.compute, '3 - a')

    def test_can_handle_arbitrary_sequence(self):
        self.assertEqual(self.compute('3 + 2 - 1 + 4'), 8)
        self.assertEqual(self.compute('6/2*3'), 9)

    def test_can_handle_operator_precedence(self):
        self.assertEqual(self.compute('6 - 4/2'), 4)
        self.assertEqual(self.compute('2 + 8/2'), 6)
        self.assertEqual(self.compute('14 + 2 * 3 - 6 / 2'), 17)

    def test_can_handle_parentheses(self):
        self.assertEqual(self.compute('7 + 3*(6/(2 + 1))'), 13)
        self.assertEqual(self.compute('7 + (((3 + 2)))'), 12)
        self.assertEqual(self.compute('7 + 3 * (10 / (12 / (3 + 1) - 1))'), 22)

    def test_can_handle_odd_parentheses(self):
        self.assertEqual(self.compute('7 + (((3 + 2)))'), 12)

    def test_can_handle_long_task(self):
        task = '7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)'
        self.assertEqual(self.compute(task), 10)


class TestInfix2Postfix(unittest.TestCase):

    def test_returns_correct_result(self):
        self.assertEqual(infix2postfix('2 + 3'), '2 3 +')

    def test_can_deal_with_multiple_operators(self):
        self.assertEqual(infix2postfix('2 + 3*5'), '2 3 5 * +')

    def test_can_deal_with_parentheses(self):
        task1 = '5 + ((1 + 2) * 4) - 3'
        self.assertEqual(infix2postfix(task1), '5 1 2 + 4 * + 3 -')
        task2 = '(5 + 3) * 12 / 3'
        self.assertEqual(infix2postfix(task2), '5 3 + 12 * 3 /')


class TestInfix2List(unittest.TestCase):

    def test_returns_correct_result(self):
        self.assertEqual(infix2lisp('1 + 2'), '(+ 1 2)')
        self.assertEqual(infix2lisp('2*7'), '(* 2 7)')

    def test_can_deal_with_multiple_operators(self):
        self.assertEqual(infix2lisp('2*7 + 3'), '(+ (* 2 7) 3)')
        self.assertEqual(infix2lisp('2 + 3*5'), '(+ 2 (* 3 5))')
        self.assertEqual(infix2lisp('7 + 5*2 - 3'), '(- (+ 7 (* 5 2)) 3)')
        task = '1 + 2 + 3 + 4 + 5'
        self.assertEqual(infix2lisp(task), '(+ (+ (+ (+ 1 2) 3) 4) 5)')

    def test_can_deal_with_parentheses(self):
        task1 = '5 + ((1 + 2) * 4) - 3'
        self.assertEqual(infix2lisp(task1), '(- (+ 5 (* (+ 1 2) 4)) 3)')
        task2 = '(5 + 3) * 12 / 3'
        self.assertEqual(infix2lisp(task2), '(/ (* (+ 5 3) 12) 3)')
