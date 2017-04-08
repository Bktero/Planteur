#include "button.hpp"
#include "delay.hpp"
#include "led.hpp"
#include "uart.hpp"

static bool led_paused = true;

static void handle_button()
{
    // Change mode
    led_paused = !led_paused;

    // Send message through UART
    const uint8_t b = '0' + led_paused;
    UART::Uart0.send(b);
}

void demo()
{
    UART::Uart0.send("MSP430 starts");
    UART::Uart0.send('\n');

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
}
