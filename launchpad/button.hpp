#ifndef BUTTON_HPP
#define BUTTON_HPP

#include <msp430.h>

typedef void (*ButtonCallback)(void);

class Button
{
public:
    static Button unique;

    void setCallback(ButtonCallback handler);

    friend void PORT1_ISR();

protected:
    void handleIsr();

private:
    enum
    {
        BUTTON_BIT = BIT3
    };

    ButtonCallback handler_m;

    Button();
};

#endif
