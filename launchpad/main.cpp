#include <msp430.h>

#define     LED0                  BIT0
#define     LED1                  BIT6
#define     LED_DIR               P1DIR
#define     LED_OUT               P1OUT

void delay(unsigned int duration)
{
	for(volatile unsigned int i = 0 ; i < duration; i++)
	{
		nop();
	}
}

class Counter
{
public:
	Counter() :
		value_m(0)
	{
	}

	void count()
	{
		++value_m;
		if (value_m > MAX)
		{
			value_m = 0;
		}
	}

	unsigned int getValue() const
	{
		return value_m;
	}

private:
	static const unsigned int MAX = 0x4096;
	unsigned int value_m;
};

int main(void) {

	WDTCTL = WDTPW + WDTHOLD;

	LED_DIR |= LED0 + LED1;
	LED_OUT |= LED0 + LED1;

	Counter counter;

	while(1)
	{
		delay(counter.getValue());
		counter.count();
		LED_OUT ^= (LED0 + LED1);
	}
}


