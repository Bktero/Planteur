#ifndef LED_HPP
#define LED_HPP

#include <msp430.h>
#include <stdint.h>

/**
 * Abstraction over hardware LEDs.
 */
class LED
{
public:
    /**
     * The green LED on the Launchpad demo board.
     */
    static LED Green;

    /**
     * The red LED on the Launchpad demo board.
     */
    static LED Red;

    /**
     * Turn the LED off.
     */
    void off()
    {
        P1OUT &= ~mask_m;
    }

    /**
     * Turn the LED on.
     */
    void on()
    {
        P1OUT |= mask_m;
    }

    /**
     * Toogle the LED state.
     */
    void toogle()
    {
        P1OUT ^= mask_m;
    }

private:
    enum
    {
        LED_RED_BIT = BIT0, LED_GREEN_BIT = BIT6
    };

    LED(int mask) :
            mask_m(mask)
    {
        P1DIR |= mask;
        P1OUT &= ~mask;
    }

    uint16_t mask_m;
};

#endif
