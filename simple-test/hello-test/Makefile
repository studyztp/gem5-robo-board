CC=arm-none-eabi-gcc

all: hello_m4.elf

hello_m4.elf: hello_m4.s
	$(CC)  -mthumb -mcpu=cortex-m4 -static -nostdlib -o hello_m4.elf hello_m4.s

clean:
	rm -f hello_m4.elf
