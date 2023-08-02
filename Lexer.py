from Const import *
from Token import Token

class Lexer:
    def __init__(self, source):
        self.source = source
        self.reset()
    def reset(self):
        self.source_lines = self.source.split("\n")
        self.position = -1
        self.line = 1
        self.current_char = None
        self.advance()
    def advance(self):
        self.position += 1
        if self.position < len(self.source):
            self.current_char = self.source[self.position]
        else:
            self.current_char = None
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char == " ":
            self.advance()
    def skip_comment(self):
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()
    def get_int(self):
        result = ""
        while self.current_char is not None and self.current_char.lower() in "0123456789abcdef":
            result = result + self.current_char
            self.advance()
        return result
    def get_label_or_opcode(self):
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ("_", ".")):
            result += self.current_char
            self.advance()
        return result
    def next_token(self):
        if self.current_char is None:
            return Token(self.line, EOF, EOF)

        while self.current_char == " ":
            self.skip_whitespace()
        if self.current_char == ";":
            self.skip_comment()
            self.line += 1
            return Token(self.line - 1, NEWLINE, NEWLINE)

        if self.current_char.isdigit() or self.current_char in ("$", "%"):
            if self.current_char == "$":
                self.advance()
                dec = int(self.get_int(), 16)
                if dec > 65535:
                    raise Exception("Illegal quantity")
                return Token(self.line, NUMBER, dec)
            if self.current_char == "%":
                self.advance()
                dec = int(self.get_int(), 2)
                if dec > 65535:
                    raise Exception("Illegal quantity")
                return Token(self.line, NUMBER, dec)
            dec = int(self.get_int())
            if dec > 65535:
                raise Exception("Illegal quantity")
            return Token(self.line, NUMBER, dec)

        if self.current_char == "+":
            self.advance()
            return Token(self.line, PLUS, PLUS)
        if self.current_char == "-":
            self.advance()
            return Token(self.line, MINUS, MINUS)
        if self.current_char == "*":
            self.advance()
            return Token(self.line, MUL, MUL)
        if self.current_char == "/":
            self.advance()
            return Token(self.line, DIV, DIV)

        if self.current_char == "&":
            self.advance()
            return Token(self.line, AND, AND)
        if self.current_char == "|":
            self.advance()
            return Token(self.line, OR, OR)
        if self.current_char == "^":
            self.advance()
            return Token(self.line, EOR, EOR)

        if self.current_char == ",":
            self.advance()
            return Token(self.line, COMMA, COMMA)
        if self.current_char == "#":
            self.advance()
            return Token(self.line, HASH, HASH)

        if self.current_char == "(":
            self.advance()
            return Token(self.line, LPAREN, LPAREN)
        if self.current_char == ")":
            self.advance()
            return Token(self.line, RPAREN, RPAREN)
        if self.current_char == "<":
            self.advance()
            return Token(self.line, LT, LT)
        if self.current_char == ">":
            self.advance()
            return Token(self.line, GT, GT)
        if self.current_char == "=":
            self.advance()
            return Token(self.line, ASSIGN, ASSIGN)
        if self.current_char == ":":
            self.advance()
            return Token(self.line, COLON, COLON)
        if self.current_char == "\n":
            self.advance()
            self.line += 1
            return Token(self.line - 1, NEWLINE, NEWLINE)
        if self.current_char.isalpha() or self.current_char in ("_", "."):
            text = self.get_label_or_opcode()
            if text.lower() in OPCODES:
                return Token(self.line, OPCODE, text.lower())
            if text.lower() in ("org", "base", ".ba"):
                return Token(self.line, ORG, ORG)
            if text.lower() in ("let"):
                return Token(self.line, LET, LET)
            if text.lower() in ("byte", "byt", ".by"):
                return Token(self.line, BYTE, BYTE)
            return Token(self.line, LABEL, text)
        raise Exception(f"Syntax ({self.current_char})")
    def get_tokens(self):
        try:
            result = []
            while True:
                token = self.next_token()
                result.append(token)
                if (token.token_type == EOF):
                    break
            return result
        except Exception as e:
            print(f"Lexer: {e} in {self.line}")

if __name__ == "__main__":
    lexer = Lexer("lda:lda\nlda")
    tokens = lexer.get_tokens()
    assert len(tokens) == 6
    assert tokens[0] == Token(1, OPCODE, "lda")
    assert tokens[1] == Token(1, COLON, COLON)
    assert tokens[2] == Token(1, OPCODE, "lda")
    assert tokens[3] == Token(1, NEWLINE, NEWLINE)
    assert tokens[4] == Token(2, OPCODE, "lda")
    assert tokens[5] == Token(2, EOF, EOF)

    lexer = Lexer("lda ($f + %101 * 3),y")
    tokens = lexer.get_tokens()
    assert len(tokens) == 11
    assert tokens[0] == Token(1, OPCODE, "lda")
    assert tokens[1] == Token(1, LPAREN, LPAREN)
    assert tokens[2] == Token(1, NUMBER, 15)
    assert tokens[3] == Token(1, PLUS, PLUS)
    assert tokens[4] == Token(1, NUMBER, 5)
    assert tokens[5] == Token(1, MUL, MUL)
    assert tokens[6] == Token(1, NUMBER, 3)
    assert tokens[7] == Token(1, RPAREN, RPAREN)
    assert tokens[8] == Token(1, COMMA, COMMA)
    assert tokens[9] == Token(1, LABEL, "y")
    assert tokens[10] == Token(1, EOF, EOF)

    lexer = Lexer("65535 +2-10")
    tokens = lexer.get_tokens()
    assert len(tokens) == 6
    assert tokens[0] == Token(1, NUMBER, 65535)
    assert tokens[1] == Token(1, PLUS, PLUS)
    assert tokens[2] == Token(1, NUMBER, 2)
    assert tokens[3] == Token(1, MINUS, MINUS)
    assert tokens[4] == Token(1, NUMBER, 10)
    assert tokens[5] == Token(1, EOF, EOF)

    lexer = Lexer("Test")
    tokens = lexer.get_tokens()
    assert len(tokens) == 2
    assert tokens == [Token(1, LABEL, "Test"), Token(1, EOF, EOF)]

    lexer = Lexer(";1  \n  ;2  \n;3\na = 8") # Every comment creates a NEWLINE
    tokens = lexer.get_tokens()
    assert len(tokens) == 7
    assert tokens == [
        Token(1, NEWLINE, NEWLINE), Token(2, NEWLINE, NEWLINE), Token(3, NEWLINE, NEWLINE),
        Token(4, LABEL, "a"), Token(4, ASSIGN, ASSIGN), Token(4, NUMBER, 8),
        Token(4, EOF, EOF)
    ]

    lexer = Lexer("byte 0, xx,y, label") # Every comment creates a NEWLINE
    tokens = lexer.get_tokens()
    assert len(tokens) == 9
    assert tokens == [
        Token(1, BYTE, BYTE), Token(1, NUMBER, 0), Token(1, COMMA, COMMA),
        Token(1, LABEL, "xx"), Token(1, COMMA, COMMA), Token(1, LABEL, "y"),
        Token(1, COMMA, COMMA), Token(1, LABEL, "label"),
        Token(1, EOF, EOF)
    ]

    print("Lexer: Ok")