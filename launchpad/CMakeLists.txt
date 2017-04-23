cmake_minimum_required(VERSION 3.5)

project(launchpad-msp430)

# Adjust compiler and linker flags
# -mmcu=msp430g2231 ou # -mmcu=msp430g2553
set(MSP430G2231_COMPILER_FLAGS "-mmcu=msp430g2553 -Wall -Wextra -O0 -g -std=c++11 -ffunction-sections -fdata-sections")

set(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} ${MSP430G2231_COMPILER_FLAGS})
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${MSP430G2231_COMPILER_FLAGS})

set(MSP430G2231_LINKER_FLAGS "-L/usr/msp430/include/ -Wl,-gc-sections")
set(CMAKE_EXE_LINKER_FLAGS ${CMAKE_EXE_LINKER_FLAGS} ${MSP430G2231_LINKER_FLAGS})


#-------------------------------------------------------
# Create target to erase the MCU's flash memory
add_custom_target(erase COMMAND mspdebug rf2500 erase)


#-------------------------------------------------------
# Create main executable
add_executable(a.out
				button.cpp button.hpp
				led.cpp led.hpp
				main.cpp
				system.hpp
				uart.cpp uart.hpp)

# Add a post-build action to print the size of the executable
add_custom_command(TARGET a.out POST_BUILD COMMAND msp430-elf-size a.out)
                   
# Add a target program the board with the executable
add_custom_target(program COMMAND mspdebug rf2500 prog\ a.out DEPENDS a.out)


#-------------------------------------------------------
# Create demo executables
add_executable(demo.out
				demo.cpp
				button.cpp button.hpp
				led.cpp led.hpp
				system.hpp
				uart.cpp uart.hpp)

add_custom_command(TARGET demo.out POST_BUILD COMMAND msp430-elf-size demo.out)

#-------------------------------------------------------
# Create test executables for XBee
add_executable(test_xbee.out test_xbee.cpp uart.cpp uart.hpp)

add_executable(test_xbee_intense.out test_xbee_intense.cpp uart.cpp uart.hpp)
