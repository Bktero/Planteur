#ifndef LED_HPP
#define LED_HPP

#include <msp430.h>
#include <stdint.h>

class LED
{
public:
    static LED Green;
    static LED Red;

    void off()
    {
        P1OUT &= ~mask_m;
    }

    void on()
    {
        P1OUT |= mask_m;
    }

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
