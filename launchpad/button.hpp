#ifndef BUTTON_HPP
#define BUTTON_HPP

#include <msp430.h>

/**
 * Abstraction over hardware buttons
 */
class Button
{
public:
    /**
     * The definition of the button callback function type.
     */
    typedef void (*ButtonCallback)(void);

    /**
     * The unique button of the Launchpad board.
     */
    static Button unique;

    /**
     * Set the callback function that will be called when the button is pressed.
     *
     * If you want the butto to have no action, simply set 'nullptr' as callback.
     *
     * @param callback the callback function
     */
    void setCallback(ButtonCallback callback);

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
