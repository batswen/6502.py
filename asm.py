IMPLIED=0 # 1 Byte (implied and akku)
RELATIVE=1; ZP=2; ZPX=3; ZPY=4; USELESS=5; INDIRECTY=6; IMMEDIATE=7 # 2 Byte 
ABSOLUTE=10; ABSOLUTEX=11; ABSOLUTEY=12; INDIRECT=13 # 3 Byte

opcodes = {
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
class Assembler:
    def __init__(self, source):
        self.lines = source.split("\n")
        self.source_line = ""
        self.line = 0
        self.tokens = []
        self.memory = bytearray(65536)
        self.min_memory = 65536
        self.max_memory = -1
        self.labels = {
            # line_number = -1 -> defined here; ignored by ".show_labels()"
            # Kernal addresses for all C= computers
            "basout": { "value": 0xffd2, "line_number": -1 }, "plot": { "value": 0xfff0, "line_number": -1 },
            "open": { "value": 0xffc0, "line_number": -1 }, "close": { "value": 0xffc3, "line_number": -1 }, "setlfs": { "value": 0xffba, "line_number": -1 }, "setnam": { "value": 0xffbd, "line_number": -1 },
            "load": { "value": 0xffd5, "line_number": -1 }, "save": { "value": 0xffd8, "line_number": -1 },
            # BASIC adr for C64
            "strout": { "value": 0xab1e, "line_number": -1 }, "chkkom": { "value": 0xaefd, "line_number": -1 }, "frmevl":{ "value": 0xe257, "line_number": -1 },
            "frmnum": { "value": 0xad8a, "line_number": -1 }, "getadr": { "value": 0xb7f7, "line_number": -1 }
        }
    def new_label(self, value):
        return { "value": value, "line_number": self.line, "refs": [] }
    def number(self, arg):
        # print(f"number '{arg}'")
        if arg.startswith("<"):               #low byte
            return self.number(arg[1:]) % 256
        if arg.startswith(">"):               #high byte
            return self.number(arg[1:]) // 256
        if arg[0].isalpha():                  #label
            if arg not in self.labels: # forward ref
                self.labels[arg] = self.new_label(65535)
            if "refs" not in self.labels[arg]:
                self.labels[arg]["refs"] = []
            if self.line not in self.labels[arg]["refs"]:
                self.labels[arg]["refs"].append(self.line)
            return self.labels[arg]["value"]
        if arg.startswith("$"):               #$hex
            try:
                dec = int(arg[1:], 16)
            except:
                raise Exception(f"Not a hex number")
            if dec > 65535:
                raise Exception(f"Illegal quantity")
            return dec
        elif arg.startswith("%"):             #%bin
            try:
                dec = int(arg[1:], 2)
            except:
                raise Exception(f"Not a binary number")
            if dec > 65535:
                raise Exception(f"Illegal quantity")
            return dec
        else:                                 #dec
            try:
                dec = int(arg)
            except:
                raise Exception(f"Not a decimal number")
            if dec > 65535:
                raise Exception(f"Illegal quantity")
            return dec

    def expression(self, arg):
        return self.number(arg)

    def test_arg(self, arg):
        #print(f"test_arg '{arg}'")
        if arg == "":
            return [IMPLIED, 0]
        if arg.startswith("#"):
            value = self.expression(arg[1:])
            if value > 255:
                raise Exception(f"Immediate value error")
            return [IMMEDIATE, value]
        if arg.startswith("("):
            if arg.endswith(",x)"):
                return [USELESS, self.expression(arg[1:-3])]
            if arg.endswith("),y"):
                return [INDIRECTY, self.expression(arg[1:-3])]
            if arg.endswith(")"):
                return [INDIRECT, self.expression(arg[1:-1])]
        if arg.endswith(",x"):
            value = self.expression(arg[:-2])
            if value <= 255:
                return [ZPX, value]
            else:
                return [ABSOLUTEX, value]
        if arg.endswith(",y"):
            value = self.expression(arg[:-2])
            if value <= 255:
                return [ZPY, value]
            else:
                return [ABSOLUTEY, value]
        return [ABSOLUTE, self.expression(arg)] # ABS/ZP or REL

    def parse(self):
        lines = []
        line_number = 1
        for line in self.lines:
            if ";" in line:
                line = line.split(";")[0]
            while "\\" in line:
                lines.append({"line_number": line_number, "line": line.split("\\")[0].strip()})
                line = line.split("\\", 1)[1]
            if line != "":
                lines.append({"line_number": line_number, "line": line.strip()})
            line_number += 1
        for i, source_line in enumerate(lines):
            label = ""
            opcode = ""
            arg = ""
            line = source_line["line"]

            if ":" in line:
                label = line.split(":")[0].strip()
                line = line.split(":")[1]
            line = line.strip()
            if " " in line:
                opcode = line.split(" ")[0].lower()
                arg = line.split(" ", 1)[1]
            else:
                opcode = line.lower()
                arg = ""

            if label != "" or opcode != "":
                self.tokens.append({ "line_number": source_line["line_number"], "label": label, "opcode": opcode, "arg": arg, "source_line": line })
        # print(self.tokens)
    def assemble(self, verbose):
        try:
            self.parse()
            self.do(1, verbose)
            self.do(2, verbose)

            print(f"Code: ${self.min_memory:04x} - ${self.max_memory - 1:04x}")
        except Exception as arg:
            print(f"Error: '{arg}' in line: {self.line}: '{self.source_line}'")
    def do(self, run, verbose):
        pc = 0
        org = False
        for token in self.tokens:
            line_number = token["line_number"]
            self.line = line_number
            label = token["label"]
            opcode = token["opcode"]
            arg = token["arg"]
            self.source_line = token["source_line"]
            if label != "":
                if run == 1:
                    self.labels[label] = self.new_label(pc)

                if opcode == "":
                    continue
            if opcode in (".ba", "org", "let", ".by", "byt", "byte"):
                if opcode in ("org", ".ba"):
                    pc = self.expression(arg)
                    if run == 2:
                        self.poke(pc, 0) # to set min_memory and max_memory
                    org = True
                elif opcode == "let" and run == 1:
                    let_label, let_value = arg.split("=")
                    let_label = let_label.strip()
                    value = self.expression(let_value)
                    if org and value < 256:
                        raise Exception(f"ZP labels must be declared before org")
                    self.labels[let_label] = self.new_label(value)
                    
                elif opcode in (".by", "byt", "byte"):
                    if run == 2:
                        arg_bytes = arg.split(",")
                        index = 0
                        for arg_byte in arg_bytes:
                            byte = self.expression(arg_byte.strip())
                            if byte > 255:
                                raise Exception("Byte must be in range 0..255")
                            self.poke(pc + index, byte)
                            index += 1
                        if verbose:
                            self.dis(line_number, pc, opcode, 0, self.expression(arg_bytes[0]), 0, self.source_line)
                    pc += arg.count(",") + 1
                continue

            if opcode not in opcodes:
                raise Exception(f"Unkonwn opcode '{opcode}'")

            arg_type, parsed_arg = self.test_arg(arg)
            rel_dist = 0
            if arg_type == ABSOLUTE:
                if parsed_arg <= 255 and ZP in opcodes[opcode]:
                    arg_type = ZP
                elif RELATIVE in opcodes[opcode]:
                    arg_type = RELATIVE
                    if parsed_arg < pc:
                        rel_dist = 254 - (pc - parsed_arg)
                    else:
                        rel_dist = parsed_arg - pc
                    if run == 2 and rel_dist > 255 or rel_dist < 0:
                        raise Exception(f"Branch error")
            if not arg_type in opcodes[opcode]:
                raise Exception(f"Unkonwn addressing mode")
  
            if run == 2:
                self.poke(pc, opcodes[opcode][arg_type])
                if verbose:
                    self.dis(line_number, pc, opcode, arg_type, parsed_arg, rel_dist, self.source_line)
                
                #if arg_type == IMPLIED:
                #    pass
                if arg_type == RELATIVE:
                    self.poke(pc + 1, rel_dist)
                elif arg_type < ABSOLUTE:
                    self.poke(pc + 1, parsed_arg)
                else:
                    self.poke(pc + 1, parsed_arg % 256)
                    self.poke(pc + 2, parsed_arg // 256)

            if arg_type == IMPLIED:
                pc = pc + 1
            elif arg_type < ABSOLUTE:
                pc = pc + 2
            else:
                pc = pc + 3
        if run == 1:
            for label in self.labels:
                if self.labels[label]["value"] == 65535:
                    raise Exception(f"Unknwon label '{label}'")
        if not org:
            raise Exception("No base address")

    def dis(self, index, pc, opcode, arg_type, parsed_arg, rel_dist, line):
        if opcode == "byte":
            print(f"{index:05d}:{pc:04x} ...     :{line}")
            return
        print(f"{index:05d}:{pc:04x} {opcodes[opcode][arg_type]:02x} ", end = "")
        if arg_type == IMPLIED:
            print(f"     :{line}")
        elif arg_type > RELATIVE and arg_type < ABSOLUTE:
            print(f"{parsed_arg:02x}   :{line}")
        elif arg_type == RELATIVE:
            print(f"{rel_dist:02x}   :{line} (Branch target: ${parsed_arg:04x})")
        else:
            print(f"{parsed_arg % 256:02x} {parsed_arg // 256:02x}:{line}")

    def show_labels(self):
        for label in self.labels:
            if self.labels[label]["line_number"] > -1:
                print(f"{label:12s}: ${self.labels[label]['value']:04x} {self.labels[label]['refs']}")
    def show_unused_labels(self):
        for label in self.labels:
            if self.labels[label]["line_number"] > -1 and len(self.labels[label]["refs"]) == 0:
                print(f"{label:12s}: ${self.labels[label]['value']:04x}")

    def poke(self, adr, byte):
        "Writes a byte into 'memory' and updates self.min_memory and self.max_memory"
        if adr < self.min_memory:
            self.min_memory = adr
        if adr > self.max_memory:
            self.max_memory = adr
        if byte > 255:
            raise Exception("byte must be in 0..255")
        self.memory[adr] = byte

    def write_binary(self, filename):
        pass
    def write_hexdump(self):
        adr = self.min_memory
        # print(f"{adr % 256:02x}{adr // 256:02x}",end="")
        while adr < self.max_memory:
            print(f"{adr:04x}:", end="")
            for i in range(8):
                if adr + i >= self.max_memory:
                    continue
                print(f"{self.memory[adr + i]:02x} ", end="")
            adr += 8
            print()
    
if __name__ == "__main__":
    file = open("test.asm")
    asm = Assembler(file.read())
    file.close()
    asm.assemble(False) # Print compiled program
    # asm.show_labels() # Print labels
    print("\n\nUnused labels:")
    asm.show_unused_labels()
    # asm.write_hexdump()
