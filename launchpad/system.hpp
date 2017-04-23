/**
 * @file
 */
#ifndef DELAY_HPP
#define DELAY_HPP

#include <msp430.h>

/**
 * @namespace Delay functions to create delays
 */
namespace Delay
{
/**
 * Active wait.
 *
 * @param micros number of microseconds to wait
 */
inline void micros(unsigned long micros)
{
    while (micros > 0)
    {
        __delay_cycles(1);
        --micros;
    }

    // TODO get clock frequency (here, assumed to be 1 MHz)
}

/**
 * Active wait.
 *
 * @param millis number of milliseconds to wait
 */
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

/**
 * @namespace Launchpad functions for Launchpad board
 */
namespace Launchpad
{
/**
 * Initialize the Launchpad board.
 *
 *  - Stop watchdog timer
 *  - Set system clock to 1 MHz
 *  - Enable interrupts
 *
 * @warning calling this function should be the first line of your main program
 */
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
