ENTRY(_start)

SECTIONS
{
  . = 0x00000000;

  .text : {
    KEEP(*(.text._start))
    *(.text*)
    *(.rodata*)
  }

  . = ALIGN(4);
  .data : { *(.data*) }

  . = ALIGN(4);
  .bss (NOLOAD) : { *(.bss*) *(COMMON) }

  /DISCARD/ : { *(.comment*) *(.note*) }
}
