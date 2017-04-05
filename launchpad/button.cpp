#include "button.hpp"

Button Button::unique;

Button::Button() :
    handler_m(nullptr)
{
    // Enable interrupt for button and clear flag
    P1IE |= BUTTON_BIT;
    P1IFG &= ~BUTTON_BIT;
}

void Button::setCallback(ButtonCallback handler)
{
    handler_m = handler;
}

void Button::handleIsr()
{
    if(handler_m != nullptr)
    {
        handler_m();
    }
}

void __interrupt_vec(PORT1_VECTOR) PORT1_ISR(void)
{
    // Ask button to handler its ISR
    Button::unique.handleIsr();

    // Clear interrupt flag
    P1IFG &= ~Button::BUTTON_BIT;
}
