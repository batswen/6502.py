# 6502.py
An assembler and disassembler for the 6502 cpu written in python

## The Assembler

Start: python asm.py file.src

### comments
Comments start with ;

### opcodes
Case insensitive

### pseudo opcodes
Case insensitive, except for strings

* org/base/.ba adr or label: set start address
* label = number: define label
* word expr{, expr}
* byte expr{, expr}
* fill amount, byte
* text "string" - NOT IMPLEMENTED

### labels
Case sensitive

Must start with a letter or underscore or dot (a-z_.), then (a-z0-9_.). Minimum length is 2 characters.

### numbers
Numbers must be in range 0..65535 or 0..255 depending on the command.
Hex numbers must start with $, binary numbers with a %.

Use +,-,*,/ for addition, subtraction, multiplication and division; and, or, eor = &, |, ^

### Future plans
* Float (FLPT and MFLPT)
* Unicode to PETSCII conversion

## The Disassembler

Look into basic.json (unfinished)
