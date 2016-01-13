# coding=utf-8

"""
Simple calculator
"""

# Token types
#
# EOF (end-of-file) token is used to indicate that there is no more input left
# for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token(object):

    def __init__(self, token_type, value):
        # Token types: INTEGER, PLUS, MINUS, EOF
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


class Interpreter(object):

    def __init__(self, text):
        self.text = text  # Client string input, ex. '3+5'
        self.pos = 0  # Index into self.text
        self.current_token = None
        self.current_char = self.text[self.pos]

    @staticmethod
    def error():
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicate EOF
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
        One token at a time.
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

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        # Compare the current token type with the passed token type and if
        # they match then "eat" the current token and assign the next token
        # to the self.current_token, otherwise raise the exception
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """Parser / Interpreter

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        self.current_token = self.get_next_token()

        # We expect the current_token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # We expect the current_token to be a plus or minus operator
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        # We expect the current_token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        # After the above code the current_token is set to be EOF

        # At this point INTEGER OP INTEGER sequence of tokens has been
        # successfully found and the method can just return the result,
        # thus effectively interpreting client input
        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
