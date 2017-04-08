#include <msp430.h>

#include "xbee.hpp"

// TODO read https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/

void init_launchpad()
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

int main(void)
{
    init_launchpad();
    xbee();

    while (1)
        ;
}
