#include <msp430.h>

#include "delay.hpp"
#include "led.hpp"
#include "uart.hpp"

#define	BUTTON_BIT		BIT3

// TODO read https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/

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

    unsigned int getValue() const
    {
        return value_m;
    }

private:
    enum
    {
        MAX = 500, MIN = 50
    };
    unsigned int value_m;
};

bool led_paused = true;

void __interrupt_vec(PORT1_VECTOR) Port_1(void)
{
    // Change mode
    led_paused = !led_paused;

    // Clear interrupt flag
    P1IFG &= ~BUTTON_BIT;

    // Send message through UART
    const uint8_t b = '0' + led_paused;
    UART::Uart0.send(b);
}

int main(void)
{
    // Stop watchdog timer
    WDTCTL = WDTPW + WDTHOLD;

    // Enable interrupt for button and clear flag
    P1IE |= BUTTON_BIT;
    P1IFG &= ~BUTTON_BIT;

    // Configure clock and UART
    // TODO verify this code taken from https://www.embeddedrelated.com/showarticle/420.php because TI's sample code do something else
    // Select lowest DCOx and MODx setting
    DCOCTL = 0;
    // Set DCO
    BCSCTL1 = CALBC1_1MHZ;
    DCOCTL = CALDCO_1MHZ;

    // Enable interrupts
    // The NOP avoids avoid a compiler's warning telling that a NOP might be needed before EINT
    __nop();
    __enable_interrupt();

    UART::Uart0.send("MSP430 starts");
    UART::Uart0.send('\n');

    // Infinite loop

    UART::Uart0.send("Send characters, the MSP430 will echo them\n");
    while (1)
    {
        uint8_t data = UART::Uart0.receive();

        if (data == 'z')
        {
            LED::Red.off();
        }
        else
        {
            LED::Red.on();
        }

        UART::Uart0.send("Received: ");
        UART::Uart0.send(data);
        UART::Uart0.send((uint8_t) '\n');
    }


//    UART::Uart0.sendAsync("Press the button so that the green LED toggles slowly\n");
//
//    while (1)
//    {
//        if (!led_paused)
//        {
//            Delay::millis(500);
//            LED::Green.toogle();
//        }
//    }

    while (1)
        ;
}

