#include <cstdint>

#include "system.hpp"
#include "uart.hpp"

#define ARRAY_LENGTH(array)    (sizeof array / sizeof array[0])

enum
    : uint8_t
    {
        GATEWAY_UID = 0, LAUNCHPAD_UID = 1, PLANT_FRAME_TYPE = 1, PLANT_FRAME_PAYLOAD_LENGTH = 2
};

static uint8_t nowatering[] = { GATEWAY_UID, LAUNCHPAD_UID, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 80, 20 };
static uint8_t humidity[] = { GATEWAY_UID, LAUNCHPAD_UID, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 40, 20 };

#define send(x) do{\
                UART::Uart0.send(x, ARRAY_LENGTH(x));\
                Delay::millis(1);\
                } while(0)

int main()
{
    Launchpad::init();

    // Configure baudrate to 9600 (default for XBee modules)
    UART::Uart0.setBaudrate(UART::Baudrate::_9600);

    // Send frames
    for (int i = 0; i < 2048; ++i)
    {
        send(nowatering);
        send(humidity);
    }
}
