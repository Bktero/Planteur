#ifndef LCD_HPP
#define LCD_HPP

#include <array>

#include "led.hpp"
#include "system.hpp"

/**
 * @brief Abstraction over LCD.
 *
 * https://fr.wikipedia.org/wiki/HD44780
 * http://www.farnell.com/datasheets/653654.pdf?_ga=1.80628375.1484903911.1492370013
 * https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
 */
class LCD
{
public:
    static const char * const EMPTY_LINE;

    enum ShiftDirection
    {
        LEFT = 0, RIGHT = 1 << 2
    };

    LCD()
    {
        init8bitInterfaceMode();
    }

    /**
     * Send a text to the LCD.
     *
     * @param text a text
     */
    LCD& operator<<(const char* text)
    {
        while (*text != 0)
        {
            writeData(*text);
            ++text;
        }

        return *this;
    }

    /**
     * Send an integer to the LCD.
     *
     * @param
     */
    LCD& operator<<(unsigned int value)
    {
        /*
         * uint16_t can store values between 0 and 65535 (= 2 << 16 - 1)
         * It means that there are at most 5 digits to extract from 'value'.
         */
        std::array < uint8_t, 5 > digits;

        for (int i = 0; i < 5; ++i)
        {
            digits[4 - i] = '0' + (value % 10);
            value /= 10;
        }

        for (std::size_t i = 0; i < digits.size() - 1; ++i)
        {
            if (digits[i] != '0')
                writeData (digits[i]);
        }

        writeData (digits[digits.size() - 1]); // always write the last digit (mandatory if value == 0)

        return *this;
    }

    LCD& operator<<(int value)
    {
        if (value < 0)
        {
            writeData('-');
            value = -value;
        }
        return *this << static_cast<unsigned int>(value);
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
     * Set cursor position.
     *
     * Further write (eg. with #writeData or operators <<)
     * will be done at this position.
     *
     * @param line
     * @param position
     */
    void setCursorPosition(int line, int position)
    {
        setAddress(line * 0x40 + position);
    }

    void shiftCursor(ShiftDirection direction)
    {
        writeCommand(0b00010000 | direction);
    }

    /**
     * Print two lines of text.
     *
     * The display is cleared first.
     * If you want to print an empty line, use #EMPTY_LINE.
     *
     * @param line1 the first line
     * @param line2 the second line
     */
    void print(const char* line1, const char* line2)
    {
        clear();

        // Line 1
        setCursorPosition(0, 0);
        *this << line1;

        // Line 2
        setCursorPosition(1, 0);
        *this << line2;
    }

    //------------------------------------------------------------
    // Mid-level functions
    /**
     * Set (DDRAM) address.
     * @param address the address (should be >= 80)
     */
    void setAddress(uint8_t address)
    {
        // Addresses are 7-bit long
        // But there is not need to mask the address because if the 8th bit is 1
        // the command we still be valid
        writeCommand(0b10000000 | address);
    }

    /**
     * Write a command to the LCD.
     *
     * @param command the command
     */
    void writeCommand(uint8_t command)
    {
        setRegisterSelect(RegisterSelect::Command);
        write(command);
        pulseEnable();

        Delay::micros(50); // all commands takes at least 37 µs to execute
    }

    /**
     * Write data the LCD (DDRAM) memory.
     *
     * @param data the data
     */
    void writeData(uint8_t data)
    {
        setRegisterSelect(RegisterSelect::Data);
        write(data);
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

    void init8bitInterfaceMode()
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
