#include <msp430.h>

// TODO read https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/

#include <cstdint>
#include "button.hpp"
#include "led.hpp"
#include "system.hpp"

#define PORT_1_MASK     (BIT4 | BIT5)
#define PORT_2_MASK     1

void allOn()
{
    P1OUT = BIT4 | BIT5;
    P2OUT = BIT0 | BIT1 | BIT2 | BIT3 | BIT4 | BIT5;
}

void allOff()
{
    P1OUT &= ~(BIT4 | BIT5);
    P2OUT &= ~(BIT0 | BIT1 | BIT2 | BIT3 | BIT4 | BIT5);
}

void initPin()
{
    // Control signals
    P1DIR |= BIT7;

    // Data signals
    P1DIR |= BIT4 | BIT5;
    P2DIR |= BIT0 | BIT1 | BIT2 | BIT3 | BIT4 | BIT5;

    allOff();
}

void write(uint8_t value)
{
// FIXME don't write entire ports

// TODO add P1
    P1OUT = ((value & 0xC0) >> 6) << 4;

    P2OUT = value & 0x3F;
}

void pulseEnable()
{
    P1OUT &= ~BIT7;
    Delay::micros(1);

    P1OUT |= BIT7;
    Delay::micros(1);

    P1OUT &= ~BIT7;
    Delay::micros(100);
}

void sendCommand(uint8_t value)
{

    write(value);
    LED::Red.off(); // FIXME before write() when write() will be fixed
    pulseEnable();

    Delay::millis(1);
}

void sendData(uint8_t value)
{

    write(value);
    LED::Red.on(); // FIXME before write() when write() will be fixed
    pulseEnable();

    Delay::millis(1);
}

//========================================

void message()
{
    // Text
    sendData('J');
    sendData('a');
    sendData('i');
    sendData('m');
    sendData('e');
    sendData(' ');
    sendData('b');
    sendData('i');
    sendData('e');
    sendData('n');
    sendData(' ');
    sendData('l');
    sendData('u');
    sendData('n');
    sendData('d');
    sendData('i');

    // Return home
    sendCommand(0b0000010);
    Delay::millis(3);

    //allOn();

    Delay::millis(2000);

    // Clear
    sendCommand(0b00000001);

    // Text
    sendData('u');
    sendData('a');
    sendData('n');
    sendData('d');
    sendData(' ');
    sendData('c');
    sendData(' ');
    sendData('f');
    sendData('e');
    sendData('r');
    sendData('i');
    sendData('e');
    sendData(' ');
    sendData('!');
    sendData('!');

    // Return home
    sendCommand(0b0000010);
    Delay::millis(3);
}
void print(const char* line1, const char* line2)
{
    // Line 1
    sendCommand(0b10000000);
    while (*line1 != 0)
    {
        sendData(*line1);
        ++line1;
    }

    // Line 2
    sendCommand(0b10000000 | 40);
    while (*line2 != 0)
    {
        sendData(*line2);
        ++line2;
    }
}

/**
 * Main program.
 */
int main(void)
{
    Launchpad::init();
    Button::unique.setCallback(message);

    initPin();

    // 1 - Wait > 40 ms after Vdd > 2.7 V
    Delay::millis(50);

    // 2 - Function set
    // RS    R/W    DB7    DB6   DB5    DB4    DB3    DB2    DB1    DB0
    // 0     0      0      0     1      1      X      X      X      X
    sendCommand(0b00110000);

    // 3 - Wait time > 4.1 ms
    Delay::millis(15);

    // 3 - Function set
    // Idem step 2
    sendCommand(0b00110000);

    // 4 - Wait time > 100 us
    Delay::millis(1);

    // 5 - Function set
    // Idem step 2
    sendCommand(0b00110000);

    // 6 - Number of lines and character font (function set too)
    // RS    R/W    DB7    DB6   DB5    DB4    DB3    DB2    DB1    DB0
    // 0     0      0      0     1      1      N      F      X      X
    // N = low --> 1-line display mode
    // F = Low --> 5x8 dots format display mode
    sendCommand(0b00111000);

    // 7 - Display off (instruction D)
    // RS    R/W    DB7    DB6   DB5    DB4    DB3    DB2    DB1    DB0
    // 0     0      0      0     0      0      1      0      0      0
    sendCommand(0b00001000);

    // 8 - Display clear (instruction A)
    // RS    R/W    DB7    DB6   DB5    DB4    DB3    DB2    DB1    DB0
    // 0     0      0      0     0      0      0      0      0      1
    sendCommand(0b00000001);

    // 9 - Entry mode set (instruction C)
    // RS    R/W    DB7    DB6   DB5    DB4    DB3    DB2    DB1    DB0
    // 0     0      0      0     0      0      0      1      I/D    S
    // I/D = ?
    // S = ?
    sendCommand(0b00000110); // TODO comprendre pour mettre S à 0 fait presque tout marcher

    //==============

    // Display on without cursor
    sendCommand(0b00001100);

    print("hello, world", "on TI launchpad");

    // =================================
    //allOn();

    while (1)
    {
        Delay::millis(500);
        LED::Green.toogle();
    }

    // http://www.farnell.com/datasheets/653654.pdf?_ga=1.80628375.1484903911.1492370013
    // https://fr.wikipedia.org/wiki/HD44780
}
