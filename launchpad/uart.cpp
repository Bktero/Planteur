#include "uart.hpp"

#include <string.h>

UART UART::Uart0;
#include "led.hpp" // FIXME remove
uint8_t UART::receive()
{
    while ((IFG2 & UCA0RXIFG) == 0)
        ;

    uint8_t data = UCA0RXBUF; // also clears the UCA0RXIFG flag
    return data;
}

void UART::send(const uint8_t data)
{
    send(&data, 1);
}

void UART::send(const char* message)
{
    send((const uint8_t*) message, strlen(message));
}

void UART::send(const uint8_t* data, size_t length)
{
    if (sending_m == false)
    {
        for (size_t i = 0; i < length; ++i)
        {
            UCA0TXBUF = data[i];
            while ((IFG2 & UCA0TXIFG) == 0)
                ;
        }
        // Writing to UCA0TXBUF clears the IT flag
        // Here we have to clear it manually because we won't write again to UCA0TXBUF
        IFG2 &= ~UCA0TXIFG;
    }
}

void UART::sendAsync(const char* message)
{
    sendAsync((const uint8_t*) message, strlen(message));
}

void UART::sendAsync(const uint8_t* data, size_t length)
{
    if (sending_m == false)
    {
        sending_m = true;

        data_m = data;
        length_m = length;
        count_m = 0;

        // Send first byte
        UCA0TXBUF = data_m[count_m];
        ++count_m;

        // Enable USCI_A0 TX interrupt
        UC0IE |= UCA0TXIE;

        // Remaining bytes will be sent by tx_isr()
    }
}

void UART::handleTxIsr()
{
    // Send next byte
    UCA0TXBUF = data_m[count_m];
    ++count_m;

    // Disable USCI_A0 TX interrupt if all data sent
    if (count_m >= length_m)
    {
        UC0IE &= ~UCA0TXIE;
        sending_m = false;
    }
}

UART::UART() :
        data_m(nullptr),
        length_m(0),
        count_m(0),
        sending_m(false)
{
    // TI's documentation:  slau144j
    // section15.3.1

    // Configure UART
    // The baudrate configuration depends on the previous clock configuration
    // FIXME get clock freq to adjust baudrate
    // Note: since UART instance is created statically at global scope, then system clock has not been set in main

    // TODO verify this code taken from https://www.embeddedrelated.com/showarticle/420.php
    P1SEL |= UART_RX_BIT + UART_TX_BIT; // P1.1 = RXD, P1.2=TXD
    P1SEL2 |= UART_RX_BIT + UART_TX_BIT; // P1.1 = RXD, P1.2=TXD

    // When MCU resets, UCSWRST is set, keeping USCI in reset condition (slau144j 15.3.1)

    UCA0CTL1 |= UCSSEL_2; // SMCLK
    UCA0BR0 = 0x08; // 1MHz 115200
    UCA0BR1 = 0x00; // 1MHz 115200
    UCA0MCTL = UCBRS2 + UCBRS0; // Modulation UCBRSx = 5

    // Release USCI_A0 for operation
    UCA0CTL1 &= ~UCSWRST;

    // Enable USCI_A0 RX interrupt (slau144j 15.3.1)
    //UC0IE |= UCA0RXIE;

    // Disable USCI_A0 TX interrupt
    //UC0IE &= ~UCA0TXIE;
}

void __interrupt_vec(USCIAB0TX_VECTOR) UART0_TX_ISR(void)
{
    UART::Uart0.handleTxIsr();
}

void __interrupt_vec(USCIAB0RX_VECTOR) USCI0RX_ISR(void)
{
//    P1OUT |= LED_RED_BIT;
//    if (UCA0RXBUF == 'a') // 'a' received?
//    {
//        i = 0;
//        UC0IE |= UCA0TXIE; // Enable USCI_A0 TX interrupt
//        UCA0TXBUF = string[i++];
//    }
//    P1OUT &= ~LED_RED_BIT;

    // Read UCA0RXBUF clears the interrupt flag. see receive()
}
