CXX=msp430-gcc
CXXFLAGS=-Wall -Wextra -std=c++03 -mmcu=msp430g2231

OBJS=main.o
OUT=a.out

all: $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(OUT) $(OBJS)

%.o: %.c
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm $(OUT) $(OBJS)
