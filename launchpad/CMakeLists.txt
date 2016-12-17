cmake_minimum_required(VERSION 3.5)

project(launchpad-msp430)

# Adjust compiler and linker flags
set(MSP430G2231_COMPILER_FLAGS "-mmcu=msp430g2231 -Wall -Wextra -O0 -g")

set(CMAKE_C_FLAGS ${CMAKE_C_FLAGS} ${MSP430G2231_COMPILER_FLAGS})
set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} ${MSP430G2231_COMPILER_FLAGS})

set(MSP430G2231_LINKER_FLAGS "-L/usr/msp430/include/")
set(CMAKE_EXE_LINKER_FLAGS ${CMAKE_EXE_LINKER_FLAGS} ${MSP430G2231_LINKER_FLAGS})

# Create executable
add_executable(a.out main.cpp)
