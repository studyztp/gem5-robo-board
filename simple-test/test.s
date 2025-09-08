    .syntax unified
    .thumb
    .text
    .p2align 2
    .globl _start
    .type _start,%function
_start:
    // write(1, msg, len)
    movs    r0, #1          // fd = 1 (stdout)
    adr     r1, msg         // r1 = &msg (PC-relative)
    movs    r2, #36         // len
    movs    r7, #4          // __NR_write
    svc     #0

    // exit(0)
    movs    r0, #0
    movs    r7, #1          // __NR_exit
    svc     #0

    .p2align 2
msg:
    .asciz  "Hello, gem5 from Cortex-M4 (Thumb)!\n"
    