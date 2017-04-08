#include <cstdint>

#include "button.hpp"
#include "led.hpp"
#include "uart.hpp"

#define ARRAY_LENGTH(array)    (sizeof array / sizeof array[0])

enum
    : uint8_t
    {
        GATEWAY_UID = 0, LAUNCHPAD_UID = 1, PLANT_FRAME_TYPE = 1
};

static uint8_t data[] =
    { GATEWAY_UID, LAUNCHPAD_UID, PLANT_FRAME_TYPE, 2 /*Payload length*/, 55/*Humidity*/, 24 /*Temperature*/};

static void button_handler()
{
    LED::Red.on();
    UART::Uart0.send(data, ARRAY_LENGTH(data));
    LED::Red.off();
}

void xbee()
{
    UART::Uart0.setBaudrate(UART::Baudrate::_9600);
    Button::unique.setCallback(button_handler);

    button_handler();
}
