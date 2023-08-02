IMPLIED=0 # 1 Byte (implied and akku)
RELATIVE=1; ZP=2; ZPX=3; ZPY=4; USELESS=5; INDIRECTY=6; IMMEDIATE=7 # 2 Byte 
ABSOLUTE=10; ABSOLUTEX=11; ABSOLUTEY=12; INDIRECT=13 # 3 Byte

EOF="EOF"
LET="LET"
NUMBER = "Number"
PLUS ="Plus";MINUS="Minus";MUL="Mul";DIV="Div";LPAREN="LParen";RPAREN="RParen"
LT="<";GT=">"
HASH="#";COMMAX=",x";COMMAY=",y"
COLON=":";NEWLINE="Newline"
ASSIGN="Assign"
ORG="Org"
OPCODE="Opcode"
LABEL="Label"

OPCODES = {
    "adc": { USELESS: 0x61, ZP: 0x65, IMMEDIATE: 0x69, ABSOLUTE: 0x6d, INDIRECTY: 0x71, ZPX: 0x75, ABSOLUTEY: 0x79, ABSOLUTEX: 0x7d },
    "and": { USELESS: 0x21, ZP: 0x25, IMMEDIATE: 0x29, ABSOLUTE: 0x2d, INDIRECTY: 0x31, ZPX: 0x35, ABSOLUTEY: 0x39, ABSOLUTEX: 0x3d },
    "asl": { ABSOLUTE: 0x0e, ZP: 0x06, IMPLIED: 0x0a, ZPX: 0x16, ABSOLUTEX: 0x1e },
    "bcc": { RELATIVE: 0x90 },
    "bcs": { RELATIVE: 0xb0 },
    "beq": { RELATIVE: 0xf0 },
    "bne": { RELATIVE: 0xd0 },
    "bmi": { RELATIVE: 0x30 },
    "bpl": { RELATIVE: 0x10 },
    "bvc": { RELATIVE: 0x50 },
    "bvs": { RELATIVE: 0x70 },
    "bit": { ZP: 0x24, ABSOLUTE: 0x2c },
    "brk": { IMPLIED: 0x00 },
    "clc": { IMPLIED: 0x18 },
    "cld": { IMPLIED: 0xd8 },
    "cli": { IMPLIED: 0x58 },
    "clv": { IMPLIED: 0xb8 },
    "cmp": { USELESS: 0xc1, ZP: 0xc5, IMMEDIATE: 0xc9, ABSOLUTE: 0xcd, INDIRECTY: 0xd1, ZPX: 0xd5, ABSOLUTEY: 0xd9, ABSOLUTEX: 0xdd },
    "cpx": { IMMEDIATE: 0xe0, ZP: 0xe4, ABSOLUTE: 0xec },
    "cpy": { IMMEDIATE: 0xc0, ZP: 0xc4, ABSOLUTE: 0xcc },
    "dec": { ZP: 0xc6, ABSOLUTE: 0xce, ZPX: 0xd6, ABSOLUTEX: 0xde },
    "dex": { IMPLIED: 0xca },
    "dey": { IMPLIED: 0x88 },
    "eor": { USELESS: 0x41, ZP: 0x45, IMMEDIATE: 0x49, ABSOLUTE: 0x4d, INDIRECTY: 0x51, ZPX: 0x55, ABSOLUTEY: 0x59 , ABSOLUTEX: 0x5d},
    "inc": { ZP: 0xe6, ABSOLUTE: 0xee,ZPX: 0xf6, ABSOLUTEX: 0xfe },
    "inx": { IMPLIED: 0xe8 },
    "iny": { IMPLIED: 0xc8 },
    "jmp": { ABSOLUTE: 0x4c, INDIRECT: 0x6c },
    "jsr": { ABSOLUTE: 0x20 },
    "lda": { USELESS: 0xa1, ZP: 0xa5, IMMEDIATE: 0xa9, ABSOLUTE: 0xad, INDIRECTY: 0xb1, ZPX: 0xb5, ABSOLUTEY: 0xb9 , ABSOLUTEX: 0xbd},
    "ldx": { IMMEDIATE: 0xa2, ZP: 0xa6, ABSOLUTE: 0xae, ZPY: 0xb6, ABSOLUTEY: 0xbe },
    "ldy": { IMMEDIATE: 0xa0, ZP: 0xa4, ABSOLUTE: 0xac, ZPX: 0xb4, ABSOLUTEX: 0xbc },
    "lsr": { ZP: 0x46, IMPLIED: 0x4a, ABSOLUTE: 0x4e, ZPX: 0x56, ABSOLUTEX: 0x5e },
    "nop": { IMPLIED: 0xea },
    "ora": { USELESS: 0x01, ZP: 0x05, IMMEDIATE: 0x09, ABSOLUTE: 0x0d, INDIRECTY: 0x11, ZPX: 0x15, ABSOLUTEY: 0x19, ABSOLUTEX: 0x1d },
    "pha": { IMPLIED: 0x48 },
    "php": { IMPLIED: 0x08 },
    "pla": { IMPLIED: 0x68 },
    "plp": { IMPLIED: 0x28 },
    "rol": { ZP: 0x26, IMPLIED: 0x2a, ABSOLUTE: 0x2e, ZPX: 0x36, ABSOLUTEX: 0x3e },
    "ror": { ZP: 0x66, IMPLIED: 0x6a, ABSOLUTE: 0x6e, ZPX: 0x76, ABSOLUTEX: 0x7e },
    "rti": { IMPLIED: 0x40 },
    "rts": { IMPLIED: 0x60 },
    "sbc": { USELESS: 0xe1, ZP: 0xe5, IMMEDIATE: 0xe9, ABSOLUTE: 0xed, INDIRECTY: 0xf1, ZPX: 0xf5, ABSOLUTEY: 0xf9, ABSOLUTEX: 0xfd},
    "sec": { IMPLIED: 0x38 },
    "sed": { IMPLIED: 0xf8 },
    "sei": { IMPLIED: 0x78 },
    "sta": { USELESS: 0x81, ZP: 0x85, ABSOLUTE: 0x8d, INDIRECTY: 0x91, ZPX: 0x95, ABSOLUTEY: 0x99, ABSOLUTEX: 0x9d },
    "stx": { ZP: 0x86, ABSOLUTE: 0x8e, ZPY: 0x96 },
    "sty": { ZP: 0x84, ABSOLUTE: 0x8c, ZPX: 0x94 },
    "tax": { IMPLIED: 0xaa },
    "tay": { IMPLIED: 0xa8 },
    "tsx": { IMPLIED: 0xba },
    "txa": { IMPLIED: 0x8a },
    "txs": { IMPLIED: 0x9a },
    "tya": { IMPLIED: 0x98 }
}
class Token:
    def __init__(self, line, token_type, value):
        self.token_type = token_type
        self.value = value
        self.line = line
        # print(self)
    def __str__(self):
        return f'Token ({self.line}, "{self.token_type}", "{self.value}")'
    def __repr__(self):
        return self.__str__()
class Lexer:
    def __init__(self, source):
        self.reset()
    def reset(self):
        self.source = source
        self.source_lines = source.split("\n")
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
        
        if self.current_char == ",":
            self.advance()
            if self.current_char.lower() == "x":
                self.advance()
                return Token(self.line, COMMAX, COMMAX)
            if self.current_char.lower() == "y":
                self.advance()
                return Token(self.line, COMMAY, COMMAY)
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
            print(f"{e} in {self.line}")
class Assembler:
    def __init__(self, lexer, labels):
        self.lexer = lexer
        self.labels = labels
        self.pc = 0
        self.current_token = self.lexer.next_token()
        self.line = self.current_token.line
        self.run = 1
    def assemble(self):
        try:
            self.lexer.reset()
            self.pc = 0
            self.current_token = self.lexer.next_token()
            self.line = self.current_token.line
            print("Pass 1")
            self.run = 1
            self.compile() # pass 1: define labels

            self.lexer.reset()
            self.pc = 0
            self.current_token = self.lexer.next_token()
            self.line = self.current_token.line
            print("Pass 2")
            self.run = 2
            self.compile() # pass 2: assemble
        except Exception as e:
            print(f"{e} in {self.line}")

    def skip(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.next_token()
            self.line = self.current_token.line
        else:
            raise Exception(f"Syntax (Expected: {token_type}, got: {self.current_token.token_type})")
    def factor(self):
        # print("factor",self.current_token)
        if self.current_token.token_type == LPAREN:
            self.skip(LPAREN)
            result = self.expression()
            self.skip(RPAREN)
            return result
        if self.current_token.token_type == NUMBER:
            token = self.current_token
            self.skip(NUMBER)
            return token.value
        if self.current_token.token_type == LT:
            self.skip(LT)
            return self.expression() % 256
        if self.current_token.token_type == GT:
            self.skip(GT)
            return self.expression() // 256
        if self.current_token.token_type == LABEL:
            token = self.current_token
            self.skip(LABEL)
            if token.value not in self.labels:
                self.labels[token.value] = { "value": 0xffff, "line": self.line }
            return self.labels[token.value]["value"]
        return None
    def term(self):
        result = self.factor()
        while self.current_token.token_type in (MUL, DIV):
            if self.current_token.token_type == MUL:
                self.skip(MUL)
                result *= self.factor()
            else:
                self.skip(DIV)
                result /= self.factor()
        return result
    def expression(self):
        
        result = self.term()
        while self.current_token.token_type in (PLUS, MINUS):
            if self.current_token.token_type == PLUS:
                self.skip(PLUS)
                result += self.term()
            else:
                self.skip(MINUS)
                result -= self.term()
        return result
    def set_label(self, label, arg):
        if label not in self.labels:
            self.labels[label] = { "value": 0xffff, "line": self.line }
        self.labels[label]["value"] = arg
    def dump_labels(self):
        for label in self.labels:
            if self.labels[label]["line"] != -1:
                print(f"{label:16}=${self.labels[label]['value']:04x} ({self.labels[label]['value']})")
    def compile(self):
        while self.current_token.token_type != EOF:
            token = self.current_token
            if token.line != self.line:
                print(self.line,token)
            if token.token_type == NEWLINE:
                self.skip(NEWLINE)
                continue
            if token.token_type == COLON:
                self.skip(COLON)
                continue
            if token.token_type == LABEL:
                self.skip(LABEL)
                if self.current_token.token_type == ASSIGN:
                    self.skip(ASSIGN)
                    self.set_label(token.value, self.expression())
                else:
                    self.set_label(token.value, self.pc)
                continue
            if token.token_type == ORG:
                self.skip(ORG)
                self.pc = self.expression()
                continue
            # if token.token_type == LET:
            #     self.skip(LET)
            #     label = self.current_token
            #     self.skip(LABEL)
            #     self.skip(ASSIGN)
            #     arg = self.expression()
            #     self.set_label(label.value, arg)
            #     continue
            self.skip(OPCODE)
            if self.current_token.token_type in (COLON, NEWLINE, EOF): #akku/implied
                self.asm_command(token, IMPLIED, None)
                continue

            if self.current_token.token_type == HASH: # token is immediate
                self.skip(HASH)
                arg = self.expression()
                if arg > 255:
                    raise Exception("Illegal quantity (#)")
                self.asm_command(token, IMMEDIATE, arg)
                continue

            if self.current_token.token_type == LPAREN: # ()
                self.skip(LPAREN)
                arg = self.expression()
                if self.current_token.token_type == COMMAX: # ,x)
                    self.skip(COMMAX)
                    self.skip(RPAREN)
                    if arg > 255:
                        raise Exception("Illegal quantity (must be 0..255)")
                    self.asm_command(token, USELESS, arg)
                elif self.current_token.token_type == RPAREN: # )
                    self.skip(RPAREN)
                    if self.current_token.token_type == COMMAY: # ),y
                        self.skip(COMMAY)
                        if arg > 255:
                            raise Exception("Illegal quantity (must be 0..255)")
                        self.asm_command(token, INDIRECTY, arg)
                    else: # indirect )
                        self.asm_command(token, INDIRECT, arg)
                continue
            #abs/zp (,x,y)
            arg = self.expression()

            # zp,x/abs,x
            if self.current_token.token_type == COMMAX:
                self.skip(COMMAX)
                if arg <= 255:
                    self.asm_command(token, ZPX, arg)
                else:
                    self.asm_command(token, ABSOLUTEX, arg)
                continue
            # zp,y/abs,y
            if self.current_token.token_type == COMMAY:
                self.skip(COMMAY)
                if arg <= 255:
                    self.asm_command(token, ZPY, arg)
                else:
                    self.asm_command(token, ABSOLUTEY, arg)
                continue
            # zp/abs
            if arg <= 255:
                self.asm_command(token, ZP, arg)
            elif RELATIVE in OPCODES[token.value]:
                self.asm_command(token, RELATIVE, arg)
            else:
                self.asm_command(token, ABSOLUTE, arg)
    def asm_command(self, token, mode, arg):
        if mode not in OPCODES[token.value.lower()]:
            raise Exception("Unknown addressing mode")
        if arg is not None:
            arg_low = arg % 256
            arg_high = arg // 256
            arg_relative = 0

            if arg <= self.pc:
                arg_relative = 254 - (self.pc - arg) 
            else:
                arg_relative = arg - self.pc - 2
        if self.run == 2:
            if mode == IMMEDIATE:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg:02x}    {token.value} #${arg:02x}")
            elif mode == ZP:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg:02x}    {token.value} ${arg:02x}")
            elif mode == ZPX:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg:02x}    {token.value} ${arg:02x},x")
            elif mode == ZPY:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg:02x}    {token.value} ${arg:02x},y")
            elif mode == USELESS:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg:02x}    {token.value} (${arg:02x},x)")
            elif mode == INDIRECTY:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg:02x}    {token.value} (${arg:02x}),y")
                
            elif mode == ABSOLUTE:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} ${arg:04x}")
            elif mode == ABSOLUTEX:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} ${arg:04x},x")
            elif mode == ABSOLUTEY:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} ${arg:04x},y")
            elif mode == INDIRECT:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} (${arg:04x})")
            elif mode == RELATIVE:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_relative:02x}    {token.value} ${arg:04x}")
            elif mode == IMPLIED:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x}       {token.value}")
        self.pc += 1
        if mode > IMPLIED:
            self.pc += 1
        if mode >= ABSOLUTE:
            self.pc += 1

labels = {
    # line = -1 -> defined here; ignored by ".show_labels()"
    # Kernal addresses for all C= computers
    "basout": { "value": 0xffd2, "line": -1 }, "plot": { "value": 0xfff0, "line": -1 },
    "open": { "value": 0xffc0, "line": -1 }, "close": { "value": 0xffc3, "line": -1 }, "setlfs": { "value": 0xffba, "line": -1 }, "setnam": { "value": 0xffbd, "line": -1 },
    "load": { "value": 0xffd5, "line": -1 }, "save": { "value": 0xffd8, "line": -1 },
    # BASIC adr for C64
    "strout": { "value": 0xab1e, "line": -1 }, "chkkom": { "value": 0xaefd, "line": -1 }, "frmevl":{ "value": 0xe257, "line": -1 },
    "frmnum": { "value": 0xad8a, "line": -1 }, "getadr": { "value": 0xb7f7, "line": -1 }
}

# source = "org 49152:lda # %101 +5:sta 123:ldx#<test:ldy#>test:jsr test\norg $c00a+ 1:test ldx #0\nrts"

file = open("test.asm")
source = file.read()
file.close()
lexer = Lexer(source)
# print(lexer.get_tokens())

ex = Assembler(lexer, labels)

ex.assemble()
ex.dump_labels()