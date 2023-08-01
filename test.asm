;test
let Abcdef= 5
let test      =         1234
    let adresse =$fff0
    org $c000
    SEi
    lda #<irq\STA $314
    lda #>irq \ sta $315
    lda #     147\    jsr basout
clI
    byte 96;rts
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
    nop\ldx Abcdef,y
    let x=500
back:
unused_label:
let y=600
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
    lda 10000,X
    sta 45054,y;hihi
    jmp again
    brk
;    xyz
    brk\ brk   \nop\ nop
    test_ende:byt %101100

    ;testcomment
;testcomment
 .ba $c068;testcomment
again:;testcomment
 lda $01fc,y;testcomment
sta ($5f),y;testcomment
 dey;testcomment
 bpl again;testcomment
 brk;testcomment
;testcomment
let z= 700
    byte 8,0, 0, $ff,>irq,<Abcdef
    .by 169
    byt 255
    rts