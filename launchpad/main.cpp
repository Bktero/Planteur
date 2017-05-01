#include <msp430.h>

// TODO read https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/

#include "led.hpp"
#include "system.hpp"

#include "lcd.hpp"

typedef std::array<int, 5> array_int_5;

int getHumidity()
{
    static array_int_5 humidities = { 80, 75, 65, 52, 45 };
    static std::size_t index = 0;

    if (index < humidities.size())
    {
        ++index;
    }
    else
    {
        index = 0;
    }

    return humidities[index];
}

int getTemperature()
{
    static array_int_5 temperatures = { 15, 18, 20, 21, 19 };
    static std::size_t index = 0;

    if (index < temperatures.size())
    {
        ++index;
    }
    else
    {
        index = 0;
    }

    return temperatures[index];
}

typedef volatile uint8_t device_register;

class GPIO
{
public:
    device_register _IN;
    device_register _OUT;
    device_register _DIR;
};

volatile GPIO& Port1 = *reinterpret_cast<volatile GPIO*>(&P1IN);
volatile GPIO& Port2 = *reinterpret_cast<volatile GPIO*>(&P2IN);

class LCDLowLevelImpl
{
public:
    using LCDMode = LCD<LCDLowLevelImpl>::Mode;
    static const LCDMode mode = LCDMode::MODE_8BITS;

    static void init()
    {
        // Control signals
        // Enable
        Port1._DIR |= BIT7;

        // Register selection
        // FIXME Red LED is used

        // RW/S is not used

        // Data signals
        // PB0-5
        Port2._DIR |= BIT0 | BIT1 | BIT2 | BIT3 | BIT4 | BIT5;
        // PB6-7
        Port1._DIR |= BIT4 | BIT5;
    }

    static void enableLow()
    {
        Port1._OUT &= ~BIT7;
    }

    static void enableHigh()
    {
        Port1._OUT |= BIT7;
    }

    static void registerSelectLow()
    {
        LED::Red.off();
    }

    static void registerSelectHigh()
    {
        LED::Red.on();
    }

    static void write(uint8_t value)
    {
        // Write port direclty because PORT2 is only used for LCD
        Port2._OUT = value & 0x3F;

        // Clear bits and send apply new values because PORT1 is not dedicated to LCD
        Port1._OUT &= ~(1 << 4);
        Port1._OUT &= ~(1 << 5);
        Port1._OUT |= ((value & 0xC0) >> 6) << 4;
    }
};

/**
 * Main program.
 */
int main(void)
{
    Launchpad::init();

    using LCD = LCD<LCDLowLevelImpl>;
    LCD lcd;
    lcd.on();

    lcd.print("launchpad", "     & planteur");
    Delay::millis(1000);

    while (1)
    {
        Delay::millis(1000);
        LED::Green.toogle();

        lcd.clear();

        lcd.setCursorPosition(0, 0);
        lcd << "Humidity " << getHumidity();

        lcd.setCursorPosition(1, 0);
        lcd << "Temperature " << getTemperature();
    }
}
