#include <msp430.h>

#define     LED0                  BIT0
#define     LED1                  BIT6
#define     LED_DIR               P1DIR
#define     LED_OUT               P1OUT

void delay(void)
{
	for(volatile unsigned int i = 0 ; i < 0x4096; i++)
	{
		nop();
	}
}


int main(void) {

	WDTCTL = WDTPW + WDTHOLD;

	LED_DIR |= LED0 + LED1;
	LED_OUT |= LED0 + LED1;

	while(1)
	{
		delay();
		LED_OUT ^= (LED0 + LED1);
	}
}


