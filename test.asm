a = 147
irqvec = $314
    org $c000
    SEi
    lda #<irq:STA irqvec
    lda #>irq : sta irqvec + 1
    ;lda #     a:    jsr basout
clI
    bcc ende
    inx
    ende
    rts
irq jmp $ea31
