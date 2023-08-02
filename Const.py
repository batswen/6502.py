IMPLIED=0 # 1 Byte (implied and akku)
RELATIVE=1; ZP=2; ZPX=3; ZPY=4; USELESS=5; INDIRECTY=6; IMMEDIATE=7 # 2 Byte
ABSOLUTE=10; ABSOLUTEX=11; ABSOLUTEY=12; INDIRECT=13 # 3 Byte

EOF="EOF"
LET="LET"
NUMBER = "Number"
PLUS ="Plus";MINUS="Minus";MUL="Mul";DIV="Div";LPAREN="LParen";RPAREN="RParen"
LT="<";GT=">";AND="&";OR="|";EOR="^"
HASH="#";
COMMA=",";COMMAX=",x";COMMAY=",y"
COLON=":";NEWLINE="Newline"
ASSIGN="Assign"
ORG="Org"
FILL="Fill"
BYTE="Byte";WORD="Word";TEXT="Text"
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

if __name__ == "__main__":
    pass