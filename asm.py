from Assembler import Assembler
from Lexer import Lexer

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

ex.assemble(True)
# ex.dump_labels()