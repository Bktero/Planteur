#include <msp430.h>

// TODO read https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/

#include "led.hpp"
#include "system.hpp"

#include "lcd.hpp"

/**
 * Main program.
 */
int main(void)
{
    Launchpad::init();

    LCD lcd;
    lcd.on();

    lcd.print("hello, world", LCD::EMPTY_LINE);

    lcd.setCursorPosition(1, 5);
    lcd << -12345;

    while (1)
    {
        Delay::millis(500);
        LED::Green.toogle();
        Delay::millis(500);
    }
}
