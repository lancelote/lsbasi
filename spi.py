# coding=utf-8
# pylint: disable=too-few-public-methods,too-many-return-statements

"""
Simple calculator
"""

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that there is no more input left
# for lexical analysis
INTEGER, LEFT_PAREN, RIGHT_PAREN, EOF = 'INTEGER', '(', ')', 'EOF'
PLUS, MINUS, MUL, DIV = 'PLUS', 'MINUS', 'MUL', 'DIV'


class Token(object):

    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        """String representation of the class instance

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token(%s, %s)' % (self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text  # Client string input
        self.pos = 0      # Index into self.text
        self.current_char = self.text[self.pos]

    @staticmethod
    def error():
        raise ValueError('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # EOF
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multi digit) integer consumed from the input"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence apart into tokens.
        One token at a time
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LEFT_PAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RIGHT_PAREN, ')')

            self.error()

        return Token(EOF, None)

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):

    pass


class BinOp(AST):

    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right


class Num(AST):

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    @staticmethod
    def error():
        raise SyntaxError('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LEFT_PAREN expr RIGHT_PAREN"""
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LEFT_PAREN:
            self.eat(LEFT_PAREN)
            node = self.expr()
            self.eat(RIGHT_PAREN)
            return node

        self.error()

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, operator=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, operator=token, right=self.term())

        return node

    def parse(self):
        node = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return node


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################


class NodeVisitor(object):

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    @staticmethod
    def generic_visit(node):
        raise AttributeError('No visit_%s method' % type(node).__name__.lower())


class Interpreter(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser

    def visit_binop(self, node):
        if node.operator.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.operator.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.operator.type == MUL:
            return self.visit(node.left)*self.visit(node.right)
        elif node.operator.type == DIV:
            return self.visit(node.left)//self.visit(node.right)

    @staticmethod
    def visit_num(node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


class Infix2PostfixTranslator(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser

    def visit_binop(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return '%s %s %s' % (left, right, node.operator.value,)

    @staticmethod
    def visit_num(node):
        return node.value

    def translate(self):
        tree = self.parser.parse()
        return self.visit(tree)


class Infix2LispTranslator(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser

    def visit_binop(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return '(%s %s %s)' % (node.operator.value, left, right,)

    @staticmethod
    def visit_num(node):
        return node.value

    def translate(self):
        tree = self.parser.parse()
        return self.visit(tree)


def infix2postfix(text):
    """Translate task to postfix style notation

    Args:
        text (str): task "1 + 2"

    Returns:
        str: postfix style notation "1 2 +"
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    translator = Infix2PostfixTranslator(parser)
    translation = translator.translate()
    return translation


def infix2lisp(text):
    """Translate task to Lisp style notation

    Args:
        text (str): task "1 + 2"

    Returns:
        str: List style notation "(+ 1 2)"
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    translator = Infix2LispTranslator(parser)
    translation = translator.translate()
    return translation


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()
