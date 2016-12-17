#include <msp430.h>

#include <assert.h>
//#define assert(x) {if(!(x)) while(1);}

#include <stdint.h>

#define LED_RED_BIT		BIT0
#define LED_GREEN_BIT	BIT6
#define	BUTTON_BIT		BIT3

void delay_millis(unsigned long millis)
{
	while(millis > 0)
	{
		__delay_cycles(1e6 / 1000);
		--millis;
	}
	// TODO get clock frequency
}
	

class Counter
{
public:
	Counter() :
		value_m(MIN)
	{
	}

	void count()
	{
		value_m += MIN;

		if (value_m > MAX)
		{
			value_m = MIN;
		}
	}

	unsigned long getValue() const
	{
		return value_m;
	}

private:
	static const unsigned int MAX = 500;
	static const unsigned int MIN = 50;
	unsigned int value_m;
};

bool led_paused = true;

void __interrupt_vec(PORT1_VECTOR) Port_1(void)
{
	// Change mode
    led_paused = !led_paused;
    
    // Clear interrupt flag
    P1IFG &= ~BUTTON_BIT;
}

// https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/


int main(void)
{
	// Stop watchdog timer
	WDTCTL = WDTPW + WDTHOLD;

	// Set the GPIO as output
	P1DIR |= LED_RED_BIT + LED_GREEN_BIT;
	
	// Turn both leds on
	P1OUT |= LED_RED_BIT + LED_GREEN_BIT;
	
	// Enable interrupt for button and clear flag
	P1IE |= BUTTON_BIT;
	P1IFG &= ~BUTTON_BIT;
	
/*	
	// Start ADC and configure to use internal temperature sensor
	ADC10CTL0 |= ADC10ON;
	ADC10CTL1 |= INCH_10;
	
	// Enable convertion
	ADC10CTL0 |= ENC;
	
	// Get temperature
	ADC10CTL0 |= ADC10SC;

	while((ADC10CTL0 & ADC10IFG) != 0)
	{
		;
	}
	
	assert((ADC10CTL1 & ADC10BUSY) == 0);
	
	uint16_t voltage = ADC10MEM;
	
	// From section 22.2.8, figure 22.13:
	// Vtemp = 0.00355 * temp + 0.986;
	// <=> temp = (Vtemp - 0.986) / 0.00355
		
	// ADC10IE for interrupt
	
	uint16_t temperature = ((voltage * 27069L - 18169625L) >> 16);
*/

	ADC10CTL0=SREF_1 + REFON + ADC10ON + ADC10SHT_3 ; //1.5V ref,Ref on,64 clocks for sample
    ADC10CTL1=INCH_10+ ADC10DIV_3; //temp sensor is at 10 and clock/4
	
    __delay_cycles(1000);              //wait 4 ref to settle
    	
	int t=0;
    ADC10CTL0 |= ENC + ADC10SC;      //enable conversion and start conversion
    while(ADC10CTL1 & BUSY);         //wait..i am converting..pum..pum..
    t=ADC10MEM;                       //store val in t
    ADC10CTL0&=~ENC;  
    
    int temp = ((t * 27069L - 18169625L) >> 16);
	
	int temp_ti = ( ((t - 630) * 761) / 1024 );
	delay_millis(10);
	
	
	// Enable interrups 
	__enable_interrupt();

	Counter counter;

	while(1)
	{
		if(!led_paused)
		{
			delay_millis((const unsigned long) counter.getValue());
			P1OUT ^= (LED_RED_BIT + LED_GREEN_BIT);
			counter.count();
		}
	}
}



