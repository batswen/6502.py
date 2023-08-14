a = 147
irqvec = $314
    org $c000
    SEi
    lda #<irq:STA irqvec
    lda #>irq : sta irqvec + 1
    lda #     a:    jsr basout
clI
    bcc ende
    inx
    ende
    rts
irq jmp $ea31
    lda #255 & 7
    ldx #32 | 7
    ldy #255 ^ 7