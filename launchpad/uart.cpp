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
    // When MCU resets, UCSWRST is set, keeping USCI in reset condition (see slau144j section 15.3.1)

    // TODO verify this code taken from https://www.embeddedrelated.com/showarticle/420.php
    P1SEL |= UART_RX_BIT + UART_TX_BIT; // P1.1 = RXD, P1.2=TXD
    P1SEL2 |= UART_RX_BIT + UART_TX_BIT; // P1.1 = RXD, P1.2=TXD

    // Select SMCLK as clock source
    UCA0CTL1 |= UCSSEL_2;
    // FIXME clock is assumed to be 1 MHz in setBaudrate()

    // Release USCI_A0 for operation
    UCA0CTL1 &= ~UCSWRST;

    // Enable USCI_A0 RX interrupt
    //UC0IE |= UCA0RXIE;

    // Disable USCI_A0 TX interrupt
    //UC0IE &= ~UCA0TXIE;

    setBaudrate(Baudrate::_115200);
}

void UART::setBaudrate(Baudrate baudrate)
{
    /*
     * From slau144J
     *
     *  15.3.10 Setting a Baud Rate
     * For a given BRCLK clock source, the baud rate used determines the required division factor N:
     * N= f_BRCLK / Baud rate
     *
     *  15.3.10.1 Low-Frequency Baud Rate Mode Setting
     * In the low-frequency mode, the integer portion of the divisor is realized by the prescaler:
     * UCBRx = INT(N)
     * and the fractional portion is realized by the modulator with the following nominal formula:
     * UCBRSx = round( ( N – INT(N) ) × 8 )
     *
     *  15.4.4 UCAxBR1, USCI_Ax Baud Rate Control Register 1
     * The 16-bit value of (UCAxBR0 + UCAxBR1 × 256) forms the prescaler value.
     */

    switch (baudrate)
    {
    // FIXME We assume that SMCLK is 1 MHz
    case Baudrate::_9600:
        // N = 104.2, UCBRSx = 1
        UCA0BR0 = 104;
        UCA0BR1 = 0;
        UCA0MCTL = UCBRS0;
        break;

    case Baudrate::_19200:
        // N = 52.08, UCBRSx = 1
        UCA0BR0 = 52;
        UCA0BR1 = 0;
        UCA0MCTL = UCBRS0;
        break;

    case Baudrate::_38400:
        // N = 26.04, UCBRSx = 0
        UCA0BR0 = 26;
        UCA0BR1 = 0;
        UCA0MCTL = 0;
        break;

    case Baudrate::_57600:
        // N = 17.36, UCBRSx = 3
        UCA0BR0 = 17;
        UCA0BR1 = 0;
        UCA0MCTL = UCBRS1 + UCBRS0;
        break;

    case Baudrate::_115200:
        // N = 8.68, UCBRSx = 5
        UCA0BR0 = 8;
        UCA0BR1 = 0;
        UCA0MCTL = UCBRS2 + UCBRS0;
        break;

    default:
        break;
    }
}

void __interrupt_vec(USCIAB0TX_VECTOR)
UART0_TX_ISR(void)
{
    UART::Uart0.handleTxIsr();
}

void __interrupt_vec(USCIAB0RX_VECTOR)
USCI0RX_ISR(void)
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
