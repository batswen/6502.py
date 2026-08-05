# 6502.py
An assembler and disassembler for the 6502 cpu written in python\
The output has a two byte (lo/hi) header for the c= load routine

## Assembler

Start: python asm.py file.src [outfile = "a.out"]

See example output below

## Disassembler

Start: python disasm.py filename|filename.json

The JSON file defines ranges of byte and word tables.\
Look into *.json (unfinished)

Saves filename + "_out.txt"

## Hexdump

Start: python hexdump.py filename

## Assembler

### Comments
Comments start with ;

### Opcodes
Case insensitive

### Pseudo opcodes
Case insensitive, except for strings

* org/base/.ba adr or label: set start address
* label = number: define label
* word expr{, expr}
* byte expr{, expr}
* fill amount, byte
* text "string"

### Labels
Case sensitive

Must start with a letter or underscore or dot (a-z_.), then (a-z0-9_.). Minimum length is 2 characters.

### Numbers
Numbers must be in range 0..65535 or 0..255 depending on the command.
Hex numbers must start with $, binary numbers with a %.

Use +,-,*,/ for addition, subtraction, multiplication and division; and, or, eor = &, |, ^

### Future plans
* Float (FLPT and MFLPT)
* Unicode to PETSCII conversion

# Example
```
Pass 1
Pass 2
00004 c000 78       sei
00005 c001 a9 15    lda #$15    ;21
00005 c003 8d 14 03 sta $0314   ;788
00006 c006 a9 c0    lda #$c0    ;192
00006 c008 8d 15 03 sta $0315   ;789
00007 c00b a9 93    lda #$93    ;147
00007 c00d 20 d2 ff jsr $ffd2   ;65490
00008 c010 58       cli
00009 c011 90 01    bcc $c014   ;49172
00010 c013 e8       inx
00012 c014 60       rts
00013 c015 4c 31 ea jmp $ea31   ;59953
00014 c018 a9 07    lda #$07    ;7
00015 c01a a2 27    ldx #$27    ;39
00016 c01c a0 f8    ldy #$f8    ;248
Code: $c000 - $c01d
00001 a               =$0093 (  147) [1, 7]
00002 irqvec          =$0314 (  788) [2, 5, 6]
00013 irq             =$c015 (49173) [5, 6, 13]
00011 ende            =$c014 (49172) [9, 11]
```
