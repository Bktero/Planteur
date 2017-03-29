#ifndef UART_HPP
#define UART_HPP

#include <msp430.h>
#include <stddef.h>
#include <stdint.h>

class UART
{
public:
    static UART Uart0; // USCIA0 module

    uint8_t receive();

    void send(const uint8_t data);
    void send(const char* message);
    void send(const uint8_t* data, size_t length);
    void sendAsync(const char* message);
    void sendAsync(const uint8_t* data, size_t length);

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
