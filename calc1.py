# coding=utf-8
# pylint: disable=too-few-public-methods

"""
Simple calculator
"""

# Token types
#
# EOF (end-of-file) token is used to indicate that there is no more input left
# for lexical analysis
INTEGER, EOF = 'INTEGER', 'EOF'
PLUS, MINUS, MUL, DIV = 'PLUS', 'MINUS', 'MUL', 'DIV'


class Token(object):

    def __init__(self, token_type, value):
        # Token types
        self.type = token_type
        # Token values: [0-9], '+', '-' or None
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
        raise Exception('Invalid character')

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

            self.error()

        return Token(EOF, None)


class Interpreter(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()  # First token

    @staticmethod
    def error():
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # Compare the current token type with the passed token type and if
        # they match then "eat" the current token and assign the next token
        # to the self.current_token, otherwise raise the exception
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """Return an INTEGER token value

        factor : INTEGER
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """Parser / Interpreter

        expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.factor()

        while self.current_token.type in (PLUS, MINUS, MUL, DIV):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.factor()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.factor()
            elif token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result //= self.factor()

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
