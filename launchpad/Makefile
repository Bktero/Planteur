CC=msp430-gcc
CFLAGS=-Wall -Wextra -std=c99 -mmcu=msp430g2231

OBJS=main.o
OUT=a.out


all: $(OBJS)
	$(CC) $(CFLAGS) -o $(OUT) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm $(OUT) $(OBJS)
