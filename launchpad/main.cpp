#include <msp430.h>

#include "button.hpp"
#include "delay.hpp"
#include "led.hpp"
#include "uart.hpp"

// TODO read https://indiantinker.wordpress.com/2012/12/13/tutorial-using-the-internal-temperature-sensor-on-a-msp430/

bool led_paused = true;

void handle_button()
{
    // Change mode
    led_paused = !led_paused;

    // Send message through UART
    const uint8_t b = '0' + led_paused;
    UART::Uart0.send(b);
}

int main(void)
{
    // Stop watchdog timer
    WDTCTL = WDTPW + WDTHOLD;

    // Configure clock to be 1 MHz
    // TODO verify this code taken from https://www.embeddedrelated.com/showarticle/420.php because TI's sample code do something else
    // Select lowest DCOx and MODx setting
    DCOCTL = 0;
    // Set DCO
    BCSCTL1 = CALBC1_1MHZ;
    DCOCTL = CALDCO_1MHZ;

    // Enable interrupts
    // The NOP avoids avoid a compiler's warning telling that a NOP might be needed before EINT
    __nop();
    __enable_interrupt();

    UART::Uart0.send("MSP430 starts");
    UART::Uart0.send('\n');

    // ============================================================
    // Infinite loops
    UART::Uart0.send("Send characters, the MSP430 will echo them\n");
    UART::Uart0.send("'z' will break the loop\n");

    while (1)
    {
        uint8_t data = UART::Uart0.receive();

        if (data == 'z')
        {
            LED::Red.off();
            break;
        }
        else
        {
            LED::Red.on();
        }

        UART::Uart0.send("Received: ");
        UART::Uart0.send(data);
        UART::Uart0.send((uint8_t) '\n');
    }

    UART::Uart0.sendAsync("Press the button so that the green LED blinks slowly\n");
    UART::Uart0.sendAsync("Press again to stop blinking\n");
    Button::unique.setCallback(handle_button);

    while (1)
    {
        if (!led_paused)
        {
            Delay::millis(500);
            LED::Green.toogle();
        }
    }

    while (1)
        ;
}

