#ifndef UART_HPP
#define UART_HPP

#include <msp430.h>
#include <cstddef>
#include <cstdint>

/**
 * Abstraction over hardware UART module.
 */
class UART
{
public:
    static UART Uart0; // USCIA0 module

    /**
     * Enumeration of the supported baudrates.
     */
    enum Baudrate
    {
        /**
         * 9600 bauds.
         */
        BR_9600,
        /**
         * 19 200 bauds.
         */
        BR_19200,
        /**
         * 38 400 bauds.
         */
        BR_38400,
        /**
         * 57 600 bauds.
         */
        BR_57600,
        /**
         * 115 200 bauds.
         */
        BR_115200
    };

    /**
     * Receive one byte.
     *
     * This is a blocking function.
     *
     * @return a received byte
     */
    uint8_t receive();

    /**
     * Send one byte.
     *
     * This is a blocking function.
     *
     * @param data the byte to send
     */
    void send(const uint8_t data);

    /**
     * Send a C-string.
     *
     * This is a blocking function.
     *
     * @param message the string to send
     */
    void send(const char* message);

    /**
     * Send bytes.
     *
     * This is a blocking function.
     *
     * @param data a pointer to the first byte
     * @param length the number of bytes to send
     */
    void send(const uint8_t* data, size_t length);

    /**
     * Send a C-string.
     *
     * This is a non-blocking function.
     * See #sendAsync(const uint8_t*, size_t) for more details.
     *
     * @param message
     */
    void sendAsync(const char* message);

    /**
     * Send bytes.
     *
     * This is a non-blocking function. It will simply triggers the sending
     * of the first byte and enable the TX interrupt. Following bytes will
     * be send by the TX ISR.
     *
     * @param data a pointer to the first byte
     * @param length the number of bytes to send
     */
    void sendAsync(const uint8_t* data, size_t length);

    /**
     * Set the baudrate of this UART.
     *
     * @param baudrate the baudrate
     */
    void setBaudrate(Baudrate baudrate);

    friend void UART0_RX_ISR();
    friend void UART0_TX_ISR();

protected:
    void handleTxIsr();

private:
    enum
    {
        UART_TX_BIT = BIT2, UART_RX_BIT = BIT1
    };

    const uint8_t* data_m;
    size_t length_m;
    size_t count_m;
    bool sending_m;

    UART();
};

#endif
