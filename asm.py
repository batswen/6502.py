import sys

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

outfile = "a.out"

# python asm.py infile.asm [outfile.bin]

if len(sys.argv) > 1:
    infile = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
else:
    print("Usage: asm.py infile.asm [outfile]")
    sys.exit(1)

file = open(infile)
source = file.read()
file.close()
lexer = Lexer(source)
# print(lexer.get_tokens())

ex = Assembler(lexer, labels)

ex.assemble(False)
mem = ex.get_memory()

file = open(outfile, "wb")

file.write(bytes([mem["start"] % 256, mem["start"] // 256]))
file.write(bytes(mem["memory"][mem["start"]:mem["end"]+1]))
# ex.dump_labels()

file.close()