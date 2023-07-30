;test
let Abcdef= 5
let test      =         1234
    let adresse =$fff0
    org $c000
    SEi
    lda #<irq ; IRQ
    STA $314
    lda #>irq
sta $315
    lda #147
    jsr basout
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
    ldx Abcdef,y
    let x=500
back:
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
    lda 10000,x
    sta 45054,y;hihi
    jmp again
    brk
;    xyz
    brk
    brk
    test_ende:brk

;testcomment
 org $c522;testcomment
again:;testcomment
 lda $01fc,y;testcomment
sta ($5f),y;testcomment
 dey;testcomment
 bpl again;testcomment
 brk;testcomment
;testcomment
let z= 700