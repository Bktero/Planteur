cmake_minimum_required(VERSION 3.5)

project(launchpad-msp430)

# Adjust compiler and linker flags
# -mmcu=msp430g2231 ou # -mmcu=msp430g2553
set(MSP430G2231_COMPILER_FLAGS "-mmcu=msp430g2553 -Wall -Wextra -O0 -g -std=c++11")

set(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} ${MSP430G2231_COMPILER_FLAGS})
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${MSP430G2231_COMPILER_FLAGS})

set(MSP430G2231_LINKER_FLAGS "-L/usr/msp430/include/")
set(CMAKE_EXE_LINKER_FLAGS ${CMAKE_EXE_LINKER_FLAGS} ${MSP430G2231_LINKER_FLAGS})

# Create executable
add_executable(a.out
				delay.hpp
				led.cpp led.hpp
				main.cpp
				uart.cpp uart.hpp)

# Add a post-build action to print the size of the executable
add_custom_command(TARGET a.out POST_BUILD COMMAND msp430-elf-size a.out)
                   
# Add a target program the board with the executable
add_custom_target(program
				COMMAND mspdebug rf2500 prog\ a.out
				DEPENDS a.out)