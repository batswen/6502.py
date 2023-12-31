from Const import *

from Token import Token
from Lexer import Lexer

class Assembler:
    def __init__(self, lexer, labels):
        self.lexer = lexer
        self.labels = labels
        self.pc = 0
        self.current_token = self.lexer.next_token()
        self.line = self.current_token.line
        self.run = 1
        self.memory = bytearray(65536)
        self.min_memory = 65536
        self.max_memory = -1
        self.verbose = False

    def get_memory(self):
        return {
            "start": self.min_memory,
            "end": self.max_memory,
            "memory": self.memory
        }

    def poke(self, address, content):
        if address < self.min_memory:
            self.min_memory = address
        if address > self.max_memory:
            self.max_memory = address
        self.memory[address] = content

    def poke_word(self, address, content):
        if address < self.min_memory:
            self.min_memory = address
        if address + 1> self.max_memory:
            self.max_memory = address
        self.memory[address] = content % 256
        self.memory[address + 1] = content // 256

    def assemble(self, verbose):
        self.verbose = verbose
        # try:
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

        print(f"Code: ${self.min_memory:04x} - ${self.max_memory:04x}")

        # except Exception as e:
        # print(f"{e} in {self.line}")

    def skip(self, token_type):
        if self.current_token.test(token_type):
            self.current_token = self.lexer.next_token()
            self.line = self.current_token.line
        else:
            raise Exception(f"Syntax (Expected: {token_type}, got: {self.current_token.token_type})")

    def add_refs_to_label(self, label):
        if "refs" in self.labels[label] and self.line not in self.labels[label]["refs"]:
            self.labels[label]["refs"].append(self.line)

    def factor(self):
        # print("factor",self.current_token)
        if self.current_token.test(LPAREN): #this could be a problem
            self.skip(LPAREN)
            result = self.expression()
            self.skip(RPAREN)
            return result
        if self.current_token.test(NUMBER): #hex/dec/bin
            token = self.current_token
            self.skip(NUMBER)
            return token.value
        if self.current_token.test(LT): # <expr
            self.skip(LT)
            return self.expression() % 256
        if self.current_token.test(GT): # >expr
            self.skip(GT)
            return self.expression() // 256
        if self.current_token.test(LABEL):
            token = self.current_token
            self.skip(LABEL)
            if token.value not in self.labels:
                self.labels[token.value] = { "value": 0xffff, "line": self.line, "refs": [] }
            self.add_refs_to_label(token.value)
            if self.run == 2 and self.labels[token.value]["value"] == 0xffff:
                raise Exception(f'Label "{token.value}" is not defined')
                pass
            return self.labels[token.value]["value"]
        return None

    def term(self):
        result = self.factor()
        while self.current_token.token_type in (MUL, DIV):
            if self.current_token.test(MUL):
                self.skip(MUL)
                result *= self.factor()
            else:
                self.skip(DIV)
                result /= self.factor()
        return result

    def pm_expr(self):
        result = self.term()
        while self.current_token.token_type in (PLUS, MINUS):
            if self.current_token.test(PLUS):
                self.skip(PLUS)
                result += self.term()
            else:
                self.skip(MINUS)
                result -= self.term()
        return result
    def and_expr(self):
        result = self.pm_expr()
        while self.current_token.token_type == AND:
            self.skip(AND)
            result &= self.pm_expr()
        return result
    def eor_expr(self):
        result = self.and_expr()
        while self.current_token.token_type == EOR:
            self.skip(EOR)
            result ^= self.and_expr()
        return result
    def expression(self):
        result = self.eor_expr()
        while self.current_token.token_type == OR:
            self.skip(OR)
            result |= self.eor_expr()
        return result

    def set_label(self, label, arg):
        if label not in self.labels:
            self.labels[label] = { "value": 0xffff, "line": self.line, "refs": [] }
        self.add_refs_to_label(label)
        self.labels[label]["value"] = arg

    def dump_labels(self):
        for label in self.labels:
            if self.labels[label]["line"] != -1:
                print(f"{self.labels[label]['line']:05} {label:16}=${self.labels[label]['value']:04x} ({self.labels[label]['value']:5}) {self.labels[label]['refs']}")

    def compile(self):
        while self.current_token.token_type != EOF:
            token = self.current_token
            if token.line != self.line:
                print(self.line,token)
            if token.test(NEWLINE):
                self.skip(NEWLINE)
                continue
            if token.test(COLON):
                self.skip(COLON)
                continue
            if token.test(FILL):
                self.skip(FILL)
                fill_amount = self.expression()
                if fill_amount > 255 or fill_amount == 0:
                    raise Exception("Illegal quantity")
                self.skip(COMMA)
                fill_byte = self.expression()
                if fill_byte > 255:
                    raise Exception("Illegal quantity")
                fill_pc = self.pc
                if self.run == 2:
                    for i in range(fill_amount):
                        self.poke(self.pc, fill_byte)
                        self.pc += 1
                    if self.verbose:
                        if fill_amount == 1:
                            print(f"{token.line:05} {fill_pc:04x}          fill ${fill_amount:02x}, ${fill_byte:02x}")
                        else:
                            print(f"{token.line:05} {fill_pc:04x}-{fill_pc + fill_amount - 1:04x}     fill ${fill_amount:02x}, ${fill_byte:02x}")
                continue
            if token.test(BYTE):
                byte_line = token.line
                byte_pc = self.pc
                byte_data = []
                self.skip(BYTE)
                while self.current_token.token_type in (LABEL, NUMBER, GT, LT):
                    value = self.expression()
                    if value > 256:
                        raise Exception("Illegal quantity")
                    if self.run == 2:
                        self.poke(self.pc, value)
                        byte_data.append(value)
                    self.pc += 1
                    if not self.current_token.test(COMMA):
                        if self.run == 2 and self.verbose:
                            if byte_pc == self.pc - 1:
                                print(f"{byte_line:05} {byte_pc:04x}          byte ${byte_data[0]:02x}", end="")
                            else:
                                print(f"{byte_line:05} {byte_pc:04x}-{self.pc - 1:04x}     byte ${byte_data[0]:02x}", end="")
                            for data in byte_data[1:]:
                                print(f", ${data:02x}",end="")
                            print()
                        break
                    self.skip(COMMA)
                continue
            if token.test(WORD):
                word_line = token.line
                word_pc = self.pc
                word_data = []
                self.skip(WORD)
                while self.current_token.token_type in (LABEL, NUMBER, GT, LT):
                    value = self.expression()
                    if self.run == 2:
                        self.poke_word(self.pc, value)
                        word_data.append(value)
                    self.pc += 2
                    if not self.current_token.test(COMMA):
                        if self.run == 2 and self.verbose:
                            print(f"{word_line:05} {word_pc:04x}-{self.pc - 1:04x}     word ${word_data[0]:04x}", end="")
                            for data in word_data[1:]:
                                print(f", ${data:04x}",end="")
                            print()
                        break
                    self.skip(COMMA)
                continue
            if token.test(TEXT):
                self.skip(TEXT)
                print(f'text "{self.current_token.value}" - NOT IMPLEMENTED')
                self.skip(STRING)
                continue
            if token.test(LABEL):
                self.skip(LABEL)
                if self.current_token.test(ASSIGN):
                    self.skip(ASSIGN)
                    self.set_label(token.value, self.expression())
                else:
                    self.set_label(token.value, self.pc)
                    if self.run == 2: # fix forward refs
                        self.labels[token.value]["line"] = self.line
                self.add_refs_to_label(token.value)
                continue
            if token.test(ORG):
                self.skip(ORG)
                self.pc = self.expression()
                continue
            # if token.test(LET:
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

            if self.current_token.test(HASH): # token is immediate
                self.skip(HASH)
                arg = self.expression()
                if arg > 255:
                    raise Exception("Illegal quantity (#)")
                self.asm_command(token, IMMEDIATE, arg)
                continue

            if self.current_token.test(LPAREN): # ()
                self.skip(LPAREN)
                arg = self.expression()
                if self.current_token.test(COMMA): # ,x)
                    self.skip(COMMA)
                    if self.current_token.value.lower() != "x":
                        raise Exception("Syntax (X expected)")
                    self.skip(LABEL)
                    self.skip(RPAREN)
                    if arg > 255:
                        raise Exception("Illegal quantity (must be 0..255)")
                    self.asm_command(token, USELESS, arg)
                elif self.current_token.test(RPAREN): # )
                    self.skip(RPAREN)
                    if self.current_token.test(COMMA): # ),y
                        self.skip(COMMA)
                        if self.current_token.value.lower() != "y":
                            raise Exception("Syntax (Y expected)")
                        self.skip(LABEL)
                        if arg > 255:
                            raise Exception("Illegal quantity (must be 0..255)")
                        self.asm_command(token, INDIRECTY, arg)
                    else: # indirect )
                        self.asm_command(token, INDIRECT, arg)
                continue
            #abs/zp (,x,y)
            arg = self.expression()

            # zp,x/abs,x
            if self.current_token.test(COMMA):
                self.skip(COMMA)
                if self.current_token.value.lower() in ("x", "y"):
                    if self.current_token.value.lower() == "x":
                        self.skip(LABEL)
                        if arg <= 255 and ZP in OPCODES[token.value]:
                            self.asm_command(token, ZPX, arg)
                        else:
                            self.asm_command(token, ABSOLUTEX, arg)
                        continue
                    elif self.current_token.value.lower() == "y":
                # zp,y/abs,y
                        self.skip(LABEL)
                        if arg <= 255 and ZP in OPCODES[token.value]:
                            self.asm_command(token, ZPY, arg)
                        else:
                            self.asm_command(token, ABSOLUTEY, arg)
                        continue
                    else:
                        raise Exception("Syntax (X or Y expected)")
            # zp/abs
            if arg <= 255 and ZP in OPCODES[token.value]:
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
            if mode == RELATIVE:
                arg_low = arg - self.pc - 2
                if arg <= self.pc:
                    arg_low = 254 - (self.pc - arg)

        if self.run == 2 and self.verbose:
            if mode == IMPLIED:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x}       {token.value}")
            # zero page
            elif mode == IMMEDIATE:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} #${arg:02x}    ;{arg}")
            elif mode == ZP:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} ${arg:02x}     ;{arg}")
            elif mode == ZPX:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} ${arg:02x},x   ;{arg}")
            elif mode == ZPY:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} ${arg:02x},y   ;{arg}")
            elif mode == USELESS:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} (${arg:02x},x) ;{arg}")
            elif mode == INDIRECTY:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} (${arg:02x}),y ;{arg}")
            # relative
            elif mode == RELATIVE:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x}    {token.value} ${arg:04x}   ;{arg}")
            # absolute
            elif mode == ABSOLUTE:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} ${arg:04x}   ;{arg}")
            elif mode == ABSOLUTEX:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} ${arg:04x},x ;{arg}")
            elif mode == ABSOLUTEY:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} ${arg:04x},y ;{arg}")
            elif mode == INDIRECT:
                print(f"{self.line:05} {self.pc:04x} {OPCODES[token.value][mode]:02x} {arg_low:02x} {arg_high:02x} {token.value} (${arg:04x}) ;{arg}")
        if self.run == 2:
            self.poke(self.pc, OPCODES[token.value][mode])
        self.pc += 1
        if mode > IMPLIED:
            if self.run == 2:
                self.poke(self.pc,arg_low)
            self.pc += 1
        if mode >= ABSOLUTE:
            if self.run == 2:
                self.poke(self.pc,arg_high)
            self.pc += 1

if __name__ == "__main__":
    pass