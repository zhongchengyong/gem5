/*
 * Minimal startup code for RISC-V bare-metal programs
 */

.section .text.init
.global _start

_start:
    /* Set up stack pointer */
    la sp, _stack_top

    /* Clear BSS section */
    la a0, _bss_start
    la a1, _bss_end
clear_bss:
    beq a0, a1, done_bss
    sd zero, 0(a0)
    addi a0, a0, 8
    j clear_bss
done_bss:

    /* Call main */
    call main

    /* Exit with return value */
    mv a0, a0
    li a7, 93        /* syscall number for exit */
    ecall

    /* Infinite loop */
halt:
    j halt
