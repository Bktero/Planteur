#ifndef DELAY_HPP
#define DELAY_HPP

#include <msp430.h>

namespace Delay
{

inline void millis(unsigned long millis)
{
    while (millis > 0)
    {
        __delay_cycles(1e6 / 1000);
        --millis;
    }

    // TODO get clock frequency (here, assumed to be 1 MHz)
}

}

namespace Launchpad
{
inline void init()
{
    // Stop watchdog timer
    WDTCTL = WDTPW + WDTHOLD;

    // Configure clock to be 1 MHz
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
}

}

#endif
