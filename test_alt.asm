         bla=2
;test
 Abcdef= 5
 test      =         1234
irqvec = $314
    adresse =$fff0
    org $c000
    SEi
    lda #<irq:STA irqvec
    lda #>irq : sta irqvec + 1
    lda #     147:    jsr basout
clI
    rts
irq:jmp $ea31
    lda #%11111110
    ldx #254
    ldy #$fe
    tay
    sta $0400
    sta 100,x
    lda Abcdef
    lda Abcdef,x
    lda (Abcdef),y
    nop:ldx Abcdef,y
x=500
back
unused_label
y=600:asl:ldx #%111*7:stx y
    nop
    bne back
    beq next
    lda (100),y
    sta (2,x);useless
next:
    lda test,x
    stx 101,y
    jmp (test_ende)
    jmp ($308)
    jsr adresse
    jmp 100
    lda $1000 + %11*  $10f  ,X ;!
    sta 45054,y;hihi
    jsr label
    jmp again
    brk
;    xyz
    brk: brk   :nop: nop
    test_ende:;byt %101100

    ;testcomment
;testcomment
 ;.ba $c068;testcomment
again:;testcomment
 lda $01fc,y;testcomment
sta ($5f),y;testcomment
 dey;testcomment
 bpl again;testcomment
 brk;testcomment
;testcomment
z= $700 | 3
org $1000
lda #0
    sta bla
    byte 8,bla, 0, $ff,>irq,<Abcdef
    .by $0a,$b, $a + 2
    fill 5, 0
    fill 1, 255
    word 0,1,irq, z, again
byt 255
    rts

    org z; ORG with label
label nop:ldx#%11:brk
    lda #0
    sta $d020
    rts