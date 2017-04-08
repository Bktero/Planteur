#include <cstdint>

#include "system.hpp"
#include "uart.hpp"

#define ARRAY_LENGTH(array)    (sizeof array / sizeof array[0])

enum
    : uint8_t
    {
        GATEWAY_UID = 0, LAUNCHPAD_UID = 1, PLANT_FRAME_TYPE = 1, PLANT_FRAME_PAYLOAD_LENGTH = 2
};

static uint8_t valid_no_watering[] =
    { GATEWAY_UID, LAUNCHPAD_UID, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 70, 30 };

static uint8_t valid_watering_humidity[] =
    { GATEWAY_UID, LAUNCHPAD_UID, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 49, 24 };

static uint8_t valid_watering_humidity_temperature[] =
    { GATEWAY_UID, LAUNCHPAD_UID, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 55, 25 };

static uint8_t invalid_bad_dest[] = { 42, LAUNCHPAD_UID, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 12, 24 };
static uint8_t invalid_bad_source[] = { GATEWAY_UID, 42, PLANT_FRAME_TYPE, PLANT_FRAME_PAYLOAD_LENGTH, 52, 26 };
static uint8_t invalid_bad_type[] = { GATEWAY_UID, LAUNCHPAD_UID, 42, PLANT_FRAME_PAYLOAD_LENGTH, 66, 33 };

#define send(x) do{\
                UART::Uart0.send(x, ARRAY_LENGTH(x));\
                Delay::millis(200);\
                } while(0)

int main()
{
    Launchpad::init();

    // Configure baudrate to 9600 (default for XBee modules)
    UART::Uart0.setBaudrate(UART::Baudrate::_9600);

    // Send valid frames
    send(valid_no_watering);
    send(valid_watering_humidity);
    send(valid_watering_humidity_temperature);

    // Send invalid frames
    send(invalid_bad_dest);
    send(invalid_bad_source);
    send(invalid_bad_type);
}
