#ifndef LCD_HPP
#define LCD_HPP

#include "led.hpp"
#include "system.hpp"

/**
 * @brief Abstraction over LCD.
 *
 * https://fr.wikipedia.org/wiki/HD44780
 */
class LCD
{
public:
    LCD()
    {
        init8bitMode();
    }

    /**
     * Clear the LCD.
     */
    void clear()
    {
        writeCommand(0b00000001);
        Delay::millis(2); // the command takes at least 1.52 ms to execute
    }

    /**
     * Return cursor to home position.
     * Also return display being shifted to the original position.
     * DDRAM content remains unchanged.
     */
    void home()
    {
        writeCommand(0b00000010);
        Delay::millis(2); // the command takes at least 1.52 ms to execute
    }

    /**
     * Turn off the LCD.
     */
    void off()
    {
        writeCommand(0b00001000);
    }

    /**
     * Turn on the LCD.
     */
    void on()
    {
        writeCommand(0b00001100);
    }

    /**
     * Set (DDRAM) address.
     * @param address the address (should be >= 127)
     */
    void setAddress(uint8_t address)
    {
        // Addresses are 7-bit long so we have to mask it to clear 8th bit
        writeCommand(0b10000000 | (address & 0x7F));
    }

    /**
     * Print two lines of text.
     *
     * The display is cleared first.
     *
     * @param line1
     * @param line2
     */
    void print(const char* line1, const char* line2)
    {
        clear();

        // Line 1
        setAddress(0);
        while (*line1 != 0)
        {
            writeData(*line1);
            ++line1;
        }

        // Line 2
        setAddress(40);
        while (*line2 != 0)
        {
            writeData(*line2);
            ++line2;
        }
    }

    //------------------------------------------------------------
    // Mid-level functions
    void writeCommand(uint8_t value)
    {
        setRegisterSelect(RegisterSelect::Command);
        write(value);
        pulseEnable();

        Delay::micros(50); // all commands takes at least 37 µs to execute
    }

    void writeData(uint8_t value)
    {
        setRegisterSelect(RegisterSelect::Data);
        write(value);
        pulseEnable();

        Delay::micros(50); // write to RAM takes at least 37 µs to execute
    }

private:
    enum RegisterSelect
    {
        Command = 0, Data = 1
    };

    void setRegisterSelect(RegisterSelect selection)
    {
        switch (selection)
        {
        case Command:

            LED::Red.off();
            break;
        case Data:
            LED::Red.on();
            break;
        default:
            break;
        }

        // FIXME LED1 = RED LED = P1.0 is used as control signal because there are two few availabe GPIOs

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

    void write(uint8_t value)
    {

        P1OUT &= ~(1 << 4);
        P1OUT &= ~(1 << 5);
        P1OUT |= ((value & 0xC0) >> 6) << 4;

        P2OUT = value & 0x3F;
    }

    void init8bitMode()
    {
        // Control signals
        P1DIR |= BIT7; // = Enable
        // Note RW/S is not used

        // Data signals
        P1DIR |= BIT4 | BIT5;
        P2DIR |= BIT0 | BIT1 | BIT2 | BIT3 | BIT4 | BIT5;

        // Initialize LCD
        // 1 - Wait > 40 ms after Vdd > 2.7 V
        Delay::millis(50);

        // 2 - Function set
        writeCommand(0b00110000);

        // 3 - Wait time > 4.1 ms
        Delay::millis(15);

        // 3 - Function set
        writeCommand(0b00110000);

        // 4 - Wait time > 100 us
        Delay::millis(1);

        // 5 - Function set
        writeCommand(0b00110000);

        // 6 - Number of lines and character font (2 lines, 5x8 dots format)
        writeCommand(0b00111000);

        // 7 - Display off
        writeCommand(0b00001000);

        // 8 - Display clear
        writeCommand(0b00000001);

        // 9 - Entry mode set
        writeCommand(0b00000110);
        // TODO comprendre pour mettre S à 0 fait presque tout marcher
    }
};

#endif
