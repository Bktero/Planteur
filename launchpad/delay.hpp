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

#endif
